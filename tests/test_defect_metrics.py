"""Tests for defect proxy metrics."""

import numpy as np

from mvp_quantum_materials.defect_metrics import compute_defect_metrics


class TestDefectMetrics:
    """Tests for compute_defect_metrics."""

    def test_returns_all_keys(self):
        """T-MET-01: Returns max, mean, std, integral, bounded_fraction."""
        C = np.array([[0.1, 0.2], [0.3, 0.4]])
        metrics = compute_defect_metrics(C, dx=0.001, dy=0.001)
        for key in ["max", "mean", "std", "integral", "bounded_fraction"]:
            assert key in metrics, f"Missing key: {key}"

    def test_finite_for_valid_input(self):
        """T-MET-02: All metrics are finite for valid C_def."""
        C = np.random.uniform(0, 1, (10, 10))
        metrics = compute_defect_metrics(C, dx=0.001, dy=0.001)
        for key, value in metrics.items():
            assert np.isfinite(value), f"Non-finite metric: {key}={value}"

    def test_integral_scales_with_grid(self):
        """T-MET-03: Integral scales with dx*dy."""
        C = np.ones((10, 10))
        m1 = compute_defect_metrics(C, dx=0.001, dy=0.001)
        m2 = compute_defect_metrics(C, dx=0.002, dy=0.002)
        # Integral should scale as (dx*dy)
        ratio = m2["integral"] / m1["integral"]
        assert np.isclose(ratio, 4.0, rtol=0.01)

    def test_bounded_fraction_detects_violations(self):
        """T-MET-04: bounded_fraction detects out-of-bounds values."""
        C_good = np.array([[0.0, 0.5], [0.8, 1.0]])
        m_good = compute_defect_metrics(C_good, dx=1.0, dy=1.0)
        assert m_good["bounded_fraction"] == 1.0

        C_bad = np.array([[0.0, 0.5], [0.8, 1.5]])
        m_bad = compute_defect_metrics(C_bad, dx=1.0, dy=1.0)
        assert m_bad["bounded_fraction"] < 1.0

    def test_zero_field(self):
        """Zero field should give zero metrics."""
        C = np.zeros((5, 5))
        m = compute_defect_metrics(C, dx=0.001, dy=0.001)
        assert m["max"] == 0.0
        assert m["mean"] == 0.0
        assert m["integral"] == 0.0
