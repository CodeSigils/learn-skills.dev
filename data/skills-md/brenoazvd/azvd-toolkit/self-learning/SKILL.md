---
name: self-learning
description: "Use para colher lições de sessão ('golden paths') e transformá-las em regras/skills reutilizáveis — a skill que se adapta a quem usa. Dispara SOZINHA quando: tarefa só funcionou após várias tentativas, usuário corrigiu, descobriu fato do projeto, ou usuário diz 'lembra disso'. Regra de promoção de 3 verificações antes de escrever."
trigger: /self-learning
---

# Self-Learning — a skill que se adapta

Meta-skill: não faz o trabalho — captura **COMO** o trabalho foi feito, incluindo as falhas
(pular um beco sem saída conhecido na próxima sessão vale mais que a própria vitória).

Adaptada de [Kulaxyz/self-learning-skills](https://github.com/Kulaxyz/self-learning-skills) (MIT) —
mesmo loop, direcionado ao ecossistema azvd-toolkit (4 skills + 4 IAs).

## Estilo do usuário (detecte ANTES de colher)

Cada usuário armazena conhecimento do seu jeito — **nunca assuma OKF**. Detecte ou pergunte:
OKF (`index.md`+`log.md`), `MEMORY.md` no repo, `CLAUDE.md`/`AGENTS.md`, auto-memory do agente,
ou nenhum (proponha o mais simples). Fatos de 1 linha e lições negativas vão para o local do
estilo detectado; blocos novos sempre para `blocks/` do prompt-blocks (portáveis).

## O loop (igual em qualquer IA)

1. **Reconhecer o momento** — qualquer sinal destes é gatilho:
   - Tarefa que só funcionou **após várias tentativas**, erros de percurso ou **correção do usuário**;
   - **Fato específico do projeto** que o agente não sabia de antemão (onde moram creds/env, comando não-óbvio, sequência obrigatória, gotcha que contraria o óbvio);
   - **Fluxo operacional que vai recorrer** (deploy, alcançar o banco, verificar em produção, rodar migração);
   - Usuário sinaliza: *"lembra disso"*, *"salva isso como regra"*, *"não me faz explicar de novo"*.
2. **Capturar sem pedir** — age no sinal imediatamente, escolhe escopo/nome sozinho, **avisa depois** (o usuário pode editar/apagar).
3. **Reutilizar** — na próxima sessão a regra/skill carrega sozinha (descrição bate com o pedido ou arquivo de instruções é sempre lido).

## Triagem: para onde vai a lição?

| Situação | Destino |
|---|---|
| Procedimento multi-passo reutilizável | skill nova (ou atualizar existente) |
| Regra nova de prompt (lição de incidente) | **bloco novo no `prompt-blocks`** — com a lição que o originou |
| Pergunta/ferramenta que a entrevista deveria puxar | **linha nova na matriz do `prompt-forge`** |
| Encaminhamento novo (pedido → skill certa) | **linha nova na matriz do `orchestrator`** |
| Fato único / correção de 1 linha (env var, path) | memória do projeto (MEMORY.md ou OKF `log.md`) — skill é overkill |
| Fatos/decisões do projeto que mudam a "doc viva" | **atualizar a memória do projeto** após a entrega (bloco B9 do prompt-blocks) |
| Run longo que pode ser cortado | **checkpoint de retomada** (bloco B10 — estado REAL, não intenção) |
| Coisa genuinamente one-off, sem chance de recorrer | pular |

## Regra de promoção (não enshrinar chute)

Skill/regra é **autoritativa** — a próxima sessão confia sem re-derivar. Só escreva quando **as 3** valerem:

1. **Check que passou** — o caminho foi verificado de verdade (teste passou, comando saiu limpo, build verde, probe/print confirmou). Registre qual foi o check. *"Pareceu funcionar"* NÃO é check.
2. **Padrão de falha nomeado** — você nomeia a falha que a regra evita ou diagnostica (ex.: "deploy parcial → chunk 404"), não um vago "às vezes quebra".
3. **Um beco sem saída descartado** — abordagem concreta que você tentou e eliminou, com o motivo.

Faltou qualquer uma → **não é regra ainda**: nota na memória (marcada `não-verificada`) ou pular.
Isso mantém chutes confiantes fora do conjunto — a skill não vira lixo.

Para **blocos do prompt-blocks** o filtro é mais fino — F1-F5 (recorrência, custo, evidência,
especificidade, tamanho) vive na própria skill `prompt-blocks`; use-o antes de propor bloco novo.

## Procedimento de colheita

1. **Aplicar a regra de promoção.** Faltou check/falha/beco → memória ou pular.
2. **Escolher escopo e nome sozinho.** Padrão: escopo do projeto. Nome claro e específico.
3. **Dedupe.** Procurar skill/bloco/linha existente para ATUALIZAR em vez de duplicar — no toolkit: `prompt-blocks` (catálogo B1-B10 em `blocks/`), `prompt-forge` (matriz de tipos), `orchestrator` (matriz de roteamento); no projeto: `.claude/skills/`, `~/.claude/skills/`, `~/.agents/skills/`. Um fato que já está no OKF pode só precisar de um ponteiro.
4. **Destilar o golden path DESTA conversa** enquanto está fresco: comandos exatos, paths, nomes de env, a ordem obrigatória e — tão importante quanto — os becos sem saída com o porquê.
5. **Escrever.**
   - **Arquivo NOVO** (bloco novo, skill nova, linha de matriz nova em arquivo próprio):
     **ANTES de criar, avise o usuário e PEÇA permissão** — proposta de 1-2 linhas (o que, onde,
     por quê). Só cria com OK. O usuário é o gate (preferência explícita).
   - **Editar EXISTENTE** (atualizar texto, adicionar lição, ajustar linha da matriz): automático.
   - Toolkit → edita no repo `azvd-toolkit` (bloco/linha nova com a lição) + commit. Projeto → skill local no dir certo.
6. **Propagar** (se mexeu no toolkit): Hermes (`~/AppData/Local/hermes/skills/`), agy (`~/.gemini/config/plugins/azvd-toolkit/skills/` — pastas reais, frontmatter SEM trigger), Claude Code (`claude plugin marketplace update azvd`), e `npx skills add` se quiser atualizar o dir universal. Se mexeu no projeto: só o repo.
7. **Avisar o usuário** — o que capturou, onde, e a lição em 1 linha. Ele pode editar/apagar (gate humano é o usuário, sempre).

## Escopo: toolkit vs projeto

- **Toolkit (azvd-toolkit)**: regras de PROMPT e orquestração que valem para qualquer projeto (blocos, matrizes, rotas). Vão para o repo e propagam para as 4 IAs.
- **Projeto (repo do cliente)**: fatos e fluxos DAQUELE código (env vars dele, schema dele, deploy dele). Ficam no repo do projeto via git.

## Skills relacionadas

- `skill-router` — porta de entrada: encaminha para esta skill quando o pedido é aprendizado/lição.
- `orchestrator` — roteia para esta skill quando o pedido é "aprendi algo novo".
- `prompt-blocks` / `prompt-forge` — destinos principais da colheita.
- `graph-engineering` — se a colheita virar um mapa de conhecimento, use o pipeline KG.
