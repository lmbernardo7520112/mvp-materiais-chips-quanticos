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

---

### TD-C1-LIT-BENCH-01: Literature Benchmark Does Not Replace Experimental Validation

- **Description:** Literature-scale benchmark contextualizes σ_eff against
  plausible D_it ranges but does not validate device behavior. Future work
  still requires experimental or high-fidelity simulation comparison.
- **Impact:** Benchmark provides order-of-magnitude confidence but cannot
  be cited as calibration evidence.
- **Status:** DEFERRED
- **Pre-requisite:** Experimental D_it data or device-level measurement.
- **Versão-alvo:** v0.6+
- **Evidence:** [v0.5.2 Literature Review](../literature_review/v0.5.2_c1_literature_scale_benchmark.md)

---

### TD-C1-ENERGY-DIST-01: Constant D_it Approximation

- **Description:** C1 currently uses N_it = D_it × ΔE_window, which assumes
  constant D_it across the energy window. ADR-010 proposes D_it(E) integration
  via piecewise-constant profiles, but implementation remains blocked until
  future RED tests and ADR acceptance.
- **Impact:** The constant approximation is dimensionally correct but does
  not capture energy-dependent trap distributions observed in real interfaces.
- **Status:** PROPOSED (ADR-010)
- **Pre-requisite:** ADR-010 acceptance + dedicated TDD cycle.
- **Versão-alvo:** v0.6+
- **Evidence:** [ADR-010](../adr/ADR-010-c1-energy-distribution-scope.md)

---

### TD-C1-EXPERIMENTAL-ANCHORING-01: Evidence-Level Labels Required

- **Description:** Future P1 D_it(E) implementation should label all profiles
  by evidence level (E0/E1/E2). E3/E4 calibration-grade evidence requires a
  separate ADR and is not authorized in the current roadmap.
- **Impact:** Without evidence labels, literature-informed bins could be
  mistaken for calibrated parameters.
- **Status:** PROPOSED (v0.5.4 feasibility review)
- **Pre-requisite:** ADR-010 acceptance + evidence taxonomy integration.
- **Versão-alvo:** v0.6+
- **Evidence:** [v0.5.4 Evidence Taxonomy](v0.5.4_energy_profile_evidence_taxonomy.md)

---

### TD-C1-ENERGY-RED-01: RED Tests Required Before Implementation

- **Description:** ADR-010 accepted. Future P1 piecewise D_it(E) implementation
  requires RED tests before any code. C1 must remain without ρ_eff, t_eff,
  solver coupling, C2/C3, or calibration claims.
- **Impact:** Without RED-first discipline, implementation could bypass the
  physics and governance guardrails established in v0.5.0–v0.5.5.
- **Status:** ACCEPTED (ADR-010 accepted in v0.5.5)
- **Pre-requisite:** v0.6.0 RED phase with all 10 future tests from v0.5.3.
- **Versão-alvo:** v0.6.0
- **Evidence:** [ADR-010 Acceptance Note](../adr/ADR-010-c1-energy-distribution-scope.md)

---

### TD-C1-EVIDENCE-MINIMUM-01: E1 Minimum for Operational Profiles

- **Description:** ADR-010 hardened (v0.5.6). Future operational D_it(E)
  profiles require at minimum E1 (literature-informed). E0 demonstrative is
  deprecated. S0 synthetic fixtures may be used only for tests and must not
  appear as scientific scenarios in release artifacts.
- **Impact:** Without E1 minimum enforcement, model-facing profiles could
  appear without literature grounding, undermining scientific positioning.
- **Status:** AMENDMENT (v0.5.6 ADR-010 amendment)
- **Pre-requisite:** v0.6.0 must enforce evidence_level >= E1 for model-facing
  profiles and confine S0 to test suites.
- **Versão-alvo:** v0.6.0
- **Evidence:** [ADR-010 Amendment v0.5.6](../adr/ADR-010-c1-energy-distribution-scope.md)

---

### TD-C1-ENERGY-PROFILE-01: Curated E1/E2 Profile Libraries

- **Description:** Piecewise D_it(E) integration is implemented as C1
  energy-distribution bookkeeping (v0.6.0). Future work may add curated
  E1 (literature-informed) or E2 (experimental-profile) profile libraries
  with pre-validated bin configurations for common Si/SiO₂ interfaces.
- **Impact:** Without curated profiles, users must manually construct
  `PiecewiseDitProfile` instances with appropriate evidence metadata.
- **Status:** DEFERRED
- **Pre-requisite:** C2 remains blocked until a separate ADR. Profile
  libraries must not enable ρ_eff, t_eff, or solver coupling.
- **Versão-alvo:** TBD (post v0.6.0)
- **Evidence:** [energy_profiles.py](../../src/mvp_quantum_materials/energy_profiles.py)

---

### TD-PROCESS-DEVICE-ROADMAP-01: Layers L3–L6 Not Implemented

- **Description:** The project is re-anchored toward a process-to-device
  demonstrator (ADR-011), but layers L3 (ρ_eff), L4 (Poisson coupling),
  L5 (V_conf), and L6 (Schrödinger) remain blocked until dedicated ADRs
  and TDD cycles are completed for each layer.
- **Impact:** The project currently reaches only L2 (σ_eff). The full
  chain from defects to quantum confinement is documented but not implemented.
- **Status:** DEFERRED (by design)
- **Pre-requisite:** Each layer requires its own ADR, council, TDD RED/GREEN.
- **Versão-alvo:** L3 at v0.7, L4 at v0.8, L5–L6 at v0.9, integration at v1.0
- **Evidence:** [ADR-011](../adr/ADR-011-process-to-device-qubit-demonstrator-roadmap.md)

---

### TD-C1-PROFILE-LIBRARY-01: Curated Profiles Are Not Calibrated

- **Description:** The curated E1/E2 profile library provides literature-
  informed scale profiles for Si/SiO₂. These are piecewise approximations
  of literature D_it ranges, not measured energy-resolved curves. Future
  C2 development must not treat these profiles as calibrated device data.
- **Impact:** Downstream quantities (N_it, σ_eff) are literature-scale
  estimates only. They cannot be used for device prediction.
- **Status:** ACCEPTED (by design)
- **Pre-requisite:** C2 requires its own ADR with explicit t_eff semantics.
- **Versão-alvo:** C2 at v0.7, must not reuse library profiles as calibration.
- **Evidence:** [dit_profile_library.py](../../src/mvp_quantum_materials/dit_profile_library.py)

---

### TD-C2-INTERFACE-SOURCE-01: ADR-C2 Proposed — Implementation Blocked

- **Description:** ADR-012 proposes C2-A (interface sheet source) as primary
  path for σ_eff → electrostatic coupling. Volume regularization (C2-B) is
  fallback only, using l_reg as numerical parameter, not physical t_eff.
  Generic physical t_eff is rejected (C2-D). Calibrated t_eff is blocked
  (C2-E). No C2 code exists.
- **Impact:** Future implementation must follow ADR-012 recommendation.
  No solver coupling, no ρ_eff API, no t_eff parameter until RED/GREEN.
- **Status:** ACTIVE (ADR-012 Accepted in v0.7.1)
- **Pre-requisite:** TDD RED phase (v0.7.2).
- **Versão-alvo:** v0.7.2 (C2 RED after ADR-012 acceptance in v0.7.1).
- **Evidence:** [ADR-012](../../docs/adr/ADR-012-c2-interface-sheet-source-vs-volume-regularization.md)

---

### TD-C2-ACCEPTANCE-01: ADR-012 Accepted — Implementation Still Blocked

- **Description:** ADR-012 accepted in v0.7.1. C2 implementation
  remains blocked until v0.7.2 RED phase. No ρ_eff/t_eff/l_reg/solver
  implementation exists yet.
- **Impact:** C2 RED must be created before any GREEN implementation.
  v0.7.2 = RED, v0.7.3 = GREEN (earliest).
- **Status:** ACTIVE (by design — awaiting v0.7.2 RED)
- **Pre-requisite:** v0.7.2 RED tests created and failing.
- **Versão-alvo:** v0.7.2 (C2 RED).
- **Evidence:** [ADR-012 Acceptance Note](../../docs/adr/ADR-012-c2-interface-sheet-source-vs-volume-regularization.md)

---

### TD-C2-GREEN-01: C2 Mapping is Bookkeeping Only

- **Description:** C2 mapping is implemented as isolated source/regularization bookkeeping only. It does not solve electrostatics, does not couple to a solver, and does not authorize physical potential interpretation.
- **Impact:** Ensures scientific integrity but leaves the project uncoupled from actual physical equation solving.
- **Status:** ACTIVE
- **Versão-alvo:** Future C3 coupling phase.

---

### TD-C2-DEMO-01: C2 Demo Exists But No Solver Coupling

- **Description:** C2 mapping demo validates charge conservation and l_reg sensitivity in isolation. No electrostatic solver coupling is authorized. Future v0.8.0 must decide solver coupling via ADR.
- **Impact:** Demo builds confidence in C2 mapping correctness but does not verify physical behavior under solver.
- **Status:** ACTIVE
- **Versão-alvo:** v0.8.0 — ADR for C3 solver coupling.

---

### TD-METHODOLOGY-ACCELERATION-01: Methodology Acceleration Skills and Templates

- **Description:** Methodology acceleration skills and templates added (v0.7.5) to reduce repetitive governance overhead while preserving ADR/TDD/CI/release discipline. Six new skills, seven templates, release methodology checklist, and human decision log created.
- **Impact:** Reduces prompt size and documentation redundancy for future releases. Does not alter scientific behavior or code.
- **Status:** RESOLVED (v0.7.5)
- **Versão-alvo:** v0.7.5 — completed.

---

### TD-AIFS-TRACK-01: AI-for-Science Track — Documentation-Only Parallel Feasibility

- **Description:** AI-for-Science track proposed as documentation-only parallel feasibility (v0.7.6). No implementation, no dependency, no ML runtime. Covers PINNs, surrogate models, and operator learning as future exploratory possibilities only.
- **Impact:** Opens a governed path for future ML exploration without contaminating the classical solver roadmap. No scientific behavior altered.
- **Status:** ACTIVE
- **Versão-alvo:** Future — activation requires accepted ADR, dependency decision, analytic benchmarks, RED tests, reproducibility plan, and human approval.
