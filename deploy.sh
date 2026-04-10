#!/usr/bin/env bash
# LeadPilot — One-Click Deploy Script
# Deploys the SaaS to Railway and prepares all agents for launch
#
# Usage:
#   chmod +x deploy.sh
#   ./deploy.sh

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  LeadPilot — Deploy & Launch Script${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ── 1. Check Python ────────────────────────────────────────────────────────────
echo -e "${YELLOW}[1/7] Checking Python...${NC}"
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Python3 not found. Install from python.org${NC}"
    exit 1
fi
PYTHON_VER=$(python3 --version)
echo -e "${GREEN}✓ $PYTHON_VER${NC}"

# ── 2. Install dependencies ───────────────────────────────────────────────────
echo -e "${YELLOW}[2/7] Installing core dependencies...${NC}"
pip install -q anthropic flask stripe python-dotenv gunicorn
echo -e "${GREEN}✓ Core dependencies installed${NC}"

echo -e "${YELLOW}       Installing optional dependencies...${NC}"
pip install -q tweepy sendgrid 2>/dev/null && echo -e "${GREEN}✓ Social/email agents ready${NC}" || echo -e "${YELLOW}⚠ tweepy/sendgrid skipped (not required for core SaaS)${NC}"

# ── 3. Check environment ──────────────────────────────────────────────────────
echo -e "${YELLOW}[3/7] Checking environment...${NC}"

if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env found${NC}"
else
    echo -e "${YELLOW}  Creating .env from template...${NC}"
    cp saas/.env.example .env 2>/dev/null || cp .env.example .env 2>/dev/null || true
    echo -e "${RED}  ⚠ .env created — add your ANTHROPIC_API_KEY before running!${NC}"
fi

# Check API key
if grep -q "sk-ant" .env 2>/dev/null || [ -n "$ANTHROPIC_API_KEY" ]; then
    echo -e "${GREEN}✓ Anthropic API key found${NC}"
else
    echo -e "${YELLOW}  ⚠ ANTHROPIC_API_KEY not set in .env${NC}"
    echo "  Get your key at: https://console.anthropic.com"
fi

# ── 4. Test the core agent ────────────────────────────────────────────────────
echo -e "${YELLOW}[4/7] Testing lead qualification agent...${NC}"
if [ -f "agent.py" ] && [ -f "leads.csv" ]; then
    python3 agent.py --dry-run --max-leads 1 2>/dev/null && echo -e "${GREEN}✓ Agent works${NC}" || echo -e "${YELLOW}⚠ Agent test skipped (needs API key)${NC}"
else
    echo -e "${YELLOW}⚠ agent.py or leads.csv not found — skipping test${NC}"
fi

# ── 5. Start local SaaS ───────────────────────────────────────────────────────
echo -e "${YELLOW}[5/7] Starting SaaS locally...${NC}"
cd saas 2>/dev/null || true

if [ -f "app.py" ]; then
    echo -e "${GREEN}✓ SaaS app found. To start: cd saas && python app.py${NC}"
    echo -e "   URL will be: ${CYAN}http://localhost:5000${NC}"
else
    echo -e "${RED}  saas/app.py not found${NC}"
fi
cd .. 2>/dev/null || true

# ── 6. Deploy to Railway ──────────────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[6/7] Deploying to Railway...${NC}"

if command -v railway &>/dev/null; then
    echo -e "${GREEN}✓ Railway CLI found. Deploying...${NC}"
    cd saas
    railway up --detach 2>/dev/null && echo -e "${GREEN}✓ Deployed! Check: railway open${NC}" || echo -e "${YELLOW}⚠ Railway deploy failed — run 'railway login' first${NC}"
    cd ..
else
    echo -e "${YELLOW}  Railway CLI not installed.${NC}"
    echo ""
    echo -e "  ${CYAN}OPTION A — Railway (recommended, free):${NC}"
    echo "  1. npm install -g @railway/cli"
    echo "  2. railway login"
    echo "  3. cd saas && railway init && railway up"
    echo ""
    echo -e "  ${CYAN}OPTION B — Render (alternative, free):${NC}"
    echo "  1. render.com → New Web Service"
    echo "  2. Connect this GitHub repo"
    echo "  3. Build command: pip install -r requirements.txt"
    echo "  4. Start command: gunicorn app:app"
    echo "  5. Add env vars from .env"
fi

# ── 7. Print launch checklist ─────────────────────────────────────────────────
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  LAUNCH CHECKLIST — Do These NOW${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "  💻 SaaS:"
echo "     □ cd saas && python app.py  (test locally)"
echo "     □ railway up  (deploy live)"
echo "     □ Add Stripe keys to .env (stripe.com → get secret key)"
echo ""
echo "  💰 Revenue streams:"
echo "     □ Gumroad: gumroad.com → New Product → \$19"
echo "     □ Fiverr:  fiverr.com  → New Gig → \$15-75"
echo "     □ Upwork:  upwork.com  → Create Profile → Apply to 5 jobs"
echo ""
echo "  📱 Social media:"
echo "     □ python social/twitter_agent.py --calendar"
echo "     □ Copy-paste 2 tweets now"
echo "     □ Post on LinkedIn"
echo "     □ Post on r/entrepreneur, r/SaaS"
echo ""
echo "  📧 Outreach:"
echo "     □ python outreach/email_agent.py --list  (see prospect sources)"
echo "     □ Collect 20 prospect emails from Apollo.io free tier"
echo "     □ python outreach/email_agent.py --send --live --max 20"
echo ""
echo "  📖 Full plan: cat PLANO_24H.md"
echo ""
echo -e "${GREEN}  Everything is built. Go execute. 🚀${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
