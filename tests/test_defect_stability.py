"""Tests for defect reaction-diffusion stability guard."""

import pytest

from mvp_quantum_materials.defect_stability import (
    compute_max_stable_dt_defect_2d,
    validate_defect_stability_2d,
)


class TestDefectStabilityComputation:
    """Tests for compute_max_stable_dt_defect_2d."""

    def test_returns_positive_finite(self):
        """T-STAB-01: dt_max is positive and finite."""
        dt = compute_max_stable_dt_defect_2d(
            dx=0.0002,
            dy=0.0002,
            D_max=1e-5,
            R_max=0.1,
            G_max=1.0,
            C_sat=1.0,
            safety_factor=0.4,
        )
        assert dt > 0.0
        assert isinstance(dt, float)

    def test_decreases_with_smaller_grid(self):
        """T-STAB-02: dt_max decreases when dx/dy decrease."""
        dt_coarse = compute_max_stable_dt_defect_2d(
            dx=0.001,
            dy=0.001,
            D_max=1e-5,
            R_max=0.1,
            G_max=1.0,
            C_sat=1.0,
            safety_factor=0.4,
        )
        dt_fine = compute_max_stable_dt_defect_2d(
            dx=0.0001,
            dy=0.0001,
            D_max=1e-5,
            R_max=0.1,
            G_max=1.0,
            C_sat=1.0,
            safety_factor=0.4,
        )
        assert dt_coarse > dt_fine

    def test_considers_reactive_term(self):
        """T-STAB-05: Stability considers both diffusive and reactive limits."""
        dt_no_react = compute_max_stable_dt_defect_2d(
            dx=0.001,
            dy=0.001,
            D_max=1e-5,
            R_max=0.0,
            G_max=0.0,
            C_sat=1.0,
            safety_factor=0.4,
        )
        dt_with_react = compute_max_stable_dt_defect_2d(
            dx=0.001,
            dy=0.001,
            D_max=1e-5,
            R_max=100.0,
            G_max=100.0,
            C_sat=1.0,
            safety_factor=0.4,
        )
        assert dt_with_react <= dt_no_react

    def test_zero_d_max_does_not_crash(self):
        """D_max=0 should not crash."""
        dt = compute_max_stable_dt_defect_2d(
            dx=0.001,
            dy=0.001,
            D_max=0.0,
            R_max=0.1,
            G_max=1.0,
            C_sat=1.0,
            safety_factor=0.4,
        )
        assert dt > 0.0


class TestDefectStabilityValidation:
    """Tests for validate_defect_stability_2d."""

    def test_accepts_stable_dt(self):
        """T-STAB-03: Accepts dt within stability limit."""
        dt_max = compute_max_stable_dt_defect_2d(
            dx=0.0002,
            dy=0.0002,
            D_max=1e-5,
            R_max=0.1,
            G_max=1.0,
            C_sat=1.0,
            safety_factor=0.4,
        )
        validate_defect_stability_2d(dt_max * 0.5, dt_max)

    def test_rejects_unstable_dt(self):
        """T-STAB-04: Rejects dt exceeding stability limit."""
        dt_max = compute_max_stable_dt_defect_2d(
            dx=0.0002,
            dy=0.0002,
            D_max=1e-5,
            R_max=0.1,
            G_max=1.0,
            C_sat=1.0,
            safety_factor=0.4,
        )
        with pytest.raises(ValueError, match="Instability"):
            validate_defect_stability_2d(dt_max * 2.0, dt_max)
