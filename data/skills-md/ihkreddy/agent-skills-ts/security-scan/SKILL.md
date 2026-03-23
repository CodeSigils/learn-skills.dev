---
name: security-scan
description: Run security checks before PR including secrets, vulnerabilities, and best practices
version: 1.0.0
author: Flight Booking Team
tags:
  - productivity
  - security
  - code-review
  - best-practices
  - pre-commit
---

# Security Scan

Performs comprehensive security analysis before PR submission, checking for secrets, vulnerabilities, insecure patterns, and security best practices.

## 🎯 Use Case Demo

### Scenario: Pre-PR Security Review

**Before (Manual Process):**
> Developer ready to submit PR, tries to remember security checks:
> - "Did I accidentally commit any secrets?"
> - "Are my dependencies secure?"
> - "Is my input validation sufficient?"
> - Forgets to check, security issue found in review (or worse, production)
> 
> **Time: Often skipped, caught late or never**

**After (With This Skill):**
> Developer: "Run security scan before I create PR"
> 
> **Agent Response:**
> ```
> 🔐 SECURITY SCAN REPORT
> ═══════════════════════════════════════════════════════════════
> 
> 📅 Scan Date: December 20, 2024
> 📁 Files Scanned: 12 changed files
> 🔍 Branch: feature/payment-integration
> 
> ═══════════════════════════════════════════════════════════════
> 📊 SCAN SUMMARY
> ═══════════════════════════════════════════════════════════════
> 
> | Category | Status | Issues |
> |----------|--------|--------|
> | Secrets Detection | 🔴 FAIL | 2 found |
> | Dependency Vulnerabilities | 🟡 WARN | 1 medium |
> | Input Validation | 🔴 FAIL | 3 missing |
> | SQL Injection | ✅ PASS | 0 found |
> | XSS Prevention | ✅ PASS | 0 found |
> | Authentication | ✅ PASS | Properly secured |
> | Logging Security | 🟡 WARN | PII in logs |
> 
> Overall: 🔴 BLOCKED - Fix critical issues before PR
> 
> ═══════════════════════════════════════════════════════════════
> 🚨 CRITICAL: SECRETS DETECTED
> ═══════════════════════════════════════════════════════════════
> 
> ⛔ MUST FIX BEFORE PR - These will block your commit
> 
> 1. API Key Detected
>    📍 Services/PaymentService.cs:34
>    ```csharp
>    private const string StripeKey = "sk_live_XXXXXXXXXXXXXXXXXXXX";
>    ```
>    🔧 Fix: Move to environment variable or secrets manager
>    ```csharp
>    private readonly string _stripeKey = Environment.GetEnvironmentVariable("STRIPE_API_KEY");
>    ```
> 
> 2. Connection String with Password
>    📍 appsettings.json:12
>    ```json
>    "ConnectionString": "Server=db.prod.com;Password=SuperSecret123!"
>    ```
>    🔧 Fix: Use Azure Key Vault or environment variables
> 
> ═══════════════════════════════════════════════════════════════
> 🔴 INPUT VALIDATION MISSING
> ═══════════════════════════════════════════════════════════════
> 
> 1. Missing Validation: CreateBooking endpoint
>    📍 Controllers/BookingsController.cs:45
>    ```csharp
>    public async Task<IActionResult> Create([FromBody] BookingRequest request)
>    {
>        // No validation before processing
>        await _service.CreateBooking(request);
>    ```
>    🔧 Fix: Add FluentValidation or DataAnnotations
>    ```csharp
>    public async Task<IActionResult> Create([FromBody] BookingRequest request)
>    {
>        if (!ModelState.IsValid)
>            return BadRequest(ModelState);
>    ```
> 
> 2. Email Not Validated
>    📍 Models/BookingRequest.cs:15
>    ```csharp
>    public string Email { get; set; }  // No validation
>    ```
>    🔧 Fix: Add email validation attribute
>    ```csharp
>    [Required]
>    [EmailAddress]
>    public string Email { get; set; }
>    ```
> 
> 3. Numeric Range Not Checked
>    📍 Models/SearchRequest.cs:8
>    ```csharp
>    public int Passengers { get; set; }  // Could be negative or huge
>    ```
>    🔧 Fix: Add range validation
>    ```csharp
>    [Range(1, 9)]
>    public int Passengers { get; set; }
>    ```
> 
> ═══════════════════════════════════════════════════════════════
> 🟡 WARNINGS (Recommended Fixes)
> ═══════════════════════════════════════════════════════════════
> 
> 1. Dependency Vulnerability
>    📦 System.Text.Json 7.0.2
>    CVE: CVE-2024-1234 (Medium severity)
>    Fix: Upgrade to 7.0.4
>    ```
>    dotnet add package System.Text.Json --version 7.0.4
>    ```
> 
> 2. PII in Logs
>    📍 Services/BookingService.cs:89
>    ```csharp
>    _logger.LogInformation($"Booking created for {request.Email}");
>    ```
>    🔧 Fix: Mask or remove PII from logs
>    ```csharp
>    _logger.LogInformation($"Booking created for {MaskEmail(request.Email)}");
>    ```
> 
> ═══════════════════════════════════════════════════════════════
> ✅ PASSED CHECKS
> ═══════════════════════════════════════════════════════════════
> 
> ✅ No SQL injection vulnerabilities
>    - All queries use parameterized statements
>    - Entity Framework properly configured
> 
> ✅ No XSS vulnerabilities
>    - Output encoding in place
>    - Content-Security-Policy configured
> 
> ✅ Authentication properly implemented
>    - JWT validation configured
>    - Endpoints have [Authorize] attributes
> 
> ✅ HTTPS enforced
>    - UseHttpsRedirection() in place
>    - HSTS configured
> 
> ═══════════════════════════════════════════════════════════════
> 📋 ACTION REQUIRED
> ═══════════════════════════════════════════════════════════════
> 
> Before creating PR, you must:
> 
> □ Remove hardcoded secrets (2 issues)
> □ Add input validation (3 issues)
> 
> Recommended (not blocking):
> □ Update vulnerable dependency
> □ Remove PII from logs
> 
> Run "Apply security fixes" to auto-fix where possible.
> 
> ═══════════════════════════════════════════════════════════════
> ```

**Result: Potential security breach prevented before code even reaches review**

---

## Agent Instructions

When this skill is activated:

1. **Secrets Detection**:
   - Scan for API keys, tokens, passwords
   - Check for patterns: `sk_live_`, `api_key`, `password=`
   - Look in: source files, config files, .env files
   - Check git history for accidentally committed secrets

2. **Dependency Vulnerabilities**:
   - Run `dotnet list package --vulnerable`
   - Check npm audit for Node.js
   - Cross-reference with CVE databases

3. **Input Validation**:
   - Check all API endpoints for validation
   - Verify model attributes (Required, Range, etc.)
   - Look for raw string inputs without sanitization

4. **SQL Injection**:
   - Look for string concatenation in queries
   - Verify parameterized queries usage
   - Check raw SQL execution

5. **XSS Prevention**:
   - Check output encoding
   - Verify CSP headers
   - Look for `@Html.Raw()` usage

6. **Authentication/Authorization**:
   - Verify [Authorize] attributes on endpoints
   - Check JWT configuration
   - Look for authorization bypass patterns

7. **Logging Security**:
   - Check for PII in log statements
   - Verify sensitive data not logged

8. **Generate Report**:
   - Categorize by severity
   - Provide specific fix recommendations
   - Block PR if critical issues found

### Example Prompts

- "Run security scan before PR"
- "Check for security vulnerabilities"
- "Are there any hardcoded secrets?"
- "Scan my changes for security issues"
- "Pre-commit security check"

---

## Checks Performed

| Check | Description | Severity |
|-------|-------------|----------|
| Secrets | API keys, passwords, tokens | 🔴 Critical |
| SQL Injection | Unsanitized queries | 🔴 Critical |
| Input Validation | Missing or weak validation | 🔴 High |
| Dependencies | Known CVEs | 🟡 Medium |
| XSS | Cross-site scripting | 🔴 High |
| PII Logging | Personal data in logs | 🟡 Medium |
| Auth Bypass | Missing authorization | 🔴 Critical |

---

## Benefits

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Security issues caught | In production | Before PR | 100% earlier |
| Time to detect secrets | Days/weeks | Seconds | Immediate |
| Developer security knowledge | Variable | Guided | Learning tool |
| Security review time | Hours | Minutes | 90% faster |
