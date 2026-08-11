#!/usr/bin/env python3
"""Deterministically validate a semantic GSAP motion plan."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


RECIPE_TAGS = {
    "impact-pop": {"number", "result", "question"},
    "stagger-list": {"list", "process"},
    "counter-roll": {"number"},
    "scan-verify": {"verify", "confirmation"},
    "connector-flow": {"process", "causality", "task-transfer"},
    "timeline-lock": {"timeline", "process"},
    "compare-split": {"compare"},
    "spotlight-mask": {"warning", "causality", "question"},
    "approval-stamp": {"confirmation", "result"},
    "warning-shake": {"warning"},
    "before-after-reveal": {"compare", "result"},
    "focus-frame": {"question", "verify", "compare"},
    "seekable-type": {"process", "result"},
    "split-reveal": {"list", "process", "result", "warning"},
    "glass-notification": {"warning", "confirmation", "result"},
}

TEXT_CUES = {
    "number": re.compile(r"\d|%|％|percent|倍|万|亿|秒|分钟", re.I),
    "list": re.compile(r"首先|其次|最后|第[一二三四五六七八九十]|步骤|一是|二是|first|second|step", re.I),
    "compare": re.compile(r"对比|相比|之前|之后|前后|但是|而是|更高|更低|versus|\bvs\b|before|after", re.I),
    "warning": re.compile(r"警告|风险|危险|不要|失败|错误|注意|warning|risk|danger|fail", re.I),
    "process": re.compile(r"流程|步骤|然后|接着|下一步|依次|workflow|process|then|next", re.I),
    "causality": re.compile(r"因为|所以|导致|因此|结果是|because|therefore|leads? to", re.I),
    "task-transfer": re.compile(r"交给|转交|分配|派给|流转|移交|hand[ -]?off|assign|route", re.I),
    "confirmation": re.compile(r"确认|批准|通过|同意|审核完成|confirm|approve|accepted|passed", re.I),
    "result": re.compile(r"结果|最终|完成|成功|产出|效果|result|finally|complete|success|outcome", re.I),
    "question": re.compile(r"[?？]|为什么|怎么|如何|是否|能不能|why|how|whether", re.I),
    "verify": re.compile(r"校验|验证|检查|扫描|核对|verify|validate|check|scan", re.I),
    "timeline": re.compile(r"时间轴|同步|锁定|对齐|音画|timeline|sync|align|locked", re.I),
}

GENERIC_VISUAL_ROLES = {"caption", "subtitle", "card", "corner-card"}
VALID_DENSITIES = {"restrained", "balanced", "energetic"}
REFERENCE_PROVIDER = "video-shotcraft"
REFERENCE_IMPLEMENTATIONS = {"gsap-adapted", "hyperframes-custom", "remotion-subclip"}


def energetic_minimum(duration: float) -> int:
    """Reach six nodes at 15s, then scale gently for longer timelines."""
    if duration <= 15:
        return max(2, math.ceil(duration / 2.5))
    return min(18, 6 + math.ceil((duration - 15) / 12))


def load_plan(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"plan not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ValueError("plan root must be a JSON object")
    return data


def load_reference_mapping() -> dict[str, dict[str, Any]]:
    path = Path(__file__).resolve().parents[1] / "references" / "shotcraft-mapping.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"ShotCraft mapping not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid ShotCraft mapping at line {exc.lineno}: {exc.msg}") from exc
    if not isinstance(data, dict) or data.get("provider") != REFERENCE_PROVIDER:
        raise ValueError("ShotCraft mapping has an invalid provider")
    cards = data.get("cards")
    if not isinstance(cards, list):
        raise ValueError("ShotCraft mapping cards must be an array")
    return {
        card["card"]: card
        for card in cards
        if isinstance(card, dict) and isinstance(card.get("card"), str)
    }


def number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def validate(plan: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    duration = number(plan.get("timeline_duration"))
    density = plan.get("motion_density")
    nodes = plan.get("nodes")
    protected = set(plan.get("protected_regions", []))
    content_logic_path = plan.get("content_logic_path")

    try:
        reference_mapping = load_reference_mapping()
    except ValueError as exc:
        errors.append(str(exc))
        reference_mapping = {}

    if duration is None or duration <= 0:
        errors.append("timeline_duration must be a positive number")
        duration = 0.0
    if density not in VALID_DENSITIES:
        errors.append("motion_density must be restrained, balanced, or energetic")
    if not isinstance(nodes, list):
        errors.append("nodes must be an array")
        nodes = []
    if not isinstance(plan.get("protected_regions", []), list):
        errors.append("protected_regions must be an array")
        protected = set()

    evidence_intervals: list[tuple[float, float, str]] = []
    raw_evidence_intervals = plan.get("evidence_intervals", [])
    if not isinstance(raw_evidence_intervals, list):
        errors.append("evidence_intervals must be an array")
    else:
        for index, interval in enumerate(raw_evidence_intervals, start=1):
            prefix = f"evidence_interval[{index}]"
            if not isinstance(interval, dict):
                errors.append(f"{prefix} must be an object")
                continue
            interval_start = number(interval.get("start"))
            interval_end = number(interval.get("end"))
            kind = interval.get("kind", "evidence")
            if interval_start is None or interval_end is None or interval_start < 0 or interval_end <= interval_start:
                errors.append(f"{prefix} needs a valid start/end")
                continue
            if duration and interval_end > duration + 0.001:
                errors.append(f"{prefix} exceeds timeline duration {duration}")
                continue
            if not isinstance(kind, str) or not kind.strip():
                errors.append(f"{prefix} kind must be a non-empty string")
                continue
            evidence_intervals.append((interval_start, interval_end, kind.strip()))

    node_ids: set[str] = set()
    visual_roles: set[str] = set()
    semantic_nodes = 0

    for index, node in enumerate(nodes, start=1):
        prefix = f"node[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{prefix} must be an object")
            continue

        node_id = node.get("node_id")
        if not isinstance(node_id, str) or not node_id.strip():
            errors.append(f"{prefix} is missing node_id")
        elif node_id in node_ids:
            errors.append(f"{prefix} duplicates node_id {node_id!r}")
        else:
            node_ids.add(node_id)

        recipe_id = node.get("recipe_id")
        semantic_tag = node.get("semantic_tag")
        if recipe_id not in RECIPE_TAGS:
            errors.append(f"{prefix} has unknown or missing recipe_id {recipe_id!r}")
        if not isinstance(semantic_tag, str) or not semantic_tag:
            errors.append(f"{prefix} is missing semantic_tag")
        elif recipe_id in RECIPE_TAGS and semantic_tag not in RECIPE_TAGS[recipe_id]:
            allowed = ", ".join(sorted(RECIPE_TAGS[recipe_id]))
            errors.append(f"{prefix} recipe {recipe_id!r} does not support semantic tag {semantic_tag!r}; allowed: {allowed}")

        start = number(node.get("start"))
        end = number(node.get("end"))
        if start is None or end is None:
            errors.append(f"{prefix} must have numeric start and end")
        elif start < 0 or end <= start or (duration and end > duration + 0.001):
            errors.append(f"{prefix} has invalid range {start}-{end} for timeline {duration}")

        evidence = node.get("semantic_evidence")
        if not isinstance(evidence, dict):
            errors.append(f"{prefix} is missing semantic_evidence")
        else:
            evidence_start = number(evidence.get("start"))
            evidence_end = number(evidence.get("end"))
            text = evidence.get("text")
            intent = evidence.get("intent")
            if evidence_start is None or evidence_end is None or evidence_end <= evidence_start:
                errors.append(f"{prefix} semantic_evidence needs a valid start/end")
            elif start is not None and end is not None and (end <= evidence_start or start >= evidence_end):
                errors.append(f"{prefix} does not overlap its caption evidence")
            if intent != semantic_tag:
                errors.append(f"{prefix} semantic_evidence.intent must equal semantic_tag")
            if not isinstance(text, str) or not text.strip():
                errors.append(f"{prefix} semantic_evidence.text must be non-empty")
            elif semantic_tag in TEXT_CUES and not TEXT_CUES[semantic_tag].search(text):
                warnings.append(f"{prefix} text heuristic could not confirm semantic tag {semantic_tag!r}; review manually")
            else:
                semantic_nodes += 1

        region = node.get("region")
        if not isinstance(region, str) or not region.strip():
            errors.append(f"{prefix} is missing region")
        elif region in protected:
            errors.append(f"{prefix} region {region!r} is protected")
        if node.get("covers_protected_regions") is not False:
            errors.append(f"{prefix} must explicitly set covers_protected_regions to false")

        visual_role = node.get("visual_role")
        if not isinstance(visual_role, str) or not visual_role.strip():
            errors.append(f"{prefix} is missing visual_role")
        else:
            visual_roles.add(visual_role.strip().lower())

        if content_logic_path:
            if not isinstance(node.get("logic_group_id"), str) or not node["logic_group_id"].strip():
                errors.append(f"{prefix} must record logic_group_id when content_logic_path is set")
            if not isinstance(node.get("logic_beat_id"), str) or not node["logic_beat_id"].strip():
                errors.append(f"{prefix} must record logic_beat_id when content_logic_path is set")

        plugin = node.get("plugin")
        fallback = node.get("fallback")
        if plugin and (not isinstance(fallback, str) or not fallback.strip()):
            errors.append(f"{prefix} names plugin {plugin!r} without a no-plugin fallback")

        reference = node.get("reference")
        if reference is not None:
            if not isinstance(reference, dict):
                errors.append(f"{prefix} reference must be an object or null")
                continue

            if not isinstance(fallback, str) or not fallback.strip():
                errors.append(f"{prefix} ShotCraft reference requires a non-empty native fallback")

            provider = reference.get("provider")
            card_name = reference.get("card")
            implementation = reference.get("implementation")
            runtime_required = reference.get("provider_required_at_runtime")
            if provider != REFERENCE_PROVIDER:
                errors.append(f"{prefix} reference.provider must be {REFERENCE_PROVIDER!r}")
            if not isinstance(card_name, str) or not card_name.strip():
                errors.append(f"{prefix} reference.card must be a non-empty string")
                mapped_card = None
            else:
                mapped_card = reference_mapping.get(card_name)
                if mapped_card is None:
                    errors.append(f"{prefix} references unknown ShotCraft card {card_name!r}")
            if implementation not in REFERENCE_IMPLEMENTATIONS:
                errors.append(
                    f"{prefix} reference.implementation must be gsap-adapted, "
                    "hyperframes-custom, or remotion-subclip"
                )
            if not isinstance(runtime_required, bool):
                errors.append(f"{prefix} reference.provider_required_at_runtime must be boolean")
            elif runtime_required:
                errors.append(f"{prefix} must remain previewable without the ShotCraft provider at runtime")

            if mapped_card is not None:
                if recipe_id not in mapped_card.get("native_recipe_ids", []):
                    errors.append(
                        f"{prefix} ShotCraft card {card_name!r} is incompatible with recipe {recipe_id!r}"
                    )
                if semantic_tag not in mapped_card.get("semantic_tags", []):
                    errors.append(
                        f"{prefix} ShotCraft card {card_name!r} is incompatible with semantic tag {semantic_tag!r}"
                    )
                if density not in mapped_card.get("densities", []):
                    errors.append(
                        f"{prefix} ShotCraft card {card_name!r} is not allowed for motion density {density!r}"
                    )
                recommended_duration = mapped_card.get("recommended_duration")
                if (
                    start is not None
                    and end is not None
                    and isinstance(recommended_duration, list)
                    and len(recommended_duration) == 2
                ):
                    node_duration = end - start
                    if node_duration < recommended_duration[0] or node_duration > recommended_duration[1]:
                        warnings.append(
                            f"{prefix} duration {node_duration:.2f}s is outside the mapped ShotCraft "
                            f"range {recommended_duration[0]}-{recommended_duration[1]}s"
                        )
                default_implementation = mapped_card.get("implementation")
                if implementation != default_implementation:
                    if implementation == "remotion-subclip" and reference.get("explicit_approval") is True:
                        warnings.append(
                            f"{prefix} uses approved remotion-subclip; pre-render it muted and keep the native fallback"
                        )
                    else:
                        errors.append(
                            f"{prefix} implementation {implementation!r} differs from mapped default "
                            f"{default_implementation!r}; remotion-subclip requires explicit_approval=true"
                        )

                if mapped_card.get("allow_during_evidence") is False:
                    if node.get("evidence_interval") is True:
                        errors.append(f"{prefix} ShotCraft reference is not allowed during evidence")
                    if start is not None and end is not None:
                        for evidence_start, evidence_end, kind in evidence_intervals:
                            if end > evidence_start and start < evidence_end:
                                errors.append(
                                    f"{prefix} ShotCraft reference overlaps protected {kind} evidence "
                                    f"at {evidence_start}-{evidence_end}"
                                )
                                break

    if density == "energetic" and duration:
        minimum = energetic_minimum(duration)
        if len(nodes) < minimum:
            errors.append(f"energetic plan has {len(nodes)} nodes; duration {duration:.2f}s requires at least {minimum}")
        if not visual_roles or visual_roles.issubset(GENERIC_VISUAL_ROLES):
            errors.append("energetic plan degenerates into subtitles/cards only; add independent semantic visual roles")
        if semantic_nodes < min(len(nodes), minimum):
            warnings.append("some energetic nodes need manual review because caption text did not confirm their declared intent")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="Path to MOTION_PLAN.json")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    args = parser.parse_args()

    try:
        plan = load_plan(args.plan)
        errors, warnings = validate(plan)
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
        print(f"Motion plan check: {'PASS' if not errors else 'FAIL'} ({len(errors)} errors, {len(warnings)} warnings)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
