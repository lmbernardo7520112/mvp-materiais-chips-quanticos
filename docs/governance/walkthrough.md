# Walkthrough — MVP v0.1

> **Date:** 2026-05-06  
> **Branch:** `feature/mvp-termo-difusivo-quantum-materials`  
> **Status:** Phases 1-6 complete. Awaiting push authorization.

## Evidence Summary

| Gate | Status | Evidence |
|------|--------|----------|
| pytest | ✅ 19/19 passed | `pytest -v --tb=short` → 19 passed in 3.13s |
| ruff check | ✅ Clean | `ruff check .` → All checks passed! |
| ruff format | ✅ Clean | `ruff format --check .` → 20 files already formatted |
| Tests ≥17 | ✅ 19 tests | `pytest --collect-only` → 19 tests collected |
| Figures ≥3 | ✅ 3 figures | `ls results/figures/*.png \| wc -l` → 3 |
| Working tree | ✅ Clean | `git status` → nothing to commit |
| Commits | ✅ 11 atomic | `git log --oneline` → 11 semantic commits |
| ci.yml created | ✅ Exists | `.github/workflows/ci.yml` — matrix 3.11+3.12 |
| CI remoto | ⏳ Pending | Awaiting push authorization |

## Commands Executed

```bash
# Repository setup
git init
git branch -m main
git checkout -b feature/mvp-termo-difusivo-quantum-materials

# Dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Quality gates
pytest -v --tb=short                        # 19/19 passed
ruff check .                                # All checks passed
ruff format --check .                       # 20 files formatted

# Result generation
python scripts/generate_all_results.py --output-dir results/figures
# Output: 3 figures generated
```

## Figures Generated

1. `results/figures/thermal_1d_evolution.png` — Thermal field T(x) evolution
2. `results/figures/diffusion_1d_evolution.png` — Concentration proxy C(x) evolution
3. `results/figures/sensitivity_analysis.png` — Parametric sensitivity (5 params)

## Commits (11 atomic, semantic)

| # | Hash | Message |
|---|------|---------|
| 1 | 8ef23f2 | chore: initialize repository structure |
| 2 | 9a7d73e | docs: add SDD implementation plan and governance tracker |
| 3 | 32b1c74 | docs: add institutional README, references and parameters |
| 4 | 7a4a8d6 | test: add domain and thermal solver specifications |
| 5 | 323bcd7 | feat: implement 1d domain and thermal solver |
| 6 | 0360a13 | test: add diffusion, arrhenius and source specifications |
| 7 | 2450bd9 | feat: implement diffusion model with stability guard |
| 8 | ae6eeee | feat: add metrics and sensitivity analysis |
| 9 | f2a0d42 | feat: add CLI scripts with --output-dir |
| 10 | c20667a | docs: add ADRs and technical debt scorecard |
| 11 | dee45d4 | ci: add GitHub Actions with ruff and matrix |

## Test Inventory (19 tests)

| ID | Test | File | Status |
|----|------|------|--------|
| T-01 | Domain coherence | test_domain.py | ✅ |
| T-01b | dx consistency | test_domain.py | ✅ |
| T-02 | Constant T stable | test_thermal_solver.py | ✅ |
| T-03 | Gradient smooths | test_thermal_solver.py | ✅ |
| T-04 | Finite output | test_thermal_solver.py | ✅ |
| T-05 | Arrhenius D(T) | test_diffusion_solver.py | ✅ |
| T-06 | Source max at Tc | test_diffusion_solver.py | ✅ |
| T-07 | Constant C stable | test_diffusion_solver.py | ✅ |
| T-08 | max/mean ≥ 1 | test_metrics.py | ✅ |
| T-09 | Metrics finite | test_metrics.py | ✅ |
| T-10 | Sensitivity table | test_sensitivity.py | ✅ |
| T-11 | Scripts execute | test_scripts.py | ✅ |
| T-12 | ≥3 figures | test_scripts.py | ✅ |
| T-13 | Source non-neg | test_diffusion_solver.py | ✅ |
| T-14 | Source decays | test_diffusion_solver.py | ✅ |
| T-15 | Thermal rejects dt | test_thermal_solver.py | ✅ |
| T-16 | Diffusion rejects dt | test_diffusion_solver.py | ✅ |
| T-17 | C finite | test_diffusion_solver.py | ✅ |
| Extra | Non-unif=0 const | test_metrics.py | ✅ |

## 2D Status

**DEFERRED** via ADR-003. Not implemented in v0.1.

## Pendências

1. **Push remoto:** Aguardando autorização para `gh repo create` ou push.
2. **CI remoto:** Validação GitHub Actions pendente até push.

> [!NOTE]
> Adendo com status/link do GitHub Actions será adicionado após push autorizado.
