# ADR-016 — One-way Poisson Coupling Strategy

## Status

Proposed

## Date

2026-06-13

## Context

v0.8.4 successfully implemented the C3 Conservative Grid Projection logic. Charge from C2 (derived from C1 D_it) is safely projected onto a continuous grid, conserving total charge and sign, while enforcing strict domain isolation.
The projection module does not currently solve Poisson's equation, couple with `poisson_solver_2d`, or produce physical `phi` output.
The next architectural step requires feeding this projected interface charge into the classical Poisson solver to demonstrate an electrostatic response, completing the pipeline C1 -> C2 -> C3 -> Poisson. 

## Core Question

How should the projected C3 charge grid be coupled with the Poisson solver to demonstrate electrostatic response without violating scale constraints (Option B) or introducing self-consistency before it is authorized?

## Options Considered

### Option 1: One-way Demonstrative Coupling (Recommended)

**Description:**
* Execute `poisson_solver_2d` using the projected charge grid as the source term (rho).
* Pass the demonstrative Option B literature-scaled variables to the solver.
* Solve Poisson's equation once (no self-consistent loop between potential and D_it filling).
* Output a dummy potential `phi_dummy` strictly marked as `demonstrative` and `not_for_physical_interpretation`.

**Pros:**
* Bridges C3 and the existing Poisson solver.
* Establishes the pipeline architecture.
* Preserves safety constraints (no false physical claims).
* Follows existing Option B precedent.

**Cons:**
* Lacks physical feedback (charging of interface states due to shifting Fermi level).

### Option 2: Self-Consistent Coupling (Rejected)

**Description:**
* Iteratively solve Poisson's equation and update the filled fraction of D_it based on the resulting local potential until convergence.

**Motivo:**
* Violates current scope. Self-consistency is explicitly deferred to v0.5+ by ADR-007 and Scope Guardrails.
* Entails high physical claim risk before validation metrics exist.

### Option 3: Two-Way Coupling with Drift-Diffusion (Rejected)

**Description:**
* Couple Poisson output with carrier transport equations (drift-diffusion).

**Motivo:**
* Out of scope. Transport is not currently modeled.

## Decision

Propose Option 1: One-way Demonstrative Coupling.

This ADR proposes future implementation of the one-way coupling. 
**This ADR is currently documentation-only. No implementation is authorized until this ADR is accepted and a formal RED phase is initiated.**

## Consequences

* The system will gain a complete, albeit demonstrative, forward path from defect distribution to electrostatic potential.
* Test coverage will need to ensure self-consistency loops are NOT accidentally invoked.
* Output artifacts must clearly flag the potential as `demonstrative`.
* Physical interpretation remains blocked until a dedicated posterior ADR.
* Any eventual solver output must be treated as a demonstrative numerical field, not as a physically calibrated potential.

## Non-Authorization Clause

ADR-016, while Proposed, does not authorize:

* code changes;
* tests;
* Poisson runtime;
* solver coupling;
* physical phi interpretation;
* dummy phi;
* potential grid;
* voltage output;
* electrostatic potential output;
* quantum confinement;
* calibration claims;
* device prediction;
* AI-for-Science runtime.

Any future implementation requires:

* ADR-016 acceptance review;
* RED phase;
* GREEN phase;
* explicit no-physical-phi guardrails;
* full validation and CI.
