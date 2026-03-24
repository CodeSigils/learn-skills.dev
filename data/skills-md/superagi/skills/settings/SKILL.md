---
name: settings
description: Navigate and configure settings in SuperAGI Sales CRM
platform: [linux, macos]
---

# SuperAGI Sales CRM — Settings

## How to Access
- URL: `https://sales.superagi.com/settings` (lands on `#general` by default)
- Or click the "AK" user avatar (top-right) → Settings
- Each sub-page uses a URL hash fragment: `/settings#profile`, `/settings#personal_mailboxes`, etc.
- "Back to Dashboard" link at the top to return to main app

## Settings Structure

Settings are split into two groups in the left sidebar:

### PERSONAL (affects only you)

| Setting | Hash | Purpose | Connects to |
|---------|------|---------|-------------|
| Profile | `#profile` | First/last name, email (disabled/auto), phone, timezone, theme (Light/Dark), country code, mute chat notifications, Salesforce user mapping | Timezone affects scheduling across outreach/automations/meetings |
| Availability | `#availability` | Inbound call toggle, meeting agent weekly schedule (Sun–Sat with time selectors), platform timezone, default personal meeting link | Meeting Agent must be created before meeting link can be set |
| Personal Mailboxes | `#personal_mailboxes` | Connect email (Outlook/Gmail/SMTP+IMAP), open+click tracking toggles | **REQUIRED before Cold Outreach or Sequences can send email** |
| Personal LinkedIn | `#linkedin_account` | Connect LinkedIn via credentials or cookie auth; daily limits (connections, messages, inmails) | **REQUIRED before LinkedIn sequence steps work** |
| Personal Tokens | `#personal_tokens` | Generate personal API tokens; table shows Name, Created At, Expires At, Last Used At | For personal programmatic access |
| SSH Keys | `#ssh_keys` | Add SSH keys; table shows Key Name, Key Type, Fingerprint, Added On | For secure authentication |

### WORKSPACE (affects entire team)

| Setting | Hash | Purpose | Connects to |
|---------|------|---------|-------------|
| General | `#general` | Workspace name, currency management (add/edit/set primary, format preview) | Currency format used across CRM deals and reports |
| Business Details | `#business` | Business name, description, website, logo upload, ICP (ideal customer profile) definition | ICP used by AI features for targeting/personalization |
| Security | `#security` | SSO configuration (disabled by default): SuperAGI SSO URL (read-only), IdP SSO URL, IdP X.509 certificate; Test Configuration + Save | Enterprise authentication for the whole team |
| Waterfall | `#waterfall` | Waterfall enrichment vendor priority ordering for Email (SuperAGI→FindyMail→LeadMagic→Prospeo→Hunter→Dropcontact→RocketReach) and Phone (SuperAGI→ContactOut→LeadMagic→Prospeo→Datagma→Forager) | Controls which enrichment providers are tried and in what order for prospect data |
| Meeting Intelligence | `#meeting_intelligence` | Add notetaker bot, auto-recording per platform (Google Meet/Zoom/Teams), custom recorder name, auto-create tasks from meeting insights | Meetings module, task creation |
| Meeting Disposition | `#meeting_disposition` | Customize meeting outcome labels (e.g. Ongoing, Done, Failed); add/remove dispositions | Used to categorize meeting results |
| Entity Scoring | `#entity_scoring` | Enable/disable scoring for Companies, Contacts, Leads; define custom scoring rules based on behavior/demographics/engagement | Prioritizes follow-ups in CRM views |
| Unibox | `#unibox` | Assign which channels (e.g. WhatsApp accounts) show in unified inbox | Controls what conversations appear in Unibox |
| Email Templates | `#email_templates` | Create/manage reusable email templates with name + subject + body; supports personalization tokens (`{{contact.firstname}}`, etc.) | Referenced in Sequences and Cold Outreach steps |
| Customer Success | `#customer_success` | Two tabs: Manage Data + AI Health Score. Configure dashboard views, default/onboarding views, deals pipeline, task spaces | Customer Success module configuration |
| Value Prop Templates | `#value_prop_templates` | Define messaging templates for Cold Outreach AI: company info, pain points, value props, proof points, tone, language, sample emails, instructions | **Used by Cold Outreach AI** to generate personalized messaging |
| Email Campaign Settings | `#email_campaign_settings` | Two tabs: **Sender Details** (add/verify sender emails) + **Sender Domains** (add domain → get DNS records TXT/CNAME/MX → verify) | **REQUIRED for marketing email campaigns** (sender domain must be verified) |
| WhatsApp | `#whatsapp` | Connected WhatsApp accounts table (Vendor, Phone Number, Status, Created At); Connect Account button | WhatsApp messaging in sequences and Unibox |
| Support | `#support` | Conversation updates toggle (auto-email when customers go offline), email-to-send-from selection, add forwarding email for support inbox | Support module email channel |
| Exports | `#exports` | Download history of all data exports (Leads, Deals, Contacts, Website Visitors, etc.) with name, type, size, exported-by, date | Read-only export log with download links |
| Audit Trail | `#audit_trail` | View all changes made in workspace | Compliance and change tracking |
| API Keys | `#api_keys` | Add API Key (name it, generate); table shows key name, created by, last updated, MCP connection toggle | For external integrations (Zapier, Make.com, custom backends, data sync scripts). **Key shown ONLY ONCE on creation — must copy immediately** |
| Custom Events | `#custom_events` | Create custom webhook events (e.g. Google Ads Webhook); table shows name, creator, last updated, status toggle | Trigger automations from external systems |
| Code Reviewer | `#code_reviewer` | Connect GitHub accounts via GitHub App; shows connected accounts, synced repos, primary account | AI code review for connected repositories |

## Setup Dependency Order

These must be configured **before** their dependent features will work:

1. **Personal Mailboxes** → Cold Outreach and Sequences cannot send email without a connected mailbox
2. **Personal LinkedIn** → LinkedIn steps in Sequences won't execute without a connected account
3. **Email Templates** → Must exist before they can be referenced in Sequence/Campaign steps
4. **Value Prop Templates** → Must be created before Cold Outreach AI can generate personalized emails
5. **Email Campaign Settings (Sender Domain)** → Marketing email campaigns require a verified sender domain with correct DNS records
6. **Business Details (ICP)** → Should be filled for AI features to correctly target prospects

## Security: SSO Configuration

- Default status: **Disabled**
- Fields:
  - SuperAGI SSO URL (read-only, auto-generated): `https://sales.superagi.com/auth_users/saml/callback`
  - Identity provider SSO URL (paste from your IdP)
  - Identity provider X.509 certificate (PEM format)
- Certificate fingerprint is calculated automatically after pasting
- Workflow: Fill IdP URL + certificate → Test Configuration → Save changes

## API Keys

- Click "Add API Key" → name it → generate
- **Key is shown ONLY ONCE** — must copy immediately after generation
- Table shows: key name, created by, last updated, MCP connection toggle
- Used for: custom backends, third-party integrations, automation platforms (Zapier, Make.com), data sync scripts

## Workflow: Navigate to a Specific Setting

1. Navigate to `https://sales.superagi.com/settings`
2. Wait for the page to fully load (async — may need 2-3 seconds)
3. `browser_snapshot` to see the settings sidebar
4. Click the setting name in the sidebar (e.g., `StaticText "Email Templates"`)
5. `browser_snapshot` to see the setting's content panel on the right

## Workflow: Connect Personal Mailbox

1. Navigate to `/settings#personal_mailboxes`
2. Click "Connect Mailbox" button
3. Choose provider: Outlook, Gmail, or Other (SMTP+IMAP)
4. After connecting: configure emails/day, emails/hour, min delay, sender name, signature
5. Toggle open tracking and click tracking as needed
6. Manage via three-dot menu: Edit Mailbox, Mark as Shared, Mark as Primary, Disconnect

## Workflow: Connect LinkedIn

1. Navigate to `/settings#linkedin_account`
2. Click "Connect LinkedIn" or "Connect" button
3. Connect via credentials or cookie auth
4. After connecting: edit daily limits via three-dot menu (default 25: connections/day, messages/day, inmails/day)

## Workflow: Add Sender Domain (for Marketing Campaigns)

1. Navigate to `/settings#email_campaign_settings`
2. Click "Sender Domains" tab
3. Click "Add Domain"
4. Get DNS records (TXT, CNAME, MX) provided by SuperAGI
5. Add these records to your DNS provider
6. Return and click "Verify Records"
7. Status changes from "Unverified" to "Active" once DNS propagates

## Gotchas
- **Async loading**: Settings pages load asynchronously — always wait 2-3 seconds and re-snapshot if the first snapshot shows minimal content
- **Sub-tabs**: Some pages have internal tabs (e.g., Email Campaign Settings has "Sender Details" and "Sender Domains"; Customer Success has "Manage Data" and "AI Health Score")
- **URL hash fragments**: Each sub-page uses a hash fragment (`/settings#general`, `/settings#profile`, etc.) — navigating via hash may require clicking the sidebar item instead
- **Sidebar click issues**: When batch-clicking sidebar items, the page may not update — click one at a time and wait for the content panel to refresh
