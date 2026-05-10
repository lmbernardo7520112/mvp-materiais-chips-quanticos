"""Tests for 2D Poisson solver.

This module validates the minimal, demonstrative 2D Poisson solver
required by v0.4 Poisson Bridge Scope (ADR-007).
"""

import numpy as np
import pytest

from mvp_quantum_materials.poisson_solver_2d import (
    PoissonSolveResult,
    solve_poisson_2d_demonstrative,
)


def test_zero_source_returns_zero_potential():
    """zero source returns zero potential."""
    rho = np.zeros((10, 10))
    result = solve_poisson_2d_demonstrative(rho, dx=1.0, dy=1.0, epsilon=1.0)
    assert np.allclose(result.phi, 0.0)
    assert result.converged


def test_output_shape_equals_rho_shape():
    """output shape equals rho shape."""
    rho = np.zeros((10, 15))
    result = solve_poisson_2d_demonstrative(rho, dx=1.0, dy=1.0, epsilon=1.0)
    assert result.phi.shape == rho.shape


def test_incompatible_rho_shape_raises():
    """incompatible rho shape raises ValueError."""
    rho = np.zeros(10)  # 1D instead of 2D
    with pytest.raises(ValueError, match="must be 2D"):
        solve_poisson_2d_demonstrative(rho, dx=1.0, dy=1.0, epsilon=1.0)


def test_invalid_grid_spacing_raises():
    """dx <= 0 raises ValueError, dy <= 0 raises ValueError."""
    rho = np.zeros((10, 10))
    with pytest.raises(ValueError, match="strictly positive"):
        solve_poisson_2d_demonstrative(rho, dx=0.0, dy=1.0, epsilon=1.0)
    with pytest.raises(ValueError, match="strictly positive"):
        solve_poisson_2d_demonstrative(rho, dx=1.0, dy=-1.0, epsilon=1.0)


def test_invalid_epsilon_raises():
    """epsilon <= 0 raises ValueError."""
    rho = np.zeros((10, 10))
    with pytest.raises(ValueError, match="strictly positive"):
        solve_poisson_2d_demonstrative(rho, dx=1.0, dy=1.0, epsilon=0.0)


def test_homogeneous_dirichlet_boundaries_remain_zero():
    """homogeneous Dirichlet boundaries remain zero."""
    rho = np.ones((5, 5))
    # Test says: Dirichlet homogeneous boundaries remain zero.
    # The solver enforces phi=0 on boundaries.
    result = solve_poisson_2d_demonstrative(rho, dx=1.0, dy=1.0, epsilon=1.0)
    phi = result.phi
    assert np.all(phi[0, :] == 0.0)
    assert np.all(phi[-1, :] == 0.0)
    assert np.all(phi[:, 0] == 0.0)
    assert np.all(phi[:, -1] == 0.0)


def test_manufactured_solution_has_acceptable_l2_error():
    """manufactured solution has acceptable L2 error."""
    Lx, Ly = 10.0, 10.0
    Nx, Ny = 20, 20
    dx, dy = Lx / (Nx - 1), Ly / (Ny - 1)
    epsilon = 1.0

    x = np.linspace(0, Lx, Nx)
    y = np.linspace(0, Ly, Ny)
    X, Y = np.meshgrid(x, y, indexing="ij")

    # phi_exact(x,y) = sin(pi*x/Lx) * sin(pi*y/Ly)
    phi_exact = np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly)

    # lambda = (pi/Lx)^2 + (pi/Ly)^2
    lam = (np.pi / Lx) ** 2 + (np.pi / Ly) ** 2

    # rho(x,y) = epsilon * lambda * phi_exact
    rho = epsilon * lam * phi_exact

    result = solve_poisson_2d_demonstrative(rho, dx=dx, dy=dy, epsilon=epsilon, tolerance=1e-5)

    # Check L2 relative error
    error = np.linalg.norm(result.phi - phi_exact) / np.linalg.norm(phi_exact)
    assert error < 0.1, f"L2 error too high: {error}"


def test_non_convergence_raises():
    """non-convergence raises RuntimeError."""
    rho = np.ones((10, 10))
    with pytest.raises(RuntimeError, match="did not converge"):
        solve_poisson_2d_demonstrative(
            rho, dx=1.0, dy=1.0, epsilon=1.0, max_iter=1, tolerance=1e-12
        )


def test_result_exposes_metadata():
    """result exposes phi, iterations, residual, converged."""
    rho = np.zeros((5, 5))
    result = solve_poisson_2d_demonstrative(rho, dx=1.0, dy=1.0, epsilon=1.0)
    assert hasattr(result, "phi")
    assert hasattr(result, "iterations")
    assert hasattr(result, "residual")
    assert hasattr(result, "converged")
    assert isinstance(result, PoissonSolveResult)
