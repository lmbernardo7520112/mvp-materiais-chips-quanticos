# ADR-011 — Process-to-Device Silicon/CMOS Qubit Demonstrator Roadmap

## Status

**Proposed**

## Date

2026-05-19

## Context

The project has completed the following layers:

- **v0.1–v0.2:** Thermal diffusion solver (1D/2D).
- **v0.3:** Defect-like reaction-diffusion (C_def).
- **v0.4:** Poisson bridge (demonstrative ρ_eff → φ solver, not coupled to C1).
- **v0.5:** C1 surface-charge bookkeeping (σ_eff = s × q_e × N_it × f_occ).
- **v0.6.0:** Piecewise D_it(E) energy integration (N_it = Σ D_i × ΔE_i).

The original roadmap (ADR-005) envisioned:

- v0.5 as Schrödinger confinement.
- v1.0 as the integrated process-to-device demonstrator.

In practice, v0.5 was dedicated to C1 bookkeeping and evidence taxonomy
hardening, which was essential but shifted the timeline. The project
now needs to explicitly re-anchor its trajectory toward the device layer.

### Device-Target Anchor

**Maurand et al. (2016).** *"A CMOS silicon spin qubit."*
Nature Communications 7, 13575. DOI: 10.1038/ncomms13575.

This paper demonstrates a spin qubit fabricated using standard CMOS
technology on silicon, establishing that process-generated interface
defects directly affect qubit quality. It serves as the **device-target
anchor** — the motivating example for why modeling the chain from
process defects to electrostatic environment matters.

**Maurand et al. is NOT:**
- A calibration source for this project.
- A parameter source for D_it, σ_eff, or any model quantity.
- Evidence of experimental validation.

## Mission Statement

> Build a process-to-device demonstrator for silicon/CMOS qubits,
> inspired by Maurand et al. 2016, to study how interface-defect and
> surface-charge profiles modify electrostatic potential and effective
> quantum confinement, without claiming experimental calibration or
> coherence prediction.

## Current Chain (v0.6.0)

```
Process/thermal → C_def(x,y) → D_it(E) → N_it → σ_eff
```

All quantities are C1 bookkeeping — not calibrated, not device-predictive.

## Target Chain (v1.0)

```
Process/thermal
  → C_def(x,y)
    → D_it(E)
      → N_it
        → σ_eff
          → ρ_eff = σ_eff / t_eff     [C2]
            → ∇·(ε∇φ) = −ρ_eff        [Poisson coupling]
              → V_conf(x,y)
                → Ĥψ = Eψ             [Schrödinger prototype]
```

## Scope Boundaries

The following are **permanently out of scope** for the MVP:

| Item | Status | Reason |
|------|--------|--------|
| T₁/T₂ prediction | BLOCKED | Requires spin-orbit, hyperfine, noise models |
| Coherence prediction | BLOCKED | Beyond demonstrator scope |
| Gate fidelity prediction | BLOCKED | Requires control Hamiltonian |
| Calibrated device simulation | BLOCKED | No experimental data |
| Industrial TCAD replacement | BLOCKED | Different scope/scale |
| QTCAD replacement | BLOCKED | Different abstraction level |
| Real-device validation claims | BLOCKED | No fab access |

The following require **dedicated ADRs** before implementation:

| Item | ADR Required | Earliest Release |
|------|-------------|-----------------|
| C2 ρ_eff/t_eff mapping | ADR-C2 | v0.7.0 |
| Poisson solver coupling | ADR-Poisson-coupling | v0.8.0 |
| Schrödinger confinement prototype | ADR-Schrödinger | v0.9.0 |
| Process-to-device integration | ADR-integration | v1.0 |
| Any experimental calibration claim | ADR-calibration | Never in MVP |

## Proposed Roadmap

| Release | Type | Scope |
|---------|------|-------|
| v0.6.1 | docs | Process-to-device roadmap re-anchoring |
| v0.6.2 | docs+code | Curated E1/E2 D_it(E) profile library |
| v0.7.0 | docs | ADR-C2: surface-to-volume charge mapping |
| v0.7.1 | code | C2 RED/GREEN if ADR accepted |
| v0.8.0 | code | Poisson coupling demonstrator |
| v0.9.0 | code | Schrödinger effective confinement prototype |
| v1.0 | integration | Integrated process-to-device demonstrator |

## Decision

ADR-011 proposes only the roadmap and mission alignment.
**It does not authorize any implementation.**

Each layer requires its own ADR, TDD cycle, and governance review
before code can be written.

## References

1. Maurand et al. (2016). DOI: 10.1038/ncomms13575
2. ADR-005: Process-to-Device Bridge Roadmap (original)
3. ADR-006: Defect-like Reaction-Diffusion Scope
4. ADR-007: Poisson Bridge Scope
5. ADR-009: Option C Surface-Density Bookkeeping Scope
6. ADR-010: C1 Energy-Distribution Scope (Accepted + v0.5.6 amendment)
