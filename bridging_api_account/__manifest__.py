{
    "name": "API : Accounting : Script",
    "version": "19.0.0.1",
    "category": "Accounting",
    "summary": "Bridging Africa : Accounting / Invoice API Script",
    "description": "Connects all Accounting / Invoice API requests",
    "author": "Digital Information Solutions",
    "website": "bridging-africa.odoo.com",
    "company": "Sesani Group",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
    ],
    "data": [
        "data/ir_cron_data.xml",
        "security/ir.model.access.csv",
        "views/account_move_view.xml",
    ],
    "installable": True,
    "application": False,
}
