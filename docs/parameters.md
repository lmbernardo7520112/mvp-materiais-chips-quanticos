# Parâmetros do MVP v0.1 / v0.2

> **NOTA:** A coluna "natureza" classifica cada parâmetro.
> Nenhum parâmetro demonstrativo deve ser apresentado como dado real de semicondutor.

## Tabela de Parâmetros — v0.1 (1D)

| Parâmetro | Símbolo | Unidade | Valor Default | Natureza | Justificativa |
|-----------|---------|---------|---------------|----------|---------------|
| Comprimento do domínio | L | m | 0.01 | configuração numérica | Escala representativa para demonstração 1D |
| Número de nós | nx | — | 101 | configuração numérica | Resolução adequada para Euler explícito |
| Difusividade térmica | α | m²/s | 8.8e-5 | físico aproximado | Ordem de grandeza do silício (~8.8e-5 m²/s a 300 K) |
| Temperatura esquerda (BC) | T_left | K | 1700 | toy/demonstrativo | Valor idealizado para demonstração de gradiente |
| Temperatura direita (BC) | T_right | K | 1400 | toy/demonstrativo | Valor idealizado para demonstração de gradiente |
| Temperatura inicial | T_init | K | 1500 | toy/demonstrativo | Média entre BCs para condição inicial |
| Tempo total | t_total | s | 1.0 | configuração numérica | Suficiente para observar evolução transiente |
| Fator de segurança CFL | safety_factor | — | 0.4 | configuração numérica | Garante estabilidade de Euler explícito (< 0.5) |
| Pré-exponencial de difusão | D₀ | m²/s | 1.0e-8 | toy/demonstrativo | Ordem de grandeza para difusão em sólidos |
| Energia de ativação | Eₐ | eV | 0.5 | toy/demonstrativo | Valor idealizado; silício real varia por espécie |
| Constante de Boltzmann | k_B | eV/K | 8.617e-5 | físico (constante) | Valor CODATA |
| Temperatura crítica | T_c | K | 1500 | toy/demonstrativo | Centro da janela de geração de heterogeneidades |
| Largura da janela | σ_T | K | 50 | toy/demonstrativo | Controla extensão da região sensível |
| Amplitude da fonte | A_C | 1/s | 1.0 | toy/demonstrativo | Magnitude da taxa de geração de C |
| Concentração inicial | C_init | — (adimensional) | 0.0 | configuração numérica | Campo C inicia zerado |

## Tabela de Parâmetros — v0.2 (2D)

| Parâmetro | Símbolo | Unidade | Valor Default | Natureza | Justificativa |
|-----------|---------|---------|---------------|----------|---------------|
| Comprimento x do domínio | Lx | m | 0.01 | configuração numérica | Escala representativa para demonstração 2D |
| Comprimento y do domínio | Ly | m | 0.01 | configuração numérica | Domínio quadrado para simplificação |
| Número de nós x | nx | — | 51 | configuração numérica | Resolução adequada para Euler 2D explícito |
| Número de nós y | ny | — | 51 | configuração numérica | Grade uniforme quadrada |
| Temperatura de contorno 2D | t_boundary | K | 1400 | toy/demonstrativo | Dirichlet homogêneo nas 4 bordas |
| Tempo total 2D | t_total | s | 0.01 | configuração numérica | Mais curto que 1D (dt 2D é menor) |
| Fator de segurança CFL 2D | safety_factor | — | 0.4 | configuração numérica | Mesmo fator da versão 1D |

### Parâmetros de Convergência

| Parâmetro | Símbolo | Unidade | Valor Default | Natureza | Justificativa |
|-----------|---------|---------|---------------|----------|---------------|
| Malhas de refinamento | nx_values | — | [11, 21, 41, 81] | configuração numérica | Sequência para análise de convergência |
| Tempo final convergência | t_final | s | 0.001 | configuração numérica | Suficiente para decaimento mensurável |
| Difusividade (convergência) | α | m²/s | 8.8e-5 | físico aproximado | Mesmo valor do solver térmico |

## Notas

1. Parâmetros classificados como **toy/demonstrativo** servem exclusivamente para
   demonstração da metodologia. Não devem ser citados como valores reais de
   semicondutores sem calibração experimental.

2. Parâmetros classificados como **físico aproximado** são baseados em ordens de
   grandeza da literatura, mas não representam valores calibrados para um material
   ou processo específico.

3. A variável C é **adimensional** e funciona como proxy de heterogeneidade/defeitos.
   Ver `docs/hipoteses_e_limitacoes.md` (L-01).

4. Os parâmetros 2D seguem a mesma política dos 1D: valores são
   **demonstrativos** e não representam um wafer ou processo real.
   O domínio 2D não é uma fatia de wafer — é uma abstração numérica.
