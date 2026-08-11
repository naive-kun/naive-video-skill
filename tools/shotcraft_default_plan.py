#!/usr/bin/env python3
"""Apply the curated ShotCraft-inspired default pack to a native motion plan."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


PROVIDER = "video-shotcraft"
VALID_DENSITIES = {"restrained", "balanced", "energetic"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path} at line {exc.lineno}: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def load_mapping() -> dict[str, Any]:
    path = Path(__file__).resolve().parents[1] / "references" / "shotcraft-mapping.json"
    data = load_json(path)
    if data.get("provider") != PROVIDER:
        raise ValueError("ShotCraft mapping has an invalid provider")
    if not isinstance(data.get("cards"), list) or not isinstance(data.get("default_pack"), dict):
        raise ValueError("ShotCraft mapping needs cards and default_pack")
    return data


def number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def overlaps(start: float, end: float, intervals: list[tuple[float, float]]) -> bool:
    return any(end > interval_start and start < interval_end for interval_start, interval_end in intervals)


def evidence_intervals(plan: dict[str, Any]) -> list[tuple[float, float]]:
    result: list[tuple[float, float]] = []
    for interval in plan.get("evidence_intervals", []):
        if not isinstance(interval, dict):
            continue
        start = number(interval.get("start"))
        end = number(interval.get("end"))
        if start is not None and end is not None and end > start:
            result.append((start, end))
    return result


def apply_defaults(
    plan: dict[str, Any], mapping: dict[str, Any], max_references: int | None
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    density = plan.get("motion_density")
    if density not in VALID_DENSITIES:
        raise ValueError("motion_density must be restrained, balanced, or energetic")
    nodes = plan.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError("motion plan nodes must be an array")

    pack = mapping["default_pack"]
    limits = pack.get("max_references_by_density", {})
    limit = max_references if max_references is not None else limits.get(density)
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        raise ValueError(f"invalid default-pack limit for density {density!r}")

    default_names = pack.get("cards", [])
    card_order = {name: index for index, name in enumerate(default_names)}
    cards = [
        card
        for card in mapping["cards"]
        if isinstance(card, dict) and card.get("card") in card_order
    ]
    cards.sort(key=lambda card: card_order[card["card"]])

    used_cards: set[str] = set()
    existing_count = 0
    for node in nodes:
        if not isinstance(node, dict):
            continue
        reference = node.get("reference")
        if isinstance(reference, dict) and reference.get("provider") == PROVIDER:
            existing_count += 1
            if isinstance(reference.get("card"), str):
                used_cards.add(reference["card"])

    remaining = max(0, limit - existing_count)
    intervals = evidence_intervals(plan)
    applied: list[dict[str, str]] = []

    for node in nodes:
        if remaining <= 0:
            break
        if not isinstance(node, dict) or node.get("reference") is not None:
            continue
        if node.get("covers_protected_regions") is not False or node.get("evidence_interval") is True:
            continue
        start = number(node.get("start"))
        end = number(node.get("end"))
        if start is None or end is None or end <= start or overlaps(start, end, intervals):
            continue
        semantic_tag = node.get("semantic_tag")
        recipe_id = node.get("recipe_id")
        fallback = node.get("fallback")
        if not isinstance(fallback, str) or not fallback.strip():
            continue

        selected = None
        for card in cards:
            name = card.get("card")
            if name in used_cards:
                continue
            if density not in card.get("densities", []):
                continue
            if semantic_tag not in card.get("semantic_tags", []):
                continue
            if recipe_id not in card.get("native_recipe_ids", []):
                continue
            recommended_duration = card.get("recommended_duration")
            if (
                not isinstance(recommended_duration, list)
                or len(recommended_duration) != 2
                or end - start < recommended_duration[0]
                or end - start > recommended_duration[1]
            ):
                continue
            selected = card
            break
        if selected is None:
            continue

        card_name = selected["card"]
        node["reference"] = {
            "provider": PROVIDER,
            "card": card_name,
            "implementation": selected["implementation"],
            "provider_required_at_runtime": False,
            "selection_mode": "automatic-default-pack",
        }
        used_cards.add(card_name)
        remaining -= 1
        applied.append(
            {
                "node_id": str(node.get("node_id", "")),
                "card": card_name,
                "recipe_id": str(recipe_id),
                "semantic_tag": str(semantic_tag),
            }
        )

    return plan, applied


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Path to MOTION_PLAN.json")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("--in-place", action="store_true", help="Update the plan atomically")
    destination.add_argument("--output", type=Path, help="Write the enriched plan to another path")
    parser.add_argument("--max-references", type=int, help="Override the density-aware cap")
    parser.add_argument("--json-summary", action="store_true", help="Emit a machine-readable summary")
    args = parser.parse_args()

    plan_path = args.plan.expanduser().resolve()
    try:
        plan = load_json(plan_path)
        enriched, applied = apply_defaults(plan, load_mapping(), args.max_references)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    output_path = None
    if args.in_place:
        output_path = plan_path
    elif args.output:
        output_path = args.output.expanduser().resolve()

    if output_path:
        atomic_write(output_path, enriched)
    elif not args.json_summary:
        print(json.dumps(enriched, ensure_ascii=False, indent=2))

    summary = {
        "ok": True,
        "changed": len(applied),
        "output": str(output_path) if output_path else None,
        "applied": applied,
    }
    if args.json_summary:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    elif output_path:
        print(f"Applied {len(applied)} curated reference(s) to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
