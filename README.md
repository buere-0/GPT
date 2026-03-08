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

## Novo: Arthur One (assistente virtual com n8n)
Além do analisador de screenshot, este repositório agora inclui um blueprint de assistente virtual autônomo para uso no celular (iPhone + Siri/Atalhos), com processos automáticos no n8n.

Arquivos principais:
- `docs/arthur-agent/README.md`: arquitetura, princípios de segurança e instruções de deploy.
- `n8n/workflows/arthur_oracle_assistant.json`: workflow importável no n8n com:
  - webhook de voz,
  - validação de identidade do Arthur,
  - orquestração de intenção,
  - resposta estruturada,
  - briefing automático diário às 07:00.
