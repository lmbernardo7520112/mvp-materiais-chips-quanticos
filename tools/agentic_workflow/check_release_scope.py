#!/usr/bin/env python3
"""Check that the files changed in a git diff respect the release scope.

Reads the workflow state file to determine:
  - forbidden_paths: files/directories that must not be modified.
  - forbidden_terms: patterns that must not appear in added lines.

Uses only the Python standard library plus git CLI.

Exit codes:
    0 — PASS (no violations)
    1 — FAIL (scope violations detected)
    2 — usage error
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def _run_git(args: list[str], cwd: str | None = None) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        print(f"git error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return result.stdout


def _load_state(path: Path) -> dict:
    """Load and return the workflow state JSON."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Cannot load state file {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def check_forbidden_paths(
    changed_files: list[str], forbidden: list[str]
) -> list[str]:
    """Return list of violation messages for forbidden path modifications."""
    violations: list[str] = []
    for f in changed_files:
        for fp in forbidden:
            # Match exact file or anything under a forbidden directory.
            if f == fp or f.startswith(fp.rstrip("/") + "/"):
                violations.append(f"  FORBIDDEN PATH modified: {f} (rule: {fp})")
    return violations



# Paths excluded from forbidden-term scanning because they legitimately
# contain forbidden terms as *configuration* (listing what is prohibited).
TERM_SCAN_EXCLUDED_PREFIXES = (
    ".agent/",
    "tools/agentic_workflow/",
    "docs/governance/",
    "docs/decision_briefs/",
    "docs/release_notes/",
    "docs/research_council/",
    "docs/adr/",
)


def check_forbidden_terms(
    base: str, forbidden_terms: list[str], cwd: str | None = None
) -> list[str]:
    """Scan added lines in git diff for forbidden term patterns.

    Files under TERM_SCAN_EXCLUDED_PREFIXES are skipped because they
    legitimately reference forbidden terms as governance configuration
    (e.g. listing ``physical_phi`` as a blocked term).
    """
    violations: list[str] = []
    diff_output = _run_git(["diff", base, "--unified=0"], cwd=cwd)

    current_file = ""
    for line in diff_output.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
        elif line.startswith("+") and not line.startswith("+++"):
            # Skip files that are governance/config by nature.
            if any(
                current_file.startswith(prefix)
                for prefix in TERM_SCAN_EXCLUDED_PREFIXES
            ):
                continue
            added_line = line[1:]
            for term in forbidden_terms:
                try:
                    if re.search(term, added_line):
                        violations.append(
                            f"  FORBIDDEN TERM '{term}' found in "
                            f"{current_file}: {added_line.strip()[:80]}"
                        )
                except re.error:
                    # If the term is not valid regex, do a literal search.
                    if term in added_line:
                        violations.append(
                            f"  FORBIDDEN TERM '{term}' found in "
                            f"{current_file}: {added_line.strip()[:80]}"
                        )
    return violations


def check_hardcoded_guards(changed_files: list[str]) -> list[str]:
    """Always-on guards regardless of state file contents."""
    violations: list[str] = []
    hardcoded_forbidden = [
        "tools/quality_gates/policy.json",
        "pyproject.toml",
    ]
    for f in changed_files:
        for hf in hardcoded_forbidden:
            if f == hf:
                violations.append(
                    f"  HARDCODED GUARD: {f} modified — requires explicit "
                    f"human approval and dependency decision brief."
                )
    return violations


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check release scope against workflow state."
    )
    parser.add_argument(
        "--base",
        required=True,
        help="Git ref to diff against (e.g. main).",
    )
    parser.add_argument(
        "--state",
        required=True,
        help="Path to the workflow state JSON file.",
    )
    args = parser.parse_args()

    state = _load_state(Path(args.state))

    # Get changed files.
    changed_output = _run_git(["diff", "--name-only", args.base])
    changed_files = [f for f in changed_output.strip().splitlines() if f]

    if not changed_files:
        print("PASS — No files changed relative to base.")
        sys.exit(0)

    print(f"Files changed vs {args.base}:")
    for f in changed_files:
        print(f"  {f}")
    print()

    all_violations: list[str] = []

    # 1. Forbidden paths from state.
    forbidden_paths = state.get("forbidden_paths", [])
    all_violations.extend(check_forbidden_paths(changed_files, forbidden_paths))

    # 2. Hardcoded guards (always checked).
    all_violations.extend(check_hardcoded_guards(changed_files))

    # 3. Forbidden terms in added lines.
    forbidden_terms = state.get("forbidden_terms", [])
    if forbidden_terms:
        all_violations.extend(
            check_forbidden_terms(args.base, forbidden_terms)
        )

    # ── report ──────────────────────────────────────────────────────
    if all_violations:
        print(f"FAIL — {len(all_violations)} scope violation(s):")
        for v in all_violations:
            print(v)
        sys.exit(1)
    else:
        print("PASS — All changed files are within authorized scope.")
        sys.exit(0)


if __name__ == "__main__":
    main()
