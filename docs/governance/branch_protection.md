# Branch Protection — main

> **Status:** Active since v0.3.1
> **Configured via:** GitHub Branch Protection Rules (API)

## Purpose

The `main` branch is the **Single Source of Truth (SSOT)** for the project.
Branch protection ensures that no code reaches `main` without passing all
required quality gates, preventing regressions, scope creep, and unreviewed
changes.

## Active Rules

| Rule | Setting |
|------|---------|
| Require a pull request before merging | ✅ Enabled |
| Required status checks | ✅ `quality (3.11)`, `quality (3.12)` |
| Require branches to be up to date | ✅ Strict mode |
| Require conversation resolution | ✅ Enabled |
| Allow force pushes | ❌ Blocked |
| Allow deletions | ❌ Blocked |
| Enforce admins | ❌ Not enforced (owner bypass for emergencies) |

## What the Required Checks Cover

Each `quality (3.X)` job in CI runs the following steps sequentially:

1. **pytest** — all tests must pass.
2. **pytest --cov** — coverage must be ≥ 70%.
3. **ruff check** — zero lint violations.
4. **ruff format --check** — zero formatting issues.
5. **pyright** — zero type errors.
6. **generate_all_results** — all figures and CSVs generated.
7. **AI-RSE Quality Gates** — all 6 gates must pass, including:
   - ADR status
   - Scope guardrails
   - Solver integrity
   - Required docs
   - Artifacts
   - Strict private forbidden terms (via `PRIVATE_FORBIDDEN_TERMS_REGEX` secret)

## How to Update Required Checks

If CI jobs are renamed or new checks are added:

1. Go to **Settings → Branches → main** in the GitHub UI.
2. Edit the branch protection rule.
3. Update the required status checks list.
4. Or use the GitHub API:

```bash
gh api repos/OWNER/REPO/branches/main/protection \
  --method PUT \
  --input protection.json
```

## When a Check Fails

1. Read the CI log to identify the failing step.
2. Fix the issue in the feature branch.
3. Push the fix — checks will re-run automatically.
4. **Never** disable a check to unblock a merge.
5. **Never** use `continue-on-error` to bypass a gate.
6. If a gate is genuinely outdated, update it via a dedicated PR with ADR justification.

## Relationship with AI-RSE GateOps

Branch protection is the **enforcement layer** for AI-RSE GateOps:

```
ADR (Decision) → Policy Update (Governance) → PR (Implementation) → CI + Gates (Validation) → Merge (SSOT)
```

The quality gates in `tools/quality_gates/` define **what** is checked.
Branch protection ensures those checks **cannot be bypassed**.

## Emergency Procedures

If a critical fix must reach `main` urgently:

1. The repository owner can bypass protection (enforce_admins is not enabled).
2. Any bypass must be documented in the next PR with justification.
3. Bypasses must never disable gates permanently.

## Repository Visibility Decision

> **Decision date:** 2026-05-09
> **Decision:** Keep repository **public**.

### Rationale

The repository was changed from private to public to enable GitHub Branch
Protection Rules, which are not available on the GitHub Free plan for private
repositories. This is a deliberate trade-off:

| Factor | Assessment |
|--------|------------|
| **Benefit** | Branch protection with required CI checks enforced on `main` |
| **Trade-off** | Code, CI logs, and repository history are publicly visible |
| **Risk: secrets in code** | ✅ **None found** — audited 2026-05-09 |
| **Risk: tokens/keys** | ✅ **None found** — no `ghp_`, `github_pat_`, `sk-`, or PEM keys |
| **Risk: email addresses** | ✅ **None found** |
| **Risk: private terms** | ✅ **Mitigated** — `PRIVATE_FORBIDDEN_TERMS_REGEX` stored as GitHub Secret only, never in repo; CI output redacted |
| **Risk: local paths** | ⚠️ **One reference** to local workspace path in `implementation_plan.md` — acceptable (no security impact) |

### Mitigations

1. **Strict private terms gate** — CI blocks any code containing forbidden
   terms, with redacted output that never leaks the regex or matched content.
2. **GitHub Secrets** — sensitive values stored exclusively as repository
   secrets, never committed to files.
3. **Branch protection** — prevents unreviewed code from reaching `main`.
4. **Scope guardrails** — AI-RSE GateOps blocks out-of-order physics
   implementation.
5. **Regular audits** — exposure audits should be performed before each
   minor release.

### Alternative for Future

If the repository must return to private (e.g., for IP protection or
institutional requirements), upgrade to **GitHub Pro**, **Team**, or
**Enterprise** to retain branch protection on private repositories.

```bash
# To revert to private (requires GitHub Pro or higher):
gh repo edit --visibility private
```
