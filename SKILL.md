---
name: resume-builder
description: 'Build, edit, and format professional resumes with PDF import, styled HTML/PDF export, and multi-language support. Use this skill whenever a user mentions resumes, CVs, or curriculum vitae — whether they want to create one from scratch, import and edit an existing PDF resume, add or update sections (education, experience, projects, skills), export to a styled HTML or PDF document, generate multi-language versions, or apply professional formatting. Also triggers for requests like "help me update my CV", "format my resume", "translate my resume to Chinese", or "I need a professional-looking resume".'
---

# Resume Builder

## Overview

Build professional resumes with AI-assisted content management, supporting PDF import/export, HTML styling, and multi-language output.

**Resume data structure and JSON schema**: See `references/data-structure.md`
**Troubleshooting**: See `references/troubleshooting.md`
**Customization (themes, languages)**: See `references/customization.md`

## Dependencies

- **HTML generation**: Python 3 (no extra deps)
- **PDF import**: `pip install pymupdf`
- **PDF export** (either one): `pip install pdfkit && brew install wkhtmltopdf` OR `pip install playwright && playwright install chromium`

## Work File Convention

Save resume JSON to `resume.json` in the current working directory unless the user specifies another path. When importing from PDF, save the extracted JSON alongside the source file.

## Workflow

### 1. Initial Import (if user provides existing PDF)

The `scripts/extract_from_pdf.py` script does basic text extraction, but it produces rough output. For best results, use your AI capabilities to read and understand the PDF content directly, then structure it into the resume JSON schema yourself. The script is available as a fallback:

```bash
python3 "$SKILL_DIR/scripts/extract_from_pdf.py" input.pdf output.json
```

After extraction (by any method), present the structured data to the user for review and ask if they want any modifications.

### 2. Content Management

When adding or editing sections, gather complete information through natural conversation. The key areas to ask about:

**For Education:** institution, degree, period, location, GPA (if applicable), honors.
**For Work Experience:** company, position, period, location, responsibilities, quantifiable achievements.
**For Projects:** name, role, period, technologies, description, key achievements.

Keep asking follow-up questions if responses are brief or unclear. The goal is a complete, well-structured entry — not a minimal one.

**Important separation principle:**
- **Work Experience** should stay high-level: job responsibilities at a business level, scope (team size, industry sectors), leadership and business impact.
- **Projects** should go deep on technical specifics: technologies, architecture, quantified achievements with metrics.

This separation makes the resume scannable for HR while providing depth for engineering interviews.

### 3. Export

1. Confirm format (HTML or PDF), theme, and language with the user.
2. Generate HTML:
   ```bash
   python3 "$SKILL_DIR/scripts/generate_html.py" --theme modern --lang en resume.json output.html
   ```
3. If PDF, also run:
   ```bash
   python3 "$SKILL_DIR/scripts/generate_pdf.py" output.html output.pdf
   ```

**Available themes:** `modern`, `classic`, `minimal`, `creative`
**Available languages:** `en`, `zh`, `ja`, `fr`, `de`, `es`

### 4. Interactive Edit Mode (Edit-Review-Export)

For collaborative refinement with the user, generate an editable HTML that includes inline editing capabilities:

```bash
python3 "$SKILL_DIR/scripts/generate_html.py" --theme modern --lang en --editable resume.json output.html
```

**Workflow:**

1. Generate the editable HTML and tell the user to open it in a browser.
2. Guide the user: "Hover over the top-right corner to reveal the edit button (pencil icon), click it to enter edit mode. You can directly modify any text in the resume."
3. The user edits content in-browser — all text fields, list items (add/remove with +/- buttons), and skill lists are editable.
4. When done, the user clicks "Copy JSON" in the toolbar to copy the updated resume JSON to clipboard.
5. The user pastes the JSON back to you (or if you have Playwright access, you can extract it directly from the page).
6. **Final review**: Check the updated content for grammar, spelling, consistency, and formatting. Suggest corrections if needed.
7. Apply any corrections to `resume.json`.
8. Generate the final, non-editable version for export (HTML or PDF) using the standard export command (without `--editable`).

**Notes:**
- Edit UI is hidden during print/PDF export, so the visual output is unaffected.
- The toolbar provides "Copy JSON" (copies to clipboard) with a fallback to browser console.
- If you have Playwright access, you can evaluate `JSON.stringify(window.extractToJson ? extractToJson() : 'N/A')` to read edits programmatically.

## Content Best Practices

- **Quantify achievements**: Include numbers and metrics (e.g., "Improved efficiency by 30%")
- **Action verbs**: Use strong action verbs (e.g., "Led", "Architected", "Built")
- **Consistency**: Maintain consistent formatting and tense across entries
- **Proofread**: Review for typos and grammatical errors before export

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/extract_from_pdf.py` | Extract text from PDF resumes (fallback — prefer AI-based parsing) |
| `scripts/generate_html.py` | Generate styled HTML from resume JSON |
| `scripts/generate_pdf.py` | Convert HTML resume to PDF |
