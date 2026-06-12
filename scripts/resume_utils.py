#!/usr/bin/env python3
"""
Shared constants and helpers for resume tooling.
"""

from __future__ import annotations

import copy
import re

SUPPORTED_THEMES = ["modern", "classic", "minimal", "creative"]
SUPPORTED_LANGUAGES = ["en", "zh", "ja", "fr", "de", "es"]

LOCALIZED_TEXT = {
    "en": {
        "summary": "Professional Summary",
        "experience": "Work Experience",
        "education": "Education",
        "projects": "Projects",
        "skills": "Skills",
        "gpa": "GPA",
        "honors": "Honors",
        "technologies": "Technologies",
        "edit_resume": "Edit resume",
        "exit_edit_mode": "Exit edit mode",
        "editing_resume": "Editing Resume",
        "copy_json": "Copy JSON",
        "done": "Done",
        "json_copied": "JSON copied to clipboard!",
        "json_console": "JSON printed to browser console (F12)",
        "add_item": "Add item",
        "remove_item": "Remove item",
        "new_item": "New item",
    },
    "zh": {
        "summary": "个人简介",
        "experience": "工作经历",
        "education": "教育背景",
        "projects": "项目经历",
        "skills": "技能",
        "gpa": "GPA",
        "honors": "荣誉",
        "technologies": "技术栈",
        "edit_resume": "编辑简历",
        "exit_edit_mode": "退出编辑模式",
        "editing_resume": "正在编辑简历",
        "copy_json": "复制 JSON",
        "done": "完成",
        "json_copied": "JSON 已复制到剪贴板",
        "json_console": "JSON 已输出到浏览器控制台 (F12)",
        "add_item": "新增条目",
        "remove_item": "删除条目",
        "new_item": "新条目",
    },
    "ja": {
        "summary": "プロフィール",
        "experience": "職歴",
        "education": "学歴",
        "projects": "プロジェクト",
        "skills": "スキル",
        "gpa": "GPA",
        "honors": "受賞歴",
        "technologies": "技術",
        "edit_resume": "履歴書を編集",
        "exit_edit_mode": "編集モードを終了",
        "editing_resume": "履歴書を編集中",
        "copy_json": "JSON をコピー",
        "done": "完了",
        "json_copied": "JSON をクリップボードにコピーしました",
        "json_console": "JSON をブラウザのコンソール (F12) に出力しました",
        "add_item": "項目を追加",
        "remove_item": "項目を削除",
        "new_item": "新しい項目",
    },
    "fr": {
        "summary": "Profil Professionnel",
        "experience": "Experience Professionnelle",
        "education": "Formation",
        "projects": "Projets",
        "skills": "Competences",
        "gpa": "GPA",
        "honors": "Distinctions",
        "technologies": "Technologies",
        "edit_resume": "Modifier le CV",
        "exit_edit_mode": "Quitter le mode edition",
        "editing_resume": "Modification du CV",
        "copy_json": "Copier le JSON",
        "done": "Termine",
        "json_copied": "JSON copie dans le presse-papiers",
        "json_console": "JSON affiche dans la console du navigateur (F12)",
        "add_item": "Ajouter un element",
        "remove_item": "Supprimer l'element",
        "new_item": "Nouvel element",
    },
    "de": {
        "summary": "Zusammenfassung",
        "experience": "Berufserfahrung",
        "education": "Ausbildung",
        "projects": "Projekte",
        "skills": "Fahigkeiten",
        "gpa": "GPA",
        "honors": "Auszeichnungen",
        "technologies": "Technologien",
        "edit_resume": "Lebenslauf bearbeiten",
        "exit_edit_mode": "Bearbeitungsmodus beenden",
        "editing_resume": "Lebenslauf wird bearbeitet",
        "copy_json": "JSON kopieren",
        "done": "Fertig",
        "json_copied": "JSON in die Zwischenablage kopiert",
        "json_console": "JSON in der Browser-Konsole (F12) ausgegeben",
        "add_item": "Eintrag hinzufugen",
        "remove_item": "Eintrag entfernen",
        "new_item": "Neuer Eintrag",
    },
    "es": {
        "summary": "Resumen Profesional",
        "experience": "Experiencia Laboral",
        "education": "Educacion",
        "projects": "Proyectos",
        "skills": "Habilidades",
        "gpa": "GPA",
        "honors": "Reconocimientos",
        "technologies": "Tecnologias",
        "edit_resume": "Editar curriculo",
        "exit_edit_mode": "Salir del modo de edicion",
        "editing_resume": "Editando curriculo",
        "copy_json": "Copiar JSON",
        "done": "Listo",
        "json_copied": "JSON copiado al portapapeles",
        "json_console": "JSON mostrado en la consola del navegador (F12)",
        "add_item": "Agregar elemento",
        "remove_item": "Eliminar elemento",
        "new_item": "Nuevo elemento",
    },
}

TOP_LEVEL_DEFAULTS = {
    "personal": {},
    "summary": "",
    "education": [],
    "experience": [],
    "projects": [],
    "skills": {},
}

PERSONAL_FIELDS = ["name", "email", "phone", "location", "linkedin", "github"]
EDUCATION_TEXT_FIELDS = ["institution", "degree", "period", "location", "gpa"]
EXPERIENCE_TEXT_FIELDS = ["company", "position", "period", "location", "description"]
PROJECT_TEXT_FIELDS = ["name", "role", "period", "description"]
SKILL_KEY_PATTERN = re.compile(r"[^a-z0-9]+")
LIST_SPLIT_PATTERN = re.compile(r"[\n,;|•·，、]+")


def get_localized_text(language):
    """Return localized UI and label strings with English fallback."""
    strings = copy.deepcopy(LOCALIZED_TEXT["en"])
    strings.update(LOCALIZED_TEXT.get(language, {}))
    return strings


def coerce_string(value):
    """Coerce scalar values to stripped strings."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value).strip()
    return ""


def normalize_skill_key(key):
    """Canonicalize a skill category key for JSON storage."""
    text = coerce_string(key).lower()
    text = SKILL_KEY_PATTERN.sub("_", text).strip("_")
    return text or "general"


def ensure_string_list(value):
    """Normalize a list-like value into a list of strings."""
    if value is None:
        return []

    if isinstance(value, (list, tuple)):
        raw_items = list(value)
    else:
        text = coerce_string(value)
        if not text:
            return []
        if LIST_SPLIT_PATTERN.search(text):
            raw_items = LIST_SPLIT_PATTERN.split(text)
        else:
            raw_items = [text]

    items = []
    for item in raw_items:
        normalized = coerce_string(item)
        if normalized:
            items.append(normalized)
    return items


def normalize_entry_list(value):
    """Normalize a section value into a list of entry objects."""
    if value is None:
        return []
    if isinstance(value, list):
        entries = value
    else:
        entries = [value]

    normalized_entries = []
    for entry in entries:
        if isinstance(entry, dict):
            normalized_entries.append(copy.deepcopy(entry))
        else:
            raw_text = coerce_string(entry)
            if raw_text:
                normalized_entries.append({"raw": raw_text})
    return normalized_entries


def normalize_resume_data(resume_data):
    """Normalize resume data into the canonical shape used by the renderer."""
    if not isinstance(resume_data, dict):
        return copy.deepcopy(TOP_LEVEL_DEFAULTS)

    normalized = copy.deepcopy(resume_data)
    for key, default_value in TOP_LEVEL_DEFAULTS.items():
        if key not in normalized or normalized[key] is None:
            normalized[key] = copy.deepcopy(default_value)

    personal = normalized.get("personal")
    if not isinstance(personal, dict):
        personal = {}
    personal = copy.deepcopy(personal)
    for field in PERSONAL_FIELDS:
        personal[field] = coerce_string(personal.get(field, ""))
    normalized["personal"] = personal

    normalized["summary"] = coerce_string(normalized.get("summary", ""))

    skills = normalized.get("skills")
    if isinstance(skills, str):
        skills = {"general": ensure_string_list(skills)}
    elif isinstance(skills, list):
        skills = {"general": ensure_string_list(skills)}
    elif not isinstance(skills, dict):
        skills = {}
    else:
        skills = copy.deepcopy(skills)

    personal_languages = personal.pop("languages", None)
    if personal_languages and not skills.get("languages"):
        skills["languages"] = ensure_string_list(personal_languages)

    normalized_skills = {}
    for category, skill_list in skills.items():
        normalized_key = normalize_skill_key(category)
        normalized_list = ensure_string_list(skill_list)
        if normalized_list:
            normalized_skills[normalized_key] = normalized_list
    normalized["skills"] = normalized_skills

    education_entries = []
    for entry in normalize_entry_list(normalized.get("education")):
        raw_text = coerce_string(entry.get("raw", ""))
        clean_entry = copy.deepcopy(entry)
        for field in EDUCATION_TEXT_FIELDS:
            clean_entry[field] = coerce_string(clean_entry.get(field, ""))
        clean_entry["honors"] = ensure_string_list(clean_entry.get("honors"))
        if raw_text and not any(clean_entry.get(field) for field in EDUCATION_TEXT_FIELDS):
            clean_entry["institution"] = raw_text
        education_entries.append(clean_entry)
    normalized["education"] = education_entries

    experience_entries = []
    for entry in normalize_entry_list(normalized.get("experience")):
        raw_text = coerce_string(entry.get("raw", ""))
        clean_entry = copy.deepcopy(entry)
        for field in EXPERIENCE_TEXT_FIELDS:
            clean_entry[field] = coerce_string(clean_entry.get(field, ""))
        clean_entry["responsibilities"] = ensure_string_list(clean_entry.get("responsibilities"))
        clean_entry["achievements"] = ensure_string_list(clean_entry.get("achievements"))
        if raw_text and not any(clean_entry.get(field) for field in EXPERIENCE_TEXT_FIELDS):
            clean_entry["description"] = raw_text
        experience_entries.append(clean_entry)
    normalized["experience"] = experience_entries

    project_entries = []
    for entry in normalize_entry_list(normalized.get("projects")):
        raw_text = coerce_string(entry.get("raw", ""))
        clean_entry = copy.deepcopy(entry)
        for field in PROJECT_TEXT_FIELDS:
            clean_entry[field] = coerce_string(clean_entry.get(field, ""))
        clean_entry["technologies"] = ensure_string_list(clean_entry.get("technologies"))
        clean_entry["achievements"] = ensure_string_list(clean_entry.get("achievements"))
        if raw_text and not any(clean_entry.get(field) for field in PROJECT_TEXT_FIELDS):
            clean_entry["description"] = raw_text
        project_entries.append(clean_entry)
    normalized["projects"] = project_entries

    return normalized


def is_valid_email(email):
    """Basic email validation."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_resume_data(resume_data):
    """Validate resume data structure and required fields."""
    errors = []

    if not isinstance(resume_data, dict):
        return ["Resume data must be a JSON object."]

    personal = resume_data.get("personal")
    if not isinstance(personal, dict):
        errors.append("Missing required object: personal")
        return errors

    if not coerce_string(personal.get("name")):
        errors.append("Missing name in personal info")

    email = coerce_string(personal.get("email"))
    if email and not is_valid_email(email):
        errors.append(f"Invalid email format: {email}")

    return errors
