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
- Guard de estabilidade + verificação de finiteness a cada passo.
- 7 testes unitários passam.

### Métricas de Heterogeneidade
- 7 métricas implementadas e testadas (incluindo boundary flux proxy).
- Todas retornam valores finitos.
- A métrica `boundary_flux_proxy` verifica qualitativamente a condição
  de Neumann no-flux nas fronteiras.

### Análise de Sensibilidade
- 5 parâmetros variados independentemente.
- 20 casos avaliados.
- CSV exportado com tabela completa.
- Ranking normalizado gerado.

### Figuras
- 4 figuras geradas automaticamente por CLI.
- 1 CSV de sensibilidade.

---

## Interpretação das Figuras

### a) `thermal_1d_evolution.png`

**O que mostra:** Evolução temporal do campo de temperatura T(x) ao longo
do domínio 1D. Múltiplas curvas representam instantâneos em tempos diferentes,
mostrando a transição do perfil inicial para o estado estacionário.

**Hipótese associada:** O campo térmico com condições de contorno Dirichlet
(T_left = 1700 K, T_right = 1400 K) evolui monotonicamente para um perfil
linear em regime estacionário, conforme esperado para a equação de calor 1D
com difusividade constante.

**Limitação:** As condições de contorno são **demonstrativas** e não representam
temperaturas reais de um processo de fabricação de wafer. T_left e T_right são
valores idealizados para visualização de gradiente. Não deve ser interpretado
como simulação de processo industrial.

**O que NÃO pode ser inferido:** Não se pode inferir taxa de resfriamento de
silício real, perfil térmico de um forno Czochralski, nem qualquer condição
de processo de fabricação de semicondutores a partir desta figura.

---

### b) `diffusion_1d_evolution.png`

**O que mostra:** Evolução temporal da variável proxy C(x) ao longo do domínio 1D.
C é gerada pelo termo-fonte gaussiano e redistribuída pela difusividade Arrhenius.
Condições de contorno Neumann no-flux são aplicadas.

**Hipótese associada:** Regiões com temperatura mais próxima de T_c recebem
maior contribuição do termo-fonte, enquanto a difusividade Arrhenius redistribui
C preferencialmente em regiões de alta temperatura. Qualitativamente,
gradientes térmicos elevados correlacionam-se com maior heterogeneidade de C.

**Limitação:** C é um **proxy adimensional** de heterogeneidade/defeitos.
C **não** representa concentração física calibrada e **não** deve ser comparado
quantitativamente com densidade real de defeitos em semicondutores.
Os parâmetros D₀, Eₐ, T_c, σ_T e A_C são demonstrativos.

**O que NÃO pode ser inferido:** Não se pode inferir concentração real de
impurezas, densidade de defeitos em silício, perfil de dopagem, nem distribuição
de vacâncias a partir desta figura. Qualquer extrapolação para dispositivos
quânticos reais requer modelos e dados experimentais fora do escopo do MVP.

---

### c) `sensitivity_analysis.png`

**O que mostra:** Curvas de variação da métrica primária (integral global de C)
em função do índice de variação de cada um dos 5 parâmetros. Cada linha
representa um parâmetro variado independentemente enquanto os demais permanecem
em valores default.

**Hipótese associada:** A integral global de C é sensível a diferentes
parâmetros com magnitudes distintas, permitindo priorizar quais variáveis
do modelo têm maior influência na heterogeneidade total.

**Limitação:** A análise é one-at-a-time (OAT), não captura interações entre
parâmetros. Os valores e ranges são demonstrativos. A métrica é adimensional
e depende dos defaults escolhidos.

**O que NÃO pode ser inferido:** Não se pode inferir sensibilidade de processos
reais de fabricação de semicondutores. Não se pode ordenar parâmetros reais
de processo por importância com base nesta análise demonstrativa.

---

### d) `sensitivity_ranking.png`

**O que mostra:** Ranking horizontal dos 5 parâmetros ordenados por
sensibilidade normalizada (S = (max - min) / |mean|) para a métrica
integral global de C.

**Hipótese associada:** Parâmetros com maior S têm maior influência relativa
na heterogeneidade total dentro do range demonstrativo testado.

**Métrica de ranking:** A sensibilidade normalizada é definida como:
```
S_i = (max(M_i) - min(M_i)) / |mean(M_i)|
```
onde M_i é a métrica primária (integral global de C) avaliada nas variações
do parâmetro i. Esta métrica mede a amplitude relativa de variação:
valores maiores indicam que o parâmetro produz maior mudança percentual
na métrica de resposta.

**Limitação:** A sensibilidade normalizada é uma métrica **demonstrativa**
e **não calibrada**. Ela é válida apenas para o range de variação testado
e para a métrica específica escolhida (integral global de C). Análises mais
robustas (Sobol, Morris) requerem amostras mais extensas e estão fora do
escopo v0.1.

**O que NÃO pode ser inferido:** Não se pode inferir ranking de importância
de parâmetros de processo real. O ranking depende dos ranges demonstrativos
e dos defaults escolhidos. Alterando ranges ou métrica, o ranking pode mudar.

---

## Campo Térmico — Natureza Demonstrativa

O perfil térmico inicial utilizado é uma condição **puramente demonstrativa**
com bordas de Dirichlet fixas (T_left = 1700 K, T_right = 1400 K).

> [!WARNING]
> Este caso **não** representa um processo físico real de wafer.
> As temperaturas foram escolhidas para gerar um gradiente visível
> e demonstrar a funcionalidade dos solvers.
> Em processos reais de crescimento de cristais de silício (Czochralski,
> Float-Zone), os perfis térmicos são tridimensionais, dependem de geometria,
> radiação e convecção, e não podem ser representados por um caso 1D Dirichlet.

## Campo C — Proxy Adimensional

> [!WARNING]
> **NATUREZA DE C:** A variável C utilizada nos modelos difusivos é um
> **proxy adimensional** de heterogeneidade/defeitos. C **não** representa
> concentração física calibrada e **não** deve ser comparado quantitativamente
> com densidade real de defeitos em semicondutores.

A métrica `boundary_flux_proxy` foi adicionada para verificar qualitativamente
a condição Neumann no-flux nas fronteiras. Valores próximos de zero confirmam
que a implementação numérica está consistente com a condição de contorno
especificada (∂C/∂x = 0 nas extremidades).

## Análise de Sensibilidade — Detalhamento

### Metodologia
Os 5 parâmetros variados independentemente são:

| Parâmetro | Range de variação | Natureza |
|-----------|-------------------|----------|
| ΔT (gradiente térmico) | 100–400 K | demonstrativo |
| D₀ (pré-exponencial) | 1e-9–5e-8 m²/s | demonstrativo |
| Eₐ (energia de ativação) | 0.3–0.6 eV | demonstrativo |
| T_c (temperatura crítica) | 1400–1550 K | demonstrativo |
| σ_T (largura da fonte) | 25–100 K | demonstrativo |

### Resultados (demonstrativos)
- **D₀** e **Eₐ** são os parâmetros com maior sensibilidade normalizada,
  indicando que a difusividade (via Arrhenius) domina a heterogeneidade
  de C no range testado.
- **ΔT** tem sensibilidade intermediária — gradientes maiores redistribuem
  C e modulam o termo-fonte.
- **σ_T** e **T_c** têm sensibilidade menor, controlando a largura e
  posição da janela de geração de C.

### Interpretação
Estes resultados são **qualitativos e demonstrativos**. Servem para ilustrar
a capacidade da metodologia de identificar parâmetros influentes, mas
**não** devem ser usados para decisões de processo real.

### CSV Exportado
A tabela completa de resultados está disponível em:
`results/tables/sensitivity_results.csv`

Colunas: parameter, variation_index, variation_value, metric_name, metric_value.

---

## Governança

- 13 commits atômicos e semânticos.
- 21 testes unitários (≥17 exigidos).
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
6. Métodos de sensibilidade global (Sobol/Morris).
