#!/usr/bin/env python3
"""Generate all results: thermal, diffusion, and sensitivity figures.

Usage:
    python scripts/generate_all_results.py [--output-dir DIR]
"""

import argparse
from pathlib import Path

from mvp_quantum_materials.config import DiffusionConfig, ThermalConfig
from mvp_quantum_materials.diffusion_solver import solve_diffusion_1d
from mvp_quantum_materials.domain import Domain1D
from mvp_quantum_materials.plots import (
    plot_diffusion_evolution,
    plot_sensitivity_results,
    plot_thermal_evolution,
)
from mvp_quantum_materials.sensitivity import run_sensitivity_analysis
from mvp_quantum_materials.thermal_solver import solve_thermal_1d


def run_thermal(output_dir: Path) -> None:
    """Run thermal simulation and generate figure."""
    domain = Domain1D(length=0.01, nx=101)
    config = ThermalConfig(
        t_left=1700.0,
        t_right=1400.0,
        t_init=1500.0,
        t_total=0.5,
    )
    print(f"  Solving thermal 1D (nx={domain.nx})...")
    result = solve_thermal_1d(domain, config)
    fig_path = plot_thermal_evolution(domain.x, result, output_dir / "thermal_1d_evolution.png")
    print(f"  Figure: {fig_path}")


def run_diffusion(output_dir: Path) -> None:
    """Run diffusion simulation and generate figure."""
    domain = Domain1D(length=0.01, nx=101)
    thermal_config = ThermalConfig(
        t_left=1700.0,
        t_right=1400.0,
        t_init=1500.0,
        t_total=0.5,
    )
    diffusion_config = DiffusionConfig(t_total=0.5)

    thermal_result = solve_thermal_1d(domain, thermal_config)
    print("  Solving diffusion 1D (Arrhenius + source)...")
    diff_result = solve_diffusion_1d(domain, thermal_result.T_final, diffusion_config)
    fig_path = plot_diffusion_evolution(
        domain.x, diff_result, output_dir / "diffusion_1d_evolution.png"
    )
    print(f"  Figure: {fig_path}")


def run_sensitivity(output_dir: Path) -> None:
    """Run sensitivity analysis and generate figure."""
    print("  Running sensitivity analysis (5 parameters)...")
    results = run_sensitivity_analysis()
    fig_path = plot_sensitivity_results(results, output_dir / "sensitivity_analysis.png")
    print(f"  Figure: {fig_path}")


def main(output_dir: Path) -> None:
    """Generate all results and figures."""
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("MVP Quantum Materials — Generating All Results")
    print(f"Output directory: {output_dir}")
    print("=" * 60)

    print("[1/3] Thermal 1D")
    run_thermal(output_dir)

    print("[2/3] Diffusion 1D")
    run_diffusion(output_dir)

    print("[3/3] Sensitivity Analysis")
    run_sensitivity(output_dir)

    figures = list(output_dir.glob("*.png"))
    print("=" * 60)
    print(f"Done. {len(figures)} figures generated:")
    for f in sorted(figures):
        print(f"  - {f.name}")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate all MVP results")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/figures"),
    )
    args = parser.parse_args()
    main(args.output_dir)
