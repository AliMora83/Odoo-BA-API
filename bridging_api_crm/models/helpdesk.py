# -*- coding: utf-8 -*-
import requests
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    ba_query_id = fields.Integer(string="BA Query ID", help="Unique ID from Bridging Africa API")

    @api.model
    def _cron_api_helpdesk_queries(self):
        \"\"\"Cron to fetch queries from Bridging Africa API and create tickets\"\"\"
        url = "https://bridging-africa.com/api/odooapi/GetCustomerQueries"
        _logger.info("Fetching Helpdesk Queries from Bridging Africa: %s", url)

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            queries = response.json()
        except Exception as e:
            _logger.error("Error fetching Helpdesk Queries: %s", str(e))
            return False

        if not isinstance(queries, list):
            _logger.error("API did not return a list of queries")
            return False

        ticket_obj = self.env['helpdesk.ticket']
        new_count = 0

        for query in queries:
            query_id = query.get('Id')
            if not query_id:
                continue

            # Check if ticket already exists
            existing_ticket = ticket_obj.search([('ba_query_id', '=', query_id)], limit=1)
            if existing_ticket:
                continue

            # Create new ticket
            vals = {
                'name': _("Inquiry from %s") % query.get('CustomerName', 'Unknown'),
                'partner_name': query.get('CustomerName'),
                'partner_email': query.get('Email'),
                'description': query.get('Issue'),
                'ba_query_id': query_id,
            }
            
            ticket_obj.create(vals)
            new_count += 1

        _logger.info("Created %d new Helpdesk tickets from Bridging Africa", new_count)
        return True
