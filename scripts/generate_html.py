#!/usr/bin/env python3
"""
Generate styled HTML resume from JSON data.
Supports multiple themes and languages.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
import html as html_escape

# Section titles in multiple languages
SECTION_TITLES = {
    "en": {
        "summary": "Professional Summary",
        "experience": "Work Experience",
        "education": "Education",
        "projects": "Projects",
        "skills": "Skills"
    },
    "zh": {
        "summary": "个人简介",
        "experience": "工作经历",
        "education": "教育背景",
        "projects": "项目经历",
        "skills": "技能"
    },
    "ja": {
        "summary": "プロフィール",
        "experience": "職歴",
        "education": "学歴",
        "projects": "プロジェクト",
        "skills": "スキル"
    },
    "fr": {
        "summary": "Profil Professionnel",
        "experience": "Expérience Professionnelle",
        "education": "Formation",
        "projects": "Projets",
        "skills": "Compétences"
    },
    "de": {
        "summary": "Zusammenfassung",
        "experience": "Berufserfahrung",
        "education": "Ausbildung",
        "projects": "Projekte",
        "skills": "Fähigkeiten"
    },
    "es": {
        "summary": "Resumen Profesional",
        "experience": "Experiencia Laboral",
        "education": "Educación",
        "projects": "Proyectos",
        "skills": "Habilidades"
    }
}


def escape_text(text):
    """Escape HTML special characters to prevent injection."""
    if text is None:
        return ""
    return html_escape.escape(str(text))


def load_template(theme_path):
    """Load HTML template file."""
    with open(theme_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_css(css_path):
    """Load CSS stylesheet."""
    with open(css_path, 'r', encoding='utf-8') as f:
        return f.read()


def validate_resume_data(resume_data):
    """Validate resume data structure and required fields."""
    errors = []

    # Check required top-level fields
    required_fields = ["personal"]
    for field in required_fields:
        if field not in resume_data:
            errors.append(f"Missing required field: {field}")

    # Validate personal info
    if "personal" in resume_data:
        personal = resume_data["personal"]
        if not personal.get("name"):
            errors.append("Missing name in personal info")

        # Validate email format
        email = personal.get("email", "")
        if email and not is_valid_email(email):
            errors.append(f"Invalid email format: {email}")

    return errors


def is_valid_email(email):
    """Basic email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def generate_resume_html(resume_data, theme="modern", language="en"):
    """
    Generate HTML resume from JSON data with specified theme and language.
    """
    # Load template and CSS
    skill_dir = Path(__file__).parent.parent
    template_path = skill_dir / "assets" / "templates" / f"{theme}.html"
    css_path = skill_dir / "assets" / "css" / f"{theme}.css"

    if not template_path.exists():
        # Fallback to modern template
        template_path = skill_dir / "assets" / "templates" / "modern.html"

    if not css_path.exists():
        # Fallback to modern CSS
        css_path = skill_dir / "assets" / "css" / "modern.css"

    template = load_template(template_path)
    css = load_css(css_path)

    # Build HTML content
    html_content = build_sections(resume_data, language)

    # Insert CSS, content, and language into template
    full_html = template.replace("{{CSS}}", css)
    full_html = full_html.replace("{{CONTENT}}", html_content)
    full_html = full_html.replace("{{LANG}}", language)

    return full_html


def build_sections(resume_data, language):
    """Build HTML sections from resume data."""
    sidebar_sections = []
    main_sections = []

    # Header (Personal Info) — always in sidebar
    sidebar_sections.append(build_header(resume_data.get("personal", {}), language))

    # Summary
    if resume_data.get("summary"):
        main_sections.append(build_summary(resume_data["summary"], language))

    # Experience
    if resume_data.get("experience"):
        main_sections.append(build_experience(resume_data["experience"], language))

    # Education
    if resume_data.get("education"):
        main_sections.append(build_education(resume_data["education"], language))

    # Projects
    if resume_data.get("projects"):
        main_sections.append(build_projects(resume_data["projects"], language))

    # Skills — always in sidebar
    if resume_data.get("skills"):
        sidebar_sections.append(build_skills(resume_data["skills"], language))

    sidebar_html = '<aside class="sidebar">' + "\n".join(sidebar_sections) + '</aside>'
    main_html = '<main class="main-content">' + "\n".join(main_sections) + '</main>'

    return sidebar_html + "\n" + main_html


def build_header(personal, language):
    """Build header section with personal info."""
    name = escape_text(personal.get("name", "Your Name"))
    email = escape_text(personal.get("email", ""))
    phone = escape_text(personal.get("phone", ""))
    location = escape_text(personal.get("location", ""))
    linkedin = escape_text(personal.get("linkedin", ""))
    github = escape_text(personal.get("github", ""))

    contact_items = []
    if email:
        contact_items.append(f'<span class="contact-item contact-email"><a href="mailto:{email}">{email}</a></span>')
    if phone:
        contact_items.append(f'<span class="contact-item contact-phone">{phone}</span>')
    if location:
        contact_items.append(f'<span class="contact-item contact-location">{location}</span>')
    if linkedin:
        contact_items.append(f'<span class="contact-item contact-linkedin"><a href="{linkedin}" target="_blank">LinkedIn</a></span>')
    if github:
        contact_items.append(f'<span class="contact-item contact-github"><a href="{github}" target="_blank">GitHub</a></span>')

    contact_html = "\n".join(contact_items) if contact_items else ""

    return f"""
<header class="resume-header">
    <h1 class="name">{name}</h1>
    <div class="contact-info">{contact_html}</div>
</header>
"""


def build_summary(summary, language):
    """Build summary section."""
    titles = SECTION_TITLES.get(language, SECTION_TITLES["en"])
    title = titles.get("summary", "Professional Summary")
    return f"""
<section class="resume-section" data-section="summary">
    <h2 class="section-title">{title}</h2>
    <p>{escape_text(summary)}</p>
</section>
"""


def build_experience(experience, language):
    """Build experience section."""
    titles = SECTION_TITLES.get(language, SECTION_TITLES["en"])
    title = titles.get("experience", "Work Experience")
    html = f'<section class="resume-section" data-section="experience"><h2 class="section-title">{title}</h2>'

    for exp in experience:
        company = escape_text(exp.get("company", "Company Name"))
        position = escape_text(exp.get("position", "Position"))
        period = escape_text(exp.get("period", ""))
        location = escape_text(exp.get("location", ""))
        description = escape_text(exp.get("description", ""))
        responsibilities = exp.get("responsibilities", [])
        achievements = exp.get("achievements", [])

        html += f"""
<div class="experience-item">
    <div class="experience-header">
        <h3 class="company-name">{company}</h3>
        <div class="position-period">
            <span class="position">{position}</span>
            <span class="period">{period}</span>
        </div>
    </div>
    {f'<div class="location">{location}</div>' if location else ''}
"""

        if description:
            html += f"<p class='experience-description'>{description}</p>"

        if responsibilities:
            html += "<ul class='responsibilities'>"
            for resp in responsibilities:
                html += f"<li>{escape_text(resp)}</li>"
            html += "</ul>"

        if achievements:
            html += "<ul class='achievements'>"
            for ach in achievements:
                html += f"<li>{escape_text(ach)}</li>"
            html += "</ul>"

        html += "</div>"

    html += "</section>"
    return html


def build_education(education, language):
    """Build education section."""
    titles = SECTION_TITLES.get(language, SECTION_TITLES["en"])
    title = titles.get("education", "Education")
    html = f'<section class="resume-section" data-section="education"><h2 class="section-title">{title}</h2>'

    for edu in education:
        institution = escape_text(edu.get("institution", "Institution Name"))
        degree = escape_text(edu.get("degree", "Degree"))
        period = escape_text(edu.get("period", ""))
        location = escape_text(edu.get("location", ""))
        gpa = escape_text(edu.get("gpa", ""))
        honors = edu.get("honors", [])

        html += f"""
<div class="education-item">
    <div class="education-header">
        <h3 class="institution">{institution}</h3>
        <div class="degree-period">
            <span class="degree">{degree}</span>
            <span class="period">{period}</span>
        </div>
    </div>
    {f'<div class="location">{location}</div>' if location else ''}
    {f'<div class="gpa">GPA: {gpa}</div>' if gpa else ''}
"""

        if honors:
            html += "<div class='honors'><strong>Honors:</strong> " + ", ".join([escape_text(h) for h in honors]) + "</div>"

        html += "</div>"

    html += "</section>"
    return html


def build_projects(projects, language):
    """Build projects section."""
    titles = SECTION_TITLES.get(language, SECTION_TITLES["en"])
    title = titles.get("projects", "Projects")
    html = f'<section class="resume-section" data-section="projects"><h2 class="section-title">{title}</h2>'

    for proj in projects:
        name = escape_text(proj.get("name", "Project Name"))
        role = escape_text(proj.get("role", ""))
        period = escape_text(proj.get("period", ""))
        technologies = proj.get("technologies", [])
        description = escape_text(proj.get("description", ""))
        achievements = proj.get("achievements", [])

        html += f"""
<div class="project-item">
    <div class="project-header">
        <h3 class="project-name">{name}</h3>
        {f'<span class="role">{role}</span>' if role else ''}
        {f'<span class="period">{period}</span>' if period else ''}
    </div>
"""

        if technologies:
            escaped_techs = [escape_text(t) for t in technologies]
            html += f"<div class='technologies'><strong>Technologies:</strong> {', '.join(escaped_techs)}</div>"

        if description:
            html += f"<p class='project-description'>{description}</p>"

        if achievements:
            html += "<ul class='achievements'>"
            for ach in achievements:
                html += f"<li>{escape_text(ach)}</li>"
            html += "</ul>"

        html += "</div>"

    html += "</section>"
    return html


def build_skills(skills, language):
    """Build skills section."""
    titles = SECTION_TITLES.get(language, SECTION_TITLES["en"])
    title = titles.get("skills", "Skills")
    html = f'<section class="resume-section" data-section="skills"><h2 class="section-title">{title}</h2>'

    for category, skill_list in skills.items():
        category_escaped = escape_text(category)
        if isinstance(skill_list, list) and skill_list:
            escaped_skills = [escape_text(s) for s in skill_list]
            html += f"""
<div class="skill-category">
    <h3 class="category-title">{category_escaped.replace('_', ' ').title()}</h3>
    <div class="skill-list">{', '.join(escaped_skills)}</div>
</div>
"""
        elif isinstance(skill_list, str):
            html += f"""
<div class="skill-category">
    <h3 class="category-title">{category_escaped.replace('_', ' ').title()}</h3>
    <div class="skill-list">{escape_text(skill_list)}</div>
</div>
"""

    html += "</section>"
    return html


def main():
    parser = argparse.ArgumentParser(description='Generate HTML resume from JSON data')
    parser.add_argument('resume_json', help='Path to resume JSON file')
    parser.add_argument('output_html', help='Path to output HTML file')
    parser.add_argument('--theme', default='modern', choices=['modern', 'classic', 'minimal', 'creative'],
                        help='Resume theme (default: modern)')
    parser.add_argument('--lang', default='en', choices=['en', 'zh', 'ja', 'fr', 'de', 'es'],
                        help='Language (default: en)')

    args = parser.parse_args()

    # Load resume data with error handling
    try:
        with open(args.resume_json, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Resume file not found: {args.resume_json}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.resume_json}")
        print(f"Details: {e}")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Failed to read file. Please ensure it's UTF-8 encoded: {args.resume_json}")
        sys.exit(1)

    # Validate resume data
    validation_errors = validate_resume_data(resume_data)
    if validation_errors:
        print("Error: Resume data validation failed:")
        for error in validation_errors:
            print(f"  - {error}")
        sys.exit(1)

    # Generate HTML
    print(f"Generating HTML resume with theme '{args.theme}' in {args.lang}...")
    try:
        html = generate_resume_html(resume_data, theme=args.theme, language=args.lang)
    except Exception as e:
        print(f"Error: Failed to generate HTML")
        print(f"Details: {e}")
        sys.exit(1)

    # Save to file with error handling
    try:
        with open(args.output_html, 'w', encoding='utf-8') as f:
            f.write(html)
    except Exception as e:
        print(f"Error: Failed to write output file: {args.output_html}")
        print(f"Details: {e}")
        sys.exit(1)

    print(f"Resume generated: {args.output_html}")
    print(f"Open in browser to view: file://{Path(args.output_html).absolute()}")


if __name__ == "__main__":
    main()
