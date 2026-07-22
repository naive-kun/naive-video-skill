#!/usr/bin/env python3
"""Inspect an offline GSAP distribution for video-composition use."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


VERSION_RE = re.compile(r"\b(?:GSAP|[A-Za-z][A-Za-z0-9]*(?:Plugin)?)\s+(\d+\.\d+\.\d+)\b")
CORE_NAMES = ("gsap.min.js", "gsap.js", "gsap-core.js")
PRODUCTION = (
    "SplitText.min.js",
    "Flip.min.js",
    "ScrambleTextPlugin.min.js",
    "DrawSVGPlugin.min.js",
    "MorphSVGPlugin.min.js",
    "MotionPathPlugin.min.js",
)
DEVELOPMENT = ("GSDevTools.min.js", "MotionPathHelper.min.js")
INTERACTION = (
    "ScrollTrigger.min.js",
    "ScrollSmoother.min.js",
    "Observer.min.js",
    "Draggable.min.js",
    "InertiaPlugin.min.js",
)


def first_match(files: dict[str, list[Path]], names: tuple[str, ...]) -> Path | None:
    for name in names:
        matches = files.get(name, [])
        if matches:
            return sorted(matches, key=lambda item: (len(item.parts), str(item)))[0]
    return None


def header(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:1600]
    except OSError:
        return ""


def version(path: Path) -> str | None:
    match = VERSION_RE.search(header(path))
    return match.group(1) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", help="Official GSAP package or project runtime directory")
    args = parser.parse_args()
    root = Path(args.directory).expanduser().resolve()

    if not root.is_dir():
        print(f"[BLOCKER] GSAP directory not found: {root}")
        return 2

    files: dict[str, list[Path]] = {}
    for path in root.rglob("*.js"):
        if path.is_file():
            files.setdefault(path.name, []).append(path)

    core = first_match(files, CORE_NAMES)
    if not core:
        print("[BLOCKER] GSAP core runtime not found (expected gsap.min.js, gsap.js, or gsap-core.js)")
        return 1

    selected = [core]
    for name in PRODUCTION + DEVELOPMENT + INTERACTION:
        match = first_match(files, (name,))
        if match:
            selected.append(match)

    versions = {str(path.relative_to(root)): version(path) for path in selected}
    known_versions = {item for item in versions.values() if item}
    missing_license_headers = [
        str(path.relative_to(root))
        for path in selected
        if "@license" not in header(path)
    ]

    print(f"[INFO] directory: {root}")
    print(f"[INFO] core: {core.relative_to(root)} ({version(core) or 'version unknown'})")
    print("[INFO] optional production plugins:")
    for name in PRODUCTION:
        match = first_match(files, (name,))
        print(f"  - {name}: {'available' if match else 'not found'}")
    present_development = [name for name in DEVELOPMENT if first_match(files, (name,))]
    present_interaction = [name for name in INTERACTION if first_match(files, (name,))]
    if present_development:
        print(f"[NOTE] development-only files present: {', '.join(present_development)}")
    if present_interaction:
        print(
            "[NOTE] page-interaction files present; normally exclude from fixed-time video: "
            + ", ".join(present_interaction)
        )
    if missing_license_headers:
        print("[WARNING] selected files without an @license header: " + ", ".join(missing_license_headers))
    if len(known_versions) > 1:
        details = ", ".join(f"{name}={value or 'unknown'}" for name, value in versions.items())
        print(f"[BLOCKER] mixed GSAP versions detected: {details}")
        return 1

    print("[PASS] GSAP runtime is usable. Copy only the project-required files and preserve license headers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
