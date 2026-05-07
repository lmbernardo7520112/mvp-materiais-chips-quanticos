# Technical Debt Scorecard — MVP v0.1 / v0.2

> **Last updated:** 2026-05-06

## Summary

| Status | Count |
|--------|-------|
| RESOLVED | 1 |
| DEFERRED | 7 |
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
- **Status:** DEFERRED
- **Justificativa:** Classificado como SHOULD na ADR-004. Funcionalidade
  coberta por scripts CLI. Não bloqueia gates MUST.
- **Versão-alvo:** v0.2.1 ou v0.3
- **Evidence:** [ADR-004 §SHOULD](../adr/ADR-004-v0.2-scope-selection.md)

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
