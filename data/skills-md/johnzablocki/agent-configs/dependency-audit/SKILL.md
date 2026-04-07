---
name: dependency-audit
description: "Check for outdated and vulnerable dependencies, suggest safe updates"
trigger: ["dependencies", "npm audit", "yarn audit", "update deps", "security vulnerabilities", "outdated packages"]
---

# Dependency Audit Skill

This skill checks your project dependencies for security vulnerabilities, outdated packages, and suggests safe update strategies.

## Objective

Audit project dependencies for security vulnerabilities (CVEs), check for outdated packages, analyze the impact of updates, and provide safe upgrade recommendations.

## Execution Steps

### 1. Identify Package Manager

```bash
# Check which package manager is used
ls package-lock.json yarn.lock pnpm-lock.yaml

# Determine from lock file
if [ -f "package-lock.json" ]; then
  PKG_MGR="npm"
elif [ -f "yarn.lock" ]; then
  PKG_MGR="yarn"
elif [ -f "pnpm-lock.yaml" ]; then
  PKG_MGR="pnpm"
fi
```

### 2. Run Security Audit

Check for known security vulnerabilities:

```bash
# npm
npm audit

# npm (JSON format for parsing)
npm audit --json

# yarn
yarn audit

# yarn (JSON format)
yarn audit --json

# pnpm
pnpm audit
```

**Parse audit output:**
- **Critical:** Immediate action required
- **High:** Update ASAP
- **Moderate:** Update soon
- **Low:** Update when convenient
- **Info:** Informational, no action needed

### 3. Analyze Vulnerability Details

For each vulnerability, extract:
- **Package name:** Which dependency is affected
- **Severity:** Critical/High/Moderate/Low
- **CVE ID:** Common Vulnerabilities and Exposures identifier
- **Vulnerability type:** XSS, RCE, DOS, etc.
- **Vulnerable versions:** Which versions are affected
- **Patched version:** Which version fixes it
- **Dependency path:** Direct vs transitive dependency

**Example audit output:**
```
┌───────────────┬──────────────────────────────────────────────────────────────┐
│ high          │ Prototype Pollution in lodash                                │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Package       │ lodash                                                       │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Patched in    │ >=4.17.21                                                    │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Dependency of │ some-package                                                 │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Path          │ some-package > other-package > lodash                        │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ More info     │ https://npmjs.com/advisories/1234                           │
└───────────────┴──────────────────────────────────────────────────────────────┘
```

### 4. Check for Outdated Packages

```bash
# npm
npm outdated

# yarn
yarn outdated

# pnpm
pnpm outdated
```

**Output shows:**
- **Current:** Version currently installed
- **Wanted:** Maximum version matching semver range in package.json
- **Latest:** Latest version available on registry
- **Type:** dependencies vs devDependencies

**Example:**
```
Package        Current  Wanted  Latest  Location
react          17.0.2   17.0.2  18.2.0  my-app
typescript     4.5.2    4.9.5   5.3.3   my-app
```

### 5. Categorize Update Risk

Assess risk for each update:

**🟢 Low Risk (Patch updates):**
- Version: `1.2.3` → `1.2.4`
- Type: Bug fixes only
- Action: Update immediately
- Example: `lodash@4.17.20` → `lodash@4.17.21`

**🟡 Medium Risk (Minor updates):**
- Version: `1.2.3` → `1.3.0`
- Type: New features, backwards compatible
- Action: Update after testing
- Example: `react@18.2.0` → `react@18.3.0`

**🔴 High Risk (Major updates):**
- Version: `1.2.3` → `2.0.0`
- Type: Breaking changes
- Action: Read migration guide, extensive testing
- Example: `webpack@4.46.0` → `webpack@5.90.0`

### 6. Prioritize Updates

Create update priority list:

**Priority 1 - Critical Security Issues:**
```
1. lodash (HIGH CVE) - Prototype Pollution
   Current: 4.17.15
   Fix: 4.17.21
   Impact: Direct dependency, easy update
   Action: Update immediately
```

**Priority 2 - High Security Issues:**
```
2. axios (HIGH CVE) - SSRF vulnerability
   Current: 0.21.1
   Fix: 0.21.4
   Impact: Transitive via api-client
   Action: Update this week
```

**Priority 3 - Outdated with No Vulnerabilities:**
```
3. react (No CVE) - Major update available
   Current: 17.0.2
   Latest: 18.2.0
   Impact: Major version, breaking changes
   Action: Plan migration, read docs
```

### 7. Apply Safe Updates

Update strategy based on risk:

#### Automatic Fixes (Low Risk)
```bash
# npm - auto-fix security issues
npm audit fix

# yarn
yarn upgrade --pattern lodash
yarn upgrade --pattern axios

# pnpm
pnpm update lodash
```

#### Targeted Updates (Medium Risk)
```bash
# Update specific package to specific version
npm install package@1.3.0
yarn add package@1.3.0
pnpm add package@1.3.0

# Update to latest compatible version
npm update package
```

#### Manual Updates (High Risk)
```bash
# Update package.json manually
"react": "^18.0.0"

# Install
npm install

# Follow migration guide
# Run tests extensively
# Update code for breaking changes
```

### 8. Handle Transitive Dependencies

When vulnerability is in a transitive dependency:

**Check dependency tree:**
```bash
npm ls lodash
yarn why lodash
pnpm why lodash
```

**Options to fix:**
1. **Update parent package** (if available)
2. **Use resolutions/overrides** (force specific version)
3. **Contact maintainer** (if parent is unmaintained)

**npm overrides (package.json):**
```json
{
  "overrides": {
    "lodash": "4.17.21"
  }
}
```

**yarn resolutions (package.json):**
```json
{
  "resolutions": {
    "lodash": "4.17.21"
  }
}
```

### 9. Test After Updates

**Critical testing steps:**
```bash
# 1. Install dependencies
npm install

# 2. Run linter
npm run lint

# 3. Run type checking (TypeScript)
npm run type-check || tsc --noEmit

# 4. Run unit tests
npm test

# 5. Run integration tests
npm run test:integration

# 6. Run E2E tests (critical paths)
npm run test:e2e

# 7. Build the project
npm run build

# 8. Manual testing of key features
```

### 10. Generate Audit Report

```
🔒 Dependency Audit Report
Date: 2024-02-14

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Dependencies: 234
  - Direct: 45
  - Transitive: 189

Vulnerabilities Found: 5
  - Critical: 0
  - High: 2
  - Moderate: 2
  - Low: 1

Outdated Packages: 23
  - Major updates: 5
  - Minor updates: 12
  - Patch updates: 6

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 HIGH PRIORITY (Action Required)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. lodash - Prototype Pollution (HIGH)
   CVE: CVE-2021-23337
   Current: 4.17.15
   Fixed in: 4.17.21
   Path: api-client > lodash
   Impact: Allows attacker to modify object prototype
   Action: ✅ FIXED - Updated to 4.17.21

2. axios - SSRF Vulnerability (HIGH)
   CVE: CVE-2023-45857
   Current: 0.21.1
   Fixed in: 1.6.0
   Path: Direct dependency
   Impact: Server-side request forgery
   Action: ✅ FIXED - Updated to 1.6.2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  MODERATE PRIORITY (Update Soon)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. semver - ReDoS Vulnerability (MODERATE)
   Current: 7.3.5
   Fixed in: 7.5.2
   Action: Update in next sprint

4. json5 - Prototype Pollution (MODERATE)
   Current: 2.2.0
   Fixed in: 2.2.3
   Action: Update in next sprint

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 OUTDATED PACKAGES (No Security Issues)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Major Updates (Breaking Changes):
  - react: 17.0.2 → 18.2.0
  - webpack: 4.46.0 → 5.90.0
  - jest: 27.5.1 → 29.7.0

Minor Updates (New Features):
  - typescript: 4.9.5 → 5.3.3
  - eslint: 8.50.0 → 8.56.0
  - prettier: 2.8.8 → 3.1.1

Patch Updates (Bug Fixes):
  - express: 4.18.2 → 4.18.3
  - dotenv: 16.3.1 → 16.4.1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ ACTIONS TAKEN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Updated lodash: 4.17.15 → 4.17.21
2. Updated axios: 0.21.1 → 1.6.2
3. Updated 6 patch-level packages (safe updates)
4. Ran test suite - all tests passing ✓
5. Built project successfully ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 RECOMMENDED NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Update semver and json5 (moderate vulnerabilities)
2. Review react 18 migration guide for major update
3. Plan webpack 5 upgrade (breaking changes)
4. Schedule regular dependency audits (monthly)
5. Consider using Dependabot for automated PR updates

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Success Criteria

- All critical and high vulnerabilities resolved
- Dependencies updated without breaking functionality
- Tests pass after updates
- Application builds successfully
- No new vulnerabilities introduced
- Lock file updated and committed

## Best Practices

### DO:
- ✅ Audit dependencies regularly (weekly/monthly)
- ✅ Fix critical/high vulnerabilities immediately
- ✅ Test thoroughly after updates
- ✅ Update lock files
- ✅ Read changelogs and migration guides for major updates
- ✅ Keep dev dependencies updated too
- ✅ Use automated tools (Dependabot, Renovate)
- ✅ Document breaking changes in team communication

### DON'T:
- ❌ Ignore security vulnerabilities
- ❌ Update everything at once without testing
- ❌ Update to latest without checking breaking changes
- ❌ Skip reading migration guides for major versions
- ❌ Update production without testing in staging
- ❌ Leave outdated dependencies indefinitely
- ❌ Trust "npm audit fix --force" blindly
- ❌ Update peer dependencies without parent package

## Handling Special Cases

### Unmaintained Packages
If a package has critical vulnerability but no fix:
1. Check for maintained alternatives
2. Search for community forks
3. Consider in-house patching (last resort)
4. Remove package if possible

### Conflicting Dependencies
When updates cause conflicts:
```bash
# Check why package is needed
npm ls package-name

# Try updating peer dependencies first
npm update

# Use overrides/resolutions carefully
# Document why override is needed
```

### Major Version Updates
For breaking changes:
1. Read official migration guide
2. Check breaking changes in changelog
3. Update in separate branch
4. Test extensively
5. Update gradually (one major package at a time)

### False Positives
Some vulnerabilities may not apply:
- Only affects dev environment
- Requires specific attack scenario
- Already mitigated by other code

Document why you're not fixing it if you skip.

## Automation

### GitHub Dependabot
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "your-team"
    labels:
      - "dependencies"
```

### Renovate Bot
```json
{
  "extends": ["config:base"],
  "schedule": ["before 3am on Monday"],
  "automerge": true,
  "automergeType": "pr",
  "major": {
    "automerge": false
  },
  "packageRules": [
    {
      "matchUpdateTypes": ["patch", "pin", "digest"],
      "automerge": true
    }
  ]
}
```

### CI/CD Integration
```yaml
# .github/workflows/security-audit.yml
name: Security Audit

on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  push:
    branches: [main]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm audit --audit-level=moderate
      - run: npm outdated || true
```

## Common Vulnerabilities

### Prototype Pollution
**Risk:** Attacker can modify Object.prototype
**Fix:** Update package, validate inputs, use Map instead of objects

### Cross-Site Scripting (XSS)
**Risk:** Inject malicious scripts
**Fix:** Update package, sanitize inputs, use CSP headers

### Regular Expression Denial of Service (ReDoS)
**Risk:** Malicious regex causes CPU exhaustion
**Fix:** Update package, limit regex complexity, timeout regexes

### SQL Injection
**Risk:** Execute arbitrary SQL queries
**Fix:** Use parameterized queries, update ORM

### Remote Code Execution (RCE)
**Risk:** Execute arbitrary code on server
**Fix:** Update immediately, validate inputs, sandbox execution

## Useful Commands

```bash
# View full dependency tree
npm ls --all

# Check specific package
npm view package-name versions
npm view package-name dist-tags

# Remove unused dependencies
npm prune
npx depcheck

# Check license compliance
npx license-checker

# Analyze bundle size
npx webpack-bundle-analyzer

# Check for circular dependencies
npx madge --circular src/

# Update interactive (choose what to update)
npx npm-check -u
```

## Notes

- Always read changelogs before major updates
- Security over convenience - fix vulnerabilities even if inconvenient
- Keep dependencies minimal - less to maintain and audit
- Regular audits prevent large, risky updates later
- Document all overrides and why they're needed
- Test in staging before production updates
