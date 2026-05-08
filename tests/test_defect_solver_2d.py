"""Tests for the 2D defect reaction-diffusion solver."""

import numpy as np
import pytest

from mvp_quantum_materials.defect_solver_2d import DefectResult2D, solve_defect_2d
from mvp_quantum_materials.domain import Domain2D


@pytest.fixture()
def small_domain():
    """Small 2D domain for fast tests."""
    return Domain2D(Lx=0.01, Ly=0.01, nx=11, ny=11)


@pytest.fixture()
def uniform_thermal_field(small_domain):
    """Uniform thermal field at 1100 K (peak generation)."""
    return np.full((small_domain.nx, small_domain.ny), 1100.0)


class TestDefectSolverBasic:
    """Basic solver behavior tests."""

    def test_zero_init_generates_positive(self, small_domain, uniform_thermal_field):
        """T-SOLV-01: Zero IC + G(T)>0 generates non-negative C_def."""
        result = solve_defect_2d(
            domain=small_domain,
            T_field=uniform_thermal_field,
            t_total=0.001,
        )
        assert np.all(result.C_def_final >= 0.0)
        assert np.any(result.C_def_final > 0.0)

    def test_output_finite(self, small_domain, uniform_thermal_field):
        """T-SOLV-02: C_def remains finite."""
        result = solve_defect_2d(
            domain=small_domain,
            T_field=uniform_thermal_field,
            t_total=0.001,
        )
        assert np.all(np.isfinite(result.C_def_final))

    def test_bounded_in_zero_one(self, small_domain, uniform_thermal_field):
        """T-SOLV-03: C_def stays in [0, 1]."""
        result = solve_defect_2d(
            domain=small_domain,
            T_field=uniform_thermal_field,
            t_total=0.01,
        )
        assert np.all(result.C_def_final >= 0.0)
        assert np.all(result.C_def_final <= 1.0)

    def test_no_nan_inf(self, small_domain, uniform_thermal_field):
        """T-SOLV-10: No NaN/inf in simulation."""
        result = solve_defect_2d(
            domain=small_domain,
            T_field=uniform_thermal_field,
            t_total=0.001,
        )
        assert not np.any(np.isnan(result.C_def_final))
        assert not np.any(np.isinf(result.C_def_final))


class TestDefectSolverPhysics:
    """Physics-motivated behavior tests."""

    def test_neumann_no_flux(self, small_domain, uniform_thermal_field):
        """T-SOLV-04: Neumann no-flux — no artificial boundary leak."""
        result = solve_defect_2d(
            domain=small_domain,
            T_field=uniform_thermal_field,
            t_total=0.001,
        )
        # With uniform T, result should be spatially uniform
        std = np.std(result.C_def_final)
        assert std < 1e-10, f"Expected uniform field, got std={std}"

    def test_uniform_t_preserves_symmetry(self, small_domain, uniform_thermal_field):
        """T-SOLV-05: Uniform T and IC maintain uniformity."""
        result = solve_defect_2d(
            domain=small_domain,
            T_field=uniform_thermal_field,
            t_total=0.001,
        )
        mean = np.mean(result.C_def_final)
        assert np.allclose(result.C_def_final, mean, atol=1e-12)

    def test_saturation_limits_generation(self, small_domain):
        """T-SOLV-06: Saturation term reduces G when C_def approaches C_sat."""
        T_field = np.full((small_domain.nx, small_domain.ny), 1100.0)
        result_short = solve_defect_2d(
            domain=small_domain,
            T_field=T_field,
            t_total=0.001,
        )
        result_long = solve_defect_2d(
            domain=small_domain,
            T_field=T_field,
            t_total=0.1,
        )
        # Longer run should not exceed C_sat=1.0
        assert np.all(result_long.C_def_final <= 1.0)
        # But should have more defects than the short run
        assert np.mean(result_long.C_def_final) >= np.mean(result_short.C_def_final)

    def test_recombination_decays_without_generation(self, small_domain):
        """T-SOLV-07: R(T) decays C_def when G(T)≈0."""
        # T far from T_G=1100 K → G≈0, but R>0
        T_cold = np.full((small_domain.nx, small_domain.ny), 500.0)
        C_init = np.full((small_domain.nx, small_domain.ny), 0.5)
        result = solve_defect_2d(
            domain=small_domain,
            T_field=T_cold,
            C_def_init=C_init,
            t_total=0.01,
        )
        assert np.mean(result.C_def_final) < 0.5


class TestDefectSolverContract:
    """Solver contract / API tests."""

    def test_rejects_unstable_dt(self, small_domain, uniform_thermal_field):
        """T-SOLV-08: Solver rejects unstable dt."""
        with pytest.raises(ValueError, match="Instability"):
            solve_defect_2d(
                domain=small_domain,
                T_field=uniform_thermal_field,
                t_total=0.001,
                dt_override=1.0,  # Way too large
            )

    def test_output_shape(self, small_domain, uniform_thermal_field):
        """T-SOLV-09: Output shape matches domain (nx, ny)."""
        result = solve_defect_2d(
            domain=small_domain,
            T_field=uniform_thermal_field,
            t_total=0.001,
        )
        assert result.C_def_final.shape == (small_domain.nx, small_domain.ny)

    def test_result_type(self, small_domain, uniform_thermal_field):
        """Result is DefectResult2D."""
        result = solve_defect_2d(
            domain=small_domain,
            T_field=uniform_thermal_field,
            t_total=0.001,
        )
        assert isinstance(result, DefectResult2D)
        assert result.dt > 0.0
        assert result.n_steps > 0
        assert len(result.times) > 0
