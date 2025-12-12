{
    "name": "API : CRM : Script",
    "version": "19.0.0.1",
    "category": "",
    "summary": """Bridging Africa : CRM API Script""",
    "description": "Bridging Africa",
    "author": "Digital Information Solutions",
    "website": "bridging-africa.com",
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
