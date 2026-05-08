"""Defect proxy metrics for v0.3 analysis.

Computes summary statistics from C_def fields. All metrics
are proxies — not calibrated physical observables.

Note:
    Demonstrative — metrics describe the adimensional C_def field,
    not real defect concentrations or charge noise.
"""

import numpy as np
import numpy.typing as npt


def compute_defect_metrics(
    C_def: npt.NDArray[np.float64],
    dx: float,
    dy: float,
    C_sat: float = 1.0,
) -> dict[str, float]:
    """Compute summary metrics from a 2D C_def field.

    Args:
        C_def: Defect-like field, shape (nx, ny). Adimensional.
        dx: Grid spacing in x [m].
        dy: Grid spacing in y [m].
        C_sat: Saturation value for boundedness check.

    Returns:
        Dict with keys: max, mean, std, integral, bounded_fraction.

    Note:
        All metrics are proxy quantities — demonstrative, not calibrated.
    """
    return {
        "max": float(np.max(C_def)),
        "mean": float(np.mean(C_def)),
        "std": float(np.std(C_def)),
        "integral": float(np.sum(C_def) * dx * dy),
        "bounded_fraction": float(
            np.sum((C_def >= 0.0) & (C_def <= C_sat)) / C_def.size
        ),
    }
