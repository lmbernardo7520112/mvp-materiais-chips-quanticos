# Tutorial: Reproduzindo os Resultados da v0.2.0

> **Versão alvo:** v0.2.0  
> **Tempo estimado:** ~5 minutos  
> **Pré-requisitos:** Python 3.11+, pip, git

---

## 1. Pré-Requisitos

- Python 3.11 ou 3.12 instalado
- `pip` funcional
- `git` instalado
- Terminal Unix/Linux (macOS/Linux) ou WSL2

---

## 2. Clonar o Repositório

```bash
git clone https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos.git
cd mvp-materiais-chips-quanticos
git checkout v0.2.0
```

---

## 3. Criar e Ativar o Ambiente Virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Instalar o Pacote e Dependências

```bash
pip install -e ".[dev]"
```

Isso instala:
- `numpy`, `matplotlib`, `scipy` (runtime)
- `pytest`, `pytest-cov`, `ruff` (dev)

---

## 5. Rodar os Testes

```bash
pytest -v --tb=short
```

**Resultado esperado:** `56 passed`

---

## 6. Verificar Cobertura

```bash
pytest --cov=mvp_quantum_materials --cov-report=term-missing --cov-fail-under=70
```

**Resultado esperado:** `Total coverage: 92.44%` (acima do gate de 70%)

---

## 7. Verificar Linting e Formatação

```bash
ruff check .
ruff format --check .
```

**Resultado esperado:** `All checks passed` / `files already formatted`

---

## 8. Gerar Todos os Resultados

```bash
python scripts/generate_all_results.py --output-dir results/figures
```

**Resultado esperado:** 6 figuras + 2 CSVs

---

## 9. Onde Encontrar os Artefatos

### Figuras (results/figures/)

| Arquivo | Conteúdo |
|---------|----------|
| `thermal_1d_evolution.png` | Evolução temporal do campo térmico 1D |
| `diffusion_1d_evolution.png` | Evolução temporal do campo difusivo 1D |
| `sensitivity_analysis.png` | Sensibilidade paramétrica OAT |
| `sensitivity_ranking.png` | Ranking de sensibilidade por parâmetro |
| `thermal_2d_final.png` | Campo térmico 2D final (contour plot) |
| `convergence_analysis.png` | Convergência log-log com referência O(dx²) |

### Tabelas (results/tables/)

| Arquivo | Conteúdo |
|---------|----------|
| `sensitivity_results.csv` | Resultados detalhados de sensibilidade OAT |
| `convergence_results.csv` | Erro L2, L∞, observed_order por refinamento |

---

## 10. Como Interpretar Cada Artefato

### thermal_2d_final.png

Mostra o campo de temperatura 2D no estado final. O gradiente suave
do interior para as bordas é consistente com BCs de Dirichlet. Não
representa uma fatia de wafer real — é demonstrativo.

### convergence_analysis.png

Gráfico log-log mostrando que o erro (L2 e L∞) diminui com o
refinamento de malha. A referência O(dx²) indica consistência do
solver com a discretização de 2ª ordem.

### convergence_results.csv

Cada linha representa um nível de refinamento. A coluna `observed_order`
mostra a taxa de convergência entre malhas consecutivas. Valores ≥ 1.5
confirmam convergência formal.

---

## 11. Rodar Scripts Individuais

```bash
# Solver térmico 2D isolado
python scripts/run_thermal_2d.py --output-dir results/figures

# Convergência isolada
python scripts/run_convergence.py --output-dir results/figures

# Solver térmico 1D isolado
python scripts/run_thermal_1d.py --output-dir results/figures

# Sensibilidade isolada
python scripts/run_sensitivity.py --output-dir results/figures
```

---

## 12. Limitações

1. Todos os parâmetros são **toy/demonstrativos**. Não são calibrados.
2. C é um **proxy adimensional**, não uma concentração física.
3. O domínio 2D é uma abstração numérica, não uma fatia de wafer.
4. BCs são Dirichlet homogêneo simplificado.
5. Solver é explícito — estabilidade limita dt para malhas finas.

---

## 13. Troubleshooting

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError` | Verifique que `pip install -e ".[dev]"` foi executado |
| Coverage abaixo de 70% | Verifique que pytest-cov está instalado: `pip install pytest-cov` |
| Figuras não geradas | Verifique que matplotlib está instalado e o output-dir existe |
| ruff não encontrado | Execute `pip install ruff` |

---

## 14. O que Este Tutorial NÃO Prova

- ❌ Que o modelo simula um semicondutor real
- ❌ Que os parâmetros estão calibrados
- ❌ Que os resultados podem ser citados como predições físicas
- ❌ Que existe eletrostática, defeitos ou confinamento quântico
- ❌ Que o sistema prediz coerência de qubits

O tutorial demonstra que a infraestrutura computacional é **reproduzível,
testada e auditável** — condição necessária para evolução científica futura.
