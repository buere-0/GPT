#!/usr/bin/env python3
"""
Social media content agent for Arauna Investimentos.

Generates a weekly Twitter/X content calendar focused on trading signals,
market education, and product awareness — in Brazilian Portuguese.

Usage:
    python twitter_agent.py --calendar          # print this week's posts
    python twitter_agent.py --calendar --days 14  # two-week calendar
    python twitter_agent.py --topic "DOGE/USDT"  # single post idea
"""

import argparse
import os
import sys
from datetime import date, timedelta

import anthropic
from dotenv import load_dotenv

load_dotenv()

BRAND = "Arauna Investimentos"
HANDLE = "@AraunaInvest"
VOICE = (
    "Você é o redator de redes sociais da Arauna Investimentos, "
    "casa de análise focada em operações de scalp cripto. "
    "Tom: direto, confiante, educativo — sem emojis em excesso. "
    "Escreva em português brasileiro. Máximo 280 caracteres por post. "
    "Inclua 1-2 hashtags relevantes ao final."
)

THEMES = [
    "dica de leitura de candle / rompimento de range",
    "gestão de risco: stop e R/R",
    "como usar sinais por screenshot na prática",
    "psicologia do trader — disciplina e consistência",
    "análise rápida de setup no DOGE ou BTC",
    "por que scalp no cripto é diferente de ações",
    "erro comum de iniciantes e como evitar",
]


def make_calendar(client: anthropic.Anthropic, days: int) -> list[dict]:
    today = date.today()
    posts = []

    # One theme per day, cycling through the list
    for i in range(days):
        post_date = today + timedelta(days=i)
        theme = THEMES[i % len(THEMES)]

        prompt = (
            f"Crie um post para Twitter sobre o tema: \"{theme}\".\n"
            f"Contexto: {BRAND}, análise de scalp cripto.\n"
            "Retorne apenas o texto do post, sem aspas nem explicações extras."
        )

        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=200,
            system=VOICE,
            messages=[{"role": "user", "content": prompt}],
        )

        text = next(
            (b.text for b in response.content if b.type == "text"), ""
        ).strip()

        posts.append({
            "date": post_date.strftime("%Y-%m-%d (%a)"),
            "theme": theme,
            "post": text,
        })

    return posts


def make_single_post(client: anthropic.Anthropic, topic: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=200,
        system=VOICE,
        messages=[{
            "role": "user",
            "content": (
                f"Crie um post para Twitter sobre: \"{topic}\".\n"
                "Retorne apenas o texto do post."
            ),
        }],
    )
    return next(
        (b.text for b in response.content if b.type == "text"), ""
    ).strip()


def print_calendar(posts: list[dict]) -> None:
    width = 64
    print("\n" + "=" * width)
    print(f"  Calendário de Posts — {BRAND} {HANDLE}")
    print("=" * width)
    for p in posts:
        print(f"\n  {p['date']}")
        print(f"  Tema : {p['theme']}")
        print(f"  Post : {p['post']}")
        print(f"  Chars: {len(p['post'])}/280")
        print("  " + "-" * (width - 2))
    print()


def main():
    parser = argparse.ArgumentParser(description="Twitter content calendar for Arauna")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--calendar", action="store_true", help="Generate weekly calendar")
    group.add_argument("--topic", metavar="TOPIC", help="Generate a single post for TOPIC")
    parser.add_argument(
        "--days", type=int, default=7, metavar="N",
        help="Number of days for calendar (default: 7)",
    )
    args = parser.parse_args()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("[ERROR] ANTHROPIC_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    if args.calendar:
        print(f"Gerando calendário de {args.days} dias...", flush=True)
        posts = make_calendar(client, args.days)
        print_calendar(posts)
    else:
        print(f"Gerando post sobre: {args.topic}...", flush=True)
        post = make_single_post(client, args.topic)
        print(f"\n{post}\n({len(post)}/280 chars)\n")


if __name__ == "__main__":
    main()
