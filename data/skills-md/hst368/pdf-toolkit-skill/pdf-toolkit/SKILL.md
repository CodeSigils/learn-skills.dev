---
name: "pdf-toolkit"
description: "Operate on PDF files: compress PDFs, render pages to images, extract text, extract embedded images, OCR scanned PDFs, and merge/split/extract/delete pages. Use when the user asks for PDF compression, PDF to image, text extraction, image extraction, OCR, or PDF page operations."
---

# PDF Toolkit

Use this skill for PDFs that already exist. For CAJ-to-PDF conversion, use the separate `caj-pdf` skill first.

## Route requests
- Compress or reduce file size: `scripts/pdf_compress.sh`
- Convert pages to PNG/JPG previews or long-image inputs: `scripts/pdf_render.sh`
- Extract text or make a `.txt`: `scripts/pdf_text.sh`
- Extract embedded images: `scripts/pdf_images.sh`
- OCR a scanned PDF: `scripts/pdf_ocr.sh`
- Merge, split, extract, or delete pages: `scripts/pdf_pages.sh`

## General rules
1. Confirm input files exist before running scripts.
2. Prefer default outputs beside the input file unless the user gives an output path.
3. Do not overwrite existing outputs unless the user explicitly asks; scripts create timestamped outputs by default.
4. Validate resulting PDFs with `pdfinfo` when available.
5. Report the final output path and the key validation result: page count, file size, or generated file count.

## Quick commands
```bash
scripts/pdf_compress.sh input.pdf
scripts/pdf_render.sh input.pdf --format png --dpi 180
scripts/pdf_text.sh input.pdf --layout
scripts/pdf_images.sh input.pdf
scripts/pdf_ocr.sh input.pdf
scripts/pdf_pages.sh extract input.pdf 1-5
scripts/pdf_pages.sh merge output.pdf a.pdf b.pdf
scripts/install_deps.sh --check
```

## Dependencies
- Compression: `gs`
- Rendering: `pdftoppm`
- Text extraction: `pdftotext`
- Image extraction: `pdfimages`
- OCR: `ocrmypdf` preferred; fallback uses `pdftoppm`, `tesseract`, and `qpdf` or `mutool`
- Page operations: `qpdf` preferred; fallback uses `mutool` for common operations

If a required dependency is missing:
1. Run `scripts/install_deps.sh --check`.
2. Show the user the missing commands and suggested package-manager command.
3. Only run `scripts/install_deps.sh --install` after the user asks to install dependencies.
4. Do not improvise with fragile parsing.

`install_deps.sh` supports Homebrew on macOS and `apt-get` on Debian/Ubuntu. On other systems, it prints the missing command names for manual installation.
