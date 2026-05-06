# Technical Debt Scorecard — MVP v0.1

> **Last updated:** 2026-05-06

## Summary

| Status | Count |
|--------|-------|
| RESOLVED | 0 |
| DEFERRED | 2 |
| OPEN | 0 |
| WONTFIX | 0 |

---

## TD-01: 2D Case Not Implemented

- **Description:** Caso 2D simplificado não implementado no v0.1.
- **Impact:** Escopo visual limitado a 1D; demonstração menos abrangente.
- **Status:** DEFERRED
- **Decision:** ADR-003 — deferido para v0.2 como stretch goal.
- **Evidence:** [ADR-003](../adr/ADR-003-2d-scope-decision.md)

---

## TD-02: Notebooks Not Created

- **Description:** Notebooks Jupyter (.ipynb) não criados no v0.1.
- **Impact:** Visualização interativa não disponível; usuários
  devem usar scripts CLI.
- **Status:** DEFERRED
- **Decision:** Notebooks deferidos para v0.2. Scripts .py
  com `--output-dir` cobrem a funcionalidade básica.
  Ver `notebooks/README.md`.
- **Evidence:** [notebooks/README.md](../../notebooks/README.md)
