# Parâmetros do MVP v0.1

> **NOTA:** A coluna "natureza" classifica cada parâmetro.
> Nenhum parâmetro demonstrativo deve ser apresentado como dado real de semicondutor.

## Tabela de Parâmetros

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

## Notas

1. Parâmetros classificados como **toy/demonstrativo** servem exclusivamente para
   demonstração da metodologia. Não devem ser citados como valores reais de
   semicondutores sem calibração experimental.

2. Parâmetros classificados como **físico aproximado** são baseados em ordens de
   grandeza da literatura, mas não representam valores calibrados para um material
   ou processo específico.

3. A variável C é **adimensional** e funciona como proxy de heterogeneidade/defeitos.
   Ver `docs/hipoteses_e_limitacoes.md` (L-01).
