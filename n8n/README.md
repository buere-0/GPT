# Screenshot Range Bot (Experimental)

Workflow para n8n que simula atendimento de três agentes (clientes) por uma IA objetiva baseada nos arquivos `index.html` e `README.md` do projeto.

## Importação
1. Abra o n8n.
2. Clique em **Import** → **From File** e selecione `experimental-bot.json`.
3. Defina credenciais (se necessário) apenas para o Webhook público.
4. Ative o workflow se quiser receber chamadas externas.

## Entradas esperadas
Envie `POST` para o endpoint exibido pelo Webhook com um JSON:

```json
{
  "agentId": "agente_manualista",
  "message": "texto do cliente"
}
```

IDs de agentes disponíveis:
- `agente_manualista` — foco em marcação manual (Laura Campos)
- `agente_auto_beta` — foco no modo Auto (Renan Leme)
- `agente_teste` — foco em QA/Testes (Camila Duarte)

Se `agentId` for omitido, o workflow usa `agente_manualista`.

## Saída
O Webhook retorna JSON com:
- `resposta`: texto pronto para enviar ao agente.
- `segmentos`: trechos da base de conhecimento que embasaram a resposta.
- `agente` e `ia`: metadados com perfis e instruções.

## Base de conhecimento
As mensagens e instruções cobrem:
- Fluxos Manual e Auto, incluindo marcações e recortes (`index.html`).
- Parametrização de buffer, stop e RR (`index.html`).
- Botão **Testes** com casos de Estrita/Inclusiva (`index.html`).
- Modos de entrada de imagem, demo e mensagens de erro (`index.html`).
- Resumo geral do projeto (`README.md`).

A IA responde em português técnico, fazendo referência às mensagens reais da interface (`index.html`).
