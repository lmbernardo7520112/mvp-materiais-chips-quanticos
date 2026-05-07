# Relatório Técnico — MVP v0.2

> **Data:** 2026-05-06  
> **Autor:** Staff Research Software Engineer (AI-assisted)  
> **Branch:** `feature/v0.2-2d-robustness`  
> **Status:** Implementação local completa — aguardando push

---

## 1. Objetivo da v0.2

A versão 0.2 do MVP de modelagem de semicondutores quânticos tem como
objetivo consolidar a **robustez numérica** da plataforma computacional,
estendendo a infraestrutura de 1D para 2D de forma controlada.

O escopo foi definido pela [ADR-004](docs/adr/ADR-004-v0.2-scope-selection.md)
(Accepted) e alinha-se com o estágio v0.2 do roadmap process-to-device
[ADR-005](docs/adr/ADR-005-process-to-device-bridge-roadmap.md):

> "v0.2: robustez numérica — convergência e extensão 2D da equação do calor."

---

## 2. O que foi implementado

### 2.1 Domain2D

Domínio computacional 2D retangular estruturado com grade uniforme:

- Parâmetros: `Lx`, `Ly`, `nx`, `ny`
- Propriedades computadas: `dx`, `dy`, `x`, `y`
- Validação: nx/ny ≥ 3, Lx/Ly > 0
- Implementação: `dataclass(frozen=True)` em `domain.py`
- **Domain1D inalterado** (additive-only)

### 2.2 Solver Térmico 2D

Solver explícito para a equação do calor 2D:

```
∂T/∂t = α · (∂²T/∂x² + ∂²T/∂y²)
```

- Método: Euler explícito + diferenças finitas centradas
- Condições de contorno: Dirichlet homogêneo (T fixo nas 4 bordas)
- Saída: `ThermalResult2D` com `T_final`, `T_history`, `dt`, `n_steps`, `times`
- Módulo: `thermal_solver_2d.py` (arquivo separado — não altera `thermal_solver.py`)

### 2.3 Critério de Estabilidade 2D

Fórmula CFL para 2D:

```
dt ≤ safety_factor · dx² · dy² / (2 · α · (dx² + dy²))
```

- Função: `compute_max_stable_dt_thermal_2d` em `config.py`
- Guard: reusa `validate_stability` existente
- **Funções de estabilidade 1D inalteradas**

### 2.4 Análise de Convergência Manufaturada

Caso analítico para validação do solver:

```
T(x,y,t) = sin(π·x/Lx) · sin(π·y/Ly) · exp(-α·π²·(1/Lx² + 1/Ly²)·t)
```

- BCs: Dirichlet homogêneo (T = 0)
- Sequência de refinamento: nx = ny ∈ {11, 21, 41, 81}
- Métricas: erro L2, erro L∞, ordem observada
- **observed_order ≥ 1.5 confirmado** em pelo menos uma faixa
- Saídas: `convergence_results.csv`, `convergence_analysis.png`

### 2.5 Coverage e CI

- `pytest-cov` adicionado às dependências dev
- CI atualizado com `--cov-fail-under=70`
- **Coverage atingido: 92.44%** (gate: 70%)
- CI verifica artefatos v0.1 (4 figs + CSV) e v0.2 (2 figs + CSV)

### 2.6 Visualização 2D

- Contour plot `thermal_2d_final.png` via `plot_thermal_2d_final`
- Todas as figuras 2D contêm disclaimer: "demonstrativo — não calibrado"
- Convergence plot log-log com referência O(dx²)

---

## 3. O que NÃO foi implementado

| Item | Classificação | Justificativa |
|------|---------------|---------------|
| Difusão 2D | SHOULD (deferido) | MUST gates devem estar verdes primeiro |
| Notebooks/Jupytext | SHOULD (deferido) | Scripts CLI cobrem funcionalidade básica |
| Morris/Sobol global | COULD (deferido) | OAT demonstrativo é suficiente |
| Poisson 2D | WON'T (v0.4) | Requer ρ_eff de C_def (v0.3) |
| Schrödinger | WON'T (v0.5) | Requer potencial V de Poisson (v0.4) |
| TCAD/QTCAD | WON'T | Quebra ADR-001 (Python/NumPy First) |
| Czochralski real | WON'T | Escopo de tese de doutorado |
| Phase-field | WON'T | Fora da rota ADR-005 |
| Coerência quântica | WON'T | ADR-002 permanente |
| Calibração de C | WON'T (v0.5+) | C permanece proxy adimensional |

---

## 4. Interpretação das Novas Figuras

### 4.1 thermal_2d_final.png

Contour plot do campo térmico 2D no estado final, mostrando:
- Gradiente suave do interior (T_init = 1500 K) para as bordas (T_boundary = 1400 K)
- Simetria radial aproximada, consistente com Dirichlet homogêneo
- **Não representa** uma fatia de wafer real — é demonstrativo

### 4.2 convergence_analysis.png

Gráfico log-log do erro (L2 e L∞) vs espaçamento dx, mostrando:
- Decaimento monotônico do erro com refinamento
- Referência O(dx²) indica que o solver se aproxima de 2ª ordem
- Anotações de `observed_order` em cada ponto de refinamento
- Convergência confirma consistência numérica do solver

---

## 5. Interpretação do convergence_results.csv

Tabela com colunas:

| Coluna | Descrição |
|--------|-----------|
| nx, ny | Número de nós da malha |
| dx, dy | Espaçamento da grade [m] |
| dt | Passo de tempo usado [s] |
| error_l2 | Erro L2 (RMS) vs solução analítica |
| error_linf | Erro máximo absoluto vs solução analítica |
| observed_order | Taxa de convergência observada entre malhas |
| elapsed_time | Tempo de execução [s] |

O erro L2 deve diminuir com o refinamento. A ordem observada confirma
que o solver é consistente com a discretização de 2ª ordem espacial.

---

## 6. Limitações

1. **C permanece proxy adimensional** — não é concentração física calibrada.
2. **Parâmetros são toy/demonstrativos** — não calibrados com dados experimentais.
3. **Domínio 2D é retangular uniforme** — não representa geometria real de wafer.
4. **Solver é explícito** — estabilidade limita dt para malhas finas (custo O(nx²·ny²·nt)).
5. **BCs são Dirichlet homogêneo** — não modela condições de contorno industriais.
6. **Sem acoplamento termo-difusivo 2D** — difusão 2D foi deferida.
7. **Convergência testada apenas com solução analítica simples** — modo fundamental.
8. **Sem ADI nem solver implícito** — limitação de desempenho para malhas grandes.

---

## 7. O que NÃO pode ser inferido

- ❌ Comportamento de wafer real em forno de Czochralski
- ❌ Distribuição de defeitos em silício
- ❌ Coerência quântica de qubits
- ❌ Parâmetros de processo industrial
- ❌ Validação experimental de qualquer natureza
- ❌ Comparação com TCAD/QTCAD comercial

---

## 8. Relação com ADR-004 e ADR-005

- **ADR-004 (Accepted):** Define v0.2 como etapa de robustez numérica.
  Todos os requisitos MUST foram atendidos. SHOULD e COULD foram deferidos
  conforme documentado na ADR.

- **ADR-005 (Accepted):** Roadmap process-to-device em 5 ondas.
  v0.2 completa a onda "robustez numérica e convergência".
  A próxima onda (v0.3) é "defect-like reaction-diffusion".

---

## 9. Próximos Passos

1. **Push autorizado** → PR → CI → merge → tag `v0.2.0`
2. **SHOULD items** (v0.2.1): difusão 2D, notebooks
3. **v0.3**: defect-like reaction-diffusion (G(T), R(T,C))
4. **v0.4**: eletrostática base (Poisson)
5. **v0.5**: confinamento quântico (Schrödinger)
6. **v1.0**: demonstrador completo do bridge process-to-device
