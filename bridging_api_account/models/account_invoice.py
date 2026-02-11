# -*- coding: utf-8 -*-
import logging
import requests

from odoo import api, fields, models, Command

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    ba_invoice_id = fields.Char(
        string="Bridging Africa Invoice ID",
        index=True,
        help="External invoice identifier used for synchronization.",
    )
    ba_status = fields.Char(
        string="BA Status",
        help="Status from Bridging Africa (e.g. Draft, Posted, Paid).",
    )
    ba_synced = fields.Boolean(
        string="Synced from Bridging Africa",
        readonly=True,
    )

    @api.model
    def _get_ba_api_url(self):
        """Get API URL from system parameters."""
        ir_config = self.env["ir.config_parameter"].sudo()
        return ir_config.get_param(
            "bridging_africa.invoice_api_url",
            default="https://bridgingafrica.ncnsoftware.com/api/odooapi/GetAllInvoices",
        )

    @api.model
    def _cron_api_account_invoices(self):
        """Cron job to sync invoices from Bridging Africa."""
        url = self._get_ba_api_url()
        _logger.info("Bridging Africa invoice sync started. URL: %s", url)

        try:
            response = requests.get(url, timeout=30)
        except Exception as e:
            _logger.exception("Error connecting to Bridging Africa Invoice API: %s", e)
            return

        if response.status_code != 200:
            _logger.error(
                "Bridging Africa Invoice API returned %s: %s",
                response.status_code,
                response.text,
            )
            return

        try:
            json_data = response.json()
        except ValueError:
            _logger.error("Invalid JSON response from Bridging Africa Invoice API")
            return

        # Expect something like: {"invoices": [...]} – adjust to actual payload
        invoices = json_data.get("invoices", []) or []
        _logger.info("Bridging Africa: received %s invoices", len(invoices))

        for data in invoices:
            self._create_or_update_invoice_from_ba(data)

        _logger.info("Bridging Africa invoice sync completed.")

    def _create_or_update_invoice_from_ba(self, data):
        """Create or update a single invoice using BA data dict."""
        Move = self.env["account.move"].sudo()

        external_id = str(data.get("Id") or "")
        if not external_id:
            _logger.warning("Skipping invoice with no Id in payload: %s", data)
            return

        # Find or create partner
        partner = self._get_or_create_partner_from_ba(data)

        # Map basic invoice fields – adapt names to your payload
        move_values = {
            "move_type": "out_invoice",  # customer invoice
            "partner_id": partner.id,
            "invoice_date": data.get("InvoiceDate") or fields.Date.context_today(self),
            "invoice_date_due": data.get("DueDate") or False,
            "currency_id": self._get_currency_from_ba(data).id,
            "ba_invoice_id": external_id,
            "ba_status": data.get("Status") or "",
            "ba_synced": True,
            "invoice_line_ids": self._prepare_invoice_lines_from_ba(data),
        }

        existing_move = Move.search(
            [("ba_invoice_id", "=", external_id)], limit=1
        )

        if existing_move:
            _logger.info("Updating existing BA invoice %s (move %s)", external_id, existing_move.id)
            existing_move.write(move_values)
            move = existing_move
        else:
            _logger.info("Creating new BA invoice %s", external_id)
            move = Move.create(move_values)

        # Optionally post invoice if BA status = Paid/Posted
        status = (data.get("Status") or "").lower()
        if status in ("posted", "paid") and move.state == "draft":
            try:
                move.action_post()
            except Exception as e:
                _logger.exception(
                    "Failed to post invoice %s for BA invoice %s: %s",
                    move.id, external_id, e
                )

    def _get_or_create_partner_from_ba(self, data):
        """Map customer from BA data to res.partner."""
        Partner = self.env["res.partner"].sudo()

        name = data.get("CustomerName") or "BA Customer"
        email = data.get("CustomerEmail")
        vat = data.get("CustomerVAT")

        domain = []
        if email:
            domain = [("email", "=", email)]
        elif vat:
            domain = [("vat", "=", vat)]

        partner = Partner.search(domain, limit=1) if domain else False

        if not partner:
            partner_vals = {
                "name": name,
                "email": email,
                "vat": vat,
                "street": data.get("CustomerAddress"),
                "phone": data.get("CustomerPhone"),
            }
            partner = Partner.create(partner_vals)

        return partner

    def _get_currency_from_ba(self, data):
        Currency = self.env["res.currency"].sudo()
        code = data.get("Currency") or self.env.company.currency_id.name
        currency = Currency.search([("name", "=", code)], limit=1)
        if not currency:
            currency = self.env.company.currency_id
        return currency

    def _prepare_invoice_lines_from_ba(self, data):
        """Return Command list for invoice_line_ids based on BA payload."""
        Product = self.env["product.product"].sudo()

        lines_data = data.get("Lines", []) or []

        commands = []
        for line in lines_data:
            product = False
            default_code = line.get("ProductCode")
            name = line.get("Description") or "BA Line"

            if default_code:
                product = Product.search(
                    [("default_code", "=", default_code)], limit=1
                )
            if not product:
                product = Product.search([("name", "=", name)], limit=1)

            if not product:
                product = Product.create(
                    {
                        "name": name,
                        "default_code": default_code,
                        "list_price": line.get("UnitPrice") or 0.0,
                    }
                )

            quantity = line.get("Quantity") or 1.0
            price_unit = line.get("UnitPrice") or 0.0
            tax_ids = self._map_taxes_from_ba(line)

            commands.append(
                Command.create(
                    {
                        "product_id": product.id,
                        "name": name,
                        "quantity": quantity,
                        "price_unit": price_unit,
                        "tax_ids": tax_ids,
                    }
                )
            )

        return commands

    def _map_taxes_from_ba(self, line):
        """Map BA tax fields to account.tax records; adjust to your data."""
        Tax = self.env["account.tax"].sudo()
        tax_code = line.get("TaxCode")
        if not tax_code:
            return []

        tax = Tax.search(
            [("name", "=", tax_code)], limit=1
        )
        return [Command.link(tax.id)] if tax else []
