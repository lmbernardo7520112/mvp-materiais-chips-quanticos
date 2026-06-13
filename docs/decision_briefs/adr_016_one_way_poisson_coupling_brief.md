# Decision Brief: ADR-016 One-way Poisson Coupling Strategy

## Context

With C3 projection in place (v0.8.4), the charge distribution is ready on a grid. To demonstrate electrostatic response without overclaiming capabilities, a strictly controlled coupling to the Poisson solver is required.

## Proposal

Implement a one-way, non-self-consistent pass of the projected charge through `poisson_solver_2d`.

## Constraints & Guardrails

* **One-Way Only**: No feedback loop updating D_it filling.
* **Demonstrative Output**: The resulting potential must be explicitly flagged as `dummy` and `not_for_physical_interpretation`.
* **Option B Scale**: Must continue using literature-scaled SI constants without asserting device calibration.
* **No ML/AI**: AI-for-Science track remains separate.

## Expected Outcomes

* A functioning pipeline connecting C1 (D_it), C2 (Mapping), C3 (Projection), and Poisson (Electrostatics).
* Clear metrics on solver performance and convergence for a single pass.
* Groundwork laid for future exploration of self-consistent coupling (v0.5+).

## Next Actions

1. Propose ADR-016 (Done).
2. Convene council for ADR-016 review.
3. If accepted, initiate C3 Poisson Coupling RED phase.
