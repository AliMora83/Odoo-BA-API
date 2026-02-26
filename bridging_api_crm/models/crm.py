# -*- coding: utf-8 -*-
import logging
import time
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, Command
import requests


class ServiceService(models.Model):
    _name = "service.service"

    name = fields.Char("Name")


class CrmLead(models.Model):
    _inherit = "crm.lead"

    quote_id = fields.Integer(
        "Quote ID",
    )
    provider_id = fields.Char(
        "Provider ID",
    )
    ispaid = fields.Boolean(
        "IsPaid",
    )
    workerrrgency = fields.Char(
        "WorkerUrgency",
    )
    q_status_id = fields.Char(
        "StatusID",
    )
    service_id = fields.Many2one(
        "service.service",
        string="Service Name",
    )

    @api.model
    def _cron_api_crm_services(self):
        URL = "https://bridging-africa.com/api/odooapi/GetAllRequests"
        Req = requests.get(URL)
        print(
            "ReqReq",
            Req.json(),
            Req.status_code,
            type(Req.status_code),
        )
        LeadObj = self.env["crm.lead"]
        if Req.status_code == 200:
            print("-------")
            json_data = Req.json()
            print("json_datajson_datajson_data", json_data)
            
            # Process completed requests
            for data in json_data.get("completed", []):
                existing_lead = LeadObj.search(
                    [("quote_id", "=", data.get("Id"))],
                    limit=1
                )
                if not existing_lead:
                    ServiceName = data.get("ServiceName")
                    service_id = self.env["service.service"].search(
                        [("name", "=", ServiceName)]
                    )
                    if not service_id:
                        service_id = self.env["service.service"].create(
                            {"name": ServiceName}
                        )
                    LeadObj.create(
                        {
                            "quote_id": data.get("Id"),
                            "provider_id": data.get("ProviderID"),
                            "contact_name": data.get("Tradesperson"),
                            "workerrrgency": data.get("Id"),
                            "ispaid": data.get("IsPaid"),
                            "q_status_id": data.get("StatusID"),
                            "name": data.get("WorkerUrgency"),
                            "partner_name": data.get("Customer"),
                            "description": data.get("JobDetail"),
                            "service_id": service_id.id,
                        }
                    )
                else:
                    api_is_paid = data.get("IsPaid")
                    if existing_lead.ispaid != api_is_paid:
                        existing_lead.write({"ispaid": api_is_paid})
            
            # Process pending requests
            for data in json_data.get("pending", []):
                existing_lead = LeadObj.search(
                    [("quote_id", "=", data.get("Id"))],
                    limit=1
                )
                if not existing_lead:
                    ServiceName = data.get("ServiceName")
                    service_id = self.env["service.service"].search(
                        [("name", "=", ServiceName)]
                    )
                    if not service_id:
                        service_id = self.env["service.service"].create(
                            {"name": ServiceName}
                        )
                    LeadObj.create(
                        {
                            "quote_id": data.get("Id"),
                            "provider_id": data.get("ProviderID"),
                            "contact_name": data.get("Tradesperson"),
                            "workerrrgency": data.get("Id"),
                            "ispaid": data.get("IsPaid"),
                            "q_status_id": data.get("StatusID"),
                            "name": data.get("WorkerUrgency"),
                            "partner_name": data.get("Customer"),
                            "description": data.get("JobDetail"),
                            "service_id": service_id.id,
                        }
                    )
                else:
                    api_is_paid = data.get("IsPaid")
                    if existing_lead.ispaid != api_is_paid:
                        existing_lead.write({"ispaid": api_is_paid})
