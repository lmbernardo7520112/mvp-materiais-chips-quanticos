# Parameter Candidates — v0.4 Poisson Bridge

> **Date:** 2026-05-10
> **Status:** Demonstrative / Uncalibrated
> **ADR:** ADR-007 (Accepted)

## Overview

The v0.4 Poisson Bridge introduces new parameters for the effective charge
closure and the 2D Poisson solver. **All parameters are demonstrative and
uncalibrated.** They exist only to validate the computational pipeline structure.

## Effective Charge Parameters (`EffectiveChargeParams`)

| Parameter | Default | Unit | Nature | Evidence Tier |
|-----------|---------|------|--------|---------------|
| `q` | 1.602e-19 | C | Physical constant | T0 (exact) |
| `N_ref` | 1.0 | dimensionless | Scale proxy | TX (demonstrative) |
| `lambda_T` | 0.0 | dimensionless | Thermal weight | TX (demonstrative) |
| `lambda_C` | 1.0 | dimensionless | Defect weight | TX (demonstrative) |
| `C_sat` | 1.0 | dimensionless | Saturation cap | TX (demonstrative) |
| `t_eff` | 1.0 | dimensionless | Effective thickness | TX (demonstrative) |
| `T_ref` | None | K | Reference temperature | TX (not used) |
| `delta_T_ref` | None | K | Temperature scale | TX (not used) |

## Poisson Solver Parameters

| Parameter | Default | Unit | Nature | Evidence Tier |
|-----------|---------|------|--------|---------------|
| `epsilon` | 1.0 | dimensionless | Permittivity proxy | TX (demonstrative) |
| `dx` | Lx/(nx-1) | dimensionless | Grid spacing x | Derived |
| `dy` | Ly/(ny-1) | dimensionless | Grid spacing y | Derived |
| `max_iter` | 20000 | — | Iteration limit | Numerical |
| `tolerance` | 1e-8 | — | Convergence threshold | Numerical |

## Script Parameters (`run_poisson_bridge.py`)

| Parameter | Value | Nature |
|-----------|-------|--------|
| `nx, ny` | 41, 41 | Grid resolution |
| `Lx, Ly` | 1.0, 1.0 | Domain size (a.u.) |
| `C_def` | 0.5 + 0.25·sin(πx)·sin(πy) | Demonstrative field |
| `T` | 300 + 10·sin(πx)·sin(πy) | Demonstrative field |

## Calibration Status

> [!CAUTION]
> **None of the v0.4 parameters are calibrated against experimental data.**
> They are chosen solely to exercise the computational pipeline and validate
> numerical convergence. Any comparison with real semiconductor physics
> requires proper calibration, which is outside the scope of this MVP.

## Future Calibration Path (out of scope)

If calibration were pursued in a future version, it would require:

1. Literature values for ε(Si), ε(SiGe), ε(oxide) at relevant temperatures.
2. Experimentally measured defect densities from DLTS, C-V, or SPM.
3. Proper unit conversion from dimensionless proxies to SI.
4. Validation against TCAD benchmarks.
5. A new ADR authorizing calibrated claims.
