#!/usr/bin/env python3
"""Run convergence analysis and generate CSV + figure.

Usage:
    python scripts/run_convergence.py [--output-dir DIR]
"""

import argparse
from pathlib import Path

from mvp_quantum_materials.convergence import (
    export_convergence_csv,
    plot_convergence,
    run_convergence_analysis,
)


def main(output_dir: Path) -> None:
    """Run convergence analysis."""
    output_dir.mkdir(parents=True, exist_ok=True)
    tables_dir = output_dir.parent / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    print("  Running convergence analysis (nx = 11, 21, 41, 81)...")
    results = run_convergence_analysis(
        nx_values=[11, 21, 41, 81],
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

    # Print summary
    print("\n  Convergence Summary:")
    for r in results:
        order_str = f"{r['observed_order']:.2f}" if r["observed_order"] is not None else "—"
        print(
            f"    nx={r['nx']:3d}  dx={r['dx']:.2e}  "
            f"L2={r['error_l2']:.2e}  order={order_str}  "
            f"time={r['elapsed_time']:.3f}s"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run convergence analysis")
    parser.add_argument("--output-dir", type=Path, default=Path("results/figures"))
    args = parser.parse_args()
    main(args.output_dir)
