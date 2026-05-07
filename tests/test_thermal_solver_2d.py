"""Tests for 2D thermal solver — T-2D-02..06."""

import numpy as np
import pytest

from mvp_quantum_materials.config import compute_max_stable_dt_thermal_2d
from mvp_quantum_materials.domain import Domain2D
from mvp_quantum_materials.thermal_solver_2d import solve_thermal_2d

# Small domain for fast tests
DOMAIN = Domain2D(Lx=0.01, Ly=0.01, nx=11, ny=11)
ALPHA = 8.8e-5
T_INIT = 1500.0
T_BOUNDARY = 1400.0


class TestThermalSolver2DConstantField:
    """T-2D-02: Constant field remains constant."""

    def test_constant_field_remains_constant(self):
        """A uniform T field with matching BCs stays constant."""
        T0 = np.full((DOMAIN.nx, DOMAIN.ny), T_BOUNDARY)

        result = solve_thermal_2d(
            domain=DOMAIN,
            T_init=T0,
            alpha=ALPHA,
            t_total=0.01,
            t_boundary=T_BOUNDARY,
            safety_factor=0.4,
        )

        assert np.allclose(result.T_final, T_BOUNDARY, atol=1e-10)


class TestThermalSolver2DSmoothing:
    """T-2D-03: Perturbation smooths over time."""

    def test_gradient_smooths(self):
        """A hot-center perturbation dissipates: max-min decreases."""
        T0 = np.full((DOMAIN.nx, DOMAIN.ny), T_BOUNDARY)
        cx, cy = DOMAIN.nx // 2, DOMAIN.ny // 2
        T0[cx, cy] = T_BOUNDARY + 100.0

        result = solve_thermal_2d(
            domain=DOMAIN,
            T_init=T0,
            alpha=ALPHA,
            t_total=0.01,
            t_boundary=T_BOUNDARY,
            safety_factor=0.4,
        )

        initial_range = T0.max() - T0.min()
        final_range = result.T_final.max() - result.T_final.min()
        assert final_range < initial_range


class TestThermalSolver2DOutputShape:
    """T-2D-04: Output is finite and has correct shape."""

    def test_output_shape(self):
        """T_final has shape (nx, ny)."""
        T0 = np.full((DOMAIN.nx, DOMAIN.ny), T_INIT)
        T0[0, :] = T_BOUNDARY
        T0[-1, :] = T_BOUNDARY
        T0[:, 0] = T_BOUNDARY
        T0[:, -1] = T_BOUNDARY

        result = solve_thermal_2d(
            domain=DOMAIN,
            T_init=T0,
            alpha=ALPHA,
            t_total=0.001,
            t_boundary=T_BOUNDARY,
            safety_factor=0.4,
        )

        assert result.T_final.shape == (DOMAIN.nx, DOMAIN.ny)

    def test_output_finite(self):
        """T_final contains no NaN or inf."""
        T0 = np.full((DOMAIN.nx, DOMAIN.ny), T_INIT)
        T0[0, :] = T_BOUNDARY
        T0[-1, :] = T_BOUNDARY
        T0[:, 0] = T_BOUNDARY
        T0[:, -1] = T_BOUNDARY

        result = solve_thermal_2d(
            domain=DOMAIN,
            T_init=T0,
            alpha=ALPHA,
            t_total=0.001,
            t_boundary=T_BOUNDARY,
            safety_factor=0.4,
        )

        assert np.all(np.isfinite(result.T_final))


class TestThermalSolver2DStabilityGuard:
    """T-2D-05: Solver recusa dt instável."""

    def test_rejects_unstable_dt(self):
        """Solver raises ValueError when dt_override violates stability."""
        T0 = np.full((DOMAIN.nx, DOMAIN.ny), T_INIT)

        dt_max = compute_max_stable_dt_thermal_2d(DOMAIN.dx, DOMAIN.dy, ALPHA, 0.4)

        with pytest.raises(ValueError, match="Instability"):
            solve_thermal_2d(
                domain=DOMAIN,
                T_init=T0,
                alpha=ALPHA,
                t_total=0.001,
                t_boundary=T_BOUNDARY,
                safety_factor=0.4,
                dt_override=dt_max * 10.0,
            )


class TestThermalSolver2DDirichletBC:
    """T-2D-06: Dirichlet BCs maintained on all four edges."""

    def test_boundary_values_preserved(self):
        """After solving, all four boundary edges equal t_boundary."""
        T0 = np.full((DOMAIN.nx, DOMAIN.ny), T_INIT)
        T0[0, :] = T_BOUNDARY
        T0[-1, :] = T_BOUNDARY
        T0[:, 0] = T_BOUNDARY
        T0[:, -1] = T_BOUNDARY

        result = solve_thermal_2d(
            domain=DOMAIN,
            T_init=T0,
            alpha=ALPHA,
            t_total=0.01,
            t_boundary=T_BOUNDARY,
            safety_factor=0.4,
        )

        # All four edges
        assert np.allclose(result.T_final[0, :], T_BOUNDARY)
        assert np.allclose(result.T_final[-1, :], T_BOUNDARY)
        assert np.allclose(result.T_final[:, 0], T_BOUNDARY)
        assert np.allclose(result.T_final[:, -1], T_BOUNDARY)
