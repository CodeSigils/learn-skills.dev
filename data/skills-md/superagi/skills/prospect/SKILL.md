---
name: prospect
description: Find and filter prospect leads and companies, enrich data, and track buying signals in SuperAGI Sales
platform: [linux, macos]
---

# SuperAGI Sales — Prospecting

Prospecting is how you find potential customers from SuperAGI's external database — these are NOT contacts already in your CRM. You search SuperAGI's database of people and companies, then save matches into your CRM (Leads/Companies) or add them directly to outreach Sequences. This is the top of the sales funnel: find people → enrich their data → reach out.

## Sidebar Navigation

Click "Prospect" in the sidebar to expand. Four sub-sections:
- **Prospect Leads** → `https://sales.superagi.com/prospect/find_leads`
- **Prospect Companies** → `https://sales.superagi.com/prospect/find_companies`
- **Signals** → `https://sales.superagi.com/signals`
- **Anonymous Website Visitors** → `https://sales.superagi.com/website_visitors`

Data Enrichment is a separate sidebar app at `https://sales.superagi.com/data_enrichments`.

---

## 1. Prospect Leads (Find Leads)

**URL:** `https://sales.superagi.com/prospect/find_leads`
**Purpose:** Search SuperAGI's database for individual people matching your ideal customer profile.

### Page Layout

**Top tabs:** "Find Leads" (default) | "Find Companies"

**Action bar (always visible):**
- **Add to List** (dropdown) — save selected leads to a new or existing list
- **Add to Sequence** (dropdown) — add selected leads directly to an outreach sequence
- **Add to Leads** (button, disabled until leads selected) — save to CRM > Leads (auto-enriches email)

**Three search modes (toggle between them):**
1. **Search with filters** — manual filter-based search (default view, shows filter panel on left)
2. **Search with AI** — natural language search with a textbox: `"Describe the leads you're looking for..."`
3. **Saved Search** — access previously saved filter sets or AI prompts

### Filter Panel (Search with filters mode)

Left-side panel with 14 collapsible filter categories. Click the filter name or toggle icon to expand/collapse each.

| Filter | Input Type | Details |
|--------|-----------|---------|
| **Lead Name** | Free text input | `"Enter lead name"` — search by person's name |
| **Job Title** | Multi-select combobox | `"Select Job Title(s)"` — type to search, select multiple. Has **Exclude Job Title** toggle |
| **Department** | Multi-select combobox | `"Select Department(s)"` — e.g., Engineering, Sales, Marketing. Has **Exclude Department** toggle |
| **Seniority** | Multi-select combobox | `"Select Seniority(s)"` — C-Suite, VP, Director, Manager, etc. Has **Exclude Seniority** toggle |
| **Lead Location** | Multi-select combobox | `"Select Lead Location(s)"` — where the person is located. Has **Exclude Lead Location** toggle |
| **HQ Location** | Multi-select combobox | `"Select HQ Location(s)"` — company headquarters location. Has **Exclude HQ Location** toggle |
| **Industry** | Multi-select combobox | `"Select Industry(s)"` — company industry vertical. Has **Exclude Industry** toggle |
| **Technologies** | Multi-select combobox | `"Select Technologies(s)"` — tech stack used by the company. Has **Include at least one (OR)** / **Include all (AND)** toggle + **Exclude Technologies** |
| **Revenue Range** | Min/Max comboboxes | Two dropdowns for minimum and maximum company revenue |
| **Employee Range** | Multi-select combobox | `"Select Employee Range(s)"` — predefined company size ranges to pick from |
| **Target Company Domains** | Multi-select combobox | `"Select Target Company Domains(s)"` — specific domains. Also: **Upload a CSV** and **Select a list** options. Has **Exclude** toggle |
| **Company Keywords** | Multi-select combobox | `"Select Company Keywords(s)"` — keywords in company description. Has **Include at least one (OR)** / **Include all (AND)** toggle + **Exclude Company Keywords** |
| **Funding Stage** | Multi-select combobox | `"Select Funding Stage(s)"` — Seed, Series A, etc. Has a **Date Range** combobox (default: "All Time") |
| **Founded Year** | Min/Max comboboxes | Two dropdowns for minimum and maximum founding year |

**Bottom buttons:**
- **Clear filters** — resets all active filters (disabled when no filters set)
- **Save filters** — saves current filter combination for reuse (disabled when no filters set)

**Default state:** Shows illustration with "Find your ideal leads" and "Enter details about your ideal leads. SuperAGI will find prospects that suit your criteria."

### AI Search Mode

When you click "Search with AI":
- Filter panel disappears, replaced by a textbox: `"Describe the leads you're looking for..."`
- Type a natural language query (e.g., "Find VPs of Engineering at SaaS companies")
- Click the **Search with AI** button to run
- **Clear prompt** button clears the textbox
- **Save prompt** button saves the AI search prompt for reuse via "Saved Search"
- Results appear immediately with estimated total count

### Lead Results

Each lead result row shows:
- **Checkbox** — for bulk selection
- **Initials/avatar** — person's initials
- **Name** — full name (clickable). If already in your CRM, shows a "LEAD" badge
- **LinkedIn** icon — link to their LinkedIn profile
- **Access Email** button — click to reveal/enrich email address (costs enrichment credits)
- **Access Phone** button — click to reveal/enrich phone number (costs enrichment credits)
- **Job Title** — current role
- **Company** — company initial + name + LinkedIn + website icons
- **Industry** — company's industry
- **Technologies/Keywords** — tech stack tags (e.g., "salesforce cloud", "product engineering", "+17" for overflow)
- **Row action icons:** email, call, add to list, add to sequence (per-row quick actions)

**Pagination:** 20 per page (configurable), page numbers 1-5+, "Go to" page input

### Selecting Leads

Click the **Select leads** dropdown button above results:
- **Select this page** — selects all leads on the current page
- **Select all (N)** — selects all matching leads across all pages (shows total like "Select all (1865)")
- **Select certain number** — enter a specific count in a text input, confirm with tick icon
- **Unselect all** — clears selection

**Estimates display:** Shows total like `"1,865 estimates"` next to the Select leads button.

Once leads are selected, the action bar buttons become active:
- **Add to Leads** — saves to CRM > Leads section (auto-enriches email)
- **Add to List** — opens dropdown to create a new list or add to existing list
- **Add to Sequence** — opens dropdown to add to an existing sequence or create new

### Workflow: Find Leads with Filters

1. Navigate to `https://sales.superagi.com/prospect/find_leads`
2. Ensure "Search with filters" mode is active (click the text if not)
3. `browser_snapshot` to see the filter panel
4. Click a filter name (e.g., "Job Title") to expand it — reveals the combobox/input
5. `browser_snapshot` to see the expanded filter input
6. Type into the combobox to search and select values
7. Repeat for additional filters — results update automatically
8. Use "Select leads" dropdown or individual checkboxes to select results
9. Click "Add to Leads", "Add to List", or "Add to Sequence"

### Workflow: Search with AI

1. Navigate to the Prospect Leads page
2. Click the text "Search with AI" (has an `image "AI Search"` icon next to it)
3. `browser_snapshot` to see the AI search input textbox
4. Type a natural language query in the textbox `"Describe the leads you're looking for..."`
5. Click the "Search with AI" button (it shows a loading state while searching)
6. Results appear with estimates — use Select leads and action buttons

### Workflow: Save and Reuse Searches

1. After setting filters: click **Save filters** → name the filter set
2. After an AI search: click **Save prompt** → saves the AI query
3. To reuse: click **Saved Search** tab → select a previously saved search

---

## 2. Prospect Companies (Find Companies)

**URL:** `https://sales.superagi.com/prospect/find_companies`
**Purpose:** Search for companies matching your ideal customer profile. Company lists can then feed back into lead prospecting — find companies first, then find people AT those companies.

### Page Layout

Same page structure as Find Leads but with:
- **"Find Companies" tab** is active
- **Add to List** (dropdown) — save companies to a list
- **Add to Companies** (button, disabled until selected) — save to CRM > Companies
- NO "Add to Sequence" button (sequences are for people, not companies)

### Company Filters

9 collapsible filters (left panel):

| Filter | Description |
|--------|-------------|
| **Company Name** | Search by company name |
| **Location** | Company location |
| **Industry** | Industry vertical |
| **Technologies** | Tech stack used |
| **Keywords** | Keywords in company description |
| **Revenue Range** | Company revenue range |
| **Company Size** | Employee count range |
| **Funding Stage** | Funding stage (Seed, Series A, etc.) |
| **Founded Year** | Year founded |

Same search modes: "Search with filters", "Search with AI", "Saved Search"

**Default state:** "Find your ideal companies" / "Enter details about your ideal companies. SuperAGI will find prospects that suit your criteria."

### Company → Lead Pipeline

This is a key workflow:
1. Use Prospect Companies to find companies matching your ICP
2. Save companies to a list
3. Go to Prospect Leads → expand the **Target Company Domains** filter
4. Click **Select a list** to load your saved company list
5. Now you're finding individual people AT those specific companies

---

## 3. Data Enrichment

**URL:** `https://sales.superagi.com/data_enrichments`
**Purpose:** Upload CSV files of people or companies to bulk-enrich their data (email, phone, company details, job title, etc.).

### Page Layout

- **Header:** "Data Enrichment"
- **Search:** textbox `"Search CSV"` — search through uploaded enrichments
- **Button:** "Enrich CSV" — starts the enrichment flow
- **Filters:** Type (dropdown), Created By (dropdown), Uploaded On (dropdown)

### Enrichment Table

Columns:
| Column | Description |
|--------|-------------|
| **Enrichment Name** | CSV file name |
| **Type** | "CSV - People" or "CSV - Company" |
| **Size** | Number of records in the file |
| **Enriched By** | User who ran the enrichment (avatar + name) |
| **Enriched On** | Date and time of enrichment |
| **Download** | Button to download the enriched CSV (disabled while processing) |

**Pagination:** 20 per page, shows total count (e.g., "1-20 of 124")

### Workflow: Enrich Data

1. Navigate to `https://sales.superagi.com/data_enrichments`
2. Click "Enrich CSV" button
3. Upload a CSV file (people or company data)
4. Map CSV columns to SuperAGI fields
5. Select which properties to enrich (email, phone, company details, etc.)
6. Run the enrichment
7. Download the enriched CSV when complete (Download button becomes active)

---

## 4. Signals

**URL:** `https://sales.superagi.com/signals`
**Purpose:** Track buying signals — real-time events that indicate a prospect or company might be ready to buy. Signals monitor news, job changes, funding, and more to help you prioritize outreach.

### Page Layout — Signals Stream Tab

The default view showing triggered signals:
- **Tabs:** "Signals Stream" (default) | "Manage Signals"
- **Search:** `"Search lead or company..."` textbox
- **Button:** "Create Signal"
- **Filters:** Last Activity (dropdown), Strength (dropdown), Type (dropdown), Signal (dropdown)

**Signal list items show:**
- Checkbox for selection
- Company avatar/logo
- Company name (e.g., "Morningstar", "Walmart", "KKR")
- Person name + title (when signal is person-level, e.g., "Nichole Teixeira · Sr Public Relations Manager")
- Signal name
- Strength indicator icon

**Right panel (click a signal to see details):**
- Company name + avatar + LinkedIn icon
- **"Go to company"** button — navigates to the company in CRM
- **Tabs:** Overview | Activity | Reasons to engage | Market Research
- **Company Info:** Company Size, Industry, Annual Revenue, Address, Description

### Page Layout — Manage Signals Tab

Table of all configured signals:

| Column | Description |
|--------|-------------|
| Created/Updated dates | When the signal was created and last modified |
| **Signal Name** | User-defined name (defaults to "Untitled Signal") |
| **Status** | Active (green dot) or Deprecated |
| **Signal Type** | The kind of event being tracked |
| More options | Per-row action menu |

**Pagination:** 20 per page (e.g., "1-20 of 58")

### Signal Types (Create Signal Wizard)

Clicking "Create Signal" opens a 3-step wizard:
1. **Signal Type** — select what to track
2. **Audience Filters** — define which companies/industries to monitor
3. **Distribute Leads** — configure where matched leads go

**Available signal types:**

| Signal Type | Description |
|-------------|-------------|
| **New Funding Announcement** | Track when companies announce new funding rounds or raise capital |
| **New Product Launch** | Track when companies launch new products or services |
| **Acquisition News** | Track when companies announce acquisitions or get acquired |
| **Awards & Recognitions** | Track when companies receive awards or industry recognition |
| **New Partnership Announcement** | Track when companies announce new partnerships or collaborations |
| **Layoffs** | Track when companies announce layoffs or workforce reductions |
| **Office Expansion** | Track when companies expand to new locations or open new offices |
| **Key Hire** | Track when companies make important leadership or executive hires |
| **Keywords mentioned in news** | Track when target keywords are getting news coverage |
| **Recent job changes** | Track when people change jobs (visible in existing signals, may be legacy) |

---

## 5. Anonymous Website Visitors

**URL:** `https://sales.superagi.com/website_visitors`
**Purpose:** Identify anonymous visitors to your website — shows which people and companies are browsing your site, so you can reach out while intent is high.

### Page Layout

- **Header:** "Anonymous Website Visitors" with Active/Inactive status indicator
- **Search:** `"Search visitors"` textbox
- **Button:** "Setup" — configure the tracking script/integration
- **Filters:** Last Activity (dropdown), Strength (dropdown), Pages URL (dropdown)

**Visitor list items show:**
- Checkbox for selection
- Avatar/initials
- Company name (e.g., "Creative Artists Agency", "KKR", "Accenture")
- Person name + title (e.g., "Natalie Pernas · Executive Assistant")
- "existing_lead" badge (if already in your CRM)
- Strength indicator

**Right panel (click a visitor to see details):**
- Person initials + name + LinkedIn icon
- Job title at Company
- **Actions:** Add to Sequence (dropdown), Email button, Call button
- **"Go to lead"** button — navigates to the lead in CRM
- **Tabs:** Overview | Activity | Reasons to engage | Market Research
- **Contact Info:** Work Email, Personal Email, Work Phone, Personal Phone, Address, Income Range
- **Company Info:** Company avatar + name + website, Company Size, Industry, Annual Revenue, Address, Description

---

## The Prospecting Pipeline

How prospecting connects to the rest of SuperAGI Sales:

```
1. FIND          → Prospect Leads (people) or Prospect Companies (orgs)
2. ENRICH        → Access Email/Phone on individual leads, or bulk via Data Enrichment CSV
3. SAVE          → Add to Leads (CRM), Add to List (for organization), or Add to Companies (CRM)
4. REACH OUT     → Add to Sequence (automated outreach) or Cold Outreach (one-off)
5. TRACK         → Signals alert you to buying intent; Website Visitors show who's browsing
6. MANAGE        → CRM Leads/Companies/Deals for pipeline management
```

**Key connections:**
- **Prospect Companies → Prospect Leads:** Find companies first, save to a list, then use that list in Prospect Leads' "Target Company Domains" > "Select a list" filter to find people at those companies
- **Prospect Leads → CRM:** "Add to Leads" moves prospects into CRM > Leads with auto email enrichment
- **Prospect Leads → Sequences:** "Add to Sequence" drops leads directly into automated outreach
- **Signals → Outreach prioritization:** Buying signals (funding, hiring, product launches) help you time outreach
- **Website Visitors → Immediate action:** See who's on your site and reach out via Email/Call/Sequence directly from the visitor detail panel

## Key Gotchas from the UI

1. **Filter expand/collapse:** Click the filter name text OR the toggle icon next to it — both work. The filter section collapses back to just the name when clicked again.
2. **Exclude toggles:** Most multi-select filters have an "Exclude" option below the combobox. This lets you exclude specific values (e.g., exclude the "Marketing" department).
3. **OR vs AND logic:** Technologies and Company Keywords filters have explicit "Include at least one (OR)" / "Include all (AND)" toggles. Default is OR.
4. **Target Company Domains extras:** This filter has three input methods — type domains manually, upload a CSV of domains, or select a saved list.
5. **AI Search vs Filter Search are separate modes:** They share the same results area but switching between them resets the other. You cannot combine AI search with manual filters.
6. **Access Email / Access Phone buttons:** These appear per-lead in results and cost enrichment credits. They reveal contact info inline without navigating away.
7. **"LEAD" badge on results:** Some prospect results show a "LEAD" badge and `lead_icon`, meaning this person is already in your CRM as a Lead.
8. **"existing_lead" badge on Website Visitors:** Similar indicator showing the visitor is already a CRM lead.
9. **Estimates count:** The total matching results number (e.g., "1,865 estimates") appears near the Select leads button — these are estimates, not exact counts.
10. **Funding Stage Date Range:** The Funding Stage filter has an additional "Date Range" sub-filter (defaults to "All Time") to scope by when the funding occurred.
11. **Company Find → No Sequences:** The Find Companies tab has "Add to Companies" but no "Add to Sequence" — sequences are for people, not companies.
12. **Signal wizard is 3 steps:** Signal Type → Audience Filters → Distribute Leads. You must complete all three to activate a signal.
13. **Data Enrichment types:** CSV uploads can be "CSV - People" or "CSV - Company" — you choose the type when uploading.
