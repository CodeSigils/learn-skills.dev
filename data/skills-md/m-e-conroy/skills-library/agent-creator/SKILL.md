---
name: agent-creator
description: Create and refine AI agent definition files (.agent.md) with clear personas, executable commands, code style examples, project structure, git workflows, and explicit boundaries. Use this skill whenever the user wants to create a new agent, write an agent.md file, define an AI agent's persona or operating manual, set up agent boundaries, or scaffold agent tooling configuration. Also triggers on "make me an agent", "agent definition", "agent instructions", or any request to define how an AI assistant should behave in a specific codebase.
---

# Agent Creator

Build complete `.agent.md` files that give AI agents a clear identity and a precise operating manual for a codebase.

An effective agent file is not a vague description — it's a **concrete playbook**. The agent should know exactly what commands to run, how to style code, where files live, which files to never touch, and how to interact with version control. Without this specificity, agents guess, and guessing produces inconsistent results.

> **Template reference:** See `references/dev-agent.tmpl.md` for the full annotated agent template covering all six core areas.

---

## Agent File Format

Agent files live in `.github/agents/` and use this structure:

```markdown
---
name: agent-name
description: One-sentence purpose. This is the trigger — make it specific.
tools: [tool1, tool2]
---

# Agent body — the operating manual
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Kebab-case identifier (e.g., `frontend-dev`, `test-engineer`) |
| `description` | Yes | What the agent does + when it should activate. Be specific and slightly "pushy" so it triggers reliably. |
| `tools` | No | Array of tool categories the agent can use. Omit to allow all enabled tools. |

---

## The Six Core Areas

Every agent operating manual should cover these six areas. The depth of each section depends on the project, but none should be skipped entirely.

### 1. Commands

Give the agent the exact shell commands it needs. Never assume it knows your scripts.

```markdown
## Commands
- **Dev server:** `npm run dev` (Vite, port 3000)
- **Build:** `npm run build` (TypeScript → dist/)
- **Test all:** `npm test` (Jest, must pass before PR)
- **Test single:** `npm test -- --testPathPattern=<file>`
- **Lint:** `npm run lint` (ESLint + Prettier)
- **Lint fix:** `npm run lint --fix`
- **Type check:** `npx tsc --noEmit`
- **DB migrate:** `npx prisma migrate dev`
```

Include every command the agent might need: build, test, lint, type-check, migrations, deployment, codegen. Specify what each does and any flags that matter.

### 2. Testing

Tell the agent how to write tests, where they go, what framework and patterns to use:

```markdown
## Testing
- Framework: **Vitest** with React Testing Library
- Unit tests colocate next to source: `Button.test.tsx` beside `Button.tsx`
- Integration tests in `tests/integration/`
- Always run `npm test` before marking work complete
- Test naming: `describe('ComponentName', () => { it('should ...') })`
- Mock API calls with **MSW** handlers in `src/test-utils/mocks/handlers.ts`
- Minimum coverage: 80% on new code
```

Include a concrete test example so the agent sees the pattern:

~~~markdown
```tsx
import { render, screen } from "@testing-library/react";
import { Button } from "./Button";

describe("Button", () => {
  it("should render with the provided label", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole("button", { name: /click me/i })).toBeInTheDocument();
  });
});
```
~~~

### 3. Project Structure

Map out where files live so the agent places new code correctly:

```markdown
## Project Structure
```
src/
├── features/          # Feature modules (auth/, dashboard/, settings/)
│   └── [feature]/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       └── index.ts   # Public API barrel
├── shared/            # Cross-feature code (components/, hooks/, utils/)
├── layouts/           # Page layout shells
├── pages/             # Route entry points
├── styles/            # Global CSS, tokens, themes
├── lib/               # Third-party wrappers
└── config/            # App config, feature flags
tests/
├── integration/
├── e2e/
└── fixtures/
```
```

Be explicit about where new components, hooks, services, and tests should go.

### 4. Code Style

Don't just name conventions — show them with contrasting examples:

```markdown
## Code Style

**Naming:**
- Components: PascalCase (`UserProfile.tsx`)
- Hooks: camelCase with `use` prefix (`useAuth.ts`)
- Utils: camelCase (`formatDate.ts`)
- Constants: UPPER_SNAKE_CASE (`MAX_RETRIES`)
- CSS: BEM or CSS Modules (`.card__header--active`)

**Example — the pattern we follow:**
```typescript
// ✅ Good — explicit types, error handling, descriptive names
async function fetchUserById(id: string): Promise<User> {
  if (!id) throw new Error("User ID is required");
  const response = await api.get<User>(`/users/${id}`);
  return response.data;
}

// ❌ Bad — implicit any, no validation, cryptic names
async function get(x) {
  return await api.get("/users/" + x).data;
}
```
```

Include framework-specific patterns if the project uses one (e.g., React hooks conventions, Vue composable patterns).

### 5. Git Workflow

Define branching strategy, commit format, and PR expectations:

```markdown
## Git Workflow
- Branch from `main`: `feat/<topic>`, `fix/<topic>`, `chore/<topic>`
- Commits: Conventional Commits — `feat(auth): add login form`
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Before pushing: `npm run lint && npm test && npx tsc --noEmit`
- PR title matches commit format
- Squash merge to main
```

### 6. Boundaries

The most critical section. Agents need explicit guardrails — what they can do freely, what requires confirmation, and what they must never do:

```markdown
## Boundaries

✅ **Always (do freely):**
- Read and write files in `src/` and `tests/`
- Run tests, lint, and type-check
- Create new components, hooks, and utilities
- Fix lint errors and type errors

⚠️ **Ask first (get confirmation):**
- Adding new dependencies to `package.json`
- Modifying database schemas or migrations
- Changing CI/CD configuration (`.github/workflows/`)
- Altering shared types that affect multiple features
- Modifying environment variable definitions

🚫 **Never (hard boundaries):**
- Edit `node_modules/`, `dist/`, or any build output
- Commit secrets, API keys, or credentials
- Delete or overwrite `.env` files
- Modify lock files (`package-lock.json`) manually
- Push directly to `main` or `production` branches
- Change authentication or authorization logic without review
```

---

## Writing Process

### Step 1: Interview the User

Gather the information needed to fill all six areas. Key questions:

1. **What is the agent's role?** (frontend dev, test engineer, docs writer, DevOps...)
2. **What's the tech stack?** (Languages, frameworks, versions, package manager)
3. **What are the key commands?** (Dev, build, test, lint, deploy)
4. **Where does code live?** (Folder structure, naming patterns)
5. **What coding conventions do you follow?** (Style guide, linting rules, patterns)
6. **What's the git workflow?** (Branching model, commit format, CI checks)
7. **What should the agent never do?** (Files to protect, actions requiring approval)

If the user can't answer everything, research the codebase — read `package.json`, check for config files, inspect the folder tree, and infer conventions from existing code.

### Step 2: Define the Persona

Write 2–3 sentences establishing who the agent is:

```markdown
You are a senior frontend engineer specializing in React and TypeScript.
You write accessible, well-tested components following this project's conventions.
You prioritize semantic HTML, comprehensive test coverage, and clean git history.
```

The persona frames the agent's decision-making style. A "test engineer" agent writes tests first. A "docs writer" agent prioritizes clarity over brevity. Match the persona to the role.

### Step 3: Draft the Agent File

Write the full `.agent.md` using the six core areas. Reference `references/dev-agent.tmpl.md` for the expected structure.

Aim for **specificity over length** — a 50-line agent with exact commands and real code examples outperforms a 200-line agent full of generic advice.

### Step 4: Validate

After drafting, verify:

- [ ] Every command is copy-pasteable and correct for the project
- [ ] Code examples match the project's actual style and patterns
- [ ] Boundaries are explicit — no ambiguity about what requires approval
- [ ] File paths reference real project locations
- [ ] The persona aligns with the agent's intended role

---

## Agent File Placement

```
.github/
└── agents/
    ├── frontend-dev.agent.md
    ├── test-engineer.agent.md
    ├── docs-writer.agent.md
    └── devops.agent.md
```

One agent file per role. Keep each focused on a single responsibility.

---

## Common Agent Types

| Agent | Persona | Key Focus Areas |
|-------|---------|----------------|
| **Frontend Dev** | Senior React/Vue/Svelte engineer | Components, hooks, accessibility, styling |
| **Backend Dev** | API/services engineer | Routes, database, validation, error handling |
| **Test Engineer** | QA specialist | Test coverage, test patterns, mocking, CI |
| **Docs Writer** | Technical writer | README, API docs, JSDoc, architecture docs |
| **DevOps** | Infrastructure engineer | CI/CD, Docker, deployment, monitoring |
| **Security Reviewer** | Security analyst | Auth, input validation, dependency audits |

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Vague commands ("run the tests") | Exact commands (`npm test -- --coverage`) |
| No code examples | Show ✅/❌ contrasting examples in the project's actual style |
| Missing boundaries | Always include the ✅/⚠️/🚫 boundary tiers |
| Generic persona ("you are helpful") | Specific role ("senior React engineer focused on accessibility") |
| Assume the agent knows the stack | List tech, versions, and framework conventions explicitly |
| One massive agent for everything | Separate agents per role — composable and focused |