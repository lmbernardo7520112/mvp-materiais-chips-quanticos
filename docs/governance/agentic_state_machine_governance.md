# Agentic State Machine Governance

## Purpose

This document defines how the AI-RSE agent uses a local state machine to reduce human micro-orchestration while preserving full scientific and governance rigor.

## Principles

1. **Skills remain principles.** The `.agent/skills/` directory contains the governance logic (scope guardrails, physics-dimensional audit, TDD discipline, release management). These skills define *what* is allowed and prohibited. They are not modified by the state machine.

2. **The state machine records operational state.** The file `.agent/workflow_state.json` (instantiated from `.agent/workflow_state.example.json`) tells the agent *where* it is: which release, which phase, which paths are authorized, which terms are forbidden. This eliminates the need for the human to re-inject 30 lines of context at every prompt.

3. **Scripts make skill checks verifiable.** The tools `validate_workflow_state.py` and `check_release_scope.py` turn soft skill rules into hard, auditable checks. The agent must run these before requesting human review.

4. **CI should become a hard gate in the future.** The current quality gates (`tools/quality_gates/`) already enforce test coverage, linting, and artifact generation. In a future release, the scope checker can be integrated into GitHub Actions so that forbidden-path violations block the PR at the CI level, not just at the agent level.

5. **Humans remain responsible for irreversible decisions.** The state machine explicitly requires human approval for:
   - Merging pull requests.
   - Creating release tags.
   - Accepting or amending ADRs.
   - Modifying `pyproject.toml` or `policy.json`.
   - Adding dependencies.
   - Enabling Poisson runtime, physical phi, solver coupling, or AI-for-Science runtime.

6. **Autonomy is assistive, not sovereign.** The agent may autonomously: create branches, write code, run tests, generate reports, push branches, and create PRs. The agent may *never* autonomously: merge, tag, accept ADRs, change governance policies, or make irreversible scientific claims.

## Workflow

```
Human provides goal (e.g., "Execute v0.8.2 C3 RED")
        │
        ▼
Agent reads .agent/workflow_state.json
        │
        ▼
Agent reads required skills
        │
        ▼
Agent creates branch ──────────────────── (autonomous)
        │
        ▼
Agent writes code/tests within allowed_paths ── (autonomous)
        │
        ▼
Agent runs local validation:
  - validate_workflow_state.py
  - check_release_scope.py
  - quality gates
  - pytest, ruff, pyright
  - generate_all_results
        │
        ▼
Agent pushes branch and creates PR ────── (autonomous)
        │
        ▼
Agent requests human review ───────────── (STOP)
        │
        ▼
Human reviews, approves, merges ───────── (human-only)
        │
        ▼
Human authorizes tag ──────────────────── (human-only)
        │
        ▼
Agent updates workflow_state.json for next phase
```

## Release Rules

The file `.agent/release_rules.yaml` defines per-release-type policies. The agent consults these rules to determine:
- Which paths it may modify.
- Which paths are forbidden.
- Which checks must pass.
- Which actions require human approval.
- Which runtime claims are forbidden.

## State Transitions

State transitions follow the TDD cycle:

| From Phase | To Phase | Trigger | Human Approval |
| :--- | :--- | :--- | :--- |
| PLANNING | RED | ADR accepted or task defined | Yes |
| RED | GREEN | All RED tests written and failing | Yes (merge RED PR first) |
| GREEN | REFACTOR | All tests passing | Yes (merge GREEN PR first) |
| GREEN | DEMO | All tests passing, demo requested | Yes |
| DEMO | CLOSED | Demo validated | Yes (tag) |
| REFACTOR | CLOSED | Refactoring complete | Yes (tag) |
| Any | AUDIT | Audit requested | No (docs-only) |
| Any | ACCEPTANCE_REVIEW | ADR review requested | No (docs-only) |

## Constraints

- The state machine never bypasses skills. It complements them.
- The state file is versioned in git and auditable.
- If the state file is missing, the agent must operate in maximum-restriction mode (equivalent to PLANNING with all paths forbidden except docs/).
- The agent must never modify the state file to grant itself additional permissions.

## BudgetOps and Cost Safety

Autonomy is not authorization for unlimited resource consumption.

1. **No paid API by default.** The budget configuration (`budget_limits.example.json`) sets `external_paid_api_allowed: false`. Any use of paid APIs (LLM endpoints, cloud services, external SDKs) requires explicit human approval.

2. **No unbounded loops.** The `/goal` command, SDK subagent invocation, and autonomous retry loops are all governed by finite limits (`max_autonomous_goal_loops`, `max_retry_cycles`). Default values are zero or conservatively low.

3. **Budget increase requires human approval.** The agent cannot self-grant additional budget. Any increase to token limits, cost limits, retry limits, or CI watch time requires `increase_budget` human approval.

4. **CI watch is finite.** The agent may monitor CI for at most `max_ci_watch_minutes` (default: 15). After timeout, the agent must stop and report status.

5. **Artifact generation is bounded.** The agent cannot generate unlimited files or artifacts. `max_new_files`, `max_artifact_size_mb`, and `max_total_generated_artifacts_mb` enforce storage discipline.

6. **Stop conditions are mandatory.** The budget limits file defines explicit stop conditions (e.g., `estimated_cost_exceeds_budget`, `retry_limit_exceeded`). The agent must halt when any stop condition is triggered.

7. **The human remains responsible for financial decisions.** The agent operates within a pre-approved budget envelope. Any request to expand that envelope returns control to the human.
