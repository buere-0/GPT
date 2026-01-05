# Automação no n8n para geração de posts de street food

Este repositório agora inclui um fluxo n8n pronto para ser importado e executar o pipeline de geração de posts 2x por semana, usando o conjunto de keywords/afiliados fornecido pelo projeto **Aventuras de Comida de Rua pelo Mundo**. O fluxo roda em ambiente self-hosted do n8n e grava os arquivos de saída em um diretório configurável (padrão `/data/content`).

## Arquivos
- `workflows/street-food-content-workflow.json`: export do fluxo n8n com gatilho semanal (seg/qui às 09:00), geração do post, gravação do JSON e atualização do manifest.

## Variáveis de ambiente
- `CONTENT_DIR`: caminho base onde os arquivos serão escritos (default: `/data/content`).
- (Opcional) `SEED`: string para tornar a escolha pseudo-determinística de keywords.

## Como usar
1. Abra o painel do n8n, clique em **Import from File**, selecione `street-food-content-workflow.json`.
2. Ajuste o `CONTENT_DIR` no painel de credenciais/variáveis globais do n8n se quiser salvar em outro local.
3. Ative o fluxo. Ele rodará automaticamente segundas e quintas às 09:00, gerando um novo post conforme a rotação de keywords.
4. Caso queira rodar imediatamente, clique em **Execute Workflow** para gerar um post e atualizar `posts.json`.

## O que o fluxo faz
- Carrega a configuração de site, categorias, afiliados e rotação de keywords embutida no nó **Gerar Post**.
- Seleciona a próxima keyword respeitando o intervalo mínimo de 180 dias por keyword (ou recicla se todas foram usadas recentemente).
- Gera um objeto de post com slug único, metadados básicos, lista de comidas, dicas, FAQ e CTA (fallback local, pronto para ser trocado por LLM se desejar estender).
- Salva o post em `CONTENT_DIR/posts/<slug>.json` e mantém `posts.json` atualizado e ordenado por data.

## Extensões sugeridas
- Adicionar um nó **HTTP Request** para enviar o prompt a um endpoint OpenAI-compatible e substituir a geração local pelo texto do modelo.
- Encadear um nó **Execute Command** para renderizar HTML ou publicar em um CMS estático.
- Criar um segundo fluxo para agendar pins do Pinterest ou disparar notificações quando um post novo for gerado.
