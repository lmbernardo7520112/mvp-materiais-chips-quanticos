# Implementation Plan — mvp-materiais-chips-quanticos v0.1-r2

> **Status:** APPROVED — Executing Phases 1-6  
> **Author:** Staff Research Software Engineer (AI-assisted)  
> **Date:** 2026-05-06  
> **Revision:** r2-final — 12 corrections + 5 final adjustments  
> **Methodology:** SDD + TDD + Clean Code  
> **Governance:** AcademiaFlow-compatible

---

## Changelog (v0.1-r1 → v0.1-r2)

| # | Correção | Seções afetadas |
|---|----------|-----------------|
| C-01 | 2D reclassificado como STRETCH GOAL; só após todos gates 1D verdes | S-12, ADR-003, §3, §8, §9, §11 |
| C-02 | Python `>=3.11,<3.13`; CI matrix 3.11+3.12; dev local 3.12 | §2, pyproject, CI |
| C-03 | Estabilidade Euler formalizada; solvers recusam dt instável; testes de violação | §6.2, §10.1, R-01 |
| C-04 | BCs explícitas: Dirichlet(T), Neumann no-flux(C); testes dedicados | §6.2, §10.1 |
| C-05 | C declarado como proxy adimensional; limitação em README/hipóteses/relatório | §2, RF-03, §4, RNF-04 |
| C-06 | `docs/parameters.md` adicionado com tabela formal de parâmetros | §6, RF-08, Commit 3 |
| C-07 | 5 testes adicionais para S_C: máximo, não-negativa, decaimento, NaN/inf, C finito | §10.1 (T-13..T-17) |
| C-08 | ruff obrigatório (`ruff check` + `ruff format --check`); black removido | §2, Gate 2, R-03 |
| C-09 | `generate_all_results.py` aceita `--output-dir`; testes usam `tmp_path`; CI artifacts | §9, RF-07, RF-09 |
| C-10 | Projetos correlatos: assunção pendente auditoria; regra de não-reuso sem registro | §2 |
| C-11 | Notebooks removidos dos gates v0.1; `notebooks/README.md` stub only | §3, §6, RNF-07 |
| C-12 | GitHub remote só após gates locais verdes; push requer autorização | §9, §11 |

---

## 1. Visão

MVP computacional institucional que demonstra ponte **metodológica** entre simulação numérica (transporte de calor/massa) e análise de heterogeneidades em materiais semicondutores para dispositivos quânticos.

> [!IMPORTANT]
> Transferência **metodológica** apenas. Não simula fabricação industrial, não prediz coerência quântica, não afirma equivalência solidificação metálica ↔ fabricação de semicondutores.

---

## 2. Contexto e Premissas

| Item | Valor |
|------|-------|
| Python | `>=3.11,<3.13` (dev local: 3.12; CI: 3.11 + 3.12) |
| Bibliotecas core | NumPy, Matplotlib, SciPy (opcional) |
| Teste | pytest |
| Linter/Formatter | ruff (`ruff check .` + `ruff format --check .`) — **obrigatório** |
| CI/CD | GitHub Actions |
| Branch | `feature/mvp-termo-difusivo-quantum-materials` |
| Repositório | `mvp-materiais-chips-quanticos` |
| Workspace | `/home/leonardomaximinobernardo/My_projects/mvp-materiais-chips-quanticos` |
| Projetos correlatos | `interdendritico`, `teseLB` — **assunção** de não-reutilização pendente auditoria formal |

> [!WARNING]
> **Regra de reuso:** Nenhum código de projetos legados será reutilizado sem auditoria explícita, registro de autoria/licença e justificativa em `walkthrough.md`.

**Premissa científica:** Condições térmicas e difusivas idealizadas como primeira aproximação para heterogeneidades em semicondutores.

**Natureza de C:** A variável C é um **proxy adimensional** de heterogeneidade/defeitos. Não representa concentração física calibrada e não deve ser comparada quantitativamente com densidade real de defeitos. Esta limitação deve constar em README, `hipoteses_e_limitacoes.md` e `relatorio_30_dias.md`.

---

## 3. Escopo

### 3.1 IN — Core (v0.1)

| ID | Escopo |
|----|--------|
| S-01 | Domínio 1D com grade uniforme |
| S-02 | Solver térmico 1D transiente (Dirichlet BCs) |
| S-03 | Solver difusivo 1D com Arrhenius + fonte (Neumann no-flux BCs) |
| S-04 | Fonte térmica S_C(T) gaussiana |
| S-05 | 6 métricas de heterogeneidade |
| S-06 | Análise de sensibilidade ≥5 parâmetros |
| S-07 | Geração automática ≥3 figuras (`--output-dir`) |
| S-08 | README institucional + `parameters.md` |
| S-09 | ≥17 testes com pytest |
| S-10 | CI/CD GitHub Actions (matrix 3.11+3.12) — ci.yml criado localmente; validação remota bloqueada até push autorizado |
| S-11 | Governança completa |

### 3.2 STRETCH GOAL (v0.1, condicional)

| ID | Escopo | Pré-condição |
|----|--------|-------------|
| S-12 | Caso 2D simplificado | **Todos** gates 1D verdes (pytest, ruff, scripts, ≥3 figuras, docs). Se qualquer falhar → deferir v0.2 via ADR-003 |

### 3.3 OUT (v0.1)

| ID | Exclusão |
|----|----------|
| X-01 | Simulação de fabricação industrial |
| X-02 | Predição de coerência quântica |
| X-03 | Phase-field models |
| X-04 | OpenFOAM/FEniCSx/MOOSE/PRISMS-PF (ADR-001) |
| X-05 | Validação experimental |
| X-06 | Notebooks `.ipynb` com lógica (deferidos v0.2) |
| X-07 | GitHub remote antes de gates locais verdes |

---

## 4. Requisitos Funcionais

| ID | Requisito | Critério de Aceite |
|----|-----------|-------------------|
| RF-01 | Domínio 1D | `Domain1D` com `length`, `nx`, `dx`, `x` coerentes |
| RF-02 | Solver térmico 1D | Campo constante→estável; gradiente→suaviza; saída finita; **recusa dt instável** |
| RF-03 | Solver difusivo 1D | D(T) Arrhenius; campo constante sem fonte→estável (Neumann); **recusa dt instável**; C proxy adimensional |
| RF-04 | Fonte térmica S_C(T) | Máximo em Tc; não-negativa; decai longe de Tc; sem NaN/inf |
| RF-05 | Métricas | 6 métricas finitas: grad_max, non_unif_T, non_unif_C, acumulo_local, integral_C, ranking |
| RF-06 | Sensibilidade | ≥5 parâmetros, tabela não-vazia |
| RF-07 | Figuras | ≥3 em `results/figures/`; CLI com `--output-dir`; testes usam `tmp_path` |
| RF-08 | Documentação | README, referências, hipóteses, parâmetros, plano técnico |
| RF-09 | CI/CD | pytest + ruff + scripts + figuras; matrix 3.11+3.12; upload artifacts |

---

## 5. Requisitos Não-Funcionais

| ID | Requisito | Verificação |
|----|-----------|-------------|
| RNF-01 | Reprodutibilidade | Scripts CLI com `--output-dir` |
| RNF-02 | Legibilidade | Funções pequenas, type hints, docstrings |
| RNF-03 | Testabilidade | ≥17 testes, pytest verde |
| RNF-04 | Prudência científica | C = proxy adimensional; fato/hipótese/inferência/limitação separados |
| RNF-05 | Rastreabilidade | Commits atômicos, ADRs, governança |
| RNF-06 | CI verde | GitHub Actions matrix passa |
| RNF-07 | Notebooks deferidos | Apenas `notebooks/README.md` em v0.1 |
| RNF-08 | Estabilidade numérica | Solvers recusam dt instável com erro claro |
| RNF-09 | Working tree limpo | Testes em `tmp_path`; geração não polui repo |

---

## 6. Arquitetura

```
mvp-materiais-chips-quanticos/
├── README.md
├── requirements.txt
├── pyproject.toml                    # requires-python = ">=3.11,<3.13"
├── .gitignore
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/ci.yml             # matrix: [3.11, 3.12]
├── docs/
│   ├── plano_tecnico_mvp.md
│   ├── hipoteses_e_limitacoes.md     # C = proxy adimensional
│   ├── referencias.md
│   ├── parameters.md                 # [NEW] tabela formal de parâmetros
│   ├── relatorio_30_dias.md
│   ├── adr/
│   │   ├── ADR-001-python-numpy-first.md
│   │   ├── ADR-002-no-quantum-coherence-prediction.md
│   │   └── ADR-003-2d-scope-decision.md  # 2D = stretch/deferred
│   └── governance/
│       ├── implementation_plan.md
│       ├── task.md
│       ├── walkthrough.md
│       ├── project_audit.md
│       └── technical_debt.md
├── src/mvp_quantum_materials/
│   ├── __init__.py
│   ├── config.py              # Dataclasses, constantes, stability checks
│   ├── domain.py              # Domain1D
│   ├── thermal_solver.py      # + stability guard
│   ├── diffusion_solver.py    # + stability guard, Neumann BC
│   ├── sensitivity.py
│   ├── metrics.py
│   └── plots.py
├── scripts/
│   ├── run_thermal_1d.py
│   ├── run_diffusion_1d.py
│   ├── run_sensitivity.py
│   └── generate_all_results.py   # --output-dir support
├── notebooks/
│   └── README.md              # stub: "notebooks em v0.2"
├── results/
│   ├── figures/
│   ├── tables/
│   └── runs/
└── tests/
    ├── test_domain.py
    ├── test_thermal_solver.py      # inclui teste de violação de estabilidade
    ├── test_diffusion_solver.py    # inclui testes S_C expandidos
    ├── test_metrics.py
    ├── test_sensitivity.py
    └── test_scripts.py             # usa tmp_path
```

### 6.1 Equações Governantes

**Calor 1D:** `∂T/∂t = α · ∂²T/∂x²`  
**Difusão com fonte:** `∂C/∂t = ∂/∂x[D(T)·∂C/∂x] + S_C(T)`  
**Arrhenius:** `D(T) = D₀·exp(-Eₐ/(k_B·T))`  
**Fonte:** `S_C(T) = A_C·exp(-(T-T_c)²/(2·σ_T²))`

### 6.2 Método Numérico

- Discretização espacial: diferenças finitas centradas
- Avanço temporal: Euler explícito
- **BCs térmicas (v0.1):** Dirichlet (T fixo nas extremidades)
- **BCs difusivas (v0.1):** Neumann no-flux (∂C/∂x = 0 nas extremidades)
- BCs configuráveis para extensão futura

**Estabilidade obrigatória:**

```
Solver térmico:   dt ≤ safety_factor × dx² / (2 × α)
Solver difusivo:  dt ≤ safety_factor × dx² / (2 × max(D(T)))
safety_factor = 0.4 (default, configurável)
```

> [!CAUTION]
> Os solvers **devem recusar** execução se dt violar o critério de estabilidade, com `ValueError` contendo mensagem clara indicando dt_max permitido. Sem clipping silencioso.

---

## 7. Matriz de Riscos

| ID | Risco | Prob. | Impacto | Mitigação |
|----|-------|-------|---------|-----------|
| R-01 | Instabilidade numérica | Média | Alto | Verificação de estabilidade obrigatória; solver recusa dt instável |
| R-02 | 2D inviável sem degradar 1D | Alta | Baixo | Stretch goal; deferido automaticamente se gates 1D falharem |
| R-03 | ruff indisponível no ambiente | Baixa | Médio | TD só com evidência de falha real de instalação |
| R-04 | Extrapolação científica | Média | Alto | C = proxy; revisão de texto; 6 limites obrigatórios |
| R-05 | CI falha por deps | Baixa | Médio | requirements.txt pinado; matrix 3.11+3.12 |
| R-06 | Reuso de código legado sem auditoria | Baixa | Alto | Regra: auditoria + licença + justificativa obrigatórias |

---

## 8. Critérios de Aceite — 22 gates: 19 locais obrigatórios + 2 stretch + 1 remoto

### 8.1 Gates 1D (obrigatórios — bloqueiam 2D e release)

| # | Gate | Verificação |
|---|------|-------------|
| 1 | pytest passa | `pytest -v` exit 0 |
| 2 | ruff passa | `ruff check . && ruff format --check .` exit 0 |
| 3 | ≥17 testes existem | `pytest --collect-only -q` |
| 4 | ≥3 figuras geradas | `ls results/figures/ \| wc -l` |
| 5 | Scripts executam com `--output-dir` | `python scripts/generate_all_results.py --output-dir /tmp/test` |
| 6 | README completo (C = proxy documentado) | Revisão |
| 7 | `docs/referencias.md` existe | `test -f` |
| 8 | `docs/hipoteses_e_limitacoes.md` existe | `test -f` |
| 9 | `docs/parameters.md` existe | `test -f` |
| 10 | Governança completa (5 docs) | `test -f` para cada |
| 11 | ≥3 ADRs existem | `ls docs/adr/` |
| 12 | PR template existe | `test -f` |
| 13 | Commits atômicos e semânticos | `git log --oneline` |
| 14 | Working tree limpo (`.gitignore` cobre `results/figures/*`, `results/tables/*`, `results/runs/*` com `.gitkeep`) | `git status` |
| 15 | Sem afirmações científicas exageradas | Revisão |
| 16 | Limitações documentadas | `grep -rl "limitação\|proxy" docs/` |
| 17 | Walkthrough com evidências locais (pytest, ruff, scripts, figuras, commits, working tree, ci.yml criado). Adendo com CI remoto só após push autorizado | Revisão de `walkthrough.md` |
| 18 | Solvers recusam dt instável | Testes T-15, T-16 |
| 19 | C finito em todas as simulações | Teste T-17 |

### 8.2 Gate stretch (2D)

| # | Gate | Verificação |
|---|------|-------------|
| 20 | Todos gates 1-19 verdes | Verificação automática |
| 21 | 2D implementado OU deferido via ADR-003 | ADR-003 atualizado |

### 8.3 Gate de release

| # | Gate | Verificação |
|---|------|-------------|
| 22 | CI GitHub Actions passa | Badge verde (após push autorizado). Não declarar CI remoto verde antes de push. |

---

## 9. Plano de Commits

| # | Mensagem | Conteúdo |
|---|----------|----------|
| 1 | `chore: initialize repository structure` | Dirs, .gitignore, requirements.txt, pyproject.toml, __init__.py, notebooks/README.md |
| 2 | `docs: add SDD implementation plan and governance tracker` | implementation_plan.md, task.md |
| 3 | `docs: add institutional README, references and parameters` | README.md, referencias.md, hipoteses_e_limitacoes.md, plano_tecnico_mvp.md, **parameters.md** |
| 4 | `test: add domain and thermal solver specifications` | test_domain.py, test_thermal_solver.py (inclui **teste de estabilidade**) |
| 5 | `feat: implement 1d domain and thermal solver` | config.py, domain.py, thermal_solver.py (com **stability guard**) |
| 6 | `test: add diffusion, arrhenius and source specifications` | test_diffusion_solver.py (inclui **5 testes S_C + estabilidade**) |
| 7 | `feat: implement diffusion model with stability guard` | diffusion_solver.py (Neumann BC, stability check) |
| 8 | `feat: add metrics and sensitivity analysis` | metrics.py, sensitivity.py, plots.py, test_metrics.py, test_sensitivity.py |
| 9 | `feat: add CLI scripts with --output-dir` | scripts/*, test_scripts.py (usa **tmp_path**) |
| 10 | `docs: add ADRs and technical debt scorecard` | ADR-001..003, technical_debt.md |
| 11 | `ci: add GitHub Actions with ruff and matrix` | ci.yml (matrix 3.11+3.12, ruff, artifacts), PR template |
| 12 | `docs: add walkthrough and project audit for v0.1` | walkthrough.md, project_audit.md, relatorio_30_dias.md |

> [!IMPORTANT]
> **Commit 11 e push remoto:** O CI só será configurado após gates locais 1-19 estarem verdes. Push para remote requer autorização explícita do usuário.

---

## 10. Plano de Verificação

### 10.1 Testes (≥17, TDD)

| # | Teste | Arquivo |
|---|-------|---------|
| T-01 | Domínio 1D: tamanho, dx, grade coerentes | test_domain.py |
| T-02 | Térmico: campo constante → estável | test_thermal_solver.py |
| T-03 | Térmico: gradiente → suaviza | test_thermal_solver.py |
| T-04 | Térmico: saída finita, shape correto | test_thermal_solver.py |
| T-05 | Arrhenius: D(T) cresce com T | test_diffusion_solver.py |
| T-06 | S_C: máximo próximo de Tc | test_diffusion_solver.py |
| T-07 | Difusivo: campo constante sem fonte → estável (Neumann) | test_diffusion_solver.py |
| T-08 | Métrica max/mean ≥ 1 | test_metrics.py |
| T-09 | Métricas finitas | test_metrics.py |
| T-10 | Sensibilidade: tabela não-vazia | test_sensitivity.py |
| T-11 | Scripts executam sem erro | test_scripts.py |
| T-12 | generate_all_results gera ≥3 figuras (tmp_path) | test_scripts.py |
| **T-13** | **S_C não-negativa para qualquer T** | test_diffusion_solver.py |
| **T-14** | **S_C tende a zero longe de Tc** | test_diffusion_solver.py |
| **T-15** | **Térmico recusa dt instável com ValueError** | test_thermal_solver.py |
| **T-16** | **Difusivo recusa dt instável com ValueError** | test_diffusion_solver.py |
| **T-17** | **C permanece finito após integração com fonte** | test_diffusion_solver.py |

### 10.2 Comandos de Validação Local

```bash
# Testes
pytest -v --tb=short

# Lint + format
ruff check .
ruff format --check .

# Geração com --output-dir
python scripts/generate_all_results.py --output-dir results/figures

# Contagens
pytest --collect-only -q | tail -1
ls results/figures/ | wc -l

# Working tree
git status
git log --oneline
```

---

## 11. Fases de Execução

### Fase 1: Scaffolding (Commits 1-3)
Repositório, estrutura, governança, documentação institucional, `parameters.md`.

### Fase 2: Core TDD (Commits 4-7)
Testes ANTES da implementação. Domínio, térmico (Dirichlet, stability), difusivo (Neumann, Arrhenius, S_C, stability). pytest verde a cada commit.

### Fase 3: Métricas e Sensibilidade (Commit 8)
Métricas, sensibilidade, plots. pytest verde.

### Fase 4: Scripts e Resultados (Commit 9)
Scripts CLI com `--output-dir`. Testes com `tmp_path`. ≥3 figuras.

### Fase 5: Governança e Qualidade (Commits 10-11)
ADRs, dívidas técnicas, CI/CD (matrix 3.11+3.12, ruff, artifacts), PR template.

### Fase 6: Auditoria e Release Local (Commit 12)
Walkthrough, project audit, relatório. Verificação de todos os 19 gates locais.

### Fase 7: Stretch Goal — 2D (condicional)
**Pré-condição:** Todos os gates 1-19 verdes.  
Se verde → implementar 2D simplificado + testes.  
Se qualquer gate falhar → deferir via ADR-003 para v0.2.

### Fase 8: Push Remoto (requer autorização)
Solicitar autorização do usuário → `gh repo create` ou push para remote existente → verificar CI verde (Gate 22).

---

## Decisões Resolvidas (ex-Open Questions)

| # | Questão | Decisão |
|---|---------|---------|
| Q-01 | GitHub remote | Só após gates locais verdes; push requer autorização |
| Q-02 | Notebooks | Deferidos v0.2; apenas `notebooks/README.md` em v0.1 |
| Q-03 | 2D | Stretch goal; condicional a gates 1D verdes |
| Q-04 | ruff/black | ruff obrigatório; black removido |

## Perguntas Remanescentes

Nenhuma pergunta remanescente bloqueia o início da implementação. O plano está autocontido.

> [!TIP]
> Se aprovado, a execução começará pela Fase 1 (Commit 1: scaffolding). Nenhum código será escrito antes da aprovação explícita.
