# Parâmetros do MVP v0.1 / v0.2 / v0.3

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

2. Parâmetros classificados como **físico aproximado** ou **literature-inspired**
   são baseados em ordens de grandeza da literatura, mas não representam valores
   calibrados para um material ou processo específico.

3. A variável C (v0.1) e C_def (v0.3) são **adimensionais** e funcionam como
   proxies de heterogeneidade/defeitos.
   Ver `docs/hipoteses_e_limitacoes.md` (L-01).

4. Os parâmetros 2D seguem a mesma política dos 1D: valores são
   **demonstrativos** e não representam um wafer ou processo real.

5. **v0.3:** Parâmetros D₀_def, E_D, A_G, T_G, σ_G, A_R, E_R foram curados a
   partir de `docs/parameters_v0.3_candidates.md`. A curadoria de parâmetros
   reais de defeitos/traps em Si requer trabalho futuro (ver technical_debt.md).

## Tabela de Parâmetros — v0.3 (Defect-like Reaction-Diffusion)

| Parâmetro | Símbolo | Unidade | Valor Default | Natureza | Justificativa |
|-----------|---------|---------|---------------|----------|---------------|
| Pré-exponencial de difusão defect | D₀_def | m²/s | 1.0e-4 | literature-inspired | Vacancy diffusion in Si: D₀ ≈ 1e-5 to 1e-3 (Sinno, Brown) |
| Energia de migração | E_D | eV | 0.4 | literature-inspired | Vacancy migration in Si: E_m ≈ 0.2–0.5 eV (Sinno 2000) |
| Amplitude de geração | A_G | 1/s | 1.0 | toy/demonstrativo | Sem fonte; ajustado para efeito visível |
| Temperatura central de geração | T_G | K | 1100 | literature-inspired | Nucleação de voids ≈ 1100°C (Voronkov 1999) |
| Largura da janela de geração | σ_G | K | 100 | toy/demonstrativo | Sem fonte; ajustado para janela suave |
| Amplitude de recombinação | A_R | 1/s | 10.0 | toy/demonstrativo | Ajustado para balanço com G |
| Energia de recombinação | E_R | eV | 0.6 | literature-inspired | Barreira de recombinação ≈ 0.3–1.0 eV (Sinno) |
| Concentração de saturação | C_sat | — (adim.) | 1.0 | matemático | Limite superior de C_def |
| C_def inicial | C_def_init | — (adim.) | 0.0 | configuração numérica | Campo C_def inicia zerado |

