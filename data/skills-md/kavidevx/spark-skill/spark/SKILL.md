---
name: spark
description: "Teaches you one new thing every time it runs — drawn from your work context, trending tech topics, and timeless developer growth concepts. Use when the user wants to learn something new, stay up to date with the industry, or grow as a developer."
metadata:
  short-description: Daily learning spark for developers
---

# Spark — Learn Something New Every Day

## Overview
Teach the user one new thing every time `/spark` is run. Topics are drawn from a **mix of three sources**:
1. The user's recent work history and current project context
2. Trending tech topics — what the industry is talking about right now (AI, new frameworks, tools, paradigms)
3. Timeless concepts that make you a better developer in every way — technically, mentally, and professionally

## Behavior

### Step 1 — Pick a Topic (Balanced Mix)
Use a rotating mix across these three sources — don't always pull from the same one:

**Source A — User's context (personal)**
- Files recently opened or edited in this session
- The current project (language, framework, domain)
- Topics the user has mentioned in the conversation
- Pick something that feels directly relevant to what they're building

**Source B — Trending tech (industry pulse)**
- What's hot in the dev world right now: AI/LLMs, edge computing, new frameworks, Web3, DevEx tools, open source breakthroughs
- Topics developers are actively discussing on X, HN, GitHub, and dev blogs
- New releases, paradigm shifts, tools gaining rapid adoption
- Example: "Bun vs Node", "htmx renaissance", "AI-assisted coding patterns", "Rust in frontend tooling"

**Source C — Developer growth (timeless)**
- Concepts that make you a better developer regardless of stack
- System design fundamentals, software craftsmanship, architecture thinking
- Career skills: code reviews, technical writing, estimation, debugging mindset
- Cross-discipline: psychology of focus, economics of tech decisions, history of computing

**Rotation rule:** Don't pick from the same source twice in a row. Vary it. Keep the user growing in all directions.

### Step 2 — Teach the Spark
Present ONE concept in this format:

```
⚡ Spark: [Topic Name]

[2-3 sentence plain English explanation — no jargon, no fluff]

Real example:
[A short, concrete example — code snippet if tech, real-life scenario if non-tech]

Why it matters to you:
[1 sentence connecting it to their work or life]
```

Keep it short. The whole spark should be readable in under 60 seconds.

### Step 3 — Offer the Choice
After the spark, always end with:

```
---
Curious? Type **deep** to dive in — or **next** for a different spark.
```

### Step 4 — Deep Dive (if user types "deep")
Go full depth on the topic:

- **How it actually works** — the internals, the mechanism
- **Why it was invented** — the problem it solved
- **Real code / real world examples** — 2-3 concrete cases
- **Common mistakes** — what people get wrong
- **Edge cases** — where it breaks or surprises you
- **What to learn next** — 2-3 related concepts that build on this
- **One thing to try today** — a small actionable exercise

End deep dives with:
```
---
Want to go even deeper on any part? Just ask.
Or type **next** for a fresh spark.
```

### Step 5 — Next Topic (if user types "next")
Pick a completely different topic — different domain, different type (switch between tech and non-tech).

---

## Topic Categories

**From User Context**
- Whatever they're building right now
- Gaps or patterns noticed in their code
- Tools/frameworks they're using but may not know deeply

**Trending Tech (Industry Pulse)**
- AI & LLMs (agents, RAG, fine-tuning, prompt engineering)
- New frameworks gaining traction (Bun, Astro, Hono, Turso, etc.)
- Paradigm shifts (edge computing, serverless, AI-native apps)
- Developer tooling breakthroughs (Cursor, Zed, Warp, etc.)
- Open source projects blowing up on GitHub
- Hot debates in the dev community

**Developer Growth (Timeless)**
- Programming concepts (data structures, algorithms, patterns)
- System design (caching, queues, databases, APIs, scaling)
- Language-specific hidden gems
- DevOps / tooling mastery
- Security, performance, accessibility
- Mental models (first principles, inversion, second-order thinking)
- Psychology (cognitive biases, motivation, focus, deep work)
- Communication (writing clearly, explaining tech, giving feedback)
- Career skills (estimation, code reviews, technical leadership)
- History of computing — why things are the way they are

---

## Rules
- Never repeat a topic in the same session
- Keep the initial spark SHORT — curiosity first, depth on demand
- Make the "why it matters to you" line feel genuinely personal, not generic
- For non-tech topics, always connect back to how it helps them as a developer or human
- Tone: like a brilliant friend explaining something over coffee — casual, smart, no textbook language
