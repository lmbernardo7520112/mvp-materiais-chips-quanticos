"""Gate: ADR status verification.

Verifies that required ADRs exist and have the expected status.
Exit code 1 if any ADR is missing or has wrong status.
"""

import re
import sys
from pathlib import Path

from tools.quality_gates.policy_loader import get_active_stage, load_policy

ADR_DIR = "docs/adr"


def check_adr_status(repo_root: Path, policy: dict) -> list[str]:
    """Check required ADRs exist and have correct status.

    Returns:
        List of failure descriptions. Empty means pass.
    """
    stage = get_active_stage(policy)
    required = stage.get("required_adrs", {})
    if not required:
        return []

    failures: list[str] = []
    for adr_file, expected_status in required.items():
        adr_path = repo_root / ADR_DIR / adr_file
        if not adr_path.exists():
            failures.append(f"  ADR missing: {adr_file}")
            continue

        content = adr_path.read_text()
        date_pos = content.find("## Date")
        search_area = content[: date_pos + 1] if date_pos >= 0 else content[:500]
        status_match = re.search(r"\*\*(\w+)\*\*", search_area)
        if status_match:
            actual = status_match.group(1)
            if actual != expected_status:
                failures.append(f"  ADR {adr_file}: expected '{expected_status}', found '{actual}'")
        else:
            failures.append(f"  ADR {adr_file}: could not parse status")

    return failures


def main() -> int:
    """Run ADR status check."""
    repo_root = Path(__file__).parent.parent.parent
    policy = load_policy()
    failures = check_adr_status(repo_root, policy)

    if failures:
        print(f"FAIL: ADR status — {len(failures)} issue(s):")
        for f in failures:
            print(f)
        return 1

    print("PASS: ADR status — all required ADRs have correct status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
