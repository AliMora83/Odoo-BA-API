# Odoo-BA-API: Bridging Africa API Integration

## Overview

Odoo-BA-API is an Odoo module that automatically synchronizes service requests from the Bridging Africa external API into your Odoo CRM system. This module eliminates manual data entry by automatically pulling completed and pending jobs, creating service records, and populating CRM leads with customer and job information.

## What This Module Does

This module provides a seamless bridge between the Bridging Africa service request system and Odoo's CRM by:

- **Automatically fetching** all completed and pending service requests from the external API
- **Preventing duplicates** by checking if requests already exist in Odoo before creating new records
- **Creating services** dynamically (Plumbing, Electrical, Carpentry, etc.) if they don't already exist
- **Populating CRM leads** with comprehensive job details including customer information, service type, pricing status, and job descriptions

## Features

✅ **Automated Synchronization** - Scheduled cron job runs automatically at set intervals <br>
✅ **Duplicate Prevention** - Checks for existing quotes before creating new leads <br>
✅ **Service Auto-Creation** - Automatically creates service types as needed <br>
✅ **Bidirectional Data Mapping** - Maps API data fields to Odoo CRM fields <br>
✅ **Status Tracking** - Captures job status (completed, pending) and payment status

## Installation

### Prerequisites

- Odoo 19.0 or higher
- Python 13+
- `requests` library installed

### Steps

1. Clone or download this module to your Odoo addons directory:
   ```
   [git clone <repo-url> ~/odoo/addons/odoo-ba-api](https://github.com/AliMora83/Odoo-BA-API.git)
   ```

2. Restart your Odoo server

3. Navigate to **Apps** in Odoo and search for "Odoo-BA-API"

4. Click **Install**

5. Configure the API endpoint URL if different from the default

## Configuration

### API Endpoint

The default API endpoint is:
```
https://bridgingafrica.ncnsoftware.com/api/odooapi/GetAllRequests
```

To modify this, edit the `_cron_api_crm_services()` method in `models/crm.py`

### Scheduling

The synchronization runs automatically via a cron job. To adjust the schedule:

1. Go to **Settings** → **Technical** → **Automation** → **Scheduled Actions**
2. Find "CRM Services API Sync" 
3. Modify the **Interval Type** and **Interval Number** as needed

**Recommended:** Run every hour or every 30 minutes for real-time data sync

## Data Mapping

### Service Model (`service.service`)

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Service type (e.g., Plumbing, Electrical) |

### CRM Lead Fields (Enhanced)

| Odoo Field | API Field | Data Type | Description |
|------------|-----------|-----------|-------------|
| `quote_id` | `Id` | Integer | Unique identifier from API |
| `provider_id` | `ProviderID` | Char | Provider/Worker identifier |
| `contact_name` | `Tradesperson` | Char | Worker or tradesperson name |
| `workerrrgency` | `Id` | Char | Worker urgency indicator |
| `ispaid` | `IsPaid` | Boolean | Payment status |
| `q_status_id` | `StatusID` | Char | Quote/Job status ID |
| `name` | `WorkerUrgency` | Char | Lead title |
| `partner_name` | `Customer` | Char | Customer name |
| `description` | `JobDetail` | Text | Job description and details |
| `service_id` | `ServiceName` | Many2one | Link to Service record |

## How It Works

### Data Flow Diagram

```
External API (Bridging Africa)
         ↓ (HTTP GET Request)
Get All Service Requests (Completed + Pending)
         ↓
Parse JSON Response
         ↓
For Each Job Request:
  ├─ Check if Quote ID already exists in Odoo
  │  ├─ If YES → Skip (prevent duplicates)
  │  └─ If NO → Continue
  ├─ Extract Service Name
  ├─ Check if Service exists
  │  ├─ If YES → Use existing Service ID
  │  └─ If NO → Create new Service
  └─ Create CRM Lead with all job details
         ↓
All Data Synced in Odoo CRM ✓
```

### Detailed Process Flow

1. **Cron Job Triggers**: Scheduled task runs at configured interval
2. **API Request**: Module sends HTTP GET request to Bridging Africa API
3. **Response Parsing**: API response is converted from JSON format
4. **Duplicate Check**: For each job, module searches for existing `quote_id` in CRM
5. **Service Lookup**: Module checks if service type exists
6. **Service Creation**: If service doesn't exist, it's created automatically
7. **Lead Creation**: New CRM lead is created with complete job information
8. **Repeat**: Process repeats for both "completed" and "pending" jobs

## Error Handling

The module includes basic error handling:

- **HTTP Status Codes**: Only processes data if API returns 200 (success)
- **Logging**: Prints status and JSON data for debugging
- **Duplicate Prevention**: Automatically skips duplicate records

## Troubleshooting

### Issue: No data syncing

**Solution**: 
- Check API endpoint URL is accessible
- Verify cron job is enabled in **Settings** → **Technical** → **Scheduled Actions**
- Check Odoo logs for error messages

### Issue: Duplicate records being created

**Solution**:
- This shouldn't happen with duplicate prevention. If it does, check the API response format hasn't changed
- Manually delete duplicates and ensure cron job is running

### Issue: Services not being created

**Solution**:
- Verify service names from API match expected format
- Check user permissions for creating service records
- Review Odoo error logs

## File Structure

```
odoo-ba-api/
├── __init__.py                 # Module initialization
├── __manifest__.py             # Module metadata
├── README.md                   # This file
├── models/
│   ├── __init__.py            # Models initialization
│   ├── service.py             # Service model definition
│   └── crm.py                 # CRM model extension (API sync logic)
├── data/
│   └── data.xml               # Sample data
└── views/
    ├── service_views.xml      # Service UI views
    └── crm_views.xml          # CRM views and dashboards
```

## Code Overview

### Service Model
```python
class ServiceService(models.Model):
    _name = "service.service"
    name = fields.Char("Name")
```
Stores available service types (Plumbing, Electrical, etc.)

### CRM Extension
```python
class CrmLead(models.Model):
    _inherit = "crm.lead"
    # ... additional fields for API data
    
    @api.model
    def _cron_api_crm_services(self):
        # Main API synchronization logic
```
Extends Odoo's CRM Lead model and includes the cron job function

## API Response Format Expected

The API should return JSON in this format:

```json
{
  "completed": [
    {
      "Id": 12345,
      "ServiceName": "Plumbing",
      "ProviderID": "PROV001",
      "Tradesperson": "Ahmed Hassan",
      "IsPaid": true,
      "StatusID": "COMPLETED",
      "WorkerUrgency": "Urgent",
      "Customer": "John Smith",
      "JobDetail": "Fix burst water pipe in bathroom"
    }
  ],
  "pending": [
    {
      "Id": 12346,
      "ServiceName": "Electrical",
      "ProviderID": "PROV002",
      "Tradesperson": "Fatima Dali",
      "IsPaid": false,
      "StatusID": "PENDING",
      "WorkerUrgency": "Standard",
      "Customer": "Jane Doe",
      "JobDetail": "Install new light fixtures in kitchen"
    }
  ]
}
```

## Security Considerations

- **API Endpoint**: Currently stores API URL in code. Consider moving to secure configuration
- **Authentication**: The current implementation doesn't include API authentication. Add if API requires it
- **Data Privacy**: Ensure customer and job data complies with privacy regulations
- **Access Control**: Restrict who can view/manage synced CRM leads

## Future Enhancements

- [ ] Add authentication/API keys for secure API access
- [ ] Implement error notifications via email/Odoo messages
- [x] Add manual sync button in UI
- [ ] Support for updating existing leads instead of only creating new ones
- [ ] Bi-directional sync (push Odoo updates back to API)
- [ ] Webhook support for real-time updates
- [ ] Advanced filtering and search options
- [x] Dashboard with sync statistics and history

## Performance Notes

- **Initial Sync**: First run may take time if API returns many records
- **Ongoing Sync**: Duplicate prevention makes subsequent runs fast
- **API Rate Limiting**: Be aware of API rate limits when adjusting cron frequency

## Support & Contribution

For issues, questions, or contributions:

1. Check the troubleshooting section above
2. Review Odoo logs in **Settings** → **Technical** → **Error Logs**
3. Contact the development team

## License

AGPL-3

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Dec 2025 | Initial release - API sync for completed and pending jobs |

## Author

**DIS Development Team**

Created: December 2025

---

**Last Updated**: December 12, 2025