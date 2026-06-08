# Resume Editor

AI-powered resume builder that runs locally. Import from PDF, edit interactively, export to styled HTML and PDF — in 6 languages, 4 themes.

**Works with:** [OpenClaw](https://github.com/openclaw/openclaw) · Claude Code · OpenAI Codex

## Features

- 📄 **PDF Import** — Extract structured data from existing resumes
- ✏️ **AI Editing** — Add/update sections through natural conversation
- 🎨 **4 Themes** — Modern, Classic, Minimal, Creative
- 🌍 **6 Languages** — English, 中文, 日本語, Français, Deutsch, Español
- 📑 **Dual Export** — Styled HTML + print-ready PDF (A4)
- 🔒 **Local-first** — Everything runs locally, no data leaves your machine

## Installation

### OpenClaw

Clone into your workspace skills directory:

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/chijiang/resume-editor.git resume-builder
```

The skill is auto-detected on next session.

### Claude Code

Clone into your project's `.claudeskills` directory:

```bash
mkdir -p .claudeskills
cd .claudeskills
git clone https://github.com/chijiang/resume-editor.git resume-builder
```

Reference in `CLAUDE.md`:

```markdown
## Skills
- Resume Builder: See `.claudeskills/resume-builder/SKILL.md`
```

### OpenAI Codex

Clone into your project's instructions directory:

```bash
mkdir -p .codex/instructions
cd .codex/instructions
git clone https://github.com/chijiang/resume-editor.git resume-builder
```

Reference in `AGENTS.md`:

```markdown
## Skills
- Resume Builder: See `.codex/instructions/resume-builder/SKILL.md`
```

## Quick Start

### Prerequisites

```bash
# Required: Python 3.7+
python3 --version

# Optional: PDF import
pip install pymupdf

# Optional: PDF export (choose one)
pip install pdfkit && brew install wkhtmltopdf          # wkhtmltopdf
pip install playwright && playwright install chromium    # Playwright
```

### Generate Resume

```bash
# 1. Start from example
cp references/example-resume.json my-resume.json

# 2. Edit with your info, then generate HTML
python3 scripts/generate_html.py --theme modern --lang en my-resume.json output.html

# 3. Convert to PDF
python3 scripts/generate_pdf.py output.html output.pdf
```

### Import from PDF

```bash
python3 scripts/extract_from_pdf.py existing-resume.pdf extracted.json
```

## Themes

| Theme | Style | Preview |
|-------|-------|---------|
| `modern` | Clean, contemporary | Default |
| `classic` | Traditional, formal | — |
| `minimal` | Content-focused | — |
| `creative` | Bold, creative | — |

## Languages

| Code | Language |
|------|----------|
| `en` | English |
| `zh` | 中文 |
| `ja` | 日本語 |
| `fr` | Français |
| `de` | Deutsch |
| `es` | Español |

## Resume Data Schema

```json
{
  "personal": {
    "name": "Your Name",
    "email": "you@example.com",
    "phone": "+86 138-0000-0000",
    "location": "City, Country",
    "linkedin": "https://linkedin.com/in/yourprofile",
    "github": "https://github.com/yourusername"
  },
  "summary": "A brief professional summary...",
  "education": [
    {
      "institution": "University Name",
      "degree": "Bachelor of Science in Computer Science",
      "period": "2016-2020",
      "location": "City",
      "gpa": "3.8/4.0",
      "honors": ["Dean's List", "Scholarship"]
    }
  ],
  "experience": [
    {
      "company": "Company Name",
      "position": "Job Title",
      "period": "2020-Present",
      "location": "City",
      "description": "High-level role description — scope, leadership, business impact.",
      "responsibilities": ["Responsibility 1", "Responsibility 2"],
      "achievements": ["Achievement with measurable result"]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "role": "Lead Developer",
      "period": "2023",
      "technologies": ["Python", "React", "AWS"],
      "description": "What the project does and your contribution.",
      "achievements": ["Key result with metrics"]
    }
  ],
  "skills": {
    "programming": ["Python", "JavaScript", "Go"],
    "frameworks": ["React", "Django"],
    "tools": ["Git", "Docker", "Kubernetes"],
    "languages": ["Chinese (Native)", "English (Fluent)"]
  }
}
```

> Only `personal.name` is required. All other fields are optional.

## Example

A complete example is in [`references/example-resume.json`](references/example-resume.json). Try it:

```bash
python3 scripts/generate_html.py \
  --theme modern --lang en \
  references/example-resume.json \
  example-output.html
```

Open `example-output.html` in a browser to preview.

## Project Structure

```
resume-editor/
├── SKILL.md                  # Skill definition for AI agents
├── plugin.json               # Plugin metadata
├── README.md                 # This file
├── references/
│   └── example-resume.json   # Example resume (fictional data)
├── scripts/
│   ├── extract_from_pdf.py   # PDF → JSON
│   ├── generate_html.py      # JSON → HTML (multi-theme, multi-language)
│   └── generate_pdf.py       # HTML → PDF
├── assets/
│   ├── css/                  # Theme stylesheets
│   │   ├── modern.css
│   │   ├── classic.css
│   │   ├── minimal.css
│   │   └── creative.css
│   └── templates/            # HTML templates
│       ├── modern.html
│       ├── classic.html
│       ├── minimal.html
│       └── creative.html
└── commands/
    └── resume-export.md      # Slash command definition
```

## Best Practices

- **Work Experience** → High-level: role scope, team size, business impact, leadership
- **Projects** → Technical depth: tools, architecture, quantified achievements
- **Quantify** — "Improved efficiency by 30%" > "Improved efficiency"
- **Action verbs** — Led, Architected, Built, Designed, Optimized
- **Proofread** — Typos kill first impressions

## License

MIT

---

<p align="center">
  <sub>Built for <a href="https://github.com/openclaw/openclaw">OpenClaw</a> · Compatible with Claude Code & Codex</sub>
</p>
