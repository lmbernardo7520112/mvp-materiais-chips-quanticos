"""Tests for 2D thermal stability guard."""

import pytest

from mvp_quantum_materials.config import (
    compute_max_stable_dt_thermal_2d,
    validate_stability,
)


class TestThermal2DStability:
    """Tests for 2D thermal stability criterion.

    Formula: dt <= safety * dx² * dy² / (2 * alpha * (dx² + dy²))
    """

    def test_returns_finite_positive(self):
        """dt_max is finite and positive for valid inputs."""
        dt_max = compute_max_stable_dt_thermal_2d(dx=1e-3, dy=1e-3, alpha=8.8e-5, safety_factor=0.4)
        assert dt_max > 0
        assert pytest.approx(dt_max, rel=1e-6) != float("inf")

    def test_dt_decreases_with_finer_grid(self):
        """dt_max decreases when dx/dy decrease."""
        dt_coarse = compute_max_stable_dt_thermal_2d(
            dx=1e-3, dy=1e-3, alpha=8.8e-5, safety_factor=0.4
        )
        dt_fine = compute_max_stable_dt_thermal_2d(
            dx=5e-4, dy=5e-4, alpha=8.8e-5, safety_factor=0.4
        )
        assert dt_fine < dt_coarse

    def test_formula_correctness(self):
        """dt_max matches the formula: safety * dx² * dy² / (2 * alpha * (dx² + dy²))."""
        dx, dy, alpha, sf = 1e-3, 2e-3, 8.8e-5, 0.4
        expected = sf * dx**2 * dy**2 / (2.0 * alpha * (dx**2 + dy**2))
        dt_max = compute_max_stable_dt_thermal_2d(dx, dy, alpha, sf)
        assert dt_max == pytest.approx(expected)

    def test_validate_accepts_stable_dt(self):
        """validate_stability accepts dt <= dt_max."""
        dt_max = compute_max_stable_dt_thermal_2d(dx=1e-3, dy=1e-3, alpha=8.8e-5, safety_factor=0.4)
        # Should not raise
        validate_stability(dt_max * 0.9, dt_max, "thermal_solver_2d")

    def test_validate_rejects_unstable_dt(self):
        """validate_stability rejects dt > dt_max with clear ValueError."""
        dt_max = compute_max_stable_dt_thermal_2d(dx=1e-3, dy=1e-3, alpha=8.8e-5, safety_factor=0.4)
        with pytest.raises(ValueError, match="Instability"):
            validate_stability(dt_max * 1.1, dt_max, "thermal_solver_2d")
