# Processos automáticos no n8n (Nutrição & Gastro — POA)

Este pacote cria 3 automações prontas para importar no n8n:

1. **Sincronizar base de profissionais** (agendamento diário)
2. **Detectar mudança de valor e gerar alerta**
3. **Receber lead por formulário e abrir atendimento**

## Como usar

1. Abra o n8n e vá em **Workflows → Import from File**.
2. Importe o arquivo `n8n/workflows/nutricao-gastro-automacoes.json`.
3. Configure credenciais necessárias:
   - Google Sheets
   - Slack (opcional)
   - SMTP/E-mail (opcional)
4. Ajuste os IDs dos recursos em cada node (`sheetId`, canal Slack, webhook URL).
5. Ative os workflows.

## Fluxos criados

### 1) Sincronizar base de profissionais
- Trigger diário às 08:00.
- Normaliza os campos (nome, especialidade, preço, endereço, link maps).
- Atualiza planilha de controle.

### 2) Detectar mudança de valor
- Roda de hora em hora.
- Compara valores atuais com último snapshot salvo no Data Store.
- Em caso de mudança, dispara alerta para Slack e e-mail.

### 3) Lead inbound (Webhook)
- Recebe `nome`, `telefone`, `interesse` via `POST`.
- Cria registro no Google Sheets.
- Envia confirmação no Slack para equipe.

## Observações

- O conteúdo da lista pode vir de banco, API, Google Sheets ou webhook.
- Se quiser, dá para incluir enriquecimento com geocoding e criação de tarefas em CRM.
