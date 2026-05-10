# Parameter Taxonomy — v0.3.5 Curated Candidates

> **Date:** 2026-05-09
> **Scope:** Classification of all MVP parameters by evidence tier
> **Status:** SPECIFICATION — no implementation changes

## Evidence Tiers

| Tier | Label | Definition |
|------|-------|------------|
| **T0** | toy/demonstrative | Arbitrary value for numerical demonstration only |
| **T1** | literature-inspired | Order of magnitude from literature; not calibrated |
| **T2** | candidate physical range | Published range exists; calibration feasible in principle |
| **T3** | calibration-required | Meaningful only with experimental calibration |
| **TX** | forbidden-to-interpret-physically | Must not be presented as physical quantity |
| **CONST** | physical constant | Exact or CODATA value; not a free parameter |

---

## v0.1 Parameters (1D Thermal + Diffusion)

| Symbol | Current Role | Current Value | Evidence Tier | Possible Physical Interpretation | Source Role | Allowed v0.3 | Allowed v0.4 | Caveat |
|--------|-------------|---------------|---------------|----------------------------------|-------------|-------------|-------------|--------|
| L | Domain length | 0.01 m | T0 | Wafer thickness or die dimension | not applicable | ✅ | ✅ | Numerical convenience |
| nx | Grid nodes | 101 | T0 | Resolution parameter | not applicable | ✅ | ✅ | Numerical convenience |
| α | Thermal diffusivity | 8.8e-5 m²/s | T1 | Si thermal diffusivity at ~300 K | parameter-source | ✅ | ✅ | Literature order-of-magnitude; temperature-dependent in reality |
| T_left | Left BC | 1700 K | T0 | Hot-zone temperature | not applicable | ✅ | ✅ | Toy value; CZ growth uses ~1685 K melt point |
| T_right | Right BC | 1400 K | T0 | Cold-zone temperature | not applicable | ✅ | ✅ | Toy value |
| T_init | Initial temperature | 1500 K | T0 | Average starting condition | not applicable | ✅ | ✅ | Toy value |
| t_total | Total time | 1.0 s | T0 | Observation window | not applicable | ✅ | ✅ | Numerical convenience |
| safety_factor | CFL factor | 0.4 | T0 | Stability margin | not applicable | ✅ | ✅ | Must be < 0.5 for Euler explicit |
| D₀ | Diffusion pre-exponential | 1.0e-8 m²/s | T0 | Impurity diffusivity pre-factor | parameter-source | ✅ | ✅ | Toy; real D₀ varies by species |
| E_a | Activation energy | 0.5 eV | T0 | Migration energy | parameter-source | ✅ | ✅ | Toy; Si vacancy E_m ≈ 0.2–0.5 eV |
| k_B | Boltzmann constant | 8.617e-5 eV/K | CONST | Physical constant | physical constant | ✅ | ✅ | CODATA value; not a free parameter |
| T_c | Critical temperature | 1500 K | T0 | Nucleation temperature | not applicable | ✅ | ✅ | Toy; void nucleation ~1100°C (~1373 K) |
| σ_T | Source width | 50 K | T0 | Temperature window | not applicable | ✅ | ✅ | Toy value |
| A_C | Source amplitude | 1.0 /s | T0 | Generation rate | not applicable | ✅ | ✅ | Toy value |
| C_init | Initial concentration | 0.0 | T0 | Starting defect density | not applicable | ✅ | ✅ | Dimensionless proxy |
| C | Dimensionless heterogeneity proxy field | — (adim.) | TX | Heterogeneity proxy | — | ✅ | ✅ | **Must not** be interpreted as physical concentration |

## v0.2 Parameters (2D Thermal + Convergence)

| Symbol | Current Role | Current Value | Evidence Tier | Possible Physical Interpretation | Source Role | Allowed v0.3 | Allowed v0.4 | Caveat |
|--------|-------------|---------------|---------------|----------------------------------|-------------|-------------|-------------|--------|
| Lx, Ly | Domain dimensions | 0.01 m | T0 | Die dimensions | not applicable | ✅ | ✅ | Numerical convenience |
| nx, ny | Grid nodes 2D | 51 | T0 | Resolution | not applicable | ✅ | ✅ | Numerical convenience |
| t_boundary | 2D BC temp | 1400 K | T0 | Boundary temperature | not applicable | ✅ | ✅ | Toy value |
| nx_values | Convergence grids | [11,21,41,81] | T0 | Refinement sequence | not applicable | ✅ | ✅ | Numerical analysis |

## v0.3 Parameters (Defect-like Reaction-Diffusion)

| Symbol | Current Role | Current Value | Evidence Tier | Possible Physical Interpretation | Source Role | Allowed v0.3 | Allowed v0.4 | Caveat |
|--------|-------------|---------------|---------------|----------------------------------|-------------|-------------|-------------|--------|
| D₀_def | Defect diffusion pre-exp | 1.0e-4 m²/s | T1 | Vacancy D₀ in Si | parameter-source | ✅ | ✅ | Sinno/Bracht: D₀ ≈ 1e-5 to 1e-3 |
| E_D | Migration energy | 0.4 eV | T1 | Vacancy E_m in Si | parameter-source | ✅ | ✅ | Sinno: E_m ≈ 0.2–0.5 eV |
| A_G | Generation amplitude | 1.0 /s | T0 | Defect generation rate | not applicable | ✅ | ✅ | Toy; no source for magnitude |
| T_G | Generation center temp | 1100 K | T0 | Void nucleation temp | not applicable | ✅ | ✅ | Toy default; Voronkov nucleation ~1100°C (~1373 K); current value does NOT match literature |
| σ_G | Generation width | 100 K | T0 | Temperature window | not applicable | ✅ | ✅ | Toy; no source for width |
| A_R | Recombination amplitude | 10.0 /s | T0 | Recombination rate | not applicable | ✅ | ✅ | Toy; tuned for G/R balance |
| E_R | Recombination energy | 0.6 eV | T1 | Frenkel pair barrier | parameter-source | ✅ | ✅ | Sinno: 0.3–1.0 eV |
| C_sat | Saturation | 1.0 (adim.) | T0 | Maximum defect density | mathematical | ✅ | ✅ | Normalization bound |
| C_def | Dimensionless defect-like proxy field | — (adim.) | TX | Defect density proxy | — | ✅ | ✅ | **Must not** be interpreted as calibrated defect density |

## Future Parameters (v0.4 — NOT implemented)

| Symbol | Anticipated Role | Evidence Tier | Status | Caveat |
|--------|-----------------|---------------|--------|--------|
| ρ_eff | Effective charge density | T3 | ❌ NOT IMPLEMENTED | Requires Poisson + charge state model |
| ε_Si | Si permittivity | T2 | ❌ NOT IMPLEMENTED | Well-known: 11.7 ε₀ |
| q | Elementary charge | CONST | ❌ NOT IMPLEMENTED | Physical constant |
| φ | Electrostatic potential | T3 | ❌ NOT IMPLEMENTED | Requires Poisson solver |
| D_it | Interface trap density | T2 | ❌ NOT IMPLEMENTED | 1e10–1e12 cm⁻² eV⁻¹ (Sze) |

> [!CAUTION]
> No v0.4 parameter may be implemented without a formal ADR (ADR-007 or later)
> and policy.json update to `current_stage: v0.4`.
