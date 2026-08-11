#!/usr/bin/env python3
"""Validate viewer-facing content logic groups before motion authoring."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


VALID_PRECISION = {"word-level", "cue-level", "manual"}
VALID_ROLES = {"input", "support", "relation", "warning", "result", "cta"}


def number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def load(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"content logic file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError("content logic root must be an object")
    return payload


def validate(payload: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    duration = number(payload.get("timeline_duration"))
    precision = payload.get("timing_precision")
    groups = payload.get("groups")

    if payload.get("status") != "ready":
        errors.append("status must be 'ready' before design approval")
    if duration is None or duration <= 0:
        errors.append("timeline_duration must be a positive number")
        duration = 0.0
    if not isinstance(payload.get("timing_source"), str) or not payload.get("timing_source", "").strip():
        errors.append("timing_source must be non-empty")
    if precision not in VALID_PRECISION:
        errors.append("timing_precision must be word-level, cue-level, or manual")
    if not isinstance(groups, list) or not groups:
        errors.append("groups must be a non-empty array")
        groups = []

    group_ids: set[str] = set()
    previous_end = -1.0
    for index, group in enumerate(groups, start=1):
        prefix = f"group[{index}]"
        if not isinstance(group, dict):
            errors.append(f"{prefix} must be an object")
            continue
        group_id = group.get("group_id")
        if not isinstance(group_id, str) or not group_id.strip():
            errors.append(f"{prefix} is missing group_id")
        elif group_id in group_ids:
            errors.append(f"{prefix} duplicates group_id {group_id!r}")
        else:
            group_ids.add(group_id)

        start = number(group.get("start"))
        end = number(group.get("end"))
        if start is None or end is None or start < 0 or end <= start or (duration and end > duration + 0.001):
            errors.append(f"{prefix} has an invalid start/end range")
        elif start < previous_end - 0.001:
            errors.append(f"{prefix} overlaps the previous logic group")
        else:
            previous_end = end

        for field in ("viewer_question", "takeaway"):
            if not isinstance(group.get(field), str) or not group[field].strip():
                errors.append(f"{prefix}.{field} must be non-empty")

        evidence = group.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{prefix}.evidence must be a non-empty array")
        else:
            for evidence_index, item in enumerate(evidence, start=1):
                item_prefix = f"{prefix}.evidence[{evidence_index}]"
                if not isinstance(item, dict):
                    errors.append(f"{item_prefix} must be an object")
                    continue
                evidence_start = number(item.get("start"))
                evidence_end = number(item.get("end"))
                if evidence_start is None or evidence_end is None or evidence_end <= evidence_start:
                    errors.append(f"{item_prefix} needs valid start/end")
                elif start is not None and end is not None and (evidence_start < start - 0.001 or evidence_end > end + 0.001):
                    errors.append(f"{item_prefix} falls outside its logic group")
                if not isinstance(item.get("text"), str) or not item["text"].strip():
                    errors.append(f"{item_prefix}.text must be non-empty")

        beats = group.get("beats")
        if not isinstance(beats, list) or not beats:
            errors.append(f"{prefix}.beats must be a non-empty array")
            continue
        beat_ids: set[str] = set()
        has_result = False
        for beat_index, beat in enumerate(beats, start=1):
            beat_prefix = f"{prefix}.beats[{beat_index}]"
            if not isinstance(beat, dict):
                errors.append(f"{beat_prefix} must be an object")
                continue
            beat_id = beat.get("beat_id")
            if not isinstance(beat_id, str) or not beat_id.strip():
                errors.append(f"{beat_prefix} is missing beat_id")
            elif beat_id in beat_ids:
                errors.append(f"{beat_prefix} duplicates beat_id {beat_id!r}")
            else:
                beat_ids.add(beat_id)
            role = beat.get("role")
            if role not in VALID_ROLES:
                errors.append(f"{beat_prefix}.role must be one of {', '.join(sorted(VALID_ROLES))}")
            has_result = has_result or role in {"result", "cta"}
            beat_start = number(beat.get("start"))
            beat_end = number(beat.get("end"))
            if beat_start is None or beat_end is None or beat_end <= beat_start:
                errors.append(f"{beat_prefix} needs valid start/end")
            elif start is not None and end is not None and (beat_start < start - 0.001 or beat_end > end + 0.001):
                errors.append(f"{beat_prefix} falls outside its logic group")
            if not isinstance(beat.get("text"), str) or not beat["text"].strip():
                errors.append(f"{beat_prefix}.text must be non-empty")
            if beat.get("keep_visible_until_group_end") not in {True, False}:
                errors.append(f"{beat_prefix}.keep_visible_until_group_end must be boolean")
        if not has_result:
            warnings.append(f"{prefix} has no result or CTA beat; confirm that the group still resolves")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        errors, warnings = validate(load(args.path))
    except ValueError as exc:
        errors, warnings = [str(exc)], []
    result = {"ok": not errors, "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for warning in warnings:
            print(f"WARN: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Content logic check: {'PASS' if not errors else 'FAIL'} ({len(errors)} errors, {len(warnings)} warnings)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
