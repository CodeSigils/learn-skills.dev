---
name: aws-ses
description: Send, receive, and manage email at scale with Amazon Simple Email Service (SES). Use when building email sending, identity verification, deliverability monitoring, email validation, tenant management, or multi-tenant email platforms. Covers V2 API patterns, DKIM/SPF/DMARC authentication, configuration sets, suppression lists, bounce/complaint handling, and dedicated IP management.
license: CC-BY-SA-4.0
compatibility: Requires AWS credentials (AWS Identity and Access Management (IAM) user, role, or environment variables) and an AWS account with Amazon SES access. SDK required - Python (boto3), Node.js (@aws-sdk/client-sesv2), or Java (software.amazon.awssdk:sesv2).
metadata:
  author: aws
  version: "1.0"
  service: ses
---

# Amazon Simple Email Service (SES)

Amazon SES is a cloud-based email sending and receiving service. It provides APIs and SMTP access for transactional, marketing, and notification email, designed to scale with your needs.

## Key Capabilities

- **Email Sending** — V2 API (`sesv2`), SMTP interface, templated and bulk sends
- **Email Receiving** — For inbound email processing, see the Mail Manager Agent Context Pack (coming soon)
- **Identity Management** — Domain and email verification with DKIM, SPF, DMARC, BIMI
- **Tenants** — Isolated workloads with per-tenant reputation monitoring and enforcement
- **Configuration Sets** — Event tracking, suppression management, IP pool assignment
- **Email Validation** — Validate addresses before sending to reduce bounces
- **Deliverability** — VDM dashboard, reputation monitoring, dedicated IP management
- **Suppression Lists** — Global, account-level, and configuration-set-level suppression

## When to Use This Skill

- Building email sending into an application
- Setting up transactional email (password resets, order confirmations, notifications)
- Building a multi-tenant email platform (ISV/SaaS)
- Migrating from another email service (SendGrid, Postmark, Mailgun)
- Setting up email authentication (DKIM, SPF, DMARC)
- Monitoring email deliverability and sender reputation
- Validating email addresses for deliverability

## Common Mistakes (Quick Reference)

| Mistake | Fix |
|---------|-----|
| Using V1 API (`ses`) | Use `sesv2` — V1 is legacy |
| Sending before verifying identity | Verify domain/email first |
| Ignoring sandbox mode | Use simulator addresses for testing; request production access before going live |
| Skipping DKIM/SPF/DMARC | Gmail and Yahoo reject unauthenticated bulk email |
| No configuration set | You lose all observability — always create one |
| No tenants | Isolate mail streams from day one — tenants provide per-stream reputation monitoring |
| Misdiagnosing throttling | TPS limit is a ceiling; check your own app's rate limiting first |
| Ignoring bounces/complaints | Bounce > 5% or complaint > 0.1% triggers enforcement |
| No delivery delay events | Gmail defers for up to 14 hours — enable notifications |
| SPF on wrong domain | SPF checks MAIL FROM, not From header — use custom MAIL FROM |
| Cold dedicated IPs | Warm up 2-4 weeks or use managed dedicated IPs |
| Sending to invalid addresses | Validate with `GetEmailAddressInsights` first |

See [AGENTS.md](../../AGENTS.md) for detailed explanations of each mistake.

## Executable Scripts

Scripts in `scripts/` accept command-line arguments and can be run directly. Available in Python and Node.js.

| Script | Description | Usage |
|--------|-------------|-------|
| `send-email` | Send a simple email | `python scripts/send-email.py --from sender@domain.com --to recipient@domain.com` |
| `send-templated` | Send with a template | `python scripts/send-templated.py --from sender@domain.com --to recipient@domain.com --template name --data '{"key":"val"}'` |
| `send-bulk` | Send bulk templated email | `python scripts/send-bulk.py --from sender@domain.com --template name --recipients '[{"email":"a@b.com","data":{"name":"Alice"}}]'` |
| `verify-domain` | Verify domain + get DKIM records | `python scripts/verify-domain.py --domain example.com` |
| `setup-config-set` | Create config set + event destinations | `python scripts/setup-config-set.py --name my-config --enable-cloudwatch` |
| `handle-bounces` | Set up bounce/complaint Amazon SNS notifications | `python scripts/handle-bounces.py --config-set my-config --email alerts@domain.com` |
| `setup-tenant` | Create tenant + associate resources | `python scripts/setup-tenant.py --name my-tenant --identity-arn arn:... --config-set-arn arn:...` |
| `validate-email` | Validate email addresses | `python scripts/validate-email.py --email user@example.com` |

For Java examples, see [references/java-examples.md](references/java-examples.md).

## What This Skill Does NOT Cover

- **Mail Manager / Inbound Email** — SES Mail Manager handles inbound email processing (ingress, routing, archiving, SMTP relay). Classic SES receipt rules (V1 API) are not covered by this skill. See the Mail Manager Agent Context Pack (coming soon) for inbound use cases.
- **Global Endpoints** — Cross-region failover configuration is an advanced topic.
- **V1 API** — Intentionally excluded. All guidance and examples use V2.

## Resource Links

- [AGENTS.md](../../AGENTS.md) — Full workflow patterns and agent instructions
- [Developer Guide](https://docs.aws.amazon.com/ses/latest/dg/llms.txt)
- [API Reference (V2)](https://docs.aws.amazon.com/ses/latest/APIReference-V2/llms.txt)
