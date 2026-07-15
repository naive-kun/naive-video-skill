#!/usr/bin/env python3
"""Validate skill structure and privacy without third-party Python packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ABSOLUTE_PRIVATE = re.compile(r"(?<![A-Za-z0-9_$.-])/(?:Users|home)/[^/< >\"']+")
SECRET = re.compile(
    r"(?i)(?:api[_-]?key|secret|password|access[_-]?token)\s*[:=]\s*[\"'][^\"']{6,}[\"']"
)
ROUTED_SKILLS = (
    "naive-video-init",
    "naive-video-captions",
    "naive-video-design",
    "naive-video-preview",
    "naive-video-export",
    "naive-video-revise",
    "naive-video-status",
    "naive-video-doctor",
    "naive-video-learn",
    "naive-video-retro",
    "naive-video-migrate",
)
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh", ".csv"}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, ["missing opening frontmatter delimiter"]
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, ["missing closing frontmatter delimiter"]
    fields: dict[str, str] = {}
    errors: list[str] = []
    current_key = None
    for raw_line in parts[1].splitlines():
        if not raw_line.strip():
            continue
        if raw_line.startswith((" ", "\t")) and current_key:
            fields[current_key] += " " + raw_line.strip()
            continue
        if ":" not in raw_line:
            errors.append(f"invalid frontmatter line: {raw_line}")
            continue
        key, value = raw_line.split(":", 1)
        current_key = key.strip()
        fields[current_key] = value.strip().strip('"\'')
    unknown = sorted(set(fields) - {"name", "description"})
    if unknown:
        errors.append(f"unsupported frontmatter fields: {', '.join(unknown)}")
    if not fields.get("name"):
        errors.append("missing name")
    elif not NAME_RE.fullmatch(fields["name"]):
        errors.append(f"invalid skill name: {fields['name']}")
    if not fields.get("description"):
        errors.append("missing description")
    return fields, errors


def privacy_findings(root: Path) -> list[str]:
    findings: list[str] = []
    ignored_parts = {".git", "node_modules", "renders", "final"}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if ABSOLUTE_PRIVATE.search(line):
                findings.append(f"{path.relative_to(root)}:{line_number}: personal absolute path")
            if SECRET.search(line):
                findings.append(f"{path.relative_to(root)}:{line_number}: possible embedded secret")
    return findings


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    root_skill = root / "SKILL.md"
    if not root_skill.exists():
        return ["missing root SKILL.md"]
    _, fm_errors = frontmatter(root_skill)
    errors.extend(f"SKILL.md: {item}" for item in fm_errors)

    for skill_name in ROUTED_SKILLS:
        path = root / "skills" / skill_name / "SKILL.md"
        if not path.exists():
            errors.append(f"missing routed skill: skills/{skill_name}/SKILL.md")
            continue
        fields, child_errors = frontmatter(path)
        if fields.get("name") and fields["name"] != skill_name:
            child_errors.append(f"name does not match folder: {fields['name']} != {skill_name}")
        errors.extend(f"skills/{skill_name}/SKILL.md: {item}" for item in child_errors)
        if not (root / "skills" / skill_name / "agents" / "openai.yaml").exists():
            errors.append(f"missing agent metadata: skills/{skill_name}/agents/openai.yaml")

    for path in (
        root / "agents" / "openai.yaml",
        root / "templates" / "state.template.json",
        root / "migrations" / "registry.md",
        root / "VERSION",
        root / "install.sh",
        root / "uninstall.sh",
    ):
        if not path.exists():
            errors.append(f"missing required file: {path.relative_to(root)}")

    state_template = root / "templates" / "state.template.json"
    if state_template.exists():
        try:
            json.loads(state_template.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid state template JSON: {exc}")
        else:
            version_path = root / "VERSION"
            if version_path.exists():
                version = version_path.read_text(encoding="utf-8").strip()
                template_version = json.loads(state_template.read_text(encoding="utf-8")).get("skill_version")
                if template_version != version:
                    errors.append(
                        f"state template skill_version {template_version!r} does not match VERSION {version!r}"
                    )

    for markdown in root.rglob("*.md"):
        if ".git" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            target = target.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (markdown.parent / target_path).resolve()
            if not resolved.exists():
                errors.append(
                    f"broken markdown link in {markdown.relative_to(root)}: {target}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--privacy-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(f"ERROR: path not found: {root}")
        return 2

    errors = [] if args.privacy_only else validate(root)
    errors.extend(privacy_findings(root))
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Validation failed with {len(errors)} issue(s).")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
