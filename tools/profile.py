#!/usr/bin/env python3
"""Manage private, local Naive Video style profiles."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_profile_path() -> Path:
    return Path.home() / ".naive-video" / "profiles" / "default.json"


def atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload["updated_at"] = now_iso()
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(temp.read_text(encoding="utf-8"))
    temp.replace(path)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


PRIVATE_RULE = re.compile(r"(?:/(?:Users|home)/[^\s]+|[A-Za-z]:\\\\Users\\\\[^\s]+)")


def normalized_rule(value: str) -> str:
    rule = " ".join(value.split())
    if not rule:
        raise ValueError("rule cannot be empty")
    if len(rule) > 300:
        raise ValueError("rule must be 300 characters or fewer")
    if PRIVATE_RULE.search(rule):
        raise ValueError("rule contains a private home path; sanitize it first")
    return rule


def rule_id(stage: str, rule: str) -> str:
    digest = hashlib.sha256(f"{stage}\0{rule}".encode("utf-8")).hexdigest()[:12]
    return f"rule-{digest}"


def write_profile_rules(path: Path, rules: list[dict]) -> None:
    active_rules = [item for item in rules if item.get("active", True) and item.get("rule")]
    lines = [
        f"- [{item.get('stage', 'design')}] {item['rule']}"
        + (f" (`{item['id']}`)" if item.get("id") else "")
        for item in active_rules
    ] or ["- None yet."]
    start = "<!-- profile-rules:start -->"
    end = "<!-- profile-rules:end -->"
    text = path.read_text(encoding="utf-8") if path.exists() else "# VIDEO LESSONS\n"
    replacement = start + "\n" + "\n".join(lines) + "\n" + end
    if start in text and end in text:
        before, remainder = text.split(start, 1)
        _, after = remainder.split(end, 1)
        text = before + replacement + after
    else:
        text += "\n\n## Imported Profile Rules\n\n" + replacement + "\n"
    path.write_text(text, encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--path", default=str(default_profile_path()))
    commands = root.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init")
    init.add_argument("--name", default="default")

    commands.add_parser("show")

    rule = commands.add_parser("add-rule")
    rule.add_argument("--rule", required=True)
    rule.add_argument("--stage", choices=("captions", "design", "preview", "render", "qa"), required=True)
    rule.add_argument("--supersedes", help="Active rule id replaced by this rule")

    deactivate = commands.add_parser("deactivate-rule")
    deactivate.add_argument("--id", required=True)

    style = commands.add_parser("set-style")
    style.add_argument("name")
    style.add_argument("value")

    apply_profile = commands.add_parser("apply")
    apply_profile.add_argument("--project", required=True)
    return root


def main() -> int:
    args = parser().parse_args()
    path = Path(args.path).expanduser().resolve()

    if args.command == "init":
        if path.exists():
            print(f"Profile already exists: {path}")
            return 0
        profile = {
            "schema_version": "1.0",
            "profile_name": args.name,
            "style_profile": {},
            "rules": [],
            "updated_at": now_iso(),
        }
        atomic_write(path, profile)
        print(f"Created profile: {path}")
        return 0

    if not path.exists():
        print(f"ERROR: profile not found: {path}", file=sys.stderr)
        print("Run profile.py init first.", file=sys.stderr)
        return 2
    try:
        profile = load(path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: invalid profile: {exc}", file=sys.stderr)
        return 2

    if args.command == "show":
        print(json.dumps(profile, ensure_ascii=False, indent=2))
        return 0

    if args.command == "add-rule":
        try:
            rule_text = normalized_rule(args.rule)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        rules = profile.setdefault("rules", [])
        if any(
            item.get("rule") == rule_text
            and item.get("stage") == args.stage
            and item.get("active", True)
            for item in rules
        ):
            print("Rule already exists; no change.")
            return 0
        if args.supersedes:
            replaced = next(
                (item for item in rules if item.get("id") == args.supersedes and item.get("active", True)),
                None,
            )
            if not replaced:
                print(f"ERROR: active rule not found: {args.supersedes}", file=sys.stderr)
                return 2
            replaced["active"] = False
            replaced["superseded_at"] = now_iso()
        identifier = rule_id(args.stage, rule_text)
        rules.append(
            {
                "id": identifier,
                "rule": rule_text,
                "stage": args.stage,
                "active": True,
                "source": "explicit_user_feedback",
                "confirmed_at": now_iso(),
                "supersedes": args.supersedes,
            }
        )
        atomic_write(path, profile)
        print(f"Added profile rule: {identifier} {rule_text}")
        return 0

    if args.command == "deactivate-rule":
        rules = profile.setdefault("rules", [])
        target = next(
            (item for item in rules if item.get("id") == args.id and item.get("active", True)),
            None,
        )
        if not target:
            print(f"ERROR: active rule not found: {args.id}", file=sys.stderr)
            return 2
        target["active"] = False
        target["deactivated_at"] = now_iso()
        atomic_write(path, profile)
        print(f"Deactivated profile rule: {args.id}")
        return 0

    if args.command == "set-style":
        profile.setdefault("style_profile", {})[args.name] = args.value
        atomic_write(path, profile)
        print(f"Updated profile style: {args.name}={args.value}")
        return 0

    if args.command == "apply":
        project = Path(args.project).expanduser().resolve()
        state_path = project / ".naive-video-state.json"
        if not state_path.exists():
            print(f"ERROR: project state not found: {state_path}", file=sys.stderr)
            return 2
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.setdefault("style_profile", {}).update(profile.get("style_profile", {}))
        state["profile"] = {
            "name": profile.get("profile_name", "default"),
            "path": str(path),
            "loaded": True,
            "rules_loaded": len(
                [item for item in profile.get("rules", []) if item.get("active", True)]
            ),
        }
        atomic_write(state_path, state)
        write_profile_rules(project / "VIDEO_LESSONS.md", profile.get("rules", []))
        print(f"Applied profile to: {project}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
