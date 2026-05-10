"""2D Poisson Solver.

This module provides a demonstrative only, homogeneous epsilon 2D Poisson solver
with homogeneous Dirichlet boundary conditions only.
It is not predictive of semiconductor electrostatics, is not a nonlinear Poisson
solver, makes no device-level claims, and has no self-consistent trap occupancy.
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class PoissonSolveResult:
    """Result of the demonstrative Poisson solver."""

    phi: np.ndarray
    iterations: int
    residual: float
    converged: bool


def solve_poisson_2d_demonstrative(
    rho: np.ndarray,
    dx: float,
    dy: float,
    epsilon: float,
    max_iter: int = 10000,
    tolerance: float = 1e-8,
) -> PoissonSolveResult:
    """Solve the demonstrative homogeneous 2D Poisson equation.

    This is the homogeneous simplification of:
    ∇·(ε∇φ) = −ρ
    for epsilon constant. Not a predictive semiconductor solver, not nonlinear Poisson,
    not self-consistent trap occupancy.
    """
    if not isinstance(rho, np.ndarray):
        raise TypeError("rho must be a numpy ndarray")
    if rho.ndim != 2:
        raise ValueError("rho must be 2D")
    if rho.shape[0] < 3 or rho.shape[1] < 3:
        raise ValueError("rho must have minimum shape 3x3")
    if not np.isfinite(rho).all():
        raise ValueError("rho must contain finite values")

    if dx <= 0.0 or dy <= 0.0:
        raise ValueError("dx and dy must be strictly positive")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be strictly positive")
    if max_iter <= 0:
        raise ValueError("max_iter must be strictly positive")
    if tolerance <= 0.0:
        raise ValueError("tolerance must be strictly positive")

    phi = np.zeros_like(rho)
    denom = 2.0 / dx**2 + 2.0 / dy**2

    # We use a vectorized Jacobi iterative solver
    for iteration in range(1, max_iter + 1):
        phi_old = phi.copy()

        # Jacobi update for interior points
        phi[1:-1, 1:-1] = (
            (phi_old[2:, 1:-1] + phi_old[:-2, 1:-1]) / dx**2
            + (phi_old[1:-1, 2:] + phi_old[1:-1, :-2]) / dy**2
            + rho[1:-1, 1:-1] / epsilon
        ) / denom

        # Dirichlet boundaries remain 0, naturally preserved
        # phi[0, :] = 0; phi[-1, :] = 0; phi[:, 0] = 0; phi[:, -1] = 0

        residual = float(np.max(np.abs(phi - phi_old)))
        if residual < tolerance:
            return PoissonSolveResult(
                phi=phi,
                iterations=iteration,
                residual=residual,
                converged=True,
            )

    raise RuntimeError("Solver did not converge within max_iter")
