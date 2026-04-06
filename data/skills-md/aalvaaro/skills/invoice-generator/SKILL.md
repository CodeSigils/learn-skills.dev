---
name: invoice-generator
description: "Generate professional invoices for freelancers and contractors. Creates a polished HTML invoice with live preview and download button, saved to /invoices. Stores contractor info (company name, address, phone) in a config file so it's only entered once. Asks for client name, email, line items, and optional payment terms each time. Auto-numbers invoices per client (saleshood_001, saleshood_002, etc.) and auto-dates to today. Supports multiple languages and currencies. The user can customize the HTML template to match their brand. Use this skill whenever the user mentions invoice, billing, bill a client, send an invoice, create an invoice, contractor invoice, freelance billing, or wants to generate any kind of invoice document — even if they just say something like 'I need to bill my client' or 'charge for last month's work'."
---

# Invoice Generator

Generate clean, professional invoices as self-contained HTML files with a live preview and a download-as-PDF button. Invoices are saved to a `/invoices` folder in the current working directory.

## How It Works

The skill uses two pieces:

1. **A config file** (`invoice-generator.local.md` in the project's `.claude/` directory) that stores your company/contractor info so you don't have to re-enter it every time.
2. **An HTML template** (`assets/invoice-template.html` bundled with this skill) that defines the look of the invoice. The user can swap this out or edit it to match their brand.

Each time the skill runs, it reads the config, asks for the per-invoice details (client, items, amounts), fills in the template, and writes the final HTML file. Invoice numbers are auto-generated per client.

---

## Step 0: Read the Config

Look for a config file at `.claude/invoice-generator.local.md` in the current project directory. This file uses YAML frontmatter to store the contractor's reusable info.

**If the file exists**, read it and extract the frontmatter fields. Confirm with the user: "I'll use your saved info — [Contractor Name], [Company Name]. Sound good?"

**If the file doesn't exist**, tell the user: "No config found yet — let me set up your info once so future invoices are instant."

Then collect each field using `AskUserQuestion`, batching up to 4 questions per call. Run three calls sequentially:

**Call 1** — locale & identity (4 questions):
1. `country` — "What country are you based in?" (header: "Country"). Options: "Mexico" (description: "MX — America/Mexico_City timezone"), "United States" (description: "US — America/New_York timezone"), "Spain" (description: "ES — Europe/Madrid timezone").
2. `language` — "What language should invoices be written in?" (header: "Language"). Options: "Español" (description: "All labels in Spanish"), "English" (description: "All labels in English"), "Português" (description: "All labels in Portuguese").
3. `company_name` — "What's your company or business name?" (header: "Company"). Options: examples like "Acme LLC", "Smith Consulting" — the user will pick Other and type their own.
4. `contractor_name` — "What's your full name (as the contractor/sender)?" (header: "Name"). Options: examples like "Jane Smith", "John Doe".

**Call 2** — address & contact (4 questions):
1. `street_address` — "What's your street address?" (header: "Address"). Options: examples like "123 Main St", "456 Oak Ave".
2. `city_state_zip` — "City, State and ZIP code?" (header: "City/ZIP"). Options: examples like "Austin, TX 78701", "Morelia, 58000, Michoacan, Mexico".
3. `phone` — "What's your phone number?" (header: "Phone"). Options: examples like "+1 512-555-0100", "+52 443-555-0100".
4. `email` — "What's your email address?" (header: "Email"). Options: examples like "you@company.com", "name@gmail.com".

**Call 3** — optional fields (2 questions):
1. `fax` — "Do you have a fax number?" (header: "Fax"). Options: "No fax" (description: "Skip this field"), "Yes, I have a fax number" (description: "I'll type it in").
2. `default_currency` — "Which currency do you use?" (header: "Currency"). Options: "$ MXN" (description: "Mexican Peso"), "$ USD" (description: "US Dollar"), "€ EUR" (description: "Euro"), "£ GBP" (description: "British Pound").

After collecting all answers, confirm the info back to the user in a summary and create the file:

```markdown
---
company_name: "Acme Consulting LLC"
contractor_name: "Jane Smith"
street_address: "123 Main St"
city_state_zip: "Austin, TX 78701"
phone: "+1 512-555-0100"
fax: ""
email: "jane@acmeconsulting.com"
default_currency: "$ MXN"
country: "Mexico"
language: "Español"
---

# Invoice Generator Config

This file stores your contractor/company info for invoice generation.
Edit the YAML fields above to update your details.
```

### Timezone from Country

Use the country to determine the timezone for date formatting:
- Mexico → `America/Mexico_City`
- United States → `America/New_York` (can be overridden)
- Spain → `Europe/Madrid`
- Other → ask or use system timezone

### Language Labels

Based on the `language` field, translate all template labels. Here's the mapping:

| Placeholder | English | Español | Português |
|---|---|---|---|
| `{{l_invoice}}` | INVOICE | FACTURA | FATURA |
| `{{l_date}}` | DATE | FECHA | DATA |
| `{{l_from}}` | FROM | DE | DE |
| `{{l_bill_to}}` | BILL TO | FACTURAR A | COBRAR DE |
| `{{l_qty}}` | QTY | CANT | QTD |
| `{{l_description}}` | Description | Descripción | Descrição |
| `{{l_unit_price}}` | Unit Price | Precio Unitario | Preço Unitário |
| `{{l_total}}` | Total | Total | Total |
| `{{l_subtotal}}` | SUBTOTAL | SUBTOTAL | SUBTOTAL |
| `{{l_total_due}}` | TOTAL DUE | TOTAL A PAGAR | TOTAL A PAGAR |
| `{{l_payment_details}}` | PAYMENT DETAILS | DETALLES DE PAGO | DETALHES DE PAGAMENTO |
| `{{l_notes}}` | NOTES | NOTAS | NOTAS |
| `{{l_thank_you}}` | THANK YOU FOR YOUR BUSINESS! | ¡GRACIAS POR SU PREFERENCIA! | OBRIGADO PELA PREFERÊNCIA! |
| `{{l_download}}` | Download as PDF | Descargar como PDF | Baixar como PDF |
| `{{lang_code}}` | en | es | pt |

Also format the invoice date according to the language:
- English: `March 27, 2026`
- Español: `27 de marzo de 2026`
- Português: `27 de março de 2026`

## Step 1: Gather Invoice Details

Collect invoice details using `AskUserQuestion`. If the user already provided some info in their initial message (e.g., "invoice for Acme Corp, 10 hours at $150"), skip those fields and only ask about what's missing.

**Call 1** — client info (3 questions):
1. "Who is this invoice for? (client name)" (header: "Client"). Options: examples like "Acme Corp", "Smith Industries".
2. "What's the client's address?" (header: "Address"). Options: examples like "123 Main St, City, ST 10001", "456 Oak Ave, Suite 200, City, ST 90210". If the user provides a multi-line address, split into street + city/state/zip lines.
3. "What's the client's email address?" (header: "Email"). Options: examples like "client@company.com", "billing@acme.com".

**Call 2** — line items & terms (3 questions):
1. "What are the line items? List each with quantity, description, and unit price." (header: "Items"). Options: examples like "10 hrs × Consulting @ $150", "1 × Website Design @ $2,000" — the user will type their actual items via Other.
2. "Any payment terms to include?" (header: "Terms"). Options: "Wire Transfer" (description: "Payment via wire / bank deposit"), "Due on receipt" (description: "Payment due immediately"), "Net 30" (description: "Payment due within 30 days"), "Custom terms" (description: "I'll specify my own terms or bank details").
3. "Any notes to add?" (header: "Notes"). Options: "No notes" (description: "Skip this section"), "Add notes" (description: "I'll type my notes — e.g., project description, thank you message").

If the user gives partial info upfront, fill in what you can and only ask about what's missing — skip questions you already have answers for.

### Auto-Numbering

The invoice number and date are **not** asked — they are generated automatically:

1. **Invoice date**: Use today's date in the user's timezone (from config `country`), formatted according to the `language` setting.
2. **Invoice number**: Derived from the client name and a sequential counter:
   - Slugify the client name: lowercase, replace spaces/special chars with hyphens (e.g., "SalesHood" → `saleshood`, "Acme Corp" → `acme-corp`)
   - List files in `invoices/` matching the pattern `{slug}_NNN.html` (e.g., `saleshood_001.html`, `saleshood_002.html`)
   - If no files exist for this client, use `001`
   - Otherwise, take the highest number and add 1, zero-padded to 3 digits
   - The invoice number displayed on the invoice is just the numeric part: `001`, `002`, etc. (or whatever format the user prefers — if they have existing invoices with a different format like `100`, `101`, continue that sequence)

## Step 2: Build the Invoice

1. Read the HTML template from `assets/invoice-template.html` (bundled with this skill).
2. Replace all the placeholders with the actual data:
   - Contractor/company info from the config
   - Client info and line items from Step 1
   - Calculate each line total (quantity × unit price)
   - Calculate the subtotal and total due
   - Fill in the auto-generated invoice number and date
   - Fill in all language label placeholders from the table above
3. The template has these placeholders — replace them all:
   - **Labels**: `{{l_invoice}}`, `{{l_date}}`, `{{l_from}}`, `{{l_bill_to}}`, `{{l_qty}}`, `{{l_description}}`, `{{l_unit_price}}`, `{{l_total}}`, `{{l_subtotal}}`, `{{l_total_due}}`, `{{l_payment_details}}`, `{{l_notes}}`, `{{l_thank_you}}`, `{{l_download}}`, `{{lang_code}}`
   - **Contractor**: `{{contractor_name}}`, `{{street_address}}`, `{{city_state_zip}}`, `{{phone}}`, `{{email}}`
   - `{{fax_line}}` — if fax is provided, render as `<br>Fax: {{fax}}`; if not, replace with empty string
   - **Client**: `{{client_name}}`, `{{client_email}}`
   - `{{client_address}}` — client's address lines (street, city/state/zip), each on its own line with `<br>`. If no address provided, leave empty.
   - **Invoice**: `{{invoice_number}}`, `{{invoice_date}}`
   - `{{line_items}}` — generate a `<tr>` for each item with `<td>` cells for qty, description, unit price, total
   - `{{subtotal}}`, `{{total_due}}`
   - `{{payment_terms_section}}` — if provided, render as: `<div class="section"><h3>{{l_payment_details}}</h3><p>...</p></div>`; if not, replace with empty string
   - `{{notes_section}}` — if notes provided, render as: `<div class="section"><h3>{{l_notes}}</h3><p>...</p></div>`; if not, replace with empty string
   - `{{currency}}` — the currency symbol + code from config (e.g., `$49,000.00 MXN`)

Format all money amounts with two decimal places, the currency symbol, and the currency code.

## Step 3: Save and Present

1. Create the `/invoices` directory in the current working directory if it doesn't exist.
2. Save the invoice using the auto-numbering scheme: `invoices/{client_slug}_{NNN}.html`
   - Example: `invoices/saleshood_001.html`, `invoices/acme-corp_003.html`
3. Tell the user where the file was saved and open it in the browser:
   ```bash
   open invoices/{client_slug}_{NNN}.html
   ```

The HTML file is fully self-contained (inline CSS, no external dependencies) and includes:
- A **print/download button** that triggers the browser's print dialog (which allows saving as PDF)
- The button is hidden when printing so it doesn't appear in the PDF

## Customizing the Template

If the user wants to change how invoices look, they can:

1. **Ask you to modify the template** — e.g., "add my logo", "change the colors to blue", "add a notes section". Read the current template, make the changes, and save it back.
2. **Edit it directly** — the template is at `assets/invoice-template.html` within the skill directory. It's standard HTML/CSS with `{{placeholder}}` markers.

When modifying the template, preserve all `{{placeholder}}` markers or update the skill logic to match any changes.
