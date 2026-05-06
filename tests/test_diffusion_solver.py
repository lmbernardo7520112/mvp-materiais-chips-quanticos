"""Tests for diffusion solver — T-05, T-06, T-07, T-13, T-14, T-16, T-17."""

import numpy as np
import pytest


def test_arrhenius_d_increases_with_temperature():
    """T-05: D(T) increases with T for positive D0 and Ea."""
    from mvp_quantum_materials.diffusion_solver import arrhenius_diffusivity

    d0, ea = 1.0e-8, 0.5
    d_low = arrhenius_diffusivity(1000.0, d0, ea)
    d_high = arrhenius_diffusivity(2000.0, d0, ea)

    assert d_high > d_low
    assert d_low > 0.0
    assert np.isfinite(d_low)
    assert np.isfinite(d_high)


def test_source_maximum_near_tc():
    """T-06: Thermal source S_C(T) has maximum near T_c."""
    from mvp_quantum_materials.diffusion_solver import thermal_source

    tc, sigma = 1500.0, 50.0
    a_c = 1.0
    temps = np.linspace(1000.0, 2000.0, 1001)
    source_vals = thermal_source(temps, a_c, tc, sigma)

    max_idx = np.argmax(source_vals)
    t_at_max = temps[max_idx]

    assert abs(t_at_max - tc) < sigma


def test_diffusion_constant_field_no_source_stable():
    """T-07: Constant C field without source remains constant (Neumann BCs)."""
    from mvp_quantum_materials.config import DiffusionConfig
    from mvp_quantum_materials.domain import Domain1D
    from mvp_quantum_materials.diffusion_solver import solve_diffusion_1d

    domain = Domain1D(length=0.01, nx=51)
    t_field = np.full(51, 1500.0)
    config = DiffusionConfig(a_c=0.0, c_init=1.0, t_total=0.1)

    result = solve_diffusion_1d(domain, t_field, config)

    assert np.allclose(result.C_final, 1.0, atol=1e-6)


def test_source_non_negative():
    """T-13: S_C is non-negative for any temperature."""
    from mvp_quantum_materials.diffusion_solver import thermal_source

    temps = np.array([0.0, 300.0, 1000.0, 1500.0, 2000.0, 5000.0, 1e6])
    source = thermal_source(temps, a_c=1.0, t_critical=1500.0, sigma_t=50.0)

    assert np.all(source >= 0.0)


def test_source_decays_far_from_tc():
    """T-14: S_C tends to zero far from T_c."""
    from mvp_quantum_materials.diffusion_solver import thermal_source

    tc, sigma = 1500.0, 50.0
    s_at_tc = thermal_source(np.array([tc]), 1.0, tc, sigma)[0]
    s_far = thermal_source(np.array([tc + 10 * sigma]), 1.0, tc, sigma)[0]

    assert s_far < 0.01 * s_at_tc


def test_diffusion_rejects_unstable_dt():
    """T-16: Diffusion solver raises ValueError for unstable dt."""
    from mvp_quantum_materials.config import DiffusionConfig
    from mvp_quantum_materials.domain import Domain1D
    from mvp_quantum_materials.diffusion_solver import solve_diffusion_1d

    domain = Domain1D(length=0.01, nx=51)
    t_field = np.full(51, 1500.0)
    config = DiffusionConfig(dt_override=1.0, t_total=0.1)

    with pytest.raises(ValueError, match="[Ss]tabilit|[Ii]nstab|dt"):
        solve_diffusion_1d(domain, t_field, config)


def test_c_remains_finite_with_source():
    """T-17: C remains finite after integration with source active."""
    from mvp_quantum_materials.config import DiffusionConfig
    from mvp_quantum_materials.domain import Domain1D
    from mvp_quantum_materials.diffusion_solver import solve_diffusion_1d

    domain = Domain1D(length=0.01, nx=51)
    t_field = np.full(51, 1500.0)  # At T_c — max source
    config = DiffusionConfig(a_c=1.0, c_init=0.0, t_total=0.5)

    result = solve_diffusion_1d(domain, t_field, config)

    assert np.all(np.isfinite(result.C_final))
    assert np.all(result.C_final >= 0.0)
