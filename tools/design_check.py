#!/usr/bin/env python3
"""Validate the brand-neutral DESIGN.md visual-quality contract."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = {
    "Profile",
    "Typography",
    "Captions",
    "Components",
    "Safe Zones",
    "Motion",
    "Do Not",
}

REQUIRED_FIELDS = {
    "Typography": ("Font family", "Display weight", "Body weight", "Text transform"),
    "Captions": ("Maximum lines", "Wrap policy"),
    "Components": ("Primary family", "Notification family", "Maximum simultaneous components"),
    "Motion": ("Timeline driver", "Font measurement"),
}

WEIGHT_WORDS = {"semibold": 600, "demibold": 600, "bold": 700, "extrabold": 800, "black": 900}


def parse_design(text: str) -> tuple[set[str], dict[str, dict[str, str]]]:
    sections: set[str] = set()
    fields: dict[str, dict[str, str]] = {}
    current = ""
    for raw in text.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", raw)
        if heading:
            current = heading.group(1).strip()
            sections.add(current)
            fields.setdefault(current, {})
            continue
        field = re.match(r"^-\s+([^:]+):\s*(.*?)\s*$", raw)
        if field and current:
            fields[current][field.group(1).strip()] = field.group(2).strip()
    return sections, fields


def numeric_weight(value: str) -> int | None:
    match = re.search(r"\b([1-9]00)\b", value)
    if match:
        return int(match.group(1))
    lowered = re.sub(r"[^a-z]", "", value.lower())
    for word, weight in WEIGHT_WORDS.items():
        if word in lowered:
            return weight
    return None


def positive_int(value: str) -> int | None:
    match = re.search(r"\b(\d+)\b", value)
    return int(match.group(1)) if match else None


def validate(path: Path) -> list[str]:
    if not path.exists():
        return [f"design file not found: {path}"]
    sections, fields = parse_design(path.read_text(encoding="utf-8"))
    errors = [f"missing section: {name}" for name in sorted(REQUIRED_SECTIONS - sections)]

    for section, names in REQUIRED_FIELDS.items():
        values = fields.get(section, {})
        for name in names:
            value = values.get(name, "")
            if not value or value.lower() in {"auto", "default", "unspecified", "tbd"}:
                errors.append(f"{section}.{name} must be explicit")

    typography = fields.get("Typography", {})
    display_weight = numeric_weight(typography.get("Display weight", ""))
    if display_weight is not None and display_weight < 600:
        errors.append("Typography.Display weight must be a real semibold or heavier face")

    transform = typography.get("Text transform", "").lower()
    if transform and not any(token in transform for token in ("level", "no rotation", "no skew", "none")):
        errors.append("Typography.Text transform must keep readable text level and unskewed")

    captions = fields.get("Captions", {})
    maximum_lines = positive_int(captions.get("Maximum lines", ""))
    if maximum_lines is not None and maximum_lines not in {1, 2}:
        errors.append("Captions.Maximum lines must be 1 or 2")

    components = fields.get("Components", {})
    maximum_components = positive_int(components.get("Maximum simultaneous components", ""))
    if maximum_components is not None and maximum_components < 1:
        errors.append("Components.Maximum simultaneous components must be positive")

    motion = fields.get("Motion", {})
    driver = motion.get("Timeline driver", "").lower()
    if driver and ("gsap" not in driver or not any(token in driver for token in ("seekable", "paused"))):
        errors.append("Motion.Timeline driver must name a paused or seekable GSAP timeline")

    font_measurement = motion.get("Font measurement", "").lower()
    if font_measurement and not any(token in font_measurement for token in ("document.fonts.ready", "after fonts load", "fonts loaded")):
        errors.append("Motion.Font measurement must occur after fonts load")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("design", type=Path, help="Path to DESIGN.md")
    args = parser.parse_args()
    errors = validate(args.design)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Design check: {'PASS' if not errors else 'FAIL'} ({len(errors)} errors)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
