#!/usr/bin/env python3
"""
Arauna Investimentos — SaaS backend.

Serves the static frontend and exposes API endpoints for lead management
and signal analysis.

Usage:
    python app.py              # production
    python app.py --debug      # dev mode with auto-reload
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent  # repo root
STATIC_DIR = BASE_DIR
LEADS_FILE = BASE_DIR / os.getenv("LEADS_FILE", "leads.csv")
QUALIFIED_FILE = BASE_DIR / os.getenv("OUTPUT_FILE", "qualified_leads.json")

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")


# ── Static pages ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "arauna.html")


@app.route("/signals")
def signals():
    return send_from_directory(STATIC_DIR, "index.html")


# ── Leads API ─────────────────────────────────────────────────────────────────

@app.route("/api/leads", methods=["GET"])
def list_leads():
    """Return all raw leads as JSON."""
    if not LEADS_FILE.exists():
        return jsonify([])
    leads = []
    with open(LEADS_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            leads.append(dict(row))
    return jsonify(leads)


@app.route("/api/leads", methods=["POST"])
def add_lead():
    """Add a new lead via JSON body {name, email, company, phone, notes}."""
    data = request.get_json(silent=True) or {}
    required = {"email"}
    missing = required - data.keys()
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    file_exists = LEADS_FILE.exists()
    fieldnames = ["name", "email", "company", "phone", "notes"]
    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({k: data.get(k, "") for k in fieldnames})

    return jsonify({"status": "ok", "lead": data}), 201


@app.route("/api/leads/qualified", methods=["GET"])
def qualified_leads():
    """Return the last qualification report."""
    if not QUALIFIED_FILE.exists():
        return jsonify({"error": "No report yet. Run: python agent.py"}), 404
    with open(QUALIFIED_FILE, encoding="utf-8") as f:
        return jsonify(json.load(f))


# ── Health ────────────────────────────────────────────────────────────────────

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Arauna SaaS"})


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Arauna SaaS backend")
    parser.add_argument("--debug", action="store_true", help="Enable debug/reload mode")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    print(f"  Arauna SaaS  →  http://{args.host}:{args.port}")
    print(f"  Sinais       →  http://{args.host}:{args.port}/signals")
    print(f"  Leads API    →  http://{args.host}:{args.port}/api/leads")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
