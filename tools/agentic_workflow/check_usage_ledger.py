import argparse
import json
import sys

ALLOWED_EVENTS = {
    "session_started",
    "phase_started",
    "command_executed",
    "validation_run",
    "validation_failed",
    "validation_passed",
    "retry_used",
    "ci_watch_started",
    "ci_watch_finished",
    "files_changed_reported",
    "artifacts_generated",
    "budget_checked",
    "human_approval_required",
    "human_approval_granted",
    "human_approval_denied",
    "session_finished",
}

REQUIRED_FIELDS = {
    "timestamp_utc",
    "session_id",
    "release_id",
    "phase",
    "event_type",
    "actor",
    "paid_api_used",
    "external_sdk_used",
    "goal_mode_used",
    "estimated_cost_brl",
}


def check_ledger(ledger_path, budget_path):
    try:
        with open(budget_path, encoding="utf-8") as f:
            budget = json.load(f)
    except Exception as e:
        print(f"FAIL — Could not load budget {budget_path}: {e}")
        return False

    mb = budget.get("monetary_budget", {})
    lb = budget.get("llm_budget", {})
    eb = budget.get("execution_budget", {})
    ab = budget.get("artifact_budget", {})

    max_cost = mb.get("max_total_estimated_cost_brl", 0.0)
    max_retries = lb.get("max_retry_cycles", 0)
    max_ci_watch = eb.get("max_ci_watch_minutes", 0)
    max_artifacts = ab.get("max_artifacts_generated", 999)  # Default high if missing

    total_cost = 0.0
    total_retries = 0
    total_ci_watch = 0
    total_artifacts = 0

    has_paid_api_used = False
    has_sdk_used = False
    has_goal_used = False
    has_human_approval = False

    errors = []

    try:
        with open(ledger_path, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    errors.append(f"Line {i}: Invalid JSON.")
                    continue

                missing = REQUIRED_FIELDS - event.keys()
                if missing:
                    errors.append(f"Line {i}: Missing fields {missing}.")

                event_type = event.get("event_type")
                if event_type not in ALLOWED_EVENTS:
                    errors.append(f"Line {i}: Invalid event_type '{event_type}'.")

                total_cost += float(event.get("estimated_cost_brl", 0.0))
                total_retries += int(event.get("retry_count", 0))
                total_ci_watch += int(event.get("ci_watch_minutes", 0))
                total_artifacts += int(event.get("artifacts_generated_count", 0))

                if event.get("paid_api_used"):
                    has_paid_api_used = True
                if event.get("external_sdk_used"):
                    has_sdk_used = True
                if event.get("goal_mode_used"):
                    has_goal_used = True

                if event_type == "human_approval_granted":
                    has_human_approval = True
    except Exception as e:
        print(f"FAIL — Could not load ledger {ledger_path}: {e}")
        return False

    if has_paid_api_used and not has_human_approval:
        errors.append("paid_api_used is true but no human_approval_granted found.")
    if has_sdk_used and not has_human_approval:
        errors.append("external_sdk_used is true but no human_approval_granted found.")
    if has_goal_used and not has_human_approval:
        errors.append("goal_mode_used is true but no human_approval_granted found.")

    if total_cost > max_cost:
        errors.append(f"Total cost ({total_cost}) exceeds budget ({max_cost}).")
    if total_retries > max_retries:
        errors.append(f"Total retries ({total_retries}) exceeds budget ({max_retries}).")
    if total_ci_watch > max_ci_watch:
        errors.append(f"CI watch mins ({total_ci_watch}) exceeds budget ({max_ci_watch}).")
    if total_artifacts > max_artifacts:
        errors.append(f"Artifacts ({total_artifacts}) exceeds budget ({max_artifacts}).")

    if errors:
        print(f"FAIL — {len(errors)} ledger violation(s):")
        for err in errors:
            print(f"  {err}")
        return False

    print("PASS — Usage ledger is valid and within budget.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True, help="Path to usage ledger JSONL")
    parser.add_argument("--budget", required=True, help="Path to budget limits JSON")
    args = parser.parse_args()

    if not check_ledger(args.ledger, args.budget):
        sys.exit(1)
    sys.exit(0)
