# Gumroad Product Listing — LeadPilot Toolkit

## Product Name
**LeadPilot — AI Lead Qualification Agent (Python)**

## Price
**$19** (one-time)

## Short Description (shown in search)
```
Qualify 100 leads in 60 seconds with Claude AI.
Upload CSV → Get scored results. Python script + web app included.
```

## Full Description (copy into Gumroad editor)

---

### Stop Spending Hours Scoring Leads by Hand

Your time is worth more than manual lead research.

**LeadPilot** is a Python-based AI agent that reads your leads CSV and qualifies every contact using Claude AI — giving you a fit score, reason, and suggested action for each one.

**100 leads. 60 seconds. Done.**

---

### What's Included

**📦 Core Script (`agent.py`)**
- Reads any CSV format (name, email, company, notes, LinkedIn, etc.)
- Claude AI scores each lead 1-10
- Outputs: fit score, reason, suggested action
- Actions: `schedule_call` / `send_info` / `nurture` / `discard`
- Exports results to JSON + CSV

**🌐 Web App (`saas/`)**
- Full Flask web application
- Drag-and-drop CSV upload interface
- Results displayed in browser + downloadable
- Ready to deploy on Railway or Render (free tier)
- Stripe payment integration skeleton included

**📱 Social Media Agent (`social/twitter_agent.py`)**
- 10 pre-written viral tweets for your product
- LinkedIn posts ready to publish
- 7-day content calendar
- Auto-scheduler with tweepy integration

**📧 Email Outreach Agent (`outreach/email_agent.py`)**
- Cold email templates for 3 buyer segments
- SendGrid integration for automated sending
- Prospect sourcing guide (where to find 100 leads in 2h)

**📋 Gig Templates (`freelance/`)**
- Upwork profile + 3 gig descriptions
- Fiverr gig copy + packaging strategy
- Proposal templates that get responses

**📖 24-Hour Execution Playbook (`PLANO_24H.md`)**
- Hour-by-hour action plan
- Revenue targets per stream
- Platform-specific launch checklists

---

### Who This Is For

✅ Freelancers who want to offer AI automation services
✅ Sales teams tired of manual lead scoring
✅ Agencies qualifying leads for multiple clients
✅ Founders building B2B SaaS tools
✅ Developers learning the Anthropic Claude API

---

### Tech Stack

- Python 3.11+
- Anthropic Claude API (claude-opus-4-6)
- Flask 3.0
- Stripe (optional)
- SendGrid (optional)
- Tweepy (optional)
- Railway/Render deployment ready

---

### What You Need

- Python 3.11+
- Anthropic API key (free to start at anthropic.com)
- That's it for the core script

Optional (for full features):
- Stripe account (payments)
- SendGrid account (email)
- Twitter Developer account (social posting)

---

### Sample Output

```json
{
  "name": "Sarah Johnson",
  "email": "sarah@company.com",
  "company": "TechCorp",
  "qualification": {
    "score": 8,
    "qualified": true,
    "reason": "VP-level decision maker at growing SaaS company — clear budget authority and explicit need stated in notes.",
    "suggested_action": "schedule_call"
  }
}
```

---

### FAQ

**Do I need to know Python?**
Basic Python knowledge helps, but the README walks through setup step by step. Most users are running in under 15 minutes.

**Does it work with my CRM's export format?**
Yes — it reads any CSV. Just export from your CRM and upload.

**What does Claude AI cost?**
Claude API charges per token. Qualifying 100 leads typically costs $0.10-0.30. The API key is yours.

**Can I sell this as a service?**
Yes. This license gives you full rights to use, modify, and build a business on top of this code.

**Do you offer refunds?**
If the code doesn't work as described after following the setup guide, I'll refund you within 7 days.

---

### License

This is a **commercial license**. You can:
- Use it for personal projects
- Use it for client work
- Build a SaaS on top of it
- Sell qualified lead reports as a service

You cannot resell the source code as-is.

---

### Get Started in 15 Minutes

1. Download the ZIP
2. `cd leadpilot && pip install -r requirements.txt`
3. Add your Anthropic API key to `.env`
4. `python agent.py --dry-run --max-leads 5`
5. You're qualifying leads

---

## Gumroad Setup Checklist

- [ ] Create account at gumroad.com
- [ ] New Product → "Digital Product"
- [ ] Upload ZIP of the full repo
- [ ] Set price: $19
- [ ] Add cover image (screenshot of landing page or output)
- [ ] Paste description above
- [ ] Enable "Let buyers name their price" (floor: $19) → increases revenue
- [ ] Add tags: AI, Python, sales, automation, lead generation, Claude
- [ ] Share link on Twitter, LinkedIn, Reddit (r/entrepreneur, r/SaaS, r/Python)
- [ ] Post in relevant Discord servers (Indie Hackers, Python communities)

## Revenue Projection

| Sales | Revenue |
|-------|---------|
| 6 sales | $114 |
| 10 sales | $190 |
| 20 sales | $380 |
| 50 sales | $950 |

**Goal: 6 sales in 24 hours = $114** (very achievable with proper promotion)
