---
name: session-handoff
description: Use quando o usuario quiser encerrar, pausar, compactar ou transferir uma conversa/trabalho para outra sessao sem perder contexto. Gera um documento Markdown de handoff autossuficiente com objetivo, contexto essencial, estado atual, proximos passos, perguntas abertas, artefatos relevantes e instrucoes para a proxima sessao. Acione em pedidos como "gere um handoff", "vou continuar em outra conversa", "preciso encerrar a sessao", "documente onde paramos" ou "crie um resumo completo para retomada".
---

# Session Handoff

## Objetivo

Gerar um arquivo Markdown autossuficiente para que outra sessao do Codex, ou outro agente compativel, retome o trabalho exatamente do ponto atual. Priorizar continuidade operacional: o leitor deve saber o que foi decidido, o que existe no disco, o que falta, quais riscos permanecem e qual e o proximo passo concreto.

## Fluxo essencial

1. Identificar o trabalho em andamento, o objetivo do usuario e a condicao de sucesso.
2. Recuperar somente o contexto necessario da conversa e, quando houver artefatos no workspace, inspecionar arquivos relevantes antes de descreve-los.
3. Separar claramente:
   - fato: ocorreu ou existe;
   - prova: arquivo, comando, trecho, link ou saida que confirma;
   - inferencia: conclusao razoavel a partir do contexto;
   - lacuna: informacao ausente;
   - risco: ponto que pode quebrar a continuidade.
4. Criar um arquivo `.md` no diretorio de trabalho atual, salvo se o usuario indicar outro caminho.
5. Validar o arquivo gerado relendo seu conteudo e checando se ele nao inventa eventos, arquivos, comandos ou decisoes.
6. Responder com o caminho absoluto do handoff e, se util, 2-4 pontos de resumo.

## Nome do arquivo

- Usar `handoff-YYYY-MM-DD-slug-curto.md`.
- O `slug` deve refletir o assunto principal em minusculas e hifenizado.
- Se ja existir arquivo com o mesmo nome, acrescentar sufixo curto como `-2`.

## Estrutura obrigatoria

Usar exatamente esta estrutura, ajustando apenas o titulo:

```markdown
# Handoff: [titulo curto e descritivo]

**Data:** [YYYY-MM-DD]
**Status:** [em andamento / bloqueado / aguardando decisao / concluido com pendencias]

## 1. Objetivo
[2-4 frases sobre o que esta sendo feito e por que.]

## 2. Contexto essencial
[Stack, ambiente, restricoes, decisoes tomadas e motivos.]

## 3. O que ja foi feito
[Lista cronologica do que foi produzido, tentado, validado ou descartado. Se algo foi descartado, explicar por que.]

## 4. Estado atual
[Onde exatamente parou. O que funciona, o que esta quebrado, o que esta pendente.]

## 5. Proximos passos
[Lista ordenada, especifica e acionavel.]

## 6. Perguntas em aberto
[Decisoes, informacoes ou investigacoes ainda necessarias. Escrever "Nenhuma identificada" se for o caso.]

## 7. Artefatos relevantes
[Arquivos com caminhos absolutos, links, comandos, snippets reais e referencias que a proxima sessao precisa.]

## 8. Instrucoes para a proxima sessao
[Tom, nivel de detalhe, cuidados, armadilhas e condicao de parada.]
```

## Regras de conteudo

- Ser exaustivo em contexto e conciso em prosa; preferir bullets e listas.
- Nao inventar nada que nao tenha ocorrido ou que nao esteja evidenciado.
- Nao transformar suposicoes em fatos. Marcar como `Inferencia`, `Lacuna` ou `Risco` quando aplicavel.
- Incluir codigo real quando codigo for necessario; nao usar pseudocodigo no lugar de trechos existentes.
- Incluir comandos reais ja executados ou recomendados somente quando forem relevantes para retomada.
- Usar caminhos absolutos para arquivos locais.
- Preservar nomes de branches, commits, issues, PRs, portas, URLs, variaveis e modelos exatamente como vistos.
- Para tarefas juridicas, preservar nuance: fatos, provas, pedidos, teses, lacunas e riscos devem ficar separados.
- Para documentos, planilhas, codigo ou artefatos visuais, registrar a validacao feita; se nao houve validacao, dizer isso e indicar a melhor checagem seguinte.
- Evitar citar ferramentas internas irrelevantes. O handoff deve ser util mesmo para uma nova sessao que so tenha acesso ao arquivo e aos artefatos indicados.

## Quando nao houver arquivo a criar

Se o ambiente nao permitir escrita, entregar o Markdown completo na resposta e explicar que nao foi possivel salvar. Ainda assim, manter a estrutura obrigatoria e informar o caminho sugerido para salvar depois.

## Checklist final

Antes de finalizar, confirmar internamente:

- O arquivo tem todas as 8 secoes obrigatorias.
- O status corresponde ao estado real.
- Cada arquivo citado existe ou esta claramente marcado como nao verificado.
- Nao ha mencao a artefatos, decisoes ou testes que nao aconteceram.
- A proxima sessao consegue executar o primeiro proximo passo sem depender da conversa original.
