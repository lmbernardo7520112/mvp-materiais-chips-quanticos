# Project Audit — MVP v0.1 / v0.2 / v0.3 / v0.3.1–v0.3.9 / v0.4 / v0.4.5 / v0.4.6 / v0.4.7 / v0.4.8 / v0.4.9 / v0.4.10 / v0.5.0

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

## v0.4.5 — Runtime Scale Metadata Integration Review

> **Date:** 2026-05-12
> **Status:** DOCUMENTATION-ONLY

- **Type:** Integration review and architectural decision.
- **Branch:** `docs/v0.4.5-runtime-scale-metadata-review`.
- **Decision:** Option B (metadata-only runtime declaration) recommended for future v0.4.6. Option C prohibited.
- **v0.4.4 audit finding:** Release report had test counts swapped (listed 17/14, actual 12/19). Total 31 correct. Correction issued.
- **Documents created:**
  - Decision brief comparing Options A/B/C.
  - Research council (5 experts, unanimous Option B).
  - Acceptance gates (9 gates).
  - Risk matrix (8 risks, 3 Critical).
  - Release notes draft.
  - v0.4.4 test count correction.
- **Scope boundaries:**
  - Zero src/ changes.
  - Zero scripts/ changes.
  - Zero tests/ changes.
  - No solver modifications.
  - No Option C implementation.
  - policy.json unchanged (current_stage v0.4).

## v0.4.6 — Runtime Metadata-Only Declaration

> **Date:** 2026-05-13
> **Status:** IMPLEMENTED

- **Type:** Metadata-only runtime integration (Option B).
- **Branch:** `feature/v0.4.6-runtime-scale-metadata-red`.
- **TDD sequence:** RED → GREEN 1 → GREEN 2 → GREEN 3.
- **Helpers added:**
  - `scale_metadata_to_record()` — serialize ScaleMetadata to flat dict.
  - `attach_scale_metadata_to_metrics()` — merge metadata without mutation.
- **CSV integration:** `poisson_bridge_metrics.csv` now includes 7 metadata columns.
- **Numeric baseline preserved:** string-identical values before and after.
- **Tests added:** 12 (7 serialization + 5 integration).
- **Total tests:** 179.
- **Coverage:** 90.86%.
- **No equation change.**
- **No solver change.**
- **No Option C.**
- **policy.json:** Unchanged (current_stage v0.4).

## v0.4.7 — Governance Infrastructure

> **Date:** 2026-05-13
> **Status:** INFRASTRUCTURE

- **Type:** Agent Skills Governance Bootstrap.
- **Branch:** `docs/v0.4.7-agent-skills-governance-bootstrap`.
- **Skills added:** 6 project-scoped Antigravity Agent Skills under `.agent/skills/`.
  - ai-rse-gateops — operational governance.
  - tdd-red-green-release — TDD cycle discipline.
  - physics-dimensional-audit — dimensional consistency.
  - scope-guardrails — scientific boundary protection.
  - release-manager — merge/tag/release sequence.
  - report-auditor — self-audit and verification.
- **Documents added:** governance plan, acceptance gates (16), risk matrix (10 risks).
- **No src/ changes.**
- **No scripts/ changes.**
- **No tests/ changes.**
- **No policy.json changes.**
- **No pyproject.toml changes.**
- **No physics change.**
- **No Option C.**
- **No external skills installed.**
- **No executable scripts in skills.**

## v0.4.8 — Skills-Governed Option C Readiness Review

> **Date:** 2026-05-13
> **Status:** DOCUMENTATION-ONLY

- **Type:** Skills-governed readiness review for Option C.
- **Branch:** `docs/v0.4.8-skills-governed-option-c-readiness`.
- **Skills used:** All 6 Agent Skills loaded and referenced.
- **Decision brief:** 10 readiness questions, 8 blocking.
- **Council:** 6 experts, 0/6 for implementation, 6/6 for ADR-009.
- **Acceptance gates:** 22 gates.
- **Risk matrix:** 12 risks (4 Critical, 5 High, 1 Medium/High).
- **Option C verdict:** NOT ready for implementation. Ready for ADR-009 Proposed.
- **No src/ changes.**
- **No scripts/ changes.**
- **No tests/ changes.**
- **No policy.json changes.**
- **No skills altered.**
- **No Option C implementation.**
- **Next step:** ADR-009 Proposed.

## v0.4.9 — Physics-first ADR-009 Proposed

> **Date:** 2026-05-13
> **Status:** DOCUMENTATION-ONLY / PHYSICS-FIRST

- **Type:** ADR-009 Proposed — C1 surface-density bookkeeping scope.
- **Branch:** `docs/v0.4.9-adr-009-physics-first-option-c-scope`.
- **Methodology audit:** AI-RSE GateOps, maturity 4.5/5, score 8.0/10.
- **Scientific decision:** C1 recommended (6/6), C2/C3 blocked.
- **Council dissent:** Skeptical Reviewer raised 3 objections, all answered.
- **Future TDD plan:** 8 RED tests specified (not created).
- **Benchmark requirement:** Manufactured solution with physical ε before C2.
- **No src/ changes.**
- **No scripts/ changes.**
- **No tests/ changes.**
- **No policy.json changes.**
- **No skills altered.**
- **No Option C implementation.**
- **Next step:** ADR-009 review/acceptance, then C1 TDD RED.

## v0.4.10 — ADR-009 Accepted

> **Date:** 2026-05-13
> **Status:** DOCUMENTATION-ONLY / ADR ACCEPTANCE

- **Type:** ADR-009 promoted from Proposed → Accepted.
- **Branch:** `docs/v0.4.10-accept-adr-009-c1-scope`.
- **Council:** 6/6 Accept (2 objections answered).
- **Acceptance review:** 14/14 criteria satisfied.
- **C1 authorized:** future RED phase only.
- **No src/ changes.**
- **No scripts/ changes.**
- **No tests/ changes.**
- **No policy.json changes.**
- **No skills altered.**
- **No Option C implementation.**
- **Next step:** v0.5.0 RED for C1 surface-density bookkeeping.

## v0.5.0 — C1 Surface-Density Bookkeeping

> **Date:** 2026-05-14
> **Status:** IMPLEMENTED — first physics code since v0.4.6

- **Type:** C1 surface-density bookkeeping (ADR-009 Accepted).
- **Branch:** `feature/v0.5.0-c1-surface-density-bookkeeping`.
- **TDD sequence:** RED → GREEN 1 → GREEN 2 → GREEN 2.1 → GREEN 3.
- **Module added:** `src/mvp_quantum_materials/surface_charge.py`.
- **API:** `convert_dit_ev_cm2_to_j_m2`, `compute_nit_areal_density`,
  `compute_sigma_eff`, `compute_c1_surface_charge`.
- **Chain:** D_it → D_it_SI → N_it → σ_eff.
- **Tests added:** 15 (in `test_surface_charge.py`).
- **Policy stage:** v0.4 → **v0.5** (`current_stage` updated).
- **ρ_eff:** not implemented.
- **t_eff:** not implemented.
- **Solver:** untouched.
- **Scripts:** untouched.
- **Skills:** unchanged.
- **pyproject.toml:** unchanged.

## v0.5.1 — C1 Validation & Demonstration Hardening

> **Date:** 2026-05-14
> **Status:** IMPLEMENTED

- **Type:** C1 Validation.
- **Branch:** `feature/v0.5.1-c1-validation-demo-hardening`.
- **Script added:** `scripts/run_c1_surface_charge_demo.py`.
- **Tests added:** `tests/test_c1_surface_charge_demo.py`.
- **Artifacts:** `c1_surface_charge_demo.csv` (72 rows), `c1_sigma_eff_sensitivity.png`.
- **Integrated:** Added to `generate_all_results.py`.
- **Policy:** Activated for new files.
- **ρ_eff:** not implemented.
- **t_eff:** not implemented.
- **Solver:** untouched.

## v0.5.2 — C1 Literature Scale Benchmark

> **Date:** 2026-05-14
> **Status:** IMPLEMENTED

- **Type:** C1 Literature Benchmark.
- **Branch:** `feature/v0.5.2-c1-literature-scale-benchmark`.
- **Literature review:** `v0.5.2_c1_literature_scale_benchmark.md`.
- **Decision brief:** `v0.5.2_c1_scale_positioning_brief.md`.
- **Script added:** `scripts/run_c1_literature_scale_benchmark.py`.
- **Tests added:** `tests/test_c1_literature_scale_benchmark.py` (8 tests).
- **Artifacts:** `c1_literature_scale_benchmark.csv` (11 rows), `c1_literature_scale_positioning.png`.
- **Scale classes:** literature_plausible_low, nominal, high, aggressive_upper_bound.
- **Integrated:** Added to `generate_all_results.py`.
- **ρ_eff:** not implemented.
- **t_eff:** not implemented.
- **Solver:** untouched.
- **Calibration claims:** NONE.

## v0.5.3 — C1 Energy-Distribution Upgrade Proposal

> **Date:** 2026-05-14
> **Status:** PROPOSED (documentation-only)

- **Type:** Physics upgrade proposal.
- **Branch:** `docs/v0.5.3-c1-energy-distribution-upgrade-proposal`.
- **ADR-010:** Proposed — C1 energy-distribution scope.
- **Profiles compared:** P0 constant, P1 piecewise, P2 gaussian, P3 triangular.
- **Recommendation:** P1 piecewise-constant.
- **Council:** 6 specialists, unanimous P1 vote.
- **Future TDD plan:** 10 tests specified, not created.
- **Risk matrix:** 8 risks (R1–R8).
- **Acceptance gates:** 19 gates (G1–G19).
- **Code changes:** NONE.
- **ρ_eff:** not implemented.
- **t_eff:** not implemented.
- **Solver:** untouched.
- **Calibration claims:** NONE.

## v0.5.4 — Experimental-Anchored Energy Profile Feasibility

> **Date:** 2026-05-14
> **Status:** PROPOSED (documentation-only)

- **Type:** Feasibility review.
- **Branch:** `docs/v0.5.4-experimental-anchored-energy-profile-feasibility`.
- **Evidence taxonomy:** E0–E4 levels defined.
- **Techniques reviewed:** 6 (charge pumping, C-V, DLTS, DCIV, noise, STM).
- **Decision options:** A (demonstrative), B (literature-informed), C (experimental prior), D (same-stack).
- **Recommendation:** Option B default, Option C conditional.
- **Council:** 7 specialists, unanimous Option B.
- **Risk matrix:** 10 risks (6 Critical).
- **Acceptance gates:** 23 gates.
- **ADR-010:** remains Proposed.
- **Code changes:** NONE.
- **ρ_eff:** not implemented.
- **t_eff:** not implemented.
- **Solver:** untouched.
- **Calibration claims:** NONE.

## v0.5.5 — ADR-010 Accepted: C1 Energy-Distribution Scope

> **Date:** 2026-05-15
> **Status:** ACCEPTED (documentation-only)

- **Type:** ADR acceptance review.
- **Branch:** `docs/v0.5.5-accept-adr-010-energy-distribution`.
- **ADR-010:** promoted from Proposed to **Accepted**.
- **Acceptance criteria:** 15/15 PASS.
- **Council:** 7 specialists, 7/7 Accept.
- **Skeptical objections:** 3 raised and addressed.
- **Option B:** literature-informed default.
- **Option C:** conditional (E2 metadata only).
- **E3/E4:** blocked.
- **Acceptance gates:** 22 gates.
- **Code changes:** NONE.
- **ρ_eff:** not implemented.
- **t_eff:** not implemented.
- **Solver:** untouched.
- **Calibration claims:** NONE.

## v0.5.6 — ADR-010 Hardening: No Demonstrative Evidence Profiles

> **Date:** 2026-05-15
> **Status:** AMENDMENT (documentation-only)

- **Type:** ADR-010 evidence policy hardening.
- **Branch:** `docs/v0.5.6-adr010-no-demonstrative-evidence-profiles`.
- **ADR-010:** Accepted + Amendment v0.5.6.
- **E0 operational:** deprecated.
- **S0 TEST_ONLY:** introduced for test fixtures only.
- **E1:** minimum operational evidence level.
- **E2:** conditional with metadata.
- **E3/E4:** blocked.
- **Council:** 7 specialists, 7/7 Accept, 3 skeptical objections.
- **Code changes:** NONE.
- **ρ_eff:** not implemented.
- **t_eff:** not implemented.
- **Solver:** untouched.
- **Calibration claims:** NONE.

## v0.6.0 — C1 Piecewise D_it(E) Energy Profiles

> **Date:** 2026-05-15
> **Status:** IMPLEMENTATION (TDD RED → GREEN)

- **Type:** C1 energy-distribution bookkeeping.
- **Branch:** `feature/v0.6.0-piecewise-dit-energy-red`.
- **Module:** `src/mvp_quantum_materials/energy_profiles.py`.
- **API:** `EnergyInterval`, `PiecewiseDitProfile`, `integrate_piecewise_dit`,
  `compute_sigma_eff_from_energy_profile`.
- **Physics:** N_it = Σ D_i × ΔE_i; σ_eff = s_charge × q_e × N_it × f_occ.
- **RED tests:** 13 created (all failed with ModuleNotFoundError).
- **GREEN tests:** 13/13 PASSED.
- **Full pytest:** 226 passed.
- **Coverage:** 88.18%.
- **Evidence policy:** S0 test-only, E0 deprecated, E1 min, E2 conditional, E3/E4 blocked.
- **Policy activation:** Documented separately.
- **ρ_eff:** not implemented.
- **t_eff:** not implemented.
- **Solver:** untouched.
- **Calibration claims:** NONE.

## v0.6.1 — Process-to-Device Roadmap Re-Anchoring

> **Date:** 2026-05-19
> **Status:** DOCUMENTATION-ONLY

- **Type:** Strategic roadmap re-anchoring.
- **Branch:** `docs/v0.6.1-process-to-device-roadmap-reanchoring`.
- **ADR-011:** Proposed — process-to-device qubit demonstrator roadmap.
- **Mission:** Process-to-device demonstrator for Si/CMOS qubits.
- **Council:** 8/8 unanimous — Option C (layer-by-layer).
- **Roadmap:** v0.6.1→v1.0 (7 releases, 7 layers).
- **Risks:** 10 identified (6 Critical).
- **Zero src/scripts/tests changes.**
- **ρ_eff:** blocked until ADR-C2.
- **t_eff:** blocked until ADR-C2.
- **Solver coupling:** blocked until v0.8.0.
- **Schrödinger:** blocked until v0.9.0.
- **Calibration claims:** NONE.
- **Coherence claims:** NONE.

## v0.6.2 — Curated E1/E2 D_it(E) Profile Library

> **Date:** 2026-05-20

- **Type:** Feature — curated profile library.
- **Branch:** `feature/v0.6.2-curated-dit-profile-library`.
- **Module:** `dit_profile_library.py`.
- **Profiles:** 3 E1 Si/SiO₂ (nominal, high, low) + E2 factory.
- **Tests:** 20 in `test_dit_profile_library.py`.
- **Full pytest:** 246 passed.
- **Coverage:** 87.37%.
- **Quality gates:** 6/6 PASS.
- **ruff:** PASS.
- **pyright:** 0 errors.
- **generate_all_results:** PASS.
- **Evidence policy:** E1 minimum, E2 with metadata, E0 rejected, E3/E4 blocked.
- **calibration_status:** not_calibrated (all profiles).
- **ρ_eff:** blocked until ADR-C2.
- **t_eff:** blocked until ADR-C2.
- **Solver coupling:** blocked.
- **Calibration claims:** NONE.
- **Coherence claims:** NONE.

## v0.7.0 — ADR-C2 Interface Sheet Source vs Volume Regularization

> **Date:** 2026-05-23

- **Type:** Documentation-only — ADR-C2 decision proposal.
- **Branch:** `docs/v0.7.0-adr-c2-interface-source-regularization`.
- **ADR-012:** Proposed (not yet accepted).
- **Decision:** C2-A primary, C2-B fallback, C2-C conditional, C2-D rejected, C2-E blocked.
- **Code changes:** NONE.
- **Test changes:** NONE.
- **Script changes:** NONE.
- **policy.json:** unchanged.
- **pyproject.toml:** unchanged.
- **ρ_eff:** blocked.
- **t_eff:** rejected (C2-D).
- **l_reg:** documented as numerical regularization only, not implemented.
- **Solver coupling:** blocked.
- **Calibration claims:** NONE.
- **Coherence claims:** NONE.

## v0.7.1 — ADR-012 Acceptance Review

> **Date:** 2026-05-24

- **Type:** Documentation-only — ADR-012 acceptance review.
- **Branch:** `docs/v0.7.1-accept-adr-012-c2-interface-source`.
- **ADR-012:** Promoted from Proposed to **Accepted**.
- **Acceptance criteria:** 18/18 satisfied.
- **Council vote:** 9/9 Accept.
- **Skeptical objections:** 5 raised, 5 addressed.
- **Decision confirmed:** C2-A primary, C2-B fallback, C2-C conditional, C2-D rejected, C2-E blocked.
- **Code changes:** NONE.
- **Test changes:** NONE.
- **Script changes:** NONE.
- **policy.json:** unchanged.
- **pyproject.toml:** unchanged.
- **ρ_eff:** not implemented.
- **t_eff:** rejected (C2-D).
- **l_reg:** not implemented.
- **Solver coupling:** blocked.
- **Calibration claims:** NONE.
- **Coherence claims:** NONE.
- **Next step:** v0.7.2 — C2 RED (earliest implementation phase).

---

## v0.7.3 C2 GREEN Validation

> **Date:** 2026-05-24
> **Type:** Feature implementation (RED/GREEN).

- **Implementation:** `c2_charge_mapping.py`
- **Core Entities:** `InterfaceSheetSource`, `ConservativeVolumeRegularization`, `DepthPriorMetadata`
- **Tests:** 20/20 C2 tests passing.
- **Coverage:** >= 70%.
- **Solver Constraints:** `poisson_solver_2d` blocked. Quantum solvers blocked.
- **Calibration Status:** Forced `not_calibrated`.

---

## v0.7.4 C2 Charge Mapping Demo & Sanity Checks

> **Date:** 2026-05-25
> **Type:** Demonstration and sanity validation.

- **Script:** `scripts/run_c2_charge_mapping_demo.py`
- **Tests:** 15/15 demo tests passing.
- **Scenarios:** 9 (3 sigma × 3 l_reg).
- **Charge conservation:** relative error ≤ 1e-12.
- **l_reg sensitivity:** rho ∝ 1/l_reg confirmed.
- **Solver constraints:** No solver import. No physical phi. No calibration.
- **Total tests:** 281 passed.
- **Coverage:** 88%.

---

## v0.7.5 AI-RSE Methodology Acceleration Skills Bootstrap

> **Date:** 2026-06-12
> **Type:** Documentation/skills-only.

- **Skills added:** 6 (release-acceleration-lanes, minimal-red-contract, dependency-governance, evidence-metrics-refresh, ai-failure-mode-review, human-decision-log).
- **Templates added:** 7 reusable templates in `docs/templates/`.
- **Governance docs added:** release methodology checklist, human decision log (6 entries).
- **Zero code changes.** Zero test changes. Zero script changes.
- **No solver coupling.** No physical phi. No calibration. No dependency added.

---

## v0.7.6 AI-for-Science Parallel Track Governance & Feasibility

> **Date:** 2026-06-12
> **Type:** Documentation-only.

- **ADR-014:** Proposed. AI-for-Science Parallel Track Governance.
- **Classical track:** Canonical. Unchanged.
- **AI track:** Exploratory, documentation-only. No code. No dependency.
- **Council:** 10 specialists, unanimous approval.
- **Risk matrix:** 12 risks, 7 Critical.
- **Future RED plan:** 20 candidate tests.
- **Separation architecture:** Defined.
- **HDL-007:** Recorded.
- **Zero code changes.** Zero test changes. Zero script changes.
- **No ML dependencies.** No ML imports. No solver replacement. No physical claims.

## v0.8.0 C3 Solver Coupling Strategy

> **Date:** 2026-06-12
> **Type:** Documentation-only.

- **ADR-013:** Proposed. C3 Solver Coupling Strategy.
- **C3-A:** Primary future path (Conservative grid projection).
- **C3-B/C:** Future/Conditional paths.
- **C3-D/E/F:** Blocked paths.
- **Council:** 10 specialists, unanimous approval.
- **Risk matrix:** 12 risks, 7 Critical.
- **Future RED plan:** 20 candidate tests.
- **HDL-008:** Recorded.
- **Zero code changes.** Zero test changes. Zero script changes.
- **No solver coupling.** No physical phi. No AI-for-Science runtime.

## v0.8.1 ADR-013 Acceptance Review

> **Date:** 2026-06-12
> **Type:** Documentation-only.

- **Acceptance Review:** Created and evaluated 30 criteria.
- **Council:** Formed and concluded with Accept.
- **ADR-013:** Accepted.
- **No implementation:** True.
- **No RED:** True.
- **No solver runtime:** True.
- **No physical phi:** True.

## AIFS-001 Analytic Benchmark Design

* AIFS-001 documentation-only benchmark design iniciado.
* Não interfere com v0.8.2 C3 RED.
* Não adiciona dependências.
* Não cria PINN.
* Não cria surrogate.
* Não toca C1/C2/C3.
* Classical Track permanece canônica.

## v0.8.2 C3 RED

* v0.8.2 C3 RED iniciado.
* ADR-013 Accepted em v0.8.1.
* Testes RED criados.
* Módulo c3_solver_projection.py ausente.
* RED executado.
* Falhas esperadas por ModuleNotFoundError / ImportError.
* Sem implementação.
* Sem solver coupling.
* Sem Poisson runtime.
* Sem physical phi.
* Sem AI-for-Science runtime.
* Audit após AIFS-001: branch atualizada, RED focal reexecutado com falhas esperadas, c3_solver_projection.py continua ausente.
\n- v0.8.4: C3 Demo Sanity checks integrated with generate_all_results.py. No solver or physical claims added.

## v0.8.5 One-way Poisson Coupling Strategy (Documentation Only)

* ADR-016 Proposed: One-way Demonstrative Coupling.
* No implementation or code changes authorized.
* No self-consistent loops allowed.
* Preserves C3 isolation.
* Classical Track advances without AI/ML.
