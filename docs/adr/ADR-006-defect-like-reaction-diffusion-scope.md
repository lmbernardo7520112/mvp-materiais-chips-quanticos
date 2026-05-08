# ADR-006 — Defect-like Reaction-Diffusion Scope for v0.3

## Status

**Accepted**

## Date

2026-05-07

## Context

The v0.2.1 release closed the institutional and reproducibility package
for the project. The roadmap (ADR-005) establishes v0.3 as the
"defect-like reaction-diffusion" wave, bridging thermal process modeling
to heterogeneity representation.

**Key context elements:**
- v0.2.1 is closed: 2D thermal robustness + institutional package
- Maurand et al. (2016) is the device-target anchor for silicon CMOS
  spin qubits, motivating why process-generated disorder matters
- Literature on point defects in CZ silicon (Dornberger, Brown, Voronkov)
  provides structural inspiration for the reaction-diffusion equation form
  (equation source; parameter values remain toy/demonstrative for v0.3)
- Literature on charge noise (Martinez & Niquet, Culcer, Shehata)
  validates the downstream impact of disorder on qubits
- The project needs to approximate semiconductor materials and defects
  while maintaining scientific prudence
- C_def must prepare the interface for ρ_eff in Poisson v0.4

**Literature basis:** See `docs/literature_review/v0.3_state_of_art_defect_like_reaction_diffusion.md`
**Council deliberation:** See `docs/research_council/v0.3_defect_like_council.md`

## Decision

### What C_def Represents

C_def(x,y,t) is a **scalar, adimensional, defect-like state variable**
representing normalized density of thermally-generated heterogeneities.
It is a proxy — not a calibrated physical concentration.

C_def can be **interpreted** (not equated) as analogous to:
- Normalized vacancy concentration (crystal growth analogy)
- Trap-like charge disorder density (interface analogy)
- Generic material heterogeneity measure

### What C_def Does NOT Represent

- Real vacancy concentration in silicon
- Real interstitial concentration
- Real interface trap density (Pb centers)
- Calibrated charge noise source
- Any quantity validated against experiment

### Governing Equation

```
∂C_def/∂t = ∇·(D(T)∇C_def) + G(T)·(1 − C_def/C_sat) − R(T)·C_def
```

### Diffusivity

```
D(T) = D₀ · exp(−E_D / (k_B · T))
```

Arrhenius form, consistent with existing diffusion_solver.py.

### Generation

```
G(T) = A_G · exp(−(T − T_G)² / (2·σ_G²))
```

Gaussian thermal window: defects generated preferentially in a
critical temperature range during cooling.

### Recombination

```
R(T) = A_R · exp(−E_R / (k_B · T))
```

First-order relaxation: R(T)·C_def. Thermally activated recombination.

### Saturation

C_sat = 1.0 (adimensional). The logistic term (1 − C_def/C_sat)
bounds C_def from above. With non-negative initial conditions and
non-negative R, C_def stays in [0, 1].

### Boundary Conditions

Neumann no-flux: ∂C_def/∂n = 0 on all boundaries.
Defects are generated internally by the thermal field; no external
source/sink at boundaries.

### Initial Condition

C_def(x,y,0) = 0 (pristine material) or small uniform seed.

### Coupling

One-way: T(x,y,t) → C_def(x,y,t).
The thermal field drives C_def via D(T), G(T), R(T).
No back-coupling of C_def on T.

### Candidate Metrics

- max(C_def) — peak defect-like density
- mean(C_def) — average heterogeneity
- ∫C_def dA — total defect-like content
- σ(C_def) — spatial non-uniformity
- freeze-in profile — C_def distribution when T drops below G threshold

### Future Interface with v0.4 Poisson

```
ρ_eff(x,y) = q_eff · C_def(x,y,t_final)
∇·(ε∇φ(x,y)) = −ρ_eff(x,y)
```

(Note: ∇²φ = −ρ_eff/ε is valid only for spatially homogeneous ε.)

C_def_final serves as input for v0.4 Poisson source term.

## Alternatives Considered

### A — Full V/I Coupled System

Two coupled PDEs (vacancies + interstitials). Closest to Dornberger/Brown
literature but requires 10+ parameters per species. Equations are
schematic representations; actual models vary by author and may include
convection, thermodiffusion, oxygen, and cluster terms. **Rejected:**
too complex, insufficient parameter availability, overclaim risk.

### B — Effective Interface-Trap Model

Models gate-voltage-dependent trap dynamics. **Rejected:** requires
device-level abstraction (gate voltage) not available until v0.4+.

### C — Generic Defect-like Scalar ✅ (Selected)

Single reaction-diffusion equation with effective C_def. Captures
qualitative behavior (generation, diffusion, recombination, freeze-in)
at minimum complexity.

### D — Defer v0.3

No new physics. **Rejected:** project has sufficient foundation to
advance; deferral risks losing momentum.

## Consequences

### Positive

- Approximates project to semiconductor materials
- Prepares clean interface for v0.4 Poisson
- Maintains simplicity and testability
- Maintains rastreability with CMOS spin-qubit target
- Reaction-diffusion form structurally inspired by crystal growth
  literature (Dornberger, Brown) — used as equation source, not as
  calibrated parameter source
- Bounded C_def (bounded model → numerical stability)
- Educational and demonstrative value

### Negative

- Not calibrated to any specific defect type
- Cannot distinguish vacancies from interstitials
- Results are qualitative only
- Requires careful documentation to prevent overclaim
- Maurand et al. does not provide equation or parameters for C_def

## Guardrails

1. C_def is **adimensional** — no physical units
2. No parameter presented as calibrated without published source
3. No prediction of experimental observables
4. No quantum coherence prediction
5. No Poisson solver in v0.3
6. No Schrödinger solver in v0.3
7. All figures must carry disclaimer: "demonstrative — not calibrated"
8. All metrics must state whether they are proxies
9. All implementations must preserve v0.2.1 regression
10. Maurand et al. cited ONLY as device-target anchor, NEVER as
    calibration source for C_def, G(T), or R(T,C)
11. thermal_solver.py and diffusion_solver.py must remain untouched
12. Additive-only policy: new modules, not modifications

## Acceptance Record

Accepted on 2026-05-08 after the v0.3 literature review, Research
Council deliberation (8/8 approve), ADR-006 proposal, and v0.3 draft
specification were merged into main via PR #6.

The accepted v0.3 direction is a bounded, adimensional, defect-like /
trap-like / charge-disorder-like state variable C_def governed by a
thermally motivated reaction-diffusion formulation:

```
∂C_def/∂t = ∇·(D(T)∇C_def) + G(T)(1 − C_def/C_sat) − R(T)C_def
```

This acceptance authorizes a future implementation branch for the v0.3
core, but does not implement it.

The accepted guardrails remain:

- C_def is adimensional.
- C_def is not a calibrated physical defect concentration.
- G(T), R(T,C_def), and D(T) parameters remain toy/demonstrative
  unless future curation explicitly upgrades them.
- v0.3 must not solve Poisson.
- v0.3 must not solve Schrödinger.
- v0.3 must not claim device-level prediction.
- v0.3 must not predict charge noise, coherence, fidelity, or
  wafer quality.
- v0.3 must preserve v0.2.1 regression.

## References

- Maurand et al. (2016). DOI: 10.1038/ncomms13575
- Dornberger et al. (2001). DOI: 10.1016/S0022-0248(01)01319-7
- Brown et al. (1994). DOI: 10.1016/0022-0248(94)91240-8
- Voronkov & Falster (1999). DOI: 10.1016/S0022-0248(99)00216-7
- Martinez & Niquet (2022). DOI: 10.1103/PhysRevApplied.17.024022
- Culcer et al. (2009). DOI: 10.1063/1.3194778
- Shehata et al. (2023). DOI: 10.1103/PhysRevB.108.045305
- Massai et al. (2024). DOI: 10.1038/s43246-024-00563-8
- Peña et al. (2024). DOI: 10.1038/s41534-024-00827-8
