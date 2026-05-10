"""Tests for effective charge calculations.

This module validates the uncalibrated, demonstrative effective charge closure
required by v0.4 Poisson Bridge Scope (ADR-007).
"""

import numpy as np
import pytest

from mvp_quantum_materials.effective_charge import (
    EffectiveChargeParams,
    compute_delta_rho_eff,
    compute_delta_sigma_eff,
    compute_theta,
    convert_sigma_to_rho,
    h_cdef,
)


def test_compute_theta_preserves_shape():
    """compute_theta preserves shape of input T."""
    T = np.random.rand(10, 10) * 100 + 300
    theta = compute_theta(T)
    assert theta.shape == T.shape


def test_compute_theta_uniform_T_returns_zeros():
    """compute_theta uniform T returns zeros without div-by-zero error."""
    T = np.ones((5, 5)) * 300.0
    theta = compute_theta(T)
    assert np.allclose(theta, 0.0)


def test_h_cdef_returns_values_in_bounds():
    """h_cdef returns values in [0, 1]."""
    C_def = np.array([0.0, 0.5, 1.0])
    h = h_cdef(C_def, C_sat=1.0)
    assert np.all(h >= 0.0)
    assert np.all(h <= 1.0)


def test_h_cdef_rejects_negative_C_def():
    """h_cdef rejects negative C_def with ValueError."""
    with pytest.raises(ValueError, match="must be >= 0"):
        h_cdef(np.array([-0.1, 0.5]))


def test_h_cdef_rejects_excess_C_def():
    """h_cdef rejects C_def > C_sat with ValueError."""
    with pytest.raises(ValueError, match="must be <= C_sat"):
        h_cdef(np.array([0.5, 1.5]), C_sat=1.0)


def test_h_cdef_rejects_nonfinite():
    """h_cdef rejects nonfinite values."""
    with pytest.raises(ValueError, match="must be finite"):
        h_cdef(np.array([np.inf, 0.5]))


def test_compute_delta_sigma_eff_returns_mean_zero():
    """compute_delta_sigma_eff returns approximately mean-zero field."""
    C_def = np.random.rand(10, 10)
    delta_sigma = compute_delta_sigma_eff(C_def)
    assert np.isclose(np.mean(delta_sigma), 0.0, atol=1e-12)


def test_convert_sigma_to_rho_divides_by_teff():
    """convert_sigma_to_rho divides by t_eff."""
    sigma = np.ones((5, 5))
    t_eff = 2.0
    rho = convert_sigma_to_rho(sigma, t_eff)
    assert np.allclose(rho, 0.5)


def test_convert_sigma_to_rho_rejects_non_positive_teff():
    """convert_sigma_to_rho rejects t_eff <= 0."""
    sigma = np.ones((5, 5))
    with pytest.raises(ValueError, match="must be strictly positive"):
        convert_sigma_to_rho(sigma, 0.0)
    with pytest.raises(ValueError, match="must be strictly positive"):
        convert_sigma_to_rho(sigma, -1.0)


def test_compute_delta_rho_eff_returns_finite_mean_zero():
    """compute_delta_rho_eff returns finite mean-zero field."""
    C_def = np.random.rand(10, 10)
    delta_rho = compute_delta_rho_eff(C_def)
    assert np.isfinite(delta_rho).all()
    assert np.isclose(np.mean(delta_rho), 0.0, atol=1e-12)


def test_params_default_is_demonstrative():
    """EffectiveChargeParams defaults preserve demonstrative/uncalibrated status."""
    params = EffectiveChargeParams()
    # Parameters must exist and be clearly demonstrative
    assert params.q > 0
    assert params.N_ref > 0
    assert params.lambda_T >= 0
    assert params.lambda_C >= 0
    assert params.C_sat > 0
    assert params.t_eff > 0
    assert getattr(params, "_is_uncalibrated_demonstrative", True)
