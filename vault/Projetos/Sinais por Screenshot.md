---
tags: [projeto, trading, crypto, ferramenta]
arquivo: index.html
status: ativo
tecnologia: HTML, JavaScript
par: DOGE/qualquer par
---

# Sinais por Screenshot

Ferramenta web estática para analisar screenshots de candles e gerar sinais de scalp por rompimento de range.

## Como funciona
1. Carrega ou cola um screenshot do gráfico
2. Usuário escolhe modo **Manual** ou **Auto (beta)**
3. No modo Manual: marca topo, fundo e último preço no gráfico
4. Ajusta buffer, stop e Risk/Reward (RR)
5. Clica em **Analisar** → overlay com níveis desenhado na imagem

## Funcionalidades
- Upload de imagem, drag-and-drop, colagem direta (Ctrl+V)
- **Modo Demo** — testa sem screenshot
- Overlay com: topo, fundo, entrada, stop, alvo
- **Testes embutidos** — valida lógica de decisão no browser
- Par principal: DOGE (adaptável a qualquer par)

## Lógica de sinal
- Regra de rompimento de range (breakout)
- Configurável: buffer, stop loss, RR
- Regras "estritas" e "inclusivas" cobertas pelos testes

## Arquivo
`index.html` (autocontido, sem dependências externas)

## Autor
[[abuere]]

## Backlinks
← [[Home]] · [[abuere]]
