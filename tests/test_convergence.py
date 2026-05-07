"""Tests for convergence analysis — T-CONV-01..04."""

import pytest

from mvp_quantum_materials.convergence import run_convergence_analysis


class TestConvergenceAnalysis:
    """Tests for manufactured solution convergence."""

    def test_returns_non_empty_table(self):
        """T-CONV-01: Convergence returns a non-empty list of results."""
        results = run_convergence_analysis(
            nx_values=[11, 21],
            alpha=8.8e-5,
            Lx=0.01,
            Ly=0.01,
            t_final=0.001,
            safety_factor=0.4,
        )
        assert len(results) > 0

    def test_error_decreases_with_refinement(self):
        """T-CONV-02: L2 error decreases with mesh refinement."""
        results = run_convergence_analysis(
            nx_values=[11, 21, 41],
            alpha=8.8e-5,
            Lx=0.01,
            Ly=0.01,
            t_final=0.0005,
            safety_factor=0.4,
        )
        errors = [r["error_l2"] for r in results]
        # At least one pair shows error decrease
        decreasing = any(errors[i + 1] < errors[i] for i in range(len(errors) - 1))
        assert decreasing, f"Error did not decrease with refinement: {errors}"

    def test_table_has_required_columns(self):
        """T-CONV-03: Each result has all required columns."""
        results = run_convergence_analysis(
            nx_values=[11, 21],
            alpha=8.8e-5,
            Lx=0.01,
            Ly=0.01,
            t_final=0.001,
            safety_factor=0.4,
        )
        required_cols = [
            "nx",
            "ny",
            "dx",
            "dy",
            "dt",
            "error_l2",
            "error_linf",
            "observed_order",
            "elapsed_time",
        ]
        for r in results:
            for col in required_cols:
                assert col in r, f"Missing column: {col}"

    def test_observed_order_reasonable(self):
        """T-CONV-04: observed_order >= 1.5 in at least one valid range."""
        results = run_convergence_analysis(
            nx_values=[11, 21, 41],
            alpha=8.8e-5,
            Lx=0.01,
            Ly=0.01,
            t_final=0.0005,
            safety_factor=0.4,
        )
        orders = [r["observed_order"] for r in results if r["observed_order"] is not None]
        if len(orders) > 0:
            max_order = max(orders)
            assert max_order >= 1.5, (
                f"Max observed order {max_order:.2f} < 1.5. All orders: {orders}"
            )
        else:
            pytest.skip("No observed orders computed (need >= 2 refinement levels)")
