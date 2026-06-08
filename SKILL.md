---
name: resume-builder
description: 'Build, edit, and format professional resumes with support for PDF import, HTML/PDF export, multi-language output, and style customization. Use when users need to: (1) Create a new resume from scratch, (2) Import and modify an existing PDF resume, (3) Add/update education, work experience, or projects, (4) Export to styled HTML or PDF formats, (5) Generate multi-language versions of the resume, or (6) Apply professional styling and formatting to resume content.'
---

# Resume Builder

## Overview

Build professional resumes with AI-assisted content management, supporting PDF import/export, HTML styling, and multi-language output.

## Core Capabilities

### 1. PDF Resume Import
- Accept user-uploaded PDF resumes
- Extract and parse resume content using PDF analysis tools
- Structure extracted data into editable format (education, experience, projects, skills)

### 2. Interactive Content Editing
- Guide users through adding new sections (education, work experience, projects)
- Ask targeted questions to gather complete information
- Ensure consistency and completeness of resume entries
- Modify existing resume content based on user requests

### 3. Resume Data Structure

Maintain resume data in structured JSON format:

```json
{
  "personal": {
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "+86 138-0000-0000",
    "location": "City, Country",
    "linkedin": "https://linkedin.com/in/...",
    "github": "https://github.com/...",
    "languages": ["English", "Chinese", "French"]
  },
  "summary": "Professional summary...",
  "education": [
    {
      "institution": "University Name",
      "degree": "Bachelor/Master/PhD in Field",
      "period": "2020-2024",
      "location": "City, Country",
      "gpa": "3.8/4.0",
      "honors": ["Dean's List", "Scholarship"]
    }
  ],
  "experience": [
    {
      "company": "Company Name",
      "position": "Job Title",
      "period": "2022-Present",
      "location": "City, Country",
      "description": "High-level description of role, responsibilities, scope, and business impact. Focus on what you did at a macro level (team size, client base, industry sectors)."
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "role": "Role (e.g., Lead Developer)",
      "period": "2023",
      "technologies": ["Python", "React", "AWS"],
      "description": "Brief overview...",
      "achievements": [
        "Launched product with 10k+ users"
      ]
    }
  ],
  "skills": {
    "programming": ["Python", "JavaScript", "Go"],
    "frameworks": ["React", "Django", "Spring Boot"],
    "tools": ["Git", "Docker", "Kubernetes"],
    "languages": ["Chinese (Native)", "English (Fluent)"]
  }
}
```

### 4. Information Gathering Workflow

When adding new sections, follow this questioning pattern:

**For Education:**
- Institution name
- Degree type and field of study
- Start and end dates (graduation year)
- Location
- GPA (if applicable)
- Honors, awards, or relevant coursework

**For Work Experience:**
- Company name
- Position/title
- Start and end dates
- Location
- Responsibilities and daily tasks
- Quantifiable achievements and impacts
- Tools/technologies used

**For Projects:**
- Project name
- Your role and team size (if applicable)
- Time period
- Technologies used
- Project description and purpose
- Key achievements or outcomes
- Links (GitHub, demo site, etc.)

**Continue asking questions until information is complete.** Ask follow-ups if responses are brief or unclear.

### 5. HTML Export with Styling

Generate professionally styled HTML resumes using templates in `assets/templates/`. Support multiple style themes.

**Available themes:**
- `modern`: Clean, contemporary design
- `classic`: Traditional, formal layout
- `minimal`: Minimalist, content-focused
- `creative`: Bold colors and creative layout

**Usage:**
```
python3 scripts/generate_html.py --theme modern --lang en resume.json resume.html
```

### 6. PDF Export

Convert HTML resumes to PDF using browser-based rendering or command-line tools.

**Usage:**
```
python3 scripts/generate_pdf.py resume.html resume.pdf
```

### 7. Multi-Language Support

Generate resumes in multiple languages with proper translations:

```
python3 scripts/generate_html.py --theme modern --lang zh resume.json resume_zh.html
```

**Supported languages:**
- English (`en`)
- Chinese (`zh`)
- Japanese (`ja`)
- French (`fr`)
- German (`de`)
- Spanish (`es`)

## Workflow

### Initial Import (if user provides existing PDF)

1. Accept PDF upload from user
2. Use PDF analysis to extract content
3. Structure data into JSON format
4. Present structured data to user for review
5. Ask for any initial modifications or clarifications

### Content Management

1. Identify which section to modify (education, experience, projects, skills)
2. For additions: Follow information gathering workflow
3. For modifications: Present current content, accept edits
4. Update JSON resume data structure

### Export

1. Confirm export format (HTML or PDF)
2. If HTML: Select theme and language
3. Generate output using appropriate scripts
4. Present result to user

## Scripts

### `scripts/extract_from_pdf.py`
Extracts text and structure from uploaded PDF resumes.

**Usage:**
```bash
python3 scripts/extract_from_pdf.py input.pdf output.json
```

### `scripts/generate_html.py`
Generates styled HTML from resume JSON data.

**Usage:**
```bash
python3 scripts/generate_html.py --theme modern --lang en resume.json output.html
```

### `scripts/generate_pdf.py`
Converts HTML resume to PDF format.

**Usage:**
```bash
python3 scripts/generate_pdf.py resume.html output.pdf
```

## Templates

HTML templates are located in `assets/templates/`:

- `modern.html`: Modern, clean design
- `classic.html`: Traditional professional layout
- `minimal.html`: Minimalist, content-focused
- `creative.html`: Bold, creative design

CSS styles are in `assets/css/`:
- `modern.css`
- `classic.css`
- `minimal.css`
- `creative.css`

## Best Practices

### Resume Structure Best Practices

**Separate Work Experience from Projects:**
- **Work Experience**: Keep it high-level and macro. Focus on:
  - Job responsibilities at a business level (not technical details)
  - Scope and scale (team size, client base, industry sectors)
  - Leadership and business impact
  - Example: "Led AI platform development for enterprise clients, managing teams of data scientists and engineers to deliver end-to-end solutions across supply chain, life sciences, and manufacturing sectors."

- **Projects**: Include detailed technical specifics and achievements. Focus on:
  - Specific technologies and tools used
  - Technical architecture and implementation details
  - Quantified achievements with metrics
  - Example: "Reduced agent hallucination rate from 37% to 0% on production test datasets using LangGraph, MCP, and custom gRPC communication pipelines."

**Why This Separation Matters:**
- **Readability**: HR can quickly scan work experience for relevant roles
- **Detail Depth**: Projects section provides technical depth for engineering interviews
- **Scannability**: Clear separation makes the resume easier to navigate
- **Flexibility**: Work experience stays concise while projects showcase technical depth

### Content Best Practices

1. **Quantify achievements**: Always include numbers and metrics (e.g., "Improved efficiency by 30%")
2. **Action verbs**: Use strong action verbs for responsibilities and achievements (e.g., "Led", "Architected", "Built")
3. **Consistency**: Maintain consistent formatting and tense across entries
4. **Relevance**: Tailor content to target job/industry when possible
5. **Proofreading**: Review for typos and grammatical errors before export

## Quality Standards

- Ensure all dates are in consistent format (YYYY or YYYY-YYYY)
- Verify contact information is complete and accurate
- Check for gaps or inconsistencies in timeline
- Confirm technical skills are properly categorized
- Test HTML rendering in multiple browsers
- Validate PDF export quality and formatting

## Troubleshooting

### Common Issues

**PDF extraction fails or produces poor results:**
- **Cause**: PDF is scanned images (not text-based) or has complex formatting
- **Solutions**:
  - Ensure PDF is text-based, not scanned images
  - Try OCR tools for scanned documents (e.g., `tesseract`)
  - Manually edit the extracted JSON data to fix issues
  - Check that the PDF uses standard fonts and encoding

**HTML generation fails:**
- **Cause**: Invalid JSON format, missing required fields, or corrupted file
- **Solutions**:
  - Validate JSON structure using a JSON validator
  - Ensure `personal.name` field exists
  - Verify file is UTF-8 encoded
  - Check error messages for specific field names

**PDF export fails:**
- **Cause**: PDF generation tools not installed
- **Solutions**:
  - Install pdfkit: `pip install pdfkit` and `brew install wkhtmltopdf`
  - Or install Playwright: `pip install playwright && playwright install chromium`
  - Verify installation by running the tool's test command

**Theme or CSS not found:**
- **Cause**: Theme files are missing from assets directory
- **Solutions**:
  - Check that theme HTML exists in `assets/templates/`
  - Verify CSS exists in `assets/css/`
  - Use `--theme modern` as fallback
  - Reinstall the skill if files are missing

**Invalid email format error:**
- **Cause**: Email address doesn't follow standard format
- **Solutions**:
  - Ensure email follows format: `user@domain.com`
  - Remove special characters or spaces
  - Use a valid email address or leave empty

**Mobile display issues:**
- **Cause**: CSS not optimized for small screens
- **Solutions**:
  - All themes now include mobile-responsive CSS
  - View on a mobile device or resize browser window
  - If issues persist, report them for theme improvement

## Customization

### Adding New Themes

To create a custom resume theme:

1. **Create HTML template** in `assets/templates/your-theme.html`:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Resume</title>
       <style>
           {{CSS}}
       </style>
   </head>
   <body>
       <div class="resume-container">
           {{CONTENT}}
       </div>
   </body>
   </html>
   ```

2. **Create CSS file** in `assets/css/your-theme.css`:
   ```css
   /* Your Custom Theme */
   * {
       margin: 0;
       padding: 0;
       box-sizing: border-box;
   }

   body {
       font-family: 'Your Font', sans-serif;
       /* ... more styles ... */
   }
   ```

3. **Add theme name** to `scripts/generate_html.py`:
   ```python
   parser.add_argument('--theme', default='modern',
                       choices=['modern', 'classic', 'minimal', 'creative', 'your-theme'],
                       help='Resume theme (default: modern)')
   ```

### Adding New Languages

To add support for a new language:

1. **Add language code** to `scripts/generate_html.py`:
   ```python
   parser.add_argument('--lang', default='en',
                       choices=['en', 'zh', 'ja', 'fr', 'de', 'es', 'your-lang'],
                       help='Language (default: en)')
   ```

2. **Add translations** to `SECTION_TITLES` dictionary:
   ```python
   SECTION_TITLES = {
       "en": {
           "summary": "Professional Summary",
           "experience": "Work Experience",
           # ...
       },
       "your-lang": {
           "summary": "Your Language Translation",
           "experience": "Work Experience in Your Language",
           # ...
       }
   }
   ```

3. **Test the new language** by generating a resume:
   ```bash
   python3 scripts/generate_html.py --theme modern --lang your-lang resume.json output.html
   ```

### Modifying Resume Data Structure

To add custom fields to the resume structure:

1. **Update the JSON schema** in your resume data file
2. **Add HTML generation logic** in `scripts/generate_html.py`:
   ```python
   def build_custom_section(custom_data, language):
       """Build custom section."""
       title = "Custom Section"  # or use SECTION_TITLES
       html = f'<section class="resume-section"><h2 class="section-title">{title}</h2>'
       
       for item in custom_data:
           html += f"<div class='custom-item'>{escape_text(item)}</div>"
       
       html += "</section>"
       return html
   ```

3. **Add CSS styles** for the custom section in your theme's CSS file

### Exporting to Other Formats

**Markdown Export:**
Convert HTML to Markdown using tools like `pandoc`:
```bash
pandoc resume.html -o resume.md
```

**Word Export:**
Convert HTML to DOCX using `pandoc`:
```bash
pandoc resume.html -o resume.docx
```

**Plain Text Export:**
Use `lynx` or `html2text`:
```bash
html2text resume.html > resume.txt
```
