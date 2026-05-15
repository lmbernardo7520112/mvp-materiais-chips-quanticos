# ADR-010 — C1 Energy-Distribution Scope

**Status:** Accepted

**Date:** 2026-05-14

**Deciders:** Research Council v0.5.3, v0.5.4, v0.5.5

**Supersedes:** None

**Related:** ADR-009 (C1 Surface-Density Bookkeeping Scope)

---

## Context

- v0.5.0 implemented C1 surface-density bookkeeping: D_it → D_it_SI → N_it → σ_eff.
- v0.5.1 demonstrated C1 with controlled CSV, sensitivity figure, and metadata
  boundary checks (72 rows, monotonicity, sign symmetry).
- v0.5.2 positioned C1 scales against literature ranges for D_it, ΔE_window,
  and occupancy using 7 peer-reviewed references.
- The current C1 chain uses a **constant D_it** approximation within the
  energy window, which is the simplest possible assumption.
- The next physics-forward evolution is to model D_it as energy-dependent
  and integrate over the energy window.

## Current C1 Approximation

```
N_it = D_it_SI × ΔE_window
```

**Units:**

| Quantity | Unit |
|----------|------|
| D_it_SI | J⁻¹·m⁻² |
| ΔE_window | J |
| N_it | m⁻² |

**Interpretation:** This form assumes D_it(E) is constant within [E₁, E₂].

## Proposed Generalization

```
N_it = ∫_{E₁}^{E₂} D_it(E) dE
```

**Units:**

| Quantity | Unit |
|----------|------|
| D_it(E) | J⁻¹·m⁻² |
| dE | J |
| N_it | m⁻² |

**Dimensional verification:** [J⁻¹·m⁻²] × [J] = [m⁻²] ✓

The downstream σ_eff chain remains unchanged:

```
σ_eff = s_charge × q_e × N_it × f_occ
```

## Candidate Profiles

### P0 — Constant Profile

```
D_it(E) = D₀
N_it = D₀ × (E₂ - E₁)
```

- Equivalent to the current C1 implementation.
- Baseline for all comparisons.
- No additional parameters.

### P1 — Piecewise-Constant Profile

```
D_it(E) = D_i  for E ∈ [E_i, E_{i+1})
N_it = Σᵢ D_i × (E_{i+1} - E_i)
```

- Approximates arbitrary D_it(E) without imposing smoothness.
- Transparent: each bin has an explicit density value.
- Easy to test: sum of rectangles.
- Clear relationship to P0 (single bin = P0).
- Low overclaim risk: no functional form assumed.

### P2 — Gaussian Profile

```
D_it(E) = A × exp[-(E - E₀)² / (2σ_E²)]
N_it = ∫ A exp[-(E - E₀)² / (2σ_E²)] dE
```

- Models trap concentration near a characteristic energy.
- Three parameters: amplitude A, center E₀, width σ_E.
- **Risk:** may create false physical specificity if parameters are not
  justified by experimental data.
- Requires numerical integration (erf or quadrature).

### P3 — Triangular Profile

```
D_it(E) = piecewise linear with peak at E_peak and finite support
```

- Simple toy profile for integration testing.
- Two parameters: peak height, support width.
- Useful for sensitivity analysis.
- Low overclaim risk if labeled as demonstrative.

## Recommendation

1. **P0** must remain as baseline and regression reference.
2. **P1 piecewise-constant** is recommended as the next implementable step:
   - Minimal parametric assumption.
   - Transparent integration (sum of rectangles).
   - Easy to test and audit.
   - Clear backward compatibility with P0 (single bin).
   - Low risk of appearing calibrated.
3. **P2 and P3** remain as future/demonstrative candidates.
4. **No implementation in this release** (v0.5.3 is documentation-only).
5. Future implementation must follow RED-GREEN-REFACTOR with dedicated tests.

## What ADR-010 Does NOT Authorize

- ❌ ρ_eff computation.
- ❌ t_eff computation.
- ❌ Solver coupling (Poisson source term).
- ❌ ε substitution in solver.
- ❌ Physical φ interpretation.
- ❌ C2 or C3 features.
- ❌ Calibration claims.
- ❌ Device prediction.
- ❌ `option_c_enabled = True`.
- ❌ `physical_interpretation_allowed = True`.

## Consequences

- C1 gains a documented route toward energy-dependent trap density.
- The model remains surface-density bookkeeping only.
- The C1/C2 boundary is preserved: σ_eff stays as the terminal output.
- Future implementation, if authorized, must be test-first (TDD).
- P0 constant profile is preserved as the regression baseline.

---

## Acceptance Note — v0.5.5

> **Accepted:** 2026-05-15
> **Council:** v0.5.5 ADR-010 Acceptance Council (7/7 Accept)

ADR-010 is accepted only for future C1 energy-distribution modeling.

Acceptance authorizes a future RED phase for P1 piecewise D_it(E).

**Accepted default:**

- Option B: literature-informed P1 bins.

**Accepted conditional path:**

- Option C: E2 experimental-profile prior only with complete metadata.

**Blocked:**

- E3/E4 calibration-grade anchoring.
- ρ_eff.
- t_eff.
- Solver coupling.
- Physical φ interpretation.
- C2/C3.
- Calibration claims.
- Device prediction.

