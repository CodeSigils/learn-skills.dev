---
name: graph-engineering
description: "Ensina graph engineering nas duas metades. Knowledge graphs (ontologia, extração de entidades/relações/eventos, fusão, GraphRAG/memória; destilado e traduzido do curso de pós-graduação de Knowledge Graph da Southeast University, npubird/KnowledgeGraphCourse, 4.4K estrelas) e task graphs (orquestração de agentes — fan-out paralelo, verificador separado, stop rule, gates humanos). Use quando pedirem para construir um knowledge graph, extrair entidades/relações de texto, desenhar ontologia, deduplicar/mesclar entidades, dar memória de grafo ou GraphRAG a um agente, orquestrar fluxos multi-agente como grafo, ou APRENDER graph engineering — no modo ensino o agente explica cada etapa com exemplos do SEU domínio e gera diagramas."
trigger: /graph-engineering
---

# Graph Engineering

Graph engineering é a disciplina de desenhar as **estruturas** com que os agentes trabalham —
não os prompts. Tem duas metades:

1. **Knowledge graphs** — o que os agentes *lembram*. Nós são entidades e fatos; arestas são
   relações com tempo e proveniência. O pipeline de 9 etapas deste arquivo cobre isso, destilado
   do curso de pós-graduação de KG da Southeast University
   (https://github.com/npubird/KnowledgeGraphCourse, Prof. Peng Wang), traduzido para o português
   e adaptado para agentes da era LLM.
2. **Task graphs** — como os agentes *trabalham*. Nós são trabalhos; arestas são dependências de
   execução: fan-out paralelo, verificadores em contexto separado, a stop rule, o gate humano.
   Leia [references/task-graphs.md](references/task-graphs.md) quando o pedido for orquestrar
   agentes em vez de construir memória.

Modelo mental central: um knowledge graph é um **produto com schema**, não uma pilha de triplas.
A qualidade vem da ORDEM do pipeline — modele o domínio ANTES de extrair, funda ANTES de
armazenar, avalie em cada etapa.

## Modo Ensino

Quando o usuário quiser APRENDER graph engineering (em vez de construir algo), ensine — não
apenas execute. Regras:

1. Ancore cada etapa no domínio do usuário: peça UM projeto ou conjunto de dados real e use-o
   como exemplo corrente em todas as etapas.
2. **Gere artefatos visuais enquanto ensina.** Conceitos desta disciplina são formas; mostre-os.
   Para cada conceito principal, produza um diagrama pequeno que o usuário possa guardar —
   mermaid (flowchart para o pipeline e task graphs, `graph LR` para ontologias e subgrafos de
   exemplo) ou uma página HTML autossuficiente quando interatividade ajudar. No mínimo: o
   pipeline de 9 etapas, uma ontologia de 3 tipos desenhada do domínio do usuário, um subgrafo
   extraído (5-10 nós) de uma amostra real, e o padrão diamond com os trabalhos do usuário como nós.
3. Ensine na ordem do pipeline, uma etapa por troca, cada uma terminando com um exercício pequeno
   ("escreva 3 competency questions para o seu projeto") antes de avançar.
4. Feche montando o que foi construído na lição em uma `ontology.yaml` inicial e um task graph
   desenhado para o primeiro build real do usuário.

## O Pipeline de 9 Etapas

Rode as etapas em ordem. Para projetos pequenos as etapas 4-6 colapsam em uma passada de extração,
mas NUNCA pule as etapas 3 (ontologia) ou 8 (fusão) — é onde grafos do mundo real falham.

1. **Escopo e teste de valor** — Confirme que um grafo vence uma estrutura mais simples. Grafo
   compensa quando as consultas são multi-hop ("quem trabalhou com X em projetos que usam Y?"),
   quando entidades recorrem entre documentos, ou quando as RELAÇÕES são o dado. Se a consulta é
   de 1 salto, use uma tabela e pare.
2. **Escolha de representação do conhecimento** — Como os fatos são codificados: property graph
   (estilo Neo4j, default pragmático), triplas RDF (interoperabilidade/padrões), ou arestas
   tipadas em JSON/SQLite (escala pequena). Decida agora como tempo e proveniência se ligam a
   cada fato.
3. **Modelagem da ontologia** — Defina tipos de entidade, tipos de relação (com domínio/range) e
   atributos ANTES da extração. Comece mínimo: 5-15 tipos de entidade, 10-30 tipos de relação.
   Duas regras do curso: toda relação ganha um verbo preciso (`ADQUIRIU`, não `RELACIONADO_COM`),
   e se dois tipos são sempre consultados juntos, mescle-os.
   Detalhes e exemplos: [references/modeling.md](references/modeling.md)
4. **Extração de entidades (NER)** — Extraia entidades tipadas das fontes. Escada de métodos:
   regras/dicionários exatos para vocabulários fechados → extração por LLM com a ontologia no
   prompt para texto aberto. Extraia SEMPRE com span + ponteiro de fonte (proveniência).
5. **Extração de relações** — Extraia arestas tipadas entre entidades reconhecidas. Restrinja o
   LLM à lista de relações da ontologia com checagem de domínio/range; rejeite arestas cujos
   extremos tenham tipos incompatíveis. Essa única validação remove a maioria da estrutura
   alucinada.
6. **Extração de eventos** — Para domínios dinâmicos (notícias, logs, transações), extraia
   eventos como nós de primeira classe (gatilho + argumentos tipados + tempo), não só arestas
   estáticas.
   Métodos de extração, padrões de prompt e modos de falha das etapas 4-6:
   [references/extraction.md](references/extraction.md)
7. **Gate de qualidade** — Antes da fusão, amostre e pontue: precisão de entidade (as entidades
   extraídas são reais e corretamente tipadas?), precisão de relação (a sentença da fonte
   realmente afirma a aresta?). Corrija o prompt/regras, não a saída, e re-rode. Meta ≥90% de
   precisão numa amostra de 50 itens antes de prosseguir — recall melhora com mais passadas;
   precisão ruim envenena o grafo permanentemente.
8. **Fusão de conhecimento** — Mescle duplicatas dentro e entre fontes: mesma entidade real,
   formas de superfície diferentes ("Acme" = "Grupo Acme" = "Acme Corporation"). Bloqueio +
   matching + política de merge. Pular isto é a causa #1 de grafos inúteis.
   Estratégias de matching: [references/fusion-and-llm.md](references/fusion-and-llm.md)
9. **Servir aos LLMs (KG × LLM)** — Torne o grafo útil aos agentes: recuperação GraphRAG
   (subgrafo → contexto), grafo-como-memória (o agente escreve fatos de volta pelas etapas 4-8),
   e LLM-como-raciocinador sobre caminhos. Padrões e armadilhas:
   [references/fusion-and-llm.md](references/fusion-and-llm.md)

## Regras de Trabalho

- **Schema primeiro, sempre.** Extração sem ontologia produz um "grafo" que é na verdade uma nuvem
  de palavras com setas. Se o usuário resistir ao design de schema, construa a ontologia mínima
  de 5 tipos a partir de 3 documentos de amostra e mostre para aprovação.
- **Proveniência em todo fato.** Cada nó/aresta guarda `source`, `extracted_at` e confiança.
  Inegociável — a fusão (etapa 8) e a confiança dependem disso.
- **Incremental em vez de big-bang.** Processe um piloto de 10 documentos pelas 9 etapas antes de
  escalar. O piloto expõe buracos na ontologia a 1% do custo.
- **Extração por LLM é maquinário de etapa, não o pipeline.** O LLM entra nas etapas 4-6; o
  schema ao redor, a validação e a fusão são o que fazem a saída ser um knowledge graph.

## Arquivos de Referência

- [references/curriculum.md](references/curriculum.md) — Currículo completo traduzido do curso
  fonte, com resumos por aula e links para os decks originais em chinês. Leia quando o usuário
  quiser profundidade teórica ou os materiais originais. (Conteúdo acadêmico: inglês.)
- [references/modeling.md](references/modeling.md) — Representação do conhecimento e engenharia
  de ontologia (aulas 2-3). Leia nas etapas 2-3. (Inglês.)
- [references/extraction.md](references/extraction.md) — Extração de entidade, relação e evento,
  de regras a prompting de LLM (aulas 4-7). Leia nas etapas 4-7. (Inglês.)
- [references/fusion-and-llm.md](references/fusion-and-llm.md) — Fusão de conhecimento e
  integração KG × LLM (aulas 8-9). Leia nas etapas 8-9. (Inglês.)
- [references/task-graphs.md](references/task-graphs.md) — A metade de orquestração: fake edges,
  o diamond, a stop rule (DeepMind×MIT), o gate humano, guardrails. Leia ao orquestrar agentes —
  é o embasamento teórico das regras de orquestração do azvd-toolkit. (PT-BR.)
- [references/workflows.md](references/workflows.md) — Nove blocos de prompt prontos para colar
  (`/kg-tutor` → `/kg-rag`), cada um um exemplar da anatomia Tarefa/Método/Meta. Leia quando o
  usuário quiser um prompt KG pronto ou um modelo de como estruturar um. (PT-BR.)

## Task graphs na prática (azvd-toolkit)

As regras de task graph são a teoria por trás dos padrões de orquestração que este toolkit já usa
(veja a matriz da skill `orchestrator` ):

| Regra (task-graphs.md) | Na prática do toolkit |
|---|---|
| **Fake edges** (apague dependência que nada lê) | Fan-out primeiro: tickets sem dependência rodam em paralelo |
| **Diamond** (split → workers → verificador SEPARADO → merge) | analyzer→reviewer→verify; revisor em contexto separado, nunca o próprio autor |
| **Stop rule** (trabalho divisível = times; sequencial = 1 agente) | "Trabalho sequencial com zero fan-out = main thread, não delegação" |
| **Human gate** (onde errar é caro de desfazer) | Aprovação antes de tocar produção/legado; não em todo passo |
| **Guardrails** (max de rodadas, 1 escritor por arquivo, caps) | `--max-turns`/`--print-timeout`; "3 agentes editando o mesmo componente = conflito) |

## Skills relacionadas (azvd-toolkit)

- `skill-router` — porta de entrada: encaminha para esta skill quando o pedido é grafos/knowledge.
- `orchestrator` — roteador: decide quando esta skill entra.
- `prompt-forge` — gera os prompts/tickets quando um task graph vira execução (um prompt por
  ticket — nunca um prompt gigante).
- `prompt-blocks` — blocos de prompt comprovados (PARE E REPORTE, teste de decisão, contrato de
  memória) usados para escrever esses tickets.

## Créditos

Destilado e traduzido de 东南大学《知识图谱》研究生课程 (curso de pós-graduação de Knowledge Graphs
da Southeast University), Prof. Peng Wang — https://github.com/npubird/KnowledgeGraphCourse.
Todos os PDFs originais das aulas são em chinês; esta skill é uma destilação independente em
português adaptada para workflows de agentes de IA.

Esta cópia no azvd-toolkit é adaptada de [codejunkie99/graph-engineering](https://github.com/codejunkie99/graph-engineering)
(MIT, feito por @Av1dlive) — a metade de task graphs usa o trabalho "Towards a Science of Scaling
Agent Systems" (Google DeepMind × MIT) e o material publicado de multi-agente da Anthropic.
