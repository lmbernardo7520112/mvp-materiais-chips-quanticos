---
name: tdd-red-green-release
description: >
  Use this skill when implementing any feature or fix using Test-Driven
  Development (TDD). It enforces the RED-GREEN-REFACTOR cycle with strict
  phase separation, commit discipline, and release readiness checks.
---

# TDD RED-GREEN-RELEASE — Test-Driven Development Skill

## When to Use

Activate this skill whenever you are asked to:

- Create new tests (RED phase).
- Implement code to make tests pass (GREEN phase).
- Refactor or prepare a release after GREEN (REFACTOR/DOCS phase).

## Phase 1: RED — Specify Before Implementing

### Rules

1. **Create tests first.** Write test files that specify the desired behavior.
2. **Prove correct failure.** Run the tests and confirm they fail for the
   right reason (e.g., `ImportError`, `AssertionError`, missing function).
3. **Do not implement.** During RED, do not modify `src/` or `scripts/`.
   Only create/modify test files and documentation.
4. **Record failure.** Register the failure count and reasons in the
   walkthrough or task document.
5. **Commit RED separately.** Use a commit message like:
   `test: add v0.X.Y <feature> red specifications`

### RED Checklist

- [ ] Test files created.
- [ ] Tests run and fail correctly.
- [ ] No implementation code written.
- [ ] Failure reasons documented.
- [ ] RED commit created.

## Phase 2: GREEN — Implement the Minimum

### Rules

1. **Implement only what is needed** to make the RED tests pass.
2. **Run target tests first.** Confirm the specific tests now pass.
3. **Run broader suite.** Confirm no regressions in related test files.
4. **Preserve scope.** Do not alter files outside the authorized scope.
5. **Validate lint/type.** Run `ruff check`, `ruff format --check`, `pyright`.
6. **Commit GREEN separately.** Use a commit message like:
   `feat: implement v0.X.Y <feature> <component>`

### GREEN Checklist

- [ ] Target tests pass.
- [ ] Broader test suite passes.
- [ ] ruff check PASS.
- [ ] ruff format PASS.
- [ ] pyright 0 errors.
- [ ] No unauthorized file changes.
- [ ] GREEN commit created.

### GREEN Sub-phases

For complex features, split GREEN into numbered sub-phases:

- **GREEN 1:** Core helpers/functions.
- **GREEN 2:** Integration (e.g., runtime script changes).
- **GREEN 3:** Global validation and PR readiness.

Each sub-phase gets its own commit and validation cycle.

## Phase 3: REFACTOR/DOCS — Prepare for Release

### Rules

1. **Run full validation suite.** Quality gates, pytest, coverage, ruff,
   pyright, generate_all_results.
2. **Update documentation.** Walkthrough, project_audit, technical_debt,
   release notes.
3. **Prepare PR.** Push branch, create PR with structured body.
4. **Do not create tag.** Tags are created only after merge + CI green on main.

### REFACTOR/DOCS Checklist

- [ ] Full suite green (179+ tests).
- [ ] Coverage ≥70%.
- [ ] Quality gates 6/6 PASS.
- [ ] Documentation updated.
- [ ] PR created.
- [ ] CI green on PR.

## Prohibited Actions

- **Never weaken a test to make it pass.** Fix the implementation, not the test.
- **Never skip RED.** Every feature must start with failing tests.
- **Never alter files outside scope.** Check authorized files before editing.
- **Never mix implementation with release/tag.** Separate concerns.
- **Never commit RED and GREEN in the same commit.** Phase discipline matters.
- **Never declare GREEN without running tests.** Show the pytest output.

## Commit Message Convention

| Phase | Pattern |
|-------|---------|
| RED | `test: add v0.X.Y <feature> red specifications` |
| GREEN | `feat: implement v0.X.Y <feature> <component>` |
| Micro-correction | `docs: <description>` or `fix: <description>` |
| Documentation | `docs: finalize v0.X.Y <feature> documentation` |
| Infrastructure | `chore: <description>` |
