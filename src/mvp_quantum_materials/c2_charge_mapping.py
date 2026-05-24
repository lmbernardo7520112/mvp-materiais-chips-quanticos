"""
C2 mapping only.
Interface sheet source primary.
Conservative volume regularization fallback.
l_reg is numerical regularization only.
Not physical t_eff.
Not calibrated.
No solver coupling.
No physical phi interpretation.
No quantum confinement solver.
No C3.
No device prediction.
"""

from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class InterfaceSheetSource:
    sigma_c_per_m2: float
    surface_dimension: str
    geometry_label: str
    units: str = "C/m²"

    source_type: str = field(default="interface_sheet", init=False)
    physical_interpretation_allowed: bool = field(default=False, init=False)
    solver_coupling_enabled: bool = field(default=False, init=False)
    phi_physical_claim: bool = field(default=False, init=False)

    def __post_init__(self):
        if self.units not in ("C/m²", "C/m^2"):
            raise ValueError("Units must be C/m²")


@dataclass(frozen=True)
class ConservativeVolumeRegularization:
    sigma_c_per_m2: float
    l_reg: float

    rho_reg_c_per_m3: float = field(init=False)
    rho_units: str = field(default="C/m³", init=False)
    metadata: dict = field(init=False)

    def __post_init__(self):
        if self.l_reg <= 0:
            raise ValueError("l_reg must be positive and finite")
        object.__setattr__(self, "rho_reg_c_per_m3", self.sigma_c_per_m2 / self.l_reg)
        object.__setattr__(
            self,
            "metadata",
            {
                "regularization_role": "numerical",
                "not_physical_t_eff": True,
                "calibration_status": "not_calibrated",
            },
        )


def regularize_sheet_charge_to_volume(sigma: float, l_reg: float) -> float:
    return sigma / l_reg


def validate_charge_conservation(
    rho_array: np.ndarray,
    vol_array: np.ndarray,
    sigma_array: np.ndarray,
    area_array: np.ndarray,
    tolerance: float = 1e-8,
) -> bool:
    rho_sum = np.sum(rho_array * vol_array)
    sigma_sum = np.sum(sigma_array * area_array)
    return bool(np.isclose(rho_sum, sigma_sum, rtol=tolerance, atol=tolerance))


@dataclass(frozen=True)
class DepthPriorMetadata:
    trap_family: str
    source: str = ""
    source_role: str = ""
    material_stack: str = ""
    interface_or_region: str = ""
    depth_or_distribution_parameter: str = ""
    length_units: str = ""
    transferability_note: str = ""
    calibration_status: str = "not_calibrated"

    def __post_init__(self):
        if self.trap_family not in {"interface", "border", "oxide", "near_interface_oxide"}:
            raise ValueError(f"Invalid trap_family: {self.trap_family}")
        if self.calibration_status == "calibrated":
            raise ValueError("calibrated status is blocked")


@dataclass(frozen=True)
class ExperimentalDepthPriorMetadata(DepthPriorMetadata):
    technique: str = ""
    extraction_assumptions: str = ""
    uncertainty_note: str = ""
    temperature_or_bias_context: str = ""


def build_interface_sheet_source(sigma: float, **kwargs) -> InterfaceSheetSource:
    if "generic_thickness" in kwargs:
        raise ValueError("generic_thickness is rejected")
    return InterfaceSheetSource(
        sigma_c_per_m2=sigma, surface_dimension="1D", geometry_label="default"
    )
