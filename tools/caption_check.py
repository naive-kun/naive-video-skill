#!/usr/bin/env python3
"""Validate SRT timing and optionally compare it with a caption CSV."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TIMESTAMP = re.compile(r"^(\d{2}):(\d{2}):(\d{2})[,.](\d{3})$")


@dataclass
class Cue:
    index: int
    start: float
    end: float
    text: str


def to_seconds(value: str) -> float:
    value = value.strip()
    match = TIMESTAMP.match(value)
    if match:
        hours, minutes, seconds, millis = (int(part) for part in match.groups())
        return hours * 3600 + minutes * 60 + seconds + millis / 1000
    return float(value)


def parse_srt(path: Path) -> list[Cue]:
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    blocks = re.split(r"\n\s*\n", raw.strip()) if raw.strip() else []
    cues: list[Cue] = []
    for position, block in enumerate(blocks, start=1):
        lines = [line.rstrip() for line in block.splitlines()]
        if len(lines) < 2:
            raise ValueError(f"block {position} is incomplete")
        try:
            index = int(lines[0].strip())
            timing = lines[1]
        except ValueError:
            index = position
            timing = lines[0]
            lines = [str(index)] + lines
        if "-->" not in timing:
            raise ValueError(f"cue {index} has no '-->' timing line")
        start_text, end_text = (part.strip().split()[0] for part in timing.split("-->", 1))
        start = to_seconds(start_text)
        end = to_seconds(end_text)
        text = "\n".join(lines[2:]).strip()
        cues.append(Cue(index=index, start=start, end=end, text=text))
    return cues


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header")
        return list(reader)


def pick(row: dict[str, str], names: tuple[str, ...]) -> str | None:
    lowered = {key.lower().strip(): value for key, value in row.items() if key is not None}
    for name in names:
        if name in lowered:
            return lowered[name]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("srt")
    parser.add_argument("csv", nargs="?")
    args = parser.parse_args()

    srt_path = Path(args.srt).expanduser()
    if not srt_path.exists():
        print(f"ERROR: SRT not found: {srt_path}")
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    try:
        cues = parse_srt(srt_path)
    except (ValueError, OSError) as exc:
        print(f"ERROR: cannot parse SRT: {exc}")
        return 2

    if not cues:
        errors.append("SRT contains no cues")

    durations = []
    previous_end = -1.0
    for cue in cues:
        duration = cue.end - cue.start
        durations.append(duration)
        if duration <= 0:
            errors.append(f"cue {cue.index} has non-positive duration")
        elif duration < 0.30:
            warnings.append(f"cue {cue.index} is very short ({duration:.3f}s)")
        if cue.start + 0.001 < previous_end:
            errors.append(f"cue {cue.index} overlaps the previous cue")
        if not cue.text:
            warnings.append(f"cue {cue.index} has empty text")
        previous_end = max(previous_end, cue.end)

    if args.csv:
        csv_path = Path(args.csv).expanduser()
        if not csv_path.exists():
            errors.append(f"CSV not found: {csv_path}")
        else:
            try:
                rows = load_csv(csv_path)
                if len(rows) != len(cues):
                    errors.append(f"cue count mismatch: SRT={len(cues)}, CSV={len(rows)}")
                for position, (cue, row) in enumerate(zip(cues, rows), start=1):
                    csv_text = pick(row, ("text", "caption", "subtitle", "字幕", "文案"))
                    if csv_text is not None and normalize(csv_text) != normalize(cue.text):
                        errors.append(f"text mismatch at row {position}")
                    csv_start = pick(row, ("start", "start_time", "开始", "开始时间"))
                    csv_end = pick(row, ("end", "end_time", "结束", "结束时间"))
                    if csv_start and abs(to_seconds(csv_start) - cue.start) > 0.02:
                        errors.append(f"start mismatch at row {position}")
                    if csv_end and abs(to_seconds(csv_end) - cue.end) > 0.02:
                        errors.append(f"end mismatch at row {position}")
            except (ValueError, OSError) as exc:
                errors.append(f"cannot parse CSV: {exc}")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    if cues:
        positive = [duration for duration in durations if duration > 0]
        shortest = min(positive) if positive else 0.0
        longest = max(positive) if positive else 0.0
        print(f"Cues: {len(cues)}")
        print(f"Duration range: {shortest:.3f}s to {longest:.3f}s")
    print(f"Result: {'FAIL' if errors else 'PASS'} ({len(errors)} errors, {len(warnings)} warnings)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
