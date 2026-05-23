# ADR-012 — C2 Interface Sheet Source vs Conservative Volume Regularization

## Status

Proposed

## Date

2026-05-23

## Context

### Where we are

v0.6.2 closed the C1 bookkeeping chain:

    D_it(E) → N_it → σ_eff   [C/m²]

with curated E1/E2 profile library and unit-conversion infrastructure.

### What comes next

The next process-to-device layer (per ADR-011, v0.7.0) must decide how
σ_eff [C/m²] enters the future electrostatic problem.

### The wrong question

> "What t_eff should we use?"

This question presupposes a volume mapping σ → ρ = σ/t that may not be
physically required and invites false calibration.

### The correct question

> "Should σ_eff remain an interface/sheet source, or be mapped to a
> conservative regularized volume source?"

### Why this matters

- σ_eff is inherently a surface/interface charge density [C/m²].
- Dividing by an arbitrary thickness to obtain ρ_eff [C/m³] is only
  legitimate if the thickness has a defined physical or numerical meaning.
- The formulation choice determines how future electrostatic coupling
  treats interface charge.
- The wrong choice embeds a false physical parameter into the solver chain.

## Current C1 Chain

```
D_it(E) [J⁻¹·m⁻²]
    ↓ integrate over energy
N_it [m⁻²]
    ↓ × q_e × sign × f_occ
σ_eff [C/m²]
```

σ_eff is the terminal quantity of C1. C2 decides what happens next.

## Future C2 Question

```
σ_eff [C/m²] → ? → source term for future electrostatic PDE
```

## Options

### C2-A — Interface Sheet Source / Jump Condition (PRIMARY)

**Formulation:**

    n̂ · (ε₂∇φ₂ − ε₁∇φ₁) = −σ_eff

where n̂ is the interface normal, ε₁/ε₂ are the permittivities on
each side, and φ₁/φ₂ are the potentials.

**Dimensional check:**

    [F/m] · [V/m] = [C/m²]  ✓

**Characteristics:**

- Treats σ_eff as what it is: interface charge.
- No invented thickness parameter.
- Highest physical fidelity for interface traps.
- Standard in semiconductor device physics (Sze & Ng, 2006).
- Compatible with both 1D and 2D future solver geometry.
- Does not require volume mesh at the interface.

**Limitations:**

- Requires solver support for jump/interface boundary conditions.
- Some numerical frameworks prefer volumetric source terms.

### C2-B — Conservative Volume Regularization (FALLBACK)

**Formulation:**

    ρ_reg = σ_eff / l_reg

distributed within a regularization layer of thickness l_reg.

**Conservation requirement (mandatory):**

    ∫_V ρ_reg dV = ∫_A σ_eff dA

Equivalently, for a 1D slice:

    ρ_reg × l_reg = σ_eff

**Dimensional check:**

    [C/m²] / [m] = [C/m³]  ✓

**Critical distinctions:**

- l_reg is a **numerical regularization length**, not a physical t_eff.
- l_reg controls numerical smearing, not physical trap depth.
- l_reg must be reported as metadata, not hidden.
- Results must be tested for sensitivity to l_reg.
- If the physical result depends pathologically on l_reg, the
  regularization is too aggressive.

**When to use:**

- Only if the future solver requires a volumetric source term
  and cannot support jump/interface conditions.
- As a conservative numerical fallback, not a physical model.

### C2-C — Literature/Experimental Depth Prior (CONDITIONAL)

**Use permitted for:**

- Informing envelopes of sensitivity for l_reg values.
- Representing hypotheses about near-interface/border/oxide trap
  spatial distributions.
- Documenting depth priors from literature without calibrating the MVP.

**Use NOT permitted for:**

- Replacing the primary C2-A sheet-source formulation.
- Claiming calibration.
- Treating literature depth as device-specific.
- Confusing interface-state D_it with border/oxide trap distributions.

**Required metadata for any depth prior:**

| Key | Purpose |
|-----|---------|
| source | Literature citation |
| source_role | e.g., depth_prior_candidate |
| trap_family | interface / border / oxide |
| material_stack | e.g., Si/SiO₂ |
| interface_or_region | e.g., Si(100)/thermal SiO₂ |
| technique | e.g., charge pumping, DLTS, C-V |
| depth_or_distribution_parameter | e.g., "1–3 nm from interface" |
| length_units | e.g., nm |
| extraction_assumptions | How depth was inferred |
| uncertainty_note | Uncertainty or spread |
| transferability_note | Conditions under which result may transfer |
| calibration_status | must be "not_calibrated" |

### C2-D — Generic Physical t_eff (REJECTED)

**Status:** Rejected for current MVP.

**Reasons:**

- Confuses numerical regularization with physical thickness.
- No universal t_eff exists for Si/SiO₂ interface traps.
- Creates false impression of physical calibration.
- High risk of embedding an arbitrary parameter as "physics."
- Literature t_eff values vary by orders of magnitude depending on
  trap family, measurement technique, and process conditions.

### C2-E — Calibrated Device-Fitted t_eff (BLOCKED)

**Status:** Blocked.

**Reasons:**

- Requires own-device experimental data or exact same-stack data.
- The MVP has no experimental validation pipeline.
- This would convert the demonstrative tool into a calibrated
  device simulator, which is beyond current scope.
- Requires its own future ADR beyond v0.7.x.

## Important Physical Distinctions

### Interface traps vs border/oxide traps

| Trap family | Location | Characteristic |
|-------------|----------|---------------|
| Interface states (D_it) | At the Si/SiO₂ interface | ~monolayer, energy-dependent |
| Border traps | Within ~1–3 nm of interface in SiO₂ | Tunnel-accessible, time-dependent |
| Oxide traps | Deeper in SiO₂ bulk | Fixed or slowly switching |

**Rule:** Interface-state D_it profiles (C1) map naturally to sheet
charge σ_eff. Border/oxide traps have spatial extent and may require
different treatment. The C2 ADR covers interface traps primarily.
Border/oxide trap depth priors are C2-C candidates only.

## Recommendation

| Option | Role | Status |
|--------|------|--------|
| C2-A | Primary | Recommended |
| C2-B | Fallback | Allowed (conservative, l_reg only) |
| C2-C | Conditional | Allowed (sensitivity/documentation only) |
| C2-D | Rejected | Not accepted for MVP |
| C2-E | Blocked | Requires future ADR |

## Decision

**ADR-012 is Proposed only.**

This ADR does not authorize implementation.

Implementation requires:

1. ADR-012 acceptance review (v0.7.1, documentation-only).
2. Future TDD RED phase specifying C2 tests (v0.7.2, earliest).
3. Future GREEN phase implementing the chosen path (v0.7.3, earliest).

## Still Blocked

- ρ_eff API implementation.
- t_eff physical parameter.
- l_reg implementation.
- σ_eff → ρ_eff mapping code.
- Solver coupling.
- Electrostatic PDE runtime coupling.
- Quantum confinement solver.
- C2 code of any kind.
- Calibration claims.
- Coherence/fidelity claims.

## References

- Sze & Ng (2006), *Physics of Semiconductor Devices*, 3rd ed.
- ADR-010: C1 energy distribution scope.
- ADR-011: Process-to-device qubit demonstrator roadmap.
- v0.6.2: Curated E1/E2 D_it(E) profile library.
- v0.5.2: C1 literature scale benchmark.
- v0.5.4: Energy profile evidence taxonomy.
