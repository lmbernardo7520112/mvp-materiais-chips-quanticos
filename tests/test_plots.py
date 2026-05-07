"""Tests for plot generation — direct function calls for coverage."""

from pathlib import Path

import numpy as np

from mvp_quantum_materials.diffusion_solver import DiffusionResult
from mvp_quantum_materials.plots import (
    plot_diffusion_evolution,
    plot_sensitivity_ranking,
    plot_sensitivity_results,
    plot_thermal_2d_final,
    plot_thermal_evolution,
)
from mvp_quantum_materials.thermal_solver import ThermalResult


def test_plot_thermal_evolution(tmp_path: Path):
    """Plot thermal evolution without error."""
    x = np.linspace(0, 0.01, 11)
    T = np.full(11, 1500.0)
    result = ThermalResult(
        T_final=T,
        T_history=[T.copy(), T.copy()],
        dt=1e-4,
        n_steps=10,
        times=[0.0, 0.001],
    )
    path = plot_thermal_evolution(x, result, tmp_path / "thermal.png")
    assert path.exists()


def test_plot_diffusion_evolution(tmp_path: Path):
    """Plot diffusion evolution without error."""
    x = np.linspace(0, 0.01, 11)
    C = np.zeros(11)
    result = DiffusionResult(
        C_final=C,
        C_history=[C.copy(), C.copy()],
        dt=1e-4,
        n_steps=10,
        times=[0.0, 0.001],
    )
    path = plot_diffusion_evolution(x, result, tmp_path / "diffusion.png")
    assert path.exists()


def test_plot_sensitivity_results(tmp_path: Path):
    """Plot sensitivity results without error."""
    results = [
        {"parameter": "alpha", "value": 0.001, "metric_value": 1.0},
        {"parameter": "alpha", "value": 0.002, "metric_value": 1.5},
    ]
    path = plot_sensitivity_results(results, tmp_path / "sens.png")
    assert path.exists()


def test_plot_sensitivity_ranking(tmp_path: Path):
    """Plot sensitivity ranking without error."""
    ranking = [
        {"parameter": "alpha", "sensitivity": 0.5},
        {"parameter": "d0", "sensitivity": 0.3},
    ]
    path = plot_sensitivity_ranking(ranking, tmp_path / "rank.png")
    assert path.exists()


def test_plot_thermal_2d_final(tmp_path: Path):
    """Plot 2D thermal field without error."""
    x = np.linspace(0, 0.01, 11)
    y = np.linspace(0, 0.01, 11)
    T = np.full((11, 11), 1500.0)
    path = plot_thermal_2d_final(x, y, T, tmp_path / "thermal_2d.png")
    assert path.exists()
