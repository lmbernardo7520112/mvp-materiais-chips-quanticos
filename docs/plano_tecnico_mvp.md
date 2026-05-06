# Plano Técnico — MVP v0.1

## Tema

"Modelagem termo-difusiva simplificada para análise de heterogeneidades
em material semicondutor idealizado."

## Equações Governantes

### Equação de Calor (1D simplificada)

```
∂T/∂t = α · ∂²T/∂x²
```

Condições de contorno: Dirichlet (T fixo nas extremidades).

### Equação Difusiva com Fonte

```
∂C/∂t = ∂/∂x [D(T) · ∂C/∂x] + S_C(T)
```

Condições de contorno: Neumann no-flux (∂C/∂x = 0 nas extremidades).

### Difusividade Arrhenius

```
D(T) = D₀ · exp(-Eₐ / (k_B · T))
```

### Termo-Fonte Gaussiano

```
S_C(T) = A_C · exp(-(T - T_c)² / (2·σ_T²))
```

## Método Numérico

- Discretização espacial: diferenças finitas centradas
- Avanço temporal: Euler explícito
- Estabilidade:
  - Térmico: dt ≤ safety_factor × dx² / (2 × α)
  - Difusivo: dt ≤ safety_factor × dx² / (2 × max(D(T)))

## Métricas de Heterogeneidade

1. Gradiente térmico máximo
2. Não-uniformidade térmica
3. Não-uniformidade de C
4. Índice de acúmulo local
5. Integral global de C
6. Ranking de sensibilidade paramétrica

## Análise de Sensibilidade

Variação de ≥5 parâmetros: ΔT (ou gradiente), D₀, Eₐ, T_c, σ_T/A_C.

## Transferência Metodológica

A transferência para materiais semicondutores é **exclusivamente metodológica**:
formulação física, solução numérica, análise de sensibilidade, métricas e governança.
Consulte `docs/hipoteses_e_limitacoes.md` para limites completos.
