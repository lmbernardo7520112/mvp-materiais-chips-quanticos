# Task Tracker — mvp-materiais-chips-quanticos v0.1-r2

> **Last updated:** 2026-05-06  
> **Status:** EXECUTING — Phases 1-6  
> **Revision:** r2-final — 12 corrections + 5 adjustments

---

## Phase 1: Scaffolding (Commits 1-3)

- `[ ]` Create repo dir and `git init`
- `[ ]` Create `.gitignore` (includes `results/figures/*`, `results/tables/*`, `results/runs/*` with `.gitkeep`), `requirements.txt`, `pyproject.toml` (`>=3.11,<3.13`)
- `[ ]` Create directory structure (src/, tests/, scripts/, docs/, results/, notebooks/)
- `[ ]` Create `src/mvp_quantum_materials/__init__.py`
- `[ ]` Create `notebooks/README.md` (stub: notebooks deferred to v0.2)
- `[ ]` **Commit 1:** `chore: initialize repository structure`
- `[ ]` Create `docs/governance/implementation_plan.md`
- `[ ]` Create `docs/governance/task.md`
- `[ ]` **Commit 2:** `docs: add SDD implementation plan and governance tracker`
- `[ ]` Create `README.md` (institutional, C = proxy adimensional documented)
- `[ ]` Create `docs/referencias.md` (≥14 refs)
- `[ ]` Create `docs/hipoteses_e_limitacoes.md` (C = proxy, limites científicos)
- `[ ]` Create `docs/plano_tecnico_mvp.md`
- `[ ]` Create `docs/parameters.md` (tabela: param|símbolo|unidade|default|natureza|justificativa)
- `[ ]` **Commit 3:** `docs: add institutional README, references and parameters`

---

## Phase 2: Core TDD (Commits 4-7)

- `[ ]` Create `tests/test_domain.py` (T-01)
- `[ ]` Create `tests/test_thermal_solver.py` (T-02, T-03, T-04, **T-15: stability rejection**)
- `[ ]` **Commit 4:** `test: add domain and thermal solver specifications`
- `[ ]` Implement `config.py` (dataclasses, constants, stability functions)
- `[ ]` Implement `domain.py` (Domain1D)
- `[ ]` Implement `thermal_solver.py` (Dirichlet BC, **stability guard**)
- `[ ]` Verify: pytest passes for domain + thermal
- `[ ]` **Commit 5:** `feat: implement 1d domain and thermal solver`
- `[ ]` Create `tests/test_diffusion_solver.py` (T-05, T-06, T-07, **T-13, T-14, T-16, T-17**)
- `[ ]` **Commit 6:** `test: add diffusion, arrhenius and source specifications`
- `[ ]` Implement `diffusion_solver.py` (Neumann no-flux BC, Arrhenius, S_C, **stability guard**)
- `[ ]` Verify: pytest passes for all tests so far
- `[ ]` **Commit 7:** `feat: implement diffusion model with stability guard`

---

## Phase 3: Metrics & Sensitivity (Commit 8)

- `[ ]` Create `tests/test_metrics.py` (T-08, T-09)
- `[ ]` Create `tests/test_sensitivity.py` (T-10)
- `[ ]` Implement `metrics.py`
- `[ ]` Implement `sensitivity.py`
- `[ ]` Implement `plots.py`
- `[ ]` Verify: pytest passes
- `[ ]` **Commit 8:** `feat: add metrics and sensitivity analysis`

---

## Phase 4: Scripts & Results (Commit 9)

- `[ ]` Create `scripts/run_thermal_1d.py`
- `[ ]` Create `scripts/run_diffusion_1d.py`
- `[ ]` Create `scripts/run_sensitivity.py`
- `[ ]` Create `scripts/generate_all_results.py` (**with `--output-dir`**)
- `[ ]` Create `tests/test_scripts.py` (T-11, T-12 — **uses `tmp_path`**)
- `[ ]` Execute `generate_all_results.py` and verify ≥3 figures
- `[ ]` Verify: pytest passes (≥17 tests), working tree clean
- `[ ]` **Commit 9:** `feat: add CLI scripts with --output-dir`

---

## Phase 5: Governance & Quality (Commits 10-11)

- `[ ]` Create `docs/adr/ADR-001-python-numpy-first.md`
- `[ ]` Create `docs/adr/ADR-002-no-quantum-coherence-prediction.md`
- `[ ]` Create `docs/adr/ADR-003-2d-scope-decision.md` (**2D = stretch/deferred**)
- `[ ]` Create `docs/governance/technical_debt.md`
- `[ ]` **Commit 10:** `docs: add ADRs and technical debt scorecard`
- `[ ]` Create `.github/workflows/ci.yml` locally (**matrix 3.11+3.12, ruff, artifacts**) — remote validation blocked until push authorized
- `[ ]` Create `.github/PULL_REQUEST_TEMPLATE.md`
- `[ ]` Verify: `ruff check . && ruff format --check .` passes
- `[ ]` **Commit 11:** `ci: add GitHub Actions with ruff and matrix`

---

## Phase 6: Audit & Local Release (Commit 12)

- `[ ]` Create `docs/governance/walkthrough.md` (local evidence: pytest, ruff, scripts, figures, commits, working tree, ci.yml). Adendo CI remoto após push.
- `[ ]` Create `docs/governance/project_audit.md`
- `[ ]` Create `docs/relatorio_30_dias.md` (C = proxy documented)
- `[ ]` **Commit 12:** `docs: add walkthrough and project audit for v0.1`

---

## Phase 7: Stretch Goal — 2D (Condicional)

- `[ ]` Verify ALL gates 1-19 are green
- `[ ]` If green: implement 2D simplificado + tests + commit
- `[ ]` If any gate fails: update ADR-003 → DEFERRED v0.2

---

## Phase 8: Remote Push (Requer Autorização)

- `[ ]` Request user authorization for remote push
- `[ ]` `gh repo create` or push to existing remote
- `[ ]` Verify CI green (Gate 22)

---

## Verification Gates

### Gates 1-19: Local (obrigatórios)

- `[ ]` G-01: pytest passes
- `[ ]` G-02: ruff check + format passes
- `[ ]` G-03: ≥17 tests exist
- `[ ]` G-04: ≥3 figures generated
- `[ ]` G-05: Scripts execute with --output-dir
- `[ ]` G-06: README complete (C = proxy)
- `[ ]` G-07: docs/referencias.md exists
- `[ ]` G-08: docs/hipoteses_e_limitacoes.md exists
- `[ ]` G-09: docs/parameters.md exists
- `[ ]` G-10: All 5 governance docs exist
- `[ ]` G-11: ≥3 ADRs exist
- `[ ]` G-12: PR template exists
- `[ ]` G-13: Commits atomic and semantic
- `[ ]` G-14: Working tree clean
- `[ ]` G-15: No exaggerated scientific claims
- `[ ]` G-16: Limitations documented
- `[ ]` G-17: Report with evidence
- `[ ]` G-18: Solvers reject unstable dt
- `[ ]` G-19: C remains finite in all simulations

### Gates 20-21: Stretch

- `[ ]` G-20: All gates 1-19 green → 2D eligible
- `[ ]` G-21: 2D implemented OR deferred via ADR-003

### Gate 22: Release

- `[ ]` G-22: CI GitHub Actions green (after authorized push)
