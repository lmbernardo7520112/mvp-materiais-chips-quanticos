---
name: release-manager
description: >
  Use this skill when merging a PR, creating a release tag, or closing a
  release cycle. It enforces the correct sequence of merge, validation,
  CI confirmation, tagging, and reporting to prevent out-of-order releases.
---

# Release Manager — Merge/Tag/Release Discipline Skill

## When to Use

Activate this skill whenever you are asked to:

- Merge a pull request.
- Create a release tag.
- Close a release cycle.
- Validate post-merge state.

## Mandatory Release Sequence

Follow these steps **in strict order**. Do not skip or reorder.

### 1. Check PR State

```bash
gh pr view <PR_NUMBER> --json state,mergeable,statusCheckRollup
```

Confirm:
- PR exists and is open.
- PR is mergeable (no conflicts).
- All status checks are passing.

### 2. Confirm CI Checks Green

```bash
gh pr checks <PR_NUMBER> --watch
```

Wait for all checks to complete. Do **not** proceed if any check fails.

### 3. Merge with Merge Commit

```bash
gh pr merge <PR_NUMBER> --merge --delete-branch=false
```

Rules:
- **Always use `--merge`** (merge commit). Never squash.
- **Never delete the branch** (`--delete-branch=false`).

### 4. Update Local Main

```bash
git checkout main
git pull origin main
git log --oneline -10
git status
```

Confirm:
- Merge commit visible in log.
- Working tree clean.

### 5. Run Post-Merge Validation

```bash
source .venv/bin/activate

PRIVATE_FORBIDDEN_TERMS_REGEX="dummy_term_that_will_never_exist_in_code" \
  PYTHONPATH=. python tools/quality_gates/run_all_quality_gates.py \
  --require-artifacts --strict-private-terms

PYTHONPATH=. pytest -v --tb=short

PYTHONPATH=. pytest --cov=mvp_quantum_materials --cov-report=term-missing \
  --cov-fail-under=70

ruff check .
ruff format --check .
pyright .

python scripts/generate_all_results.py --output-dir results/figures
```

All checks must pass on main before tagging.

### 6. Confirm Remote CI on Main

```bash
gh run list --branch main --limit 5
```

If the merge run is still pending:

```bash
gh run watch --exit-status
```

**Do not create a tag if CI on main is pending or red.**

### 7. Create Annotated Tag

Only after CI is green on main:

```bash
git tag -a v0.X.Y -m "v0.X.Y: <description>"
git push origin v0.X.Y
```

### 8. Verify Tag

```bash
git rev-parse v0.X.Y
git branch --contains v0.X.Y
git merge-base --is-ancestor v0.X.Y main && echo "TAG_CONTAINED_IN_MAIN" \
  || echo "TAG_NOT_IN_MAIN"
git tag -l "v0.X*"
git status
```

Confirm:
- Tag resolves to a commit hash.
- Tag is contained in main.
- Working tree is clean.

### 9. Produce Final Report

Report must include:

1. PR URL.
2. PR final state (merged).
3. Merge method (merge commit).
4. Final commit on main (hash).
5. CI status on main.
6. Tag name and hash.
7. Tag contained in main.
8. Quality gates result.
9. pytest count.
10. Coverage percentage.
11. ruff result.
12. pyright result.
13. generate_all_results result.
14. Scope confirmation.
15. Working tree status.

## Prohibited Actions

- **Never squash merge.** Always use merge commit.
- **Never create a tag before CI is green on main.**
- **Never create a tag on a feature branch.**
- **Never release without a clean working tree.**
- **Never produce a report without commit hash and tag hash.**
- **Never delete a branch after merge** (preserve history).
- **Never merge if any CI check is failing.**
