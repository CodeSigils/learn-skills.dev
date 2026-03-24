---
name: navigation
description: Navigate SuperAGI Sales platform — complete URL map, sidebar structure, product context, and core workflows
platform: [linux, macos]
---

# SuperAGI Sales Platform — Navigation & Product Context

SuperAGI Sales (`sales.superagi.com`) is an AI-native sales platform. The UI uses a left sidebar for navigation, a top header bar with search/notifications/avatar, and a main content area.

---

## 1. Complete URL Map

### Core Sales Modules

| Section | Sub-item | URL |
|---------|----------|-----|
| **I Assistant** | — | `/i-assistant` |
| **CRM** | Contacts | `/crm/contacts` |
| | Leads | `/crm/leads` |
| | Companies | `/crm/companies` |
| | Deals | `/crm/deals` |
| | Lists | `/list` |
| | Users | `/crm/users` |
| | CRM Tasks | `/tasks` |
| | Customers | `/crm/customers` |
| **Engage** | Cold Outreach | `/cold-outreach` |
| | Sequences | `/sequences` |
| | Conversations | `/conversations` |
| | Emails | `/emails` |
| | LinkedIn | `/linkedin/logs` |
| **Prospect** | Prospect Leads | `/prospect/find_leads` |
| | Prospect Companies | `/prospect/find_companies` |
| | Signals | `/signals` |
| | Anonymous Website Visitors | `/website_visitors` |
| **Automate** | Workflows | `/workflows` |
| **Library** | Content | `/content` |
| | Marketing Emails | `/email-templates` |
| **Analyze** | Analytics | `/analytics` |
| | AI Analytics | `/ai-analytics` |
| **Marketing** | Campaigns | `/marketing/campaigns` |
| **Voice Agents** | Agents | `/voice-agents/agents` |
| | Campaign | `/voice-agents/campaign` |
| | Call Logs | `/voice-agents/call-logs` |

### Productivity & Tools

| Section | Sub-item | URL |
|---------|----------|-----|
| **Dashboards** | — | `/dashboards` |
| **Forms** | — | `/forms` |
| **Process Design** | — | `/process_design` |
| **Unibox** | — | `/unibox` |
| **Customer Success** | Summary | `/customer_success/summary` |
| | Onboarding | `/customer_success/onboarding` |
| | Customers | `/customer_success/customers` |
| | Deals | `/customer_success/deals` |
| | Tasks | `/customer_success/tasks` |
| | Alerts | `/customer_success/alerts` |
| **Projects** | Tasks | `/spaces/projects/tasks` |
| | Chat | `/projects/chats` |
| | Notes | `/projects/notes` |
| **Business Phone** | — (Call Logs) | `/business-phone/call_logs` |
| **AI Meeting Notetaker** | — | `/ai_notetaker` |
| **Digital Employees** | — | `/digital-employees` |
| **Developer Center** | — | `/developer-center` |
| **Data Enrichment** | — | `/data_enrichments` |
| **Meeting Router** | — | `/routing_form` |
| **Business Receptionist** | — | `/business-receptionist` |

### Expandable Tool Groups

| Section | Sub-item | URL |
|---------|----------|-----|
| **Live Assist** | Download App | `/live-assist/download` |
| | Templates | `/live-assist/templates` |
| | Activity | `/live-assist/activity` |
| **Meeting Links** | Meeting Agents | `/meeting_agent` |
| | Meeting Logs | `/meeting_log` |
| **Sales Dialer** | Campaigns | `/sales-dialer/campaigns` |
| | Call Logs | `/sales-dialer/call_logs` |
| **E-Sign** | Agreements | `/esign/agreements` |
| | Templates | `/esign/templates` |
| **Developer Tools** | Codebase | `/developer_tools/codebase` |
| | Code Reviewer | `/developer_tools/code_reviewer` |
| | AI QA | `/developer_tools/ai-qa` |
| **Support** | Inbox | `/inbound_agent/inbox` |
| | Knowledge Base | `/inbound_agent/knowledge_base` |
| | Agent Instructions | `/inbound_agent/instructions` |
| | LiveChat Widget | `/inbound_agent/live_chat` |
| | Tickets | `/inbound_agent/tickets` |

### Vibe Coder Apps

| Item | URL |
|------|-----|
| Vibe Coder (Full-Stack App) | `/coder/full-stack-app` |
| Mobile App | `/coder/mobile-app` |
| Landing Page | `/coder/landing-page` |

### Community / Marketplace Apps

| Item | URL |
|------|-----|
| Invoice Generator PRO | `/community-app/community_app_2_133` |
| POS | `/community-app/community_app_2_178` |
| Num | `/community-app/community_app_2_200` |
| Workbox HR | `/community-app/community_app_2_208` |
| Content Pilot | `/community-app/community_app_2_211` |
| Add Apps (Marketplace) | `/market` |

### Other Key URLs

| Page | URL |
|------|-----|
| Search | `/search` |
| Settings | `/settings` |

---

## 2. Sidebar Structure

The sidebar has two types of items:

### Expandable Groups (have `right_arrow_small` icon)
Click the group name text to expand. Sub-items appear as links below. Groups are:
- CRM, Engage, Automate, Library, Analyze, Marketing, Prospect, Voice Agents
- Customer Success, Projects, Live Assist, Meeting Links, Sales Dialer
- E-Sign, Developer Tools, Support

### Direct Links (have `more_options` icon or no arrow)
Click to navigate immediately:
- I Assistant, Dashboards, Forms, Process Design, Unibox, Vibe Coder
- Business Phone, AI Meeting Notetaker, Digital Employees, Developer Center
- Invoice Generator PRO, Data Enrichment, Meeting Router, Business Receptionist
- Mobile App, Landing Page, POS, Content Pilot, Num, Workbox HR
- **Add Apps** (at bottom) — opens the marketplace at `/market`

### CRM Custom Objects
The CRM group may also contain workspace-specific custom objects (e.g., `Funnel`, `Transactions`, `Branches`, `Partners`, `Brands`). These appear as sub-items under CRM at `/crm/<object_name>`.

---

## 3. Global UI Elements

### Search Bar ("Search SuperAGI")
- Located in top header bar
- Click to open — navigates to full-page search at `/search`
- Searches across ALL modules with tabbed results: **All**, **Contacts**, **Companies**, **Leads**, **Deals**
- Each tab shows a count of matching records
- Results display as table rows with entity-specific columns (e.g., Contacts show First Name, Last Name, Email, Phone, Company)
- Clicking a result navigates to that record's detail page

### Notification Bell
- Top-right header, shows a red badge with unread count (e.g., "25")
- Click to open a dropdown panel titled "Notifications"
- Lists notifications with: icon, type (e.g., "Sequence reply received"), person name, timestamp
- Notifications come from sequences, outreach campaigns, CRM activity, etc.

### User Avatar ("AK")
- Top-right corner, shows user initials
- Click to open dropdown with:
  - **User info**: initials + email (e.g., `adithyan.k@superagi.com`)
  - **WORKSPACES**: list of workspaces with checkmark on current one, option to switch, "Create New Workspace"
  - **Billing Overview**: shows remaining credits (e.g., "9,964,173 credits remaining")
  - **Settings** — navigates to `/settings`
  - **What's New?** — changelog/release notes
  - **Talk to Onboarding Assistant**
  - **Talk to Sales Assistant**
  - **Refer a business**
  - **Logout**

---

## 4. Settings Page (`/settings`)

Settings has its own left sidebar with two sections:

### PERSONAL
| Item | Description |
|------|-------------|
| Profile | User name, email, avatar |
| Availability | Calendar/availability settings |
| Personal Mailboxes | Connect email accounts for outreach |
| Personal LinkedIn | Connect LinkedIn account |
| Personal Tokens | API tokens for personal use |
| SSH Keys | SSH key management |

### WORKSPACE
| Item | Description |
|------|-------------|
| General | Workspace name, logo, timezone |
| Business Details | Company info |
| Security | Auth/SSO settings |
| Waterfall | Lead waterfall/routing config |
| Meeting Intelligence | Meeting analysis settings |
| Meeting Disposition | Post-meeting outcome tracking |
| Entity Scoring | Lead/contact scoring rules |
| Unibox | Unified inbox settings |
| Email Templates | Shared email templates |
| Customer Success | CS module configuration |
| Value Prop Templates | Standardized messaging for AI outreach |
| Email Campaign Settings | Campaign defaults |
| WhatsApp | WhatsApp integration |
| Support | Support module settings |
| Exports | Data export settings |
| Audit Trail | Activity logging |
| API Keys | Workspace API keys |
| Custom Events | Custom event definitions |
| Code Reviewer | Code review settings |

---

## 5. Core Sales Workflow

The typical sales workflow in SuperAGI follows this sequence:

### Step 1: Setup (one-time)
- **Connect mailboxes**: Settings → Personal Mailboxes (connect Gmail/Outlook for sending outreach)
- **Connect LinkedIn**: Settings → Personal LinkedIn
- **Create value prop templates**: Settings → Value Prop Templates (messaging used by AI SDR)
- **Configure outreach settings**: Settings → Email Campaign Settings

### Step 2: Find Leads (Prospecting)
- **Prospect → Prospect Leads** (`/prospect/find_leads`): Use filters or AI search to find matching leads by role, company, industry, location, company size, etc.
- **Prospect → Prospect Companies** (`/prospect/find_companies`): Search for companies, then find contacts within them
- **Prospect → Signals** (`/signals`): Monitor intent signals — job changes, funding rounds, news mentions, website visits

### Step 3: Enrich
- Auto-enrich email addresses when saving leads from Prospect
- **Data Enrichment** (`/data_enrichments`): Bulk enrich phone numbers, company data, and other fields

### Step 4: Save to CRM
- Save prospects to a **List** (CRM → Lists at `/list`) for organized outreach
- Or save directly to **CRM → Leads** (`/crm/leads`)
- Prospects become Leads once saved to CRM

### Step 5: Outreach (choose one approach)
- **Cold Outreach** (`/cold-outreach`): AI SDR handles prospecting + personalization + follow-ups at scale. Create a "Campaign" — the AI writes, sends, and follows up.
- **Sequences** (`/sequences`): Build manual multi-channel sequences with full control per step (email, LinkedIn, call, task). More hands-on than Cold Outreach.

### Step 6: Track & Respond
- **Unibox** (`/unibox`): Unified inbox — see replies across all channels (email, LinkedIn) in one place
- **Engage → Conversations** (`/conversations`): Conversation threads
- **Engage → Emails** (`/emails`): Email-specific tracking
- **Engage → LinkedIn** (`/linkedin/logs`): LinkedIn activity logs
- Campaign dashboards (within Cold Outreach/Sequences): Track Outputs, Replies, Opens, Analytics

### Step 7: Convert
- Move engaged leads to **CRM → Deals** (`/crm/deals`): Create deal records, manage through pipeline stages
- **CRM → CRM Tasks** (`/tasks`): Track follow-up tasks
- **CRM → Contacts** (`/crm/contacts`): Full contact records with activity history

### Step 8: Analyze
- **Analyze → Analytics** (`/analytics`): Performance reports and dashboards
- **Analyze → AI Analytics** (`/ai-analytics`): AI-powered insights
- **Dashboards** (`/dashboards`): Custom dashboards

---

## 6. Feature Dependency Chain

What must be set up before what:

```
Settings → Personal Mailboxes     ──→  Cold Outreach / Sequences (email steps)
Settings → Personal LinkedIn      ──→  Sequences (LinkedIn steps), Engage → LinkedIn
Settings → Value Prop Templates   ──→  Cold Outreach (AI uses these for messaging)
Settings → Email Campaign Settings ──→ Cold Outreach / Marketing Campaigns

Prospect → Find Leads             ──→  Save to List or CRM Leads
CRM → Lists                       ──→  Cold Outreach / Sequences (select leads from list)
CRM → Leads                       ──→  Deals pipeline

Add Apps (/market)                 ──→  Some sidebar items only appear after enabling the app
```

**Key dependencies:**
1. You MUST connect at least one mailbox before creating email outreach campaigns
2. You MUST connect LinkedIn before using LinkedIn sequence steps
3. Value Prop Templates improve Cold Outreach AI quality but aren't strictly required
4. Some sidebar sections (e.g., Voice Agents, Support, E-Sign) require enabling via **Add Apps** (`/market`) first
5. CRM custom objects appear in sidebar only after creation in CRM settings

---

## 7. Terminology Glossary

| Term | Definition |
|------|-----------|
| **Campaign** | An outreach effort in Cold Outreach — AI-driven, handles prospecting + personalization + follow-ups automatically |
| **Sequence** | A multi-step outreach workflow built manually in Sequences — you define each step (email, LinkedIn, call, task) with timing |
| **Prospect** | A lead found via the Prospect module (not yet saved to CRM) |
| **Lead** | A prospect that's been saved to CRM (lives in CRM → Leads) |
| **Contact** | A person record in CRM (CRM → Contacts) — may or may not be a sales lead |
| **Company** | An organization record in CRM (CRM → Companies) |
| **Deal** | A sales opportunity tracked through pipeline stages (CRM → Deals) |
| **Signal** | An intent trigger — job change, funding round, news mention, or website visit (Prospect → Signals) |
| **Unibox** | Unified inbox across all communication channels — see all replies in one place |
| **Value Prop Template** | Standardized messaging template used by Cold Outreach AI to generate personalized emails |
| **List** | A collection of leads organized for outreach (CRM → Lists) |
| **Cold Outreach** | The AI SDR module — fully automated email outreach with AI-written, personalized messages |
| **Custom Object** | User-defined CRM entity (e.g., Funnel, Transactions) — appears as sub-item under CRM |
| **Workspace** | An organizational unit — users can belong to multiple workspaces, switch via avatar menu |

---

## 8. How to Navigate

### To reach a page by URL (fastest):
Navigate directly: `browser_open https://sales.superagi.com<path>` using the URL map above.

### To reach an expandable sidebar section:
1. `browser_snapshot` to see the sidebar
2. Find the group with `right_arrow_small` icon (e.g., `StaticText "Prospect"`)
3. The group text is NOT a link ref — use `browser_eval` to click it:
   ```
   browser_eval: (function(){ const spans = document.querySelectorAll('span'); for(const s of spans){ if(s.textContent.trim()==='Prospect') { s.click(); return 'expanded'; }} return 'not found'; })()
   ```
4. `browser_snapshot` again — sub-items now appear as `link` refs (e.g., `link "Prospect Leads more_options" [ref=eNN]`)
5. Click the sub-item ref: `browser_click @eNN`

### To reach a direct link in sidebar:
1. `browser_snapshot` — find the link ref (e.g., `link "dashboards_icon Dashboards more_options" [ref=eNN]`)
2. `browser_click @eNN`

### To reach Settings:
- Direct: `browser_open https://sales.superagi.com/settings`
- Or: click AK avatar → Settings

---

## 9. Key Gotchas

1. **Sidebar group collapse**: Expanding one group collapses the previously expanded group. If you expanded "Engage" then click "Prospect", Engage sub-items disappear.

2. **Expandable groups are NOT link refs**: They appear as generic elements with `StaticText` + `right_arrow_small` image, not as clickable `link` refs. You must use `eval` with JS click or click the text content directly.

3. **Some sections need apps enabled first**: Items like Voice Agents, E-Sign, Support (inbound agent), etc. may not appear or may show empty states until enabled via Add Apps (`/market`).

4. **Settings page loads async**: After navigating to `/settings`, the settings sidebar and content load asynchronously. Wait 1-2 seconds before snapshotting.

5. **Refs become stale after navigation**: After clicking a link that changes the page URL, all previously captured `@eNN` refs are invalid. Always re-snapshot after navigation.

6. **Search navigates away**: Clicking the "Search SuperAGI" bar and typing will navigate to `/search` — you leave the current page. Use browser back or direct URL to return.

7. **Custom objects in CRM**: The CRM section may contain workspace-specific custom objects (e.g., `movies`, `test sources`, `Funnel`). These are NOT standard — they vary by workspace.

8. **URL inconsistency**: Some URLs don't follow a consistent pattern — e.g., Lists is `/list` (not `/crm/lists`), CRM Tasks is `/tasks` (not `/crm/tasks`), Unibox is `/unibox`. Always use the URL map above.
