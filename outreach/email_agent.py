#!/usr/bin/env python3
"""
LeadPilot Cold Email Outreach Agent
Finds potential customers and sends personalized cold emails via SendGrid.

Setup:
  pip install sendgrid python-dotenv anthropic
  SENDGRID_API_KEY in .env
  FROM_EMAIL=hello@yourdomain.com in .env

Run:
  python email_agent.py --dry-run          # preview emails without sending
  python email_agent.py --send --max 10    # send to first 10 prospects
  python email_agent.py --list             # show prospect list
"""

import argparse
import csv
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

FROM_EMAIL = os.getenv("FROM_EMAIL", "hello@leadpilot.ai")
FROM_NAME = os.getenv("FROM_NAME", "Alex from LeadPilot")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")

# ─── Prospect Segments ────────────────────────────────────────────────────────

# In production, use Apollo.io, Hunter.io, or LinkedIn Sales Navigator
# These are example prospect types to target
PROSPECT_SEGMENTS = [
    {
        "segment": "Sales Managers at SMBs",
        "where_to_find": [
            "LinkedIn: search 'Sales Manager' + '51-200 employees' + 'SaaS'",
            "Apollo.io: filter by title + company size + industry",
            "Hunter.io: find emails from LinkedIn profiles",
        ],
        "pain_point": "spending hours qualifying leads manually",
        "template": "sales_manager",
    },
    {
        "segment": "Growth Agencies",
        "where_to_find": [
            "Clutch.co: search B2B lead gen agencies",
            "LinkedIn: search 'Lead Generation Agency'",
            "Google: 'B2B lead generation agency [city]'",
        ],
        "pain_point": "scaling lead qualification for multiple clients",
        "template": "agency",
    },
    {
        "segment": "Solo Founders / Consultants",
        "where_to_find": [
            "Twitter/X: search 'sales consultant' bio",
            "Indie Hackers: find B2B SaaS founders",
            "ProductHunt: makers of sales tools",
        ],
        "pain_point": "doing everything alone without a sales team",
        "template": "founder",
    },
]


# ─── Email Templates ──────────────────────────────────────────────────────────

TEMPLATES = {
    "sales_manager": {
        "subject_lines": [
            "qualify all your leads in 60 seconds (seriously)",
            "how {company} could save 8h/week on lead scoring",
            "quick question about how you qualify leads at {company}",
        ],
        "body": """\
Hi {first_name},

I'm going to keep this short.

Sales managers at companies like {company} typically spend 6-10 hours/week manually scoring leads — or paying someone else to do it.

I built LeadPilot to fix that. Upload your leads CSV, and Claude AI qualifies all of them in under 60 seconds with:
- A fit score (1-10)
- A one-sentence reason
- A suggested action (schedule_call / send_info / nurture / discard)

First 5 leads are free, no signup required.

Worth 2 minutes to try: leadpilot.ai

— {from_name}

P.S. If this isn't relevant to your team's workflow, reply "not for us" and I won't bother you again.""",
    },
    "agency": {
        "subject_lines": [
            "qualifying leads for all your clients at once",
            "white-label AI lead scoring for agencies",
            "how agencies are cutting lead research time by 80%",
        ],
        "body": """\
Hi {first_name},

Running an agency means qualifying leads for multiple clients simultaneously — and that doesn't scale well manually.

LeadPilot lets you upload a client's lead list and get AI-scored results in 60 seconds. Our Agency plan ($97/mo) gives you:
- White-label reports with your branding
- 5 team seats
- Unlimited leads per month
- Custom AI qualification prompts per client

We already have 3 agencies using this for 10+ clients each.

Free to try (first 5 leads, no card): leadpilot.ai

Happy to do a quick 15-min demo if you want to see it with your actual leads.

— {from_name}""",
    },
    "founder": {
        "subject_lines": [
            "stop spending your Sundays scoring leads",
            "you don't need a VA for lead qualification",
            "60 seconds to know which leads are worth your time",
        ],
        "body": """\
Hi {first_name},

Building something solo means every hour matters.

Most founders I talk to spend 3-5 hours/week sorting through leads to figure out who's worth calling. That's time that could go into building, or just not working weekends.

I made LeadPilot for exactly this. Upload your CSV, get back a scored list in 60 seconds. No setup, no integrations, no VA needed.

$9 one-time for up to 200 leads. Free for the first 5.

Try it at leadpilot.ai — takes 2 minutes.

— {from_name}

(founder-to-founder, happy to swap feedback on what you're building too)""",
    },
}


# ─── Email Sending ────────────────────────────────────────────────────────────

def send_email(to_email: str, to_name: str, subject: str, body: str, dry_run: bool = True) -> dict:
    """Send email via SendGrid."""
    if dry_run:
        print(f"\n{'─'*60}")
        print(f"TO: {to_name} <{to_email}>")
        print(f"SUBJECT: {subject}")
        print(f"BODY:\n{body}")
        print(f"{'─'*60}")
        return {"status": "dry_run"}

    if not SENDGRID_API_KEY:
        print("[ERROR] SENDGRID_API_KEY not set")
        return {"status": "error", "error": "no api key"}

    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail, Email, To, Content
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        message = Mail(
            from_email=Email(FROM_EMAIL, FROM_NAME),
            to_emails=To(to_email, to_name),
            subject=subject,
            plain_text_content=Content("text/plain", body),
        )
        resp = sg.client.mail.send.post(request_body=message.get())
        print(f"[SENT] {to_email} — Status: {resp.status_code}")
        return {"status": "sent", "code": resp.status_code}
    except ImportError:
        print("[ERROR] sendgrid not installed. Run: pip install sendgrid")
        return {"status": "error", "error": "sendgrid not installed"}
    except Exception as e:
        print(f"[ERROR] {to_email}: {e}")
        return {"status": "error", "error": str(e)}


def compose_email(prospect: dict, template_key: str) -> tuple[str, str]:
    """Compose subject + body for a prospect."""
    template = TEMPLATES.get(template_key, TEMPLATES["founder"])
    subject = template["subject_lines"][0].format(**prospect)
    body = template["body"].format(**prospect, from_name=FROM_NAME)
    return subject, body


def run_outreach(prospects: list[dict], dry_run: bool = True, max_emails: int = 10, delay: float = 2.0):
    """Send outreach emails to a list of prospects."""
    print(f"\n[OUTREACH] {len(prospects)} prospects | dry_run={dry_run} | max={max_emails}")
    results = []
    sent = 0

    for p in prospects[:max_emails]:
        template_key = p.get("template", "founder")
        subject, body = compose_email(p, template_key)
        result = send_email(
            to_email=p["email"],
            to_name=p.get("first_name", "there"),
            subject=subject,
            body=body,
            dry_run=dry_run,
        )
        results.append({"prospect": p, "result": result})
        sent += 1
        if not dry_run and sent < max_emails:
            time.sleep(delay)  # be polite to SendGrid rate limits

    print(f"\n[SUMMARY] {sent} emails {'previewed' if dry_run else 'sent'}")
    return results


# ─── Sample Prospect List ─────────────────────────────────────────────────────

SAMPLE_PROSPECTS = [
    {
        "first_name": "Sarah",
        "last_name": "Johnson",
        "email": "sarah@techsalesco.com",
        "company": "TechSales Co",
        "role": "VP of Sales",
        "template": "sales_manager",
    },
    {
        "first_name": "Mike",
        "last_name": "Chen",
        "email": "mike@growthagency.io",
        "company": "Growth Agency",
        "role": "Founder",
        "template": "agency",
    },
    {
        "first_name": "Emma",
        "last_name": "Davis",
        "email": "emma@b2bstartup.com",
        "company": "B2B Startup",
        "role": "CEO",
        "template": "founder",
    },
]


def print_prospect_sources():
    """Print where to find qualified prospects."""
    print("\n" + "=" * 70)
    print("WHERE TO FIND 100 PROSPECTS IN 2 HOURS")
    print("=" * 70)
    for seg in PROSPECT_SEGMENTS:
        print(f"\n🎯 {seg['segment']}")
        print(f"   Pain: {seg['pain_point']}")
        print("   Find them:")
        for source in seg["where_to_find"]:
            print(f"   → {source}")
    print("\n" + "=" * 70)
    print("QUICK PROSPECT COLLECTION WORKFLOW:")
    print("1. Go to Apollo.io (free tier) → filter Sales Manager + 50-500 employees")
    print("2. Export 50 contacts with email")
    print("3. Paste into prospects.csv")
    print("4. Run: python email_agent.py --send --max 25")
    print("5. Wait 24h, follow up with openers")
    print("=" * 70)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LeadPilot outreach agent")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--live", action="store_true", help="Actually send emails")
    parser.add_argument("--send", action="store_true", help="Run outreach campaign")
    parser.add_argument("--list", action="store_true", help="Show prospect sources")
    parser.add_argument("--max", type=int, default=10, help="Max emails to send")
    parser.add_argument("--prospects-file", default="prospects.csv", help="CSV of prospects")
    args = parser.parse_args()

    dry_run = not args.live

    if args.list:
        print_prospect_sources()
    elif args.send:
        # Try to load from file, fall back to samples
        prospects_path = Path(args.prospects_file)
        if prospects_path.exists():
            with open(prospects_path, newline="") as f:
                prospects = list(csv.DictReader(f))
            print(f"[INFO] Loaded {len(prospects)} prospects from {args.prospects_file}")
        else:
            print(f"[INFO] {args.prospects_file} not found — using sample prospects")
            prospects = SAMPLE_PROSPECTS
        run_outreach(prospects, dry_run=dry_run, max_emails=args.max)
    else:
        print_prospect_sources()
        print("\n\nSAMPLE EMAIL PREVIEW:")
        run_outreach(SAMPLE_PROSPECTS, dry_run=True, max_emails=3)


if __name__ == "__main__":
    main()
