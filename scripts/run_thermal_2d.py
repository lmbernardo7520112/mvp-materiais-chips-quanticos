#!/usr/bin/env python3
"""Run 2D thermal simulation and generate figure.

Usage:
    python scripts/run_thermal_2d.py [--output-dir DIR]
"""

import argparse
from pathlib import Path

import numpy as np

from mvp_quantum_materials.domain import Domain2D
from mvp_quantum_materials.plots import plot_thermal_2d_final
from mvp_quantum_materials.thermal_solver_2d import solve_thermal_2d


def main(output_dir: Path) -> None:
    """Run 2D thermal simulation."""
    output_dir.mkdir(parents=True, exist_ok=True)

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run 2D thermal simulation")
    parser.add_argument("--output-dir", type=Path, default=Path("results/figures"))
    args = parser.parse_args()
    main(args.output_dir)
