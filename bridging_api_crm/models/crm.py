# -*- coding: utf-8 -*-
import logging
import requests
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class ServiceService(models.Model):
    _name = "service.service"
    _description = "Service Type" 
    name = fields.Char("Name")

class CrmLead(models.Model):
    _inherit = "crm.lead"

    quote_id = fields.Integer("Quote ID")
    provider_id = fields.Char("Provider ID")
    ispaid = fields.Boolean("IsPaid")
    workerrrgency = fields.Char("WorkerUrgency")
    q_status_id = fields.Char("StatusID")
    service_id = fields.Many2one("service.service", string="Service Name")

    @api.model
    def _cron_api_crm_services(self):
        """Fetch leads from Bridging Africa API and create or update them in Odoo."""
        URL = "https://bridging-africa.com/api/odooapi/GetAllRequests"
        _logger.info("=== Starting CRM Lead Sync from API ===")
        
        try:
            req = requests.get(URL, timeout=30)
            if req.status_code != 200:
                _logger.error(f"API Error: {req.status_code}")
                return False
            
            json_data = req.json()
            sections = ["completed", "pending"]
            sync_count = 0
            
            for section in sections:
                leads_data = json_data.get(section, [])
                for data in leads_data:
                    if self._create_or_update_lead_from_data(data):
                        sync_count += 1
            
            _logger.info(f"=== CRM Lead Sync Completed: {sync_count} leads processed ===")
            return True
            
        except Exception as e:
            _logger.error(f"CRM Sync Exception: {str(e)}")
            return False

    def _create_or_update_lead_from_data(self, data):
       
        quote_id = data.get("Id")
            
        existing_lead = self.search([("quote_id", "=", quote_id)], limit=1)
        
        service_name = data.get("ServiceName")
        service = self.env["service.service"].search([("name", "=", service_name)], limit=1)
        if not service and service_name:
            service = self.env["service.service"].create({"name": service_name})
            
        vals = {
            "quote_id": quote_id,
            "provider_id": data.get("ProviderID"),
            "contact_name": data.get("Tradesperson"),
            "workerrrgency": data.get("WorkerUrgency"),
            "ispaid": data.get("IsPaid"),
            "q_status_id": data.get("StatusID"),
            "name": f"Job #{quote_id} - {service_name or 'Request'}",
            "partner_name": data.get("Customer"),
            "description": data.get("JobDetail"),
            "service_id": service.id if service else False,
        }
        
        if existing_lead:
            existing_lead.write(vals)
            return True
        else:
            self.create(vals)
            return True
