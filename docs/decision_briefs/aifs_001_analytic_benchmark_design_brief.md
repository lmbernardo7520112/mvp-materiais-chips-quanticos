# AIFS-001 Analytic Benchmark Design Brief

## Core Question

Should the AI-for-Science track advance now?

## Answer

Yes, but only as analytic benchmark design.

## Why Not PINN Runtime Now?

* no accepted AIFS benchmark ADR;
* no dependency decision;
* no baseline implementation;
* no RED tests;
* no reproducibility protocol;
* no uncertainty/error threshold;
* no reason to involve project C1/C2/C3;
* high risk of overclaim.

## Options

| Option  | Description                               | Scientific value | Contamination risk | Readiness | Governance fit | Score |
| ------- | ----------------------------------------- | ---------------: | -----------------: | --------: | -------------: | ----: |
| AIFS-B1 | 1D Poisson manufactured solution design   |              8.5 |                1.0 |       9.0 |            9.5 |    93 |
| AIFS-B2 | 1D diffusion manufactured solution design |              8.0 |                1.0 |       8.5 |            9.0 |    90 |
| AIFS-B3 | 2D Poisson analytic benchmark design      |              8.5 |                2.0 |       7.0 |            8.5 |    84 |
| AIFS-B4 | Isolated PINN prototype now               |              7.0 |                7.0 |       3.0 |            4.0 |    45 |
| AIFS-B5 | Add PyTorch/JAX now                       |              6.0 |                8.5 |       3.0 |            3.0 |    35 |
| AIFS-B6 | Surrogate for project solver now          |  8.0 theoretical |                9.0 |       2.0 |            2.0 |    25 |

## Recommendation

Proceed with AIFS-B1 documentation-only.

Do not implement PINN.

Do not add ML dependencies.

Do not touch C1/C2/C3.
