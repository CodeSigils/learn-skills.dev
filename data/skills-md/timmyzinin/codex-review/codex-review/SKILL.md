---
name: codex-review
description: "Run independent Codex code review on current changes. Use when user says '/codex-review', 'codex review', 'ревью кодексом', 'проверь кодексом', or wants independent AI review."
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# /codex-review — Независимый code review через OpenAI Codex

Запускает Codex CLI в sandboxed read-only mode для независимого review.

## Аргументы

- `/codex-review` — ревью текущих изменений (staged → unstaged)
- `/codex-review security` — фокус на безопасности
- `/codex-review path/to/file.py` — ревью конкретного файла
- `/codex-review "любой текст"` — кастомный фокус
- `/codex-review --yolo` — без sandbox (только по явному запросу пользователя)

## Протокол

### 1. Prerequisites

```bash
set -euo pipefail
command -v codex >/dev/null 2>&1 || { echo "ERROR: codex not installed. Run: npm install -g @openai/codex"; exit 1; }
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "ERROR: not inside git repo"; exit 1; }
```

### 2. Определить scope

```bash
STAGED=$(git diff --cached --stat)
UNSTAGED=$(git diff --stat)
```

- Есть staged → scope = `git diff --cached`
- Есть unstaged → scope = `git diff`
- Оба есть → scope = оба
- Оба пусты → показать `git log --oneline -5` и СПРОСИТЬ пользователя какой коммит/range ревьюить. **Без явного scope — не запускать.**

Если аргумент — путь к файлу: проверить что файл существует (`test -f`) и находится внутри текущего git repo (`git ls-files --error-unmatch`). Если нет — сообщить ошибку и не запускать.

### 3. Запомнить состояние repo

```bash
set -euo pipefail
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
git status --porcelain > /tmp/codex-review-pre-${TIMESTAMP}.txt
```

### 4. Собрать prompt

Через bash heredoc записать в `/tmp/codex-review-prompt-${TIMESTAMP}.md`:

```
You are an independent code reviewer performing READ-ONLY analysis.

## HARD CONSTRAINTS — violation of any = failed review
- Do NOT modify, create, or delete any files
- Do NOT run git checkout, git reset, git commit, git rebase, git stash, git push
- Do NOT run formatters, linters with --fix, or any auto-fix tools
- Do NOT install or remove dependencies
- Do NOT apply patches or write to any file in the repository
- Do NOT spawn sub-agents unless explicitly requested
- You MAY ONLY run: git diff, git log, git show, cat, head, tail, grep, find, tree, wc, file

## Task
Review the code changes in this repository.

### Gather context
- `git diff --cached` (staged changes)
- `git diff` (unstaged changes)
{EXPLICIT_RANGE_IF_USER_SPECIFIED}
- Read modified files in full for surrounding context

{CUSTOM_FOCUS}

### Review criteria
For each changed area check:
- **Correctness:** Logic errors, off-by-one, null/undefined, race conditions, unhandled edge cases
- **Security:** Injection (SQL, XSS, command), hardcoded secrets, broken auth/authz, SSRF, path traversal
- **Architecture:** Coupling, separation of concerns, naming, duplication
- **Tests:** Missing tests for new code, uncovered edge cases

### Output rules
- Findings first, ordered by severity: CRITICAL → HIGH → MEDIUM → LOW
- Only include issues justifiable from actual diff and code context
- Include file:line reference when possible
- Do NOT praise the code
- Do NOT invent metrics (coverage %, complexity scores, performance numbers)
- Do NOT speculate about intentions — only report what is observable
- If no issues found, say "No issues found" — do not pad with filler

### Output format
Write to stdout only. Do NOT create files.

CODEX REVIEW

VERDICT: APPROVED | NEEDS_CHANGES (N critical, M high)

FINDINGS:

[CRITICAL] Title
File: path/to/file.py:42
Issue: Description
Fix: Concrete suggestion

[HIGH] Title
...

[MEDIUM] Title
...

[LOW] Title
...
```

Подстановки `{CUSTOM_FOCUS}`:
- `security` → "Focus primarily on security: OWASP Top 10, secrets, injection, auth bypass"
- путь к файлу → "Focus on file: {path}. Read it fully."
- произвольный текст → вставить как есть

### 5. Запустить Codex

Определить флаги — приоритет:
1. Если пользователь передал `--yolo` → `CODEX_FLAGS="--dangerously-bypass-approvals-and-sandbox"` (ничто не переопределяет)
2. Иначе если задан env var `REVIEW_CODEX_FLAGS` → использовать его
3. Иначе дефолт → `CODEX_FLAGS="-s read-only"`

Запуск Bash tool с **timeout 600000**:

```bash
set -euo pipefail
codex exec ${CODEX_FLAGS} - < /tmp/codex-review-prompt-${TIMESTAMP}.md 2>/tmp/codex-review-stderr-${TIMESTAMP}.txt | tee /tmp/codex-review-output-${TIMESTAMP}.txt
```

### 6. Проверить что Codex не навредил

```bash
set -euo pipefail
git status --porcelain > /tmp/codex-review-post-${TIMESTAMP}.txt
if ! diff -q /tmp/codex-review-pre-${TIMESTAMP}.txt /tmp/codex-review-post-${TIMESTAMP}.txt >/dev/null 2>&1; then
  echo "WARNING: Codex modified files:"
  git status --short
  git diff --name-only
fi
```

Если файлы изменились:
- Показать пользователю `git status --short` и `git diff --name-only`
- **НЕ откатывать автоматически** — пользователь решает сам

### 7. Показать результат

Прочитать `/tmp/codex-review-output-${TIMESTAMP}.txt`.

Формат вывода пользователю:
- **Всегда:** VERDICT + summary (кол-во findings по severity)
- **Полностью:** CRITICAL и HIGH findings
- **Кратко (только заголовок + file):** MEDIUM и LOW
- **По запросу:** полный текст medium/low если пользователь попросит

Если stderr не пустой — показать ошибки.

### 8. Предложить действия

Если NEEDS_CHANGES → "Исправить critical/high findings?"
Если APPROVED → сообщить и закончить.
