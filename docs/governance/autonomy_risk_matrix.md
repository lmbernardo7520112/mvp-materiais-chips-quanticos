# Autonomy Risk Matrix

## Purpose

Identifies risks introduced by agentic autonomy and defines mitigations to ensure the agent cannot bypass scientific governance.

## Risk Register

| ID | Risk | Severity | Likelihood | Mitigation |
| :--- | :--- | :--- | :--- | :--- |
| R1 | Agent merges PR without human authorization. | **Critical** | Low | `human_approval_required_for` must always include `merge_pr`. State validator rejects state files missing this gate. GitHub branch protection rules require manual approval. |
| R2 | Agent creates tag without human authorization. | **Critical** | Low | `human_approval_required_for` must always include `create_tag`. State validator enforces this. Tag creation requires authenticated push. |
| R3 | Agent accepts ADR prematurely (promotes Proposed → Accepted without review). | **Critical** | Medium | `human_approval_required_for` must always include `accept_adr`. Council and acceptance review documents must exist before any status change. |
| R4 | Agent alters `pyproject.toml` without dependency decision brief. | **High** | Medium | `pyproject.toml` is in `forbidden_paths` for all release types except GREEN (where it requires `change_pyproject` human approval). Scope checker flags it as hardcoded guard. |
| R5 | Agent alters `policy.json` to make quality gates pass. | **Critical** | Low | `policy.json` is a hardcoded guard in the scope checker. Any modification is flagged regardless of state file. `human_approval_required_for` includes `change_policy`. |
| R6 | Agent reduces test assertions or removes tests to pass CI. | **High** | Medium | RED tests are contracts. The `minimal-red-contract` skill requires tests to encode physical, dimensional, and computational invariants. Post-merge test count must be monotonically non-decreasing (enforced by quality gates). |
| R7 | Agent creates `physical_phi` by inference (e.g., naming a variable `phi` and claiming it represents electrostatic potential). | **Critical** | Medium | `forbidden_terms` includes `physical_phi`. The `scope-guardrails` skill blocks physical interpretation claims. The `physics-dimensional-audit` skill requires all outputs to carry explicit `physical_interpretation_allowed=False` metadata. |
| R8 | Agent initiates Poisson runtime outside ADR authorization. | **Critical** | Low | `forbidden_terms` includes patterns for Poisson solver imports. `blocked_actions` includes `enable_poisson_runtime`. Scope checker scans added lines for solver imports. |
| R9 | Agent uses SDK/subagents without auditability (opaque delegated execution). | **High** | Low (blocked currently) | Multi-agent execution is not authorized in this release. The `blocked_actions` list includes any SDK invocation. Future multi-agent releases require a separate ADR with audit trail requirements. |
| R10 | State machine becomes stale (agent operates with outdated permissions). | **Medium** | High | The state file is committed to git and versioned. The agent must re-read the state file at the start of every session. The human must update the state file when transitioning between releases. |
| R11 | Token/cost budget exceeded without detection. | **High** | Medium | Budget limits file defines `max_total_estimated_cost_brl`. Budget validator checks that cost field exists and is finite. Stop condition `estimated_cost_exceeds_budget` halts execution. |
| R12 | Autonomous SDK call creates unexpected billing. | **Critical** | Low | `external_paid_api_allowed` is false by default. `use_paid_api` and `use_external_sdk` require human approval. `blocked_actions` includes `paid_api_without_budget` and `sdk_without_approval`. |
| R13 | Unlimited `/goal` loop burns tokens and time. | **High** | Medium | `max_autonomous_goal_loops` defaults to 0. `enable_goal_mode` requires human approval. `blocked_actions` includes `unlimited_goal_loop`. |
| R14 | Repeated CI retries consume resources. | **Medium** | Medium | `max_retry_cycles` capped at 0-5. `max_ci_watch_minutes` capped at 1-60 (default 15). `blocked_actions` includes `unbounded_retry` and `unbounded_ci_watch`. |
| R15 | Large generated artifacts increase storage/cost. | **Medium** | Low | `artifact_budget` limits `max_new_files`, `max_artifact_size_mb`, and `max_total_generated_artifacts_mb`. |
| R16 | Budget silently increased by agent. | **Critical** | Low | `requires_human_approval_to_increase_budget` must be true. `blocked_actions` includes `autonomous_budget_increase`. Budget validator rejects state files missing this flag. |

## Residual Risk Assessment

Even with all mitigations, the following residual risks remain:

1. **Context window decay** may cause the agent to forget skill constraints mid-session. Mitigation: state file re-read at each invocation, plus CI as independent hard gate.
2. **Novel violation patterns** not covered by `forbidden_terms` regex. Mitigation: human review of every PR before merge; periodic audit of `forbidden_terms` adequacy.
3. **State file tampering by agent.** Mitigation: the agent is instructed never to self-grant permissions. Git diff auditing catches unauthorized state modifications.
4. **Cost estimation inaccuracy.** The agent cannot precisely predict token or API costs at planning time. Mitigation: default monetary budget is zero; any non-zero budget requires explicit human approval with documented justification.
