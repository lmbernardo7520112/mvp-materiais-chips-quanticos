"""
C2 Charge Mapping Demo — v0.7.4

Demonstrates isolated C2 charge-source mapping:
- Interface sheet source (primary)
- Conservative volume regularization (fallback)
- Charge conservation validation
- l_reg sensitivity

No solver coupling.
No Poisson runtime.
No physical phi interpretation.
No quantum confinement solver.
No C3.
No calibration claims.
No device prediction.
"""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from mvp_quantum_materials.c2_charge_mapping import (  # noqa: E402
    ConservativeVolumeRegularization,
    InterfaceSheetSource,
)


def main():
    parser = argparse.ArgumentParser(description="C2 Charge Mapping Demo")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="Output directory for CSV and figures",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    csv_dir = output_dir / "csv"
    fig_dir = output_dir / "figures"
    csv_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    # Scenarios
    sigma_values = [-1e-6, 1e-6, 5e-6]  # C/m²
    area = 1e-12  # m²
    l_reg_values = [1e-9, 2e-9, 5e-9]  # m

    rows = []
    scenario_id = 0

    for sigma in sigma_values:
        for l_reg in l_reg_values:
            scenario_id += 1

            # Create C2 objects
            source = InterfaceSheetSource(
                sigma_c_per_m2=sigma,
                surface_dimension="1D",
                geometry_label="demo",
            )
            reg = ConservativeVolumeRegularization(
                sigma_c_per_m2=sigma,
                l_reg=l_reg,
            )

            volume = area * l_reg
            total_sheet_charge = sigma * area
            total_volume_charge = reg.rho_reg_c_per_m3 * volume

            if total_sheet_charge != 0.0:
                relative_error = abs(
                    (total_volume_charge - total_sheet_charge) / total_sheet_charge
                )
            else:
                relative_error = 0.0

            rows.append(
                {
                    "scenario_id": scenario_id,
                    "sigma_c_per_m2": sigma,
                    "sigma_sign": "positive" if sigma > 0 else "negative",
                    "area_m2": area,
                    "l_reg_m": l_reg,
                    "rho_reg_c_per_m3": reg.rho_reg_c_per_m3,
                    "volume_m3": volume,
                    "total_sheet_charge_c": total_sheet_charge,
                    "total_volume_charge_c": total_volume_charge,
                    "relative_charge_error": relative_error,
                    "regularization_role": reg.metadata["regularization_role"],
                    "not_physical_t_eff": reg.metadata["not_physical_t_eff"],
                    "calibration_status": reg.metadata["calibration_status"],
                    "solver_coupling_enabled": source.solver_coupling_enabled,
                    "physical_interpretation_allowed": source.physical_interpretation_allowed,
                }
            )

    # Write CSV
    csv_path = csv_dir / "c2_charge_mapping_demo.csv"
    fieldnames = list(rows[0].keys())
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated CSV: {csv_path}")

    # Figure 1: Charge conservation
    scenario_ids = [r["scenario_id"] for r in rows]
    errors = [r["relative_charge_error"] for r in rows]

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(range(len(scenario_ids)), errors, color="steelblue")
    ax1.set_xticks(range(len(scenario_ids)))
    ax1.set_xticklabels([str(s) for s in scenario_ids])
    ax1.set_xlabel("Scenario ID")
    ax1.set_ylabel("Relative Charge Error")
    ax1.set_title("C2 Charge Conservation Sanity Check")
    ax1.set_ylim(-1e-15, max(1e-15, max(errors) * 1.5))
    fig1.tight_layout()
    fig1_path = fig_dir / "c2_charge_conservation.png"
    fig1.savefig(fig1_path, dpi=150)
    plt.close(fig1)
    print(f"Generated Figure: {fig1_path}")

    # Figure 2: l_reg sensitivity
    l_reg_arr = np.array(l_reg_values)
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    for sigma in sigma_values:
        rho_vals = [abs(sigma / lr) for lr in l_reg_values]
        label = f"σ = {sigma:.1e} C/m²"
        ax2.plot(l_reg_arr * 1e9, rho_vals, "o-", label=label)
    ax2.set_xlabel("l_reg [nm]")
    ax2.set_ylabel("|ρ_reg| [C/m³]")
    ax2.set_title("C2 ρ_reg Sensitivity to l_reg")
    ax2.legend()
    ax2.set_yscale("log")
    fig2.tight_layout()
    fig2_path = fig_dir / "c2_l_reg_sensitivity.png"
    fig2.savefig(fig2_path, dpi=150)
    plt.close(fig2)
    print(f"Generated Figure: {fig2_path}")


if __name__ == "__main__":
    main()
