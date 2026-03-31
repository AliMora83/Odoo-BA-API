# AGENT-ONBOARDING — Odoo-BA-API

## Welcome, AGENT
This document defines the constraints and patterns for the Odoo-BA-API bridging project.

## Architecture & Conventions
- **Framework:** FastAPI (Python) for proxy logic.
- **Odoo Communication:** XML-RPC (v17) is the core integration mechanism.
- **Service Patterns:** Modular logic in `bridging_api_crm` and `website_custom`.
- **API Documentation:** Auto-generated via Swagger (/docs).

## Critical Workflows
- **Validation:** Every Odoo call must be validated with proper type checking and error handling to ensure data integrity for downstream projects.
- **Sync:** The project status is automatically synced to the Namka Mission Control dashboard via `PROJECT-SYNC.json` generated on every push to `main`.

## Verification Loop
1. Run local FastAPI tests.
2. Verify XML-RPC authentication flows.
3. Validate and update `Master.md` and `AI_CHANGELOG.md` for each significant change.
