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

        plugin = node.get("plugin")
        fallback = node.get("fallback")
        if plugin and (not isinstance(fallback, str) or not fallback.strip()):
            errors.append(f"{prefix} names plugin {plugin!r} without a no-plugin fallback")

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
