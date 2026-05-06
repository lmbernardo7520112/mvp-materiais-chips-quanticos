"""Tests for heterogeneity metrics — T-08, T-09."""

import numpy as np
import pytest


def test_max_over_mean_gte_1():
    """T-08: max/mean ratio >= 1 for positive fields."""
    from mvp_quantum_materials.metrics import max_over_mean_ratio

    field = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    ratio = max_over_mean_ratio(field)

    assert ratio >= 1.0


def test_metrics_return_finite_values():
    """T-09: All metrics return finite values."""
    from mvp_quantum_materials.metrics import compute_all_metrics

    t_field = np.linspace(1400.0, 1700.0, 51)
    c_field = np.linspace(0.0, 1.0, 51)
    dx = 0.01 / 50

    metrics = compute_all_metrics(t_field, c_field, dx)

    for key, value in metrics.items():
        assert np.isfinite(value), f"Metric '{key}' is not finite: {value}"


def test_thermal_non_uniformity_zero_for_constant():
    """Extra: thermal non-uniformity is 0 for constant T field."""
    from mvp_quantum_materials.metrics import thermal_non_uniformity

    t_field = np.full(51, 1500.0)
    nu = thermal_non_uniformity(t_field)

    assert nu == pytest.approx(0.0, abs=1e-10)
