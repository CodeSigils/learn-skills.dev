---
name: top-web-vulnerabilities
description: Comprehensive reference for the OWASP Top 100 web vulnerabilities. Identifies vulnerable patterns, explains impacts, and provides remediation guidance across injection attacks, authentication flaws, data exposure, and advanced attack vectors.
version: 2.0.0
dependencies:
  - guardian
tags:
  - security
  - web
  - vulnerabilities
  - owasp
  - testing
---

# Top 100 Web Vulnerabilities

Comprehensive reference for the OWASP Top 100 most critical web application vulnerabilities.

## When to Use This Skill

Use when:

- Identifying web application vulnerabilities during code review
- Explaining common security flaws to developers
- Understanding vulnerability categories and impacts
- Providing remediation guidance for security findings
- Testing for OWASP-listed vulnerabilities
- Building secure applications and avoiding known patterns
- Assessing application security posture
- Training on secure coding practices

---

## Core Capabilities

1. **Injection & Input Validation** - SQL, XSS, command, template injection attacks
2. **Authentication & Authorization** - Session management, privilege escalation, IDOR
3. **Data Exposure & Configuration** - Information disclosure, misconfiguration, missing headers
4. **Advanced Attacks** - Deserialization, SSRF, DoS, race conditions
5. **API & Transport Security** - Insecure APIs, MITM, TLS configuration
6. **Client-Side Security** - DOM-based XSS, clickjacking, browser cache poisoning
7. **Business Logic Flaws** - Workflow abuse, payment bypass, authorization logic

---

## Vulnerability References

For detailed vulnerability guidance, see:

### [Injection & Input Validation Vulnerabilities](references/injection-vulnerabilities.md)

**Use when:** Identifying and fixing injection attacks

Covers:

- SQL Injection (OWASP #1)
- Cross-Site Scripting - XSS (OWASP #2)
- Command Injection (OWASP #5, #11)
- XML Injection variants (XXE, XPath, LDAP, SSTI)
- Server-Side Template Injection (OWASP #13)

### [Authentication & Authorization Flaws](references/auth-authorization.md)

**Use when:** Securing authentication and access control

Covers:

- Session Fixation (OWASP #14)
- Brute Force Attacks (OWASP #15)
- Session Hijacking (OWASP #16)
- Credential Stuffing (OWASP #22)
- IDOR - Insecure Direct Object References (OWASP #23, #42)
- Privilege Escalation (OWASP #41)
- Forceful Browsing (OWASP #43)

### [Data Exposure & Configuration Flaws](references/data-exposure-config.md)

**Use when:** Protecting sensitive data and securing configuration

Covers:

- Data Leakage (OWASP #24)
- Unencrypted Data Storage (OWASP #25)
- Missing Security Headers (OWASP #26)
- Default Passwords (OWASP #28)
- Information Disclosure (OWASP #33)
- Unprotected APIs (OWASP #30)
- Misconfigured CORS (OWASP #35)

### [Advanced Attack Vectors](references/advanced-attacks.md)

**Use when:** Addressing complex attack scenarios

Covers:

- Insecure Deserialization (OWASP #45-47)
- Server-Side Request Forgery - SSRF (OWASP #66)
- Distributed Denial of Service (OWASP #61, #62)
- Resource Exhaustion (OWASP #63)
- Request timeouts and rate limiting

---

## Quick Vulnerability Lookup

| Category | OWASP # | Vulnerability | Reference |
| :------- | :------ | :------------- | :-------- |
| **Injection** | 1 | SQL Injection | [Injection Vulnerabilities](references/injection-vulnerabilities.md) |
| **Injection** | 2 | Cross-Site Scripting (XSS) | [Injection Vulnerabilities](references/injection-vulnerabilities.md) |
| **Auth** | 14 | Session Fixation | [Auth & Authorization](references/auth-authorization.md) |
| **Auth** | 15 | Brute Force | [Auth & Authorization](references/auth-authorization.md) |
| **Auth** | 16 | Session Hijacking | [Auth & Authorization](references/auth-authorization.md) |
| **Auth** | 23 | IDOR | [Auth & Authorization](references/auth-authorization.md) |
| **Data** | 24 | Data Leakage | [Data Exposure](references/data-exposure-config.md) |
| **Data** | 25 | Unencrypted Storage | [Data Exposure](references/data-exposure-config.md) |
| **Data** | 33 | Information Disclosure | [Data Exposure](references/data-exposure-config.md) |
| **Advanced** | 45 | Insecure Deserialization | [Advanced Attacks](references/advanced-attacks.md) |
| **Advanced** | 66 | SSRF | [Advanced Attacks](references/advanced-attacks.md) |

---

## Assessment Workflow

### Phase 1: Code Review

1. Identify user input entry points (forms, APIs, cookies)
2. Trace input through application (filters, validation, storage)
3. Check for injection vulnerabilities (SQL, XSS, command)
4. Verify authorization checks on sensitive operations
5. Review encryption and data protection

### Phase 2: Configuration Review

1. Check security headers (CSP, HSTS, X-Frame-Options)
2. Verify HTTPS/TLS configuration
3. Review API authentication and rate limiting
4. Audit access controls and IAM
5. Check for default credentials and debug features

### Phase 3: Testing

1. Test authentication (brute force, session fixation)
2. Test authorization (IDOR, privilege escalation)
3. Test input validation (injection, XSS)
4. Test rate limiting and DoS protections
5. Test data encryption and HTTPS

### Phase 4: Remediation

1. Implement fixes with highest severity first
2. Add unit/integration tests for vulnerabilities
3. Perform regression testing
4. Deploy with monitoring
5. Document security improvements

---

## Best Practices

### Input & Output Handling

- ✅ **Validate Input**: Whitelist acceptable input patterns
- ✅ **Encode Output**: Escape data based on context (HTML, JavaScript, SQL)
- ✅ **Parameterized Queries**: Use prepared statements for databases
- ✅ **Content Security Policy**: Implement CSP headers

### Authentication & Authorization

- ✅ **Strong Passwords**: Enforce complexity, minimum length
- ✅ **MFA**: Implement multi-factor authentication
- ✅ **Rate Limiting**: Limit failed login attempts
- ✅ **Least Privilege**: Grant minimum necessary permissions
- ✅ **Session Security**: HttpOnly, Secure, SameSite cookie flags

### Data Protection

- ✅ **Encryption in Transit**: Use TLS 1.2+ with strong ciphers
- ✅ **Encryption at Rest**: Encrypt PII and sensitive data
- ✅ **Secrets Management**: Use vaults, never hardcode secrets
- ✅ **Data Minimization**: Only collect and store necessary data
- ✅ **Access Logging**: Audit and alert on sensitive data access

### Security Configuration

- ✅ **Security Headers**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- ✅ **Disable Debug Mode**: No stack traces or error details in production
- ✅ **Change Defaults**: Remove default credentials and configurations
- ✅ **Patch Management**: Keep frameworks, libraries, and OS updated
- ✅ **Security Scanning**: Regular SAST/DAST scans

---

## Dependencies

- **guardian** - For security review and compliance verification
