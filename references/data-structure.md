# Resume Data Structure

Resume data is maintained in structured JSON format. The `personal.name` field is required; all other fields are optional.

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
      "description": "High-level description of role and responsibilities.",
      "achievements": ["Quantified achievement with metrics"]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "role": "Role (e.g., Lead Developer)",
      "period": "2023",
      "technologies": ["Python", "React", "AWS"],
      "description": "Brief overview...",
      "achievements": ["Launched product with 10k+ users"]
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

## Work File Convention

By default, save resume JSON to `resume.json` in the current working directory. If the user specifies a different location, use that instead. When importing from PDF, extract to the same location with a `.json` extension replacing `.pdf`.
