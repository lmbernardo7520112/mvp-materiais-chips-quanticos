# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # MVP Quantum Materials — v0.2 Demonstration
#
# > **NOTA:** Este notebook é demonstrativo. Os parâmetros são
# > toy/idealizados e os resultados não podem ser citados como predições
# > físicas de semicondutores reais.
#
# Este notebook demonstra as capacidades adicionadas na v0.2.0:
# - Domínio computacional 2D (`Domain2D`)
# - Solver térmico 2D (Euler explícito, Dirichlet BCs)
# - Análise de convergência com solução manufaturada
#
# Todas as funções são importadas do pacote `mvp_quantum_materials`.
# Nenhuma lógica científica nova é definida aqui.

# %% [markdown]
# ## 1. Setup

# %%
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from mvp_quantum_materials.convergence import run_convergence_analysis  # noqa: E402
from mvp_quantum_materials.domain import Domain2D  # noqa: E402
from mvp_quantum_materials.thermal_solver_2d import solve_thermal_2d  # noqa: E402

# %% [markdown]
# ## 2. Domain2D — Domínio Computacional 2D
#
# O `Domain2D` define um domínio retangular estruturado com grade uniforme.
# Ele é imutável (frozen dataclass) e valida automaticamente os parâmetros.

# %%
domain = Domain2D(Lx=0.01, Ly=0.01, nx=51, ny=51)

print(f"Lx = {domain.Lx} m")
print(f"Ly = {domain.Ly} m")
print(f"nx = {domain.nx}, ny = {domain.ny}")
print(f"dx = {domain.dx:.6e} m")
print(f"dy = {domain.dy:.6e} m")
print(f"x shape: {domain.x.shape}")
print(f"y shape: {domain.y.shape}")

# %% [markdown]
# ## 3. Solver Térmico 2D
#
# A equação do calor 2D é resolvida com Euler explícito e diferenças
# finitas centradas:
#
# dT/dt = alpha * (d²T/dx² + d²T/dy²)
#
# O passo de tempo é calculado automaticamente para
# garantir estabilidade (CFL 2D).
# BCs: Dirichlet homogêneo nas 4 bordas.

# %%
# Parâmetros demonstrativos (NÃO calibrados)
alpha = 8.8e-5  # m²/s — ordem de grandeza do Si
t_total = 0.01  # s
T_init_value = 1500.0  # K — demonstrativo
T_boundary = 1400.0  # K — demonstrativo
safety_factor = 0.4

# Condição inicial: uniforme no interior
T0 = np.full((domain.nx, domain.ny), T_init_value)

# Resolver — o solver aplica BCs automaticamente
result = solve_thermal_2d(
    domain=domain,
    T_init=T0,
    alpha=alpha,
    t_total=t_total,
    t_boundary=T_boundary,
    safety_factor=safety_factor,
)

print(f"dt usado: {result.dt:.6e} s")
print(f"n_steps: {result.n_steps}")
print(f"T_final shape: {result.T_final.shape}")
print(f"T_final min: {result.T_final.min():.1f} K")
print(f"T_final max: {result.T_final.max():.1f} K")
print(f"Snapshots: {len(result.T_history)}")

# %% [markdown]
# ### Visualização do Campo Térmico 2D Final
#
# > **AVISO:** Resultado demonstrativo — não calibrado para nenhum material real.

# %%
fig, ax = plt.subplots(figsize=(8, 6))
c = ax.contourf(domain.x, domain.y, result.T_final.T, levels=50, cmap="inferno")
fig.colorbar(c, ax=ax, label="Temperature [K]")
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_title("Campo térmico 2D final — demonstrativo, não calibrado")
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig("results/figures/notebook_thermal_2d.png", dpi=150)
print("Figura salva: results/figures/notebook_thermal_2d.png")
plt.close()

# %% [markdown]
# ## 4. Análise de Convergência
#
# A convergência é verificada contra uma solução analítica manufaturada:
#
# T(x,y,t) = sin(pi*x/Lx) * sin(pi*y/Ly)
#           * exp(-alpha*pi²*(1/Lx² + 1/Ly²)*t)
#
# O erro (L2 e L∞) diminui com o refinamento.
# A ordem observada confirma consistência com
# a discretização de 2ª ordem.

# %%
results = run_convergence_analysis(
    nx_values=[11, 21, 41],
    alpha=8.8e-5,
    Lx=0.01,
    Ly=0.01,
    t_final=0.001,
    safety_factor=0.4,
)

print(f"{'nx':>4}  {'dx':>12}  {'error_l2':>12}  {'observed_order':>15}")
print("-" * 50)
for r in results:
    order = f"{r['observed_order']:.2f}" if r["observed_order"] is not None else "—"
    print(f"{r['nx']:4d}  {r['dx']:12.6e}  {r['error_l2']:12.6e}  {order:>15}")

# %% [markdown]
# ### Gráfico de Convergência

# %%
dx_vals = [r["dx"] for r in results]
l2_vals = [r["error_l2"] for r in results]
linf_vals = [r["error_linf"] for r in results]

fig, ax = plt.subplots(figsize=(8, 6))
ax.loglog(dx_vals, l2_vals, "o-", label="Error L2")
ax.loglog(dx_vals, linf_vals, "s-", label="Error L∞")

# Referência O(dx²)
dx_ref = np.array(dx_vals)
scale = 0.5 * (dx_ref / dx_ref[0]) ** 2 * l2_vals[0]
ax.loglog(dx_ref, scale, "--", color="gray", label="O(dx²) ref")

ax.set_xlabel("dx [m]")
ax.set_ylabel("Error")
ax.set_title("Convergence Analysis — demonstrativo")
ax.legend()
ax.grid(True, which="both", ls="--", alpha=0.5)
plt.tight_layout()
plt.savefig("results/figures/notebook_convergence.png", dpi=150)
print("Figura salva: results/figures/notebook_convergence.png")
plt.close()

# %% [markdown]
# ## 5. Limitações
#
# - Todos os parâmetros são **toy/demonstrativos**
# - C permanece **proxy adimensional**
# - O domínio 2D **não é uma fatia de wafer real**
# - **Não existe** eletrostática, defeitos, ou confinamento quântico
# - Resultados **não podem** ser citados como predições físicas
# - O solver é **explícito** (CFL limita dt para malhas finas)
#
# Este notebook serve como demonstração reproduzível da infraestrutura
# computacional. A evolução científica continua no roadmap ADR-005.
