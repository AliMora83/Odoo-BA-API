# -*- coding: utf-8 -*-
from odoo import models, fields, api, Command, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class CrmLeadAutomation(models.Model):
    _inherit = "crm.lead"
    
    # Automation tracking fields
    auto_converted_to_opportunity = fields.Boolean(
        string="Auto-Converted to Opportunity",
        default=False,
        help="Technical field to track if this lead was auto-converted"
    )
    auto_invoice_created = fields.Boolean(
        string="Auto-Invoice Created", 
        default=False,
        help="Technical field to track if invoice was auto-created"
    )
    related_sale_order_id = fields.Many2one(
        'sale.order',
        string="Related Sales Order",
        readonly=True,
        help="Sales order created from opportunity"
    )
    related_invoice_ids = fields.Many2many(
        'account.move',
        string="Related Invoices",
        readonly=True,
        help="Invoices created from this lead"
    )

    def _cron_process_paid_leads(self):
        """Main cron: Find paid leads and convert to opportunity + invoice"""
        _logger.info("=== Starting Paid Lead Automation Process ===")
        
        paid_leads = self.search([
            ('ispaid', '=', True),
            ('auto_converted_to_opportunity', '=', False),
            ('active', '=', True)
        ], limit=50)
        
        _logger.info(f"Found {len(paid_leads)} paid leads to process")
        
        success_count = 0
        for lead in paid_leads:
            try:
                lead._process_paid_lead_workflow()
                success_count += 1
                _logger.info(f"✓ Processed lead: {lead.name} (ID: {lead.id})")
            except Exception as e:
                _logger.error(f"✗ Failed lead {lead.name} (ID: {lead.id}): {str(e)}")
                continue
        
        _logger.info(f"=== Completed: {success_count}/{len(paid_leads)} leads processed ===")
        return True

    def _process_paid_lead_workflow(self):
        """Complete workflow: Lead → Opportunity → Sales Order → Invoice + Payment"""
        self.ensure_one()
        _logger.info(f"🚀 Processing workflow for: {self.name}")
        
        # Step 1: Convert to Opportunity
        opportunity = self._convert_to_opportunity_auto()
        
        # Step 2: Create Sales Order
        sale_order = opportunity._create_sale_order_from_opportunity()
        
        # Step 3: Confirm Sales Order
        sale_order.action_confirm()
        _logger.info(f"📦 Sales Order {sale_order.name} confirmed")
        
        # Step 4: Create Invoice
        invoices = sale_order._create_invoices(final=True)
        if not invoices:
            raise UserError("Failed to create invoice from sales order")
        invoice = invoices[0]
        
        # Step 5: Post Invoice
        invoice.action_post()
        _logger.info(f"📄 Invoice {invoice.name} posted")

        # Step 6: Register Payment (Since it was paid on the website)
        self._register_payment_for_invoice(invoice)
        
        # Mark as processed
        self.write({
            'auto_converted_to_opportunity': True,
            'auto_invoice_created': True,
            'related_sale_order_id': sale_order.id,
            'related_invoice_ids': [Command.set([invoice.id])]
        })
        
        # Chatter notification
        self.message_post(
            body=_("""
                <div style="background:#f0f9ff;border-left:4px solid #0ea5e9;padding:12px;margin:8px 0;">
                    <h3 style="color:#0369a1;margin:0 0 8px 0;">🤖 Automated Workflow Complete</h3>
                    <p style="margin:4px 0;"><b>Status:</b> Paid lead automatically processed and invoice marked as paid.</p>
                    <p style="margin:4px 0;"><b>Opportunity:</b> %(opp)s</p>
                    <p style="margin:4px 0;"><b>Sales Order:</b> %(so)s</p>
                    <p style="margin:4px 0;"><b>Invoice:</b> %(inv)s</p>
                    <p style="margin:4px 0;"><b>Amount:</b> %(amt)s</p>
                </div>
            """) % {
                'opp': opportunity.name,
                'so': sale_order.name,
                'inv': invoice.name,
                'amt': f"{invoice.currency_id.symbol}{invoice.amount_total:,.2f}"
            },
            message_type='notification',
            subtype_xmlid='mail.mt_note'
        )
        
        return True

    def _register_payment_for_invoice(self, invoice):
        """Register a payment for the $1 lead fee invoice."""
        self.ensure_one()
        # Find a suitable journal (usually Bank or Cash)
        journal = self.env['account.journal'].search([('type', 'in', ('bank', 'cash'))], limit=1)
        if not journal:
            _logger.warning("No bank/cash journal found to register payment")
            return False
            
        payment = self.env['account.payment.register'].with_context(
            active_model='account.move',
            active_ids=invoice.ids
        ).create({
            'journal_id': journal.id,
            'payment_date': fields.Date.context_today(self),
        })._create_payments()
        
        _logger.info(f"💰 Payment registered for invoice {invoice.name}")
        return payment

    def _convert_to_opportunity_auto(self):
        """Convert lead to opportunity programmatically"""
        self.ensure_one()
        if self.type == 'opportunity':
            self.auto_converted_to_opportunity = True
            return self
            
        vals = {
            'type': 'opportunity',
            'date_conversion': fields.Datetime.now(),
            'probability': 100,
        }
        
        if not self.partner_id:
            partner_name = self.contact_name or self.name
            partner = self.env['res.partner'].search([
                ('name', '=', partner_name),
                ('email', '=', self.email_from)
            ], limit=1)
            
            if not partner:
                partner_vals = {
                    'name': partner_name,
                    'email': self.email_from,
                    'phone': self.phone,
                    'street': self.street,
                    'city': self.city,
                    'zip': self.zip,
                    'country_id': self.country_id.id if self.country_id else False,
                    'type': 'contact',
                }
                partner = self.env['res.partner'].create(partner_vals)
            vals['partner_id'] = partner.id
            
        self.write(vals)
        return self

    def _create_sale_order_from_opportunity(self):
        """Create Sales Order from opportunity"""
        self.ensure_one()
        product = self._get_or_create_service_product()
        
        order_vals = {
            'partner_id': self.partner_id.id,
            'opportunity_id': self.id,
            'origin': f"Opportunity: {self.name}",
            'note': f"Auto-created lead fee from Bridging Africa.
Quote ID: {self.quote_id or 'N/A'}",
            'order_line': [(0, 0, {
                'product_id': product.id,
                'name': f"Lead Fee - {self.service_id.name or 'Service'} - Job #{self.quote_id}",
                'product_uom_qty': 1,
                'price_unit': 1.0,
                'tax_id': [(6, 0, 
            })],
        }
        
        return self.env['sale.order'].create(order_vals)

    def _get_or_create_service_product(self):
        """Get or create lead fee service product"""
        product_obj = self.env['product.product']
        product = product_obj.search([
            ('default_code', '=', 'BA-LEAD-FEE'),
            ('type', '=', 'service')
        ], limit=1)
        
        if product:
            return product
            
        default_tax = self.env['account.tax'].search([
            ('type_tax_use', '=', 'sale'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        
        product_vals = {
            'name': 'Bridging Africa Lead Fee',
            'type': 'service',
            'list_price': 1.0,
            'default_code': 'BA-LEAD-FEE',
            'invoice_policy': 'order',
            'taxes_id': [(6, 0, default_tax.ids)] if default_tax else False,
        }
        
        return product_obj.create(product_vals)
