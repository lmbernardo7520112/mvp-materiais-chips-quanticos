# ADR-017 — Manufactured Poisson Benchmark Strategy

## Status

Proposed

## Context

The project needs a rigorous numerical benchmark path before any claim of physical phi, calibration, or device prediction.

The benchmark must validate numerical consistency, not experimental truth.

## Decision

Adopt manufactured Poisson benchmark planning as the next scientific validation path.

## Benchmark Strategy

Recommended first benchmark:

1D manufactured Poisson benchmark.

Candidate manufactured solution:

u(x) = sin(pi x), x in [0, 1]

Equation form:

-u''(x) = f(x)

with:

f(x) = pi^2 sin(pi x)

Boundary conditions:

u(0) = 0
u(1) = 0

Future optional extension:

2D manufactured solution:

u(x, y) = sin(pi x) sin(pi y)

with Dirichlet boundaries.

## Required Future Metrics

* L2 error.
* Linf error.
* boundary residual.
* source residual.
* convergence slope.
* grid refinement table.
* reproducibility metadata.
* no calibration claim.
* no device prediction.

## Explicit Non-Authorization

This ADR does not authorize:

* code implementation;
* RED tests;
* benchmark runtime;
* solver runtime;
* physical phi;
* physical potential claim;
* calibration claim;
* experimental validation claim;
* device prediction;
* coherence prediction;
* AI-for-Science runtime;
* paid API;
* SDK;
* /goal.

## Consequences

Future releases may prepare RED tests only after ADR-017 acceptance.

GREEN implementation will require separate authorization.

## Rejected Alternatives

* jumping directly to experimental calibration;
* claiming physical phi from current metadata adapter;
* using device prediction as benchmark;
* using AI surrogate/PINN before classical benchmark;
* comparing to external solver before internal manufactured benchmark.
