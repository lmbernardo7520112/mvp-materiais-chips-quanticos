"""Heterogeneity metrics for thermal and concentration fields.

All metrics return finite scalar values.
"""

import numpy as np
import numpy.typing as npt


def max_thermal_gradient(t_field: npt.NDArray[np.float64], dx: float) -> float:
    """Maximum absolute thermal gradient |dT/dx|.

    Args:
        t_field: Temperature field [K].
        dx: Grid spacing [m].

    Returns:
        Maximum gradient [K/m].
    """
    grad = np.abs(np.diff(t_field)) / dx
    return float(np.max(grad))


def thermal_non_uniformity(t_field: npt.NDArray[np.float64]) -> float:
    """Thermal non-uniformity: (T_max - T_min) / T_mean.

    Args:
        t_field: Temperature field [K].

    Returns:
        Non-uniformity ratio (dimensionless).
    """
    t_mean = np.mean(t_field)
    if t_mean == 0.0:
        return 0.0
    return float((np.max(t_field) - np.min(t_field)) / t_mean)


def concentration_non_uniformity(c_field: npt.NDArray[np.float64]) -> float:
    """Concentration non-uniformity: (C_max - C_min) / max(C_mean, eps).

    Args:
        c_field: Concentration field (adimensional proxy).

    Returns:
        Non-uniformity ratio.
    """
    c_mean = np.mean(c_field)
    denominator = max(c_mean, 1e-30)
    return float((np.max(c_field) - np.min(c_field)) / denominator)


def local_accumulation_index(c_field: npt.NDArray[np.float64]) -> float:
    """Local accumulation index: max(C) / max(mean(C), eps).

    Args:
        c_field: Concentration field.

    Returns:
        Accumulation ratio.
    """
    c_mean = np.mean(c_field)
    denominator = max(c_mean, 1e-30)
    return float(np.max(c_field) / denominator)


def global_c_integral(c_field: npt.NDArray[np.float64], dx: float) -> float:
    """Global integral of C over the domain: ∫C dx.

    Args:
        c_field: Concentration field.
        dx: Grid spacing [m].

    Returns:
        Integral value.
    """
    return float(np.trapz(c_field, dx=dx))


def max_over_mean_ratio(field: npt.NDArray[np.float64]) -> float:
    """Ratio max(field) / mean(field). Always >= 1 for positive fields.

    Args:
        field: Input array (positive values).

    Returns:
        Ratio value.
    """
    f_mean = np.mean(field)
    if f_mean <= 0.0:
        return 1.0
    return float(np.max(field) / f_mean)


def compute_all_metrics(
    t_field: npt.NDArray[np.float64],
    c_field: npt.NDArray[np.float64],
    dx: float,
) -> dict[str, float]:
    """Compute all heterogeneity metrics.

    Args:
        t_field: Temperature field [K].
        c_field: Concentration field (adimensional proxy).
        dx: Grid spacing [m].

    Returns:
        Dictionary with all metric values.
    """
    return {
        "max_thermal_gradient": max_thermal_gradient(t_field, dx),
        "thermal_non_uniformity": thermal_non_uniformity(t_field),
        "concentration_non_uniformity": concentration_non_uniformity(c_field),
        "local_accumulation_index": local_accumulation_index(c_field),
        "global_c_integral": global_c_integral(c_field, dx),
        "max_over_mean_c": max_over_mean_ratio(c_field),
    }
