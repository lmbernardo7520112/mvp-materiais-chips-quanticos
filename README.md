# MVP — Quantum Semiconductor Materials Modeling

> **Simplified thermo-diffusive and defect reaction-diffusion modeling for
> heterogeneity analysis in idealized semiconductor material**

[![CI](https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos/actions/workflows/ci.yml)
[![Python 3.11 | 3.12](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org/)
[![Latest Release](https://img.shields.io/github/v/tag/lmbernardo7520112/mvp-materiais-chips-quanticos?label=release)](https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos/tags)
[![Coverage](https://img.shields.io/badge/coverage-91.78%25-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Scientific Motivation

This project explores the **methodological bridge** between numerical
simulation of heat and mass transport phenomena and the study of
heterogeneities in semiconductor materials relevant to solid-state quantum
devices. The approach is strictly **demonstrative and pedagogical**.

## What This Project Is

- A computational MVP for 1D/2D thermal, diffusive, defect
  reaction-diffusion, and demonstrative electrostatic modeling.
- A demonstrative framework with toy/pedagogical parameters.
- A governance-hardened repository using AI-RSE GateOps.
- An academic exercise in reproducible computational science.

## What This Project Is NOT

> [!CAUTION]
> This project does **not**:
> - Simulate real wafer fabrication or industrial processes.
> - Predict quantum coherence, qubit fidelity, or charge noise.
> - Use calibrated experimental parameters.
> - Replace TCAD, Sentaurus, Silvaco, or any commercial tool.
> - Solve nonlinear or self-consistent Poisson equations.
> - Compute calibrated carrier densities or device-level ρ_eff.
> - Claim equivalence between metallic solidification and semiconductor
>   fabrication.

## Current Release

| Item | Status |
|------|--------|
| **Version** | v0.4.0 (pending merge) |
| **Tests** | 127+ passing |
| **Coverage** | ≥91% (gate ≥ 70%) |
| **CI** | GitHub Actions — Python 3.11 + 3.12 |
| **Quality Gates** | 6 AI-RSE gates active |
| **Branch Protection** | Required checks enforced on `main` |

### Nature of C and C_def

> [!IMPORTANT]
> The variable **C** (diffusion) and **C_def** (defect reaction-diffusion) are
> **dimensionless proxies** of heterogeneity/defect density. They do **not**
> represent physically calibrated concentrations and must **not** be compared
> quantitatively with real defect densities in semiconductors.

### Parameters

All physical parameters (D₀, E_a, σ_T, etc.) are **toy/demonstrative** values
chosen to produce numerically stable and visually interpretable results. They
are **not** calibrated to any real semiconductor system.

## Quickstart

```bash
# Clone
git clone https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos.git
cd mvp-materiais-chips-quanticos

# Virtual environment
python -m venv .venv
source .venv/bin/activate

# Install
pip install -e ".[dev]"
```

## Reproduce Results

```bash
# Generate all figures and CSV tables
python scripts/generate_all_results.py --output-dir results/figures

# Run tests
pytest -v --tb=short

# Run with coverage
pytest --cov=mvp_quantum_materials --cov-report=term-missing --cov-fail-under=70

# Lint
ruff check .
ruff format --check .

# Type checking
pyright .
```

### Output Artifacts

| Artifact | Description |
|----------|-------------|
| 9 figures | Thermal 1D/2D, diffusion 1D, defect 2D, sensitivity, convergence |
| 4 CSVs | Sensitivity results, convergence, defect metrics, defect snapshot |

## Architecture

```
src/mvp_quantum_materials/
├── config.py              # Physical constants, stability checks
├── domain.py              # 1D and 2D computational domains
├── thermal_solver.py      # 1D thermal solver (Dirichlet BCs)
├── thermal_solver_2d.py   # 2D thermal solver (Dirichlet BCs)
├── diffusion_solver.py    # 1D diffusion with Arrhenius + source (Neumann BCs)
├── defect_kinetics.py     # D(T), G(T), R(T) — toy kinetics
├── defect_stability.py    # CFL-like stability guard for defect solver
├── defect_solver_2d.py    # 2D reaction-diffusion solver
├── defect_metrics.py      # Proxy metrics for C_def fields
├── convergence.py         # Grid convergence analysis
├── sensitivity.py         # Parametric sensitivity analysis
├── metrics.py             # Heterogeneity metrics
└── plots.py               # Figure generation
```

## AI-RSE GateOps

This project uses **AI-RSE GateOps** — a version-aware quality gate framework
that enforces scientific scope, documentation, and CI discipline at every PR:

| Gate | Purpose |
|------|---------|
| ADR Status | Architectural decisions must be accepted before implementation |
| Scope Guardrails | Blocks out-of-scope physics (Poisson, ρ_eff, Schrödinger) |
| Solver Integrity | Verifies solver files are unmodified when not in scope |
| Required Docs | Ensures governance documentation exists |
| Artifacts | Validates generated figures and CSVs |
| Private Forbidden Terms | Blocks sensitive terms via redacted CI secret |

See [AI-RSE Quality Gates](docs/governance/ai_rse_quality_gates.md) for details.

## Scientific Limitations

1. All models use **explicit Euler** time-stepping — first-order accurate.
2. Boundary conditions are simplified (Dirichlet for thermal, Neumann no-flux
   for diffusion/defects).
3. No electrostatics (Poisson equation not implemented).
4. No quantum transport (Schrödinger equation not implemented).
5. No real carrier density (ρ_eff not implemented).
6. Parameters are toy values — no experimental calibration.
7. The defect solver uses Python loops — performance limited to small grids.
8. Fact, hypothesis, inference, and limitation are separated throughout
   the documentation.

## Roadmap

| Version | Status | Scope |
|---------|--------|-------|
| v0.1 | ✅ Released | 1D thermal + diffusion, sensitivity, CI |
| v0.2 | ✅ Released | 2D thermal, convergence analysis, coverage gate |
| v0.3 | ✅ Released | Defect reaction-diffusion, AI-RSE GateOps |
| v0.3.1 | ✅ Released | Strict private terms gate hardening |
| v0.3.2 | ✅ Released | Branch protection, public governance |
| v0.3.3 | ✅ Released | Public repository polish |
| v0.3.4 | ✅ Released | MIT License, public legal metadata |
| v0.3.5 | ✅ Released | Parameter curation, evidence tiers, C_def→ρ_eff spec |
| v0.4 | 📋 ADR-007 Proposed | Poisson bridge scope (Boussinesq-inspired closure) |

## Governance

This project follows the **AcademiaFlow** governance standard:
SDD + Clean Code + TDD + GitHub Actions + semantic commits + ADR-driven scope.

| Document | Path |
|----------|------|
| Implementation Plan | [docs/governance/implementation_plan.md](docs/governance/implementation_plan.md) |
| Walkthrough | [docs/governance/walkthrough.md](docs/governance/walkthrough.md) |
| Project Audit | [docs/governance/project_audit.md](docs/governance/project_audit.md) |
| Technical Debt | [docs/governance/technical_debt.md](docs/governance/technical_debt.md) |
| Branch Protection | [docs/governance/branch_protection.md](docs/governance/branch_protection.md) |
| AI-RSE Quality Gates | [docs/governance/ai_rse_quality_gates.md](docs/governance/ai_rse_quality_gates.md) |
| ADRs | [docs/adr/](docs/adr/) |

## License

This project is licensed under the [MIT License](LICENSE).

## Citation

See [CITATION.cff](CITATION.cff) for citation metadata.
