# Arthur One — Assistente Virtual Autônomo (n8n + iPhone)

Este projeto define um agente **interativo**, pensado para uso no celular do Arthur, com foco em:

- execução autônoma de rotinas;
- interação por voz via iPhone (Siri/Atalhos);
- respostas com personalidade própria;
- obediência estrita às regras e mandamentos definidos por Arthur;
- redução de retrabalho (agente resiliente com validações e fallback).

## 1) Visão de alto nível

```text
iPhone (Atalho Siri / modo voz)
   -> Webhook n8n (/arthur/voice)
      -> Guardião de Identidade (somente Arthur)
      -> Orquestrador de Intenção
         -> Memória de contexto
         -> Ferramentas (agenda, tarefas, e-mail, resumo diário)
      -> Resposta final (texto + ação executada)
```

## 2) Princípios de comportamento

1. **Mandamentos do Arthur sempre vencem** qualquer opinião do agente.
2. O agente pode sugerir alternativas, mas nunca executar ação proibida.
3. Toda automação crítica exige:
   - validação de identidade;
   - confirmação explícita para ações destrutivas;
   - log de auditoria.
4. Em caso de incerteza, responder: “não tenho confiança suficiente” e pedir confirmação.

## 3) Integração no iPhone (voz)

1. Criar um Atalho no app **Atalhos** com comando de voz (Siri).
2. Atalho captura áudio, converte para texto e envia para o webhook do n8n.
3. O retorno do webhook é lido por voz no iPhone.
4. Opcional: disparo por botão de ação/tela bloqueada para uso ultra-rápido.

## 4) Processos automáticos prontos (n8n)

### A) Assistente conversacional com execução
- Entrada por webhook (voz/texto).
- Filtro de identidade com chave secreta do Arthur.
- Classificação de intenção:
  - agenda,
  - tarefas,
  - resumo,
  - foco/trabalho profundo,
  - companhia (mensagens proativas saudáveis).

### B) Briefing matinal automático (07:00)
- Consolida calendário + tarefas + pendências críticas.
- Envia briefing curto e objetivo no canal preferido.

### C) Guardião de foco
- Detecta excesso de reuniões/tarefas sem pausa.
- Sugere blocos de foco e pausas.

### D) Companheiro noturno
- Check-in diário de energia/humor/progresso.
- Gera resumo de vitórias e plano de amanhã em 3 passos.

## 5) Segurança e confiabilidade

- Chave `ARTHUR_MASTER_KEY` obrigatória em todas as requisições.
- `allowlist` de comandos que podem ser executados sem confirmação.
- Modo seguro para ações de risco (exige “CONFIRMAR”).
- Retentativas com limite e alerta em erro repetido.

## 6) Prompt-base recomendado

Use este bloco no nó de IA:

> Você é o Arthur One. Você pode ter opinião própria para sugerir caminhos mais eficientes, mas a prioridade absoluta é obedecer os mandamentos definidos por Arthur. Se houver conflito entre sua sugestão e uma regra de Arthur, siga Arthur sem exceções. Nunca invente execução feita. Sempre retorne: (1) o que entendeu, (2) ação executada, (3) próximo passo recomendado.

## 7) Deploy rápido

1. Importar `n8n/workflows/arthur_oracle_assistant.json` no n8n.
2. Configurar variáveis de ambiente:
   - `ARTHUR_MASTER_KEY`
   - `OPENAI_API_KEY` (ou provedor equivalente)
3. Conectar credenciais de calendário/e-mail/tarefas.
4. Ativar workflow e testar via webhook com payload de exemplo.

## 8) Payload de exemplo

```json
{
  "user": "Arthur",
  "master_key": "SUA_CHAVE_FORTE",
  "channel": "iphone_voice",
  "message": "Organize meu dia e bloqueie 2 horas de foco após o almoço"
}
```
