"""AI-RSE GateOps — consolidated quality gate runner.

Executes all version-aware quality gates and reports results.
Exit code 1 if any gate fails.

Usage from repo root:
    PYTHONPATH=. python tools/quality_gates/run_all_quality_gates.py
    PYTHONPATH=. python tools/quality_gates/run_all_quality_gates.py --require-artifacts
"""

import argparse
import sys
from pathlib import Path

from tools.quality_gates.check_adr_status import check_adr_status
from tools.quality_gates.check_artifacts import check_artifacts
from tools.quality_gates.check_docs_required import check_docs_required
from tools.quality_gates.check_private_forbidden_terms import (
    _load_patterns as load_private_patterns,
)
from tools.quality_gates.check_private_forbidden_terms import (
    check_private_forbidden_terms,
)
from tools.quality_gates.check_scope_guardrails import check_scope_guardrails
from tools.quality_gates.check_solver_integrity import check_solver_integrity
from tools.quality_gates.policy_loader import get_stage_name, load_policy


def main() -> int:
    """Run all quality gates."""
    parser = argparse.ArgumentParser(description="AI-RSE GateOps — run all quality gates")
    parser.add_argument(
        "--require-artifacts",
        action="store_true",
        help="Include artifacts gate",
    )
    parser.add_argument(
        "--strict-private-terms",
        action="store_true",
        help="Fail if private forbidden terms source is not configured",
    )
    parser.add_argument(
        "--figures-dir",
        default="results/figures",
        help="Directory containing figures",
    )
    parser.add_argument(
        "--tables-dir",
        default="results/tables",
        help="Directory containing CSVs",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.parent
    policy = load_policy()
    stage = get_stage_name(policy)

    print(f"AI-RSE GateOps — stage: {stage}")
    print("=" * 60)

    results: dict[str, str] = {}
    any_fail = False

    # Gate 1: ADR status
    failures = check_adr_status(repo_root, policy)
    if failures:
        results["ADR status"] = f"FAIL ({len(failures)})"
        any_fail = True
        for f in failures:
            print(f)
    else:
        results["ADR status"] = "PASS"

    # Gate 2: Scope guardrails
    violations = check_scope_guardrails(repo_root, policy)
    if violations:
        results["Scope guardrails"] = f"FAIL ({len(violations)})"
        any_fail = True
        for v in violations:
            print(v)
    else:
        results["Scope guardrails"] = "PASS"

    # Gate 3: Solver integrity
    failures = check_solver_integrity(repo_root, policy)
    if failures:
        results["Solver integrity"] = f"FAIL ({len(failures)})"
        any_fail = True
        for f in failures:
            print(f)
    else:
        results["Solver integrity"] = "PASS"

    # Gate 4: Required docs
    failures = check_docs_required(repo_root, policy)
    if failures:
        results["Required docs"] = f"FAIL ({len(failures)})"
        any_fail = True
        for f in failures:
            print(f)
    else:
        results["Required docs"] = "PASS"

    # Gate 5: Artifacts (optional)
    if args.require_artifacts:
        failures = check_artifacts(
            repo_root / args.figures_dir,
            repo_root / args.tables_dir,
            policy,
        )
        if failures:
            results["Artifacts"] = f"FAIL ({len(failures)})"
            any_fail = True
            for f in failures:
                print(f)
        else:
            results["Artifacts"] = "PASS"
    else:
        results["Artifacts"] = "SKIPPED"

    # Gate 6: Private forbidden terms
    patterns = load_private_patterns()
    if patterns is None:
        if args.strict_private_terms:
            results["Private terms"] = "FAIL (no source)"
            any_fail = True
        else:
            results["Private terms"] = "SKIPPED (no source)"
    else:
        violations = check_private_forbidden_terms(repo_root, patterns)
        if violations:
            results["Private terms"] = f"FAIL ({len(violations)})"
            any_fail = True
            for v in violations:
                print(v)
        else:
            results["Private terms"] = "PASS"

    # Summary
    print()
    print("=" * 60)
    print(f"AI-RSE GateOps Summary — stage: {stage}")
    print("-" * 60)
    for gate, status in results.items():
        marker = "PASS" if "PASS" in status else "SKIP" if "SKIP" in status else "FAIL"
        print(f"  [{marker}] {gate}: {status}")
    print("=" * 60)

    if any_fail:
        print("RESULT: FAIL — one or more gates failed")
        return 1

    print("RESULT: PASS — all gates passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
