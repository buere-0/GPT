---
description: Run the lead qualification agent against leads.csv and display results
---

Run the lead qualification agent using the following steps:

1. Check that `leads.csv` exists in the project root. If not, tell the user it's missing.
2. Check that `ANTHROPIC_API_KEY` is set in the environment or `.env` file.
3. Run: `python agent.py --dry-run --max-leads 20`
4. Display a summary of the results showing how many leads were qualified, their scores, and suggested actions.
5. Ask the user if they want to run without `--dry-run` to write `qualified_leads.json`.
