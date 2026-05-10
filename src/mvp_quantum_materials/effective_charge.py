"""Effective charge calculations.

This module provides demonstrative only, uncalibrated effective charge closure
functions. It is not predictive of semiconductor electrostatics and makes no
device-level claims. `C_def` remains dimensionless and `delta_rho_eff` is an
effective perturbation source, not calibrated charge density.
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class EffectiveChargeParams:
    """Parameters for effective charge calculation.

    All default parameters are demonstrative and uncalibrated.
    """

    q: float = 1.602176634e-19
    N_ref: float = 1.0
    lambda_T: float = 0.0  # noqa: N815
    lambda_C: float = 1.0  # noqa: N815
    C_sat: float = 1.0
    t_eff: float = 1.0
    T_ref: float | None = None
    delta_T_ref: float | None = None  # noqa: N815
    _is_uncalibrated_demonstrative: bool = True


def compute_theta(
    T: np.ndarray,
    T_ref: float | None = None,
    delta_T_ref: float | None = None,
) -> np.ndarray:
    """Compute dimensionless thermal activation parameter theta.

    Demonstrative only.
    """
    if not np.isfinite(T).all():
        raise ValueError("T must be a finite array.")

    t_ref_val = np.mean(T) if T_ref is None else T_ref
    dt_ref_val = (np.max(T) - np.min(T)) if delta_T_ref is None else delta_T_ref

    if dt_ref_val == 0.0:
        return np.zeros_like(T)
    if dt_ref_val < 0.0:
        raise ValueError("delta_T_ref must be > 0.")

    return (T - t_ref_val) / dt_ref_val


def h_cdef(C_def: np.ndarray, C_sat: float = 1.0) -> np.ndarray:
    """Compute dimensionless normalized defect concentration.

    Demonstrative only. C_def remains dimensionless.
    """
    if not np.isfinite(C_def).all():
        raise ValueError("C_def must be finite.")
    if C_sat <= 0:
        raise ValueError("C_sat must be > 0.")
    if np.any(C_def < 0):
        raise ValueError("C_def must be >= 0.")
    if np.any(C_def > C_sat):
        raise ValueError("C_def must be <= C_sat.")

    return C_def / C_sat


def compute_delta_sigma_eff(
    C_def: np.ndarray,
    T: np.ndarray | None = None,
    params: EffectiveChargeParams | None = None,
) -> np.ndarray:
    """Compute demonstrative effective surface charge proxy fluctuation.

    Demonstrative only, uncalibrated, not a predictive physical claim.
    """
    if params is None:
        params = EffectiveChargeParams()

    h = h_cdef(C_def, params.C_sat)

    if T is None:
        theta = np.zeros_like(C_def)
    else:
        if T.shape != C_def.shape:
            raise ValueError("T and C_def must have the same shape.")
        theta = compute_theta(T, params.T_ref, params.delta_T_ref)

    sigma_raw = params.q * params.N_ref * (1.0 + params.lambda_T * theta + params.lambda_C * h)
    delta_sigma_eff = sigma_raw - np.mean(sigma_raw)

    return delta_sigma_eff


def convert_sigma_to_rho(delta_sigma_eff: np.ndarray, t_eff: float) -> np.ndarray:
    """Convert surface charge proxy to volumetric density proxy.

    Demonstrative only.
    """
    if t_eff <= 0.0:
        raise ValueError("t_eff must be strictly positive.")
    if not np.isfinite(delta_sigma_eff).all():
        raise ValueError("delta_sigma_eff must be finite.")

    return delta_sigma_eff / t_eff


def compute_delta_rho_eff(
    C_def: np.ndarray,
    T: np.ndarray | None = None,
    params: EffectiveChargeParams | None = None,
) -> np.ndarray:
    """Compute effective volumetric charge density proxy fluctuation.

    Demonstrative only. delta_rho_eff is an effective perturbation source,
    not calibrated charge density.
    """
    if params is None:
        params = EffectiveChargeParams()

    delta_sigma_eff = compute_delta_sigma_eff(C_def, T, params)
    delta_rho_eff = convert_sigma_to_rho(delta_sigma_eff, params.t_eff)

    return delta_rho_eff
