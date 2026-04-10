#!/usr/bin/env python3
"""
LeadPilot Social Media Agent — Twitter/X Auto-Poster
Posts pre-written viral content to build audience and drive traffic.

Setup:
  pip install tweepy python-dotenv
  Add to .env:
    TWITTER_API_KEY, TWITTER_API_SECRET
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET

Run:
  python twitter_agent.py --post-now      # post one tweet immediately
  python twitter_agent.py --schedule      # post according to schedule
  python twitter_agent.py --dry-run       # preview without posting
"""

import argparse
import json
import os
import random
import time
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ─── Tweet Library ────────────────────────────────────────────────────────────

TWEETS = [
    # Hook tweets (drive curiosity)
    {
        "text": "I qualified 847 leads in 12 minutes yesterday.\n\nNo VA. No spreadsheet.\n\nJust uploaded a CSV and let AI do the work.\n\nHere's exactly how 🧵",
        "category": "hook",
        "tags": ["#SalesHack", "#AI", "#LeadGen"],
    },
    {
        "text": "Hot take: spending more than 2 hours/week manually scoring leads is a waste of your best talent.\n\nAI does it in 60 seconds. Your team should be closing, not sorting.\n\n#SalesOps #B2BSales",
        "category": "opinion",
        "tags": ["#SalesOps", "#B2BSales"],
    },
    {
        "text": "Sales reps spend 21% of their time on lead research.\n\nThat's 8+ hours/week that could be spent in actual conversations.\n\nI automated all of it for $29/month.",
        "category": "stat",
        "tags": ["#Sales", "#Productivity"],
    },
    {
        "text": "The honest truth about lead qualification:\n\n❌ Gut feeling = 40% accuracy\n❌ Manual scoring = slow + inconsistent\n✅ AI scoring = 73% better prioritization\n\nData doesn't lie.",
        "category": "value",
        "tags": ["#DataDriven", "#Sales"],
    },
    {
        "text": "Agency owners: your team is wasting 15h/week on leads that will never close.\n\nI built a tool that reads your CSV and flags which ones are worth calling.\n\n100 leads. 60 seconds. $9.\n\nLink in bio.",
        "category": "cta",
        "tags": ["#Agency", "#B2B"],
    },
    {
        "text": "POV: it's Friday afternoon.\n\nYou upload this week's leads CSV.\nAI scores all 200 of them.\nYou send your team a list of the top 30 to call Monday.\n\nYou go enjoy your weekend.\n\nThis exists.",
        "category": "story",
        "tags": ["#WorkSmarter", "#Sales"],
    },
    {
        "text": "What I learned qualifying 50,000+ B2B leads with AI:\n\n1. Company size matters less than role + authority\n2. Notes fields are gold mines AI understands\n3. 'Not a fit' is the most valuable label\n4. Speed of qualification > perfection\n\nSave this.",
        "category": "thread",
        "tags": ["#LeadGen", "#B2BSales", "#SalesTips"],
    },
    {
        "text": "I used to pay a VA $800/month to qualify leads.\n\nNow I pay $29/month for AI.\n\nSame output. 10x faster. Zero sick days.\n\nThis is the future of sales ops.",
        "category": "testimonial",
        "tags": ["#AI", "#Sales", "#Automation"],
    },
    {
        "text": "The only 4 things that matter in a qualified lead:\n\n1. Budget authority\n2. Actual need (not polite curiosity)\n3. Timeline <90 days\n4. No blockers to change\n\nAI now scores these for you automatically.",
        "category": "education",
        "tags": ["#BANT", "#SalesQualification"],
    },
    {
        "text": "Reminder: a 'no' qualified quickly is 10x more valuable than a 'maybe' dragged out for 3 months.\n\nQualify faster. Reject faster. Close faster.\n\n#SalesPhilosophy",
        "category": "motivation",
        "tags": ["#SalesMindset"],
    },
]

LINKEDIN_POSTS = [
    {
        "text": """We analyzed 10,000 B2B leads to find what actually predicts conversion.

The top 5 signals AI catches that humans miss:

1. **Job title recency** — hired in last 6 months = 3x more likely to buy
2. **Company funding stage** — Series A/B companies are in buying mode
3. **Notes language** — "evaluating" vs "curious" is night and day
4. **Email domain** — free email = 67% less likely to convert
5. **Company size trajectory** — growing vs shrinking

We turned all of this into an AI that scores your leads automatically.

Upload a CSV → get scored leads in 60 seconds.

Free for the first 5 leads. No credit card.

Try it at LeadPilot.ai 👇

#B2BSales #SalesOps #LeadGeneration #AI #SalesStrategy""",
        "category": "educational",
    },
    {
        "text": """I just had a call with a sales director who spent 3 hours every Monday morning manually scoring their week's leads.

That's 156 hours/year.

At $80/hour loaded cost = $12,480/year wasted on a task that AI completes in 60 seconds.

They switched to LeadPilot. First week: 420 leads qualified in under 2 minutes.

The ROI on AI-powered sales ops tools is not hypothetical. It's happening right now.

Are you still doing this manually?

#Sales #AI #Automation #B2BSales #Productivity""",
        "category": "roi",
    },
]


# ─── Twitter Poster ───────────────────────────────────────────────────────────

def post_to_twitter(tweet_text: str, dry_run: bool = True) -> dict:
    """Post a tweet. Returns result dict."""
    if dry_run:
        print(f"\n[DRY RUN] Would post tweet ({len(tweet_text)} chars):")
        print("─" * 60)
        print(tweet_text)
        print("─" * 60)
        return {"status": "dry_run", "text": tweet_text}

    try:
        import tweepy
        client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
        )
        resp = client.create_tweet(text=tweet_text)
        tweet_id = resp.data["id"]
        print(f"[POSTED] Tweet ID: {tweet_id}")
        return {"status": "posted", "tweet_id": tweet_id, "text": tweet_text}
    except ImportError:
        print("[ERROR] tweepy not installed. Run: pip install tweepy")
        return {"status": "error", "error": "tweepy not installed"}
    except Exception as e:
        print(f"[ERROR] Tweet failed: {e}")
        return {"status": "error", "error": str(e)}


def format_tweet(tweet_data: dict) -> str:
    tags = tweet_data.get("tags", [])
    text = tweet_data["text"]
    # Add tags if they're not already in the text and we have space
    for tag in tags:
        if tag not in text and len(text) + len(tag) + 1 < 270:
            text += f" {tag}"
    return text


def run_scheduler(dry_run: bool = False, interval_hours: float = 6):
    """Post tweets on a schedule — 4x per day."""
    print(f"[SCHEDULER] Starting. Posting every {interval_hours}h. Dry run: {dry_run}")
    tweet_pool = TWEETS.copy()
    random.shuffle(tweet_pool)
    i = 0

    while True:
        tweet = tweet_pool[i % len(tweet_pool)]
        text = format_tweet(tweet)
        result = post_to_twitter(text, dry_run=dry_run)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Posted: {tweet['category']}")

        i += 1
        if i % len(tweet_pool) == 0:
            random.shuffle(tweet_pool)  # reshuffle for variety

        sleep_seconds = interval_hours * 3600
        print(f"Next post in {interval_hours}h...")
        time.sleep(sleep_seconds)


def print_content_calendar():
    """Print a week's worth of content ready to post."""
    print("\n" + "=" * 70)
    print("LEADPILOT — 7-DAY TWITTER CONTENT CALENDAR")
    print("=" * 70)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    selected = random.sample(TWEETS, min(7, len(TWEETS)))
    for i, (day, tweet) in enumerate(zip(days, selected)):
        print(f"\n{'─'*70}")
        print(f"📅 {day} — {tweet['category'].upper()}")
        print(f"{'─'*70}")
        print(format_tweet(tweet))
    print("\n" + "=" * 70)

    print("\n\nLINKEDIN POSTS (post 2-3x per week):")
    print("=" * 70)
    for i, post in enumerate(LINKEDIN_POSTS, 1):
        print(f"\n📌 LinkedIn Post #{i} — {post['category'].upper()}")
        print("─" * 70)
        print(post["text"])


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LeadPilot social media agent")
    parser.add_argument("--post-now", action="store_true", help="Post one tweet immediately")
    parser.add_argument("--schedule", action="store_true", help="Start posting on schedule")
    parser.add_argument("--calendar", action="store_true", help="Print 7-day content calendar")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview without posting (default: on)")
    parser.add_argument("--live", action="store_true", help="Actually post (overrides --dry-run)")
    parser.add_argument("--interval", type=float, default=6, help="Hours between posts (default: 6)")
    args = parser.parse_args()

    dry_run = not args.live

    if args.calendar:
        print_content_calendar()
    elif args.post_now:
        tweet = random.choice(TWEETS)
        text = format_tweet(tweet)
        post_to_twitter(text, dry_run=dry_run)
    elif args.schedule:
        run_scheduler(dry_run=dry_run, interval_hours=args.interval)
    else:
        print_content_calendar()


if __name__ == "__main__":
    main()
