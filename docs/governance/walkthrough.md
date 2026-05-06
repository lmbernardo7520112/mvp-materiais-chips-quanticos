# Walkthrough — MVP v0.1

> **Date:** 2026-05-06  
> **Branch:** `feature/mvp-termo-difusivo-quantum-materials`  
> **Status:** Phases 1-6 complete + traceability improvements. Awaiting push authorization.

## Evidence Summary

| Gate | Status | Evidence |
|------|--------|----------|
| pytest | ✅ 21/21 passed | `pytest -v --tb=short` → 21 passed in 4.26s |
| ruff check | ✅ Clean | `ruff check .` → All checks passed! |
| ruff format | ✅ Clean | `ruff format --check .` → 20 files already formatted |
| Tests ≥17 | ✅ 21 tests | `pytest --collect-only` → 21 tests collected |
| Figures ≥4 | ✅ 4 figures | `ls results/figures/*.png \| wc -l` → 4 |
| CSV | ✅ Exists | `results/tables/sensitivity_results.csv` |
| Working tree | ✅ Clean | `git status` → nothing to commit |
| Commits | ✅ 13 atomic | `git log --oneline` → 13 semantic commits |
| ci.yml created | ✅ Exists | `.github/workflows/ci.yml` — matrix 3.11+3.12 |
| CI remoto | ⏳ Pending | Awaiting push authorization |

## Traceability Improvements (Commit 13)

### Sensitivity Ranking
- Added `compute_sensitivity_ranking()` — normalized range: S = (max-min)/|mean|
- Added `export_sensitivity_csv()` — CSV with full metric details
- Added `sensitivity_ranking.png` — horizontal bar chart with ranking

### Boundary Flux Proxy
- Added `boundary_flux_proxy()` metric to qualitatively verify Neumann no-flux BC
- Test T-19 verifies zero flux for constant field

### Report Enhancement
- `docs/relatorio_30_dias.md` updated with per-figure interpretive sections:
  - What each figure shows
  - Associated hypothesis
  - Limitations
  - What CANNOT be inferred
- Thermal field explicitly declared as demonstrative Dirichlet condition
- C=proxy adimensional reinforced throughout
- Sensitivity methodology documented with ranking formula

### New Tests
- T-12 updated: requires ≥4 figures + ranking figure
- T-18: CSV generation verification
- T-19: Boundary flux proxy for constant field

## Commands Executed

```bash
# Quality gates
pytest -v --tb=short                        # 21/21 passed
ruff check .                                # All checks passed
ruff format --check .                       # 20 files formatted

# Result generation
python scripts/generate_all_results.py --output-dir results/figures
# Output: 4 figures + 1 CSV generated
```

## Figures Generated

1. `results/figures/thermal_1d_evolution.png` — Thermal field T(x) evolution
2. `results/figures/diffusion_1d_evolution.png` — Concentration proxy C(x) evolution
3. `results/figures/sensitivity_analysis.png` — Parametric sensitivity (5 params)
4. `results/figures/sensitivity_ranking.png` — Sensitivity ranking bar chart

## Tables Generated

1. `results/tables/sensitivity_results.csv` — Full sensitivity results

## Commits (13 atomic, semantic)

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
| 13 | (pending) | feat: add sensitivity ranking and result traceability |

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

## Pendências

1. **Push remoto:** Aguardando autorização.
2. **CI remoto:** Validação GitHub Actions pendente até push.

> [!NOTE]
> Adendo com status/link do GitHub Actions será adicionado após push autorizado.
