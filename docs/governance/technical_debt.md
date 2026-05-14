# Technical Debt Scorecard — MVP v0.1 / v0.2 / v0.2.1 / v0.3 / v0.3.1–v0.3.9 / v0.4 / v0.4.2 / v0.4.4 / v0.4.5 / v0.4.6 / v0.4.7 / v0.4.8 / v0.4.9 / v0.4.10

> **Last updated:** 2026-05-13

## Summary

| Status | Count |
|--------|-------|
| RESOLVED | 8 |
| PARTIALLY RESOLVED | 1 |
| DEFERRED | 6 |
| OPEN | 0 |
| WONTFIX | 0 |

---

## v0.1 Technical Debts

### TD-01: 2D Case Not Implemented

- **Description:** Caso 2D simplificado não implementado no v0.1.
- **Impact:** Escopo visual limitado a 1D; demonstração menos abrangente.
- **Status:** ✅ RESOLVED in v0.2
- **Decision:** ADR-003 — deferido para v0.2. Implementado como Domain2D + thermal_solver_2d.
- **Evidence:** [ADR-003](../adr/ADR-003-2d-scope-decision.md), [ADR-004](../adr/ADR-004-v0.2-scope-selection.md)

---

### TD-02: Notebooks Not Created

- **Description:** Notebooks Jupyter (.ipynb) não criados no v0.1.
- **Impact:** Visualização interativa não disponível; usuários
  devem usar scripts CLI.
- **Status:** DEFERRED
- **Decision:** Notebooks deferidos para v0.2. Scripts .py
  com `--output-dir` cobrem a funcionalidade básica.
  Ver `notebooks/README.md`.
- **Evidence:** [notebooks/README.md](../../notebooks/README.md)
- **Note v0.2:** Permanece deferido. Classificado como SHOULD na ADR-004.
  Reclassificado como TD-v0.2-02 abaixo.

---

### TD-03: Global Sensitivity Methods

- **Description:** Análise de sensibilidade usa método OAT (one-at-a-time)
  com sensibilidade normalizada demonstrativa.
- **Impact:** Não captura interações entre parâmetros. Ranking depende
  dos ranges e defaults escolhidos.
- **Status:** DEFERRED
- **Decision:** Métodos globais (Sobol, Morris) deferidos para v0.2.
  O método OAT demonstrativo é suficiente para o escopo v0.1.
- **Evidence:** Documentado em `docs/relatorio_30_dias.md`, seção Sensibilidade.
- **Note v0.2:** Permanece deferido. Classificado como COULD na ADR-004.
  Reclassificado como TD-v0.2-03 abaixo.

---

## v0.2 Technical Debts

### TD-v0.2-01: Diffusion 2D Deferred

- **Description:** Solver difusivo 2D (Arrhenius + Neumann no-flux) não
  implementado na v0.2 core.
- **Impact:** Extensão 2D cobre apenas o campo térmico. Acoplamento
  termo-difusivo 2D não demonstrado.
- **Status:** DEFERRED
- **Justificativa:** Classificado como SHOULD condicional na ADR-004.
  Implementação exige todos os MUST gates verdes primeiro.
  `generate_all_results.py` NÃO depende de difusão 2D.
- **Versão-alvo:** v0.2.1 ou v0.3
- **Evidence:** [ADR-004 §SHOULD](../adr/ADR-004-v0.2-scope-selection.md),
  [v0.2 Risk Matrix R-08](v0.2_risk_matrix.md)

---

### TD-v0.2-02: Notebooks/Jupytext Deferred

- **Description:** Notebooks Jupyter/Jupytext demonstrativos não criados na v0.2.
- **Impact:** Usuários interagem apenas via CLI. Demonstração interativa
  não disponível.
- **Status:** ✅ PARTIALLY RESOLVED in v0.2.1
- **Resolution:** `notebooks/v0.2_demo.py` criado como Jupytext percent-format.
  Notebook executa Domain2D, solver térmico 2D e convergência.
  Jupytext como dependência formal não adicionada (script executável diretamente).
- **Residual:** Conversão para .ipynb nativo requer `jupytext --to notebook`.
- **Evidence:** [notebooks/v0.2_demo.py](../../notebooks/v0.2_demo.py)

---

### TD-v0.2-03: Morris/Global Sensitivity Deferred

- **Description:** Análise de sensibilidade global (Morris screening, Sobol)
  não implementada.
- **Impact:** Sensibilidade permanece OAT demonstrativa. Interações entre
  parâmetros não capturadas.
- **Status:** DEFERRED
- **Justificativa:** Classificado como COULD na ADR-004. O método OAT é
  suficiente para o escopo demonstrativo do MVP.
- **Versão-alvo:** v0.3+
- **Evidence:** [ADR-004 §COULD](../adr/ADR-004-v0.2-scope-selection.md)

---

### TD-v0.2-04: Poisson/Eletrostática Out of Scope

- **Description:** Equação de Poisson (eletrostática) não implementada.
  Requer ρ_eff que depende de C_def (defect-like, v0.3).
- **Impact:** Sem eletrostática, o modelo não resolve potencial V(x,y).
  Impossibilita confinamento quântico (Schrödinger).
- **Status:** DEFERRED
- **Justificativa:** Classificado como WON'T na ADR-004. Roadmap ADR-005:
  Poisson = v0.4, Schrödinger = v0.5.
- **Versão-alvo:** v0.4
- **Evidence:** [ADR-004 §WON'T](../adr/ADR-004-v0.2-scope-selection.md),
  [ADR-005](../adr/ADR-005-process-to-device-bridge-roadmap.md)

---

### TD-v0.2-05: Parameters Not Calibrated

- **Description:** Todos os parâmetros do modelo (α, D₀, Eₐ, T_c, σ_T, A_C,
  BCs) são toy/demonstrativos. Nenhum está calibrado com dados experimentais
  ou literatura quantitativa para um material específico.
- **Impact:** Resultados numéricos são qualitativos. Não podem ser citados
  como predições físicas.
- **Status:** DEFERRED
- **Justificativa:** Calibração requer curadoria de dados experimentais
  e validação, fora do escopo do MVP. C permanece proxy adimensional
  (ADR-002, hipótese L-01).
- **Versão-alvo:** v0.5+ ou publicação
- **Evidence:** [parameters.md](../parameters.md),
  [hipoteses_e_limitacoes.md](../hipoteses_e_limitacoes.md),
  [ADR-002](../adr/ADR-002-no-quantum-coherence-prediction.md)

---

## v0.3 Technical Debts

### TD-v0.3-01: Defect Parameter Curation Deferred

- **Description:** v0.3 defect kinetics parameters (D₀, E_D, A_G, T_G, σ_G,
  A_R, E_R) are toy/demonstrative or literature-inspired order-of-magnitude.
  No parameter is calibrated for a specific defect type in silicon.
- **Impact:** C_def dynamics are qualitative. Cannot predict real defect
  concentrations or charge noise.
- **Status:** DEFERRED
- **Justificativa:** Calibration requires curated experimental data and
  targeted literature review per defect species (V, I, O_i, etc.).
- **Versão-alvo:** v0.5+ or publication
- **Evidence:** [parameters_v0.3_candidates.md](../parameters_v0.3_candidates.md),
  [ADR-006](../adr/ADR-006-defect-like-reaction-diffusion-scope.md)

---

### TD-v0.3-02: Poisson Electrostatics Deferred

- **Description:** v0.3 exports C_def_final but does NOT compute ρ_eff or
  solve Poisson (∇·(ε∇φ) = −ρ_eff). The coupling C_def → ρ_eff → φ is
  explicitly deferred to v0.4 per ADR-005/ADR-006.
- **Impact:** No electrostatic potential, no confinement, no device physics.
- **Status:** DEFERRED
- **Versão-alvo:** v0.4
- **Evidence:** [ADR-006 §Acceptance Record](../adr/ADR-006-defect-like-reaction-diffusion-scope.md)

---

### TD-v0.3-03: Solver Performance (Python Loops)

- **Description:** defect_solver_2d uses explicit Python loops for the
  interior update (variable D). A vectorized/Cython/Numba implementation
  would improve performance on fine grids.
- **Impact:** Solver is slow for nx/ny > ~100. Acceptable for demonstrative
  grids (51×51).
- **Status:** DEFERRED
- **Versão-alvo:** v0.4+ if performance becomes blocking

---

### TD-v0.3.1-01: Branch Protection Not Configured

- **Description:** The `main` branch had no protection rules, allowing direct
  pushes and merges without CI validation.
- **Impact:** Risk of unreviewed code reaching SSOT.
- **Status:** ✅ RESOLVED in v0.3.1
- **Resolution:** Branch protection configured via GitHub API. Required checks:
  `quality (3.11)`, `quality (3.12)`. Force push and deletion blocked.
  Repository made public to enable protection on GitHub Free plan.
- **Evidence:** [branch_protection.md](branch_protection.md)

---

### TD-v0.3.3-01: README Not Public-Facing

- **Description:** The README was written for internal development with v0.1
  scope only, missing badges, architecture, limitations, and roadmap.
- **Impact:** Poor first impression for external readers of a public repo.
- **Status:** ✅ RESOLVED in v0.3.3
- **Resolution:** Complete rewrite with CI badge, scientific limitations,
  architecture diagram, roadmap, governance links, and explicit disclaimers.

---

### TD-v0.3.3-02: Local Path Hardcoded in Documentation

- **Description:** `implementation_plan.md` contained a hardcoded local
  workspace path (`/home/...`).
- **Impact:** Unprofessional in a public repository; no security risk.
- **Status:** ✅ RESOLVED in v0.3.3
- **Resolution:** Replaced with generic `<your-workspace>` placeholder.

---

### TD-v0.3.4-01: No LICENSE File

- **Description:** The repository was public without a formal LICENSE file.
  README mentioned MIT informally but no legal text was committed.
- **Impact:** Legal ambiguity for public code.
- **Status:** ✅ RESOLVED in v0.3.4
- **Resolution:** MIT License file added. README badge and CITATION.cff
  updated. Decision brief marked as Accepted.
- **Evidence:** [LICENSE](../../LICENSE), [public_release_metadata.md](../decision_briefs/public_release_metadata.md)

---

### TD-v0.3.5-01: Parameter Curation Absent

- **Description:** MVP parameters lacked formal evidence classification.
  No literature review justified parameter ranges. No machine-readable
  registry existed.
- **Impact:** Risk of overclaim; difficulty tracing parameter provenance.
- **Status:** ✅ RESOLVED in v0.3.5
- **Resolution:** Evidence tier system (T0–TX) defined. 17 parameters
  classified in JSON registry. Directed literature review with 10 sources.
  C_def → ρ_eff mapping options documented.
- **Evidence:** [parameter_registry](../parameter_registry/v0.3.5_parameter_registry.json),
  [literature_review](../literature_review/v0.3.5_parameter_curation.md)

---

### TD-ADR007-01: v0.4 Implementation Pending ADR Acceptance

- **Description:** ADR-007 specifies the v0.4 Poisson bridge scope with
  Option C-B (Boussinesq-inspired closure). Implementation was blocked
  until ADR was promoted to Accepted and policy.json updated.
- **Impact:** No electrostatic coupling until v0.4 is implemented.
- **Status:** ✅ RESOLVED in v0.4
- **Resolution:** ADR-007 accepted (v0.3.7). Policy updated to v0.4 (v0.3.8).
  Implementation plan refined (v0.3.9). TDD RED/GREEN phases completed.
  effective_charge.py, poisson_solver_2d.py, and run_poisson_bridge.py
  implemented with full test coverage.
- **Evidence:** [ADR-007](../adr/ADR-007-v0.4-poisson-bridge-scope.md),
  [implementation_plan](implementation_plan.md)
---

### TD-PARAMS-01: Unit Conversion Infrastructure

- **Description:** The MVP uses demonstrative/dimensionless parameters.
  Literature-supported T2 values (epsilon_r, D_it) exist but cannot be
  used without implementing SI unit conversion throughout the pipeline.
- **Impact:** Cannot promote parameters from demonstrative to calibrated
  without unit infrastructure.
- **Status:** DEFERRED
- **Pre-requisite:** ADR authorizing unit conversion and calibrated mode.
- **Evidence:** [v0.4.1 parameter registry](../parameter_registry/v0.4.1_parameter_registry.json),
  [literature review](../literature_review/v0.4.1_deep_parameter_curation.md)

---

### TD-UNITS-02: SI Unit Conversion Infrastructure Pending ADR-008 Acceptance

- **Description:** The MVP requires a formal SI unit conversion infrastructure
  to transition from demonstrative mode (ε = 1.0, N_ref = 1.0) to
  literature-scaled mode (ε = ε_r · ε₀, physical D_it). ADR-008 proposes
  the scope and criteria for this infrastructure but does not implement it.
- **Impact:** Cannot validate physical scale of outputs (φ, ρ_eff) without
  unit conversion. Risk of false calibration if units are introduced ad-hoc.
- **Status:** DEFERRED
- **Pre-requisite:** ADR-008 must be Accepted. Option B (literature-scaled
  constants only) is the recommended first implementation step.
- **Versão-alvo:** v0.4.3+ (after ADR-008 acceptance)
- **Evidence:** [ADR-008](../adr/ADR-008-v0.4.2-si-units-scale-audit.md),
  [v0.4.2 Decision Brief](../decision_briefs/v0.4.2_units_vs_demonstrative.md),
  [v0.4.2 Council](../research_council/v0.4.2_units_scale_council.md)

---

### TD-UNITS-03: Option C Physical Charge Mapping Deferred

- **Description:** Option B scaffolding (SI constants, scale mode metadata)
  is implemented in v0.4.4. Option C (D_it → σ_eff, σ_eff → ρ_eff, t_eff
  physical use, delta_E_window, charge sign convention) remains deferred
  until a dedicated ADR amendment and TDD implementation PR.
- **Impact:** The model cannot compute physical charge density from
  literature D_it values. φ remains demonstrative or dimensional scaffolding.
- **Status:** DEFERRED
- **Pre-requisite:** Dedicated PR satisfying ADR-008 Acceptance Record
  prerequisites #7–#10 (delta_E_window, t_eff, charge sign, perturbation mode).
- **Versão-alvo:** v0.5+
- **Evidence:** [ADR-008 Acceptance Record](../adr/ADR-008-v0.4.2-si-units-scale-audit.md),
  [v0.4.4 TDD Plan](v0.4.4_si_constants_tdd_plan.md)

---

### TD-METADATA-01: Runtime Scale Metadata Integration

- **Description:** The v0.4.4 modules `units.py` and `scale_modes.py` are
  available at import time but not used by any runtime code. CSV outputs and
  figures do not declare their scale context (demonstrative vs physical).
  Integration as metadata-only (Option B) was evaluated in v0.4.5 and
  recommended for future implementation.
- **Impact:** Artifacts lack self-describing scale metadata. Consumers cannot
  programmatically distinguish demonstrative from physical outputs.
- **Status:** ✅ RESOLVED in v0.4.6
- **Resolution:** Metadata-only declaration implemented via TDD (RED → GREEN).
  `scale_metadata_to_record()` and `attach_scale_metadata_to_metrics()` added
  to `scale_modes.py`. `poisson_bridge_metrics.csv` now includes 7 metadata
  columns. Numeric baseline preserved. physical_interpretation_allowed remains
  False. Future physical charge mapping remains deferred pending new ADR.
- **Evidence:** [v0.4.6 TDD Plan](v0.4.6_runtime_metadata_tdd_plan.md),
  [v0.4.6 Release Notes](../release_notes/v0.4.6_draft.md)

---

### TD-RUNTIME-METADATA-01: Physical Charge Mapping Still Deferred

- **Description:** Metadata-only declaration implemented in v0.4.6.
  Future physical charge mapping (Option C: D_it → σ_eff, charge sign
  convention, delta_E_window, t_eff physical) remains deferred.
- **Impact:** The model cannot compute physical charge density from
  literature D_it values. φ remains demonstrative.
- **Status:** DEFERRED
- **Pre-requisite:** New ADR and TDD plan for Option C.
- **Versão-alvo:** v0.5+
- **Evidence:** [v0.4.5 Decision Brief](../decision_briefs/v0.4.5_runtime_scale_metadata_integration.md)

---

### TD-SKILLS-01: Agent Skills Are Markdown-Only Playbooks

- **Description:** Agent Skills created in v0.4.7 are Markdown-only
  project-scoped playbooks under `.agent/skills/`. They contain no
  executable scripts, no automation hooks, and no deterministic
  validation logic.
- **Impact:** Skills guide the agent but do not enforce rules
  programmatically. Compliance depends on agent following the playbook.
- **Status:** DEFERRED
- **Future evolution:** Deterministic scripts (e.g., pre-commit hooks,
  validation runners) may be added in future releases via dedicated
  PR with acceptance gates and ADR review.
- **Versão-alvo:** v0.5+ (if automation is needed)
- **Evidence:** [v0.4.7 Governance Plan](v0.4.7_agent_skills_governance_plan.md),
  [v0.4.7 Risk Matrix](v0.4.7_agent_skills_risk_matrix.md)

---

### TD-OPTIONC-READINESS-01: Option C Requires ADR-009 Before Implementation

- **Description:** Option C (physical charge mapping: D_it → σ_eff,
  σ_eff → ρ_eff, t_eff regularization, δE_window, charge sign convention,
  ε substitution, physical φ interpretation) requires ADR-009 before any
  code implementation. v0.4.8 readiness review identified 8 of 10 blocking
  gaps and 12 risks (4 Critical).
- **Impact:** Cannot implement Option C without resolving: δE_window
  convention, charge sign convention, t_eff regularization semantics,
  geometry mode (normalized_2d vs physical_2d), ε substitution strategy,
  φ scale sanity checks, solver stability with physical ε, and TDD plan.
- **Status:** DEFERRED
- **Pre-requisite:** ADR-009 Proposed → Council → Accepted → TDD RED.
- **Versão-alvo:** v0.5+ (after ADR-009 acceptance)
- **Evidence:** [v0.4.8 Decision Brief](../decision_briefs/v0.4.8_option_c_readiness_review.md),
  [v0.4.8 Council](../research_council/v0.4.8_option_c_readiness_council.md),
  [v0.4.8 Risk Matrix](v0.4.8_option_c_readiness_risk_matrix.md)

---

### TD-ADR009-C1-01: C1 Surface-Density Bookkeeping Proposed but Not Implemented

- **Description:** ADR-009 proposes C1 (D_it → D_it_SI → N_it → σ_eff)
  as next physics step. Unresolved decisions: δE_window convention, charge
  sign convention, occupancy convention, and explicit no-ρ_eff boundary.
- **Impact:** Cannot advance to physical charge mapping until C1 is
  implemented with TDD RED→GREEN after ADR-009 acceptance.
- **Status:** DEFERRED
- **Pre-requisite:** ADR-009 Accepted → TDD RED → GREEN.
- **Versão-alvo:** v0.5.0 (C1 implementation)
- **Evidence:** [ADR-009](../adr/ADR-009-option-c-surface-density-bookkeeping-scope.md),
  [v0.4.9 TDD Plan](v0.4.9_adr009_future_tdd_plan.md)

---

### TD-C1-RED-01: ADR-009 Accepted but C1 Not Yet Implemented

- **Description:** ADR-009 accepted for C1 surface-density bookkeeping.
  Implementation requires RED tests before code: D_it conversion,
  δE_window explicitness, sign convention, occupancy bounds, N_it,
  σ_eff, no ρ_eff, no solver coupling, metadata blocks physical φ.
- **Impact:** C1 cannot produce dimensional charge bookkeeping until
  v0.5.0 RED→GREEN cycle is completed.
- **Status:** ✅ RESOLVED in v0.5.0
- **Resolution:** C1 implemented in `surface_charge.py` with 15 tests.
  TDD RED→GREEN 1→GREEN 2→GREEN 2.1→GREEN 3 cycle completed.
  Policy stage promoted to v0.5.
- **Evidence:** [ADR-009 Accepted](../adr/ADR-009-option-c-surface-density-bookkeeping-scope.md),
  [v0.5.0 TDD Plan](v0.5.0_c1_surface_charge_tdd_plan.md),
  [v0.5.0 Policy Activation](v0.5.0_c1_policy_activation.md)

---

### TD-C1-C2-BOUNDARY-01: C2 Blocked Until Future ADR

- **Description:** C1 is implemented as surface-density bookkeeping only.
  C2 remains blocked until a future ADR defines ρ_eff, t_eff regularization,
  geometry mode, epsilon mode, and solver-coupling tests.
- **Impact:** Cannot compute volume charge density or couple to solver.
- **Status:** DEFERRED
- **Pre-requisite:** New ADR extending ADR-009 for C2 scope.
- **Versão-alvo:** v0.6+
- **Evidence:** [ADR-009](../adr/ADR-009-option-c-surface-density-bookkeeping-scope.md)

---

### TD-C1-VALIDATION-01: C1 Lacks Experimental Validation

- **Description:** C1 validates dimensional bookkeeping (unit conversion,
  sign convention, occupancy bounds) but does not validate experimental
  device behavior. Future work requires benchmark or analytic sanity
  checks before physical interpretation.
- **Impact:** σ_eff values are dimensionally correct but not calibrated.
- **Status:** DEFERRED
- **Pre-requisite:** Experimental D_it data or manufactured solution.
- **Versão-alvo:** v0.6+
- **Evidence:** [v0.5.0 TDD Plan](v0.5.0_c1_surface_charge_tdd_plan.md)

---

### TD-C1-DEMO-01: C1 Validation is Numerical Only

- **Description:** C1 demonstration artifacts validate monotonicity, sign
  symmetry, and metadata boundaries but do not validate device behavior
  or experimental calibration.
- **Impact:** C1 provides a dimensionally consistent framework but remains
  a demonstrative module until physics-based regularization (C2) and
  experimental validation.
- **Status:** DEFERRED
- **Pre-requisite:** C2 and experimental data.
- **Versão-alvo:** v0.6+
- **Evidence:** [v0.5.1 C1 Validation Scale Brief](../decision_briefs/v0.5.1_c1_validation_scale_brief.md)
