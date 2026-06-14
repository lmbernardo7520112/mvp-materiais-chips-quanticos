import argparse
import json
import sys


def summarize_ledger(ledger_path, output_path=None):
    total_cost = 0.0
    total_retries = 0
    total_ci_watch = 0
    total_files_changed = 0
    total_artifacts = 0
    total_events = 0

    session_id = None
    release_id = None

    paid_api = False
    sdk = False
    goal = False

    approvals_granted = 0
    approvals_denied = 0

    try:
        with open(ledger_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue

                total_events += 1
                if session_id is None:
                    session_id = event.get("session_id")
                if release_id is None:
                    release_id = event.get("release_id")

                total_cost += float(event.get("estimated_cost_brl", 0.0))
                total_retries += int(event.get("retry_count", 0))
                total_ci_watch += int(event.get("ci_watch_minutes", 0))
                total_files_changed += int(event.get("files_changed_count", 0))
                total_artifacts += int(event.get("artifacts_generated_count", 0))

                if event.get("paid_api_used"):
                    paid_api = True
                if event.get("external_sdk_used"):
                    sdk = True
                if event.get("goal_mode_used"):
                    goal = True

                event_type = event.get("event_type")
                if event_type == "human_approval_granted":
                    approvals_granted += 1
                elif event_type == "human_approval_denied":
                    approvals_denied += 1
    except Exception as e:
        print(f"Could not load ledger {ledger_path}: {e}")
        return False

    lines = [
        "=== USAGE LEDGER SUMMARY ===",
        f"Session ID: {session_id}",
        f"Release ID: {release_id}",
        f"Total Events: {total_events}",
        f"Total Estimated Cost: R$ {total_cost:.2f}",
        f"Paid API Used: {paid_api}",
        f"External SDK Used: {sdk}",
        f"Goal Mode Used: {goal}",
        f"Total Retries: {total_retries}",
        f"Total CI Watch Minutes: {total_ci_watch}",
        f"Total Files Changed: {total_files_changed}",
        f"Total Artifacts Generated: {total_artifacts}",
        f"Human Approvals Granted: {approvals_granted}",
        f"Human Approvals Denied: {approvals_denied}",
        "============================"
    ]

    summary_text = "\n".join(lines)
    print(summary_text)

    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(summary_text)
        except Exception as e:
            print(f"Could not write to {output_path}: {e}")
            return False

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True, help="Path to usage ledger JSONL")
    parser.add_argument("--output", help="Optional output path for the markdown summary")
    args = parser.parse_args()

    if not summarize_ledger(args.ledger, args.output):
        sys.exit(1)
    sys.exit(0)
