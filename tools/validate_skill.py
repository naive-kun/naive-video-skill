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
WORKFLOW_FILES = (
    "init.md",
    "rough-cut.md",
    "captions.md",
    "design.md",
    "preview.md",
    "export.md",
    "revise.md",
    "status.md",
    "doctor.md",
    "learn.md",
    "retro.md",
    "migrate.md",
)
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh", ".csv"}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
RECURSIVE_FORCE_DELETE = re.compile(
    r"\b" + "r" + "m" + r"\s+-(?:[^\s]*r[^\s]*f|[^\s]*f[^\s]*r)\b"
)
SHOTCRAFT_IMPLEMENTATIONS = {"gsap-adapted", "hyperframes-custom"}
MOTION_DENSITIES = {"restrained", "balanced", "energetic"}


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
            if RECURSIVE_FORCE_DELETE.search(line):
                findings.append(
                    f"{path.relative_to(root)}:{line_number}: recursive force-delete command is forbidden"
                )
            if "shutil." + "rmtree" in line:
                findings.append(
                    f"{path.relative_to(root)}:{line_number}: recursive tree deletion is forbidden"
                )
    return findings


def validate_shotcraft_mapping(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return [f"invalid ShotCraft mapping JSON: {exc}"]
    if not isinstance(data, dict):
        return ["ShotCraft mapping root must be an object"]
    if data.get("provider") != "video-shotcraft":
        errors.append("ShotCraft mapping provider must be video-shotcraft")
    cards = data.get("cards")
    if not isinstance(cards, list) or not cards:
        return errors + ["ShotCraft mapping cards must be a non-empty array"]

    default_pack = data.get("default_pack")
    if not isinstance(default_pack, dict):
        errors.append("ShotCraft mapping needs a default_pack object")

    names: set[str] = set()
    for index, card in enumerate(cards, start=1):
        prefix = f"ShotCraft mapping card[{index}]"
        if not isinstance(card, dict):
            errors.append(f"{prefix} must be an object")
            continue
        name = card.get("card")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{prefix} needs a card name")
        elif name in names:
            errors.append(f"{prefix} duplicates card {name!r}")
        else:
            names.add(name)
        if not isinstance(card.get("native_recipe_ids"), list) or not card["native_recipe_ids"]:
            errors.append(f"{prefix} needs native_recipe_ids")
        if not isinstance(card.get("semantic_tags"), list) or not card["semantic_tags"]:
            errors.append(f"{prefix} needs semantic_tags")
        if card.get("implementation") not in SHOTCRAFT_IMPLEMENTATIONS:
            errors.append(f"{prefix} has unsupported default implementation")
        densities = card.get("densities")
        if not isinstance(densities, list) or not densities or not set(densities).issubset(MOTION_DENSITIES):
            errors.append(f"{prefix} has invalid densities")
        duration = card.get("recommended_duration")
        if (
            not isinstance(duration, list)
            or len(duration) != 2
            or not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in duration)
            or duration[0] <= 0
            or duration[1] <= duration[0]
        ):
            errors.append(f"{prefix} has invalid recommended_duration")
        if not isinstance(card.get("allow_during_evidence"), bool):
            errors.append(f"{prefix} needs boolean allow_during_evidence")

    if isinstance(default_pack, dict):
        if not isinstance(default_pack.get("pack_id"), str) or not default_pack["pack_id"].strip():
            errors.append("ShotCraft default_pack needs pack_id")
        if default_pack.get("enabled_for_new_projects") is not True:
            errors.append("ShotCraft default_pack must be enabled for new projects")
        if default_pack.get("provider_required_at_runtime") is not False:
            errors.append("ShotCraft default_pack must not require the provider at runtime")
        if default_pack.get("remotion_required") is not False:
            errors.append("ShotCraft default_pack must not require Remotion")
        limits = default_pack.get("max_references_by_density")
        if not isinstance(limits, dict) or set(limits) != MOTION_DENSITIES:
            errors.append("ShotCraft default_pack needs a cap for every motion density")
        elif any(
            not isinstance(value, int) or isinstance(value, bool) or value < 0
            for value in limits.values()
        ):
            errors.append("ShotCraft default_pack density caps must be non-negative integers")
        default_cards = default_pack.get("cards")
        if not isinstance(default_cards, list) or not default_cards:
            errors.append("ShotCraft default_pack cards must be a non-empty array")
        elif len(default_cards) != len(set(default_cards)):
            errors.append("ShotCraft default_pack cards must be unique")
        else:
            unknown = sorted(set(default_cards) - names)
            if unknown:
                errors.append(
                    "ShotCraft default_pack references unknown cards: " + ", ".join(unknown)
                )
    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    root_skill = root / "SKILL.md"
    if not root_skill.exists():
        return ["missing root SKILL.md"]
    _, fm_errors = frontmatter(root_skill)
    errors.extend(f"SKILL.md: {item}" for item in fm_errors)

    skill_manifests = [
        path for path in root.rglob("SKILL.md") if ".git" not in path.parts
    ]
    if len(skill_manifests) != 1 or skill_manifests[0] != root_skill:
        listed = ", ".join(str(path.relative_to(root)) for path in skill_manifests)
        errors.append(
            "public package must expose exactly one SKILL.md for WorkBuddy-style installers; "
            f"found: {listed or 'none'}"
        )

    for workflow_name in WORKFLOW_FILES:
        path = root / "references" / "workflows" / workflow_name
        if not path.exists():
            errors.append(f"missing internal workflow: references/workflows/{workflow_name}")

    for path in (
        root / "agents" / "openai.yaml",
        root / "templates" / "state.template.json",
        root / "templates" / "CONTENT_LOGIC.template.json",
        root / "templates" / "KEYFRAME_REVIEW.template.md",
        root / "references" / "content-logic-workflow.md",
        root / "references" / "visual-quality-rules.md",
        root / "references" / "video-use-integration.md",
        root / "references" / "asset-onboarding.md",
        root / "references" / "gsap-runtime.md",
        root / "references" / "shotcraft-integration.md",
        root / "references" / "shotcraft-default-pack.md",
        root / "references" / "shotcraft-mapping.json",
        root / "tools" / "design_check.py",
        root / "tools" / "content_logic_check.py",
        root / "tools" / "gsap_check.py",
        root / "tools" / "shotcraft_catalog.py",
        root / "tools" / "shotcraft_default_plan.py",
        root / "tools" / "remotion_runtime.py",
        root / "tools" / "install_copy.py",
        root / "templates" / "MOTION_PLAN.template.json",
        root / "tests" / "fixtures" / "shotcraft-mini-library.json",
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

    shotcraft_mapping = root / "references" / "shotcraft-mapping.json"
    if shotcraft_mapping.exists():
        errors.extend(validate_shotcraft_mapping(shotcraft_mapping))

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
