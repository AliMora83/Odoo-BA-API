{
    "name": "API : CRM : Script",
    "version": "19.0.0.1",
    "category": "Software Development",
    "summary": """Bridging Africa : CRM API Script""",
    "description": "Connects all CRM API requests",
    "author": "Digital Information Solutions",
    "website": "bridging-africa.odoo.com",
    "company": "Sesani Group",
    "license": "AGPL-3",
    "sequence": 1,
    "depends": [
        "base",
        "crm",
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/crm_lead.xml",
    ],
    "installable": True,
    "application": False,
}
