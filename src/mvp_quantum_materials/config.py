"""Configuration dataclasses and physical constants.

Centralizes all configuration, constants, and stability checks.
No magic numbers allowed outside this module.
"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Physical Constants
# ---------------------------------------------------------------------------

BOLTZMANN_EV: float = 8.617333262e-5  # eV/K (CODATA 2018)

# ---------------------------------------------------------------------------
# Configuration Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ThermalConfig:
    """Configuration for the 1D thermal solver.

    Attributes:
        alpha: Thermal diffusivity [m²/s].
        t_left: Left boundary temperature (Dirichlet) [K].
        t_right: Right boundary temperature (Dirichlet) [K].
        t_init: Initial temperature [K].
        t_total: Total simulation time [s].
        safety_factor: CFL safety factor (must be < 0.5 for stability).
        dt_override: If set, use this dt instead of auto-calculated.
            Solver will still validate stability.
        n_snapshots: Number of time snapshots to store in history.
    """

    alpha: float = 8.8e-5
    t_left: float = 1700.0
    t_right: float = 1400.0
    t_init: float = 1500.0
    t_total: float = 1.0
    safety_factor: float = 0.4
    dt_override: float | None = None
    n_snapshots: int = 10


@dataclass(frozen=True)
class DiffusionConfig:
    """Configuration for the 1D diffusion solver with Arrhenius and source.

    Attributes:
        d0: Pre-exponential diffusion coefficient [m²/s].
        ea: Activation energy [eV].
        t_critical: Critical temperature for source term [K].
        sigma_t: Width of Gaussian source term [K].
        a_c: Amplitude of source term [1/s].
        c_init: Initial concentration (adimensional proxy).
        t_total: Total simulation time [s].
        safety_factor: CFL safety factor (must be < 0.5).
        dt_override: If set, use this dt. Solver validates stability.
        n_snapshots: Number of time snapshots to store.
    """

    d0: float = 1.0e-8
    ea: float = 0.5
    t_critical: float = 1500.0
    sigma_t: float = 50.0
    a_c: float = 1.0
    c_init: float = 0.0
    t_total: float = 1.0
    safety_factor: float = 0.4
    dt_override: float | None = None
    n_snapshots: int = 10


# ---------------------------------------------------------------------------
# Stability Functions
# ---------------------------------------------------------------------------


def compute_max_stable_dt_thermal(dx: float, alpha: float, safety_factor: float) -> float:
    """Compute maximum stable dt for explicit Euler thermal solver.

    Formula: dt_max = safety_factor * dx² / (2 * alpha)

    Args:
        dx: Grid spacing [m].
        alpha: Thermal diffusivity [m²/s].
        safety_factor: Safety factor (< 0.5).

    Returns:
        Maximum stable time step [s].
    """
    return safety_factor * dx**2 / (2.0 * alpha)


def compute_max_stable_dt_diffusion(dx: float, d_max: float, safety_factor: float) -> float:
    """Compute maximum stable dt for explicit Euler diffusion solver.

    Formula: dt_max = safety_factor * dx² / (2 * max(D(T)))

    Args:
        dx: Grid spacing [m].
        d_max: Maximum diffusivity in the domain [m²/s].
        safety_factor: Safety factor (< 0.5).

    Returns:
        Maximum stable time step [s].
    """
    if d_max <= 0.0:
        return float("inf")
    return safety_factor * dx**2 / (2.0 * d_max)


def validate_stability(dt: float, dt_max: float, solver_name: str) -> None:
    """Validate that dt does not violate stability criterion.

    Args:
        dt: Proposed time step [s].
        dt_max: Maximum stable time step [s].
        solver_name: Name of the solver (for error message).

    Raises:
        ValueError: If dt > dt_max, with clear message.
    """
    if dt > dt_max:
        raise ValueError(
            f"Instability detected in {solver_name}: "
            f"dt={dt:.6e} exceeds maximum stable dt={dt_max:.6e}. "
            f"Reduce dt or increase grid spacing."
        )


# ---------------------------------------------------------------------------
# 2D Stability Functions (v0.2)
# ---------------------------------------------------------------------------


def compute_max_stable_dt_thermal_2d(
    dx: float, dy: float, alpha: float, safety_factor: float
) -> float:
    """Compute maximum stable dt for explicit Euler 2D thermal solver.

    Formula: dt_max = safety_factor * dx² * dy² / (2 * alpha * (dx² + dy²))

    Args:
        dx: Grid spacing in x-direction [m].
        dy: Grid spacing in y-direction [m].
        alpha: Thermal diffusivity [m²/s].
        safety_factor: Safety factor (< 0.5).

    Returns:
        Maximum stable time step [s].
    """
    return safety_factor * dx**2 * dy**2 / (2.0 * alpha * (dx**2 + dy**2))
