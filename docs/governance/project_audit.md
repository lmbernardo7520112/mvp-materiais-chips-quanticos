# Project Audit — MVP v0.1

> **Date:** 2026-05-06  
> **Auditor:** Staff Research Software Engineer (AI-assisted)

## Repository Topology

```
mvp-materiais-chips-quanticos/
├── .github/                    # CI/CD and templates
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/ci.yml
├── docs/                       # Documentation
│   ├── adr/                    # 3 ADRs
│   ├── governance/             # 5 governance documents
│   ├── hipoteses_e_limitacoes.md
│   ├── parameters.md
│   ├── plano_tecnico_mvp.md
│   ├── referencias.md
│   └── relatorio_30_dias.md
├── notebooks/README.md         # Stub (deferred to v0.2)
├── results/
│   ├── figures/                # 4 generated figures
│   └── tables/                 # 1 CSV (sensitivity)
├── scripts/                    # 4 CLI scripts
├── src/mvp_quantum_materials/  # 7 modules
└── tests/                      # 6 test files, 21 tests
```

## File Inventory

### Source (7 modules)
| File | Purpose |
|------|---------|
| __init__.py | Package init, disclaimers |
| config.py | Dataclasses, constants, stability functions |
| domain.py | Domain1D |
| thermal_solver.py | Thermal solver, Dirichlet, stability guard |
| diffusion_solver.py | Diffusion, Arrhenius, source, Neumann, finiteness |
| metrics.py | 7 heterogeneity metrics (incl. boundary flux proxy) |
| sensitivity.py | 5-parameter analysis, CSV export, ranking |
| plots.py | 4 figure types |

### Tests (6 files, 21 tests)
| File | Tests | Coverage |
|------|-------|----------|
| test_domain.py | 2 | Domain1D coherence |
| test_thermal_solver.py | 4 | T-02,03,04,15 |
| test_diffusion_solver.py | 7 | T-05,06,07,13,14,16,17 |
| test_metrics.py | 4 | T-08,09,19,extra |
| test_sensitivity.py | 1 | T-10 |
| test_scripts.py | 3 | T-11,12,18 |

### Results
| File | Purpose |
|------|---------|
| thermal_1d_evolution.png | Thermal field evolution |
| diffusion_1d_evolution.png | Concentration proxy evolution |
| sensitivity_analysis.png | Parameter variation curves |
| sensitivity_ranking.png | Ranked sensitivity bar chart |
| sensitivity_results.csv | Full tabular sensitivity data |

### Documentation (14+ files)
| File | Purpose |
|------|---------|
| README.md | Institutional README |
| docs/referencias.md | 14 references |
| docs/hipoteses_e_limitacoes.md | 7 limitations |
| docs/parameters.md | Parameter table |
| docs/plano_tecnico_mvp.md | Technical plan |
| docs/relatorio_30_dias.md | Interpretive report (per-figure) |
| docs/adr/ADR-001..003 | 3 ADRs |
| docs/governance/* | 5 governance docs |

## Metrics

| Metric | Value |
|--------|-------|
| Tests | 21 |
| pytest result | 21/21 passed |
| ruff check | All checks passed |
| ruff format | 20 files formatted |
| Figures generated | 4 |
| CSV tables | 1 |
| References documented | 14 |
| ADRs | 3 |
| Technical debts (open) | 0 |
| Technical debts (deferred) | 2 |
| Commits | 13 |
| Branch | feature/mvp-termo-difusivo-quantum-materials |
| Working tree | Clean |
| CI remoto | Pending (push not authorized) |

## Risks & Limitations

1. **C is adimensional proxy** — documented in README, hipóteses, parameters, report.
2. **No industrial simulation** — L-02.
3. **No quantum coherence prediction** — ADR-002, L-03.
4. **No solidification equivalence** — L-04.
5. **Toy/demonstrative parameters** — documented in parameters.md.
6. **2D deferred** — ADR-003, TD-01.
7. **Notebooks deferred** — TD-02.

## Next Steps (v0.2)

1. Implement 2D simplified case.
2. Create Jupyter notebooks from scripts.
3. Add convergence analysis.
4. Consider ADI or implicit solver.
5. Explore parameter calibration with literature.
6. Coverage measurement with pytest-cov.
7. Global sensitivity methods (Sobol/Morris).
