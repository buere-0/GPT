#!/usr/bin/env python3
"""
Client outreach agent for Arauna Investimentos.

Two modes:
  --list    Show where and how to find potential clients (ICP guide).
  --draft   Draft a cold outreach email for a specific lead.

Usage:
    python email_agent.py --list
    python email_agent.py --draft --name "João Silva" --company "XP Inc." --role "Trader"
"""

import argparse
import os
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()

BRAND = "Arauna Investimentos"
ICP = (
    "Perfil ideal de cliente (ICP): traders de cripto e renda variável "
    "brasileiros que operam scalp ou day trade, especialmente em DOGE, BTC, ETH. "
    "Faixa: amadores avançados a profissionais independentes. "
    "Dor principal: falta de método objetivo para identificar entrada/saída."
)

SOURCING_PROMPT = f"""
Você é consultor de crescimento B2C para {BRAND}.
{ICP}

Liste os 10 melhores canais e táticas para encontrar esse perfil de cliente no Brasil,
com instruções práticas para cada um (ex.: grupos do Telegram, comunidades Discord,
fóruns, eventos, influenciadores parceiros, LinkedIn, YouTube, etc.).

Formato de saída:
  Canal / Plataforma
  - Por que funciona para esse ICP
  - Como abordar / o que oferecer
  - Dica de copy ou hook

Escreva em português brasileiro, seja direto e acionável.
"""

EMAIL_SYSTEM = (
    f"Você é o responsável de vendas da {BRAND}. "
    "Escreva cold e-mails curtos (máx. 150 palavras), diretos e personalizados. "
    "Tom: profissional mas acessível. Português brasileiro. "
    "Nunca prometa retornos financeiros específicos."
)


def get_sourcing_guide(client: anthropic.Anthropic) -> str:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": SOURCING_PROMPT}],
    )
    return next(
        (b.text for b in response.content if b.type == "text"), ""
    ).strip()


def draft_email(
    client: anthropic.Anthropic, name: str, company: str, role: str
) -> str:
    prompt = (
        f"Escreva um cold e-mail de apresentação da {BRAND} para:\n"
        f"  Nome   : {name}\n"
        f"  Empresa: {company}\n"
        f"  Cargo  : {role}\n\n"
        f"Contexto do produto: ferramenta de análise de sinais por screenshot "
        f"para scalp cripto. Inclua assunto do e-mail na primeira linha (Assunto: ...)."
    )
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=400,
        system=EMAIL_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return next(
        (b.text for b in response.content if b.type == "text"), ""
    ).strip()


def main():
    parser = argparse.ArgumentParser(description="Outreach agent for Arauna")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--list", dest="show_list", action="store_true",
        help="Show ICP sourcing guide (where to find clients)",
    )
    group.add_argument(
        "--draft", action="store_true",
        help="Draft a cold e-mail for a specific lead",
    )
    parser.add_argument("--name", default="", help="Lead full name (for --draft)")
    parser.add_argument("--company", default="", help="Lead company (for --draft)")
    parser.add_argument("--role", default="Trader", help="Lead role/cargo (for --draft)")
    args = parser.parse_args()

    if args.draft and not args.name:
        parser.error("--draft requires --name")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("[ERROR] ANTHROPIC_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    if args.show_list:
        print("Gerando guia de prospecção...\n", flush=True)
        guide = get_sourcing_guide(client)
        print("=" * 64)
        print(f"  Onde Encontrar Clientes — {BRAND}")
        print("=" * 64)
        print(guide)
        print()
    else:
        print(f"Redigindo e-mail para {args.name}...\n", flush=True)
        email = draft_email(client, args.name, args.company, args.role)
        print("=" * 64)
        print(email)
        print("=" * 64)
        print()


if __name__ == "__main__":
    main()
