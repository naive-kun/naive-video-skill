#!/usr/bin/env python3
"""Safely read and update Naive Video Skill project state."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


STAGES = (
    "initialized",
    "captions_ready",
    "design_ready",
    "preview_ready",
    "approved",
    "rendering",
    "final_ready",
)
APPROVAL = ("pending", "approved", "skipped_by_user")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load(project: Path) -> tuple[Path, dict]:
    path = project / ".naive-video-state.json"
    if not path.exists():
        raise FileNotFoundError(f"state not found: {path}")
    return path, json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, state: dict) -> None:
    state["updated_at"] = now_iso()
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(temp.read_text(encoding="utf-8"))
    temp.replace(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("show")

    stage = subparsers.add_parser("stage")
    stage.add_argument("value", choices=STAGES)
    stage.add_argument("--force", action="store_true", help="Allow an intentional stage regression")

    approval = subparsers.add_parser("approval")
    approval.add_argument("value", choices=APPROVAL)
    approval.add_argument("--url")

    output = subparsers.add_parser("output")
    output.add_argument("name")
    output.add_argument("path")

    style = subparsers.add_parser("style")
    style.add_argument("name")
    style.add_argument("value")

    error = subparsers.add_parser("error")
    error.add_argument("message", nargs="?")
    error.add_argument("--clear", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    project = Path(args.project).expanduser().resolve()
    try:
        path, state = load(project)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.command == "show":
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0

    if args.command == "stage":
        current = state.get("stage", "initialized")
        if current not in STAGES:
            print(f"ERROR: current state has invalid stage: {current}", file=sys.stderr)
            return 2
        if STAGES.index(args.value) < STAGES.index(current) and not args.force:
            print("ERROR: stage regression requires --force", file=sys.stderr)
            return 2
        state["stage"] = args.value

    elif args.command == "approval":
        approval = state.setdefault("approval", {})
        approval["status"] = args.value
        approval["approved_at"] = now_iso() if args.value in {"approved", "skipped_by_user"} else None
        if args.url:
            approval["preview_url"] = args.url
        if args.value == "approved" and state.get("stage") == "preview_ready":
            state["stage"] = "approved"
        if args.value == "pending" and state.get("stage") in {"approved", "rendering", "final_ready"}:
            state["stage"] = "preview_ready"

    elif args.command == "output":
        state.setdefault("outputs", {})[args.name] = args.path

    elif args.command == "style":
        state.setdefault("style_profile", {})[args.name] = args.value

    elif args.command == "error":
        state["last_error"] = None if args.clear else args.message

    save(path, state)
    print(f"Updated: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
