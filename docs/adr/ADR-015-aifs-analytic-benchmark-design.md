# ADR-015 — AI-for-Science Analytic Benchmark Design

## Status

Proposed

## Date

2026-06-13

## Context

ADR-014 opened an AI-for-Science track as a parallel, exploratory, documentation-first path.

The project must not implement PINNs, surrogates, ML dependencies, training, inference, or solver replacement before analytic benchmarks and governance contracts exist.

The classical track remains canonical.

## Core Question

What analytic benchmark should be designed before any future AI-for-Science prototype?

## Decision Direction

Propose AIFS-001:

A documentation-only analytic benchmark design based on a simple 1D manufactured Poisson problem.

## Benchmark Candidate

### AIFS-B1 — 1D Poisson Manufactured Solution

Domain:

x ∈ [0, 1]

Exact solution:

u(x) = sin(pi x)

Boundary conditions:

u(0) = 0
u(1) = 0

Example operator convention:

-u''(x) = f(x)

Then:

f(x) = pi² sin(pi x)

Alternative conventions must explicitly document sign.

## Why This Benchmark

* analytic solution known;
* simple boundary conditions;
* deterministic;
* no project physics coupling;
* suitable for future baseline comparison;
* can test residual error;
* can test boundary condition enforcement;
* can test reproducibility;
* does not require experimental data.

## What This Does Not Authorize

* no code;
* no tests;
* no PINN;
* no surrogate;
* no ML dependency;
* no notebook;
* no training;
* no inference;
* no solver replacement;
* no C1/C2/C3 import;
* no Poisson runtime from project solver;
* no physical phi;
* no calibration;
* no device prediction.

## Future Gates Before Any Prototype

A future prototype requires:

1. ADR acceptance.
2. Dependency decision, if any ML package is proposed.
3. RED tests.
4. Classical or analytic baseline.
5. Explicit error metrics.
6. Reproducibility controls.
7. Human decision log.
8. Isolation from C1/C2/C3.
9. No project-physics claims.
10. Rollback plan.

## Relationship to Classical Track

The classical track remains canonical.

AIFS-B1 is only a benchmark design.

AIFS outputs cannot become source of truth.

## Relationship to C3

No C3 imports.

No C3 dependency.

No interaction with v0.8.2 RED.

C3 and AIFS proceed in parallel but remain isolated.
