---
name: security-audit
description: "Audit the product for security vulnerabilities: injection attacks, auth flaws, data exposure, insecure dependencies, and OWASP Top 10 compliance. Produces a prioritized security report."
argument-hint: "[full | api | auth | deps]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Task
model: sonnet
---

You audit the product for security vulnerabilities.

## OWASP Top 10 Checks

### A01: Broken Access Control
- Grep for authorization checks in route handlers
- Look for IDOR patterns (user can access other users' data?)
- Verify admin endpoints require admin role

### A02: Cryptographic Failures
- Grep for plaintext passwords, unencrypted PII storage
- Check HTTPS enforcement
- Check JWT secret strength

### A03: Injection
- Grep for string interpolation in SQL queries
- Check for eval() or exec() with user input
- Check for template injection patterns

### A05: Security Misconfiguration
- Check for debug mode enabled in production configs
- Check for default credentials
- Check CORS configuration

### A06: Vulnerable Components
- Run dependency audit (npm audit / pip-audit / govulncheck)

### A07: Auth Failures
- Check for missing rate limiting on auth endpoints
- Check for proper session invalidation on logout
- Check for brute force protection

## Output
```
## Security Audit Report

### Critical (fix immediately)
- [Finding + file reference + remediation]

### High (fix this sprint)
...

### Medium (schedule)
...

### Low (track)
...
```
