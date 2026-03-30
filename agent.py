#!/usr/bin/env python3
"""
Lead qualification agent.

Reads leads from a CSV file, uses Claude to score/qualify each one,
and writes a report of qualified leads.

Usage:
    python agent.py --dry-run --max-leads 20   # test without writing output
    python agent.py --max-leads 100            # production run
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a lead qualification specialist. Given information about a potential lead,
evaluate their fit and return a JSON object with exactly these fields:
{
  "score": <integer 1-10>,
  "qualified": <true or false>,
  "reason": "<one sentence explaining the score>",
  "suggested_action": "<next step: 'schedule_call', 'send_info', 'nurture', or 'discard'>"
}
Respond with only valid JSON, no other text."""


def load_leads(leads_file: str, max_leads: int) -> list[dict]:
    path = Path(leads_file)
    if not path.exists():
        print(f"[ERROR] Leads file not found: {leads_file}", file=sys.stderr)
        sys.exit(1)

    leads = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(dict(row))
            if len(leads) >= max_leads:
                break

    return leads


def qualify_lead(client: anthropic.Anthropic, lead: dict) -> dict:
    lead_text = "\n".join(f"{k}: {v}" for k, v in lead.items() if v)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Qualify this lead:\n\n{lead_text}"}],
    )

    text = next(
        (block.text for block in response.content if block.type == "text"), ""
    )
    return json.loads(text)


def run(dry_run: bool, max_leads: int) -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("[ERROR] ANTHROPIC_API_KEY not set in environment.", file=sys.stderr)
        sys.exit(1)

    leads_file = os.getenv("LEADS_FILE", "leads.csv")
    output_file = os.getenv("OUTPUT_FILE", "qualified_leads.json")

    leads = load_leads(leads_file, max_leads)
    print(f"Loaded {len(leads)} lead(s) from {leads_file}")

    if dry_run:
        print("[DRY RUN] No output will be written.\n")

    client = anthropic.Anthropic(api_key=api_key)
    results = []

    for i, lead in enumerate(leads, 1):
        name = lead.get("name") or lead.get("email") or f"Lead #{i}"
        print(f"  [{i}/{len(leads)}] Qualifying: {name} ...", end=" ", flush=True)

        try:
            qualification = qualify_lead(client, lead)
            score = qualification.get("score", 0)
            qualified = qualification.get("qualified", False)
            action = qualification.get("suggested_action", "—")
            reason = qualification.get("reason", "")

            status = "QUALIFIED" if qualified else "not qualified"
            print(f"score={score}/10  {status}  action={action}")
            if reason:
                print(f"      {reason}")

            results.append({**lead, "qualification": qualification})
        except (json.JSONDecodeError, anthropic.APIError) as e:
            print(f"ERROR: {e}")
            results.append({**lead, "qualification": {"error": str(e)}})

    qualified_count = sum(
        1 for r in results
        if r.get("qualification", {}).get("qualified") is True
    )
    print(f"\nSummary: {qualified_count}/{len(results)} lead(s) qualified.")

    if not dry_run:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Report written to: {output_file}")
    else:
        print("[DRY RUN] Skipped writing output file.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Lead qualification agent powered by Claude.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without writing output files (safe for testing).",
    )
    parser.add_argument(
        "--max-leads",
        type=int,
        default=50,
        metavar="N",
        help="Maximum number of leads to process (default: 50).",
    )
    args = parser.parse_args()
    run(dry_run=args.dry_run, max_leads=args.max_leads)


if __name__ == "__main__":
    main()
