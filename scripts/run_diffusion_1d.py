#!/usr/bin/env python3
"""Run 1D diffusion solver and save results.

Usage:
    python scripts/run_diffusion_1d.py [--output-dir DIR]
"""

import argparse
from pathlib import Path

from mvp_quantum_materials.config import DiffusionConfig, ThermalConfig
from mvp_quantum_materials.diffusion_solver import solve_diffusion_1d
from mvp_quantum_materials.domain import Domain1D
from mvp_quantum_materials.plots import plot_diffusion_evolution
from mvp_quantum_materials.thermal_solver import solve_thermal_1d


def main(output_dir: Path) -> None:
    """Run thermal + diffusion simulation and generate figure."""
    domain = Domain1D(length=0.01, nx=101)
    thermal_config = ThermalConfig(
        t_left=1700.0,
        t_right=1400.0,
        t_init=1500.0,
        t_total=0.5,
    )
    diffusion_config = DiffusionConfig(t_total=0.5)

    print("Running thermal 1D solver...")
    thermal_result = solve_thermal_1d(domain, thermal_config)

    print("Running diffusion 1D solver (Arrhenius + source)...")
    diff_result = solve_diffusion_1d(domain, thermal_result.T_final, diffusion_config)
    print(f"  dt = {diff_result.dt:.6e} s, n_steps = {diff_result.n_steps}")
    print(f"  C range: [{diff_result.C_final.min():.4f}, {diff_result.C_final.max():.4f}]")

    fig_path = plot_diffusion_evolution(
        domain.x, diff_result, output_dir / "diffusion_1d_evolution.png"
    )
    print(f"  Figure saved: {fig_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run 1D diffusion solver")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/figures"),
    )
    args = parser.parse_args()
    main(args.output_dir)
