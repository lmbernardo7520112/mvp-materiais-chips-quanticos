#!/usr/bin/env python3
"""Generate all results: thermal, diffusion, sensitivity figures and CSV.

v0.1 artifacts (preserved):
  - thermal_1d_evolution.png
  - diffusion_1d_evolution.png
  - sensitivity_analysis.png
  - sensitivity_ranking.png
  - sensitivity_results.csv

v0.2 artifacts (new):
  - thermal_2d_final.png
  - convergence_analysis.png
  - convergence_results.csv

Usage:
    python scripts/generate_all_results.py [--output-dir DIR]
"""

import argparse
from pathlib import Path

import numpy as np

from mvp_quantum_materials.config import DiffusionConfig, ThermalConfig
from mvp_quantum_materials.convergence import (
    export_convergence_csv,
    plot_convergence,
    run_convergence_analysis,
)
from mvp_quantum_materials.diffusion_solver import solve_diffusion_1d
from mvp_quantum_materials.domain import Domain1D, Domain2D
from mvp_quantum_materials.plots import (
    plot_diffusion_evolution,
    plot_sensitivity_ranking,
    plot_sensitivity_results,
    plot_thermal_2d_final,
    plot_thermal_evolution,
)
from mvp_quantum_materials.sensitivity import (
    compute_sensitivity_ranking,
    export_sensitivity_csv,
    run_sensitivity_analysis,
)
from mvp_quantum_materials.thermal_solver import solve_thermal_1d
from mvp_quantum_materials.thermal_solver_2d import solve_thermal_2d


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


def run_sensitivity(output_dir: Path, tables_dir: Path) -> None:
    """Run sensitivity analysis, generate figures and CSV."""
    print("  Running sensitivity analysis (5 parameters)...")
    results = run_sensitivity_analysis()

    fig_path = plot_sensitivity_results(results, output_dir / "sensitivity_analysis.png")
    print(f"  Figure: {fig_path}")

    # Ranking
    ranking = compute_sensitivity_ranking(results)
    fig_rank = plot_sensitivity_ranking(ranking, output_dir / "sensitivity_ranking.png")
    print(f"  Figure: {fig_rank}")

    # CSV
    csv_path = export_sensitivity_csv(results, tables_dir / "sensitivity_results.csv")
    print(f"  CSV: {csv_path}")

    # Print ranking
    print("\n  Sensitivity Ranking (normalized range, demonstrative):")
    for r in ranking:
        print(f"    {r['parameter']:15s}  S = {r['sensitivity']:.4f}")


def run_thermal_2d(output_dir: Path) -> None:
    """Run 2D thermal simulation and generate figure."""
    domain = Domain2D(Lx=0.01, Ly=0.01, nx=51, ny=51)
    T_init = np.full((domain.nx, domain.ny), 1500.0)
    T_init[0, :] = 1400.0
    T_init[-1, :] = 1400.0
    T_init[:, 0] = 1400.0
    T_init[:, -1] = 1400.0

    print(f"  Solving thermal 2D (nx={domain.nx}, ny={domain.ny})...")
    result = solve_thermal_2d(
        domain=domain,
        T_init=T_init,
        alpha=8.8e-5,
        t_total=0.01,
        t_boundary=1400.0,
        safety_factor=0.4,
    )

    fig_path = plot_thermal_2d_final(
        domain.x, domain.y, result.T_final, output_dir / "thermal_2d_final.png"
    )
    print(f"  Figure: {fig_path}")


def run_convergence(output_dir: Path, tables_dir: Path) -> None:
    """Run convergence analysis with manufactured solution."""
    print("  Running convergence analysis (nx = 11, 21, 41)...")
    results = run_convergence_analysis(
        nx_values=[11, 21, 41],
        alpha=8.8e-5,
        Lx=0.01,
        Ly=0.01,
        t_final=0.001,
        safety_factor=0.4,
    )

    csv_path = export_convergence_csv(results, tables_dir / "convergence_results.csv")
    print(f"  CSV: {csv_path}")

    fig_path = plot_convergence(results, output_dir / "convergence_analysis.png")
    print(f"  Figure: {fig_path}")


def main(output_dir: Path) -> None:
    """Generate all results and figures."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Tables dir: sibling of output_dir or results/tables
    tables_dir = output_dir.parent / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("MVP Quantum Materials — Generating All Results")
    print(f"Output directory: {output_dir}")
    print(f"Tables directory: {tables_dir}")
    print("=" * 60)

    # --- v0.1 artifacts (preserved) ---
    print("[1/6] Thermal 1D")
    run_thermal(output_dir)

    print("[2/6] Diffusion 1D")
    run_diffusion(output_dir)

    print("[3/6] Sensitivity Analysis + Ranking")
    run_sensitivity(output_dir, tables_dir)

    # --- v0.2 artifacts (new) ---
    print("[4/6] Thermal 2D")
    run_thermal_2d(output_dir)

    print("[5/6] Convergence Analysis")
    run_convergence(output_dir, tables_dir)

    print("[6/6] Summary")
    figures = list(output_dir.glob("*.png"))
    csvs = list(tables_dir.glob("*.csv"))
    print("=" * 60)
    print(f"Done. {len(figures)} figures, {len(csvs)} CSV(s) generated:")
    for f in sorted(figures):
        print(f"  - {f.name}")
    for c in sorted(csvs):
        print(f"  - {c.name}")
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
