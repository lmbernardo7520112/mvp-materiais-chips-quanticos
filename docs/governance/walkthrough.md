# Walkthrough — MVP v0.1

> **Date:** 2026-05-06  
> **Status:** ✅ V0.1 RELEASE CLOSED

## Post-Merge Validation Evidence

| Item | Value |
|------|-------|
| **PR #1** | [Merged via merge commit](https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos/pull/1) |
| **Target Branch** | `main` |
| **Final Commit** | `dbfa832` |
| **Tag** | `v0.1.0` (contained in `main`) |
| **Post-Merge `pytest`** | ✅ 21/21 passed in `main` |
| **Post-Merge `ruff`** | ✅ Clean in `main` |
| **Post-Merge Figures** | ✅ 4 generated |
| **Working Tree** | ✅ Clean |

## Remote Validation Evidence

| Item | Value |
|------|-------|
| **Repository URL** | https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos |
| **Visibility** | Private |
| **Branch pushed** | `feature/mvp-termo-difusivo-quantum-materials` |
| **Push CI Run** | [25450236235](https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos/actions/runs/25450236235) — ✅ success |
| **PR CI Run** | [25450411341](https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos/actions/runs/25450411341) — ✅ success |

## Confirmations

- ✅ 2D permanece deferido via ADR-003
- ✅ Nenhuma alteração de escopo físico
- ✅ C permanece documentado como proxy adimensional
- ✅ Repositório remoto é privado

## Figures Generated

1. `results/figures/thermal_1d_evolution.png`
2. `results/figures/diffusion_1d_evolution.png`
3. `results/figures/sensitivity_analysis.png`
4. `results/figures/sensitivity_ranking.png`

## Tables Generated

1. `results/tables/sensitivity_results.csv`

## Commits (13 atomic, semantic + 1 merge)

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
| 12 | f14179f | docs: add walkthrough and project audit for v0.1 |
| 13 | 38b44d2 | feat: add sensitivity ranking and result traceability |
| 14 | fa0481f | docs: add remote ci validation evidence |
| 15 | dbfa832 | Merge pull request #1 from lmbernardo7520112/feature/mvp-termo-difusivo-quantum-materials |

## Test Inventory (21 tests)

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
| T-12 | ≥4 figures + ranking | test_scripts.py | ✅ |
| T-13 | Source non-neg | test_diffusion_solver.py | ✅ |
| T-14 | Source decays | test_diffusion_solver.py | ✅ |
| T-15 | Thermal rejects dt | test_thermal_solver.py | ✅ |
| T-16 | Diffusion rejects dt | test_diffusion_solver.py | ✅ |
| T-17 | C finite | test_diffusion_solver.py | ✅ |
| T-18 | CSV generated | test_scripts.py | ✅ |
| T-19 | Boundary flux=0 const | test_metrics.py | ✅ |
| Extra | Non-unif=0 const | test_metrics.py | ✅ |
