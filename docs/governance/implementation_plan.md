# v0.4 Poisson Bridge Core Implementation Plan

This document refines the implementation plan for the v0.4 Poisson Bridge core following strict TDD principles, adhering to ADR-007 Accepted scope.

## v0.4 Effective Charge Closure — Required Equations

### theta
`θ(x,y) = [T(x,y) − T_ref] / ΔT_ref`

**Rules:**
- Se `T_ref=None`, usar `mean(T)`.
- Se `ΔT_ref=None`, usar `max(T) - min(T)`.
- Se `max(T) - min(T) == 0`, retornar `θ=0` sem divisão por zero.
- `θ` é adimensional.

### h(C_def)
`h(C_def) = C_def / C_sat`

**Rules:**
- `C_def` deve ser finito.
- `C_sat > 0`.
- `C_def` deve estar no intervalo `[0, C_sat]`.
- Fora do intervalo deve levantar `ValueError` por padrão.
- `h(C_def)` é adimensional e limitado em `[0,1]`.

### raw surface charge proxy
`σ_raw = q · N_ref · [1 + λT θ + λC h(C_def)]`

### mean subtraction
`δσ_eff = σ_raw − mean(σ_raw)`

### volumetric conversion
`δρ_eff = δσ_eff / t_eff`

**Rules:**
- `t_eff > 0`.
- `δσ_eff` tem média aproximadamente zero.
- `δρ_eff` tem média aproximadamente zero.
- `N_ref`, `λT`, `λC`, `t_eff` são *uncalibrated demonstrative/T3/T0*, não parâmetros físicos calibrados.

## v0.4 Poisson Solver — Minimal Demonstrative Scope

**Definition:**
- Resolver apenas caso 2D homogêneo demonstrativo.
- `ε` constante.
- Malha regular `dx`, `dy`.
- Condição de contorno Dirichlet homogênea como primeiro alvo.
- Equação implementada no caso mínimo: `∇²φ = −δρ_eff/ε`.
  *Nota:* Esta é apenas a simplificação homogênea da forma geral `∇·(ε∇φ) = −δρ_eff`.

**Method:**
- Jacobi ou Gauss-Seidel.
- `max_iter` explícito.
- `tolerance` explícita.
- Erro se não convergir.
- Validação de shape.
- Validação de `dx`, `dy`, `epsilon` positivos.
- Validação de finitude.

**Do not implement now:**
- Neumann.
- Periódico.
- `ε` variável.
- Geometria real de device.
- Poisson não linear.
- Auto-consistência `φ → occupancy → rho_eff`.

## Manufactured Solution Test

Usar:
`φ_exact(x,y) = sin(πx/Lx) sin(πy/Ly)`

`λ = (π/Lx)^2 + (π/Ly)^2`

`ρ(x,y) = ε · λ · φ_exact(x,y)`

Pois:
`∇²φ_exact = −λφ_exact`
`∇²φ = −ρ/ε`

**Criteria:**
- Bordas Dirichlet são zero.
- Erro L2 deve ficar abaixo de tolerância demonstrativa.
- Opcionalmente, erro deve reduzir em malha mais fina, se custo computacional permitir.

## TDD Execution Protocol

Sequência obrigatória:
1. Criar branch `feature/v0.4-poisson-bridge-core`.
2. Criar `tests/test_effective_charge.py`.
3. Criar `tests/test_poisson_solver_2d.py`.
4. Rodar testes alvo e confirmar falha por `ModuleNotFoundError` ou `ImportError` esperado.
5. Registrar evidência da falha no `walkthrough.md`.
6. Implementar `effective_charge.py`.
7. Rodar `tests/test_effective_charge.py` até verde.
8. Implementar `poisson_solver_2d.py`.
9. Rodar `tests/test_poisson_solver_2d.py` até verde.
10. Rodar suíte completa.
11. Só depois criar script `run_poisson_bridge.py`.
12. Só depois atualizar `generate_all_results.py`.
13. Só depois atualizar documentação.

## Required Public API

**effective_charge.py:**
- `compute_theta(T: np.ndarray, T_ref: float | None = None, delta_T_ref: float | None = None) -> np.ndarray`
- `h_cdef(C_def: np.ndarray, C_sat: float = 1.0) -> np.ndarray`
- `compute_delta_sigma_eff(C_def: np.ndarray, T: np.ndarray | None = None, params: EffectiveChargeParams | None = None) -> np.ndarray`
- `convert_sigma_to_rho(delta_sigma_eff: np.ndarray, t_eff: float) -> np.ndarray`
- `compute_delta_rho_eff(C_def: np.ndarray, T: np.ndarray | None = None, params: EffectiveChargeParams | None = None) -> np.ndarray`

**Dataclass:**
`EffectiveChargeParams`
Campos mínimos:
- `q`
- `N_ref`
- `lambda_T`
- `lambda_C`
- `C_sat`
- `t_eff`
- `T_ref`
- `delta_T_ref`

**poisson_solver_2d.py:**
- `solve_poisson_2d_demonstrative(rho: np.ndarray, dx: float, dy: float, epsilon: float, max_iter: int = 10000, tolerance: float = 1e-8) -> PoissonSolveResult`

**Dataclass:**
`PoissonSolveResult`
Campos mínimos:
- `phi`
- `iterations`
- `residual`
- `converged`

**Disclaimers in code:**
All new modules must contain docstrings noting:
- demonstrative only;
- uncalibrated;
- not predictive semiconductor electrostatics;
- no device-level claim;
- C_def remains dimensionless.

## Expected Final Artifacts

Outputs mínimos:
- `results/figures/poisson_bridge_potential.png`
- `results/tables/poisson_bridge_metrics.csv`
- `docs/release_notes/v0.4.0_draft.md`
- `docs/parameters_v0.4_candidates.md`

Métricas mínimas do CSV:
- `max_abs_delta_rho_eff`
- `mean_delta_rho_eff`
- `max_abs_phi`
- `solver_iterations`
- `solver_residual`
- `converged`
