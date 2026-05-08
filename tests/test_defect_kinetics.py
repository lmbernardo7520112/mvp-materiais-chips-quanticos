"""Tests for defect kinetics functions: D(T), G(T), R(T).

All kinetics are demonstrative — not calibrated to real silicon defects.
"""

import numpy as np
import pytest

from mvp_quantum_materials.defect_kinetics import (
    defect_diffusivity,
    defect_generation,
    defect_recombination,
)


class TestDefectDiffusivity:
    """Tests for Arrhenius diffusivity D(T) = D0 * exp(-E_D / (k_B * T))."""

    def test_positive_and_finite(self):
        """T-KIN-01: D(T) returns positive finite values."""
        D = defect_diffusivity(T=1200.0, D0=1e-4, E_D=0.4)
        assert D > 0.0
        assert np.isfinite(D)

    def test_increases_with_temperature(self):
        """T-KIN-02: D(T) increases with T for E_D > 0."""
        D_low = defect_diffusivity(T=800.0, D0=1e-4, E_D=0.4)
        D_high = defect_diffusivity(T=1200.0, D0=1e-4, E_D=0.4)
        assert D_high > D_low

    def test_rejects_invalid_temperature(self):
        """T-KIN-07a: Rejects T <= 0."""
        with pytest.raises(ValueError, match="T must be positive"):
            defect_diffusivity(T=0.0, D0=1e-4, E_D=0.4)
        with pytest.raises(ValueError, match="T must be positive"):
            defect_diffusivity(T=-100.0, D0=1e-4, E_D=0.4)

    def test_rejects_negative_d0(self):
        """T-KIN-07b: Rejects D0 < 0."""
        with pytest.raises(ValueError, match="D0 must be non-negative"):
            defect_diffusivity(T=1000.0, D0=-1e-4, E_D=0.4)

    def test_zero_d0_gives_zero(self):
        """D0=0 should give D=0."""
        assert defect_diffusivity(T=1000.0, D0=0.0, E_D=0.4) == 0.0


class TestDefectGeneration:
    """Tests for Gaussian generation G(T) = A_G * exp(-(T-T_G)^2/(2*sigma^2))."""

    def test_peak_near_t_g(self):
        """T-KIN-03: G(T) reaches maximum near T_G."""
        G_peak = defect_generation(T=1100.0, A_G=1.0, T_G=1100.0, sigma_G=100.0)
        G_off = defect_generation(T=900.0, A_G=1.0, T_G=1100.0, sigma_G=100.0)
        assert G_peak > G_off
        assert np.isclose(G_peak, 1.0, rtol=1e-10)

    def test_non_negative_and_finite(self):
        """T-KIN-04: G(T) is non-negative and finite."""
        for T in [300.0, 800.0, 1100.0, 1500.0, 2000.0]:
            G = defect_generation(T=T, A_G=1.0, T_G=1100.0, sigma_G=100.0)
            assert G >= 0.0
            assert np.isfinite(G)

    def test_rejects_invalid_params(self):
        """T-KIN-07c: Rejects T<=0, A_G<0, sigma_G<=0."""
        with pytest.raises(ValueError, match="T must be positive"):
            defect_generation(T=0.0, A_G=1.0, T_G=1100.0, sigma_G=100.0)
        with pytest.raises(ValueError, match="A_G must be non-negative"):
            defect_generation(T=1000.0, A_G=-1.0, T_G=1100.0, sigma_G=100.0)
        with pytest.raises(ValueError, match="sigma_G must be positive"):
            defect_generation(T=1000.0, A_G=1.0, T_G=1100.0, sigma_G=0.0)


class TestDefectRecombination:
    """Tests for Arrhenius recombination R(T) = A_R * exp(-E_R/(k_B*T))."""

    def test_positive_and_finite(self):
        """T-KIN-05: R(T) returns positive finite values."""
        R = defect_recombination(T=1200.0, A_R=10.0, E_R=0.6)
        assert R > 0.0
        assert np.isfinite(R)

    def test_increases_with_temperature(self):
        """T-KIN-06: R(T) increases with T for E_R > 0."""
        R_low = defect_recombination(T=800.0, A_R=10.0, E_R=0.6)
        R_high = defect_recombination(T=1200.0, A_R=10.0, E_R=0.6)
        assert R_high > R_low

    def test_rejects_invalid_params(self):
        """T-KIN-07d: Rejects T<=0, A_R<0."""
        with pytest.raises(ValueError, match="T must be positive"):
            defect_recombination(T=0.0, A_R=10.0, E_R=0.6)
        with pytest.raises(ValueError, match="A_R must be non-negative"):
            defect_recombination(T=1000.0, A_R=-10.0, E_R=0.6)
