#!/usr/bin/env python3
"""Run parametric sensitivity analysis and save results.

Usage:
    python scripts/run_sensitivity.py [--output-dir DIR]
"""

import argparse
from pathlib import Path

from mvp_quantum_materials.plots import plot_sensitivity_results
from mvp_quantum_materials.sensitivity import run_sensitivity_analysis


def main(output_dir: Path) -> None:
    """Run sensitivity analysis and generate figure."""
    print("Running sensitivity analysis (5 parameters)...")
    results = run_sensitivity_analysis()
    print(f"  {len(results)} cases evaluated")

    fig_path = plot_sensitivity_results(
        results, output_dir / "sensitivity_analysis.png"
    )
    print(f"  Figure saved: {fig_path}")

    # Print summary table
    print("\n  Parameter          | Value     | Global C Integral")
    print("  " + "-" * 55)
    for r in results:
        print(f"  {r['parameter']:20s} | {r['value']:9.4g} | {r['metric_value']:.6e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run sensitivity analysis")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("results/figures"),
    )
    args = parser.parse_args()
    main(args.output_dir)
