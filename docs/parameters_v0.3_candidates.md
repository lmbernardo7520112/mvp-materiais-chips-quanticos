# Candidate Parameters — v0.3 Defect-like Reaction-Diffusion

> **Date:** 2026-05-07
> **Status:** DRAFT — candidates for council review
> **Warning:** ALL parameters are toy/demonstrative unless explicitly
> marked with a literature source.

---

## Parameter Classification

| Category | Description |
|----------|-------------|
| **Toy/Demonstrative** | Chosen for numerical behavior, not physical accuracy |
| **Literature-Inspired** | Order of magnitude from published data, not calibrated for C_def |
| **Undefined** | Not yet determined; requires further deliberation |
| **Prohibited** | Must NOT be presented as physically calibrated |

**Critical distinction:** Crystal growth references (Dornberger, Brown,
Voronkov) serve as **equation sources** (the form of the PDE) but NOT
as **parameter sources** (the numerical values). Literature-inspired
values use published orders of magnitude as starting points for toy
parameters, not as calibrated values for our C_def model.

---

## Diffusivity D(T)

| Parameter | Symbol | Unit | Candidate Value | Nature | Source | Risk |
|-----------|--------|------|-----------------|--------|--------|------|
| Pre-exponential | D₀ | m²/s | 1.0e-4 | Literature-inspired | Vacancy diffusion in Si: D₀ ≈ 1e-5 to 1e-3 m²/s (Sinno, Brown) | Must not claim calibration |
| Migration energy | E_D | eV | 0.4 | Literature-inspired | Vacancy migration in Si: E_m ≈ 0.2–0.5 eV (Sinno 2000, A5) | Order of magnitude only |
| Boltzmann constant | k_B | eV/K | 8.617e-5 | Physical constant | — | Exact |

**D(T) = D₀ · exp(−E_D / (k_B · T))**

At T = 1200 K: D ≈ 1e-4 · exp(−0.4/(8.617e-5·1200)) ≈ 1e-4 · exp(−3.87) ≈ 2.1e-6 m²/s
At T = 800 K: D ≈ 1e-4 · exp(−5.80) ≈ 3.0e-7 m²/s

---

## Generation G(T)

| Parameter | Symbol | Unit | Candidate Value | Nature | Source | Risk |
|-----------|--------|------|-----------------|--------|--------|------|
| Amplitude | A_G | 1/s | 1.0 | Toy/Demonstrative | No source; tuned for visible effect | High: must label toy |
| Center temperature | T_G | K | 1100.0 | Literature-inspired | Void nucleation ≈1100°C (Voronkov 1999) | Order of magnitude |
| Width | σ_G | K | 100.0 | Toy/Demonstrative | No source; tuned for smooth window | Must label toy |

**G(T) = A_G · exp(−(T − T_G)² / (2·σ_G²))**

At T = 1100 K: G = 1.0 (peak)
At T = 900 K: G ≈ exp(−2.0) ≈ 0.14
At T = 1400 K: G ≈ exp(−4.5) ≈ 0.011

---

## Recombination R(T)

| Parameter | Symbol | Unit | Candidate Value | Nature | Source | Risk |
|-----------|--------|------|-----------------|--------|--------|------|
| Pre-exponential | A_R | 1/s | 10.0 | Toy/Demonstrative | Tuned for balance with G | Must label toy |
| Activation energy | E_R | eV | 0.6 | Literature-inspired | Recombination barrier ≈ 0.3–1.0 eV (Sinno) | Order of magnitude |

**R(T) = A_R · exp(−E_R / (k_B · T))**

Applied as R(T)·C_def (first-order kinetics).

At T = 1200 K: R ≈ 10 · exp(−5.80) ≈ 0.030 /s
At T = 800 K: R ≈ 10 · exp(−8.70) ≈ 0.0017 /s

---

## Saturation

| Parameter | Symbol | Unit | Candidate Value | Nature | Source | Risk |
|-----------|--------|------|-----------------|--------|--------|------|
| Saturation | C_sat | — | 1.0 | Mathematical | Normalization choice | None |

---

## Domain and Solver

| Parameter | Symbol | Unit | Candidate Value | Nature | Source | Risk |
|-----------|--------|------|-----------------|--------|--------|------|
| Domain size | Lx, Ly | m | 0.01 | Toy | Same as v0.2 thermal | — |
| Grid points | nx, ny | — | 51 | Toy | Same as v0.2 thermal | — |
| Safety factor | — | — | 0.4 | Numerical | Same as v0.2 thermal | — |

---

## Thermal Field (Input)

| Parameter | Source | Note |
|-----------|--------|------|
| α (thermal diffusivity) | 8.8e-5 m²/s | From v0.2, order of Si |
| T_init | 1500 K | Demonstrative |
| T_boundary | 300 K (or 1400 K) | Demonstrative |
| t_total | 0.1 s or longer | Adjusted for freeze-in |

---

## Prohibited Claims

The following MUST NOT be stated:

- "These parameters reproduce silicon vacancy dynamics"
- "C_def is calibrated against experimental data"
- "The model predicts real defect concentrations"
- "Parameters are from Maurand et al."
- "Results can be compared to TCAD simulations"
- "Literature-inspired values are calibrated for this model"
- "The parameters are taken from Dornberger/Brown/Voronkov"
  (correct: "the equation *form* is inspired by..., values are toy")
