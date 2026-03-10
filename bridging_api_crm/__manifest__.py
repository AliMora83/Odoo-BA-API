{
    "name": "API : CRM : Script",
    "version": "19.0.1.3a",
    "category": "CRM",
    "summary": """Sync Bridging Africa jobs to Odoo CRM + Auto-invoice workflow""",
    "description": """
Bridging Africa API Integration with Full Automation
====================================================

Features:
---------
1. **API Sync**: Sync external jobs to CRM leads every 10 minutes
2. **Payment Tracking**: Real-time IsPaid status from Bridging Africa
3. **AUTOMATIC WORKFLOW** (NEW):
   - Paid leads auto-convert to opportunities (100% probability)
   - Auto-create and confirm sales orders
   - Auto-generate and post customer invoices
   - Links all related documents for easy tracking

Cron Jobs:
----------
- API Sync: Every 10 minutes
- Paid Lead Processing: Every 15 minutes

Manual Actions:
---------------
- "⚡ Process Paid Lead Now" button for immediate processing
- Bulk processing available in list view

UI Enhancements:
----------------
- Visual automation status indicators
- Related Sales Order and Invoice links on lead form
- Custom filters: "Paid - Pending Automation", "Auto-Processed"

Safety Features:
----------------
- Duplicate prevention flags
- Batch processing (max 50 per run)
- Individual error handling per lead
- Comprehensive audit logging
    """,
    "author": "Digital Information Solutions",
    "website": "bridging-africa.com",
    "company": "Sesani Group",
    "license": "AGPL-3",
    "sequence": 1,
    "depends": [
        "base",
        "crm",
        "sale",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "data/automation_cron.xml",
        "data/server_actions.xml",
        "views/crm_lead.xml",
        "views/crm_automation_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
