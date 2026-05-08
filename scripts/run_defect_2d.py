#!/usr/bin/env python3
"""Run 2D defect reaction-diffusion simulation and generate outputs.

Produces:
- C_def contour plot (demonstrative — not calibrated)
- Defect metrics CSV
- C_def final snapshot CSV (for future v0.4 coupling)

Usage:
    python scripts/run_defect_2d.py [--output-dir DIR] [--table-dir DIR]
"""

import argparse
import csv
from pathlib import Path

import numpy as np

from mvp_quantum_materials.defect_metrics import compute_defect_metrics
from mvp_quantum_materials.defect_solver_2d import solve_defect_2d
from mvp_quantum_materials.domain import Domain2D
from mvp_quantum_materials.thermal_solver_2d import solve_thermal_2d


def main(output_dir: Path, table_dir: Path) -> None:
    """Run defect 2D simulation and generate all outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)

    # Domain
    domain = Domain2D(Lx=0.01, Ly=0.01, nx=51, ny=51)

    # Step 1: Generate thermal field (reuse v0.2 approach)
    print("  [1/4] Generating thermal field...")
    T_init = np.full((domain.nx, domain.ny), 1500.0)
    T_init[0, :] = 1400.0
    T_init[-1, :] = 1400.0
    T_init[:, 0] = 1400.0
    T_init[:, -1] = 1400.0

    thermal_result = solve_thermal_2d(
        domain=domain,
        T_init=T_init,
        alpha=8.8e-5,
        t_total=0.01,
        t_boundary=1400.0,
        safety_factor=0.4,
    )

    # Step 2: Run defect solver with thermal field
    print("  [2/4] Solving defect reaction-diffusion 2D...")
    defect_result = solve_defect_2d(
        domain=domain,
        T_field=thermal_result.T_final,
        t_total=0.01,
    )

    # Step 3: Plot C_def final
    print("  [3/4] Generating defect contour plot...")
    from mvp_quantum_materials.plots import plot_defect_2d_final

    fig_path = plot_defect_2d_final(
        domain.x,
        domain.y,
        defect_result.C_def_final,
        output_dir / "defect_2d_final.png",
    )
    print(f"    Figure: {fig_path}")

    # Step 4: Metrics and CSV
    print("  [4/4] Computing metrics and exporting CSV...")
    metrics = compute_defect_metrics(
        defect_result.C_def_final,
        domain.dx,
        domain.dy,
    )

    # Metrics CSV
    metrics_path = table_dir / "defect_metrics.csv"
    with open(metrics_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value", "nature"])
        for key, val in metrics.items():
            writer.writerow([key, f"{val:.6e}", "proxy/demonstrative"])
    print(f"    CSV: {metrics_path}")

    # Final snapshot CSV for future v0.4
    snapshot_path = table_dir / "defect_final_snapshot.csv"
    with open(snapshot_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["# C_def final snapshot — adimensional proxy"])
        writer.writerow([f"# Shape: ({domain.nx}, {domain.ny})"])
        writer.writerow(["# For future v0.4 coupling: C_def → rho_eff"])
        writer.writerow(["i", "j", "x_m", "y_m", "C_def"])
        for i in range(domain.nx):
            for j in range(domain.ny):
                writer.writerow(
                    [
                        i,
                        j,
                        f"{domain.x[i]:.6e}",
                        f"{domain.y[j]:.6e}",
                        f"{defect_result.C_def_final[i, j]:.6e}",
                    ]
                )
    print(f"    CSV: {snapshot_path}")

    # Summary
    print(f"\n  Defect solver: {defect_result.n_steps} steps, dt={defect_result.dt:.4e} s")
    for key, val in metrics.items():
        print(f"    {key}: {val:.6e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run defect 2D simulation")
    parser.add_argument("--output-dir", type=Path, default=Path("results/figures"))
    parser.add_argument("--table-dir", type=Path, default=Path("results/tables"))
    args = parser.parse_args()
    main(args.output_dir, args.table_dir)
