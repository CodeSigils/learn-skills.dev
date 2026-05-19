---
name: codebase-exploration
description: "I am a new developer onboarding onto this codebase. I want to explore it through its primary use cases first. Explore this repository and identify the most common, essential, and core use cases."
tools:
  [vscode, execute, read, agent, edit, search, web, browser, neon/search, todo]
---

### **Objectives**

Identify and document the repository's primary functionalities and workflows to facilitate developer onboarding.

### **Guardrails**

- Ground every use case in files, routes, tests, docs, or observed behavior.
- Label assumptions and unknowns instead of filling gaps with guesses.
- Prefer the smallest useful onboarding map: core flows first, peripheral features later.
- Do not modify source code while exploring.

#### **Required Content**

1. **Core Use Cases:** An ordered list of the most essential and frequent use cases supported by the codebase.
2. **User Journeys:** Descriptions of typical end-to-end user paths through the system.

---

### **Execution Workflow**

1. **Repository Exploration:** Use `codebase` and `search` to map high-level architecture.
2. **Context Gathering:** Identify entry points and core logic using `usages` and `findTestFiles`.
3. **Documentation:** Synthesize findings into the specified sections.
4. **Persistence:** Write the final analysis to `.planning/system/use_cases.md`.

---
---

> **Install:** ``npx skills add ChristopherAlphonse/calphonse-skills --skill codebase-exploration``
