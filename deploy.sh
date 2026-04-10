#!/usr/bin/env bash
# deploy.sh — Arauna Investimentos SaaS bootstrap
# Usage: ./deploy.sh

set -e
cd "$(dirname "$0")"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

ok()   { echo -e "  ${GREEN}✓${RESET}  $1"; }
warn() { echo -e "  ${YELLOW}!${RESET}  $1"; }
fail() { echo -e "  ${RED}✗${RESET}  $1"; }
info() { echo -e "  ${CYAN}→${RESET}  $1"; }

echo ""
echo -e "${BOLD}  Arauna Investimentos — Setup${RESET}"
echo "  ────────────────────────────────────────"

# ── 1. Python ────────────────────────────────────────────────────────────────
echo ""
echo -e "  ${BOLD}[1/4] Python${RESET}"
if command -v python3 &>/dev/null; then
  PY=$(python3 --version)
  ok "$PY found"
else
  fail "python3 not found — install Python 3.10+"
  exit 1
fi

# ── 2. Dependencies ──────────────────────────────────────────────────────────
echo ""
echo -e "  ${BOLD}[2/4] Dependências${RESET}"

# Add Flask if not already in requirements.txt
if ! grep -q "flask" requirements.txt 2>/dev/null; then
  echo "flask>=3.0.0" >> requirements.txt
  info "flask adicionado ao requirements.txt"
fi

pip install -q -r requirements.txt && ok "requirements.txt instalado" || {
  fail "pip install falhou"
  exit 1
}

# ── 3. .env ───────────────────────────────────────────────────────────────────
echo ""
echo -e "  ${BOLD}[3/4] Variáveis de ambiente${RESET}"

if [ -f .env ]; then
  ok ".env encontrado"
else
  cat > .env <<'ENVEOF'
# Arauna Investimentos — environment variables
ANTHROPIC_API_KEY=sk-ant-...    # substitua pela sua chave
LEADS_FILE=leads.csv
OUTPUT_FILE=qualified_leads.json
ENVEOF
  warn ".env criado — edite ANTHROPIC_API_KEY antes de continuar"
fi

if grep -q "sk-ant-\.\.\." .env 2>/dev/null; then
  warn "ANTHROPIC_API_KEY ainda é o placeholder — configure-a no .env"
fi

# ── 4. Checklist ─────────────────────────────────────────────────────────────
echo ""
echo -e "  ${BOLD}[4/4] Checklist de inicialização${RESET}"
echo ""

check_file() {
  local label="$1" path="$2"
  if [ -f "$path" ]; then
    ok "$label  (${path})"
  else
    fail "$label  (${path} — não encontrado)"
  fi
}

check_file "Frontend principal"        "index.html"
check_file "Landing page Arauna"       "arauna.html"
check_file "SaaS backend"             "saas/app.py"
check_file "Agent qualificação leads"  "agent.py"
check_file "Agent Twitter/social"      "social/twitter_agent.py"
check_file "Agent e-mail / outreach"   "outreach/email_agent.py"
check_file "Leads CSV"                 "leads.csv"

echo ""
echo "  ────────────────────────────────────────"
echo -e "${BOLD}  Pronto! Próximos passos:${RESET}"
echo ""
echo "    # Iniciar o servidor SaaS (porta 5000)"
echo "    cd saas && python app.py"
echo ""
echo "    # Abrir interface de sinais"
echo "    open http://localhost:5000/signals"
echo ""
echo "    # Qualificar leads"
echo "    python agent.py --dry-run --max-leads 20"
echo ""
echo "    # Calendário de posts para Twitter"
echo "    python social/twitter_agent.py --calendar"
echo ""
echo "    # Onde encontrar clientes"
echo "    python outreach/email_agent.py --list"
echo ""
echo "    # Redigir cold e-mail"
echo "    python outreach/email_agent.py --draft --name 'João' --company 'XP'"
echo ""
