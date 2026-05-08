"""Gate: solver integrity verification.

Ensures critical solver files have not been modified beyond allowed exceptions.
Uses git diff against the main branch.

Exit code 1 if behavioral changes are detected.
"""

import subprocess
import sys
from pathlib import Path

from tools.quality_gates.policy_loader import get_active_stage, load_policy

CRITICAL_FILES = {
    "thermal_solver.py": "src/mvp_quantum_materials/thermal_solver.py",
    "diffusion_solver.py": "src/mvp_quantum_materials/diffusion_solver.py",
}

# Lines that are allowed for type-only @overload exceptions
TYPE_ONLY_PATTERNS = [
    "from typing import overload",
    "@overload",
    "def arrhenius_diffusivity(",
    "temperature: float,",
    "temperature: npt.NDArray[np.float64],",
    "d0: float,",
    "ea: float,",
    ") -> float: ...",
    ") -> npt.NDArray[np.float64]: ...",
]


def _get_diff_lines(repo_root: Path, filepath: str) -> list[str]:
    """Get added/removed lines from git diff against main."""
    for ref in ["main", "origin/main"]:
        try:
            result = subprocess.run(
                ["git", "diff", ref, "--", filepath],
                capture_output=True,
                text=True,
                cwd=str(repo_root),
                timeout=10,
            )
            if result.returncode == 0:
                return result.stdout.splitlines()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return ["ERROR: git diff failed — neither main nor origin/main available"]


def _is_type_only_change(diff_lines: list[str]) -> bool:
    """Check if all changes are type-only (imports, overloads)."""
    for line in diff_lines:
        if not line.startswith("+") and not line.startswith("-"):
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("@@"):
            continue

        content = line[1:].strip()
        if not content:
            continue

        if any(pattern in content for pattern in TYPE_ONLY_PATTERNS):
            continue

        # This is a non-type-only change
        return False

    return True


def check_solver_integrity(repo_root: Path, policy: dict) -> list[str]:
    """Check solver files for unauthorized modifications.

    Returns:
        List of failure descriptions. Empty means pass.
    """
    stage = get_active_stage(policy)
    allowed_exceptions = stage.get("allowed_exceptions", {})
    failures: list[str] = []

    for name, filepath in CRITICAL_FILES.items():
        diff_lines = _get_diff_lines(repo_root, filepath)

        if any(line.startswith("ERROR:") for line in diff_lines):
            failures.append(f"  {name}: {diff_lines[0]}")
            continue

        # Filter to only actual change lines
        change_lines = [
            line
            for line in diff_lines
            if (line.startswith("+") or line.startswith("-"))
            and not line.startswith("+++")
            and not line.startswith("---")
        ]

        if not change_lines:
            # No diff — perfect
            continue

        # Check if this file has allowed exceptions
        if name in allowed_exceptions:
            exception_types = allowed_exceptions[name]
            if "type_only_overload" in exception_types:
                if _is_type_only_change(diff_lines):
                    continue
                else:
                    failures.append(f"  {name}: has changes beyond type-only @overload exception")
                    continue

        # No exception — any change is a failure
        failures.append(
            f"  {name}: unauthorized modification detected ({len(change_lines)} changed lines)"
        )

    return failures


def main() -> int:
    """Run solver integrity check."""
    repo_root = Path(__file__).parent.parent.parent
    policy = load_policy()
    failures = check_solver_integrity(repo_root, policy)

    if failures:
        print(f"FAIL: solver integrity — {len(failures)} issue(s):")
        for f in failures:
            print(f)
        return 1

    print("PASS: solver integrity — critical files verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
