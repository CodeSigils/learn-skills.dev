---
name: security-review
description: Use after building an application and before launch to audit security - covers database RLS policies, input sanitization, authentication hardening, API security, environment variable exposure, rate limiting, dependency vulnerabilities, and infrastructure configuration with user approval at each area.
---

# Security Review

## Overview

Comprehensive security audit for startup MVPs before going live. Covers the most critical vulnerabilities that affect early-stage apps. Run this after the app is built but before launch - it pairs with the pre-launch checklist in `/launch-planner`.

Outputs a `SECURITY-REPORT.md` after all areas are reviewed.

## Prerequisites

Ask the user for:
- Tech stack (frontend framework, backend language/framework)
- Database (Supabase/Postgres, MySQL, MongoDB, Firebase, etc.)
- Auth provider (Supabase Auth, Clerk, Auth0, NextAuth, custom, etc.)
- API type (REST, GraphQL, tRPC, server actions)
- Hosting target (Vercel, Railway, Fly.io, AWS, etc.)
- Any known concerns or areas they're unsure about

Ask them to share relevant code files or paste code snippets as each area is reviewed.

---

## Area 1: Database Security (RLS + Access Control)

**For Supabase / PostgreSQL with RLS:**

Checklist - review each item against their actual schema and policies:
- [ ] RLS is enabled on ALL tables - run: `SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';`
- [ ] RLS policies exist for every CRUD operation that touches user data
- [ ] Policies tested as the anon role (what can an unauthenticated user see?)
- [ ] Policies tested as an authenticated user (can user A read user B's data?)
- [ ] No table has a policy of `USING (true)` unless it's intentionally public
- [ ] Service role key is NEVER in client-side code or exposed to the browser
- [ ] Anon key only has the minimum required permissions

**Ask the user to share their RLS policies for:**
- users / profiles table
- Any table containing sensitive user data
- Any table with financial or PII data

**Test queries to suggest:**
```sql
-- Test anon access (run in Supabase SQL editor as anon role)
SET ROLE anon;
SELECT * FROM users LIMIT 1;  -- Should return empty or error

-- Test cross-user access (run as authenticated with a test user ID)
SET ROLE authenticated;
SET request.jwt.claims = '{"sub": "other-user-id"}';
SELECT * FROM orders WHERE user_id = 'your-own-user-id';  -- Should return empty
```

**For non-Supabase databases:**
- Are all queries using an ORM or parameterized statements? (prevents SQL injection)
- Is there a concept of "as this user" for all data access?
- Are admin queries separated from user queries at the connection level?

**STOP.**
```
Area 1 complete. Findings above.
Type APPROVE to continue to Area 2, or share code/policies to discuss further.
```

---

## Area 2: Authentication Security

Checklist:
- [ ] Session tokens are in httpOnly, Secure cookies - NOT localStorage or sessionStorage
- [ ] JWT expiry is set (not infinite) - what is the access token TTL?
- [ ] Refresh token rotation enabled (old refresh token invalidated on use)
- [ ] Password minimum requirements enforced server-side (not just client-side)
- [ ] Email verification required before user can access the app
- [ ] OAuth redirect URIs are strictly allowlisted (no wildcard `*`)
- [ ] Every API route / server action checks authentication - no unprotected routes
- [ ] Rate limiting on login, signup, and password reset endpoints
- [ ] Account lockout after N failed login attempts (or CAPTCHA)

**For Supabase Auth specifically:**
- [ ] Email confirmations enabled in dashboard
- [ ] Password recovery flow tested end-to-end
- [ ] `auth.users` table protected - users cannot read other users' auth records
- [ ] No direct modifications to `auth` schema

**Ask the user to show:**
- How they check auth on a typical protected API route or server action
- Their login rate limiting setup (or confirm it doesn't exist yet)

**STOP.**
```
Area 2 complete. Findings above.
Type APPROVE to continue to Area 3, or share code to review.
```

---

## Area 3: Input Sanitization + Injection Prevention

**SQL Injection:**
- [ ] All database queries use parameterized queries, prepared statements, or ORM methods
- [ ] No raw SQL string concatenation with user-provided values: `"SELECT * FROM users WHERE id = " + userId` is a critical vulnerability
- [ ] Search/filter inputs are escaped or passed as parameters

**XSS (Cross-Site Scripting):**
- [ ] User-generated content is never rendered as raw HTML
- [ ] Any use of `dangerouslySetInnerHTML` in React is sanitized with DOMPurify first
- [ ] Rich text editors (Quill, TipTap, etc.) sanitize output before storing and before rendering
- [ ] URLs from user input are validated before using as `href` or `src`

**File Uploads:**
- [ ] File type validated server-side by MIME type inspection - not just by file extension (extensions are spoofable)
- [ ] File size limits enforced server-side
- [ ] Uploaded files stored in object storage (S3, Supabase Storage) - never on the filesystem with execution permission
- [ ] Uploaded file names sanitized before storage (strip path traversal: `../`)
- [ ] Uploaded files not served from the same domain as the app (prevents cookie theft)

**Command Injection:**
- [ ] No `exec()`, `eval()`, `child_process.exec()` with user input
- [ ] Any shell commands use argument arrays, not string interpolation

**Ask the user to show any code that:**
- Accepts file uploads
- Renders user-provided content as HTML
- Constructs database queries with user input

**STOP.**
```
Area 3 complete. Findings above.
Type APPROVE to continue to Area 4, or share code to review.
```

---

## Area 4: API Security

**Authentication + Authorization:**
- [ ] Every endpoint checks authentication (session/JWT present and valid)
- [ ] Every endpoint checks authorization (does this user own this resource?)
- [ ] Authentication != Authorization - passing auth check doesn't mean they can do everything
- [ ] Object-level authorization: `GET /invoices/123` - does user own invoice 123?
- [ ] Function-level authorization: `DELETE /admin/users` - is this user an admin?

**Input Validation:**
- [ ] All request bodies are validated with a schema (Zod, Joi, Yup, class-validator)
- [ ] Validation happens server-side - never trust client-side validation alone
- [ ] Unknown fields are stripped (not passed through to DB)
- [ ] Number fields have min/max bounds (no `limit=999999` on a paginated endpoint)

**Response Security:**
- [ ] Error responses never expose stack traces, SQL errors, or internal paths in production
- [ ] Error messages are generic to the user, specific in logs
- [ ] No sensitive data in responses that isn't needed by the client

**Infrastructure:**
- [ ] CORS is configured with an explicit allowlist - never `Access-Control-Allow-Origin: *` in production
- [ ] Rate limiting on all public endpoints (not just auth)
- [ ] HTTP methods restricted per endpoint (a GET endpoint shouldn't accept POST)

**For GraphQL specifically:**
- [ ] Query depth limiting enabled (prevents deeply nested attacks)
- [ ] Query complexity limits enabled
- [ ] Introspection disabled in production
- [ ] No batching without limits

**STOP.**
```
Area 4 complete. Findings above.
Type APPROVE to continue to Area 5, or share code to review.
```

---

## Area 5: Environment Variables + Secrets

Checklist:
- [ ] `.env`, `.env.local`, `.env.production` files are in `.gitignore`
- [ ] No secrets are committed to git history

Run this to check git history for secrets:
```bash
git log --all -p | grep -iE "(secret|password|api_key|apikey|token|private_key)" | head -50
```

- [ ] Production secrets are different from development secrets (different API keys, different DB)
- [ ] Client-side env vars contain ONLY non-sensitive values
  - Next.js: Only `NEXT_PUBLIC_` vars go to the browser
  - Expo/React Native: Only `EXPO_PUBLIC_` vars go to the bundle
  - Everything else stays server-only
- [ ] API keys have minimum required scopes (not admin/root keys in production)
- [ ] Database connection string is not the superuser/admin connection

**Ask the user to confirm:**
- Where each env var is used (server-side or client-side)
- That production secrets are rotated from any that were shared in Slack/email/docs

**STOP.**
```
Area 5 complete. Findings above.
Type APPROVE to continue to Area 6, or discuss specific secrets.
```

---

## Area 6: Dependencies + Supply Chain

Run these commands and share the output:

```bash
# Check for known vulnerabilities
npm audit --production

# Or for yarn/pnpm:
yarn audit
pnpm audit --prod

# Find outdated packages
npm outdated
```

Checklist:
- [ ] No critical or high severity vulnerabilities in production dependencies
- [ ] Lockfile is committed (`package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`)
- [ ] Lockfile is not gitignored (it prevents supply chain attacks)
- [ ] Dependencies are reasonably up to date (not 2+ major versions behind)
- [ ] No packages with extremely low download counts or unknown publishers with broad filesystem/network access

**For high/critical vulnerabilities:**
- Check if there's a patched version: `npm audit fix`
- If no fix exists, assess the actual risk (is the vulnerable code path reachable?)
- Document unpatched vulnerabilities with rationale

**STOP.**
```
Area 6 complete. Findings above.
Type APPROVE to continue to Area 7, or review specific packages.
```

---

## Area 7: Infrastructure + Deployment

Checklist:
- [ ] HTTPS enforced on all endpoints - no HTTP in production
- [ ] Security headers configured:
  - `Content-Security-Policy` (CSP)
  - `Strict-Transport-Security` (HSTS)
  - `X-Frame-Options: DENY` (prevents clickjacking)
  - `X-Content-Type-Options: nosniff`
  - `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] Database is NOT publicly accessible - either on a private network or behind an IP allowlist
- [ ] Admin panels (Supabase Studio, database UIs) are not accessible from public internet in production
- [ ] Production environment has error monitoring (Sentry or equivalent)
- [ ] Production logs capture auth events and errors (but NOT passwords or tokens)
- [ ] Database backups are configured and have been tested (test restore!)
- [ ] No debug routes, test endpoints, or seed scripts accessible in production

**For Vercel/Netlify/Railway deployments:**
- [ ] Preview deployments don't have access to production secrets
- [ ] Environment variables are set per-environment (not one set for all)

**STOP.**
```
Area 7 complete. Findings above.
Type APPROVE to generate the Security Report, or review specific infrastructure concerns.
```

---

## Output

After all areas are complete, generate a `SECURITY-REPORT.md` file:

```markdown
# Security Report - [App Name]
Date: [Date]
Reviewer: Claude Code

## Summary
- Critical (fix before launch): N
- High (fix this week): N
- Medium (fix this month): N
- Low / informational: N
- Passed: N

## Critical - Fix Before Launch
[Each issue with: what it is, where it is, how to fix it]

## High - Fix This Week
[Each issue with: what it is, where it is, how to fix it]

## Medium - Fix This Month
[Each issue]

## Low / Informational
[Each item]

## Passed Checks
[List of all checks that passed]

## Re-test Checklist
After fixing critical/high issues, re-test:
- [ ] [Item 1]
- [ ] [Item 2]
```

**STOP.**
```
Security review complete. Type APPROVE to write SECURITY-REPORT.md, or revisit any area.
```

---

## Severity Definitions

| Severity | Definition | Example |
|----------|------------|---------|
| Critical | Exploitable now, data loss or account takeover likely | Missing RLS, SQL injection |
| High | Serious risk, likely exploited if discovered | No auth on endpoints, secrets in git |
| Medium | Risk exists but requires specific conditions | Missing rate limiting, weak CSP |
| Low | Defense in depth, best practice | Missing security headers, outdated non-critical dep |
