---
name: lint-fix
description: "Run linter (ESLint/Prettier), identify issues, and automatically fix them"
trigger: ["lint", "eslint", "prettier", "fix formatting", "code style", "linting errors"]
---

# Lint Fix Skill

This skill runs code linters and formatters, detects code quality issues, and automatically fixes them where possible.

## Objective

Execute linting tools (ESLint, Prettier, or project-specific linters) to identify and automatically fix code style, formatting, and quality issues.

## Execution Steps

### 1. Detect Project Configuration

**Check for linting tools:**
```bash
# Look for ESLint
ls .eslintrc* eslint.config.* package.json

# Look for Prettier
ls .prettierrc* prettier.config.* package.json

# Check package.json scripts
grep -E "\"(lint|format|eslint|prettier)\"" package.json
```

**Common configurations:**
- ESLint: `.eslintrc.js`, `.eslintrc.json`, `eslint.config.js`
- Prettier: `.prettierrc`, `.prettierrc.json`, `prettier.config.js`
- Both: Often used together

### 2. Run Linter in Check Mode

Run linter first to see what issues exist:

```bash
# ESLint
npm run lint || yarn lint || npx eslint . || eslint .

# If specific paths are needed
npx eslint src/ --ext .js,.jsx,.ts,.tsx

# Prettier
npm run format:check || npx prettier --check "**/*.{js,jsx,ts,tsx,json,css,md}"
```

Capture the output to analyze issues.

### 3. Analyze Linting Errors

Parse the output for error categories:

**ESLint Error Types:**
- **Formatting:** Indentation, spacing, quotes, semicolons
- **Code Quality:** Unused vars, console.logs, debugger statements
- **Best Practices:** no-var, prefer-const, eqeqeq
- **TypeScript:** @typescript-eslint rules
- **React:** react-hooks rules, jsx-a11y rules
- **Security:** no-eval, no-unsafe-regex

**Example ESLint Output:**
```
src/components/Button.tsx
  12:5  error  'React' is defined but never used  no-unused-vars
  15:3  error  Unexpected console statement      no-console
  18:5  warning  Missing JSDoc comment            jsdoc/require-jsdoc
```

Extract:
- File path
- Line number
- Rule name
- Error message
- Severity (error/warning)

### 4. Apply Automatic Fixes

Try automatic fixes first (safest approach):

```bash
# ESLint auto-fix
npm run lint:fix || npx eslint . --fix

# Prettier auto-format
npm run format || npx prettier --write "**/*.{js,jsx,ts,tsx,json,css,md}"

# Run both (if project uses both)
npx prettier --write . && npx eslint . --fix
```

**What auto-fix handles:**
- ✅ Indentation and spacing
- ✅ Quotes (single vs double)
- ✅ Semicolons (add/remove)
- ✅ Trailing commas
- ✅ Line breaks
- ✅ Import sorting
- ✅ Some simple code transformations

### 5. Manual Fixes for Remaining Issues

If errors remain after auto-fix, manually address them:

#### Unused Variables
```typescript
// Error: 'foo' is defined but never used
const foo = 'bar';

// Fix: Remove if truly unused
// Or prefix with underscore if intentionally unused (for function params)
const _foo = 'bar';
```

#### Console Statements
```typescript
// Error: Unexpected console statement
console.log('Debug info');

// Fix Options:
// 1. Remove if debugging statement
// 2. Replace with proper logger
logger.debug('Debug info');
// 3. Add eslint-disable if intentional
// eslint-disable-next-line no-console
console.log('Critical user message');
```

#### Missing Dependencies (React Hooks)
```typescript
// Error: React Hook useEffect has a missing dependency: 'count'
useEffect(() => {
  setTotal(count * 2);
}, []);

// Fix: Add to dependency array
useEffect(() => {
  setTotal(count * 2);
}, [count]);
```

#### Type Issues (TypeScript ESLint)
```typescript
// Error: Unsafe assignment of an 'any' value
const data: any = fetchData();
const value = data.value;

// Fix: Use proper types
interface Data {
  value: string;
}
const data: Data = fetchData();
const value = data.value;
```

### 6. Handle Configuration Conflicts

If ESLint and Prettier conflict:

```bash
# Install eslint-config-prettier to disable conflicting ESLint rules
npm install --save-dev eslint-config-prettier

# Add to .eslintrc.json extends
{
  "extends": [
    "eslint:recommended",
    "prettier" // Must be last
  ]
}
```

### 7. Verify Fixes

After applying fixes, run linter again:

```bash
# Should pass with no errors
npm run lint
npm run format:check

# If still failing, investigate remaining issues
```

### 8. Report Results

Provide a summary:
```
✅ Linting Complete

Fixed Automatically:
- 23 formatting issues (indentation, spacing)
- 5 import sorting issues
- 3 trailing comma additions

Fixed Manually:
- Removed 2 unused variables (src/utils/helpers.ts)
- Replaced console.log with logger (src/api/users.ts)
- Added missing useEffect dependency (src/components/UserList.tsx)

Remaining Issues:
- None! All linting checks pass ✨

Files Modified:
- src/components/Button.tsx
- src/components/UserList.tsx
- src/utils/helpers.ts
- src/api/users.ts
```

## Success Criteria

- Linter exits with code 0 (no errors)
- Formatter check passes
- No eslint-disable comments added unnecessarily
- Code maintains original functionality
- All fixes follow project's style guide

## Common Linting Rules & Fixes

### JavaScript/TypeScript

| Rule | Issue | Fix |
|------|-------|-----|
| `no-unused-vars` | Variable declared but not used | Remove or prefix with `_` |
| `no-console` | Console statement in code | Remove or use proper logger |
| `no-var` | Using `var` instead of `let`/`const` | Replace with `const` or `let` |
| `prefer-const` | `let` for variable never reassigned | Change to `const` |
| `eqeqeq` | Using `==` instead of `===` | Use strict equality `===` |
| `no-debugger` | Debugger statement in code | Remove |

### React

| Rule | Issue | Fix |
|------|-------|-----|
| `react-hooks/exhaustive-deps` | Missing dependency in useEffect | Add to dependency array |
| `react/prop-types` | Missing prop-types definition | Add PropTypes or use TypeScript |
| `react/jsx-key` | Missing key prop in list | Add unique key prop |
| `jsx-a11y/alt-text` | Image missing alt text | Add alt attribute |

### TypeScript

| Rule | Issue | Fix |
|------|-------|-----|
| `@typescript-eslint/no-explicit-any` | Using `any` type | Use specific type or `unknown` |
| `@typescript-eslint/no-unused-vars` | Unused variable | Remove or mark as intentional |
| `@typescript-eslint/explicit-function-return-type` | Missing return type | Add return type annotation |

## Constraints & Best Practices

### DO:
- ✅ Run auto-fix first before manual changes
- ✅ Understand what each rule is enforcing
- ✅ Preserve code functionality
- ✅ Follow project's existing patterns
- ✅ Run tests after fixing to ensure nothing broke
- ✅ Commit linting fixes separately from feature changes

### DON'T:
- ❌ Add `eslint-disable` comments everywhere
- ❌ Remove rules from config to make errors go away
- ❌ Change business logic while fixing style issues
- ❌ Mix linting fixes with feature changes in same commit
- ❌ Ignore warnings without understanding them
- ❌ Auto-fix everything blindly (review changes)

## Handling Edge Cases

### Large Codebase
For projects with many files:
```bash
# Fix one directory at a time
npx eslint src/components --fix
npx eslint src/utils --fix

# Or use staged files only
npx lint-staged
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Lint Check
  run: |
    npm run lint
    npm run format:check

# Auto-fix and commit (be careful!)
- name: Auto-fix
  run: |
    npm run lint:fix
    npm run format
- uses: stefanzweifel/git-auto-commit-action@v4
  with:
    commit_message: "style: auto-fix linting issues"
```

### Conflicting Rules
If rules conflict, prioritize:
1. **Prettier** for formatting (spacing, quotes, etc.)
2. **ESLint** for code quality (unused vars, best practices)
3. **TypeScript** for type safety

## File Types Supported

- **JavaScript:** `.js`, `.mjs`, `.cjs`
- **TypeScript:** `.ts`, `.tsx`, `.d.ts`
- **React:** `.jsx`, `.tsx`
- **Vue:** `.vue` (with eslint-plugin-vue)
- **JSON:** `.json` (Prettier)
- **CSS:** `.css`, `.scss`, `.less` (stylelint)
- **Markdown:** `.md` (Prettier)

## Dependencies

This skill requires:
- Node.js and npm/yarn installed
- ESLint and/or Prettier configured in project
- Project dependencies installed (`npm install`)

## Usage Examples

### Basic Usage
```
"Run lint-fix to clean up the code style"
```

### After Feature Development
```
"I just finished the new feature. Run lint-fix to ensure code quality before committing"
```

### CI/CD Failure
```
"The linting check failed in CI. Can you fix all the issues?"
```

### Pre-Commit
```
"Before I commit these changes, run lint-fix to make sure everything is formatted correctly"
```

## Notes

- This skill modifies files in place - ensure you have a clean git state or can revert changes
- Some linting errors require human judgment (e.g., whether a variable is truly unused)
- Always run tests after linting fixes to ensure functionality is preserved
- Consider using husky + lint-staged to auto-fix on commit
