"""Demonstrative Poisson Bridge Orchestration.

This script runs a demonstrative, uncalibrated 2D effective charge and Poisson
solver pipeline. It makes no physical device-level claims and the outputs are
strictly for structural validation of the Poisson Bridge.
"""

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from mvp_quantum_materials.effective_charge import (
    EffectiveChargeParams,
    compute_delta_rho_eff,
)
from mvp_quantum_materials.poisson_solver_2d import solve_poisson_2d_demonstrative


def run_poisson_bridge(output_dir: Path, tables_dir: Path) -> None:
    """Run the demonstrative Poisson bridge pipeline."""

    output_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    # 1 & 2. Create demonstrative C_def and T fields
    nx, ny = 41, 41
    Lx, Ly = 1.0, 1.0
    x = np.linspace(0, Lx, nx)
    y = np.linspace(0, Ly, ny)
    X, Y = np.meshgrid(x, y, indexing="ij")

    # Demonstrative dimensionless defect concentration in [0, 1]
    C_def = 0.5 + 0.25 * np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly)

    # Demonstrative thermal field
    T = 300.0 + 10.0 * np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly)

    # 3. Parameters
    params = EffectiveChargeParams(
        q=1.602176634e-19,
        N_ref=1.0,
        lambda_T=0.1,
        lambda_C=1.0,
        C_sat=1.0,
        t_eff=1.0,
        T_ref=None,
        delta_T_ref=None,
    )

    # Calculate demonstrative effective charge
    delta_rho_eff = compute_delta_rho_eff(C_def, T, params=params)

    # 4. Solve Poisson
    dx = Lx / (nx - 1)
    dy = Ly / (ny - 1)
    epsilon = 1.0

    result = solve_poisson_2d_demonstrative(
        rho=delta_rho_eff,
        dx=dx,
        dy=dy,
        epsilon=epsilon,
        max_iter=20000,
        tolerance=1e-8,
    )

    # 5. Save PNG
    plt.figure(figsize=(6, 5))
    im = plt.imshow(
        result.phi.T,
        origin="lower",
        extent=(0.0, float(Lx), 0.0, float(Ly)),
        cmap="viridis",
    )
    plt.colorbar(im, label="Demonstrative Phi (a.u.)")
    plt.title("Demonstrative Poisson Bridge Potential")
    plt.xlabel("X (a.u.)")
    plt.ylabel("Y (a.u.)")
    plt.tight_layout()
    fig_path = output_dir / "poisson_bridge_potential.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()

    # 6. Save CSV
    headers = [
        "max_abs_delta_rho_eff",
        "mean_delta_rho_eff",
        "max_abs_phi",
        "solver_iterations",
        "solver_residual",
        "converged",
    ]
    row = [
        float(np.max(np.abs(delta_rho_eff))),
        float(np.mean(delta_rho_eff)),
        float(np.max(np.abs(result.phi))),
        result.iterations,
        result.residual,
        result.converged,
    ]
    csv_path = tables_dir / "poisson_bridge_metrics.csv"
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(row)

    print(f"Generated {fig_path}")
    print(f"Generated {csv_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Demonstrative Poisson Bridge.")
    parser.add_argument(
        "--output-dir", type=str, default="results/figures", help="Output directory for figures."
    )
    parser.add_argument(
        "--tables-dir", type=str, default="results/tables", help="Output directory for tables."
    )
    args = parser.parse_args()
    run_poisson_bridge(Path(args.output_dir), Path(args.tables_dir))


if __name__ == "__main__":
    main()
