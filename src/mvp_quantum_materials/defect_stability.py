"""Stability guard for the 2D defect reaction-diffusion solver.

Computes maximum stable time step considering both diffusive and
reactive CFL-like constraints for explicit Euler integration.

Note:
    This is a conservative demonstrative guard — not calibrated
    for production semiconductor simulation.
"""


def compute_max_stable_dt_defect_2d(
    dx: float,
    dy: float,
    D_max: float,
    R_max: float,
    G_max: float,
    C_sat: float,
    safety_factor: float = 0.4,
) -> float:
    """Compute maximum stable dt for explicit Euler defect solver.

    Considers two limits:
    - Diffusive: dt_diff = safety * dx² * dy² / (2 * D_max * (dx² + dy²))
    - Reactive:  dt_react = safety / max(R_max + G_max/C_sat, eps)

    Returns min(dt_diff, dt_react).

    Args:
        dx: Grid spacing in x [m].
        dy: Grid spacing in y [m].
        D_max: Maximum diffusivity in the domain [m²/s].
        R_max: Maximum recombination rate [1/s].
        G_max: Maximum generation rate [1/s].
        C_sat: Saturation concentration (adimensional, typically 1.0).
        safety_factor: Safety factor in (0, 1].

    Returns:
        Maximum stable time step [s].
    """
    eps = 1e-30  # Avoid division by zero

    # Diffusive limit
    if D_max > 0.0:
        dt_diff = safety_factor * dx**2 * dy**2 / (2.0 * D_max * (dx**2 + dy**2))
    else:
        dt_diff = float("inf")

    # Reactive limit (linearized worst case)
    react_rate = R_max + G_max / max(C_sat, eps)
    if react_rate > eps:
        dt_react = safety_factor / react_rate
    else:
        dt_react = float("inf")

    return min(dt_diff, dt_react)


def validate_defect_stability_2d(dt: float, dt_max: float) -> None:
    """Validate that dt does not violate defect solver stability.

    Args:
        dt: Proposed time step [s].
        dt_max: Maximum stable time step [s].

    Raises:
        ValueError: If dt > dt_max.
    """
    if dt > dt_max:
        raise ValueError(
            f"Instability detected in defect_solver_2d: "
            f"dt={dt:.6e} exceeds maximum stable dt={dt_max:.6e}. "
            f"Reduce dt or increase grid spacing."
        )
