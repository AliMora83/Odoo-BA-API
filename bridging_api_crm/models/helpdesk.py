# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class BaHelpdeskQuery(models.Model):
    _name = 'ba.helpdesk.query'
    _description = 'Bridging Africa Helpdesk Query'
    _order = 'create_date desc'

    name = fields.Char(string='Query Reference', required=True, default='New')
    ba_query_id = fields.Integer(string='BA Query ID', help='Unique ID from Bridging Africa API')
    customer_name = fields.Char(string='Customer Name')
    customer_email = fields.Char(string='Customer Email')
    description = fields.Text(string='Query Description')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='new')
    create_date = fields.Datetime(string='Created On', readonly=True)

    @api.model
    def _cron_api_helpdesk_queries(self):
        """Cron to fetch queries from Bridging Africa API.
        Endpoint not yet implemented - stubbed for future use."""
        _logger.info(
            'BA Helpdesk cron: GetCustomerQueries endpoint not yet '
            'implemented on bridging-africa.com. Skipping.'
        )
        return True
