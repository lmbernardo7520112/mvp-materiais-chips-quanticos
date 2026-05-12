# Project Audit — MVP v0.1 / v0.2 / v0.3 / v0.3.1–v0.3.9 / v0.4

> **Date:** 2026-05-10  
> **Auditor:** Staff Research Software Engineer (AI-assisted)  
> **Status:** ADR-007 ACCEPTED ✅ | v0.4 IMPLEMENTED ✅ | main PROTECTED ✅

## Remote Infrastructure

| Item | Value |
|------|-------|
| Repository | https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos |
| Visibility | **Public** |
| Branch | `main` (protected) |
| PR #1 | [Merged](https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos/pull/1) — v0.1 |
| PR #2 | [Merged](https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos/pull/2) — v0.2 spec |
| PR #3 | [Merged](https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos/pull/3) — ADR-004 acceptance |
| PR #8 | [Merged](https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos/pull/8) — v0.3 core + AI-RSE GateOps |
| PR #9 | [Merged](https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos/pull/9) — v0.3.1 strict private terms |
| Tags | `v0.1.0`, `v0.2.0`, `v0.3.0`, `v0.3.1` |
| Branch protection | Required checks: `quality (3.11)`, `quality (3.12)` |

---

## v0.1 Repository Topology

```
mvp-materiais-chips-quanticos/
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/ci.yml
├── docs/
│   ├── adr/ (3 ADRs)
│   ├── governance/ (5 governance docs)
│   ├── hipoteses_e_limitacoes.md
│   ├── parameters.md
│   ├── plano_tecnico_mvp.md
│   ├── referencias.md
│   └── relatorio_30_dias.md
├── notebooks/README.md
├── results/
│   ├── figures/ (4 figures)
│   └── tables/ (1 CSV)
├── scripts/ (4 CLI scripts)
├── src/mvp_quantum_materials/ (7 modules)
└── tests/ (6 files, 21 tests)
```

## v0.1 Metrics

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
| Technical debts (deferred) | 3 |
| Commits | 13 feature + 1 merge |
| CI runs (all green) | 2 (feature) + 1 (main pending) |
| Working tree | Clean |

## v0.1 Confirmations

- ✅ 2D permanece deferido via ADR-003
- ✅ Nenhum escopo físico novo introduzido
- ✅ C permanece documentado como proxy adimensional
- ✅ Repositório remoto é privado
- ✅ PR #1 mergeado de forma controlada (merge commit)
- ✅ Tag v0.1.0 intacta e válida

---

## v0.2 Audit — Local Implementation

> **Branch:** `feature/v0.2-2d-robustness`  
> **Status:** LOCAL COMPLETE — awaiting push

### v0.2 Repository Topology (delta from v0.1)

```
mvp-materiais-chips-quanticos/
├── .github/workflows/ci.yml                    [MODIFIED — coverage gate]
├── docs/
│   ├── adr/
│   │   ├── ADR-004-v0.2-scope-selection.md     [NEW — Accepted]
│   │   └── ADR-005-process-to-device-bridge.md [NEW — roadmap]
│   ├── governance/
│   │   ├── v0.2_implementation_plan.md         [NEW — spec]
│   │   ├── v0.2_task.md                        [NEW — tracker]
│   │   ├── v0.2_risk_matrix.md                 [NEW — 11 risks]
│   │   ├── v0.2_acceptance_gates.md            [NEW — 26 gates]
│   │   ├── walkthrough.md                      [MODIFIED — v0.2 evidence]
│   │   ├── project_audit.md                    [MODIFIED — v0.2 section]
│   │   └── technical_debt.md                   [MODIFIED — v0.2 TDs]
│   ├── research_council/
│   │   └── evolution_deliberation.md           [NEW]
│   ├── relatorio_v0.2.md                       [NEW]
│   └── parameters.md                           [MODIFIED — 2D params]
├── results/
│   ├── figures/ (6 figures: 4 v0.1 + 2 v0.2)
│   └── tables/ (2 CSVs: 1 v0.1 + 1 v0.2)
├── scripts/ (6 CLI scripts: 4 v0.1 + 2 v0.2)
├── src/mvp_quantum_materials/ (9 modules: 7 v0.1 + 2 v0.2)
└── tests/ (11 files, 56 tests: 21 v0.1 + 35 v0.2)
```

### New Modules (v0.2)

| Module | Purpose |
|--------|---------|
| `thermal_solver_2d.py` | 2D heat equation: explicit Euler, Dirichlet BCs, stability guard |
| `convergence.py` | Manufactured analytical solution, mesh refinement, CSV/plot export |

### Extended Modules (additive-only)

| Module | Extension |
|--------|-----------|
| `domain.py` | `Domain2D` dataclass (Domain1D untouched) |
| `config.py` | `compute_max_stable_dt_thermal_2d` (1D functions untouched) |
| `plots.py` | `plot_thermal_2d_final` contour function (1D functions untouched) |

### New Scripts (v0.2)

| Script | Purpose |
|--------|---------|
| `run_thermal_2d.py` | Run 2D thermal simulation |
| `run_convergence.py` | Run convergence analysis with CSV and figure |

### v0.2 Metrics

| Metric | v0.1 | v0.2 | Delta |
|--------|------|------|-------|
| Tests | 21 | 56 | +35 |
| Coverage | N/A | 92.44% | Gate: 70% |
| Figures | 4 | 6 | +2 |
| CSVs | 1 | 2 | +1 |
| Source modules | 7 | 9 | +2 |
| Scripts | 4 | 6 | +2 |
| Test files | 6 | 11 | +5 |
| ADRs | 3 | 5 | +2 |
| Commits | 15 | 26 | +11 |

### Risks Mitigated

| Risk | Status |
|------|--------|
| R-01: Numerical instability 2D | ✅ Stability guard + CFL formula |
| R-02: No convergence evidence | ✅ Manufactured solution + observed_order ≥ 1.5 |
| R-03: Coverage blind spots | ✅ 92.44% coverage with CI gate |
| R-04: v0.1 regression | ✅ Zero diff on 1D solvers, 21 tests pass |
| R-11: Additive-only violation | ✅ thermal_solver.py and diffusion_solver.py untouched |

### Residual Risks

| Risk | Status | Mitigation |
|------|--------|------------|
| Diffusion 2D not tested | DEFERRED | Documented in TD-v0.2-01 |
| Parameters not calibrated | ACKNOWLEDGED | Documented in TD-v0.2-05, disclaimers present |
| sensitivity.py coverage 59% | LOW | Subprocess coverage boundary; OAT is demonstrative |

## v0.2.0 Release Status

1. ✅ Branch `feature/v0.2-2d-robustness` pushed
2. ✅ PR #4 created and CI green (5/5 checks)
3. ✅ PR #4 merged to main
4. ✅ Tag `v0.2.0` created on main (`77e37ba`)
5. ✅ CI green on main post-merge

---

## v0.2.1 Institutional Release Audit

> **Date:** 2026-05-07  
> **Type:** Documentation-only release

### New Documentation

| Document | Purpose |
|----------|---------|
| `docs/release_notes/v0.2.0.md` | Formal changelog for v0.2.0 |
| `docs/tutorials/reproduce_v0.2.0.md` | Step-by-step reproducibility guide |
| `notebooks/v0.2_demo.py` | Jupytext demonstrative notebook |
| `docs/decision_briefs/v0.2.1_vs_v0.3.md` | Strategic decision: why v0.2.1 before v0.3 |
| `docs/institutional/cnpem_lnnano_summary.md` | Institutional summary for partners |
| `docs/governance/v0.2.1_task.md` | Task tracker |

### v0.2.1 Metrics

| Metric | v0.2.0 | v0.2.1 | Delta |
|--------|--------|--------|-------|
| Tests | 56 | 56 | 0 (no code changes) |
| Coverage | 92.44% | 92.44% | 0 |
| Figures | 6 | 6 | 0 |
| CSVs | 2 | 2 | 0 |
| Documentation files | ~25 | ~31 | +6 |

### Scope Confirmation

- ✅ No physics changes
- ✅ No solver modifications
- ✅ Diffusion 2D remains deferred
- ✅ v0.3 not started
- ✅ C remains adimensional proxy

---

## v0.3 Core Implementation Audit

> **Date:** 2026-05-08
> **Branch:** `feature/v0.3-defect-like-core`

### Topology v0.3

| Layer | Files |
|-------|-------|
| Kinetics | `defect_kinetics.py` — D(T), G(T), R(T) |
| Stability | `defect_stability.py` — CFL-like guard |
| Solver | `defect_solver_2d.py` — explicit Euler, Neumann no-flux |
| Metrics | `defect_metrics.py` — proxy summary statistics |
| CLI | `run_defect_2d.py` |
| Plots | `plots.py` → `plot_defect_2d_final` |
| Tests | 4 test files (33 new tests) |

### v0.3 Metrics

| Metric | v0.2.1 | v0.3 | Delta |
|--------|--------|------|-------|
| Tests | 56 | 92 | +36 |
| Coverage | 92.44% | 91.78% | −0.66% (new code well-tested; sensitivity.py ratio) |
| Figures | 6 | 9 | +3 (1 defect + 2 notebook) |
| CSVs | 2 | 4 | +2 |
| Source modules | 8 | 12 | +4 |
| pyright errors | 6 | 0 | −6 (resolved) |

### Controlled Exception

| File | Nature | Impact |
|------|--------|--------|
| `diffusion_solver.py` | `@overload` type annotations | **Zero behavioral change** |
| `plots.py` | `matplotlib.colormaps[]` API migration | **Zero behavioral change** |

Both changes resolve Pylance/Pyright IDE errors. Neither changes
any calculation, formula, loop, boundary condition, or return value.

### Risks Mitigated

| Risk | Status |
|------|--------|
| R-30: C_def unbounded | ✅ Clipping [0, C_sat] + test verification |
| R-31: Stability violation | ✅ CFL guard with safety_factor=0.4 |
| R-32: v0.1/v0.2 regression | ✅ 56 existing tests pass, zero diff on thermal_solver.py |
| R-33: Scope creep (Poisson) | ✅ Zero Poisson/Schrödinger/TCAD in code |
| R-34: False calibration claims | ✅ All params labeled toy/demonstrative |
| R-35: Out-of-scope platform leakage | ✅ Zero occurrences |

### Residual Risks

| Risk | Status | Mitigation |
|------|--------|------------|
| Defect params not calibrated | DEFERRED | TD-v0.3-01 |
| Poisson not yet coupled | DEFERRED | TD-v0.3-02 |
| Solver perf on fine grids | DEFERRED | TD-v0.3-03 |
| sensitivity.py coverage 59% | LOW | Pre-existing, OAT is demonstrative |

---

## Next Steps

1. v0.3: push branch, create PR, CI green, merge, tag v0.3.0
2. v0.4: Poisson 2D — ∇·(ε∇φ) = −ρ_eff with C_def → ρ_eff coupling
3. v0.5: Schrödinger simplificado
4. Parameter curation: real defect/trap data from peer-reviewed literature

---

## v0.4 Preparation Audit

> **Date:** 2026-05-10
> **Status:** GOVERNANCE PREPARED ✅ — implementation complete

- ✅ **ADR-007**: Accepted (Option C-B).
- ✅ **Policy Stage**: Activated `current_stage: v0.4`.
- ✅ **effective_charge.py**: Implemented (11 tests passing).
- ✅ **poisson_solver_2d.py**: Implemented (9 tests passing).
- ✅ **run_poisson_bridge.py**: Implemented and integrated.
- ✅ **Quality Gates**: 6/6 PASS.
- ✅ **Artifacts**: poisson_bridge_potential.png + poisson_bridge_metrics.csv.
- ✅ **Next Phase**: PR review, merge, and tag v0.4.0.

## v0.4.1 Parameter Curation Audit

> **Date:** 2026-05-10
> **Status:** DOCUMENTATION COMPLETE

- Registry: 20 parameters, 7 tiers (CONST/T0/T1/T2/T3/TX/NUM).
- Sources: 11 references (BibTeX).
- Unit audit: surface vs volume density distinction documented.
- Overclaim audit: all TX params have do_not_claim fields.
- Zero src/scripts/tests changes.
- No calibration performed.

## v0.4.2 Proposed Scope

> **Date:** 2026-05-11
> **Status:** ADR-008 PROPOSED — documentation only

- **ADR-008:** SI Unit Conversion & Parameter Scale Audit.
- **Branch:** `docs/adr-008-si-units-scale-audit`.
- **Type:** Documentation-only proposal. Zero code changes.
- **Decision brief:** Options A (demonstrative), B (literature-scaled constants), C (full charge closure).
- **Council:** 5 simulated experts, unanimous vote for Option B.
- **Risks:** 10 risks identified, 3 Critical (R1, R2, R7).
- **Gates:** 10 acceptance gates defined.
- **policy.json:** Unchanged (current_stage v0.4).
- **No implementation authorized** until ADR-008 is Accepted via PR review.

## v0.4.4 — SI Constants Scaffolding

- **ADR-008:** Accepted (v0.4.3).
- **Branch:** `feature/v0.4.4-si-constants-scaffolding`.
- **Option:** B — literature-scaled constants only (dimensional scaffolding).
- **Modules added:**
  - `src/mvp_quantum_materials/units.py` — SI constants and permittivity lookups.
  - `src/mvp_quantum_materials/scale_modes.py` — Scale mode, geometry mode, and potential interpretation metadata.
- **Tests added:**
  - `tests/test_units.py` — 12 tests for constants, permittivity, docstring disclaimers.
  - `tests/test_scale_modes.py` — 19 tests for enum values, metadata defaults, safety invariants.
- **Total tests:** 167 (136 original + 31 new).
- **Coverage:** 91.02%.
- **Scope boundaries:**
  - No D_it → D_it_SI conversion.
  - No σ_eff or ρ_eff physical computation.
  - No t_eff physical conversion.
  - No delta_E_window calculation.
  - No solver or script changes.
  - No physical interpretation of φ authorized.
  - Demonstrative mode preserved as default.
- **Option C:** NOT initiated.
- **policy.json:** Unchanged (current_stage v0.4).

