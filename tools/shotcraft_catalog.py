#!/usr/bin/env python3
"""Discover optional ShotCraft cards and query the local semantic mapping."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


PROVIDER = "video-shotcraft"
LIBRARY_RELATIVE = Path("gallery/api/library.json")
VALID_DENSITIES = {"restrained", "balanced", "energetic"}
IDENTIFIER_KEYS = {"card", "id", "name", "slug"}


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path} at line {exc.lineno}: {exc.msg}") from exc


def load_mapping() -> dict[str, Any]:
    path = skill_root() / "references" / "shotcraft-mapping.json"
    data = load_json(path)
    if not isinstance(data, dict) or data.get("provider") != PROVIDER:
        raise ValueError(f"invalid ShotCraft mapping: {path}")
    if not isinstance(data.get("cards"), list):
        raise ValueError("ShotCraft mapping cards must be an array")
    return data


def candidate_roots(explicit: Path | None) -> list[Path]:
    if explicit is not None:
        return [explicit.expanduser()]

    roots: list[Path] = []
    env_root = os.environ.get("VIDEO_SHOTCRAFT_HOME")
    if env_root:
        roots.append(Path(env_root).expanduser())

    home = Path.home()
    roots.extend(
        [
            home / ".naive-video/providers/video-shotcraft",
            home / ".codex/skills/video-shotcraft",
            home / ".claude/skills/video-shotcraft",
            home / ".agents/skills/video-shotcraft",
        ]
    )
    return roots


def discover_provider(explicit: Path | None) -> tuple[Path | None, Path | None]:
    for root in candidate_roots(explicit):
        library = root / LIBRARY_RELATIVE
        if library.is_file():
            return root.resolve(), library.resolve()
    return None, None


def collect_identifiers(value: Any) -> set[str]:
    identifiers: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in IDENTIFIER_KEYS and isinstance(item, str) and item.strip():
                identifiers.add(item.strip())
            identifiers.update(collect_identifiers(item))
    elif isinstance(value, list):
        for item in value:
            identifiers.update(collect_identifiers(item))
    return identifiers


def select_cards(
    mapping: dict[str, Any],
    semantic: str | None,
    density: str | None,
    card_name: str | None,
    defaults_only: bool,
) -> list[dict[str, Any]]:
    default_cards = mapping.get("default_pack", {}).get("cards", [])
    default_order = {
        name: index for index, name in enumerate(default_cards) if isinstance(name, str)
    }
    selected: list[dict[str, Any]] = []
    for card in mapping["cards"]:
        if not isinstance(card, dict):
            continue
        if defaults_only and card.get("card") not in default_order:
            continue
        if card_name and card.get("card") != card_name:
            continue
        if semantic and semantic not in card.get("semantic_tags", []):
            continue
        if density and density not in card.get("densities", []):
            continue
        selected.append(dict(card))
    if defaults_only:
        return sorted(
            selected,
            key=lambda item: (
                default_order.get(item.get("card"), 9999),
                item.get("priority", 9999),
                item.get("card", ""),
            ),
        )
    return sorted(selected, key=lambda item: (item.get("priority", 9999), item.get("card", "")))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--semantic", help="Semantic tag such as list, number, verify, or process")
    parser.add_argument("--density", choices=sorted(VALID_DENSITIES))
    parser.add_argument("--card", help="Exact ShotCraft card name")
    parser.add_argument(
        "--defaults",
        action="store_true",
        help="List only cards in the curated beginner default pack",
    )
    parser.add_argument("--root", type=Path, help="Existing local video-shotcraft repository")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    parser.add_argument(
        "--require-installed",
        action="store_true",
        help="Fail unless the selected cards are present in a discovered local library",
    )
    args = parser.parse_args()

    try:
        mapping = load_mapping()
        provider_root, library_path = discover_provider(args.root)
        installed_cards: set[str] = set()
        if library_path:
            installed_cards = collect_identifiers(load_json(library_path))
        selected = select_cards(mapping, args.semantic, args.density, args.card, args.defaults)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for item in selected:
        if library_path is None:
            item["availability"] = "reference-only"
        elif item["card"] in installed_cards:
            item["availability"] = "installed"
        else:
            item["availability"] = "missing"

    result = {
        "provider": PROVIDER,
        "provider_url": mapping.get("provider_url"),
        "mapping_schema_version": mapping.get("schema_version"),
        "provider_root": str(provider_root) if provider_root else None,
        "library_path": str(library_path) if library_path else None,
        "filters": {
            "semantic": args.semantic,
            "density": args.density,
            "card": args.card,
            "defaults": args.defaults,
        },
        "default_pack": mapping.get("default_pack"),
        "cards": selected,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        state = "installed" if library_path else "not installed; reference mapping only"
        print(f"ShotCraft provider: {state}")
        for item in selected:
            print(
                f"- {item['card']}: {item['implementation']} "
                f"[{item['availability']}] -> {', '.join(item['native_recipe_ids'])}"
            )

    if not selected:
        print("No ShotCraft mapping matched the requested filters.", file=sys.stderr)
        return 1
    if args.require_installed and any(item["availability"] != "installed" for item in selected):
        print("ERROR: one or more selected cards are not installed locally", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
