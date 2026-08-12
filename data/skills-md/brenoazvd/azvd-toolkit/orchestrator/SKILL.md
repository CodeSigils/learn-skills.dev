---
name: orchestrator
description: "Roteador do toolkit: decide qual skill usar e encadeia (prompt-forge, prompt-blocks, graph-engineering). Primeira parada de QUALQUER pedido de prompt/orquestração. Em dúvida, pergunta ao usuário — nunca roteia no chute."
trigger: /orchestrator
---

# Orchestrator — roteador do toolkit

Papel: receber o pedido do usuário e rotear para a skill certa (ou encadear). **NÃO executa a tarefa em si** — apenas direciona. As skills se conversam: a saída de uma é entrada da outra.

## Matriz de roteamento

| Se o usuário pedir... | Rota |
|---|---|
| "monta um prompt pra IA" / "como peço X pra IA" / "refina meu prompt" | `prompt-forge` (entrevista interativa) |
| "usa os blocos prontos" / "o que já sabemos que funciona em prompt" | `prompt-blocks` |
| "estrutura esse código/docs/conhecimento em grafo" / "mapeia relações" | `graph-engineering` (pipeline KG) |
| "orquestra N agentes/CLIs/tickets pra fazer X" / "planeja em fases" | `graph-engineering` → `references/task-graphs.md` (fan-out, diamond, human gate) + `prompt-forge` (UM prompt por ticket) |
| "quero aprender graph engineering" | `graph-engineering` (modo ensino, diagramas por etapa) |
| "aprendi algo novo" / "lembra disso" / lição da sessão | `self-learning` (colhe o golden path e atualiza as skills) |
| "qual skill resolve isso?" / "não sei qual skill usar" | `skill-router` (1º azvd, 2º skills globais do PC) |
| "segurança/review de segurança/ache secrets/vulnerabilidade" | `skill-router` → `SecuritySkills` (global; instalar com `npx skills add UnitOneAI/SecuritySkills -g`) |
| pedido misto (ex.: prompt + orquestração) | encadear: `prompt-forge` → `graph-engineering` (ou vice-versa) |
| intenção ambígua | **PERGUNTAR** — uma pergunta, formato A/B com recomendação |

## Regras de encadeamento (as skills se conversam)

1. `prompt-forge` **consome** `prompt-blocks` — compõe as seções do prompt com os blocos B1-B7 (não reescreve o que já está provado).
2. `graph-engineering` (task graphs) **gera** tickets; cada ticket vira prompt via `prompt-forge`.
3. `prompt-blocks` é a **memória de lições** — qualquer skill que monte prompt deve consultá-la.
4. Saída de uma skill = entrada da próxima. Nunca refazer o que a skill anterior já entregou.

## Regras de parada

- Pedido cabe em **UM prompt autocontido** → `prompt-forge`, pare aí.
- Pedido precisa de **N prompts** (multi-repo, multi-fase) → NUNCA juntar tudo num prompt gigante ("buga a IA"): task graph primeiro, um prompt por ticket.
- Dúvida de **intenção** → perguntar ao usuário. Dúvida de **conteúdo** → a entrevista da `prompt-forge` resolve.

## Auto-atualização

Descobriu um encaminhamento novo (pedido → skill) durante o uso? Adicione uma linha na matriz de
roteamento acima (protocolo `self-learning`, regra de promoção de 3 verificações) — esta skill se
adapta a quem usa.

## Skills relacionadas

- `prompt-forge`, `prompt-blocks`, `graph-engineering` — as 3 skills que este roteador orquestra.
- `ask-matt` (global `~/.claude/skills`) — router mais amplo de skills; este é o router do azvd-toolkit.
