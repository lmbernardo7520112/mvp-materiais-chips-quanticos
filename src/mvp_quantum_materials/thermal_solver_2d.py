"""2D thermal solver using explicit Euler finite differences.

Solves: ∂T/∂t = α · (∂²T/∂x² + ∂²T/∂y²)
Boundary conditions: Dirichlet (fixed T on all four edges).
Stability: enforced via CFL check before execution.

Note:
    This solver is demonstrative — it does not simulate real wafer processing.
    Domain is a rectangular uniform grid.
"""

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from mvp_quantum_materials.config import (
    compute_max_stable_dt_thermal_2d,
    validate_stability,
)
from mvp_quantum_materials.domain import Domain2D


@dataclass
class ThermalResult2D:
    """Result container for the 2D thermal solver.

    Attributes:
        T_final: Final temperature field [K], shape (nx, ny).
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


def solve_thermal_2d(
    domain: Domain2D,
    T_init: npt.NDArray[np.float64],
    alpha: float,
    t_total: float,
    t_boundary: float,
    safety_factor: float = 0.4,
    dt_override: float | None = None,
    n_snapshots: int = 10,
) -> ThermalResult2D:
    """Solve the 2D heat equation with explicit Euler.

    Args:
        domain: 2D computational domain.
        T_init: Initial temperature field, shape (nx, ny) [K].
        alpha: Thermal diffusivity [m²/s].
        t_total: Total simulation time [s].
        t_boundary: Dirichlet boundary temperature [K] (all edges).
        safety_factor: CFL safety factor (< 0.5).
        dt_override: If set, use this dt. Solver validates stability.
        n_snapshots: Number of time snapshots to store.

    Returns:
        ThermalResult2D with final field and history.

    Raises:
        ValueError: If dt violates stability criterion.

    Note:
        This is a demonstrative solver — not calibrated for real materials.
    """
    dx = domain.dx
    dy = domain.dy

    dt_max = compute_max_stable_dt_thermal_2d(dx, dy, alpha, safety_factor)

    if dt_override is not None:
        dt = dt_override
    else:
        dt = dt_max

    validate_stability(dt, dt_max, "thermal_solver_2d")

    n_steps = max(1, int(t_total / dt))

    # Initialize
    T = T_init.copy().astype(np.float64)

    # Enforce Dirichlet BCs on initial field
    T[0, :] = t_boundary
    T[-1, :] = t_boundary
    T[:, 0] = t_boundary
    T[:, -1] = t_boundary

    # Precompute coefficients
    rx = alpha * dt / dx**2
    ry = alpha * dt / dy**2

    # Snapshot storage
    snapshot_interval = max(1, n_steps // n_snapshots)
    history: list[npt.NDArray[np.float64]] = [T.copy()]
    times: list[float] = [0.0]

    for step in range(1, n_steps + 1):
        T_new = T.copy()

        # Interior update: explicit Euler with centered differences
        T_new[1:-1, 1:-1] = (
            T[1:-1, 1:-1]
            + rx * (T[2:, 1:-1] - 2.0 * T[1:-1, 1:-1] + T[:-2, 1:-1])
            + ry * (T[1:-1, 2:] - 2.0 * T[1:-1, 1:-1] + T[1:-1, :-2])
        )

        # Enforce Dirichlet BCs
        T_new[0, :] = t_boundary
        T_new[-1, :] = t_boundary
        T_new[:, 0] = t_boundary
        T_new[:, -1] = t_boundary

        T = T_new

        if step % snapshot_interval == 0 or step == n_steps:
            history.append(T.copy())
            times.append(step * dt)

    return ThermalResult2D(
        T_final=T,
        T_history=history,
        dt=dt,
        n_steps=n_steps,
        times=times,
    )
