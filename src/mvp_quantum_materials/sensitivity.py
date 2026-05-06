"""Sensitivity analysis for thermal-diffusive model.

Varies ≥5 parameters and measures impact on heterogeneity metrics.
"""

from typing import Any

from mvp_quantum_materials.config import DiffusionConfig, ThermalConfig
from mvp_quantum_materials.diffusion_solver import solve_diffusion_1d
from mvp_quantum_materials.domain import Domain1D
from mvp_quantum_materials.metrics import compute_all_metrics
from mvp_quantum_materials.thermal_solver import solve_thermal_1d

# Default parameter variations for sensitivity analysis
SENSITIVITY_PARAMETERS: dict[str, list[Any]] = {
    "delta_t": [100.0, 200.0, 300.0, 400.0],
    "d0": [1e-9, 5e-9, 1e-8, 5e-8],
    "ea": [0.3, 0.4, 0.5, 0.6],
    "t_critical": [1400.0, 1450.0, 1500.0, 1550.0],
    "sigma_t": [25.0, 50.0, 75.0, 100.0],
}


def _run_single_case(
    domain: Domain1D,
    thermal_cfg: ThermalConfig,
    diffusion_cfg: DiffusionConfig,
) -> dict[str, float]:
    """Run one thermal+diffusion case and return metrics.

    Args:
        domain: Computational domain.
        thermal_cfg: Thermal configuration.
        diffusion_cfg: Diffusion configuration.

    Returns:
        Dictionary of metric values.
    """
    thermal_result = solve_thermal_1d(domain, thermal_cfg)
    diffusion_result = solve_diffusion_1d(domain, thermal_result.T_final, diffusion_cfg)
    return compute_all_metrics(
        thermal_result.T_final,
        diffusion_result.C_final,
        domain.dx,
    )


def run_sensitivity_analysis(
    nx: int = 51,
    length: float = 0.01,
    parameters: dict[str, list[Any]] | None = None,
) -> list[dict[str, Any]]:
    """Run parametric sensitivity analysis.

    Varies each parameter independently while keeping others at default.

    Args:
        nx: Number of grid nodes.
        length: Domain length [m].
        parameters: Dict of parameter names to lists of values.
            If None, uses SENSITIVITY_PARAMETERS.

    Returns:
        List of result dictionaries, each with 'parameter', 'value',
        and 'metric_value' (global_c_integral as primary metric).
    """
    if parameters is None:
        parameters = SENSITIVITY_PARAMETERS

    domain = Domain1D(length=length, nx=nx)
    results: list[dict[str, Any]] = []

    base_t_left = 1700.0
    base_t_right = 1400.0

    for param_name, values in parameters.items():
        for val in values:
            # Start from defaults
            thermal_kwargs: dict[str, Any] = {
                "t_left": base_t_left,
                "t_right": base_t_right,
                "t_init": 1500.0,
                "t_total": 0.5,
            }
            diffusion_kwargs: dict[str, Any] = {
                "t_total": 0.5,
            }

            if param_name == "delta_t":
                thermal_kwargs["t_left"] = 1500.0 + val / 2
                thermal_kwargs["t_right"] = 1500.0 - val / 2
            elif param_name == "d0":
                diffusion_kwargs["d0"] = val
            elif param_name == "ea":
                diffusion_kwargs["ea"] = val
            elif param_name == "t_critical":
                diffusion_kwargs["t_critical"] = val
            elif param_name == "sigma_t":
                diffusion_kwargs["sigma_t"] = val

            thermal_cfg = ThermalConfig(**thermal_kwargs)
            diffusion_cfg = DiffusionConfig(**diffusion_kwargs)

            metrics = _run_single_case(domain, thermal_cfg, diffusion_cfg)

            results.append(
                {
                    "parameter": param_name,
                    "value": val,
                    "metric_value": metrics["global_c_integral"],
                    "all_metrics": metrics,
                }
            )

    return results
