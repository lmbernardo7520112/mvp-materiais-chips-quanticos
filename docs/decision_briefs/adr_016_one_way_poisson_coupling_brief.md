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

## v0.8.5 Scope

This release (v0.8.5) is **documentation-only**. ADR-016 status remains **Proposed**.

v0.8.5 does not authorize:

* Implementation of any kind.
* Poisson runtime or solver coupling.
* Physical phi interpretation.
* Dummy phi outputs.
* Potential grid generation.
* Calibration claims or device prediction.
* AI-for-Science runtime, PINN, or surrogate models.

Any future implementation requires ADR-016 acceptance review, TDD RED/GREEN phases, explicit no-physical-phi guardrails, and full CI validation.
