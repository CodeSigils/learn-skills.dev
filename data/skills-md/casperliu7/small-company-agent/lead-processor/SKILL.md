---
name: Lead Processor
description: Handles CRM sales leads and inbox triage. Categorizes real human emails vs. marketing noise and generates structured, human-in-the-loop replies.
---

# Lead Processor Skill

This skill defines the standard operating procedure (SOP) for processing inbound sales leads and managing customer support mailboxes.

## 1. Inbox Triage & Classification
- Scan IMAP mailboxes configured in `config/accounts.json` using real, fetched email data only.
- Classify emails into:
  - **Actionable Leads**: Real human inquiries and customer requests.
  - **System Notifications**: Automated alerts, system logs, receipts, product notifications. Move to the designated System/Archive folder.
  - **Marketing/Spam**: Cold outreach, SEO services, promotional content. Move to the designated Marketing folder.
- Never delete emails permanently; only move them to designated categorized folders.

## 2. Drafting Replies (Human-in-the-Loop)
- When a genuine lead is found, extract the core request.
- Provide a concise "Customer Info Check" (客户信息核对) summarizing the sender and intent.
- Generate 3 response options (A, B, and C).
- Each option must have the drafted text immediately followed by its translation (e.g., English text followed directly by Chinese translation).
- Match the customer's language unless the user asks otherwise.
- **CRITICAL CONSTRAINT**: Do NOT send the email automatically. Save as a draft if requested, but only send via SMTP after the user explicitly replies with the confirmation keyword (e.g., `【确认发送】`).

## 3. CRM Synchronization
- Once an email is confirmed and sent, update the corresponding CRM record.
- Update the status field to indicate progression (e.g., `Replied`, `Failed`, or custom pipeline stages).
- Only update lead-specific tables; do not sync general mailbox thread follow-ups to the CRM unless explicitly requested.

## 4. Daily Sweep Automation
- Support daily scheduled sweeps to keep the inbox clean.
- Generate a concise daily report summarizing new actionable leads, the number of junk/system emails moved, and pending actions.

## 5. Thread Preservation
- Drafts saved to the mailbox and final outbound emails must preserve the **full available thread**.
- Ensure nested quotes (e.g., `<blockquote class="gmail_quote">`) and original headers are intact so the recipient sees the complete conversation history.
