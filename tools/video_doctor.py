#!/usr/bin/env python3
"""Read-only environment and project consistency checks."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from design_check import validate as validate_design


REQUIRED_COMMANDS = ("python3", "ffmpeg", "ffprobe")
OPTIONAL_COMMANDS = ("node", "npm", "npx")
VALID_STAGES = {
    "initialized",
    "captions_ready",
    "design_ready",
    "preview_ready",
    "approved",
    "rendering",
    "final_ready",
}


def resolve_project_path(project: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else (project / path).resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    blockers: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    for command in REQUIRED_COMMANDS:
        path = shutil.which(command)
        if path:
            info.append(f"{command}: {path}")
        else:
            blockers.append(f"required command missing: {command}")
    for command in OPTIONAL_COMMANDS:
        path = shutil.which(command)
        if path:
            info.append(f"{command}: {path}")
        else:
            warnings.append(f"optional preview command missing: {command}")

    if not project.exists():
        blockers.append(f"project directory not found: {project}")
    state_path = project / ".naive-video-state.json"
    state = None
    if not state_path.exists():
        blockers.append("missing .naive-video-state.json; run the root skill's init workflow")
    else:
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            info.append(f"state schema: {state.get('schema_version', 'missing')}")
        except (OSError, json.JSONDecodeError) as exc:
            blockers.append(f"invalid state JSON: {exc}")

    for relative in (
        "EDIT_PLAN.md",
        "DESIGN.md",
        "VIDEO_LESSONS.md",
        "VIDEO_RETRO.md",
        "qa/QA_REPORT.md",
    ):
        path = project / relative
        if path.exists():
            info.append(f"project file: {relative}")
        else:
            warnings.append(f"project file missing: {relative}")

    if state:
        stage = state.get("stage")
        if stage not in VALID_STAGES:
            blockers.append(f"invalid stage: {stage!r}")
        else:
            info.append(f"stage: {stage}")

        main_video = state.get("main_video")
        if not main_video:
            blockers.append("state has no main_video")
        else:
            source = resolve_project_path(project, main_video)
            if not source.exists():
                blockers.append(f"main video missing: {source}")
            else:
                info.append(f"main video: {source}")

        working_video = state.get("working_video")
        if working_video:
            working = resolve_project_path(project, str(working_video))
            if not working.exists():
                blockers.append(f"working video missing: {working}")
            else:
                info.append(f"working video: {working}")
            if state.get("master_audio") != "working_video":
                warnings.append("working_video exists but master_audio is not working_video")
        elif state.get("master_audio") == "working_video":
            blockers.append("master_audio points to working_video, but no working_video is recorded")

        approval = state.get("approval", {})
        if stage in {"approved", "rendering", "final_ready"} and approval.get("status") not in {
            "approved",
            "skipped_by_user",
        }:
            blockers.append(f"stage {stage} requires approved or explicitly skipped preview")
        if stage in {"preview_ready", "approved", "rendering", "final_ready"} and not approval.get("preview_url"):
            if approval.get("status") != "skipped_by_user":
                warnings.append("preview-stage project has no recorded official preview URL")

        outputs = state.get("outputs", {})
        if isinstance(outputs, dict):
            for name, value in outputs.items():
                if not value:
                    continue
                output = resolve_project_path(project, str(value))
                if output.exists():
                    info.append(f"output {name}: {output}")
                else:
                    warnings.append(f"state output missing ({name}): {output}")
        else:
            blockers.append("state outputs must be an object")

        if stage == "final_ready":
            final_value = outputs.get("final") if isinstance(outputs, dict) else None
            if not final_value:
                blockers.append("final_ready stage requires outputs.final")
            else:
                final_path = resolve_project_path(project, str(final_value))
                if not final_path.exists() or final_path.stat().st_size == 0:
                    blockers.append(f"final output is missing or empty: {final_path}")

        if stage in {"captions_ready", "design_ready", "preview_ready", "approved", "rendering", "final_ready"}:
            srt = project / "edit" / "script-aligned.srt"
            csv = project / "edit" / "caption-table.csv"
            if not srt.exists() or not csv.exists():
                blockers.append("stage expects caption files, but SRT or CSV is missing")

        if stage in {"design_ready", "preview_ready", "approved", "rendering", "final_ready"}:
            design_path = project / "DESIGN.md"
            if design_path.exists():
                design_errors = validate_design(design_path)
                if design_errors:
                    blockers.extend(f"design contract: {error}" for error in design_errors)
                else:
                    info.append("design contract: passed")

        if stage in {"preview_ready", "approved", "rendering", "final_ready"}:
            preview_dir = project / "preview"
            if not preview_dir.exists() or not any(preview_dir.iterdir()):
                blockers.append("stage expects preview artifacts, but preview directory is empty")

    for message in blockers:
        print(f"[BLOCKER] {message}")
    for message in warnings:
        print(f"[WARNING] {message}")
    for message in info:
        print(f"[INFO] {message}")
    print(f"Summary: {len(blockers)} blockers, {len(warnings)} warnings, {len(info)} verified facts")
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
