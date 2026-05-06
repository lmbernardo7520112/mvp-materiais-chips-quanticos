"""1D diffusion solver with Arrhenius diffusivity and Gaussian source.

Solves: ∂C/∂t = ∂/∂x [D(T) · ∂C/∂x] + S_C(T)
Boundary conditions: Neumann no-flux (∂C/∂x = 0 at both ends).
Diffusivity: D(T) = D₀ · exp(-Eₐ / (k_B · T))
Source: S_C(T) = A_C · exp(-(T - T_c)² / (2·σ_T²))

LIMITATION: C is an adimensional proxy for heterogeneity/defects.
C does NOT represent calibrated physical concentration.
"""

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from mvp_quantum_materials.config import (
    BOLTZMANN_EV,
    DiffusionConfig,
    compute_max_stable_dt_diffusion,
    validate_stability,
)
from mvp_quantum_materials.domain import Domain1D


@dataclass
class DiffusionResult:
    """Result container for the diffusion solver.

    Attributes:
        C_final: Final concentration field (adimensional proxy).
        C_history: List of concentration snapshots.
        dt: Time step used [s].
        n_steps: Total time steps.
        times: Snapshot times [s].
    """

    C_final: npt.NDArray[np.float64]
    C_history: list[npt.NDArray[np.float64]]
    dt: float
    n_steps: int
    times: list[float]


def arrhenius_diffusivity(
    temperature: float | npt.NDArray[np.float64],
    d0: float,
    ea: float,
) -> float | npt.NDArray[np.float64]:
    """Compute Arrhenius diffusivity D(T) = D₀ · exp(-Eₐ / (k_B · T)).

    Args:
        temperature: Temperature [K]. Scalar or array.
        d0: Pre-exponential factor [m²/s].
        ea: Activation energy [eV].

    Returns:
        Diffusivity [m²/s].
    """
    return d0 * np.exp(-ea / (BOLTZMANN_EV * temperature))


def thermal_source(
    temperature: npt.NDArray[np.float64],
    a_c: float,
    t_critical: float,
    sigma_t: float,
) -> npt.NDArray[np.float64]:
    """Compute Gaussian thermal source S_C(T).

    S_C(T) = A_C · exp(-(T - T_c)² / (2·σ_T²))

    Args:
        temperature: Temperature field [K].
        a_c: Source amplitude [1/s].
        t_critical: Critical temperature [K].
        sigma_t: Width of Gaussian [K].

    Returns:
        Source term array (non-negative).
    """
    return a_c * np.exp(-((temperature - t_critical) ** 2) / (2.0 * sigma_t**2))


def solve_diffusion_1d(
    domain: Domain1D,
    t_field: npt.NDArray[np.float64],
    config: DiffusionConfig,
) -> DiffusionResult:
    """Solve 1D diffusion equation with Arrhenius and source.

    Args:
        domain: Computational domain.
        t_field: Temperature field [K] (assumed steady for diffusion).
        config: Diffusion configuration.

    Returns:
        DiffusionResult with final field and history.

    Raises:
        ValueError: If dt violates stability or C becomes non-finite.
    """
    dx = domain.dx

    # Compute diffusivity field
    d_field = arrhenius_diffusivity(t_field, config.d0, config.ea)
    d_max = float(np.max(d_field))

    dt_max = compute_max_stable_dt_diffusion(dx, d_max, config.safety_factor)

    if config.dt_override is not None:
        dt = config.dt_override
    else:
        dt = dt_max

    validate_stability(dt, dt_max, "diffusion_solver")

    n_steps = int(config.t_total / dt)
    if n_steps < 1:
        n_steps = 1

    # Initialize concentration field
    C = np.full(domain.nx, config.c_init)

    # Source term (constant in time since T is steady)
    source = thermal_source(t_field, config.a_c, config.t_critical, config.sigma_t)

    # Snapshot management
    snapshot_interval = max(1, n_steps // config.n_snapshots)
    history: list[npt.NDArray[np.float64]] = [C.copy()]
    times: list[float] = [0.0]

    for step in range(1, n_steps + 1):
        C_new = C.copy()

        # Interior: ∂/∂x [D(T) · ∂C/∂x] using central differences
        # D at half-points
        d_right = 0.5 * (d_field[1:-1] + d_field[2:])
        d_left = 0.5 * (d_field[1:-1] + d_field[:-2])

        flux_right = d_right * (C[2:] - C[1:-1]) / dx
        flux_left = d_left * (C[1:-1] - C[:-2]) / dx

        diffusion_term = (flux_right - flux_left) / dx
        C_new[1:-1] = C[1:-1] + dt * (diffusion_term + source[1:-1])

        # Neumann no-flux BCs: ∂C/∂x = 0 at boundaries
        C_new[0] = C_new[1]
        C_new[-1] = C_new[-2]

        # Check finiteness — fail loud, no silent clipping
        if not np.all(np.isfinite(C_new)):
            raise ValueError(
                f"Non-finite values detected in C at step {step}. "
                f"This indicates numerical instability. "
                f"dt={dt:.6e}, dx={dx:.6e}, D_max={d_max:.6e}"
            )

        C = C_new

        if step % snapshot_interval == 0 or step == n_steps:
            history.append(C.copy())
            times.append(step * dt)

    return DiffusionResult(
        C_final=C,
        C_history=history,
        dt=dt,
        n_steps=n_steps,
        times=times,
    )
