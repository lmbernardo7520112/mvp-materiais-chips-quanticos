#!/usr/bin/env python3
"""Run 1D thermal solver and save results.

Usage:
    python scripts/run_thermal_1d.py [--output-dir DIR]
"""

import argparse
from pathlib import Path

from mvp_quantum_materials.config import ThermalConfig
from mvp_quantum_materials.domain import Domain1D
from mvp_quantum_materials.plots import plot_thermal_evolution
from mvp_quantum_materials.thermal_solver import solve_thermal_1d


def main(output_dir: Path) -> None:
    """Run thermal simulation and generate figure."""
    domain = Domain1D(length=0.01, nx=101)
    config = ThermalConfig(
        alpha=8.8e-5,
        t_left=1700.0,
        t_right=1400.0,
        t_init=1500.0,
        t_total=0.5,
    )

    print(f"Running thermal 1D solver (nx={domain.nx}, t_total={config.t_total}s)...")
    result = solve_thermal_1d(domain, config)
    print(f"  dt = {result.dt:.6e} s, n_steps = {result.n_steps}")
    print(f"  T range: [{result.T_final.min():.1f}, {result.T_final.max():.1f}] K")

    fig_path = plot_thermal_evolution(domain.x, result, output_dir / "thermal_1d_evolution.png")
    print(f"  Figure saved: {fig_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run 1D thermal solver")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/figures"),
        help="Output directory for figures",
    )
    args = parser.parse_args()
    main(args.output_dir)
