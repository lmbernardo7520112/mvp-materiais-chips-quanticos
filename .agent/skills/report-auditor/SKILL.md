---
name: report-auditor
description: >
  Use this skill to audit reports produced by the agent itself or by previous
  sessions. It checks for consistency between claims and evidence, detects
  counting errors, scope creep, and out-of-order operations.
---

# Report Auditor — Self-Audit and Verification Skill

## When to Use

Activate this skill whenever you are asked to:

- Verify a previous session's report.
- Audit a release report for accuracy.
- Cross-check claims against actual repository state.
- Review a walkthrough or project audit document.

## Audit Principles

### 1. Separate Evidence from Assertion

For every claim in a report, ask:

- **What command was run** to produce this evidence?
- **What was the actual output** of that command?
- **Does the output actually support the claim?**

Example of a bad claim:
> "All tests pass." (No pytest output shown.)

Example of a good claim:
> "All tests pass: `179 passed in 22.13s`" (with actual output.)

### 2. Verify Commands Actually Prove Claims

Check that:

- A `pytest` summary line is shown, not just "tests pass."
- A `coverage` percentage is shown, not just "coverage meets threshold."
- A `gh pr checks` output is shown, not just "CI green."
- A `git log` output is shown, not just "commit exists."

### 3. Detect Counting Inconsistencies

Cross-reference:

- Test count in report vs. pytest output.
- File count in report vs. `git diff --name-status` output.
- Coverage percentage in report vs. coverage tool output.
- Gate pass count in report vs. quality gates output.

Known historical issue: v0.4.4 release report had swapped test counts
(listed 17/14, actual was 12/19). This was corrected in v0.4.5.

### 4. Verify Correct Files Were Changed

Run:

```bash
git diff --name-status main
```

Check:

- Are only authorized files listed?
- Are any files changed that should not be?
- Does the report accurately list all changed files?

### 5. Verify Corrections Were Actually Made

If a report claims a correction was made:

```bash
git diff <before_commit>..<after_commit> -- <file>
# or
grep -n "<corrected_content>" <file>
```

Never accept "already fixed" without verifiable evidence.

### 6. Classify Report Quality

After auditing, classify the report as:

| Classification | Meaning |
|---------------|---------|
| **Approved** | All claims verified, no issues found |
| **Microcorrect** | Minor inaccuracies, fixable without re-implementation |
| **Reject** | Material inaccuracies, missing evidence, or scope violations |

### 7. Distinguish Local vs Remote CI

A report must clearly distinguish:

- **Local validation:** pytest, ruff, pyright run on the developer's machine.
- **Remote CI:** GitHub Actions checks triggered by push/PR.

Saying "CI green" without specifying which is ambiguous and should be flagged.

### 8. Verify Tag/Merge Order

Check that:

- Tag was created **after** merge to main.
- Tag was created **after** CI green on main.
- Tag is contained in main (`git merge-base --is-ancestor`).
- No tag exists on a feature branch.

### 9. Detect Scope Creep

Check if:

- Files outside the authorized scope were modified.
- Policy changes were made without authorization.
- Physics or solver code was altered when the task was documentation-only.
- Option C was initiated when not authorized.

## Audit Checklist

When auditing any report, verify each applicable item:

- [ ] PR URL exists and is accessible?
- [ ] CI green (remote, not just local)?
- [ ] New commit exists with expected hash?
- [ ] `git diff` matches the claimed scope?
- [ ] Test count matches pytest output?
- [ ] Coverage matches coverage tool output?
- [ ] Policy unchanged (if scope says so)?
- [ ] src/scripts/tests altered only as authorized?
- [ ] Tags created at the correct point in sequence?
- [ ] No confusion between local and remote CI?
- [ ] Working tree clean at end?
- [ ] All corrections verifiable by diff/grep/commit?

## Common Audit Failures

| Failure | How to Detect |
|---------|--------------|
| Test count mismatch | Compare report count vs. `pytest -v` output |
| "Already done" without evidence | Ask for diff or commit hash |
| Tag before CI | Check `gh run list` timestamps vs tag creation |
| Scope creep | `git diff --name-only main` shows unauthorized files |
| Local/remote CI confusion | Report says "CI green" without `gh` command output |
| Missing validation step | Checklist item not backed by command output |
