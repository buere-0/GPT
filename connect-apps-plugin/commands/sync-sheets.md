---
description: Sync qualified leads to a Google Sheet using the Sheets API
---

Sync qualified leads from `qualified_leads.json` to Google Sheets:

1. Check that `qualified_leads.json` exists. If not, tell the user to run `/connect-apps:qualify` first.
2. Check for required env vars:
   - `GOOGLE_SHEETS_ID` — the spreadsheet ID from the sheet URL
   - `GOOGLE_SERVICE_ACCOUNT_JSON` — path to a service account credentials JSON file
   If either is missing, guide the user to set them.
3. Install `gspread` if not present: `pip install gspread`.
4. Write a Python script that:
   - Authenticates using the service account credentials
   - Opens the sheet by `GOOGLE_SHEETS_ID`
   - Clears the first sheet and writes headers: Name, Email, Company, Score, Qualified, Action, Reason
   - Appends one row per lead from `qualified_leads.json`
5. Run the script and report how many rows were written.
