# Autonomy-001 — Agentic State Machine Governance

## Summary

Introduces a local state machine and scope-checking tooling to reduce human micro-orchestration while preserving full scientific and governance rigor.

## What is included

* `.agent/workflow_state.example.json` — example state file with all mandatory fields.
* `.agent/workflow_state.schema.json` — JSON Schema for the state file.
* `.agent/release_rules.yaml` — per-release-type scope policies.
* `tools/agentic_workflow/validate_workflow_state.py` — stdlib-only state validator.
* `tools/agentic_workflow/check_release_scope.py` — git-based scope checker.
* `docs/governance/agentic_state_machine_governance.md` — governance architecture.
* `docs/governance/autonomy_risk_matrix.md` — 10-risk matrix with mitigations.
* `docs/governance/autonomy_acceptance_gates.md` — 37 acceptance gates.
* `docs/decision_briefs/autonomy_001_state_machine_brief.md` — decision brief.

## What is NOT included

* No auto-merge.
* No auto-tag.
* No ADR auto-acceptance.
* No scientific code changes.
* No dependency changes.
* No Poisson runtime.
* No physical phi.
* No AI-for-Science runtime.
* No multi-agent SDK.

## Human approval still required for

* Merging PRs.
* Creating tags.
* Accepting ADRs.
* Modifying pyproject.toml.
* Modifying policy.json.
* Adding dependencies.
* Enabling Poisson runtime, physical phi, solver coupling, or AIFS runtime.
