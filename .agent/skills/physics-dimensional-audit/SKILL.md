---
name: physics-dimensional-audit
description: >
  Use this skill when auditing equations, units, scale modes, or physical
  claims in the MVP Quantum Materials project. It enforces dimensional
  consistency, prevents false calibration, and ensures physical interpretation
  guards are correctly maintained.
---

# Physics Dimensional Audit — Scientific Integrity Skill

## When to Use

Activate this skill whenever you are asked to:

- Add or modify equations, constants, or unit conversions.
- Review parameter evidence tiers (T0/T1/T2/T3/TX).
- Audit scale modes (demonstrative vs. literature-scaled vs. calibrated).
- Verify CSV metadata fields for physical correctness.
- Assess whether a change constitutes "new physics."

## Audit Steps

### 1. Separate Proxy from Physical Quantity

For every variable in the codebase, classify it:

| Classification | Example | Can claim physics? |
|---------------|---------|-------------------|
| **Proxy/adimensional** | `C_def` (defect concentration) | No |
| **Demonstrative** | `phi` with ε=1, N_ref=1 | No |
| **Literature-scaled** | `epsilon_r_Si = 11.7` | Scaffolding only |
| **Calibrated** | Device-specific fit | Only with evidence |

### 2. Explicit Dimension of Each Term

When reviewing an equation, write out the dimension of each term:

```
Example: ∇·(ε∇φ) = −ρ_eff

ε  → [F/m] = [C²·s²/(kg·m³)]  (only if physical)
φ  → [V] = [kg·m²/(A·s³)]     (only if physical)
ρ  → [C/m³]                    (only if physical)
```

If any term is proxy/demonstrative, the equation output is **not physical**.

### 3. Verify Dimensional Chain

For any unit conversion, verify the full chain:

```
D_it [eV⁻¹·cm⁻²] → D_it_SI [J⁻¹·m⁻²]
  Factor: 1/(eV_to_J) × 1/(cm_to_m)²
  = 1/(1.602e-19) × 1/(1e-2)²
  = 6.242e18 × 1e4
  = 6.242e22

σ_eff [C/m²] = q_e × D_it_SI × delta_E_window
  [C] × [J⁻¹·m⁻²] × [J] = [C/m²] ✓

ρ_eff [C/m³] = σ_eff / t_eff
  [C/m²] / [m] = [C/m³] ✓

ε_abs [F/m] = ε_r × ε₀
  [dimensionless] × [F/m] = [F/m] ✓
```

### 4. Identify Parameter Classification

For every parameter, check its evidence tier:

| Tier | Meaning | Source |
|------|---------|--------|
| CONST | Fundamental constant | CODATA/NIST |
| T0 | Exact by definition | Standards body |
| T1 | Well-established | Multiple references |
| T2 | Literature-supported | Specific references |
| T3 | Order-of-magnitude | Approximate literature |
| TX | Toy/demonstrative | No physical basis |
| NUM | Numerical parameter | Algorithm choice |

### 5. Prevent False Calibration

Never claim a parameter is calibrated unless:

- It has been fitted to experimental data.
- The fitting procedure is documented.
- The uncertainty is quantified.
- The material and conditions are specified.

### 6. Prevent Physical Interpretation of Demonstrative Outputs

Check these guards in the codebase and CSV:

- `physical_interpretation_allowed` must be `False` in demonstrative mode.
- `option_c_enabled` must be `False` until Option C ADR is accepted.
- `numerical_values_modified` must be `False` when no physics change occurred.
- `scale_mode` must accurately reflect the current operating mode.

### 7. Sanity Check When Physical Units Are Present

If a computation uses physical units (SI), verify:

- Order of magnitude is physically plausible.
- Sign convention is documented.
- Boundary conditions are dimensionally consistent.
- Source term has correct units.

### 8. Register Limits

Document explicitly what the model **cannot** predict:

- Device-level performance.
- Calibrated charge noise.
- Qubit coherence or fidelity.
- Wafer-quality metrics.

## Prohibited Claims

The following claims are **never** permitted without explicit ADR authorization
and calibration evidence:

- "Calibrated simulation."
- "Device-level prediction."
- "Physical phi interpretation" (while in demonstrative mode).
- "Coherence/fidelity prediction."
- "Charge-noise prediction" (as a real prediction, not demonstrative proxy).
- "Wafer-quality prediction."

## Dimensional Audit Checklist

- [ ] All variables classified (proxy/demonstrative/literature/calibrated).
- [ ] All equation terms have explicit dimensions.
- [ ] Unit conversion chains verified end-to-end.
- [ ] Parameter evidence tiers documented.
- [ ] No false calibration claims.
- [ ] `physical_interpretation_allowed` correctly set.
- [ ] `option_c_enabled` correctly set.
- [ ] `numerical_values_modified` correctly set.
- [ ] Limits and disclaimers documented.
