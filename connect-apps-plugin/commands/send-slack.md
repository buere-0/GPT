---
description: Send a lead qualification summary to a Slack channel via webhook
---

Send a summary of qualified leads to Slack:

1. Check that `qualified_leads.json` exists. If not, tell the user to run `/connect-apps:qualify` first.
2. Check that `SLACK_WEBHOOK_URL` is set in the environment or `.env` file. If not, tell the user to add it.
3. Build a summary message with:
   - Total leads processed
   - Number qualified
   - Top 3 leads by score (name/email, score, suggested_action)
4. POST the message to `SLACK_WEBHOOK_URL` using `curl` or Python `urllib`.
5. Report success or failure with the HTTP status code.

Example curl command to test:
```
curl -X POST "$SLACK_WEBHOOK_URL" -H 'Content-type: application/json' --data '{"text":"Lead qualification complete: N leads qualified."}'
```
