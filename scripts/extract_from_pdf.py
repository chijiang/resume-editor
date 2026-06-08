#!/usr/bin/env python3
"""
Extract resume content from PDF and structure into JSON format.
Supports extraction of personal info, education, experience, projects, and skills.
"""

import json
import sys
import re
from pathlib import Path

# Use PyMuPDF (fitz) for PDF text extraction
try:
    import fitz
except ImportError:
    print("Error: PyMuPDF (fitz) not installed. Run: pip install pymupdf")
    sys.exit(1)


def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def parse_resume_text(text):
    """
    Parse resume text into structured JSON format.
    This is a basic parser - for production use, consider more sophisticated NLP.
    """
    resume = {
        "personal": {},
        "summary": "",
        "education": [],
        "experience": [],
        "projects": [],
        "skills": {}
    }

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    current_section = None

    # Simple section detection
    section_patterns = {
        "summary": ["summary", "个人简介", "简介", "about"],
        "education": ["education", "教育背景", "学历", "academic"],
        "experience": ["experience", "work experience", "工作经历", "工作", "employment"],
        "projects": ["projects", "项目", "project experience"],
        "skills": ["skills", "技能", "技术栈", "technologies"]
    }

    for i, line in enumerate(lines):
        # Detect section headers
        line_lower = line.lower()
        new_section = None
        for section, patterns in section_patterns.items():
            if any(pattern in line_lower for pattern in patterns):
                new_section = section
                break

        if new_section:
            current_section = new_section
            continue

        # Parse content based on current section
        if current_section == "summary" and not resume["summary"]:
            resume["summary"] = line
        elif current_section == "education":
            if any(char.isdigit() for char in line):
                # Likely contains a year
                resume["education"].append({"raw": line})
        elif current_section == "experience":
            if line and not any(keyword in line.lower() for keyword in ["responsibilities", "achievements"]):
                resume["experience"].append({"raw": line})
        elif current_section == "projects":
            if line and len(line.split()) > 2:  # Ignore short lines
                resume["projects"].append({"raw": line})
        elif current_section == "skills":
            if ":" in line or "-" in line or "•" in line:
                resume["skills"]["general"] = resume["skills"].get("general", "") + " " + line

    # Try to extract personal info from first few lines
    if len(lines) >= 3:
        resume["personal"]["name"] = lines[0]
        if "@" in lines[1]:
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', lines[1])
            if email_match:
                resume["personal"]["email"] = email_match.group()

    return resume


def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_from_pdf.py <input.pdf> <output.json>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_json = sys.argv[2]

    if not Path(input_pdf).exists():
        print(f"Error: PDF file not found: {input_pdf}")
        sys.exit(1)

    print(f"Extracting content from: {input_pdf}")

    # Extract text from PDF
    text = extract_text_from_pdf(input_pdf)

    # Parse into structured format
    resume = parse_resume_text(text)

    # Save to JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(resume, f, ensure_ascii=False, indent=2)

    print(f"Resume data extracted and saved to: {output_json}")
    print("\nExtracted structure:")
    print(f"  Personal info: {len(resume['personal'])} fields")
    print(f"  Summary: {len(resume['summary'])} chars")
    print(f"  Education: {len(resume['education'])} entries")
    print(f"  Experience: {len(resume['experience'])} entries")
    print(f"  Projects: {len(resume['projects'])} entries")
    print(f"  Skills: {len(resume['skills'])} categories")


if __name__ == "__main__":
    main()
