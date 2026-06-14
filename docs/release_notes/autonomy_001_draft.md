# Autonomy-001 — Agentic State Machine Governance

## Summary

Introduces a local state machine, scope-checking tooling, and BudgetOps guardrails to reduce human micro-orchestration while preserving full scientific and governance rigor.

## What is included

* `.agent/workflow_state.example.json` — example state file with all mandatory fields including budget.
* `.agent/workflow_state.schema.json` — JSON Schema for the state file (requires budget).
* `.agent/release_rules.yaml` — per-release-type scope policies with budget guardrails.
* `.agent/budget_limits.example.json` — BudgetOps configuration with conservative defaults.
* `tools/agentic_workflow/validate_workflow_state.py` — stdlib-only state validator (includes budget checks).
* `tools/agentic_workflow/check_release_scope.py` — git-based scope checker (includes budget guardrails).
* `tools/agentic_workflow/check_budget_limits.py` — stdlib-only budget limits validator.
* `docs/governance/agentic_state_machine_governance.md` — governance architecture with BudgetOps section.
* `docs/governance/autonomy_risk_matrix.md` — 16-risk matrix with mitigations (includes R11-R16 budget risks).
* `docs/governance/autonomy_acceptance_gates.md` — 47 acceptance gates (includes G38-G47 budget gates).
* `docs/decision_briefs/autonomy_001_state_machine_brief.md` — decision brief with budget decision.

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
* No paid API allowed by default.
* No unbounded /goal loops.

## BudgetOps guardrails

* Default monetary budget: 0 BRL.
* Paid API: disabled by default.
* External SDK: disabled by default.
* Goal mode: disabled by default.
* Retry limit: 0-5 (default 2).
* CI watch limit: 1-60 minutes (default 15).
* Artifact limits: finite.
* Budget increase: requires human approval.
* Stop conditions: 11 mandatory triggers defined.

## Human approval still required for

* Merging PRs.
* Creating tags.
* Accepting ADRs.
* Modifying pyproject.toml.
* Modifying policy.json.
* Adding dependencies.
* Enabling Poisson runtime, physical phi, solver coupling, or AIFS runtime.
* Increasing budget.
* Using paid API.
* Using external SDK.
* Enabling goal mode.
