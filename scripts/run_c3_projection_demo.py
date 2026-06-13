import argparse
import csv
import json
import math
from pathlib import Path

from mvp_quantum_materials.c3_solver_projection import (
    BoundaryConditionMetadata,
    ProjectedC3Source,
    project_c2_source_to_grid,
    validate_projected_charge_conservation,
)


def main():
    parser = argparse.ArgumentParser(description="Run C3 Conservative Grid Projection Demo")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/figures"),
        help="Directory to save the CSV and JSON artifacts",
    )
    args = parser.parse_args()

    out_dir: Path = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Define a C2 source (e.g. a charged defect in continuous space)
    # Total source charge = +1.5e-19 C
    c2_source = {
        "x": 4.5,
        "y": 5.2,
        "total_charge": 1.5e-19,
        "source_type": "point_defect",
        "metadata": {"source_layer": "SiO2"},
    }

    # 2. Define a boundary layer metadata
    boundary_metadata = BoundaryConditionMetadata(
        boundary_type="dirichlet", metadata={"location": "edges", "value": 0.0}
    )

    # 3. Perform conservative grid projection
    # using a dummy domain object
    domain = "dummy_domain"

    projected: ProjectedC3Source = project_c2_source_to_grid(
        source=c2_source,
        domain=domain,
        grid_spacing=1.0,
        cell_area=1.0,
        bc_metadata=boundary_metadata,
        geometry_label="demo_2d_grid",
    )

    # 4. Validate conservation
    validate_projected_charge_conservation(
        source_charge=c2_source["total_charge"],
        projected_charge=projected.total_projected_charge,
        tol=1e-25,
    )

    conservation_error = abs(c2_source["total_charge"] - projected.total_projected_charge)

    # 5. Determine sign preservation
    original_sign = math.copysign(1, c2_source["total_charge"])
    projected_sign = math.copysign(1, projected.total_projected_charge)
    sign_preserved = original_sign == projected_sign

    # 6. Determine metadata preservation (we check if source_layer is in metadata)
    metadata_preserved = (
        "source_layer" in projected.metadata and projected.metadata["source_layer"] == "SiO2"
    )

    # 7. Write Summary JSON
    summary_data = {
        "total_source_charge": c2_source["total_charge"],
        "total_projected_charge": projected.total_projected_charge,
        "charge_conservation_error": conservation_error,
        "sign_preserved": sign_preserved,
        "metadata_preserved": metadata_preserved,
        "physical_interpretation_allowed": projected.physical_interpretation_allowed,
        "solver_coupling_enabled": projected.solver_coupling_enabled,
        "calibration_status": projected.calibration_status,
    }

    json_path = out_dir / "c3_projection_demo_summary.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    # 8. Write Grid to CSV
    csv_path = out_dir / "c3_projection_demo.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "charge_density"])
        for idx, val in enumerate(projected.charge_array):
            if abs(val) > 1e-25:
                writer.writerow([idx, val])


if __name__ == "__main__":
    main()
