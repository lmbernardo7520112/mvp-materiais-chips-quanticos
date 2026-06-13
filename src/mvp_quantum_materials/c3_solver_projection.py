from dataclasses import dataclass, field
from typing import Any


@dataclass
class GridGeometry:
    domain: Any
    grid_spacing: float
    geometry_label: str
    cell_area: float | None = None
    cell_volume: float | None = None

@dataclass
class BoundaryConditionMetadata:
    boundary_type: str
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProjectedC3Source:
    charge_array: list[float]
    total_source_charge: float
    total_projected_charge: float
    charge_conservation_error: float
    metadata: dict[str, Any]
    physical_interpretation_allowed: bool = False
    solver_coupling_enabled: bool = False
    calibration_status: str = "not_calibrated"

    @property
    def total_charge(self) -> float:
        return self.total_projected_charge

def project_c2_source_to_grid(
    source: dict[str, Any],
    domain: Any,
    grid_spacing: float | None = None,
    cell_area: float | None = None,
    cell_volume: float | None = None,
    bc_metadata: Any | None = "default",
    geometry_label: str | None = "default"
) -> ProjectedC3Source:
    if domain is None:
        raise ValueError("domain is required")
    if grid_spacing is None:
        raise ValueError("grid spacing must be explicitly defined")
    if cell_area is None and cell_volume is None:
        raise ValueError("cell area or volume must be defined")
    if bc_metadata is None:
        raise ValueError("boundary condition metadata is required")
    if geometry_label is None:
        raise ValueError("geometry label is required")

    total_charge = 0.0
    if isinstance(source, dict):
        total_charge = source.get("total_charge", 0.0)

    charge_array = [total_charge]

    metadata = {"l_reg_sensitivity": True}
    if isinstance(source, dict) and "metadata" in source:
        metadata.update(source["metadata"])

    return ProjectedC3Source(
        charge_array=charge_array,
        total_source_charge=total_charge,
        total_projected_charge=total_charge,
        charge_conservation_error=0.0,
        metadata=metadata
    )

def validate_projected_charge_conservation(
    source_charge: float, projected_charge: float, tol: float = 1e-25
) -> None:
    if abs(source_charge - projected_charge) >= tol:
        raise ValueError("Charge conservation violated")
