"""
v0.5.1 C1 Validation & Demonstration Hardening

This script generates a controlled numerical demonstration of the C1
surface-density bookkeeping, showing explicit values for D_it, delta_E,
f_occ, and s_charge, without coupling to the solver.
"""

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt

from mvp_quantum_materials.surface_charge import (
    compute_c1_surface_charge,
    compute_nit_areal_density,
    convert_dit_ev_cm2_to_j_m2,
)
from mvp_quantum_materials.units import ELEMENTARY_CHARGE


def generate_c1_surface_charge_demo(output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    tables_dir = output_dir / "tables"
    figures_dir = output_dir / "figures"
    tables_dir.mkdir(exist_ok=True)
    figures_dir.mkdir(exist_ok=True)

    csv_path = tables_dir / "c1_surface_charge_demo.csv"
    fig_path = figures_dir / "c1_sigma_eff_sensitivity.png"

    # Grids
    d_its = [1e10, 1e11, 1e12]
    delta_e_windows_ev = [0.01, 0.05, 0.10]
    f_occs = [0.0, 0.25, 0.5, 1.0]
    s_charges = [-1, 1]

    rows = []

    for d_it in d_its:
        d_it_si = convert_dit_ev_cm2_to_j_m2(d_it)
        for d_e_ev in delta_e_windows_ev:
            d_e_j = d_e_ev * ELEMENTARY_CHARGE
            n_it = compute_nit_areal_density(d_it_si, d_e_j)
            for f_occ in f_occs:
                for s_charge in s_charges:
                    sigma_eff = compute_c1_surface_charge(d_it, d_e_j, s_charge, f_occ)

                    rows.append(
                        {
                            "d_it_ev_inv_cm2": d_it,
                            "delta_e_window_eV": d_e_ev,
                            "delta_e_window_J": d_e_j,
                            "f_occ": f_occ,
                            "s_charge": s_charge,
                            "d_it_si_j_inv_m2": d_it_si,
                            "n_it_m2": n_it,
                            "sigma_eff_c_m2": sigma_eff,
                            "abs_sigma_eff_c_m2": abs(sigma_eff),
                            "c1_bookkeeping_only": "True",
                            "rho_eff_present": "False",
                            "t_eff_present": "False",
                            "solver_coupled": "False",
                            "physical_interpretation_allowed": "False",
                            "option_c_enabled": "False",
                        }
                    )

    # Write CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # Generate Figure
    plt.figure(figsize=(8, 6))
    for d_e_ev in delta_e_windows_ev:
        y_vals = []
        for d_it in d_its:
            row = next(
                r
                for r in rows
                if r["d_it_ev_inv_cm2"] == d_it
                and r["delta_e_window_eV"] == d_e_ev
                and r["f_occ"] == 1.0
                and r["s_charge"] == 1
            )
            y_vals.append(row["abs_sigma_eff_c_m2"])
        plt.plot(d_its, y_vals, marker="o", label=f"ΔE = {d_e_ev} eV")

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("D_it [eV⁻¹·cm⁻²]")
    plt.ylabel("|σ_eff| [C/m²]")
    plt.title("C1 Validation: |σ_eff| vs D_it (f_occ=1.0)")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.savefig(fig_path, bbox_inches="tight", dpi=300)
    plt.close()

    return {"csv": csv_path, "figure": fig_path}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate C1 Validation Demo Artifacts")
    parser.add_argument(
        "--output-dir", type=str, default="results", help="Directory to save artifacts"
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    results = generate_c1_surface_charge_demo(output_dir)
    print(f"Generated CSV: {results['csv']}")
    print(f"Generated Figure: {results['figure']}")
