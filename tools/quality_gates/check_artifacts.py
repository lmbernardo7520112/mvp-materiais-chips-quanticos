"""Gate: required artifacts verification.

Checks that required figures and CSVs exist per the active policy stage.
Exit code 1 if any artifact is missing or count is below minimum.
"""

import argparse
import sys
from pathlib import Path

from tools.quality_gates.policy_loader import get_active_stage, load_policy


def check_artifacts(figures_dir: Path, tables_dir: Path, policy: dict) -> list[str]:
    """Check required artifacts exist.

    Returns:
        List of failure descriptions. Empty means pass.
    """
    stage = get_active_stage(policy)
    req = stage.get("required_artifacts", {})
    if not req:
        return []

    failures: list[str] = []

    # Check minimum figure count
    figures_min = req.get("figures_min", 0)
    actual_figs = list(figures_dir.glob("*.png")) if figures_dir.exists() else []
    if len(actual_figs) < figures_min:
        failures.append(f"  Figures: expected >= {figures_min}, found {len(actual_figs)}")

    # Check minimum CSV count
    csv_min = req.get("csv_min", 0)
    actual_csvs = list(tables_dir.glob("*.csv")) if tables_dir.exists() else []
    if len(actual_csvs) < csv_min:
        failures.append(f"  CSVs: expected >= {csv_min}, found {len(actual_csvs)}")

    # Check required figures
    for fig in req.get("figures", []):
        if not (figures_dir / fig).exists():
            failures.append(f"  Missing figure: {fig}")

    # Check required tables
    for tbl in req.get("tables", []):
        if not (tables_dir / tbl).exists():
            failures.append(f"  Missing CSV: {tbl}")

    return failures


def main() -> int:
    """Run artifacts check."""
    parser = argparse.ArgumentParser(description="Check required artifacts")
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
    failures = check_artifacts(
        repo_root / args.figures_dir,
        repo_root / args.tables_dir,
        policy,
    )

    if failures:
        print(f"FAIL: artifacts — {len(failures)} issue(s):")
        for f in failures:
            print(f)
        return 1

    print("PASS: artifacts — all required artifacts present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
