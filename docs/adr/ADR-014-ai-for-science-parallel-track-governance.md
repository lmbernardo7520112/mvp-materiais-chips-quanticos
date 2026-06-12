# ADR-014 — AI-for-Science Parallel Track Governance

## Status

Proposed

## Date

2026-06-12

## Context

The project currently follows a classical process-to-device numerical modeling roadmap. The chain C1 (surface charge bookkeeping), C2 (conservative source mapping), and future C3 (solver coupling) are based on governed numerical methods with explicit dimensional analysis, literature anchoring, and TDD discipline.

Recent discussions have raised the possibility of exploring AI-for-Science methods — Physics-Informed Neural Networks (PINNs), surrogate models, and operator learning — as complementary or alternative approaches to classical PDE solvers.

Such approaches may be promising in the broader scientific community, but they introduce significant new risks within this project's governance framework:

- **Overclaim:** Presenting ML approximations as validated physics without proper benchmarks.
- **Dependency creep:** Adding heavy ML frameworks (PyTorch, JAX, TensorFlow) without governance.
- **False validation:** Treating low training loss as physical correctness.
- **Premature solver replacement:** Substituting the classical solver before it is fully coupled and baselined.
- **Opacity:** Neural networks are less interpretable than explicit numerical schemes.
- **Training without data:** No experimental device data exists in this project for supervised learning.
- **Insufficient benchmarks:** No classical solver baseline yet exists for C3 coupling.
- **Demo-science confusion:** Treating a toy PINN demo as scientific validation.

## Core Decision Question

How can AI-for-Science methods be explored without contaminating the classical solver roadmap or weakening scientific governance?

## Decision

Propose a parallel, isolated, documentation-first AI-for-Science track.

## Tracks

### Classical Track

**Status:** Canonical.

**Includes:**

- Process/thermal simulation.
- Defect reaction-diffusion.
- D_it(E) energy profile library.
- C1 sigma_eff surface charge bookkeeping.
- C2 conservative source mapping.
- C3 conservative grid projection (future).
- Future classical solver coupling.
- Future quantum confinement prototype.

**Rules:**

- Remains the sole source of truth for physical modeling.
- Cannot be modified by AI-for-Science experiments.
- Cannot be replaced without a future dedicated ADR.
- Remains required as baseline for any future AI-for-Science benchmarks.

### AI-for-Science Track

**Status:** Exploratory, blocked from runtime.

**Possible future topics:**

- PINNs (Physics-Informed Neural Networks).
- Surrogate models (emulators of classical solver outputs).
- Operator learning (e.g., DeepONet, Fourier Neural Operator).
- Emulator of classical solver outputs for parameter sweeps.
- Inverse design prototypes.

**Current v0.7.6 status:**

- Documentation only.
- No code.
- No dependency.
- No training.
- No inference.
- No notebook.
- No dataset.

## Allowed Now

- Feasibility analysis.
- Risk taxonomy.
- Benchmark requirements definition.
- Dependency decision criteria.
- Evidence level taxonomy.
- Future RED test candidates.
- Separation strategy.
- Human decision log entry.

## Blocked Now

- PyTorch.
- TensorFlow.
- JAX.
- scikit-learn.
- Neural operator packages (neuraloperator, deepxde, etc.).
- PINN implementation.
- Surrogate implementation.
- Model training.
- Learned inference.
- Replacing classical solver.
- Claiming speedup.
- Claiming accuracy parity.
- Claiming physical validation from ML.
- Claiming device prediction from ML.

## Future AI-for-Science Evidence Levels

| Level | Name | Meaning | Allowed now? |
|-------|------|---------|--------------|
| AIFS-0 | Conceptual feasibility | Documentation only | Yes |
| AIFS-1 | Analytic benchmark design | Equations and toy benchmark specs only | Yes |
| AIFS-2 | Isolated toy prototype | Future code, no project physics coupling | Blocked now |
| AIFS-3 | Solver-emulator benchmark | Trained against classical solver outputs | Blocked now |
| AIFS-4 | Physics-informed surrogate | Benchmarked, uncertainty-aware | Blocked now |
| AIFS-5 | Experimental-data-informed model | Requires real data governance | Blocked |
| AIFS-6 | Device-predictive ML | Out of MVP scope | Blocked |

## Required Future Gates Before Any ML Code

- ADR accepted (not just proposed).
- Dependency decision brief approved.
- Benchmark definition with analytic solution.
- Classical solver baseline established.
- RED tests written and audited.
- Uncertainty/error metric defined.
- No physical overclaim allowed.
- Isolation from classical track enforced.
- Reproducibility plan (seeds, deterministic mode).
- Rollback plan documented.

## Decision Direction

- Keep classical track canonical.
- Open AI-for-Science track only as governed feasibility documentation.
- No implementation in v0.7.6.
- Future implementation must begin with an analytic benchmark (e.g., 1D Poisson with known solution), not project physics.
- No neural model may touch C1/C2/C3 without explicit ADR and benchmark evidence.

## Not Authorized

- No code.
- No tests.
- No scripts.
- No dependency.
- No solver replacement.
- No ML model.
- No training.
- No inference.
- No calibration.
- No device prediction.
