#!/usr/bin/env python3
"""Validate BudgetOps limits for the AI-RSE agentic workflow.

Uses only the Python standard library.  Reads both the workflow state
file and the budget limits file, then checks that budget guardrails
are present, conservative, and require human approval for escalation.

Exit codes:
    0 — PASS
    1 — FAIL (budget violations found)
    2 — usage error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def validate_budget(state: dict, budget: dict) -> list[str]:
    """Return a list of budget validation error messages."""
    errors: list[str] = []

    # ── state-level budget section ──────────────────────────────────
    if "budget" not in state:
        errors.append("  State file missing 'budget' section.")
        return errors

    sb = state["budget"]

    # external_paid_api_allowed must be false by default
    if sb.get("external_paid_api_allowed") is not False:
        errors.append("  budget.external_paid_api_allowed must be false by default.")

    # max_total_estimated_cost_brl must exist and be >= 0
    cost = sb.get("max_total_estimated_cost_brl")
    if cost is None or not isinstance(cost, (int, float)) or cost < 0:
        errors.append("  budget.max_total_estimated_cost_brl must exist and be >= 0.")

    # max_llm_calls_per_goal must exist and be >= 0
    llm = sb.get("max_llm_calls_per_goal")
    if llm is None or not isinstance(llm, int) or llm < 0:
        errors.append("  budget.max_llm_calls_per_goal must exist and be integer >= 0.")

    # max_autonomous_goal_loops must exist and be between 0 and 5
    loops = sb.get("max_autonomous_goal_loops")
    if loops is None or not isinstance(loops, int) or loops < 0 or loops > 5:
        errors.append("  budget.max_autonomous_goal_loops must exist and be integer 0-5.")

    # max_retry_cycles must exist and be between 0 and 5
    retries = sb.get("max_retry_cycles")
    if retries is None or not isinstance(retries, int) or retries < 0 or retries > 5:
        errors.append("  budget.max_retry_cycles must exist and be integer 0-5.")

    # max_ci_watch_minutes must exist and be finite (1-60)
    ci = sb.get("max_ci_watch_minutes")
    if ci is None or not isinstance(ci, int) or ci < 1 or ci > 60:
        errors.append("  budget.max_ci_watch_minutes must exist and be integer 1-60.")

    # Human approval gates
    if sb.get("requires_human_approval_to_increase_budget") is not True:
        errors.append("  budget.requires_human_approval_to_increase_budget must be true.")

    if sb.get("requires_human_approval_for_sdk_use") is not True:
        errors.append("  budget.requires_human_approval_for_sdk_use must be true.")

    if sb.get("requires_human_approval_for_goal_mode") is not True:
        errors.append("  budget.requires_human_approval_for_goal_mode must be true.")

    # ── budget limits file checks ───────────────────────────────────
    if "version" not in budget:
        errors.append("  Budget limits file missing 'version' field.")

    if budget.get("budget_mode") != "strict":
        errors.append("  Budget limits file budget_mode should be 'strict'.")

    mb = budget.get("monetary_budget", {})
    if mb.get("external_paid_api_allowed") is not False:
        errors.append(
            "  Budget limits: monetary_budget.external_paid_api_allowed must be false by default."
        )

    if mb.get("requires_human_approval_to_increase") is not True:
        errors.append(
            "  Budget limits: monetary_budget.requires_human_approval_to_increase must be true."
        )

    lb = budget.get("llm_budget", {})
    if lb.get("requires_human_approval_for_goal_mode") is not True:
        errors.append(
            "  Budget limits: llm_budget.requires_human_approval_for_goal_mode must be true."
        )

    if lb.get("requires_human_approval_for_sdk_use") is not True:
        errors.append(
            "  Budget limits: llm_budget.requires_human_approval_for_sdk_use must be true."
        )

    eb = budget.get("execution_budget", {})
    max_retry = eb.get("max_failed_validation_attempts")
    if max_retry is None or not isinstance(max_retry, int) or max_retry < 0 or max_retry > 5:
        errors.append(
            "  Budget limits: execution_budget.max_failed_validation_attempts must be integer 0-5."
        )

    max_ci = eb.get("max_ci_watch_minutes")
    if max_ci is None or not isinstance(max_ci, int) or max_ci < 1 or max_ci > 60:
        errors.append(
            "  Budget limits: execution_budget.max_ci_watch_minutes must be integer 1-60."
        )

    # ── stop conditions ─────────────────────────────────────────────
    stops = set(budget.get("stop_conditions", []))
    required_stops = {
        "estimated_cost_exceeds_budget",
        "paid_api_requested_without_approval",
        "sdk_requested_without_approval",
        "goal_mode_requested_without_approval",
        "retry_limit_exceeded",
        "ci_watch_timeout_exceeded",
    }
    missing = required_stops - stops
    if missing:
        errors.append(f"  Budget limits: missing stop_conditions: {sorted(missing)}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate BudgetOps limits for the agentic workflow."
    )
    parser.add_argument(
        "--state",
        required=True,
        help="Path to the workflow state JSON file.",
    )
    parser.add_argument(
        "--budget",
        required=True,
        help="Path to the budget limits JSON file.",
    )
    args = parser.parse_args()

    state = _load_json(Path(args.state))
    budget = _load_json(Path(args.budget))

    errors = validate_budget(state, budget)

    # -- check usage accounting
    ua = budget.get("usage_accounting")
    if not isinstance(ua, dict):
        errors.append("usage_accounting must exist and be an object.")
    else:
        for flag in (
            "usage_ledger_required",
            "usage_summary_required",
            "human_review_required_before_merge",
            "human_review_required_before_tag",
            "fail_if_ledger_missing",
        ):
            if ua.get(flag) is not True:
                errors.append(f"  usage_accounting.{flag} must be true.")

    if errors:
        print(f"FAIL — {len(errors)} budget violation(s):")
        for err in errors:
            print(err)
        sys.exit(1)
    else:
        print("PASS — BudgetOps limits are valid and conservative.")
        sys.exit(0)


if __name__ == "__main__":
    main()
