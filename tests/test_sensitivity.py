"""Tests for sensitivity analysis — T-10."""

import pytest


def test_sensitivity_returns_non_empty_table():
    """T-10: Sensitivity analysis returns a non-empty results table."""
    from mvp_quantum_materials.sensitivity import run_sensitivity_analysis

    results = run_sensitivity_analysis()

    assert len(results) > 0
    assert "parameter" in results[0]
    assert "metric_value" in results[0]
