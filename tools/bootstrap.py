#!/usr/bin/env python3
"""Create or adopt a Naive Video Skill project without touching source media."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = "1.0"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def probe_video(path: Path) -> dict:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return {"status": "unavailable", "reason": "ffprobe not found"}

    command = [
        ffprobe,
        "-v",
        "error",
        "-show_entries",
        "format=duration,size",
        "-show_entries",
        "stream=index,codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        reason = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "probe failed"
        return {"status": "error", "reason": reason}
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return {"status": "error", "reason": f"invalid ffprobe JSON: {exc}"}
    payload["status"] = "ok"
    return payload


def atomic_json_write(path: Path, payload: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(temp.read_text(encoding="utf-8"))
    temp.replace(path)


def write_template(source: Path, destination: Path, replacements: dict[str, str]) -> bool:
    if destination.exists():
        return False
    text = source.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    destination.write_text(text, encoding="utf-8")
    return True


def write_profile_rules(path: Path, rules: list[dict]) -> None:
    """Replace the generated profile-rule block without touching project feedback."""
    active_rules = [item for item in rules if item.get("active", True) and item.get("rule")]
    lines = [
        f"- [{item.get('stage', 'design')}] {item['rule']}"
        + (f" (`{item['id']}`)" if item.get("id") else "")
        for item in active_rules
    ] or ["- None yet."]
    start = "<!-- profile-rules:start -->"
    end = "<!-- profile-rules:end -->"
    text = path.read_text(encoding="utf-8")
    replacement = start + "\n" + "\n".join(lines) + "\n" + end
    if start in text and end in text:
        before, remainder = text.split(start, 1)
        _, after = remainder.split(end, 1)
        text = before + replacement + after
    else:
        text += "\n\n## Imported Profile Rules\n\n" + replacement + "\n"
    path.write_text(text, encoding="utf-8")


def detect_adopted_stage(project: Path) -> str:
    srt = project / "edit" / "script-aligned.srt"
    csv = project / "edit" / "caption-table.csv"
    if srt.exists() and csv.exists() and srt.stat().st_size and csv.stat().st_size:
        return "captions_ready"
    return "initialized"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="User video project directory")
    parser.add_argument("--video", required=True, help="Main source video path")
    parser.add_argument("--mode", choices=("quick", "guided"), default="quick")
    parser.add_argument("--preset", choices=("clean", "dark", "sticker", "minimal"), default="clean")
    parser.add_argument("--accent", default="#2F7DF4")
    parser.add_argument("--aspect", default="preserve-source")
    parser.add_argument("--project-name")
    parser.add_argument(
        "--profile",
        default="auto",
        help="auto, none, or a path to a private local profile JSON",
    )
    parser.add_argument("--adopt-existing", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = Path(args.project).expanduser().resolve()
    video = Path(args.video).expanduser().resolve()
    skill_root = Path(__file__).resolve().parents[1]
    templates = skill_root / "templates"
    skill_version = (skill_root / "VERSION").read_text(encoding="utf-8").strip()

    profile_path = None
    profile = None
    if args.profile != "none":
        candidate = (
            Path.home() / ".naive-video" / "profiles" / "default.json"
            if args.profile == "auto"
            else Path(args.profile).expanduser().resolve()
        )
        if candidate.exists():
            try:
                profile = json.loads(candidate.read_text(encoding="utf-8"))
                profile_path = candidate
            except (OSError, json.JSONDecodeError) as exc:
                print(f"WARNING: profile ignored because it is invalid: {exc}")

    if not video.exists() or not video.is_file():
        print(f"ERROR: main video not found: {video}", file=sys.stderr)
        return 2

    project.mkdir(parents=True, exist_ok=True)
    state_path = project / ".naive-video-state.json"
    if state_path.exists():
        print(f"Project already initialized: {state_path}")
        print("Run naive-video-status or naive-video-doctor instead of initializing again.")
        return 3

    for directory in (
        project / "edit" / "transcripts",
        project / "preview",
        project / "final",
        project / "qa",
    ):
        directory.mkdir(parents=True, exist_ok=True)

    name = args.project_name or video.stem
    profile_style = profile.get("style_profile", {}) if profile else {}
    preset = str(profile_style.get("preset", args.preset))
    accent = str(profile_style.get("accent_color", args.accent))
    aspect = str(profile_style.get("aspect_ratio", args.aspect))
    motion_density = str(profile_style.get("motion_density", "balanced"))
    replacements = {
        "<project_name>": name,
        "<main_video>": str(video),
        "#2F7DF4": accent,
        "preserve source": aspect,
        "Preset: clean": f"Preset: {preset}",
        "Motion density: balanced": f"Motion density: {motion_density}",
    }
    created = []
    template_map = {
        templates / "EDIT_PLAN.template.md": project / "EDIT_PLAN.md",
        templates / "DESIGN.template.md": project / "DESIGN.md",
        templates / "VIDEO_LESSONS.template.md": project / "VIDEO_LESSONS.md",
        templates / "VIDEO_RETRO.template.md": project / "VIDEO_RETRO.md",
        templates / "QA_REPORT.template.md": project / "qa" / "QA_REPORT.md",
    }
    for source, destination in template_map.items():
        if write_template(source, destination, replacements):
            created.append(str(destination))

    profile_rules = profile.get("rules", []) if profile else []
    if profile_rules:
        write_profile_rules(project / "VIDEO_LESSONS.md", profile_rules)

    stage = detect_adopted_stage(project) if args.adopt_existing else "initialized"
    state = {
        "schema_version": SCHEMA_VERSION,
        "skill_version": skill_version,
        "project_name": name,
        "stage": stage,
        "main_video": str(video),
        "master_audio": "main_video",
        "source_probe": probe_video(video),
        "preview_required": True,
        "approval": {"status": "pending", "approved_at": None, "preview_url": None},
        "style_profile": {
            "setup_mode": args.mode,
            "preset": preset,
            "accent_color": accent,
            "aspect_ratio": aspect,
            "motion_density": motion_density,
            "safe_zones": ["face", "existing-captions", "screenshots", "product-ui"],
        },
        "profile": {
            "name": profile.get("profile_name", "default") if profile else None,
            "path": str(profile_path) if profile_path else None,
            "loaded": bool(profile),
            "rules_loaded": len(
                [item for item in profile_rules if item.get("active", True) and item.get("rule")]
            ),
        },
        "outputs": {},
        "last_error": None,
        "updated_at": now_iso(),
    }
    atomic_json_write(state_path, state)
    created.insert(0, str(state_path))

    print("Naive Video project initialized.")
    print(f"Project: {project}")
    print(f"Main video: {video}")
    print(f"Stage: {stage}")
    print(f"Profile: {profile_path if profile_path else 'project-only defaults'}")
    print("Created:")
    for item in created:
        print(f"  - {item}")
    if state["source_probe"].get("status") != "ok":
        print(f"WARNING: source probe {state['source_probe'].get('status')}: {state['source_probe'].get('reason')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
