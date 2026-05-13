---
name: ai-rse-gateops
description: >
  Use this skill when executing any critical operation in the MVP Quantum
  Materials repository. It enforces the AI-RSE (AI Research Software Engineer)
  governance standard for branch inspection, scoped changes, validation,
  evidence collection, and auditable reporting.
---

# AI-RSE GateOps — Operational Governance Skill

## When to Use

Activate this skill whenever you are asked to:

- Implement code changes (RED, GREEN, REFACTOR).
- Create, review, or merge a pull request.
- Create a release tag.
- Run quality gates or validation suites.
- Audit the repository state.
- Produce any report that claims success or failure.

## Mandatory Sequence

Follow these steps in order for every critical operation:

### 1. Inspect State

Before any change, run and record:

```bash
git checkout <branch>
git status
git log --oneline main..HEAD
git diff --name-status main
```

Confirm: correct branch, clean working tree, expected commit history.

### 2. Identify Authorized Scope

Before writing any code or docs:

- List files that **may** be altered (per the task prompt or ADR).
- List files that **must not** be altered (solvers, policy, etc.).
- If the task is ambiguous, ask before proceeding.

### 3. Execute Minimal Change

- Change only what is necessary to satisfy the task.
- Do not add features, refactors, or cleanups not requested.
- Do not alter files outside the authorized scope.

### 4. Run Local Validation

After every change, run all applicable checks:

```bash
source .venv/bin/activate

# Quality gates
PRIVATE_FORBIDDEN_TERMS_REGEX="dummy_term_that_will_never_exist_in_code" \
  PYTHONPATH=. python tools/quality_gates/run_all_quality_gates.py \
  --require-artifacts --strict-private-terms

# Full test suite
PYTHONPATH=. pytest -v --tb=short

# Coverage
PYTHONPATH=. pytest --cov=mvp_quantum_materials --cov-report=term-missing \
  --cov-fail-under=70

# Lint and format
ruff check .
ruff format --check .

# Type checking
pyright .

# Artifacts (when applicable)
python scripts/generate_all_results.py --output-dir results/figures
```

### 5. Never Declare Success Without Evidence

- Every claim must be backed by a command output you actually ran.
- Do not say "tests pass" without showing the pytest summary line.
- Do not say "CI green" without showing `gh pr checks` or `gh run list` output.
- Do not confuse local validation with remote CI.

### 6. Record Commands and Results

For every validation step, record:

- The exact command executed.
- The summary output (pass/fail count, coverage %, gate results).
- Any errors or warnings encountered.

### 7. Tag and Release Discipline

- Never create a tag before CI is green on main.
- Never confuse local CI with remote CI.
- Always verify tag is contained in main after creation.

### 8. Produce Auditable Report

Every critical operation must end with a structured report containing:

- Branch name.
- PR URL (if applicable).
- Commits included.
- Files created/modified.
- Validation results (all items from step 4).
- CI status (local vs remote, clearly distinguished).
- Scope confirmation (what was and was not changed).

## Mandatory Evidence Checklist

Before closing any task, confirm you have evidence for each applicable item:

- [ ] `git status` — clean working tree
- [ ] `git log --oneline main..HEAD` — expected commits
- [ ] `git diff --name-status main` — expected file changes
- [ ] Quality gates — 6/6 PASS
- [ ] pytest — all passed
- [ ] Coverage — ≥70%
- [ ] ruff check — PASS
- [ ] ruff format — PASS
- [ ] pyright — 0 errors
- [ ] `generate_all_results` — figures and CSVs generated (when applicable)
- [ ] `gh pr checks` — all checks passed (when PR exists)
- [ ] `gh run list --branch main` — CI green on main (when post-merge)

## Anti-Patterns

Do NOT:

- Skip validation steps to save time.
- Report "expected green" instead of actual results.
- Combine unrelated changes in a single commit.
- Create a tag on a feature branch.
- Merge without CI confirmation.
- Accept "already done" without verifiable evidence.
