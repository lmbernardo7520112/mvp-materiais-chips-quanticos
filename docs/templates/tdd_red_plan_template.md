# TDD RED Plan Template

## Goal

[What behavior is being specified?]

## Authorized By

[ADR reference or governance decision]

## Future Module

[Target file in src/ that does not yet exist]

## Physical Contract

[What physical claim is allowed? What is blocked?]

## Dimensional Contract

[What units must be preserved?]

## Computational Contract

[What API behavior is required?]

## Governance Contract

[What must remain blocked during this phase?]

## Non-goals

[What must not be implemented?]

## Tests

| Test Name | Contract Type | Expected Failure |
|-----------|---------------|------------------|
| | | ModuleNotFoundError / AssertionError |

## Expected RED Failure

- Total tests: [N]
- Expected failed: [N]
- Expected passed: [N] (static/governance checks only)
- Failure reason: [ModuleNotFoundError — target module absent]

## Audit Requirements

- [ ] No production code exists.
- [ ] Target module absent.
- [ ] No scope leak.
- [ ] Failure reasons documented.
