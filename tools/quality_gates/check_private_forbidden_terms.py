"""Gate: private forbidden terms.

Checks for terms that must NOT appear anywhere in the repository.
Terms are loaded from:
  1. Environment variable PRIVATE_FORBIDDEN_TERMS_REGEX
  2. Local gitignored file .quality_gates_forbidden_terms.local

The terms are NEVER stored in the repository itself.

Exit code 1 if any violation is found (strict mode).
SKIPPED if no terms source is configured (non-strict mode).
"""

import argparse
import os
import re
import sys
from pathlib import Path

TERMS_ENV_VAR = "PRIVATE_FORBIDDEN_TERMS_REGEX"
LOCAL_FILE = ".quality_gates_forbidden_terms.local"

SCAN_EXTENSIONS = {
    ".py",
    ".md",
    ".yml",
    ".yaml",
    ".toml",
    ".txt",
    ".csv",
    ".cfg",
}
SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
}


def _load_patterns() -> list[str] | None:
    """Load forbidden term patterns from env or local file.

    Returns:
        List of regex patterns, or None if no source configured.
    """
    # Try environment variable first
    env_val = os.environ.get(TERMS_ENV_VAR, "").strip()
    if env_val:
        return [p.strip() for p in env_val.split("|") if p.strip()]

    # Try local file
    local = Path(LOCAL_FILE)
    if local.exists():
        lines = local.read_text().strip().splitlines()
        return [line.strip() for line in lines if line.strip() and not line.startswith("#")]

    return None


def check_private_forbidden_terms(repo_root: Path, patterns: list[str]) -> list[str]:
    """Scan repository for forbidden term patterns.

    Returns:
        List of violation descriptions. Empty means pass.
    """
    violations: list[str] = []
    compiled = [re.compile(p, re.IGNORECASE) for p in patterns]

    for fpath in sorted(repo_root.rglob("*")):
        if fpath.is_dir():
            continue
        if any(skip in fpath.parts for skip in SKIP_DIRS):
            continue
        if fpath.suffix not in SCAN_EXTENSIONS:
            continue
        # Skip this gate file itself
        if fpath.name == "check_private_forbidden_terms.py":
            continue

        try:
            content = fpath.read_text(errors="replace")
        except Exception:
            continue

        rel = fpath.relative_to(repo_root)
        for line_num, line in enumerate(content.splitlines(), 1):
            for pattern in compiled:
                if pattern.search(line):
                    violations.append(f"  PRIVATE_FORBIDDEN_TERMS violation at {rel}:{line_num}")

    return violations


def main() -> int:
    """Run private forbidden terms check."""
    parser = argparse.ArgumentParser(description="Check for private forbidden terms")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if no terms source is configured",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.parent
    patterns = _load_patterns()

    if patterns is None:
        if args.strict:
            print(
                "FAIL: private forbidden terms — no terms source "
                f"configured (set {TERMS_ENV_VAR} or "
                f"create {LOCAL_FILE})"
            )
            return 1
        else:
            print(
                f"SKIPPED: private forbidden terms — no terms "
                f"source configured (set {TERMS_ENV_VAR} or "
                f"create {LOCAL_FILE})"
            )
            return 0

    violations = check_private_forbidden_terms(repo_root, patterns)

    if violations:
        print(f"FAIL: private forbidden terms — {len(violations)} violation(s):")
        for v in violations:
            print(v)
        return 1

    print("PASS: private forbidden terms — no matches found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
