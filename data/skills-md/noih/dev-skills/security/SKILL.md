---
name: security
description: Security principles and vulnerability patterns. Use when writing, reviewing, or designing code that handles user input, authentication, or sensitive data.
user-invocable: false
---

# Security

Assume all external input is malicious.

## Injection

- **SQL Injection** — String concatenation in queries, missing parameterized queries
- **Command Injection** — Unsanitized input in shell commands, exec calls
- **XSS** — Unescaped user input in HTML/DOM, missing output encoding, unsafe use of `dangerouslySetInnerHTML` / `v-html` / `innerHTML`
- **Template Injection** — User input in template engines without escaping
- **Path Traversal** — Unsanitized file paths from user input
- **SSRF** — User-controlled URLs used in server-side requests (fetch, HTTP clients). Validate and whitelist allowed hosts
- **Unsafe Deserialization** — Deserializing untrusted data: prototype pollution (JS), pickle (Python), ObjectInputStream (Java). Use safe alternatives or validate before deserializing

## Authentication & Authorization

- **Missing auth checks** — Endpoints or operations accessible without proper authentication
- **Broken access control** — Users can access resources they shouldn't
- **Insecure session management** — Weak tokens, missing expiry, no rotation
- **Missing rate limiting** — Auth endpoints without brute-force protection; no account lockout or throttling

## Input Validation

- **Missing validation** at system boundaries (API endpoints, form handlers)
- **Insufficient validation** — Checking type but not range, length, or format
- **Client-side only validation** — No server-side re-validation
- **Mass assignment** — Accepting all request body fields without whitelisting allowed properties

## Sensitive Data

- **Secrets in code** — API keys, passwords, tokens, credentials committed to source or hardcoded
- **Logging sensitive data** — Passwords, tokens, PII in log output
- **Insecure storage** — Passwords not hashed, tokens not encrypted; sensitive data in localStorage/sessionStorage without encryption
- **Data leakage** — PII in error messages, API responses, or client-side state exposed in DevTools

## Dependencies & Configuration

- **Known vulnerable dependencies** — Outdated packages with CVEs
- **Insecure defaults** — Debug mode, verbose errors in production configs
- **Missing security headers** — CORS misconfiguration, missing CSP
- **Insecure TLS/crypto** — Weak algorithms, disabled certificate validation

## Frontend-Specific

- **CSRF** — Missing CSRF tokens on state-changing requests; over-reliance on SameSite cookies alone
- **Open redirects** — Unvalidated redirect URLs from user input or query parameters
- **Clickjacking** — Missing frame-busting headers (X-Frame-Options, CSP frame-ancestors)
- **postMessage** — Missing origin validation on `message` event listeners; sending sensitive data without target origin restriction
- **Third-party scripts** — Loading external scripts without SRI (Subresource Integrity); excessive third-party permissions

## Concurrency

- **TOCTOU** — Time-of-check to time-of-use vulnerabilities
- **Shared mutable state** — Missing locks, unsafe concurrent access
- **Double-spend / double-submit** — Missing idempotency protections

## Acceptable when

- Theoretical vulnerabilities with unlikely attack vectors
- Security handled by the framework (e.g., CSRF tokens auto-applied, React's JSX auto-escaping)
- Internal-only code that never touches external input
