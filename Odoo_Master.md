## 📋 Master.md - Bridging Africa Odoo Integration

```markdown
# Bridging Africa Odoo API Integration - Master Documentation

**Project:** Odoo-BA-API  
**Repository:** https://github.com/AliMora83/Odoo-BA-API  
**Odoo.sh Instance:** bridging-africa-sh  
**Author:** Digital Information Solutions  
**Created:** December 2025  
**Last Updated:** March 2, 2026  

---

## 🎯 Project Overview

This project integrates the **Bridging Africa** external service request platform with **Odoo 19 CRM**. It automatically synchronizes service requests (jobs) from the external API into Odoo CRM leads, including payment status tracking.

### Key Features
- ✅ Automatic sync of completed and pending jobs
- ✅ Payment status tracking (`IsPaid` checkbox)
- ✅ Service type auto-creation
- ✅ Duplicate prevention by Quote ID
- ✅ Scheduled cron job (configurable interval)

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
├── bridging_api_crm/              # Main CRM module (ACTIVE)
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── data/
│   │   └── data.xml               # Cron job definition
│   ├── models/
│   │   ├── __init__.py
│   │   └── crm.py                 # Main sync logic
│   ├── security/
│   │   └── ir.model.access.csv
│   └── views/
│       └── crm_lead.xml           # CRM UI extensions
│
├── website_custom/                # Website customizations
├── README.md
└── .gitignore

DELETED MODULES (do not recreate):
├── bridging_api_account/          # ❌ DELETED - Accounting/Invoice sync
│   # Removed due to errors and no longer needed
```

---

## 🔧 Module: `bridging_api_crm`

### Purpose
Synchronizes Bridging Africa service requests with Odoo CRM leads.

### Models

#### 1. `service.service`
Simple model for service types (Plumbing, Electrical, etc.)

```python
_name = "service.service"
name = fields.Char("Name")
```

#### 2. `crm.lead` (Extended)
Inherits `crm.lead` and adds API-specific fields:

| Field | Type | API Source | Purpose |
|-------|------|------------|---------|
| `quote_id` | Integer | `Id` | Unique identifier from API |
| `provider_id` | Char | `ProviderID` | Worker/Provider ID |
| `ispaid` | Boolean | `IsPaid` | **Payment status** (auto-updates) |
| `workerrrgency` | Char | `Id` | Worker urgency (legacy) |
| `q_status_id` | Char | `StatusID` | Quote status ID |
| `service_id` | Many2one | `ServiceName` | Link to service type |

### Main Method: `_cron_api_crm_services()`

**Location:** `models/crm.py`

**Function:** Fetches data from external API and creates/updates CRM leads.

**API Endpoint:**
```
https://bridging-africa.com/api/odooapi/GetAllRequests
```

**Process:**
1. HTTP GET request to API
2. Parse JSON response (`completed` and `pending` arrays)
3. For each job:
   - Check if `quote_id` exists in Odoo
   - **If NEW:** Create lead with all data
   - **If EXISTS:** Update `ispaid` field if changed
4. Auto-create service types if they don't exist

**Key Code Logic:**
```python
# Check for existing lead
existing_lead = LeadObj.search([("quote_id", "=", data.get("Id"))], limit=1)

if not existing_lead:
    # Create new lead
    LeadObj.create({...})
else:
    # Update IsPaid if changed
    api_is_paid = data.get("IsPaid")
    if existing_lead.ispaid != api_is_paid:
        existing_lead.write({"ispaid": api_is_paid})
```

---

## ⏰ Cron Job Configuration

**File:** `data/data.xml`

```xml
<record id="ir_cron_api_call_crm" model="ir.cron">
    <field name="name">API: CRM web services</field>
    <field name="model_id" ref="crm.model_crm_lead"/>
    <field name="state">code</field>
    <field name="code">model._cron_api_crm_services()</field>
    <field name="interval_number">10</field>      <!-- Minutes -->
    <field name="interval_type">minutes</field>
    <field name="active" eval="True"/>           <!-- ENABLED -->
</record>
```

**Current Settings:**
- Interval: Every 10 minutes
- Status: Active
- User: OdooBot

---

## 🚀 Deployment Workflow (Odoo.sh)

### Branch Structure
| Branch | Purpose | Auto-deploy |
|--------|---------|-------------|
| `prod` | Production | Yes |
| `19.0-staging` | Staging/Testing | Yes |
| `main` | Development | No |

### Standard Update Process
1. **Develop** on `main` branch
2. **Test** by dragging to `19.0-staging` in Odoo.sh
3. **Deploy** by dragging `19.0-staging` to `prod`
4. **Verify** in Odoo Apps (version bump triggers update)

### Version Bumping
Always bump version in `__manifest__.py` to trigger auto-update:
```python
"version": "19.0.0.2",  # Increment last digit for minor updates
```

---

## 🐛 Troubleshooting Guide

### Issue: `IsPaid` not updating
**Solution:**
- Verify cron job is **Active** (Settings → Technical → Scheduled Actions)
- Check that `data.xml` has `eval="True"` for active field
- Manually run cron and check logs

### Issue: "Module not found" errors in logs
**Solution:**
- Check if module was deleted from filesystem but not database
- Use Odoo shell to delete from `ir_module_module` table:
```python
env.cr.execute("DELETE FROM ir_module_module WHERE name = 'module_name';")
env.cr.commit()
```

### Issue: Cron job not appearing
**Solution:**
- Ensure `data/data.xml` is listed in `__manifest__.py` `data` array
- Update module (bump version or manually update in Apps)

### Issue: Duplicate leads created
**Solution:**
- Verify `limit=1` is set in `search()` calls
- Check API is returning consistent `Id` values

---

## 🗑️ Historical Issues & Resolutions

### March 2, 2026: Deleted `bridging_api_account` Module
**Problem:** Accounting module was causing errors after folder deletion:
```
AttributeError: 'account.move' object has no attribute '_cron_api_account_invoices'
```

**Solution:**
1. Deleted module record from database via Odoo shell:
```python
env.cr.execute("DELETE FROM ir_module_module WHERE name = 'bridging_api_account';")
env.cr.commit()
```
2. Restarted Odoo instance
3. Verified no more errors in logs

---

## 🔐 Security Notes

- API endpoint is currently public (no authentication)
- Consider adding API key if external system supports it
- Module runs as OdooBot (admin privileges)

---

## 📊 External System: Bridging Africa

**Platform:** https://bridging-africa.com/  
**Admin Panel:** All Trades Request management  
**API Endpoint:** `/api/odooapi/GetAllRequests`

### Data Flow
```
Bridging Africa Platform
    ↓ (HTTP GET)
Odoo Cron Job (every 10 min)
    ↓
Odoo CRM Leads
    ↓
IsPaid checkbox updates automatically
```

### Payment Status Sync
- When tradesperson marks job as "Paid" in Bridging Africa
- Next cron run updates `IsPaid` checkbox in Odoo
- No manual intervention needed

---

## 📝 Maintenance Checklist

| Task | Frequency | How |
|------|-----------|-----|
| Check cron job logs | Weekly | Odoo.sh → Logs |
| Verify IsPaid sync | Daily | Sample CRM leads |
| Monitor API errors | Daily | Odoo.sh → Logs (filter ERROR) |
| Update module | As needed | Git push → Odoo.sh auto-deploy |

---

## 🆘 Emergency Contacts

- **Developer:** Digital Information Solutions
- **Repository:** https://github.com/AliMora83/Odoo-BA-API
- **Odoo.sh:** bridging-africa-sh (AliMora83)

---

## 🔄 Recent Changes Log

| Date | Change | Commit |
|------|--------|--------|
| Mar 2, 2026 | Deleted bridging_api_account module | `30c0f8cb` |
| Mar 2, 2026 | Fixed IsPaid auto-update logic | `c12c7644` |
| Mar 2, 2026 | Activated CRM cron job (10 min interval) | `564d6531` |
| Feb 20, 2026 | Initial CRM sync implementation | `8a9df1c4` |

---

**END OF MASTER DOCUMENTATION**
```
