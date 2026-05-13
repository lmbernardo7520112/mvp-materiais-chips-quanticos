# ADR-009 — Option C Surface-Density Bookkeeping Scope

**Status:** Accepted
**Date:** 2026-05-13
**Supersedes:** None (extends ADR-008 Option B)
**Skills used:** physics-dimensional-audit, scope-guardrails, tdd-red-green-release

---

## Context

| Version | Milestone |
|---------|-----------|
| v0.4.0 | Poisson Bridge demonstrative (ε=1, proxy ρ_eff) |
| v0.4.4 | SI constants scaffolding (units.py, scale_modes.py) |
| v0.4.6 | Runtime metadata-only declaration in CSV |
| v0.4.8 | Readiness review: 0/6 for immediate code, 8/10 blocking gaps |
| v0.4.8 audit | Methodology mature (4.5/5); principal limitation is epistemic, not procedural |

The governance is mature. The model is still demonstrative. The next
priority must be **physics**, not more process.

## Decision

ADR-009 proposes **Option C1 — Surface-density bookkeeping only** as
the next minimal physics-forward step.

C1 computes and tests the chain from D_it to σ_eff **without coupling
charge density to the Poisson solver**.

## Option C Subroutes

| Route | Scope | Changes solver? | Needs t_eff? | Risk |
|-------|-------|-----------------|-------------|------|
| C0 | Keep metadata-only | No | No | Low — but no physics progress |
| **C1** | **Surface-density bookkeeping** | **No** | **No** | **Medium/Low** |
| C2 | Volume-smearing demonstrative source | Yes | Yes | High |
| C3 | Full physically interpreted charge map | Yes | Yes + validation | Critical |

**Selected: C1.**

## Candidate Dimensional Chain (C1)

### Step 1 — Interface Trap Density (input)

```
D_it [eV⁻¹·cm⁻²]    (literature input, tier T2/T3)
```

### Step 2 — SI Conversion

```
D_it_SI = D_it × 10⁴ / q_e
```

Where:
- `D_it` is expressed in eV⁻¹·cm⁻².
- `10⁴` converts cm⁻² → m⁻² (1 cm⁻² = 10⁴ m⁻²).
- `q_e = 1.602176634 × 10⁻¹⁹ J/eV` converts eV⁻¹ → J⁻¹.
- Therefore: `D_it_SI = D_it × 6.241509074 × 10²²` in units of [J⁻¹·m⁻²].

### Step 3 — Energy Integration Window

```
δE_window [J]    (must be explicit, never a silent default)
```

**Unresolved.** Candidate values:
- kT at 300 K ≈ 0.026 eV ≈ 4.14 × 10⁻²¹ J (conservative)
- Midgap ±2kT ≈ 0.10 eV (moderate)
- Full bandgap Si ≈ 1.12 eV (overestimate)

ADR-009 does not fix δE_window. Future implementation must require
it as an explicit parameter with no hidden default.

### Step 4 — Areal Trap Density

```
N_it = D_it_SI × δE_window

Unit: [m⁻²]
Constraint: N_it ≥ 0
```

### Step 5 — Surface Charge Density

```
σ_eff = s_charge × q_e × N_it × f_occ

Unit: [C/m²]
```

With:
- `s_charge ∈ {-1, +1}` — sign convention, **unresolved**:
  - Acceptor-like traps (above midgap): s_charge = -1 when filled.
  - Donor-like traps (below midgap): s_charge = +1 when empty.
  - ADR-009 requires the sign to be an explicit parameter.
- `f_occ ∈ [0, 1]` — occupancy fraction:
  - Demonstrative: f_occ = 1.0 (full occupation).
  - Physical: requires Fermi level (out of C1 scope).

## What C1 Does NOT Do

- ❌ Does NOT compute ρ_eff = σ_eff / t_eff.
- ❌ Does NOT modify the Poisson solver.
- ❌ Does NOT substitute ε = ε_r × ε₀.
- ❌ Does NOT produce physical φ.
- ❌ Does NOT set `physical_interpretation_allowed = True`.
- ❌ Does NOT set `option_c_enabled = True` in runtime CSV.

> **Note on `option_c_enabled`:** C1 is a subroute of Option C, but it
> does not couple physical charge to the Poisson solver. In the existing
> runtime CSV, `option_c_enabled` remains `False` because that flag
> governs solver-level coupling semantics. A future C1-specific artifact
> may expose `c1_bookkeeping_enabled = True`, but only outside the
> current solver runtime CSV.

## Why C1

1. **Advances physics** — exits purely demonstrative proxy for dimensional
   charge bookkeeping with real SI units.
2. **Avoids premature volume coupling** — no t_eff, no solver change.
3. **Testable** — unit conversion, sign convention, and bounds are
   verifiable with pure unit tests (no PDE solver needed).
4. **Reversible** — if dimensional chain proves wrong, σ_eff bookkeeping
   can be corrected without touching the solver.
5. **Prepares C2** — once σ_eff is validated, C2 can propose t_eff and
   solver coupling with a known-good upstream chain.

## Required Future RED Tests (to be created in implementation PR)

| # | Test | Verifies |
|---|------|----------|
| 1 | `test_dit_ev_cm2_to_j_m2_conversion` | D_it_SI factor = 6.242e22 × D_it |
| 2 | `test_delta_e_window_must_be_explicit_positive` | No silent default; must be > 0 |
| 3 | `test_nit_areal_density_units_and_values` | N_it = D_it_SI × δE_window; N_it ≥ 0 |
| 4 | `test_sigma_eff_requires_sign_convention` | s_charge must be explicit ±1 |
| 5 | `test_occupancy_bounds` | 0 ≤ f_occ ≤ 1 |
| 6 | `test_c1_does_not_create_rho_eff` | No ρ_eff computation in C1 module |
| 7 | `test_c1_does_not_modify_solver` | Solver hash unchanged |
| 8 | `test_metadata_blocks_physical_phi` | physical_interpretation_allowed = False |

## Required Benchmark Before C2

Before any future C2 proposal, at least one of:

- **Manufactured Poisson solution** with physical ε but artificial source
  (verify solver convergence and φ magnitude).
- **1D parallel-plate capacitor** sanity check (analytical solution
  φ = ρL²/(2ε) compared with solver output).

C2 is **blocked** until such a benchmark is specified and passes.

## Consequences

- C1 becomes the recommended next implementation route.
- C2/C3 remain blocked.
- `policy.json` remains unchanged until ADR-009 is Accepted.
- Implementation requires a separate PR with TDD RED→GREEN.
- ADR-009 must be Accepted via council review before any code.

## Acceptance Record

- [x] Council review completed.
- [x] Human approval obtained.
- [x] Status changed to Accepted.
- [ ] Implementation PR opened with RED tests.

## Acceptance Note — v0.4.10

ADR-009 is accepted only for C1 surface-density bookkeeping.

Acceptance authorizes a future RED phase for C1 unit tests.

Acceptance does NOT authorize:

- ρ_eff computation;
- t_eff usage;
- solver coupling;
- ε substitution;
- physical φ interpretation;
- C2/C3;
- runtime `option_c_enabled = True`.
