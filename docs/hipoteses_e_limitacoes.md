# Hipóteses e Limitações

## Hipótese Central

Condições térmicas e difusivas idealizadas podem ser usadas como primeira
aproximação para estudar heterogeneidades em materiais semicondutores, servindo
como etapa inicial para conversas técnicas sobre defeitos, interfaces,
variabilidade e controle de processo em dispositivos quânticos de estado sólido.

## Hipóteses Operacionais

1. **Domínio 1D simplificado** é suficiente para demonstrar a metodologia
   de análise de heterogeneidades no escopo do MVP v0.1.

2. **Euler explícito** com verificação de estabilidade CFL é adequado para
   o regime de parâmetros utilizado (toy/demonstrativo).

3. **Difusividade Arrhenius** captura qualitativamente a dependência térmica
   da difusão em semicondutores, sem pretensão de calibração quantitativa.

4. **Termo-fonte gaussiano** modela qualitativamente a geração de
   heterogeneidades em janela crítica de temperatura.

## Limitações Fundamentais

### L-01: Natureza de C
A variável C é um **proxy adimensional** de heterogeneidade/defeitos.
- C **não** representa concentração física calibrada.
- C **não** deve ser comparado quantitativamente com densidade real de defeitos.
- Valores de C são relativos e servem para análise qualitativa de tendências.

### L-02: Sem Simulação Industrial
O MVP **não** simula fabricação industrial real de wafer.
Os parâmetros são demonstrativos ou fisicamente aproximados, não calibrados
com dados experimentais de processo.

### L-03: Sem Predição de Coerência Quântica
O MVP **não** prediz coerência quântica.
A relação entre heterogeneidades simuladas e propriedades quânticas requer
modelos de mecânica quântica fora do escopo deste trabalho.

### L-04: Sem Equivalência Direta
**Não** há equivalência direta entre solidificação metálica e fabricação
de semicondutores. A transferência é exclusivamente **metodológica**.

### L-05: Parâmetros Demonstrativos
Os parâmetros físicos utilizados são de natureza toy/demonstrativa ou
fisicamente aproximada. Consulte `docs/parameters.md` para classificação
detalhada de cada parâmetro.

### L-06: Condições de Contorno Simplificadas
- Térmico: Dirichlet (temperatura fixa nas extremidades)
- Difusivo: Neumann no-flux (fluxo zero nas extremidades)
- Condições mais realistas requerem modelagem específica do processo.

### L-07: 1D Apenas
O MVP v0.1 é exclusivamente 1D. Extensão 2D é stretch goal condicionado
à qualidade dos gates 1D.

## Separação Fato / Hipótese / Inferência / Limitação

| Tipo | Descrição |
|------|-----------|
| **Fato** | As equações de calor e difusão são matematicamente bem-postas para os parâmetros utilizados |
| **Hipótese** | A metodologia de análise de heterogeneidades é transferível entre domínios de materiais |
| **Inferência** | Gradientes térmicos elevados correlacionam-se com maior heterogeneidade de C (prudente, qualitativa) |
| **Limitação** | Qualquer extrapolação para dispositivos quânticos reais requer validação experimental |
