"""Gate: version-aware scope guardrails.

Scans src/, scripts/, and tests/ for terms forbidden by the active stage.
Does NOT scan docs/ — documentation may reference future scope.

Exit code 1 if any violation is found.
"""

import sys
from pathlib import Path

from tools.quality_gates.policy_loader import get_active_stage, load_policy

SCAN_DIRS = ["src", "scripts", "tests"]

# Test files that intentionally contain forbidden terms as test fixtures
EXCLUDED_FILES = {"test_quality_gates.py"}


def check_scope_guardrails(repo_root: Path, policy: dict) -> list[str]:
    """Check for forbidden terms in code directories.

    Returns:
        List of violation descriptions. Empty means pass.
    """
    stage = get_active_stage(policy)
    forbidden = stage.get("forbidden_in_code", [])
    if not forbidden:
        return []

    violations: list[str] = []
    for scan_dir in SCAN_DIRS:
        d = repo_root / scan_dir
        if not d.exists():
            continue
        for fpath in sorted(d.rglob("*.py")):
            if fpath.name in EXCLUDED_FILES:
                continue
            content = fpath.read_text(errors="replace")
            for term in forbidden:
                for line_num, line in enumerate(content.splitlines(), 1):
                    if term in line:
                        rel = fpath.relative_to(repo_root)
                        violations.append(
                            f"  {rel}:{line_num} — forbidden term '{term}': {line.strip()}"
                        )
    return violations


def main() -> int:
    """Run scope guardrails check."""
    repo_root = Path(__file__).parent.parent.parent
    policy = load_policy()
    violations = check_scope_guardrails(repo_root, policy)

    if violations:
        print(f"FAIL: scope guardrails — {len(violations)} violation(s):")
        for v in violations:
            print(v)
        return 1

    print("PASS: scope guardrails — no forbidden terms in code")
    return 0


if __name__ == "__main__":
    sys.exit(main())
