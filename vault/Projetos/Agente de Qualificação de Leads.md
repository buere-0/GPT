# Agente de Qualificação de Leads

Agente Python que lê leads de um CSV, usa o modelo Claude (Anthropic API) para pontuar e qualificar cada um, e gera um relatório JSON.

## Arquivo
`agent.py`

## Uso
```bash
# Teste sem gravar saída
python agent.py --dry-run --max-leads 20

# Execução de produção
python agent.py --max-leads 100
```

## Configuração (`.env`)
```
ANTHROPIC_API_KEY=sk-ant-...
LEADS_FILE=leads.csv        # padrão
OUTPUT_FILE=qualified_leads.json  # padrão
```

## Formato do CSV de entrada (`leads.csv`)
| Coluna | Obrigatório |
|---|---|
| name | não |
| email | não |
| company | não |
| phone | não |
| notes | não |

## Saída por lead (JSON)
```json
{
  "score": 7,
  "qualified": true,
  "reason": "Uma frase explicando a pontuação.",
  "suggested_action": "schedule_call"
}
```

### Ações possíveis
- `schedule_call` — agendar ligação
- `send_info` — enviar material
- `nurture` — nutrir o lead
- `discard` — descartar

## Modelo utilizado
`claude-opus-4-6` via `anthropic` SDK

## Dependências
```
anthropic
python-dotenv
```
(`requirements.txt` na raiz do projeto)

## Fluxo
1. Carrega leads do CSV (respeita `--max-leads`)
2. Para cada lead, envia ao Claude com prompt de qualificação
3. Parseia a resposta JSON
4. Exibe score, status e ação no terminal
5. Grava `qualified_leads.json` (exceto em `--dry-run`)
6. Exibe resumo final: `N/M lead(s) qualified`
