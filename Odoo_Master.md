# Bridging Africa Odoo API Integration - Master Documentation
**Project:** Odoo-BA-API
**Repository:** https://github.com/AliMora83/Odoo-BA-API
**Odoo.sh Instance:** bridging-africa-sh
**Author:** Digital Information Solutions
**Created:** December 2025
**Last Updated:** March 24, 2026
---
## 🎯 Project Overview
This project integrates the **Bridging Africa** external service request platform with **Odoo 19 CRM** and **Helpdesk**. It automatically synchronizes service requests (jobs) from the external API into Odoo CRM leads and customer queries into Helpdesk tickets.

### Key Features
- ✅ Automatic sync of completed and pending jobs to CRM Leads
- ✅ Payment status tracking (`IsPaid` checkbox) with auto-conversion workflow
- ✅ **NEW:** Helpdesk Integration for customer query synchronization
- ✅ Automatic workflow: Paid Lead → Opportunity → Sales Order → Invoice
- ✅ Service type auto-creation
- ✅ Duplicate prevention by unique IDs (Quote ID and Query ID)
- ✅ Scheduled cron jobs (CRM: 10m, Automation: 15m, Helpdesk: 30m)
---
## 🏗️ Tech Stack
| Component | Technology |
|-----------|------------|
| **ERP Platform** | Odoo 19.0 (Enterprise/Community) |
| **Cloud Hosting** | Odoo.sh (bridging-africa-sh) |
| **Language** | Python 3.11+ |
| **Database** | PostgreSQL |
| **External API** | Bridging Africa (https://bridging-africa.com/) |
| **Version Control** | GitHub → Odoo.sh integration |
---
## 📁 File Structure
```
Odoo-BA-API/
├── bridging_api_crm/ # Main CRM and API module (ACTIVE)
│   ├── data/
│   │   ├── automation_cron.xml # Paid lead processing
│   │   ├── data.xml # CRM sync cron
│   │   ├── helpdesk_cron.xml # Helpdesk sync cron
│   │   └── server_actions.xml # Manual automation triggers
│   ├── models/
│   │   ├── crm.py # CRM sync logic
│   │   ├── crm_automation.py # Lead -> Invoice workflow
│   │   ├── helpdesk.py # Helpdesk ticket sync
│   │   └── __init__.py
│   ├── security/
│   │   └── ir.model.access.csv
│   ├── views/
│   │   ├── crm_automation_views.xml # Automation UI
│   │   ├── crm_lead.xml # CRM UI extensions
│   │   └── helpdesk_ticket_views.xml # Helpdesk UI extensions
│   ├── __init__.py
│   └── __manifest__.py
├── website_custom/ # Website customizations
├── README.md
└── .gitignore
```
DELETED MODULES (do not recreate):
- `bridging_api_account` (Merged into automation workflow in CRM module)

---
## 🔧 Module: `bridging_api_crm`
### Models
#### 1. `crm.lead` (Extended)
Inherits `crm.lead` for API sync and automation.
- **Sync Method:** `_cron_api_crm_services()`
- **Automation Method:** `_cron_process_paid_leads()`

#### 2. `helpdesk.ticket` (Extended)
Inherits `helpdesk.ticket` for external query synchronization.
| Field | Type | API Source | Purpose |
|---|---|---|---|
| `ba_query_id` | Integer | `Id` | Unique identifier for deduplication |

- **Sync Method:** `_cron_api_helpdesk_queries()`
- **Endpoint:** `https://bridging-africa.com/api/odooapi/GetCustomerQueries`

---
## ⏰ Cron Job Configuration
| Job Name | Interval | Method |
|---|---|---|
| API: CRM web services | 10 Minutes | `model._cron_api_crm_services()` |
| BA: Auto-process Paid Leads | 15 Minutes | `model._cron_process_paid_leads()` |
| Bridging Africa: Fetch Helpdesk Queries | 30 Minutes | `model._cron_api_helpdesk_queries()` |

---
## 🚀 Deployment Workflow (Odoo.sh)
1. **Develop** on `main` branch.
2. **Test** by dragging to `19.0-staging`.
3. **Deploy** by dragging to `prod`.
4. **Version Bump** in `__manifest__.py` is required to trigger module update.

---
## 🔄 Recent Changes Log
| Date | Change | Commit |
|---|---|---|
| Mar 24, 2026 | Implemented Phase 3: Helpdesk Integration | `21da44f2` |
| Mar 24, 2026 | Added Helpdesk ticket sync model and views | `88bf40df` |
| Mar 24, 2026 | Finalized Lead -> Invoice automation workflow | `75ac695e` |
| Mar 2, 2026 | Deleted legacy account module and fixed IsPaid logic | `30c0f8cb` |

---
## 📝 To-Do / Next Steps
- [ ] **Phase 4: Accounting Refinement** - Optimize invoice layout and payment reconciliation.
- [ ] **Phase 5: Customer Portal** - Enhance the Bridging Africa customer experience in Odoo.
- [ ] **Testing:** Verify Helpdesk query sync in production environment.
- [ ] **Security:** Implement API key authentication for production endpoints.

**END OF MASTER DOCUMENTATION**
