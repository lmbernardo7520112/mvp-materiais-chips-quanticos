"""Gate: required documentation verification.

Checks that all required documents exist per the active policy stage.
Exit code 1 if any document is missing.
"""

import sys
from pathlib import Path

from tools.quality_gates.policy_loader import get_active_stage, load_policy


def check_docs_required(repo_root: Path, policy: dict) -> list[str]:
    """Check required documents exist.

    Returns:
        List of failure descriptions. Empty means pass.
    """
    stage = get_active_stage(policy)
    required = stage.get("required_docs", [])

    failures: list[str] = []
    for doc_path in required:
        if not (repo_root / doc_path).exists():
            failures.append(f"  Missing: {doc_path}")

    return failures


def main() -> int:
    """Run docs required check."""
    repo_root = Path(__file__).parent.parent.parent
    policy = load_policy()
    failures = check_docs_required(repo_root, policy)

    if failures:
        print(f"FAIL: required docs — {len(failures)} missing:")
        for f in failures:
            print(f)
        return 1

    print("PASS: required docs — all present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
