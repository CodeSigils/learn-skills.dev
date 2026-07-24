---
name: skill-forge
description: Create, review, and refactor agent skills for predictable execution.
disable-model-invocation: true
---

# Purpose

Create skills that produce predictable execution paths.

# Workflow

## 1. Define boundary

Identify:

- what behavior this skill controls ?
- what is outside its scope ?

Completion: The skill scope can be describe in one sentence.

---

## 2. Select invocation mode

Choose:

- model-invoked
- user-invoked

Use model-invoked when automatic discovery is required.
Use user-invoked when explicit selection is preferred.

See: [references/invocation.md](./references/invocation.md)

Completion: Invocation mode and reason are defined.

---

## 3. Separate execution from reference

Put in SKILL.md:

- workflow
- required decisions
- completion criteria

Put in references:

- explanations
- examples
- uncommon cases

See: [references/hierarchy.md](./references/hierarchy.md)

Completion: Every piece of information has a clear location.

---

## 4. Add completion criteria

Every step must define how completion is verified.
Avoid vague instructions.

Bad:

```markdown
Check carefully.
```

Good:

```markdown
Verify every modified file has passed validation.
```

Completion: Every step has an observable done condition.

---

## 5. Remove duplication

Keep every rule in one authoritative location.

See: [references/pruning.md](./references/pruning.md)

Completion: No behavior is defined twice.

---

## 6. Apply stable terminology

Use leading words for repeated concepts.

See: [references/leading-words.md](./references/leading-words.md)

Completion: Repeated concepts use consistent names.

---

## 7. Split when predictable improves

Split by:

- invocation
- execution sequence

Only split when it improves predictability.

See: [references/splitting.md](./references/splitting.md)

Completion: Every split has a predictable reason.

---

# Validation

Before finishing:

- [ ] Scope is clear
- [ ] Invocation mode is intentional
- [ ] Steps have completion criteria
- [ ] References are progressively disclosed
- [ ] Rules have one source of truth
- [ ] No unnecessary prose remains

See: [references/failure-modes.md](./references/failure-modes.md)
