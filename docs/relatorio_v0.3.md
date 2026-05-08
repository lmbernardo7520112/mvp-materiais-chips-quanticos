# Relatório Técnico — v0.3 Defect-like Reaction-Diffusion

> **Data:** 2026-05-08
> **Versão:** v0.3.0 (draft)
> **Autor:** Staff Research Software Engineer (AI-assisted)

---

## 1. Objetivo

Implementar a primeira camada material do projeto: uma variável
adimensional C_def(x,y,t) governada por dinâmica de reaction-diffusion
termicamente ativada.

## 2. Equação Governante

```
∂C_def/∂t = ∇·(D(T)∇C_def) + G(T)(1 − C_def/C_sat) − R(T)·C_def
```

- D(T) = D₀·exp(−E_D/(k_B·T)) — Arrhenius diffusivity
- G(T) = A_G·exp(−(T−T_G)²/(2σ_G²)) — Gaussian generation window
- R(T) = A_R·exp(−E_R/(k_B·T)) — Arrhenius recombination

## 3. Implementação

| Componente | Arquivo | Status |
|------------|---------|--------|
| Cinética D(T), G(T), R(T) | `defect_kinetics.py` | ✅ Implementado |
| Estabilidade | `defect_stability.py` | ✅ Implementado |
| Solver 2D | `defect_solver_2d.py` | ✅ Implementado |
| Métricas | `defect_metrics.py` | ✅ Implementado |
| Plot C_def | `plots.py` | ✅ Adicionado |
| CLI | `run_defect_2d.py` | ✅ Criado |
| Generate all | `generate_all_results.py` | ✅ Atualizado |

## 4. Parâmetros (Toy/Demonstrativos)

| Parâmetro | Valor | Natureza |
|-----------|-------|----------|
| D₀ | 1.0e-4 m²/s | Literature-inspired |
| E_D | 0.4 eV | Literature-inspired |
| A_G | 1.0 1/s | Toy/demonstrative |
| T_G | 1100 K | Literature-inspired |
| σ_G | 100 K | Toy/demonstrative |
| A_R | 10.0 1/s | Toy/demonstrative |
| E_R | 0.6 eV | Literature-inspired |
| C_sat | 1.0 | Mathematical |

## 5. Artefatos Gerados

### Figuras (7+ total)
- `defect_2d_final.png` — C_def(x,y) contour (v0.3)
- `thermal_2d_final.png` — T(x,y) contour (v0.2)
- `convergence_analysis.png` (v0.2)
- `thermal_1d_evolution.png` (v0.1)
- `diffusion_1d_evolution.png` (v0.1)
- `sensitivity_analysis.png` (v0.1)
- `sensitivity_ranking.png` (v0.1)

### CSVs (4 total)
- `defect_metrics.csv` — proxy metrics (v0.3)
- `defect_final_snapshot.csv` — C_def final for future v0.4 (v0.3)
- `convergence_results.csv` (v0.2)
- `sensitivity_results.csv` (v0.1)

## 6. Limitações Explícitas

- C_def é **adimensional** — não é concentração física calibrada.
- Parâmetros são **toy/demonstrativos** salvo curadoria futura.
- O modelo **NÃO** prediz:
  - concentração real de defeitos em silício
  - charge noise
  - coerência de qubits
  - fidelidade de portas quânticas
  - qualidade de wafer
- **NÃO** foi implementado:
  - Poisson (∇·(ε∇φ) = −ρ_eff)
  - Schrödinger
  - TCAD/QTCAD
  - ρ_eff
  - Phase-field
  - Czochralski real

## 7. Regressão

- `thermal_solver.py`: zero diff vs main
- `diffusion_solver.py`: zero diff vs main
- Todos os 56 testes v0.1/v0.2 preservados
- Novos testes v0.3 adicionados

## 8. Preparação para v0.4

C_def_final(x,y) está exportado em `defect_final_snapshot.csv`.
A futura v0.4 poderá usar:

```
ρ_eff(x,y) = q_eff · C_def(x,y)
∇·(ε∇φ) = −ρ_eff
```

Essa interface **não foi implementada** na v0.3.
