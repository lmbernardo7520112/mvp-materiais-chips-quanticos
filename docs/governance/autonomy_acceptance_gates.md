# Autonomy Acceptance Gates

## Purpose

Defines the minimum criteria for accepting the Autonomy-001 release.

## Gates

| # | Gate | Required | Status |
| :--- | :--- | :--- | :--- |
| G1 | Documentation and tooling only — no scientific code changes. | Yes | |
| G2 | Zero changes to `src/`. | Yes | |
| G3 | Zero changes to `tests/` (physics tests). | Yes | |
| G4 | Zero changes to `scripts/` (scientific scripts). | Yes | |
| G5 | Zero changes to `results/`. | Yes | |
| G6 | Zero changes to `pyproject.toml`. | Yes | |
| G7 | Zero changes to `tools/quality_gates/policy.json`. | Yes | |
| G8 | Zero changes to `.agent/skills/`. | Yes | |
| G9 | No dependencies added. | Yes | |
| G10 | Workflow state schema exists (`.agent/workflow_state.schema.json`). | Yes | |
| G11 | Workflow state example exists (`.agent/workflow_state.example.json`). | Yes | |
| G12 | Release rules exist (`.agent/release_rules.yaml`). | Yes | |
| G13 | State validator exists and runs (`validate_workflow_state.py`). | Yes | |
| G14 | Scope checker exists and runs (`check_release_scope.py`). | Yes | |
| G15 | State validator PASS on example state. | Yes | |
| G16 | Scope checker PASS on current diff. | Yes | |
| G17 | Critical actions require human approval in state schema. | Yes | |
| G18 | `merge_pr` requires human approval. | Yes | |
| G19 | `create_tag` requires human approval. | Yes | |
| G20 | `accept_adr` requires human approval. | Yes | |
| G21 | `change_pyproject` requires human approval. | Yes | |
| G22 | `change_policy` requires human approval. | Yes | |
| G23 | `enable_poisson_runtime` requires human approval. | Yes | |
| G24 | `enable_physical_phi` requires human approval. | Yes | |
| G25 | `enable_solver_coupling` requires human approval. | Yes | |
| G26 | `enable_aifs_runtime` requires human approval. | Yes | |
| G27 | No auto-merge capability. | Yes | |
| G28 | No auto-tag capability. | Yes | |
| G29 | No ADR auto-acceptance capability. | Yes | |
| G30 | Risk matrix exists with 16 risks documented. | Yes | |
| G31 | Governance document exists. | Yes | |
| G32 | Quality gates PASS (6/6). | Yes | |
| G33 | pytest PASS (281+ passed). | Yes | |
| G34 | Coverage ≥ 70%. | Yes | |
| G35 | ruff PASS. | Yes | |
| G36 | pyright PASS (0 errors). | Yes | |
| G37 | `generate_all_results` PASS. | Yes | |
| G38 | Budget config exists (`.agent/budget_limits.example.json`). | Yes | |
| G39 | Budget schema exists in workflow state schema. | Yes | |
| G40 | Budget validator exists (`check_budget_limits.py`). | Yes | |
| G41 | Paid API disabled by default. | Yes | |
| G42 | External SDK disabled by default. | Yes | |
| G43 | Goal mode disabled by default. | Yes | |
| G44 | Budget increase requires human approval. | Yes | |
| G45 | Retry limit finite (0-5). | Yes | |
| G46 | CI watch limit finite (1-60 minutes). | Yes | |
| G47 | Artifact budget finite. | Yes | |
