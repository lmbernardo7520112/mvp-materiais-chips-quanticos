# Relatório Técnico — MVP v0.1 (30 dias)

> **Data:** 2026-05-06  
> **Projeto:** mvp-materiais-chips-quanticos  
> **Autor:** L. Bernardo

## Resumo Executivo

Foi desenvolvido um MVP computacional para demonstrar a ponte **metodológica**
entre simulação numérica de transporte de calor/massa e análise de
heterogeneidades em materiais semicondutores idealizados para dispositivos
quânticos de estado sólido.

## Resultados Obtidos

### Solver Térmico 1D
- Equação de calor resolvida com Euler explícito e diferenças finitas centradas.
- Condições de contorno Dirichlet.
- Guard de estabilidade: rejeita dt instável com erro claro.
- 4 testes unitários passam.

### Solver Difusivo 1D
- Difusividade Arrhenius: D(T) = D₀·exp(-Eₐ/(k_B·T)).
- Fonte gaussiana: S_C(T) = A_C·exp(-(T-T_c)²/(2·σ_T²)).
- Condições de contorno Neumann no-flux.
- Guard de estabilidade.
- 7 testes unitários passam.

### Métricas de Heterogeneidade
- 6 métricas implementadas e testadas.
- Todas retornam valores finitos.

### Análise de Sensibilidade
- 5 parâmetros variados independentemente.
- 20 casos avaliados.
- Tabela de resultados e figura gerada.

### Figuras
- 3 figuras geradas automaticamente por CLI.

## Limitações

> [!WARNING]
> **Natureza de C:** A variável C utilizada nos modelos difusivos é um
> **proxy adimensional** de heterogeneidade/defeitos. C **não** representa
> concentração física calibrada e **não** deve ser comparado quantitativamente
> com densidade real de defeitos em semicondutores.

Consulte `docs/hipoteses_e_limitacoes.md` para lista completa de 7 limitações.

## Governança

- 11 commits atômicos e semânticos.
- 19 testes unitários (≥17 exigidos).
- ruff check + ruff format verdes.
- 3 ADRs documentados.
- 2 dívidas técnicas deferidas (2D, notebooks).
- Working tree limpo.
- CI workflow criado (validação remota pendente push).

## Próximos Passos (v0.2)

1. Caso 2D simplificado.
2. Notebooks Jupyter derivados dos scripts.
3. Análise de convergência.
4. Calibração de parâmetros com literatura.
5. Coverage com pytest-cov.
