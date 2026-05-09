# Technical Debt Scorecard — MVP v0.1 / v0.2 / v0.2.1 / v0.3 / v0.3.1–v0.3.5

> **Last updated:** 2026-05-09

## Summary

| Status | Count |
|--------|-------|
| RESOLVED | 6 |
| PARTIALLY RESOLVED | 1 |
| DEFERRED | 5 |
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
