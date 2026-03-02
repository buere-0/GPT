# Sinais por Screenshot — DOGE/qualquer par

Interface web estática para analisar screenshots de candles e sugerir operações de scalp com base em rompimento de range.

## Como usar
1. Abra `index.html` em um navegador desktop.
2. Carregue ou cole um screenshot do gráfico.
3. Escolha o modo **Manual** (marque topo, fundo e último preço) ou **Auto (beta)**.
4. Ajuste buffer, stop e RR conforme necessário e clique em **Analisar**.
5. Use o botão **Testes** para validar a lógica de decisão diretamente no navegador.

## Recursos
- Upload, arrastar/soltar e colagem direta de imagens.
- Modo Demo para testar sem screenshot.
- Overlay com níveis de topo, fundo, entrada, stop e alvo.
- Testes embutidos cobrindo regras estritas e inclusivas.

## Automações n8n (Nutrição & Gastro POA)

Adicionei um pacote pronto de workflows do n8n para automatizar operação de captação e monitoramento:

- `n8n/workflows/nutricao-gastro-automacoes.json`
- `n8n-processos-nutricao-gastro.md`

Fluxos incluídos:
1. Sincronização diária da base de profissionais.
2. Alerta de mudança de valores.
3. Captura de lead via webhook com envio para planilha + Slack.

Importe o JSON no n8n e configure as credenciais (Google Sheets/Slack).
