# Autonomy-001 Decision Brief — Agentic State Machine

## Decision

Introduce a file-based state machine (`.agent/workflow_state.json`) and scope-checking scripts to reduce human micro-orchestration of AI-RSE release operations.

## Context

The audit of AI-RSE skill utilization (2026-06-14) concluded that the 12 agent skills are highly effective for governance (zero scientific violations, zero unauthorized dependency additions) but require the human to manually orchestrate every diff, validation, check, and PR step. The human acts as the "state controller" of the release machine.

## Proposed Solution

1. A JSON state file records current release, phase, allowed/forbidden paths, forbidden terms, required checks, and human-approval gates.
2. A state validator (`validate_workflow_state.py`) ensures the state file is structurally sound and that critical actions always require human approval.
3. A scope checker (`check_release_scope.py`) inspects `git diff` output against the state file's constraints, blocking forbidden-path modifications and forbidden-term introductions.
4. Release rules (`.agent/release_rules.yaml`) define per-release-type policies.

## Alternatives Considered

| Alternative | Decision | Rationale |
| :--- | :--- | :--- |
| Multi-agent SDK (Antigravity) | Deferred | Requires separate ADR, audit trail design, and maturity assessment. Too early for current project stage. |
| `/goal` command for autonomous loops | Deferred | Assumes `/goal` reliability and auditability that has not been validated. |
| No autonomy — keep current manual orchestration | Rejected | Unsustainable cognitive burden on human; does not scale. |
| Full auto-merge and auto-tag | Rejected | Violates human-in-the-loop principle for irreversible decisions. |

## Risks

See `docs/governance/autonomy_risk_matrix.md` for the full 16-risk matrix.

## Acceptance Criteria

See `docs/governance/autonomy_acceptance_gates.md` for 47 gates.

## Constraints

- No scientific code changes.
- No dependency changes.
- Human approval required for all irreversible actions.
- Skills remain authoritative; state machine is operational only.

## Budget Decision

Autonomy-001 authorizes no paid API usage and no external SDK usage. Any future paid or token-consuming automation requires explicit budget approval. The default monetary budget is zero BRL. The `/goal` command and subagent SDK are blocked by default and require `enable_goal_mode` human approval.
