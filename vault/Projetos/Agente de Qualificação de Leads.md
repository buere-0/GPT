---
tags: [projeto, IA, automação, python, claude-api]
arquivo: agent.py
status: ativo
tecnologia: Python, Claude API (Anthropic)
modelo: claude-opus-4-6
---

# Agente de Qualificação de Leads

Agente CLI em Python que usa Claude para qualificar leads automaticamente a partir de um CSV.

## Fluxo
```
leads.csv → Claude (claude-opus-4-6) → score + ação → qualified_leads.json
```

## Saída por lead
```json
{
  "score": 1–10,
  "qualified": true | false,
  "reason": "frase explicando o score",
  "suggested_action": "schedule_call | send_info | nurture | discard"
}
```

## Uso
```bash
python agent.py --dry-run --max-leads 20    # teste sem gravar
python agent.py --max-leads 100             # produção
python agent.py --list-obsidian             # lista arquivos do vault Obsidian
```

## Variáveis de ambiente
| Variável | Default | Descrição |
|---|---|---|
| `ANTHROPIC_API_KEY` | obrigatório | chave da API Anthropic |
| `LEADS_FILE` | `leads.csv` | arquivo de leads |
| `OUTPUT_FILE` | `qualified_leads.json` | relatório de saída |
| `OBSIDIAN_VAULT_PATH` | auto-detectado | caminho do vault Obsidian |

## Ferramenta Obsidian
Possui tool use integrado: Claude pode chamar `list_obsidian_files` para listar `.md` do vault, com suporte a subpastas. Detecta automaticamente o vault em locais padrão.

## Dependências
- `anthropic >= 0.40.0`
- `python-dotenv >= 1.0.0`

## Empresa
Usado pela [[Arauna Investimentos]] para qualificar prospects.

## Autor
[[abuere]]

## Backlinks
← [[Home]] · [[abuere]] · [[Arauna Investimentos]]
