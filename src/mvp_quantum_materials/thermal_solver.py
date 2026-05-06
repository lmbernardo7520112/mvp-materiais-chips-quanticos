"""1D thermal solver using explicit Euler finite differences.

Solves: ∂T/∂t = α · ∂²T/∂x²
Boundary conditions: Dirichlet (fixed T at both ends).
Stability: enforced via CFL check before execution.
"""

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from mvp_quantum_materials.config import (
    ThermalConfig,
    compute_max_stable_dt_thermal,
    validate_stability,
)
from mvp_quantum_materials.domain import Domain1D


@dataclass
class ThermalResult:
    """Result container for the thermal solver.

    Attributes:
        T_final: Final temperature field [K].
        T_history: List of temperature snapshots over time.
        dt: Time step used [s].
        n_steps: Total number of time steps.
        times: Snapshot times [s].
    """

    T_final: npt.NDArray[np.float64]
    T_history: list[npt.NDArray[np.float64]]
    dt: float
    n_steps: int
    times: list[float]


def solve_thermal_1d(domain: Domain1D, config: ThermalConfig) -> ThermalResult:
    """Solve the 1D heat equation with explicit Euler.

    Args:
        domain: Computational domain.
        config: Thermal solver configuration.

    Returns:
        ThermalResult with final field and history.

    Raises:
        ValueError: If dt violates stability criterion.
    """
    dx = domain.dx
    dt_max = compute_max_stable_dt_thermal(dx, config.alpha, config.safety_factor)

    if config.dt_override is not None:
        dt = config.dt_override
    else:
        dt = dt_max

    validate_stability(dt, dt_max, "thermal_solver")

    n_steps = int(config.t_total / dt)
    if n_steps < 1:
        n_steps = 1

    # Initialize temperature field
    T = np.full(domain.nx, config.t_init)
    T[0] = config.t_left
    T[-1] = config.t_right

    # Snapshot interval
    snapshot_interval = max(1, n_steps // config.n_snapshots)
    history: list[npt.NDArray[np.float64]] = [T.copy()]
    times: list[float] = [0.0]

    r = config.alpha * dt / dx**2

    for step in range(1, n_steps + 1):
        T_new = T.copy()
        T_new[1:-1] = T[1:-1] + r * (T[2:] - 2.0 * T[1:-1] + T[:-2])

        # Enforce Dirichlet BCs
        T_new[0] = config.t_left
        T_new[-1] = config.t_right

        T = T_new

        if step % snapshot_interval == 0 or step == n_steps:
            history.append(T.copy())
            times.append(step * dt)

    return ThermalResult(
        T_final=T,
        T_history=history,
        dt=dt,
        n_steps=n_steps,
        times=times,
    )
