"""
v0.5.0 RED — C1 Surface-Density Bookkeeping Tests

These tests specify the future surface_charge module accepted by ADR-009.
In the RED phase, all tests that import from surface_charge MUST fail
with ImportError because the module does not yet exist.

Chain: D_it [eV⁻¹·cm⁻²] → D_it_SI [J⁻¹·m⁻²] → N_it [m⁻²] → σ_eff [C/m²]
"""

import math

import pytest


# ---------------------------------------------------------------------------
# Test 1 — D_it unit conversion
# ---------------------------------------------------------------------------
class TestDitConversion:
    """Verify D_it [eV⁻¹·cm⁻²] → D_it_SI [J⁻¹·m⁻²]."""

    def test_dit_ev_cm2_to_j_m2_conversion(self) -> None:
        from mvp_quantum_materials.surface_charge import convert_dit_ev_cm2_to_j_m2

        d_it = 1.0  # 1 eV⁻¹·cm⁻²
        d_it_si = convert_dit_ev_cm2_to_j_m2(d_it)

        # Expected: 1.0 × 10⁴ / 1.602176634e-19 = 6.241509074e22
        expected = 6.241509074e22
        assert d_it_si == pytest.approx(expected, rel=1e-6)
        assert d_it_si > 0


# ---------------------------------------------------------------------------
# Test 2 — δE_window must be explicit and positive
# ---------------------------------------------------------------------------
class TestDeltaEWindow:
    """δE_window must be explicit, never a silent default."""

    def test_delta_e_window_none_raises(self) -> None:
        from mvp_quantum_materials.surface_charge import compute_nit_areal_density

        with pytest.raises((TypeError, ValueError)):
            compute_nit_areal_density(d_it_si=1e22, delta_e_window=None)  # type: ignore[arg-type]

    def test_delta_e_window_zero_raises(self) -> None:
        from mvp_quantum_materials.surface_charge import compute_nit_areal_density

        with pytest.raises(ValueError):
            compute_nit_areal_density(d_it_si=1e22, delta_e_window=0.0)

    def test_delta_e_window_negative_raises(self) -> None:
        from mvp_quantum_materials.surface_charge import compute_nit_areal_density

        with pytest.raises(ValueError):
            compute_nit_areal_density(d_it_si=1e22, delta_e_window=-0.026)


# ---------------------------------------------------------------------------
# Test 3 — N_it areal density units and values
# ---------------------------------------------------------------------------
class TestNitArealDensity:
    """N_it = D_it_SI × δE_window; must be ≥ 0 and finite."""

    def test_nit_areal_density_units_and_values(self) -> None:
        from mvp_quantum_materials.surface_charge import compute_nit_areal_density

        d_it_si = 6.241509074e22  # J⁻¹·m⁻²
        delta_e_window = 4.14e-21  # kT at 300 K in J

        n_it = compute_nit_areal_density(d_it_si, delta_e_window)

        expected = d_it_si * delta_e_window
        assert n_it == pytest.approx(expected, rel=1e-6)
        assert n_it >= 0
        assert math.isfinite(n_it)


# ---------------------------------------------------------------------------
# Test 4 — Sign convention must be explicit
# ---------------------------------------------------------------------------
class TestSignConvention:
    """s_charge must be explicitly +1 or -1."""

    def test_sigma_eff_requires_sign_convention(self) -> None:
        from mvp_quantum_materials.surface_charge import compute_sigma_eff

        n_it = 1e16  # m⁻²
        f_occ = 1.0

        # Valid signs
        sigma_neg = compute_sigma_eff(n_it, s_charge=-1, f_occ=f_occ)
        sigma_pos = compute_sigma_eff(n_it, s_charge=+1, f_occ=f_occ)

        assert sigma_neg < 0
        assert sigma_pos > 0

    def test_sign_zero_raises(self) -> None:
        from mvp_quantum_materials.surface_charge import compute_sigma_eff

        with pytest.raises(ValueError):
            compute_sigma_eff(n_it=1e16, s_charge=0, f_occ=1.0)

    def test_sign_invalid_raises(self) -> None:
        from mvp_quantum_materials.surface_charge import compute_sigma_eff

        with pytest.raises(ValueError):
            compute_sigma_eff(n_it=1e16, s_charge=2, f_occ=1.0)


# ---------------------------------------------------------------------------
# Test 5 — Occupancy bounds
# ---------------------------------------------------------------------------
class TestOccupancyBounds:
    """f_occ must be in [0, 1]."""

    def test_occupancy_negative_raises(self) -> None:
        from mvp_quantum_materials.surface_charge import compute_sigma_eff

        with pytest.raises(ValueError):
            compute_sigma_eff(n_it=1e16, s_charge=-1, f_occ=-0.1)

    def test_occupancy_above_one_raises(self) -> None:
        from mvp_quantum_materials.surface_charge import compute_sigma_eff

        with pytest.raises(ValueError):
            compute_sigma_eff(n_it=1e16, s_charge=-1, f_occ=1.5)

    def test_occupancy_zero_gives_zero_sigma(self) -> None:
        from mvp_quantum_materials.surface_charge import compute_sigma_eff

        sigma = compute_sigma_eff(n_it=1e16, s_charge=-1, f_occ=0.0)
        assert sigma == 0.0

    def test_occupancy_one_is_valid(self) -> None:
        from mvp_quantum_materials.surface_charge import compute_sigma_eff

        sigma = compute_sigma_eff(n_it=1e16, s_charge=-1, f_occ=1.0)
        assert sigma != 0.0


# ---------------------------------------------------------------------------
# Test 6 — C1 does NOT create rho_eff
# ---------------------------------------------------------------------------
class TestNoRhoEff:
    """C1 module must not expose rho_eff computation."""

    def test_c1_does_not_create_rho_eff(self) -> None:
        import mvp_quantum_materials.surface_charge as sc

        assert not hasattr(sc, "compute_rho_eff")
        assert not hasattr(sc, "rho_eff")

        # Also verify the module's public API does not mention rho
        public = [name for name in dir(sc) if not name.startswith("_")]
        for name in public:
            assert "rho" not in name.lower()


# ---------------------------------------------------------------------------
# Test 7 — C1 does NOT modify solver
# ---------------------------------------------------------------------------
class TestNoSolverCoupling:
    """C1 must not import or modify the Poisson solver."""

    def test_c1_does_not_modify_solver(self) -> None:
        import importlib
        import inspect

        sc = importlib.import_module("mvp_quantum_materials.surface_charge")
        source = inspect.getsource(sc)

        # surface_charge must not import poisson_solver_2d
        assert "poisson_solver_2d" not in source
        assert "effective_charge" not in source


# ---------------------------------------------------------------------------
# Test 8 — Metadata still blocks physical phi (non-regression)
# ---------------------------------------------------------------------------
class TestMetadataBlocksPhysicalPhi:
    """Runtime metadata must still block physical interpretation."""

    def test_metadata_blocks_physical_phi(self) -> None:
        from mvp_quantum_materials.scale_modes import (
            ScaleMetadata,
            scale_metadata_to_record,
        )

        meta = ScaleMetadata()
        assert meta.physical_interpretation_allowed() is False

        record = scale_metadata_to_record(meta)
        assert record["option_c_enabled"] is False

