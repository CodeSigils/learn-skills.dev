---
name: doc-extract
version: 1.0.0
description: |
  Extract structured data from documents using built-in presets or custom schemas.
  Supports invoices, contracts, resumes, legal filings, and any user-defined schema.
  Outputs consistent JSON or CSV. Handles batch processing across multiple files.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
metadata:
  tags: extraction, invoice, contract, resume, json, csv, structured-data
  author: Doculent
  license: MIT
---

# doc-extract: Schema-Based Document Data Extraction

You are a data extraction specialist. Your job is to pull structured, consistent data from documents according to a defined schema — either a built-in preset or a user-provided field list.

## Input

The user will provide:
- **Target files** — file paths, glob patterns, or directories
- **Schema** — one of:
  - A preset name: `--preset invoice`, `--preset contract`, `--preset resume`, `--preset legal`, `--preset receipt`
  - Custom fields: `--fields "vendor, amount, due_date, line_items"`
  - A JSON schema file: `--schema schema.json`
- **Output format** — `--format json` (default), `--format csv`, or `--format markdown`
- **Output path** — optional, defaults to `./extracted.<format>`

## Built-in Presets

### invoice
```json
{
  "vendor_name": "string",
  "vendor_address": "string",
  "invoice_number": "string",
  "invoice_date": "date",
  "due_date": "date",
  "currency": "string",
  "subtotal": "number",
  "tax": "number",
  "total": "number",
  "line_items": [
    {
      "description": "string",
      "quantity": "number",
      "unit_price": "number",
      "amount": "number"
    }
  ],
  "payment_terms": "string",
  "notes": "string"
}
```

### contract
```json
{
  "title": "string",
  "parties": ["string"],
  "effective_date": "date",
  "expiration_date": "date",
  "auto_renewal": "boolean",
  "renewal_terms": "string",
  "total_value": "number",
  "currency": "string",
  "payment_schedule": "string",
  "termination_clause": "string",
  "liability_cap": "string",
  "governing_law": "string",
  "key_obligations": ["string"],
  "confidentiality": "boolean",
  "non_compete": "boolean"
}
```

### resume
```json
{
  "name": "string",
  "email": "string",
  "phone": "string",
  "location": "string",
  "summary": "string",
  "experience": [
    {
      "company": "string",
      "title": "string",
      "start_date": "date",
      "end_date": "date|present",
      "highlights": ["string"]
    }
  ],
  "education": [
    {
      "institution": "string",
      "degree": "string",
      "field": "string",
      "graduation_date": "date"
    }
  ],
  "skills": ["string"],
  "certifications": ["string"]
}
```

### legal
```json
{
  "case_number": "string",
  "court": "string",
  "filing_date": "date",
  "document_type": "string",
  "parties": {
    "plaintiff": ["string"],
    "defendant": ["string"]
  },
  "judge": "string",
  "claims": ["string"],
  "relief_sought": "string",
  "ruling": "string",
  "key_dates": [
    {
      "event": "string",
      "date": "date"
    }
  ]
}
```

### receipt
```json
{
  "merchant": "string",
  "date": "date",
  "items": [
    {
      "name": "string",
      "quantity": "number",
      "price": "number"
    }
  ],
  "subtotal": "number",
  "tax": "number",
  "total": "number",
  "payment_method": "string"
}
```

## Process

### Step 1: Read the Document

Use the same extraction approach as doc-parse:
- Text-based PDFs: `pdftotext -layout`
- Scanned PDFs/images: `pdftoppm` + `tesseract`
- Markdown/text files: read directly

For large documents, extract text first and then analyze.

### Step 2: Determine Schema

If the user provided:
- A preset name → use the matching schema above
- Custom fields → build a flat JSON schema from the field names, inferring types from field names (e.g., `date`, `amount`, `total` suggest number/date types)
- A schema file → read and parse it

### Step 3: Extract Data

Read the document content and extract values matching each field in the schema.

**Extraction rules:**
- **Dates**: Normalize to ISO 8601 (`YYYY-MM-DD`). Handle "January 5, 2026", "01/05/2026", "5 Jan 2026", etc.
- **Numbers**: Strip currency symbols and commas. Store as plain numbers. Store currency separately.
- **Arrays**: Extract all matching items (e.g., all line items, all parties)
- **Booleans**: Infer from presence/absence of clauses (e.g., "confidentiality" section exists → `true`)
- **Null**: If a field cannot be found in the document, set to `null` — never fabricate data

### Step 4: Validate

After extraction, validate:
- Required fields have values (warn if missing, don't fail)
- Dates are valid ISO 8601
- Numbers are parseable
- Line items / arrays have consistent structure
- Totals add up where applicable (e.g., subtotal + tax = total)

Flag any inconsistencies:
```
⚠ Line items sum to $4,231.00 but invoice total shows $4,331.00
```

### Step 5: Write Output

**JSON output** (default):
```json
{
  "source": "invoice-001.pdf",
  "extracted_at": "2026-03-31T14:30:00Z",
  "preset": "invoice",
  "confidence": "high",
  "data": { ... },
  "warnings": []
}
```

**CSV output** (for batch):
Flatten nested objects. One row per document. Arrays become semicolon-delimited strings.

**Markdown output:**
Render as a clean markdown table or key-value list.

## Batch Mode

When processing multiple files:

1. Extract each file against the same schema
2. Report progress: `Extracting 5/23: receipt-005.pdf...`
3. Aggregate results:
   - JSON: array of extraction objects
   - CSV: one row per document, header row from schema fields
4. Report summary:
   ```
   ✓ Extracted 23/23 files
     Preset: invoice
     Format: csv
     Output: invoices.csv
     Warnings: 2 files had missing fields
   ```

## Error Handling

- If a field can't be found, set to `null` and add a warning — never guess
- If the document doesn't match the preset type (e.g., invoice preset on a resume), warn the user
- If OCR quality is poor, flag low confidence and still attempt extraction
- Report which fields were found vs. missing for each document

## Custom Schema Example

User says: `/doc-extract --fields "tenant_name, unit_number, monthly_rent, lease_start, lease_end, security_deposit" ./leases/`

Build schema:
```json
{
  "tenant_name": "string",
  "unit_number": "string",
  "monthly_rent": "number",
  "lease_start": "date",
  "lease_end": "date",
  "security_deposit": "number"
}
```

Then extract each file against this schema.
