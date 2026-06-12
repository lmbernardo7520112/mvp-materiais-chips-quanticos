# Release Methodology Checklist

## Purpose

Standardize AI-RSE GateOps releases and reduce redundant process overhead.

## Release Types

### 1. Documentation-only release

- Required: release notes, walkthrough update, acceptance gates.
- Optional: council, risk matrix.
- Forbidden: src changes, tests changes, scripts changes, physics implementation.
- Commands: quality gates, pytest, ruff, pyright.
- Stop: if any src/tests/scripts diff appears.
- Council mandatory: no.
- Risk matrix mandatory: no.

### 2. ADR acceptance release

- Required: ADR status update, acceptance review, council, acceptance gates, release notes.
- Optional: risk matrix.
- Forbidden: implementation code, solver coupling, calibration claims.
- Commands: quality gates, pytest, ruff, pyright.
- Stop: if implementation appears before acceptance.
- Council mandatory: yes.
- Risk matrix mandatory: no (unless physics boundary).

### 3. RED-only release

- Required: TDD plan, RED tests, RED audit, release notes, acceptance gates.
- Optional: risk matrix.
- Forbidden: production code in src/, GREEN implementation.
- Commands: quality gates, pytest (expect failures), ruff, pyright.
- Stop: if production code appears.
- Council mandatory: no.
- Risk matrix mandatory: no.

### 4. GREEN implementation release

- Required: GREEN implementation, focal tests passing, full suite green, coverage check, scope diff, release notes, acceptance gates, walkthrough update.
- Optional: council.
- Forbidden: scope leak, unauthorized file changes, solver coupling without ADR.
- Commands: quality gates, pytest, coverage, ruff, pyright, generate_all_results.
- Stop: if scope exceeds budget.
- Council mandatory: no (unless physics boundary).
- Risk matrix mandatory: no (unless new physics).

### 5. Demo/sanity release

- Required: demo script, demo tests, demo CSV/figures, release notes, acceptance gates.
- Optional: council, risk matrix.
- Forbidden: core physics mutation, solver coupling, calibration.
- Commands: quality gates, pytest, coverage, ruff, pyright, generate_all_results.
- Stop: if core physics changes.
- Council mandatory: no.
- Risk matrix mandatory: no.

### 6. Dependency decision release

- Required: dependency decision brief, pyproject update (if accepted), CI validation, release notes.
- Optional: council.
- Forbidden: adding dependency without brief.
- Commands: quality gates, pytest, ruff, pyright, pip install verification.
- Stop: if dependency added without decision.
- Council mandatory: no (unless major dependency).
- Risk matrix mandatory: no.

### 7. Closure/tag release

- Required: PR merge, CI main green, tag, closure report.
- Forbidden: tag before CI main, squash merge, tag without containment check.
- Commands: gh pr checks, git merge-base --is-ancestor, git tag.
- Stop: if CI main not green.
- Council mandatory: no.
- Risk matrix mandatory: no.

## Fast Lanes

- **Fast Lane A** — Documentation-only simple: no council, no risk matrix, no ADR.
- **Fast Lane B** — Demo/sanity checks: TDD plan, demo tests, no council required.
- **Fast Lane C** — Safe refactor: no output change, before/after validation.

## Slow Lane Mandatory Triggers

- solver coupling;
- physical phi;
- calibration;
- new dependency;
- policy change;
- pyproject change;
- quantum confinement;
- new experimental data;
- device prediction;
- boundary condition changes.

## Universal Pre-PR Checklist

- [ ] Scope diff reviewed.
- [ ] AI failure mode review completed.
- [ ] Evidence metrics refreshed.
- [ ] Dependency check completed.
- [ ] Quality gates PASS.
- [ ] pytest PASS.
- [ ] ruff PASS.
- [ ] pyright 0 errors.
- [ ] generate_all_results PASS.
- [ ] Human decision recorded if needed.
