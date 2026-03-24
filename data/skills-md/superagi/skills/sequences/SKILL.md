---
name: sequences
description: Create and manage multi-channel outreach sequences in SuperAGI Sales CRM
platform: [linux, macos]
---

# SuperAGI Sales CRM — Sequences

Sequences are manually-built, multi-channel outreach workflows with granular control over each step. Unlike **Cold Outreach** (`/cold-outreach`), which is an AI SDR that automates lead sourcing + personalization + follow-up at scale, Sequences give you full control over step ordering, timing, content, and channel mix. You build the sequence step-by-step, add contacts yourself, and decide exactly what happens at each touchpoint.

**Direct URL:** `https://sales.superagi.com/sequences`
**Sidebar path:** Engage > Sequences

## Sequences List Page (`/sequences`)

**Left sidebar:** Folder system for organizing sequences. "All Sequences" is the default. Custom folders can be created (add_icon) or deleted (delete_icon).

**Search & Create:**
- `Search Sequences` textbox — filter sequences by name
- `Create Sequence` button (top-right) — opens creation modal

**Filters bar:** Three dropdowns above the table:
- **Status** dropdown — filter by sequence status
- **Created Date** dropdown — filter by creation date
- **Tags** dropdown — filter by tags

**Sequence table columns:**
| Column | Description |
|--------|-------------|
| Name | Sequence name (clickable — opens detail page at `/sequences/{id}`) |
| Status | Status with color-coded dot indicator (e.g., Inactive white_dot) |
| Total Contacts/Leads | Number of contacts/leads in the sequence |
| Active | Currently active contacts |
| Finished | Contacts that completed all steps |
| Replied | Contacts that replied |
| Sent | Total messages sent |

Each row has a **more_icon** for row actions (three-dot menu).

**Pagination:** Bottom of table. Page numbers with left/right arrows. "20 per page" selector.

## Sequence Statuses

| Status | Dot Color | Meaning |
|--------|-----------|---------|
| Inactive | white_dot | Created but not launched or paused |
| Active | colored_dot | Currently running, sending outreach |
| Paused | white_dot | Temporarily stopped |
| Completed | white_dot | All contacts finished the sequence |

## Creating a Sequence

### Step 1: Create Sequence Modal

Click "Create Sequence". A modal appears with:

- **Sequence Name** — text field (placeholder: "Enter new Sequence name")
- **Build from scratch** — "Create a new Sequence from ground up" (radio card, default selected)
- **Choose a Prebuilt Template** — "Select a Sequence template from our library" (radio card)
- **Who can access** — dropdown (e.g., "Team can view and edit")
- **Tags** — "Add tags to organize your Sequence" (multi-tag input)
- **Continue** button (disabled until name is entered)

### Path A: Build from Scratch

Clicking Continue with "Build from scratch" selected creates the sequence and opens the detail page at `/sequences/{id}`. The sequence starts empty — you add steps via the "+ Add a new step" button.

### Path B: Choose a Prebuilt Template

Clicking Continue with "Choose a Prebuilt Template" selected navigates to the template picker at `/sequences/templates`.

**Template picker layout:**
- **Left sidebar categories:**
  - Sales outreach
  - People signal-based targeting
  - Company signal-based targeting
  - LinkedIn-based targeting
- **Search templates** textbox at top
- **Template cards** showing: name, description, step count, duration

**Available Prebuilt Templates:**

| Template | Category | Description |
|----------|----------|-------------|
| High Value Account Outreach | Sales outreach | Engage key decision-makers at high-value accounts. Combines targeted emails, Call tasks and LinkedIn touchpoints. 7 steps, 14 days. |
| Reachout to Website Visitors | Sales outreach | Multi-channel outreach to engage visitors who browsed your site, using contextualized website activity. 5 steps, 8 days. |
| Funding Announcement | Company signal-based | Target companies that recently received funding |
| Leadership Change | Company signal-based | Target companies with recent leadership changes |
| Job Posting | Company signal-based | Target companies with relevant job postings |
| Job change by Prospects | People signal-based | Target prospects who recently changed jobs |
| Convert Inbound Leads | Sales outreach | Convert inbound leads with multi-step follow-up |
| Multi Channel Outreach | Sales outreach | Multi-channel sequence combining email, LinkedIn, and calls |
| LinkedIn Nurture Flow | LinkedIn-based | LinkedIn-focused nurture sequence |
| Onboarding Template | Sales outreach | Onboarding sequence for new customers/users |

## Sequence Detail Page (`/sequences/{id}`)

**Header:**
- Back arrow — returns to sequence list
- Sequence name with edit_icon for renaming
- **Add Contacts/Leads** button (dropdown arrow)
- **Launch** button (green, with play icon)

### Seven Tabs

| Tab | What it shows |
|-----|---------------|
| Overview | Sequence steps with stats and step builder |
| Contacts/Leads | All contacts/leads added to this sequence |
| Emails | Email activity across the sequence |
| LinkedIn | LinkedIn activity across the sequence |
| Audit Trail | History of changes to the sequence |
| Analytics | Performance metrics and charts |
| Settings | Sequence configuration (schedule, rules, etc.) |

### Overview Tab (Default)

Shows the sequence steps in vertical order. Each step card displays:

- **Step number and type** — e.g., "1. AI Email Agent - Day 1"
- **Schedule description** — e.g., "Scheduled immediately after the person is added to Sequence" or "Step 2 - Schedule in 2 days if no reply received"
- **Stats:** Total Complete, Total Active, Paused, Replies
- **Toggle switch** — enable/disable the step
- **Variants:** Each variant (A, B, C, D) shows: variant letter, thread name (e.g., "New Thread"), and stats (Total Sent, Total Open, Clicks, Replies)
- **+ Add A/B** — add A/B test variants to the step
- **Three-dot menu** — step actions (edit, delete, etc.)

**"+ Add a new step"** button at the bottom opens the step type selector modal.

## Step Types

The "Add Step" modal organizes step types into three categories:

### Agents (AI-powered, auto-generate content)

| Step Type | Description |
|-----------|-------------|
| AI Email Agent | Automatically creates and sends AI-personalized emails to prospects |
| Qualification Agent | Assesses and qualifies leads based on predefined criteria |
| Market Research Agent | Researches prospects and companies automatically |
| Multi Threading Agent | Automatically engage multiple stakeholders within a single company |
| AI LinkedIn - Message Agent | Automatically creates and sends AI-personalized LinkedIn messages |
| AI LinkedIn - InMail Agent | Automatically creates and sends AI-personalized LinkedIn InMails |

### Automatic (you write content, system sends it)

| Step Type | Description |
|-----------|-------------|
| Automatic Email | Emails are delivered automatically without manual effort |
| Automatic LinkedIn - Message | Send LinkedIn Messages automatically |
| Automatic LinkedIn - InMail | Send LinkedIn InMails automatically |
| Automatic LinkedIn - Connection Request | Send LinkedIn connection requests with or without note automatically |
| Automatic WhatsApp Message | Send WhatsApp messages automatically |

### Manual (creates a task for the user to complete)

| Step Type | Description |
|-----------|-------------|
| Manual Email Task | Task is created to send an email manually |
| Manual Phone Call Task | Task is created to make a phone call |
| Manual LinkedIn - Message Task | Task is created to send a LinkedIn message to a prospect |
| Manual LinkedIn - InMail Task | Task is created to send a LinkedIn InMail to a prospect |
| Manual LinkedIn - Connection Request Task | Task is created to send a LinkedIn Connection Request to a prospect |
| Manual WhatsApp Message Task | Task is created to send a WhatsApp message to a prospect |

## Step Editors

### AI Email Agent Editor (`/sequences/{id}/step/{stepId}/edit`)

Split-pane layout with Cancel and "Save & Continue" buttons.

**Left pane:**
- "Write a prompt for the AI agent" — textarea where you describe what the email should accomplish
- Checkbox: **Insert Email Signature**
- Checkbox: **Insert Meeting Agent**

**Right pane — Preview:**
- "Select Contact/Lead" dropdown — pick a contact to preview personalization
- To: contact name <contact@email.com>
- Subject: (AI-generated)
- Message: (AI-generated)
- **Generate Preview** button — generates a sample email based on the prompt

### Automatic Email Editor

Split-pane layout with Cancel and "Save & Continue" buttons.

**Left pane — Message Details:**
- Checkbox: **Reply to previous thread** — sends as a reply to the previous email step
- **Subject** field with personalization token insertion
- **Rich text editor** with toolbar: text formatting (Normal/Bold/Italic/Underline/Strikethrough), links, personalization tokens, ordered/unordered lists, indentation, code blocks
- **Email body** — write the full email content manually
- Bottom toolbar actions:
  - **+ Insert** — insert dynamic content
  - **Attach Files** — attach files to the email
  - **Email Template** — select from saved email templates
  - **AI Personalize** — AI-powered personalization of the email
  - **Personalize** — insert personalization tokens (First Name, Last Name, Full Name, Current Company, etc.)

**Right pane — Preview:** Same structure as AI Email Agent preview.

### Step Timing

Each step (except step 1) has configurable timing:
- **Immediately** — runs right after the previous step
- **Delay** — wait N minutes/hours/days before executing
- **Condition** — "if no reply received" (common for follow-up steps)

Step 1 is always "Scheduled immediately after the person is added to Sequence."

### A/B Testing

Each step supports up to 4 variants (A, B, C, D) for A/B testing:
- Click "+ Add A/B" on any step to add a variant
- Each variant has its own content/prompt
- Stats are tracked per variant (Sent, Open, Clicks, Replies)
- Toggle switches control which variants are active

## Adding Contacts to a Sequence

Click "Add Contacts/Leads" dropdown button in the header. Three methods:

| Method | Description |
|--------|-------------|
| **Prospect** | Search and add individual prospects from the CRM |
| **Select a list** | Choose an existing contact list from your CRM |
| **Select Manually** | Manually select specific contacts |

## Settings Tab

### General
- **Who can access** — permission dropdown (e.g., "Team can view and edit")

### Schedule
- **Timezone** — dropdown (e.g., "Asia/Kolkata")
- **Use lead's local timezone** — checkbox: "Use the lead/contact's local time zone instead of the schedule's time zone, if the lead/contact contains location data."
- **Active Days** — day pills (Monday through Friday by default, removable/addable)
- **Tags** — "Add tags to organize your Sequences" (with "Press Enter or comma to add new tags")
- **Start Time** — dropdown (e.g., "9:00am")
- **End Time** — dropdown (e.g., "5:30pm")

### Additional Settings (toggle switches)

The Settings tab contains multiple toggle switches for advanced configuration including:
- **Execution rules** — control how steps execute
- **Lead handling** — rules for managing leads in the sequence
- **Fallback options** — what happens when a step can't execute
- **Duplicate prevention** — prevent contacts from being added to the same sequence twice
- **Timing behavior** — additional timing controls beyond the schedule

## Launch Validation

Clicking "Launch" validates the sequence before activation. Known validations:
- **Active variants required** — all steps must have at least one active variant. Error toast: "Steps 1, 2, 3 have no active variant"
- **Sender settings** — email steps require connected mailboxes; LinkedIn steps require connected LinkedIn account
- **Contacts** — sequence should have contacts added (or they can be added after launch)

## URL Patterns

| URL | What it shows |
|-----|---------------|
| `/sequences` | Sequence list page with folders, search, filters |
| `/sequences/templates?name=...&permission=...&tags=[]` | Prebuilt template picker |
| `/sequences/{id}` | Sequence detail page (Overview tab default) |
| `/sequences/{id}?tab=settings` | Sequence settings tab |
| `/sequences/{id}/step/{stepId}/edit` | Step editor for a specific step variant |

## Key Dependencies & Relationships

- **Personal Mailboxes** (Settings) — must have connected mailboxes for email steps (Automatic Email, AI Email Agent). The sender mailbox is configured per sequence.
- **Personal LinkedIn** (Settings) — required for all LinkedIn step types (messages, InMails, connection requests)
- **Email Templates** (Library) — reusable templates available in the Automatic Email step editor via "Email Template" button
- **Contact Lists** (CRM) — used by the "Select a list" method when adding contacts
- **Meeting Agent** — can be inserted into AI Email Agent steps via "Insert Meeting Agent" checkbox
- **Email Signatures** — insertable via "Insert Email Signature" checkbox in AI Email Agent, or via signature tokens in Automatic Email

## Gotchas & Non-Obvious Behaviors

- **Sequence links use click handlers, not href** — like Cold Outreach, the `<a>` tags in the list have no `href`. You must click the inner `<div>` containing the sequence name text to navigate. Clicking the outer `<a>` does nothing.
- **"Build from scratch" vs template creates different initial states** — Build from scratch creates an empty sequence at `/sequences/{id}`. Template selection goes to `/sequences/templates` first.
- **Step numbering includes day counts** — Step names show "Day N" calculated from cumulative delays (e.g., "AI Email Agent - Day 1", "Automatic Email - Day 3").
- **AI Agent steps vs Automatic steps have completely different editors** — AI Agent steps take a prompt and auto-generate content. Automatic steps have a full rich text editor where you write the content manually.
- **A/B variants must be active for launch** — The Launch button validates that every step has at least one active variant (toggle switch on). Without this, launch fails with an error toast.
- **Settings tab can be slow to load** — The settings tab sometimes shows "Loading.." for extended periods. The `?tab=settings` URL parameter navigates directly to it.
- **The "Add Contacts/Leads" button is a dropdown, not a direct action** — Clicking it shows three options: Prospect, Select a list, Select Manually.
- **Template picker has categories** — Templates are organized into 4 categories (Sales outreach, People signal-based targeting, Company signal-based targeting, LinkedIn-based targeting) accessible via left sidebar.
- **WhatsApp steps are available** — In addition to Email and LinkedIn, sequences support WhatsApp messages (both Automatic and Manual).
- **Multi Threading Agent** enables multi-stakeholder outreach within a single company, engaging multiple contacts at the same organization.
