---
description: Export qualified leads from qualified_leads.json to a CRM-ready CSV
---

Export the qualified leads to a CRM-compatible CSV file:

1. Check that `qualified_leads.json` exists. If not, tell the user to run `/connect-apps:qualify` first.
2. Read `qualified_leads.json` and filter to only leads where `qualification.qualified` is `true`.
3. Write a file called `crm_export.csv` with these columns:
   - name, email, company, score, suggested_action, reason
   - Map fields from the lead data and the nested `qualification` object.
4. Report how many qualified leads were exported and the output path.
5. Remind the user they can import `crm_export.csv` into HubSpot, Salesforce, or any CRM that accepts CSV.
