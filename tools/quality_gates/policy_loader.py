"""Load and validate the version-aware quality gate policy."""

import json
from pathlib import Path

_POLICY_PATH = Path(__file__).parent / "policy.json"


def load_policy(path: Path | None = None) -> dict:
    """Load the JSON policy and return parsed dict.

    Args:
        path: Optional override for the policy file location.

    Returns:
        Parsed policy dict.

    Raises:
        FileNotFoundError: If the policy file does not exist.
        ValueError: If the policy is malformed.
    """
    p = path or _POLICY_PATH
    if not p.exists():
        raise FileNotFoundError(f"Policy file not found: {p}")

    with open(p) as f:
        policy = json.load(f)

    if not isinstance(policy, dict):
        raise ValueError("Policy file must be a JSON object")

    if "current_stage" not in policy:
        raise ValueError("Policy must define 'current_stage'")

    if "stages" not in policy or not isinstance(policy["stages"], dict):
        raise ValueError("Policy must define 'stages' as a mapping")

    stage = policy["current_stage"]
    if stage not in policy["stages"]:
        raise ValueError(
            f"current_stage '{stage}' not found in stages: {list(policy['stages'].keys())}"
        )

    return policy


def get_active_stage(policy: dict) -> dict:
    """Return the rules for the currently active stage.

    Args:
        policy: Parsed policy dict.

    Returns:
        Dict of rules for the active stage.
    """
    return policy["stages"][policy["current_stage"]]


def get_stage_name(policy: dict) -> str:
    """Return the name of the currently active stage."""
    return policy["current_stage"]
