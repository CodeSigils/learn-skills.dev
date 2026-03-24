---
name: cold-outreach
description: Create and manage cold outreach campaigns in SuperAGI Sales CRM
platform: [linux, macos]
---

# SuperAGI Sales CRM — Cold Outreach

Cold Outreach is SuperAGI's AI SDR (Sales Development Representative). It automatically finds leads matching your ICP, personalizes multi-step email and LinkedIn sequences, and follows up — all at scale. This is distinct from **Sequences** (`/sequences`), which are manually-built multi-channel sequences with more granular control. Cold Outreach is volume-oriented and AI-driven; Sequences are manual and step-by-step.

**Direct URL:** `https://sales.superagi.com/cold-outreach`
**Sidebar path:** Engage → Cold Outreach

## Cold Outreach List Page (`/cold-outreach`)

The page has two top-level tabs:
- **Campaigns** — the campaign list (default view)
- **Replies** — a cross-campaign view of all leads who replied (shows count, e.g. "Replies 337")

### Campaigns Tab

**Left sidebar:** Campaign folders for organizing campaigns. "All Campaigns" is the default folder. Custom folders can be created (add_icon) or deleted (delete_icon). Each folder has a three-dot menu with "Add Members" to move campaigns into folders.

**Filters bar:** Two dropdown filters above the table:
- **Status** dropdown — filter by campaign status
- **Created Date** dropdown — filter by creation date

**Search & Create:**
- `Search campaigns` textbox — filter campaigns by name
- `Create Campaign` button (top-right) — opens campaign creation modal

**Campaign table columns:**
| Column | Description |
|--------|-------------|
| Name | Campaign name (clickable — opens detail/editor) |
| Status | Status with color-coded dot indicator |
| Total Leads | Number of leads in campaign |
| Total Sent | Emails/messages sent |
| Total Clicks | Link clicks tracked |
| Replies | Reply count |
| Created on | Creation date (MM/DD/YYYY) |

Each row also has a three-dot **more_icon** for row actions.

**Pagination:** Bottom of table. Shows page numbers with left/right arrows. Includes a "20 per page" selector to adjust page size.

### Replies Tab (Top-Level)

Shows all replies across all campaigns in one unified view. This is useful for sales teams to triage responses without opening individual campaigns.

**Columns:** Name (with avatar/initials), Current Company, Campaign Name, Category, Replied on

**Reply Categories** (AI-classified):
- **Interested** — lead expressed interest
- **Not Interested** — lead declined
- **Out Of Office** — auto-reply / OOO
- **Do Not Contact** — requested removal
- **Information Request** — asked for more details
- **Wrong Person** — not the right contact
- **Meeting Request** — wants to schedule a call

**Filters:** Campaign dropdown, Category dropdown

**Left sidebar:** "All Replies" folder with ability to create custom reply folders.

## Campaign Statuses

| Status | Dot Color | Meaning |
|--------|-----------|---------|
| Draft | white_dot | Created but not launched. Opens in wizard editor (`/campaigns/{id}/edit`) |
| In Progress | colored dot | Actively sending outreach |
| Paused | white_dot | Temporarily stopped. Can be resumed |
| Completed | white_dot | Finished sending all outreach steps |

## Creating a Campaign

### Step 1: Create Campaign Modal

Click "Create Campaign" button. A modal appears with:

- **Campaign name** — text field (defaults to "Untitled campaign")
- **Type** — three options (radio-style cards):
  1. **Find new leads** (AUTOMATED) — "Let SuperAGI source and enrich leads" — AI finds and enriches leads matching your ICP. This is the primary Cold Outreach flow.
  2. **Select a list** (MANUAL_LIST) — "Select an existing list in SuperAGI" — use an existing contact list from your CRM.
  3. **Automate your outreach** (AUTOMATION) — "Outreach is automated based on events" — trigger outreach based on CRM events.
- **Create** button — creates the campaign and opens the wizard

### Step 2: Campaign Creation Wizard

After creation, the wizard opens at `/campaigns/{id}/edit`. It has a 5-step stepper at the top. Navigation uses **Back** and **Continue** buttons (the last step shows **Launch Campaign** instead of Continue).

The campaign name is shown at the top with an **Edit_Icon** for renaming.

#### Step 1: Create ICP (Ideal Customer Profile)

Only shown for "Find new leads" type. Defines the target audience with expandable filter sections:

- **Lead Name** — search for specific people
- **Job Title** — target role titles
- **Department** — e.g., business_development, engineering
- **Seniority** — e.g., entry, manager, VP, C-suite
- **HQ Location** — company headquarters region (e.g., APJ, EMEA)
- **Lead Location** — where the contact is based
- **Industry** — e.g., Airlines/Aviation, SaaS, etc.
- **Technologies** (info tooltip) — tech stack filters
- **Revenue Range** — company revenue filter
- **Employee Range** — company size filter
- **Target Company Domains** (info tooltip) — specific company websites
- **Company Keywords** (info tooltip) — keyword-based company matching
- **Funding Stage** — e.g., Series A, Series B
- **Founded Year** — filter by company age

**Preview Leads** button at the bottom shows estimated lead count matching the ICP criteria. Shows "No results found!" when no matches or filters are too narrow.

#### Step 2: Define Value Prop

Defines what your outreach will say. This is the core messaging configuration.

- **Value Prop Template** — dropdown to select a saved template (from Settings → Value Prop Templates)
- **Company Website** — your company URL (used for AI research)
- **Generate Template** button — AI auto-fills all fields below by researching the website
- **Company Name*** (required) — your company name
- **What are you selling*** (required) — description of product/service (info tooltip available)
- **Pain Points** — list of customer pain points (add/remove with +Add and close_icon buttons)
- **Value Propositions** — list of value props (add/remove)
- **Proof Points** — social proof, case studies, metrics (add/remove)
- **Personality** — tone dropdown (e.g., "😊 Friendly")
- **Outreach Language** — language dropdown (e.g., "🇺🇸 American English")
- **Train Cold Outreach for Emails** — textarea to provide sample emails for AI training
- **Give Instructions to Cold Outreach** — textarea for custom AI instructions (+ Add for multiple)
- **Call to action** toggle — when enabled, shows:
  - CTA Button Text (e.g., "Call Us Today")
  - CTA Link Type dropdown (e.g., "Meeting Agent Link")
  - CTA Link dropdown (meeting link URL)

#### Step 3: Sender Details

Configures which email accounts send the outreach.

- **Mailbox Rotation** toggle (switch) — "Dynamically use any of the selected mailboxes to improve email deliverability." Links to **settings** page to connect more mailboxes.
- **Mailbox table** with columns:
  - Checkbox — select/deselect mailbox for this campaign
  - **Sender Account** — email address (with prefix icon)
  - **Display name to be shown in email body** — combobox (e.g., "Use Name"). Only enabled for checked mailboxes.
  - **Edit** button — edit display name details. Only enabled for checked mailboxes.

The mailboxes shown come from **Settings → Personal Mailboxes**. You must have at least one mailbox connected before creating campaigns.

#### Step 4: Approve Outreach

Defines the outreach sequence — what emails/messages to send and when.

**Top controls:**
- **Template** toggle (switch) — show as template vs. final
- **AI Personalized** label with agi_icon
- **Regenerate All** button — regenerate all step content

**Info banner:** "This is a sample outreach thread. When sending out, each outreach is personalized"

**Outreach steps** (vertical sequence with step_icon connectors):

1. **Email Outreach** (first step, always email):
   - Subject line (textbox, may be disabled in template mode)
   - Email body with template variables: `{{contact.firstname | default: ''}}`, `{{contact.company | default: ''}}`, `{{email.signature | default: ''}}`
   - Links in email body are shown as `<link>` elements (e.g., meeting links, CTAs)
   - **Regenerate** button — regenerate this step only
   - **delete_icon** button — remove this step

2. **Follow Up Emails** (subsequent steps):
   - "Wait for" delay control: spinbutton (number) + combobox (unit: Days)
   - Increase/Decrease Value buttons for the delay
   - Same body structure with template variables
   - Regenerate and delete buttons per step

**+ Add Step** button (with dropdown arrow) — adds new outreach steps. Steps can be Email or LinkedIn (connection request, message, InMail).

#### Step 5: Automate

Final configuration before launch.

- **Daily Leads Quota** — number of leads to prospect daily (default: 30, editable). Shows calculated max emails (e.g., "Maximum of 120 emails will be sent approx. in this campaign per day")

- **Mode selection** (two cards):
  - **Manual** — "Your approval will be required before sending emails" (tick_icon when selected)
  - **Autopilot** — "SuperAGI will send out all the emails by itself"

- **Toggles:**
  - "Exclude people from lists" (switch)
  - "Exclude people already added in SuperAGI" (switch, default on)

- **Advanced Filters** (collapsible section):
  - **Timezone** — combobox (e.g., "Asia/Kolkata")
  - **Active Days** — day pills (Monday–Friday default) with add combobox
  - **Start Time** — combobox (e.g., "9:30am")
  - **End Time** — combobox (e.g., "5:30pm")
  - **Add unsubscribe link to Campaign** — toggle with description
  - **Limit leads per company** — toggle to restrict enrichment from single company
  - **Send to CC and BCC emails** — toggle to include CC/BCC addresses

- **Launch Campaign** button — launches the campaign (replaces "Continue")

## Campaign Detail Page (Launched Campaigns)

**URL pattern:** `/campaigns/{id}` (no `/edit` suffix — draft campaigns use `/campaigns/{id}/edit`)

**Header:**
- Back arrow (variant1_back_arrow) — returns to campaign list
- Campaign name with Edit_Icon for renaming
- **Edit** button — opens campaign in wizard editor
- **Status button** with dropdown arrow (e.g., "Paused ▼") — change status (pause/resume/etc.)

### Four Tabs

#### Outputs Tab
Shows all leads in the campaign and their current state.
- **Filter combobox** — "All" by default, can filter by lead status
- Table of leads with campaign progress per lead
- Click a lead's "Campaign Status" to see which outreach step they're on and what's been completed
- Shows "No results found!" with empty_icon when no leads

#### Replies Tab (Campaign-Level)
Shows all leads who replied within this specific campaign.
- Same structure as top-level Replies but scoped to this campaign
- Shows reply count in tab label (e.g., "Replies 0")

#### Analytics Tab
Campaign performance metrics and charts.

- **Time range filter** — combobox (e.g., "Last 30 days")
- **Total leads count** — shown prominently

**Email section** (heading level 2):
- Metrics: Sent, Opened, Clicked, Replies, Positive Replies, Bounced, Unsubscribed, Skipped
- SVG line chart over time with legend (Sent, Opened, Clicks, Replies, Bounced, Unsubscribed, Skipped)

**LinkedIn section** (heading level 2):
- Metrics: Connections Sent, Connections Accepted, Messages Sent, Message Replies, Inmails Sent, Inmails Replies, Skipped
- SVG line chart with legend (Connections Sent, Messages Sent, Message Replies, InMails Sent, InMail Replies, Skipped, Connections Accepted)

#### Overview Tab
Read-only summary of campaign configuration, organized in 5 sub-sections (clickable tabs within the tab):

1. **ICP** — displays all ICP filter values (Current Role, Department, Seniority, Company HQ Location, Contact Location, Industry, Technologies, Revenue Range, Employee Range, Target Specific Companies, Funding Stage). Shows "--" for unset fields.
2. **Value Prop** — company details, pain points, value propositions, proof points
3. **Sender Details** — selected mailboxes and rotation config
4. **Outreach Messaging** — the email/LinkedIn sequence steps
5. **Automation** — daily quota, manual/autopilot mode, schedule settings

## Key Dependencies & Relationships

- **Personal Mailboxes** (Settings) — must have at least one connected mailbox for Sender Details step. The Sender Details step links directly to settings.
- **LinkedIn Account** (Settings) — required for LinkedIn outreach steps (connection requests, messages, InMails)
- **Value Prop Templates** (Settings) — reusable templates that can be selected in the Define Value Prop step
- **Contact Lists** (CRM) — used by "Select a list" campaign type
- **Meeting Links** — CTA links can reference Meeting Agent Links configured in the platform

## Template Variables

Outreach emails use Liquid-style template variables that get personalized per lead:
- `{{contact.firstname | default: ''}}` — lead's first name
- `{{contact.company | default: ''}}` — lead's company name
- `{{email.signature | default: ''}}` — sender's email signature

## URL Patterns

| URL | What it shows |
|-----|---------------|
| `/cold-outreach` | Campaign list page with Campaigns and Replies tabs |
| `/campaigns/{id}/edit` | Campaign creation/edit wizard (for Draft campaigns) |
| `/campaigns/{id}` | Campaign detail view with Outputs/Replies/Analytics/Overview (for launched campaigns) |

## Gotchas & Non-Obvious Behaviors

- **Campaign links in the list use `role="link"` on `<a>` tags with no `href`** — they are click-handler-driven, not standard links. Clicking the campaign name text (the inner div) is what navigates, not the outer link element.
- **Draft vs launched URL difference**: Clicking a Draft campaign opens `/campaigns/{id}/edit` (wizard). Clicking a launched/paused campaign opens `/campaigns/{id}` (detail view with tabs).
- **The Create Campaign modal persists** — if you switch tabs (Campaigns ↔ Replies) while the modal is open, it stays visible. Press Escape or click close_icon to dismiss.
- **Mailbox checkboxes control editability** — in Sender Details, unchecked mailboxes have disabled display-name combobox and edit button. You must check the mailbox first.
- **Wizard step navigation** — the stepper labels (Create ICP, Define Value Prop, etc.) are clickable to jump between steps. You don't have to go sequentially.
- **AI Personalized toggle** in Approve Outreach changes whether email subjects/bodies are auto-personalized per lead. The template view shows sample content; actual sends are personalized.
- **Daily Leads Quota math** — the quota (e.g., 30 leads) multiplied by outreach steps determines the approximate daily email count shown.
- **Page count can be large** — campaigns are paginated at 20 per page with potentially 26+ pages. Use search to find specific campaigns rather than paginating.
- **Reply categories are AI-assigned** — the system automatically classifies replies (Interested, Not Interested, Out Of Office, etc.) which appear in the Replies tab.
