#!/usr/bin/env python3
"""Validate an AI-RSE agentic workflow state file.

Uses only the Python standard library.  Checks that the JSON file
contains all mandatory fields, that types are correct, and that
critical human-approval gates are present.

Exit codes:
    0 — PASS
    1 — FAIL (validation errors found)
    2 — usage error (bad arguments or missing file)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# ── mandatory fields and their expected Python types ────────────────
REQUIRED_FIELDS: dict[str, type] = {
    "current_release": str,
    "current_phase": str,
    "track": str,
    "branch": str,
    "allowed_paths": list,
    "forbidden_paths": list,
    "forbidden_terms": list,
    "required_skills": list,
    "required_checks": list,
    "human_approval_required_for": list,
    "next_allowed_actions": list,
    "blocked_actions": list,
}

VALID_PHASES = frozenset(
    {
        "PLANNING",
        "RED",
        "GREEN",
        "REFACTOR",
        "DEMO",
        "AUDIT",
        "ACCEPTANCE_REVIEW",
        "DOCS_ONLY",
        "CLOSED",
    }
)

VALID_TRACKS = frozenset({"classical", "ai_for_science", "infrastructure"})

# Actions that *must always* require human approval.
MANDATORY_HUMAN_GATES = frozenset(
    {
        "merge_pr",
        "create_tag",
        "accept_adr",
        "change_pyproject",
        "change_policy",
        "add_dependency",
        "enable_poisson_runtime",
        "enable_physical_phi",
        "enable_solver_coupling",
        "enable_aifs_runtime",
    }
)


def _check_list_items_are_strings(
    data: dict, field: str, errors: list[str]
) -> None:
    """Ensure every item in *field* is a string."""
    for i, item in enumerate(data[field]):
        if not isinstance(item, str):
            errors.append(
                f"  {field}[{i}] must be a string, got {type(item).__name__}"
            )


def validate(path: Path) -> list[str]:
    """Return a list of validation error messages (empty → PASS)."""
    errors: list[str] = []

    # ── load JSON ───────────────────────────────────────────────────
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [f"File not found: {path}"]
    except OSError as exc:
        return [f"Cannot read {path}: {exc}"]

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["Top-level value must be a JSON object"]

    # ── required fields & types ─────────────────────────────────────
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            errors.append(f"  Missing required field: {field}")
        elif not isinstance(data[field], expected_type):
            errors.append(
                f"  Field '{field}' must be {expected_type.__name__}, "
                f"got {type(data[field]).__name__}"
            )

    # Early return if structural errors prevent deeper checks.
    if errors:
        return errors

    # ── enum checks ─────────────────────────────────────────────────
    if data["current_phase"] not in VALID_PHASES:
        errors.append(
            f"  current_phase '{data['current_phase']}' is not valid. "
            f"Must be one of: {sorted(VALID_PHASES)}"
        )

    if data["track"] not in VALID_TRACKS:
        errors.append(
            f"  track '{data['track']}' is not valid. "
            f"Must be one of: {sorted(VALID_TRACKS)}"
        )

    # ── list-item type checks ───────────────────────────────────────
    for field in REQUIRED_FIELDS:
        if REQUIRED_FIELDS[field] is list:
            _check_list_items_are_strings(data, field, errors)

    # ── mandatory human-approval gates ──────────────────────────────
    declared_gates = set(data["human_approval_required_for"])
    missing_gates = MANDATORY_HUMAN_GATES - declared_gates
    if missing_gates:
        errors.append(
            f"  human_approval_required_for is missing mandatory gates: "
            f"{sorted(missing_gates)}"
        )

    # ── blocked_actions must not overlap with next_allowed_actions ──
    allowed_set = set(data["next_allowed_actions"])
    blocked_set = set(data["blocked_actions"])
    overlap = allowed_set & blocked_set
    if overlap:
        errors.append(
            f"  next_allowed_actions and blocked_actions overlap: "
            f"{sorted(overlap)}"
        )

    # ── release version pattern ─────────────────────────────────────
    import re

    if not re.match(r"^v\d+\.\d+\.\d+$", data["current_release"]):
        errors.append(
            f"  current_release '{data['current_release']}' does not match "
            f"pattern vX.Y.Z"
        )

    return errors


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: validate_workflow_state.py <path-to-state.json>")
        sys.exit(2)

    state_path = Path(sys.argv[1])
    errors = validate(state_path)

    if errors:
        print(f"FAIL — {len(errors)} validation error(s) in {state_path}:")
        for err in errors:
            print(err)
        sys.exit(1)
    else:
        print(f"PASS — {state_path} is valid.")
        sys.exit(0)


if __name__ == "__main__":
    main()
