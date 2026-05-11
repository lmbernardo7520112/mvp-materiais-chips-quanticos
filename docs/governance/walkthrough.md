# Walkthrough — MVP v0.1 / v0.2 / v0.3 / v0.3.1–v0.3.5 / ADR-007 / v0.4.2

> **Date:** 2026-05-11  
> **Status:** ✅ ADR-008 PROPOSED — v0.4.2 SI Unit Conversion & Scale Audit

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

- Evidence tier system: T0/T1/T2/T3/TX/CONST defined and applied
- 4 parameters at T1 (literature-inspired): α, D₀_def, E_D, E_R
- T_G downgraded from T1 to T0 (1100 K ≠ Voronkov ~1100°C = ~1373 K)
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

---

## ADR-007 Poisson Bridge Scope Evidence

> **Date:** 2026-05-09
> **Status:** SPECIFICATION COMPLETE — ADR-007 Accepted, policy v0.4 activated, no implementation

### Scientific Deliverables

| Document | Content |
|----------|--------|
| `docs/adr/ADR-007-v0.4-poisson-bridge-scope.md` | Architecture decision record (Accepted) |
| `docs/decision_briefs/v0.4_boussinesq_inspired_charge_closure.md` | Option C-B derivation |
| `docs/research_council/v0.4_poisson_bridge_council.md` | 5-expert deliberation |
| `docs/governance/v0.4_implementation_plan_draft.md` | Draft impl plan (pending TDD PR) |
| `docs/governance/v0.4_acceptance_gates_draft.md` | 24 draft gates (Activated) |
| `docs/governance/v0.4_risk_matrix_draft.md` | 10 risks identified |
| `docs/quality_gates/policy_v0.4_draft.md` | Policy activated |
| `docs/release_notes/v0.4.0_scope_draft.md` | Scope release notes |

### Key Decisions

- Option C-B (Boussinesq-inspired linearized trap-charge closure) recommended
- δρ_eff = ρ_eff_raw − ⟨ρ_eff_raw⟩ (mean-subtracted perturbation)
- General Poisson form: ∇·(ε∇φ) = −δρ_eff
- ADR-007 status: **Accepted**
- Policy status: **v0.4 Activated**
- Implementation blocked until a dedicated TDD PR is opened

### Non-Regression Confirmations

- ✅ No src/ changes
- ✅ No scripts/ changes
- ✅ No solver modifications
- ✅ C_def remains adimensional proxy
- ✅ Poisson NOT implemented
- ✅ rho_eff NOT implemented
- ✅ policy.json current_stage is now v0.4 (GateOps prepared)

## v0.4 GREEN 1 — effective_charge.py

- **File Created**: `src/mvp_quantum_materials/effective_charge.py`
- **Tests Run**: `PYTHONPATH=. pytest tests/test_effective_charge.py -v --tb=short`
- **Result**: `11 passed` (Green state).
- **Confirmations**:
  - `poisson_solver_2d.py` does not exist yet.
  - `run_poisson_bridge.py` does not exist yet.
  - The global test suite is still expected to fail (missing Poisson solver).

## v0.4 GREEN 2 — poisson_solver_2d.py

- **File Created**: `src/mvp_quantum_materials/poisson_solver_2d.py`
- **Numerical Method Used**: Vectorized Jacobi (Iterative, $\omega=1.0$)
- **Tests Run**: `PYTHONPATH=. pytest tests/test_poisson_solver_2d.py -v --tb=short`
- **Result**: `20 passed` (Green state across both effective_charge and poisson_solver_2d).
- **Confirmations**:
  - `effective_charge.py` continues to pass cleanly.
  - `run_poisson_bridge.py` does not exist yet.
  - `generate_all_results.py` is entirely untouched.
  - The solver explicitly asserts that it is homogeneous, demonstrative, and non-predictive.

## v0.4 GREEN 3 — Poisson Bridge Script & Artifacts

- **Script Created**: `scripts/run_poisson_bridge.py`
- **Command Executed**: `python scripts/run_poisson_bridge.py --output-dir results/figures --tables-dir results/tables`
- **PNG Generated**: `results/figures/poisson_bridge_potential.png`
- **CSV Generated**: `results/tables/poisson_bridge_metrics.csv`
- **Metrics Summary**: max_abs_delta_rho_eff (~3.44e-20), max_abs_phi (~5.38e-24), converged (True).
- **Integration**: `scripts/generate_all_results.py` successfully updated with P-Bridge stage to avoid Quality Gate term violation.
- **Global Validation**: `run_all_quality_gates.py` passed cleanly (0 violations).
- **Confirmation**: The script explicitly outputs demonstrative uncalibrated fields without physical device claims.

## v0.4 GREEN 3 Audit and Final Documentation

- **Audit findings**:
  - pandas: zero references in codebase or pyproject.toml.
  - generate_all_results.py: hardened to use sys.executable.
  - run_poisson_bridge.py: removed cosmetic self-assignments.
- **Documentation created/updated**:
  - docs/release_notes/v0.4.0_draft.md (new).
  - docs/parameters_v0.4_candidates.md (new).
  - docs/governance/technical_debt.md (TD-ADR007-01 resolved).
  - docs/governance/project_audit.md (v0.4 status updated).
  - README.md (v0.4 scope, demonstrative electrostatic modeling).
- **Branch ready for PR**.

## v0.4.1 Deep Parameter Literature Curation

- **Scope:** Documentation-only. Zero src/scripts/tests changes.
- **Literature review:** 11 sources audited (Sze 2007, Bracht 1998, Sinno 1999, Watkins 2000, Fleetwood 2018, Connors 2022, Zwanenburg 2013, Burkard 2023, Stesmans 1998, CODATA 2018, Ioffe Institute).
- **Registry:** 20 parameters classified across CONST/T0/T1/T2/T3/TX/NUM tiers.
- **Unit audit:** C/m2 vs C/m3 documented; eV-1 cm-2 to J-1 m-2 conversion documented; t_eff role clarified.
- **Promotions:** D0_def T0->T1; N_ref TX->T1. No parameter promoted to calibrated.
- **New T2 candidates (not in code):** epsilon_r(Si), epsilon_r(SiO2), D_it.
- **Overclaim audit:** All TX parameters have do_not_claim fields. No calibration claims made.
- **Decision:** Curation only; calibration requires future ADR.

## v0.4.2 — ADR-008 SI Unit Conversion & Scale Audit Proposal

> **Date:** 2026-05-11
> **Branch:** `docs/adr-008-si-units-scale-audit`
> **Status:** DOCUMENTATION-ONLY — ADR-008 Proposed
> **Decision:** Proposal for SI unit conversion infrastructure; no implementation

### Files Created

| File | Purpose |
|------|---------|
| `docs/adr/ADR-008-v0.4.2-si-units-scale-audit.md` | ADR proposing SI unit conversion scope |
| `docs/decision_briefs/v0.4.2_units_vs_demonstrative.md` | Option A/B/C comparison |
| `docs/research_council/v0.4.2_units_scale_council.md` | 5-expert council deliberation |
| `docs/governance/v0.4.2_acceptance_gates.md` | 10 acceptance gates |
| `docs/governance/v0.4.2_risk_matrix.md` | 10 risks identified |
| `docs/release_notes/v0.4.2_draft.md` | Release notes draft |

### Files Updated

| File | Change |
|------|--------|
| `docs/governance/walkthrough.md` | Added v0.4.2 section |
| `docs/governance/project_audit.md` | Added v0.4.2 proposed scope |
| `docs/governance/technical_debt.md` | Added TD-UNITS-02 |

### Key Decisions

- **ADR-008 Status:** Proposed (not Accepted).
- **Council Recommendation:** Option B (literature-scaled constants only) as next step.
- **Option C deferred:** Full charge closure requires ΔE convention, t_eff justification.
- **No implementation:** Zero src/scripts/tests changes.
- **policy.json unchanged:** current_stage remains v0.4.

### Non-Regression Confirmations

- ✅ Zero src/ changes
- ✅ Zero scripts/ changes
- ✅ Zero tests/ changes
- ✅ policy.json current_stage remains v0.4
- ✅ No SI unit conversion implemented
- ✅ No parameter values changed in code
- ✅ No tag created
- ✅ Quality gates green
