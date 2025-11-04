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

## Automação n8n (experimento de agentes)

Um fluxo de exemplo para o n8n foi adicionado em `n8n/scalp-screenshot-agents.json`. Ele cria três contas simuladas de clientes (`cliente-alpha`, `cliente-beta` e `cliente-gamma`) e uma IA responsiva (`scalp-ia`) que responde de forma objetiva com base nas informações desta interface. Para usar:

1. Importe o arquivo no n8n (`Settings → Import from File`).
2. Publique o workflow e copie a URL do gatilho `POST /scalp-screenshot-agents`.
3. Envie requisições JSON com os campos `agent` (um dos IDs acima) e `message` para receber respostas consistentes com o conteúdo do projeto.
4. Ajuste as mensagens, personas ou regras dentro do nó **Lógica de Conversa** conforme necessário.
