"""2D defect reaction-diffusion solver using explicit Euler.

Solves: ∂C_def/∂t = ∇·(D(T)∇C_def) + G(T)(1 − C_def/C_sat) − R(T)·C_def

Boundary conditions: Neumann no-flux (∂C_def/∂n = 0) on all edges.
Coupling: One-way T(x,y) → C_def(x,y,t). T is static during integration.
Stability: enforced via CFL-like guard before execution.

Note:
    This solver is demonstrative — C_def is an adimensional proxy,
    not a calibrated physical defect concentration.
    Equation form is structurally inspired by crystal growth literature
    (Dornberger 2001, Brown 1994); parameter values are toy/demonstrative.
"""

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from mvp_quantum_materials.defect_kinetics import (
    defect_diffusivity,
    defect_generation,
    defect_recombination,
)
from mvp_quantum_materials.defect_stability import (
    compute_max_stable_dt_defect_2d,
    validate_defect_stability_2d,
)
from mvp_quantum_materials.domain import Domain2D

# Default toy/demonstrative parameters (see docs/parameters_v0.3_candidates.md)
_DEFAULT_D0 = 1.0e-4  # m²/s — literature-inspired order of magnitude
_DEFAULT_E_D = 0.4  # eV — literature-inspired order of magnitude
_DEFAULT_A_G = 1.0  # 1/s — toy/demonstrative
_DEFAULT_T_G = 1100.0  # K — literature-inspired (Voronkov 1999)
_DEFAULT_SIGMA_G = 100.0  # K — toy/demonstrative
_DEFAULT_A_R = 10.0  # 1/s — toy/demonstrative
_DEFAULT_E_R = 0.6  # eV — literature-inspired order of magnitude
_DEFAULT_C_SAT = 1.0  # adimensional


@dataclass
class DefectResult2D:
    """Result container for the 2D defect solver.

    Attributes:
        C_def_final: Final defect-like field, shape (nx, ny). Adimensional.
        C_def_history: List of C_def snapshots over time.
        dt: Time step used [s].
        n_steps: Total number of time steps.
        times: Snapshot times [s].
    """

    C_def_final: npt.NDArray[np.float64]
    C_def_history: list[npt.NDArray[np.float64]]
    dt: float
    n_steps: int
    times: list[float]


def solve_defect_2d(
    domain: Domain2D,
    T_field: npt.NDArray[np.float64],
    t_total: float,
    C_def_init: npt.NDArray[np.float64] | None = None,
    D0: float = _DEFAULT_D0,
    E_D: float = _DEFAULT_E_D,
    A_G: float = _DEFAULT_A_G,
    T_G: float = _DEFAULT_T_G,
    sigma_G: float = _DEFAULT_SIGMA_G,
    A_R: float = _DEFAULT_A_R,
    E_R: float = _DEFAULT_E_R,
    C_sat: float = _DEFAULT_C_SAT,
    safety_factor: float = 0.4,
    dt_override: float | None = None,
    n_snapshots: int = 10,
) -> DefectResult2D:
    """Solve the 2D defect reaction-diffusion equation.

    ∂C_def/∂t = ∇·(D(T)∇C_def) + G(T)(1 − C_def/C_sat) − R(T)·C_def

    Args:
        domain: 2D computational domain.
        T_field: Static temperature field, shape (nx, ny) [K].
        t_total: Total simulation time [s].
        C_def_init: Initial defect field (nx, ny). Default: zeros.
        D0: Diffusivity pre-exponential [m²/s]. Toy/demonstrative.
        E_D: Migration energy [eV]. Toy/demonstrative.
        A_G: Generation amplitude [1/s]. Toy/demonstrative.
        T_G: Generation center temperature [K]. Toy/demonstrative.
        sigma_G: Generation window width [K]. Toy/demonstrative.
        A_R: Recombination pre-exponential [1/s]. Toy/demonstrative.
        E_R: Recombination energy [eV]. Toy/demonstrative.
        C_sat: Saturation value (adimensional, default 1.0).
        safety_factor: CFL safety factor.
        dt_override: If set, use this dt. Solver validates stability.
        n_snapshots: Number of time snapshots to store.

    Returns:
        DefectResult2D with final field and history.

    Raises:
        ValueError: If dt violates stability criterion.

    Note:
        Demonstrative solver — C_def is adimensional, not calibrated.
        Parameters are toy/demonstrative unless curated from literature.
    """
    dx = domain.dx
    dy = domain.dy
    nx = domain.nx
    ny = domain.ny

    # Precompute kinetics fields (T is static)
    D_field = np.zeros((nx, ny))
    G_field = np.zeros((nx, ny))
    R_field = np.zeros((nx, ny))

    for i in range(nx):
        for j in range(ny):
            T_ij = float(T_field[i, j])
            D_field[i, j] = defect_diffusivity(T_ij, D0, E_D)
            G_field[i, j] = defect_generation(T_ij, A_G, T_G, sigma_G)
            R_field[i, j] = defect_recombination(T_ij, A_R, E_R)

    D_max = float(np.max(D_field))
    R_max = float(np.max(R_field))
    G_max = float(np.max(G_field))

    # Stability guard
    dt_max = compute_max_stable_dt_defect_2d(
        dx,
        dy,
        D_max,
        R_max,
        G_max,
        C_sat,
        safety_factor,
    )

    if dt_override is not None:
        dt = dt_override
    else:
        dt = dt_max

    validate_defect_stability_2d(dt, dt_max)

    n_steps = max(1, int(t_total / dt))

    # Initialize C_def
    if C_def_init is not None:
        C = C_def_init.copy().astype(np.float64)
    else:
        C = np.zeros((nx, ny), dtype=np.float64)

    # Snapshot storage
    snapshot_interval = max(1, n_steps // n_snapshots)
    history: list[npt.NDArray[np.float64]] = [C.copy()]
    times: list[float] = [0.0]

    for step in range(1, n_steps + 1):
        C_new = C.copy()

        # Interior update: diffusion (centered differences) + reaction
        for i in range(1, nx - 1):
            for j in range(1, ny - 1):
                # Diffusion: ∇·(D∇C) with variable D
                D_ip = 0.5 * (D_field[i + 1, j] + D_field[i, j])
                D_im = 0.5 * (D_field[i - 1, j] + D_field[i, j])
                D_jp = 0.5 * (D_field[i, j + 1] + D_field[i, j])
                D_jm = 0.5 * (D_field[i, j - 1] + D_field[i, j])

                diff_x = (D_ip * (C[i + 1, j] - C[i, j]) - D_im * (C[i, j] - C[i - 1, j])) / dx**2
                diff_y = (D_jp * (C[i, j + 1] - C[i, j]) - D_jm * (C[i, j] - C[i, j - 1])) / dy**2

                diffusion = diff_x + diff_y

                # Generation with saturation
                generation = G_field[i, j] * (1.0 - C[i, j] / C_sat)

                # Recombination (first-order)
                recombination = R_field[i, j] * C[i, j]

                C_new[i, j] = C[i, j] + dt * (diffusion + generation - recombination)

        # Neumann no-flux BCs: copy from nearest interior
        C_new[0, :] = C_new[1, :]
        C_new[-1, :] = C_new[-2, :]
        C_new[:, 0] = C_new[:, 1]
        C_new[:, -1] = C_new[:, -2]

        # Enforce boundedness [0, C_sat]
        np.clip(C_new, 0.0, C_sat, out=C_new)

        C = C_new

        if step % snapshot_interval == 0 or step == n_steps:
            history.append(C.copy())
            times.append(step * dt)

    return DefectResult2D(
        C_def_final=C,
        C_def_history=history,
        dt=dt,
        n_steps=n_steps,
        times=times,
    )
