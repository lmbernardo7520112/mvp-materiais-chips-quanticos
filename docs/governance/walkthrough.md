# Walkthrough — MVP v0.1 / v0.2 / v0.3 / v0.3.1–v0.3.5

> **Date:** 2026-05-09  
> **Status:** ✅ v0.3.5 PARAMETER CURATION SPECIFICATION

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

---

## v0.2 Local Implementation Evidence

> **Date:** 2026-05-06  
> **Branch:** `feature/v0.2-2d-robustness`  
> **Status:** LOCAL IMPLEMENTATION COMPLETE — awaiting push authorization  
> **Version:** 0.2.0 (candidate — tag NOT created yet)

### v0.2 Commits (11 atomic, semantic, TDD)

| # | Hash | Message |
|---|------|---------|
| 1 | 6e1459a | test: add domain2d specifications |
| 2 | bc81718 | feat: implement domain2d |
| 3 | f7fb0ea | test: add thermal 2d stability specifications |
| 4 | cc26363 | feat: add thermal 2d stability guard |
| 5 | d9db771 | test: add thermal solver 2d specifications |
| 6 | 0d19ff0 | feat: implement thermal solver 2d |
| 7 | 8be83f2 | test: add convergence analysis specifications |
| 8 | dbc2b4a | feat: implement convergence analysis |
| 9 | c2c7a57 | feat: add 2d scripts, plots and update result generation |
| 10 | 2cd88a9 | ci: add coverage gate and v0.2 artifact verification |
| 11 | f37a01e | docs: update governance and bump version to 0.2.0 |

### Files Created

| File | Type |
|------|------|
| `src/mvp_quantum_materials/thermal_solver_2d.py` | Module — 2D thermal solver |
| `src/mvp_quantum_materials/convergence.py` | Module — convergence analysis |
| `scripts/run_thermal_2d.py` | Script — 2D thermal CLI |
| `scripts/run_convergence.py` | Script — convergence CLI |
| `tests/test_domain_2d.py` | Tests — Domain2D (11 tests) |
| `tests/test_stability_2d.py` | Tests — 2D stability (5 tests) |
| `tests/test_thermal_solver_2d.py` | Tests — 2D solver (6 tests) |
| `tests/test_convergence.py` | Tests — convergence (6 tests) |
| `tests/test_plots.py` | Tests — direct plot coverage (5 tests) |

### Files Modified (additive-only)

| File | Change |
|------|--------|
| `src/mvp_quantum_materials/domain.py` | Add Domain2D (Domain1D untouched) |
| `src/mvp_quantum_materials/config.py` | Add `compute_max_stable_dt_thermal_2d` (1D functions untouched) |
| `src/mvp_quantum_materials/plots.py` | Add `plot_thermal_2d_final` (1D functions untouched) |
| `scripts/generate_all_results.py` | Add 2D thermal + convergence outputs (1D outputs preserved) |
| `tests/test_scripts.py` | Add v0.2 artifact tests (v0.1 tests preserved) |
| `pyproject.toml` | Add pytest-cov, bump to 0.2.0, add N803 ignore |
| `src/mvp_quantum_materials/__init__.py` | Bump `__version__` to 0.2.0 |
| `.github/workflows/ci.yml` | Add coverage gate, v0.2 artifact verification |

### Quality Gates

| Gate | Result |
|------|--------|
| pytest | ✅ 56/56 passed |
| Coverage | ✅ 92.44% (gate: 70%) |
| ruff check | ✅ All checks passed |
| ruff format | ✅ 29 files formatted |
| v0.1 regression | ✅ 21 original tests pass |
| v0.1 artifacts | ✅ 4 figures + 1 CSV preserved |
| Convergence order | ✅ observed_order ≥ 1.5 |

### Figures Generated (6 total)

1. `results/figures/thermal_1d_evolution.png` (v0.1)
2. `results/figures/diffusion_1d_evolution.png` (v0.1)
3. `results/figures/sensitivity_analysis.png` (v0.1)
4. `results/figures/sensitivity_ranking.png` (v0.1)
5. `results/figures/thermal_2d_final.png` (v0.2 — new)
6. `results/figures/convergence_analysis.png` (v0.2 — new)

### Tables Generated (2 total)

1. `results/tables/sensitivity_results.csv` (v0.1)
2. `results/tables/convergence_results.csv` (v0.2 — new)

### Non-Regression Confirmations

- ✅ `thermal_solver.py`: **zero diff** vs main
- ✅ `diffusion_solver.py`: **zero diff** vs main
- ✅ All 21 v0.1 tests passing
- ✅ All 4 v0.1 figures generated
- ✅ `sensitivity_results.csv` generated
- ✅ C remains adimensional proxy
- ✅ Scientific disclaimers intact

### Scope Exclusions (confirmed)

- ✅ Diffusion 2D: **deferred** (SHOULD conditional — documented in TD)
- ✅ Notebooks/Jupytext: **deferred** (SHOULD — documented in TD)
- ✅ Morris/Sobol global sensitivity: **deferred** (COULD — documented in TD)
- ✅ Poisson/Schrödinger/TCAD: **NOT implemented** (WON'T until v0.4/v0.5)
- ✅ Czochralski/phase-field/OpenFOAM: **NOT implemented**
- ✅ Quantum coherence: **NOT implemented** (ADR-002 permanent)

### Version Note

- `pyproject.toml` and `__init__.py` set to `0.2.0`
- Tag `v0.2.0` created on main after PR #4 merge and CI green
- Merge commit: `77e37ba`

---

## v0.2.1 Institutional Release Evidence

> **Date:** 2026-05-07
> **Branch:** `feature/v0.2.1-institutional`
> **Status:** Documentation-only release — no physics changes

### Files Created

| File | Type |
|------|------|
| `docs/release_notes/v0.2.0.md` | Release notes formal |
| `docs/tutorials/reproduce_v0.2.0.md` | Reproducibility tutorial |
| `notebooks/v0.2_demo.py` | Jupytext percent-format notebook |
| `docs/decision_briefs/v0.2.1_vs_v0.3.md` | Strategic decision brief |
| `docs/institutional/cnpem_lnnano_summary.md` | Institutional summary |
| `docs/governance/v0.2.1_task.md` | Task tracker |

### Confirmations

- ✅ No physics changes
- ✅ No solver modifications (thermal_solver.py, diffusion_solver.py: zero diff)
- ✅ Diffusion 2D NOT implemented (remains deferred)
- ✅ v0.3 NOT started
- ✅ C remains adimensional proxy
- ✅ Notebook executes correctly (Agg backend, no new logic)
- ✅ Decision brief answers 6 banca-level questions
- ✅ Institutional summary uses prudent tone

---

## v0.3 Core Implementation Evidence

> **Date:** 2026-05-08
> **Branch:** `feature/v0.3-defect-like-core`
> **Status:** LOCAL IMPLEMENTATION COMPLETE — awaiting push authorization
> **ADR:** ADR-006 (Accepted)

### v0.3 Commits

| # | Hash | Message |
|---|------|---------|
| 1 | 252c86f | feat: implement defect kinetics D(T), G(T), R(T) with TDD |
| 2 | c74cece | feat: implement defect stability guard with TDD |
| 3 | 56df00d | feat: implement 2D defect reaction-diffusion solver with TDD |
| 4 | 9d9c6dc | feat: implement defect proxy metrics with TDD |
| 5 | f9c59c5 | feat: add defect 2D CLI, plots, and artifact generation |
| 6 | 741225a | ci: validate v0.3 defect artifacts in CI pipeline |
| 7 | 156822e | docs: update v0.3 governance and technical report |
| 8 | 2726fb2 | style: apply ruff formatting to v0.3 modules |
| 9 | 5381d64 | fix: resolve Pylance/pyright type errors in diffusion_solver and plots |
| 10 | 6f277ed | test: verify v0.3 artifact generation and C_def boundedness |
| 11 | 5edb0bc | docs: complete v0.3 local implementation governance |
| 12 | cad02f1 | docs: remove out-of-scope platform reference |
| 13 | 082950f | docs: complete v0.3 release governance |
| 14 | 9a1e9de | docs: sanitize out-of-scope platform references |

### Files Created

| File | Type |
|------|------|
| `src/mvp_quantum_materials/defect_kinetics.py` | Module — D(T), G(T), R(T) |
| `src/mvp_quantum_materials/defect_stability.py` | Module — CFL-like stability guard |
| `src/mvp_quantum_materials/defect_solver_2d.py` | Module — 2D reaction-diffusion solver |
| `src/mvp_quantum_materials/defect_metrics.py` | Module — proxy metrics |
| `scripts/run_defect_2d.py` | Script — defect CLI |
| `tests/test_defect_kinetics.py` | Tests — 11 kinetics tests |
| `tests/test_defect_stability.py` | Tests — 6 stability tests |
| `tests/test_defect_solver_2d.py` | Tests — 11 solver tests |
| `tests/test_defect_metrics.py` | Tests — 5 metrics tests |
| `docs/relatorio_v0.3.md` | Technical report |
| `docs/release_notes/v0.3.0_draft.md` | Release notes draft |

### Files Modified (additive-only)

| File | Change |
|------|--------|
| `plots.py` | Add `plot_defect_2d_final`; fix `matplotlib.colormaps[]` (Pylance) |
| `generate_all_results.py` | Add v0.3 defect outputs |
| `ci.yml` | Add v0.3 artifact verification |
| `test_scripts.py` | Add 3 v0.3 artifact tests |
| `parameters.md` | Add v0.3 parameter table |
| `technical_debt.md` | Add TD-v0.3-01/02/03 |
| `v0.3_task.md` | Mark items complete |

### Controlled Exception: diffusion_solver.py

| Aspect | Detail |
|--------|--------|
| **File** | `diffusion_solver.py` |
| **Change** | `@overload` type signatures for `arrhenius_diffusivity` |
| **Reason** | Resolve Pylance/Pyright `reportIndexIssue` |
| **Behavioral impact** | **Zero** — type annotations only |
| **Physics impact** | **Zero** — no formula, loop, BC, or return change |

### Quality Gates

| Gate | Result |
|------|--------|
| pytest | ✅ 92/92 passed |
| Coverage | ✅ 91.78% (gate 70%) |
| ruff check | ✅ All checks passed |
| ruff format | ✅ All files formatted |
| pyright | ✅ 0 errors, 0 warnings |
| generate_all_results | ✅ 9 figures + 4 CSVs |

### v0.3 Artifacts

| Artifact | Type |
|----------|------|
| `defect_2d_final.png` | Figure — C_def contour |
| `defect_metrics.csv` | CSV — proxy metrics |
| `defect_final_snapshot.csv` | CSV — C_def snapshot for v0.4 |

### Non-Regression Confirmations

- ✅ `thermal_solver.py`: **zero diff** vs main
- ✅ `diffusion_solver.py`: **type-only** @overload fix (zero behavior change)
- ✅ All 56 v0.1/v0.2 tests passing
- ✅ All 6+2 v0.1/v0.2 artifacts preserved
- ✅ C_def remains adimensional proxy
- ✅ Parameters classified as toy/demonstrative
- ✅ Poisson NOT implemented
- ✅ ρ_eff NOT implemented
- ✅ Schrödinger NOT implemented
- ✅ Charge noise NOT predicted
- ✅ Zero references to explicitly excluded out-of-scope quantum-material platforms

---

## v0.3.1 Hardening Evidence

> **Date:** 2026-05-09
> **Tag:** v0.3.1
> **Status:** HARDENING COMPLETE

### Changes (PR #9)

| # | Hash | Message |
|---|------|---------|
| 1 | 0793b71 | test: harden private forbidden terms gate tests / chore: redact output |
| 2 | df9e543 | ci: enable strict private terms gate |
| 3 | 3e18944 | docs: document strict private terms secret setup |
| 4 | c6cfdd7 | style: fix trailing whitespace |
| 5 | 1ecb842 | style: apply ruff format |
| 6 | a2084c9 | fix: handle invalid regex gracefully |
| 7 | 5acf108 | fix: do not split private terms regex by pipe |

### Security Hardening

| Measure | Status |
|---------|--------|
| `PRIVATE_FORBIDDEN_TERMS_REGEX` secret | ✅ Configured |
| `--strict-private-terms` in CI | ✅ Active |
| Violation output redacted | ✅ No term, regex, or line content leaked |
| Invalid regex handled gracefully | ✅ No crash, no value exposure |
| Secret value stored in repo | ❌ Never |

### Branch Protection (post v0.3.1)

| Rule | Status |
|------|--------|
| PR required before merge | ✅ Active |
| Required status checks: `quality (3.11)`, `quality (3.12)` | ✅ Active |
| Strict mode (branch up to date) | ✅ Active |
| Conversation resolution required | ✅ Active |
| Force push blocked | ✅ Active |
| Branch deletion blocked | ✅ Active |
| Repository visibility | Public |

### Quality Gates

| Gate | Result |
|------|--------|
| pytest | ✅ 114/114 passed |
| Coverage | ✅ 91.78% (gate 70%) |
| ruff | ✅ Verde |
| pyright | ✅ 0 errors |
| AI-RSE GateOps | ✅ 6/6 gates pass |
| Strict private terms | ✅ Active in CI |

### Non-Regression Confirmations

- ✅ No physics changes
- ✅ No solver modifications
- ✅ C_def remains adimensional proxy
- ✅ Poisson NOT implemented
- ✅ rho_eff NOT implemented
- ✅ policy.json current_stage remains v0.3

---

## v0.3.3 Public Repository Polish Evidence

> **Date:** 2026-05-09
> **Status:** PUBLIC POLISH COMPLETE

### Files Created

| File | Type |
|------|------|
| `README.md` | Complete rewrite for public audience |
| `CITATION.cff` | Citation metadata |
| `CONTRIBUTING.md` | Contribution guidelines |
| `SECURITY.md` | Security policy |
| `docs/decision_briefs/public_release_metadata.md` | License decision brief |
| `docs/release_notes/v0.3.3_draft.md` | Release notes draft |

### Files Modified

| File | Change |
|------|--------|
| `docs/governance/implementation_plan.md` | Sanitized local path |
| `docs/governance/walkthrough.md` | Added v0.3.3 evidence |
| `docs/governance/project_audit.md` | Updated for v0.3.3 |
| `docs/governance/technical_debt.md` | Resolved README TD |

### Non-Regression Confirmations

- ✅ No physics changes
- ✅ No solver modifications
- ✅ C_def remains adimensional proxy
- ✅ Poisson NOT implemented
- ✅ rho_eff NOT implemented
- ✅ policy.json current_stage remains v0.3
- ✅ License decision deferred to user (MIT recommended)

---

## v0.3.4 MIT License Release Evidence

> **Date:** 2026-05-09
> **Status:** LICENSE RELEASE COMPLETE

### Files Created

| File | Type |
|------|------|
| `LICENSE` | MIT License |
| `docs/release_notes/v0.3.4_draft.md` | Release notes draft |

### Files Modified

| File | Change |
|------|--------|
| `README.md` | MIT badge + license section updated |
| `CITATION.cff` | Added `license: MIT`, bumped version |
| `docs/decision_briefs/public_release_metadata.md` | Marked Accepted |
| `docs/governance/walkthrough.md` | Added v0.3.4 evidence |
| `docs/governance/project_audit.md` | Updated for v0.3.4 |
| `docs/governance/technical_debt.md` | Resolved LICENSE TD |

### Non-Regression Confirmations

- ✅ No physics changes
- ✅ No solver modifications
- ✅ C_def remains adimensional proxy
- ✅ Poisson NOT implemented
- ✅ rho_eff NOT implemented
- ✅ policy.json current_stage remains v0.3
- ✅ MIT License formally adopted

---

## v0.3.5 Parameter Curation & Registry Evidence

> **Date:** 2026-05-09
> **Status:** SPECIFICATION COMPLETE — no implementation

### Scientific Deliverables

| Document | Content |
|----------|--------|
| `docs/literature_review/v0.3.5_parameter_curation.md` | 10 sources, 5 blocks (A–E) |
| `docs/parameters_v0.3.5_curated_candidates.md` | Full parameter taxonomy with evidence tiers |
| `docs/decision_briefs/Cdef_to_rhoeff_mapping_options.md` | 3 mapping options compared |
| `docs/parameter_registry/v0.3.5_parameter_registry.json` | 17 parameters in machine-readable format |

### Key Findings

- Evidence tier system: T0/T1/T2/T3/TX defined and applied
- 4 parameters at T1 (literature-inspired): α, D₀_def, E_D, T_G, E_R
- 2 fields at TX (forbidden physical interpretation): C, C_def
- Option C (trap/interface occupancy proxy) preferred for ADR-007
- No implementation performed

### Non-Regression Confirmations

- ✅ No src/ changes
- ✅ No scripts/ changes
- ✅ No tests/ changes
- ✅ No solver modifications
- ✅ C_def remains adimensional proxy
- ✅ Poisson NOT implemented
- ✅ rho_eff NOT implemented
- ✅ policy.json current_stage remains v0.3
