# Sinais por Screenshot

Ferramenta web estática para analisar screenshots de gráficos de candle e sugerir operações de scalp com base em rompimento de range.

## Arquivo
`index.html` — página única, sem backend, sem dependências externas

## Como usar
1. Abra `index.html` no navegador.
2. Carregue um screenshot via upload, arrastar/soltar ou colar (`Ctrl/⌘+V`).
3. Escolha o modo:
   - **Manual** (recomendado) — clique 3 pontos: Topo do range → Fundo do range → Último preço
   - **Auto (beta)** — estima topo/fundo pela borda direita do gráfico
4. Ajuste os parâmetros e clique em **Analisar**.

## Parâmetros
| Parâmetro | Padrão | Descrição |
|---|---|---|
| Buffer | 6 px | Margem de rompimento acima/abaixo do range |
| Stop | 18 px | Distância do stop em pixels |
| RR | 1.5× | Relação Risco/Retorno (alvo = stop × RR) |
| Regra de limite | Estrita | `>` / `<` ou `≥` / `≤` para inclusiva |

## Lógica de decisão
```
lastY < (topY - buffer)  → COMPRA  (rompimento de topo)
lastY > (botY + buffer)  → VENDA   (rompimento de fundo)
caso contrário           → ESPERA  (dentro do range)
```
*(em pixels: y menor = preço mais alto)*

## Funcionalidades extras
- **Demo** — gráfico sintético para testar sem imagem
- **Testes** — suite embutida cobrindo regras estritas e inclusivas
- Overlay visual com linhas: topo/fundo (azul), entrada (amarelo), alvo (verde), stop (vermelho)

## Tecnologia
- HTML + CSS inline + JavaScript vanilla
- Canvas 2D API para renderização e overlay
- Sem frameworks, sem backend
