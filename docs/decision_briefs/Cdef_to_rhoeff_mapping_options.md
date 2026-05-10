# Decision Brief — C_def → ρ_eff Mapping Options

> **Date:** 2026-05-09
> **Status:** ANALYSIS COMPLETE — NO IMPLEMENTATION
> **Decision:** None selected for v0.3.5. Preferred candidate identified for
> future ADR-007 deliberation.

## Context

The defect field C_def is currently a **dimensionless proxy** (tier TX) that
represents spatial heterogeneity in a 2D reaction-diffusion model. To bridge
toward device-relevant predictions (charge disorder, threshold voltage
variation, noise), a mapping from C_def to an effective charge density ρ_eff
is needed. This mapping would feed a Poisson solver: ∇·(ε∇φ) = −ρ_eff
(or ∇²φ = −ρ_eff/ε in the homogeneous-permittivity simplification).

This brief compares three candidate approaches.

> [!IMPORTANT]
> **None of these options are implemented in v0.3.5.** This is a specification
> document only. Implementation requires ADR-007 approval and v0.4 policy.

---

## Option A: Linear Proportional Mapping

### Mathematical Sketch

```
ρ_eff(x,y) = q · n_ref · C_def(x,y)
```

Where:
- q = elementary charge (1.602e-19 C)
- n_ref = reference defect density scale [cm⁻³] (to be calibrated)
- C_def ∈ [0, 1] dimensionless

### Maturity

**Low.** Simplest possible mapping. No physical basis beyond dimensional
analysis.

### Assumptions

1. All defects contribute equally to charge.
2. Single charge state (no amphoteric behavior).
3. No Fermi level dependence.
4. No temperature dependence of occupancy.

### Risks

- Overclaims physical validity.
- Ignores charge state complexity.
- n_ref is entirely arbitrary without calibration.

### Required Literature

- Defect charge state data (Sze, Pichler).
- Interface trap density ranges (Fleetwood).

### Recommended Status

⚠️ **Acceptable as v0.4 starting point** — with explicit disclaimer that
n_ref is uncalibrated and the mapping is a placeholder.

---

## Option B: Heterogeneity-Weighted Mapping

### Mathematical Sketch

```
ρ_eff(x,y) = q · n_ref · f(∇C_def, ∂C_def/∂t)
```

Where f is a functional of spatial gradients and temporal evolution,
capturing the idea that charge disorder arises from **non-uniform** defect
distributions, not from the absolute density alone.

Possible form:
```
f = |∇C_def|² / max(|∇C_def|²)    (normalized gradient squared)
```

### Maturity

**Very low.** Conceptually motivated but no direct literature support for
this specific functional form.

### Assumptions

1. Charge disorder scales with spatial heterogeneity, not bulk density.
2. Gradient magnitude is a proxy for interface quality.
3. Normalization avoids magnitude issues.

### Risks

- No experimental validation pathway.
- Gradient computation adds numerical noise.
- Physical interpretation unclear.

### Required Literature

- Spatial correlation of charge noise (Connors 2022, Struck 2020).
- No direct equation source exists.

### Recommended Status

❌ **Not recommended for v0.4.** Interesting for v0.5+ if spatial correlation
data becomes available.

---

## Option C: Trap/Interface Occupancy Proxy

### Mathematical Sketch

```
ρ_eff(x,y) = q · D_it · ∫ [f_T(E, T) · g(E)] dE · h(C_def)
```

Where:
- D_it = interface trap density [cm⁻² eV⁻¹]
- f_T = Fermi-Dirac occupancy at temperature T
- g(E) = trap energy distribution (uniform or Gaussian)
- h(C_def) = monotonic function mapping C_def to trap density modifier

Simplified v0.4 candidate:
```
ρ_eff(x,y) ≈ q · D_it_ref · C_def(x,y)
```

(reduces to Option A with n_ref = D_it_ref when integrated over energy)

### Maturity

**Low-Medium.** Grounded in interface trap physics (Fleetwood, Sze) but
requires significant simplification for the MVP.

### Assumptions

1. Trap density correlates with defect proxy C_def.
2. Single effective energy level or uniform distribution.
3. Equilibrium occupancy (no transient charging).
4. D_it_ref provides physical scale.

### Risks

- D_it_ref requires calibration or literature bounding.
- Fermi level self-consistency requires iterative Poisson solver.
- Simplification may not capture essential physics.

### Required Literature

- D_it values (Sze: 1e10–1e12 cm⁻² eV⁻¹).
- Trap energy distributions (Fleetwood 2018).
- Fermi level pinning effects.

### Recommended Status

🟡 **Preferred candidate for ADR-007** — physically grounded, reduces to
Option A as special case, extensible with better trap models.

---

## Comparison Summary

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Simplicity | ✅ High | ⚠️ Medium | ⚠️ Medium |
| Physical grounding | ❌ Minimal | ❌ Weak | 🟡 Moderate |
| Literature support | ⚠️ Indirect | ❌ None | 🟡 Interface trap physics |
| Calibration path | ⚠️ n_ref only | ❌ No pathway | 🟡 D_it from literature |
| Risk of overclaim | ⚠️ Medium | ✅ Low | ⚠️ Medium |
| Extensibility | ❌ Limited | ⚠️ Research-grade | ✅ Good |
| **v0.4 readiness** | ✅ Yes | ❌ No | 🟡 Yes (simplified form) |

## Recommendation

1. **v0.3.5:** No implementation. Document options only.
2. **ADR-007:** Propose Option C (simplified form ≈ Option A with D_it_ref
   as scale factor) as starting candidate.
3. **v0.4:** Implement simplified ρ_eff with explicit tier T3 caveat.
4. **v0.5+:** Extend to full trap occupancy model if justified.

> [!WARNING]
> Any ρ_eff implementation **must** be accompanied by:
> - A Poisson solver (or Poisson-like coupling).
> - Explicit disclaimer that D_it_ref is uncalibrated.
> - Quality gate enforcement (scope guardrails).
> - ADR approval.
