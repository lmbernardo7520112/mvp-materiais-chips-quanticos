# AIFS-001 — AI-for-Science Analytic Benchmark Design

## Summary

Creates a documentation-only benchmark design for a future isolated AI-for-Science prototype.

## Added

* ADR-015 Proposed.
* Decision brief.
* Analytic benchmark specification.
* Risk matrix.
* Future RED plan.
* Acceptance gates.
* HDL-010.

## Benchmark

1D Poisson manufactured solution:

-u''(x) = f(x)

u(x) = sin(pi x)

f(x) = pi² sin(pi x)

u(0) = u(1) = 0

## Not Implemented

* no code;
* no tests;
* no scripts;
* no notebook;
* no PINN;
* no surrogate;
* no ML dependency;
* no training;
* no inference;
* no project physics coupling;
* no C1/C2/C3 import;
* no physical phi;
* no calibration;
* no device prediction.

## Relationship to C3

No interaction with v0.8.2 C3 RED.

C3 remains canonical.
