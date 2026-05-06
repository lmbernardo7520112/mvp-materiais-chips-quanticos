# mvp-materiais-chips-quanticos

> **Modelagem termo-difusiva simplificada para análise de heterogeneidades
> em material semicondutor idealizado**

[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Status](https://img.shields.io/badge/status-MVP%20v0.1-orange)]()

## Objetivo

MVP computacional institucional e tecnicamente defensável para demonstrar uma
ponte **metodológica** entre simulação numérica (transporte de calor e massa,
mudança de fase) e uma nova frente em materiais semicondutores aplicáveis a
dispositivos quânticos de estado sólido.

## Hipótese Central

Condições térmicas e difusivas idealizadas podem ser usadas como primeira
aproximação para estudar heterogeneidades em materiais semicondutores, servindo
como etapa inicial para conversas técnicas sobre defeitos, interfaces,
variabilidade e controle de processo em dispositivos quânticos de estado sólido.

## Limites Científicos Obrigatórios

1. **Não** afirma que o MVP simula fabricação industrial real de wafer.
2. **Não** afirma que o MVP prediz coerência quântica.
3. **Não** afirma equivalência direta entre solidificação metálica e fabricação de semicondutores.
4. A transferência é **metodológica**: formulação física, solução numérica, análise de sensibilidade, métricas e governança.
5. Fato, hipótese, inferência e limitação são separados em toda a documentação.
6. Qualquer inferência sobre chips quânticos é formulada de modo prudente e não causal.

## Natureza da Variável C

> **IMPORTANTE:** A variável C utilizada nos modelos difusivos é um **proxy
> adimensional** de heterogeneidade/defeitos. C **não** representa concentração
> física calibrada e **não** deve ser comparado quantitativamente com densidade
> real de defeitos em semicondutores.

## Escopo Funcional (v0.1)

- Solver térmico 1D — condução transiente (Dirichlet BCs)
- Solver difusivo 1D — variável C com difusividade Arrhenius e fonte gaussiana (Neumann no-flux BCs)
- 6 métricas de heterogeneidade
- Análise de sensibilidade com ≥5 parâmetros
- Geração automática de figuras
- Documentação institucional e governança completa

## Instalação

```bash
# Clone
git clone <repo-url>
cd mvp-materiais-chips-quanticos

# Ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate

# Dependências
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Uso

```bash
# Solver térmico 1D
python scripts/run_thermal_1d.py

# Solver difusivo 1D
python scripts/run_diffusion_1d.py

# Análise de sensibilidade
python scripts/run_sensitivity.py

# Gerar todos os resultados
python scripts/generate_all_results.py --output-dir results/figures
```

## Testes

```bash
pytest -v --tb=short
```

## Lint

```bash
ruff check .
ruff format --check .
```

## Arquitetura

```
src/mvp_quantum_materials/
├── config.py              # Constantes físicas, dataclasses de configuração
├── domain.py              # Domínio computacional 1D
├── thermal_solver.py      # Solver térmico com guard de estabilidade
├── diffusion_solver.py    # Solver difusivo (Arrhenius + fonte + guard)
├── metrics.py             # Métricas de heterogeneidade
├── sensitivity.py         # Análise de sensibilidade paramétrica
└── plots.py               # Geração de figuras
```

## Documentação

- [Plano Técnico](docs/plano_tecnico_mvp.md)
- [Hipóteses e Limitações](docs/hipoteses_e_limitacoes.md)
- [Referências](docs/referencias.md)
- [Parâmetros](docs/parameters.md)
- [Governança](docs/governance/)
- [ADRs](docs/adr/)

## Governança

Este projeto segue o padrão AcademiaFlow de governança:
SDD + Clean Code + TDD + GitHub Actions + commits profissionais.

## Licença

MIT
