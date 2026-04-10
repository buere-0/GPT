#!/usr/bin/env python3
"""
LeadPilot SaaS — Flask backend
Qualifies leads from CSV using Claude AI, accepts Stripe payments.

Deploy to Railway/Render for free:
  railway up   OR   render deploy

Environment variables needed:
  ANTHROPIC_API_KEY   - Anthropic API key
  STRIPE_SECRET_KEY   - Stripe secret key (sk_live_... or sk_test_...)
  STRIPE_WEBHOOK_SECRET - Stripe webhook signing secret
  STRIPE_PRICE_STARTER  - Stripe Price ID for $9 one-time
  STRIPE_PRICE_PRO      - Stripe Price ID for $29/month
  SECRET_KEY          - Flask session secret (any random string)
"""

import csv
import io
import json
import os
import time

import anthropic
import stripe
from flask import (
    Flask, jsonify, redirect, render_template, request,
    session, url_for, send_file,
)
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(32))

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

FREE_TIER_LIMIT = 5   # leads free per session
PRO_LEAD_LIMIT = 10_000

QUALIFY_PROMPT = """You are a lead qualification specialist.
Given information about a potential sales lead, return ONLY a JSON object with:
{
  "score": <integer 1-10>,
  "qualified": <true or false>,
  "reason": "<one clear sentence explaining the score>",
  "suggested_action": "<one of: schedule_call, send_info, nurture, discard>"
}
Score 8-10 = strong fit (schedule call), 5-7 = moderate (send info/nurture), 1-4 = poor fit (discard).
Respond with ONLY valid JSON. No markdown, no explanation."""


# ─── Helpers ──────────────────────────────────────────────────────────────────

def qualify_lead(client: anthropic.Anthropic, lead: dict) -> dict:
    lead_text = "\n".join(f"{k}: {v}" for k, v in lead.items() if v)
    resp = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=300,
        system=QUALIFY_PROMPT,
        messages=[{"role": "user", "content": f"Qualify this lead:\n\n{lead_text}"}],
    )
    text = next((b.text for b in resp.content if b.type == "text"), "{}")
    return json.loads(text)


def parse_csv(file_bytes: bytes) -> list[dict]:
    text = file_bytes.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    return [dict(row) for row in reader]


def qualify_leads_batch(leads: list[dict], limit: int) -> list[dict]:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    results = []
    for lead in leads[:limit]:
        try:
            q = qualify_lead(client, lead)
        except Exception as e:
            q = {"score": 0, "qualified": False, "reason": str(e), "suggested_action": "discard"}
        results.append({**lead, "qualification": q})
    return results


def results_to_csv(results: list[dict]) -> str:
    if not results:
        return ""
    qual_keys = ["score", "qualified", "reason", "suggested_action"]
    lead_keys = [k for k in results[0].keys() if k != "qualification"]
    fieldnames = lead_keys + [f"ai_{k}" for k in qual_keys]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        flat = {k: row[k] for k in lead_keys}
        q = row.get("qualification", {})
        for k in qual_keys:
            flat[f"ai_{k}"] = q.get(k, "")
        writer.writerow(flat)
    return buf.getvalue()


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/qualify", methods=["POST"])
def qualify():
    """Free demo: qualify up to FREE_TIER_LIMIT leads."""
    if "file" not in request.files or request.files["file"].filename == "":
        return jsonify({"error": "No file uploaded"}), 400

    file_bytes = request.files["file"].read()
    leads = parse_csv(file_bytes)
    if not leads:
        return jsonify({"error": "CSV is empty or invalid"}), 400

    limit = FREE_TIER_LIMIT
    # Paid users get more
    if session.get("paid_plan") in ("pro", "agency"):
        limit = PRO_LEAD_LIMIT
    elif session.get("paid_plan") == "starter":
        limit = 200

    results = qualify_leads_batch(leads, limit)
    qualified = [r for r in results if r["qualification"].get("qualified")]
    summary = {
        "total": len(leads),
        "processed": len(results),
        "qualified": len(qualified),
        "limit_applied": limit,
        "results": results,
    }

    session["last_results"] = results  # store for download
    return jsonify(summary)


@app.route("/download")
def download():
    """Download last results as CSV."""
    results = session.get("last_results")
    if not results:
        return redirect(url_for("index"))
    csv_data = results_to_csv(results)
    buf = io.BytesIO(csv_data.encode())
    buf.seek(0)
    return send_file(buf, mimetype="text/csv", as_attachment=True, download_name="qualified_leads.csv")


# ─── Stripe Checkout ──────────────────────────────────────────────────────────

PRICE_IDS = {
    "starter": os.getenv("STRIPE_PRICE_STARTER", "price_starter_placeholder"),
    "pro":     os.getenv("STRIPE_PRICE_PRO",     "price_pro_placeholder"),
}

@app.route("/checkout")
def checkout():
    plan = request.args.get("plan", "pro")
    price_id = PRICE_IDS.get(plan)
    if not price_id or "placeholder" in price_id:
        # Demo mode — no real Stripe configured yet
        return render_template("checkout_demo.html", plan=plan)

    session_obj = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription" if plan != "starter" else "payment",
        success_url=url_for("payment_success", _external=True) + "?plan=" + plan,
        cancel_url=url_for("index", _external=True) + "#pricing",
    )
    return redirect(session_obj.url, code=303)


@app.route("/payment/success")
def payment_success():
    plan = request.args.get("plan", "pro")
    session["paid_plan"] = plan
    return render_template("success.html", plan=plan)


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data()
    sig = request.headers.get("Stripe-Signature", "")
    secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig, secret)
    except (stripe.error.SignatureVerificationError, ValueError):
        return jsonify({"error": "Bad signature"}), 400

    if event["type"] in ("checkout.session.completed", "invoice.payment_succeeded"):
        # In production: look up customer, provision access, send email
        print(f"[WEBHOOK] Payment event: {event['type']}")

    return jsonify({"received": True})


# ─── Health ───────────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status": "ok", "ts": int(time.time())})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "0") == "1")
