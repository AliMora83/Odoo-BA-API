# HelpDesk.md - Bridging Africa Helpdesk Integration

## Overview
This document specifies the integration between the Bridging Africa external API and Odoo Helpdesk.

## Target API Endpoint
`GET https://bridging-africa.com/api/odooapi/GetCustomerQueries`

## Data Mapping
| BA Query Field | Odoo Ticket Field |
| --- | --- |
| Id | ba_query_id (Unique ID) |
| CustomerName | partner_name |
| Email | partner_email |
| Issue | description |
| Status | status (mapped to Odoo stages) |

## Implementation Steps
1. **Enable Helpdesk App**: Ensure `helpdesk` is installed in Odoo.
2. **New Model**: Create `bridging_api_crm/models/helpdesk.py`.
3. **Cron Job**: Create a recurring cron job to fetch new queries every 30 minutes.
4. **Deduplication**: Use `ba_query_id` to prevent duplicate tickets.
5. **Stage Mapping**: Map BA statuses to Odoo Helpdesk stages (New, In Progress, Solved, etc.).

## Technical Details
- **Module**: `bridging_api_crm`
- **Dependency**: Add `helpdesk` to `depends` in `__manifest__.py`.
- **User**: Runs as OdooBot.
