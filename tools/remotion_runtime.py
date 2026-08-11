#!/usr/bin/env python3
"""Plan, check, or explicitly install an isolated project-local Remotion runtime."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_REMOTION_VERSION = "4.0.507"
DEFAULT_REACT_VERSION = "19.2.8"
RUNTIME_RELATIVE = Path("runtime/remotion")


def package_payload(remotion_version: str, react_version: str) -> dict[str, Any]:
    return {
        "name": "naive-video-remotion-runtime",
        "version": "1.0.0",
        "private": True,
        "scripts": {"remotion": "remotion"},
        "dependencies": {
            "@remotion/cli": remotion_version,
            "react": react_version,
            "react-dom": react_version,
            "remotion": remotion_version,
        },
    }


def command_version(command: str) -> str | None:
    executable = shutil.which(command)
    if not executable:
        return None
    result = subprocess.run(
        [executable, "--version"], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip().splitlines()[0] if result.stdout.strip() else "unknown"


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def installed_version(runtime: Path, package: str) -> str | None:
    parts = package.split("/")
    path = runtime / "node_modules"
    for part in parts:
        path /= part
    data = load_json(path / "package.json")
    value = data.get("version") if data else None
    return value if isinstance(value, str) else None


def runtime_status(runtime: Path, expected: dict[str, Any]) -> dict[str, Any]:
    package_path = runtime / "package.json"
    configured = load_json(package_path)
    expected_dependencies = expected["dependencies"]
    installed = {
        name: installed_version(runtime, name) for name in expected_dependencies
    }
    ready = bool(configured) and configured.get("dependencies") == expected_dependencies
    ready = ready and all(installed.get(name) == version for name, version in expected_dependencies.items())
    return {
        "runtime_dir": str(runtime),
        "package_json": str(package_path),
        "node": command_version("node"),
        "npm": command_version("npm"),
        "configured": configured is not None,
        "installed_versions": installed,
        "ready": ready,
    }


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


def print_result(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"Remotion runtime: {result['runtime_dir']}")
    print(f"Node: {result.get('node') or 'not found'}")
    print(f"npm: {result.get('npm') or 'not found'}")
    print(f"Configured: {result.get('configured', False)}")
    print(f"Ready: {result.get('ready', False)}")
    if result.get("install_command"):
        print("Install command:")
        print("  " + " ".join(result["install_command"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path, help="Existing video project directory")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true", help="Check without writing or networking")
    action.add_argument("--plan", action="store_true", help="Show the isolated install plan only")
    action.add_argument("--install", action="store_true", help="Install after explicit approval")
    parser.add_argument("--yes", action="store_true", help="Required explicit confirmation for --install")
    parser.add_argument("--remotion-version", default=DEFAULT_REMOTION_VERSION)
    parser.add_argument("--react-version", default=DEFAULT_REACT_VERSION)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    project = args.project.expanduser().resolve()
    if not project.is_dir():
        print(f"ERROR: project directory not found: {project}", file=sys.stderr)
        return 2
    runtime = project / RUNTIME_RELATIVE
    expected = package_payload(args.remotion_version, args.react_version)
    install_command = ["npm", "install", "--no-audit", "--no-fund"]

    if args.check:
        result = runtime_status(runtime, expected)
        print_result(result, args.json)
        return 0 if result["ready"] else 1

    if args.plan:
        result = runtime_status(runtime, expected)
        result.update(
            {
                "action": "plan-only",
                "will_write": False,
                "will_use_network": False,
                "expected_dependencies": expected["dependencies"],
                "install_command": install_command,
                "license_url": "https://www.remotion.dev/license",
            }
        )
        print_result(result, args.json)
        return 0

    if not args.yes:
        print(
            "ERROR: --install requires --yes after the user explicitly approves the "
            "project-local download and Remotion license review",
            file=sys.stderr,
        )
        return 2
    if not shutil.which("node") or not shutil.which("npm"):
        print("ERROR: Node.js and npm must already be available; this tool does not install them", file=sys.stderr)
        return 2

    runtime.mkdir(parents=True, exist_ok=True)
    package_path = runtime / "package.json"
    current = load_json(package_path)
    if current is not None and current != expected:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = runtime / f"package.json.backup-{timestamp}"
        shutil.copy2(package_path, backup)
        print(f"Backed up existing runtime package: {backup}")
    atomic_write(package_path, expected)

    result = subprocess.run(install_command, cwd=runtime, check=False)
    if result.returncode != 0:
        print(f"ERROR: npm install failed with exit code {result.returncode}", file=sys.stderr)
        return result.returncode or 1

    status = runtime_status(runtime, expected)
    status["action"] = "installed"
    status["license_url"] = "https://www.remotion.dev/license"
    print_result(status, args.json)
    return 0 if status["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
