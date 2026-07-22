#!/usr/bin/env python3
"""Copy one skill directory without overwriting or deleting an existing target."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("destination")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    destination = Path(args.destination).expanduser()
    if not source.is_dir():
        print(f"ERROR: skill source is not a directory: {source}")
        return 2
    if destination.exists() or destination.is_symlink():
        print(f"ERROR: destination already exists: {destination}")
        return 2

    shutil.copytree(
        source,
        destination,
        symlinks=True,
        ignore=shutil.ignore_patterns(".git", ".DS_Store", "__pycache__", "*.pyc"),
    )
    print(f"Copied: {source} -> {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
