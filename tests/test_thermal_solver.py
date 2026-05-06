"""Tests for thermal solver — T-02, T-03, T-04, T-15."""

import numpy as np
import pytest


def test_thermal_constant_field_remains_constant():
    """T-02: A uniform temperature field with matching BCs stays constant."""
    from mvp_quantum_materials.config import ThermalConfig
    from mvp_quantum_materials.domain import Domain1D
    from mvp_quantum_materials.thermal_solver import solve_thermal_1d

    domain = Domain1D(length=0.01, nx=51)
    config = ThermalConfig(
        alpha=8.8e-5,
        t_left=1500.0,
        t_right=1500.0,
        t_init=1500.0,
        t_total=0.1,
        safety_factor=0.4,
    )

    result = solve_thermal_1d(domain, config)

    assert np.allclose(result.T_final, 1500.0, atol=1e-6)


def test_thermal_gradient_smooths():
    """T-03: An initial step gradient smooths over time."""
    from mvp_quantum_materials.config import ThermalConfig
    from mvp_quantum_materials.domain import Domain1D
    from mvp_quantum_materials.thermal_solver import solve_thermal_1d

    domain = Domain1D(length=0.01, nx=51)
    config = ThermalConfig(
        alpha=8.8e-5,
        t_left=1700.0,
        t_right=1400.0,
        t_init=1500.0,
        t_total=0.5,
        safety_factor=0.4,
    )

    result = solve_thermal_1d(domain, config)

    # Max gradient should be less than the initial step
    grad = np.abs(np.diff(result.T_final))
    initial_grad = np.abs(np.diff(result.T_history[0]))
    assert np.max(grad) <= np.max(initial_grad) + 1e-10


def test_thermal_output_finite_and_shape():
    """T-04: Output is finite and has correct shape."""
    from mvp_quantum_materials.config import ThermalConfig
    from mvp_quantum_materials.domain import Domain1D
    from mvp_quantum_materials.thermal_solver import solve_thermal_1d

    domain = Domain1D(length=0.01, nx=51)
    config = ThermalConfig(
        alpha=8.8e-5,
        t_left=1700.0,
        t_right=1400.0,
        t_init=1500.0,
        t_total=0.1,
        safety_factor=0.4,
    )

    result = solve_thermal_1d(domain, config)

    assert result.T_final.shape == (51,)
    assert np.all(np.isfinite(result.T_final))
    assert len(result.T_history) > 0


def test_thermal_rejects_unstable_dt():
    """T-15: Solver raises ValueError if dt violates stability criterion."""
    from mvp_quantum_materials.config import ThermalConfig
    from mvp_quantum_materials.domain import Domain1D
    from mvp_quantum_materials.thermal_solver import solve_thermal_1d

    domain = Domain1D(length=0.01, nx=51)
    config = ThermalConfig(
        alpha=8.8e-5,
        t_left=1700.0,
        t_right=1400.0,
        t_init=1500.0,
        t_total=0.1,
        safety_factor=0.4,
        dt_override=1.0,  # Way too large — should trigger rejection
    )

    with pytest.raises(ValueError, match="[Ss]tabilit|[Ii]nstab|dt"):
        solve_thermal_1d(domain, config)
