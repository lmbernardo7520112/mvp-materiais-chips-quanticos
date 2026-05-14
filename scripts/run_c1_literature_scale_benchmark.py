"""
v0.5.2 C1 Literature Scale Benchmark

Generates a benchmark CSV and positioning figure comparing C1 sigma_eff
values against literature-scale ranges for D_it, delta_E_window, and
occupancy. Does NOT calibrate the model or predict device behavior.
"""

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt

from mvp_quantum_materials.surface_charge import compute_c1_surface_charge
from mvp_quantum_materials.units import ELEMENTARY_CHARGE

# Benchmark scenarios from decision brief
SCENARIOS = [
    {
        "scenario": "low_clean",
        "d_it": 1e10,
        "de_ev": 0.05,
        "f_occ": 0.50,
        "s_charge": 1,
        "scale_class": "literature_plausible_low",
        "evidence_tier": "T2",
    },
    {
        "scenario": "low_clean_neg",
        "d_it": 1e10,
        "de_ev": 0.05,
        "f_occ": 0.50,
        "s_charge": -1,
        "scale_class": "literature_plausible_low",
        "evidence_tier": "T2",
    },
    {
        "scenario": "nominal",
        "d_it": 5e10,
        "de_ev": 0.05,
        "f_occ": 0.50,
        "s_charge": 1,
        "scale_class": "literature_plausible_nominal",
        "evidence_tier": "T2",
    },
    {
        "scenario": "nominal_neg",
        "d_it": 5e10,
        "de_ev": 0.05,
        "f_occ": 0.50,
        "s_charge": -1,
        "scale_class": "literature_plausible_nominal",
        "evidence_tier": "T2",
    },
    {
        "scenario": "nominal_wide",
        "d_it": 5e10,
        "de_ev": 0.10,
        "f_occ": 0.50,
        "s_charge": 1,
        "scale_class": "literature_plausible_nominal",
        "evidence_tier": "T2",
    },
    {
        "scenario": "nominal_full_occ",
        "d_it": 5e10,
        "de_ev": 0.05,
        "f_occ": 1.00,
        "s_charge": 1,
        "scale_class": "literature_plausible_nominal",
        "evidence_tier": "T2",
    },
    {
        "scenario": "nominal_zero_occ",
        "d_it": 5e10,
        "de_ev": 0.05,
        "f_occ": 0.00,
        "s_charge": 1,
        "scale_class": "literature_plausible_nominal",
        "evidence_tier": "T2",
    },
    {
        "scenario": "high_degraded",
        "d_it": 5e11,
        "de_ev": 0.05,
        "f_occ": 0.50,
        "s_charge": 1,
        "scale_class": "literature_plausible_high",
        "evidence_tier": "T3",
    },
    {
        "scenario": "high_degraded_neg",
        "d_it": 5e11,
        "de_ev": 0.05,
        "f_occ": 0.50,
        "s_charge": -1,
        "scale_class": "literature_plausible_high",
        "evidence_tier": "T3",
    },
    {
        "scenario": "aggressive",
        "d_it": 1e12,
        "de_ev": 0.10,
        "f_occ": 1.00,
        "s_charge": 1,
        "scale_class": "aggressive_upper_bound",
        "evidence_tier": "T3",
    },
    {
        "scenario": "aggressive_neg",
        "d_it": 1e12,
        "de_ev": 0.10,
        "f_occ": 1.00,
        "s_charge": -1,
        "scale_class": "aggressive_upper_bound",
        "evidence_tier": "T3",
    },
]


def generate_c1_literature_scale_benchmark(
    output_dir: Path,
) -> dict[str, Path]:
    """Generate benchmark CSV and positioning figure."""
    output_dir.mkdir(parents=True, exist_ok=True)

    tables_dir = output_dir / "tables"
    figures_dir = output_dir / "figures"
    tables_dir.mkdir(exist_ok=True)
    figures_dir.mkdir(exist_ok=True)

    csv_path = tables_dir / "c1_literature_scale_benchmark.csv"
    fig_path = figures_dir / "c1_literature_scale_positioning.png"

    rows = []
    for sc in SCENARIOS:
        delta_e_j = sc["de_ev"] * ELEMENTARY_CHARGE
        sigma_eff = compute_c1_surface_charge(sc["d_it"], delta_e_j, sc["s_charge"], sc["f_occ"])

        rows.append(
            {
                "scenario": sc["scenario"],
                "d_it_ev_inv_cm2": sc["d_it"],
                "delta_e_window_eV": sc["de_ev"],
                "f_occ": sc["f_occ"],
                "s_charge": sc["s_charge"],
                "sigma_eff_c_m2": sigma_eff,
                "abs_sigma_eff_c_m2": abs(sigma_eff),
                "scale_class": sc["scale_class"],
                "evidence_tier": sc["evidence_tier"],
                "calibration_status": "not_calibrated",
                "device_prediction_claimed": "False",
                "solver_coupled": "False",
                "rho_eff_present": "False",
                "t_eff_present": "False",
            }
        )

    # Write CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # Generate positioning figure
    pos_rows = [r for r in rows if r["f_occ"] > 0 and r["s_charge"] == 1]

    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {
        "literature_plausible_low": "#2196F3",
        "literature_plausible_nominal": "#4CAF50",
        "literature_plausible_high": "#FF9800",
        "aggressive_upper_bound": "#F44336",
    }

    for row in pos_rows:
        ax.barh(
            row["scenario"],
            row["abs_sigma_eff_c_m2"],
            color=colors.get(row["scale_class"], "#9E9E9E"),
            edgecolor="black",
            linewidth=0.5,
        )

    ax.set_xscale("log")
    ax.set_xlabel("|σ_eff| [C/m²]")
    ax.set_title("C1 Literature Scale Positioning\n(NOT calibrated — benchmark only)")
    ax.grid(True, which="both", ls="--", alpha=0.3, axis="x")

    # Legend
    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor=c, edgecolor="black", label=lbl) for lbl, c in colors.items()
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=8)

    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()

    return {"csv": csv_path, "figure": fig_path}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate C1 Literature Scale Benchmark")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="Directory to save artifacts",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    results = generate_c1_literature_scale_benchmark(output_dir)
    print(f"Generated CSV: {results['csv']}")
    print(f"Generated Figure: {results['figure']}")
