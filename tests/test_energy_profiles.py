"""
v0.6.0 RED — Piecewise D_it(E) Energy Integration Specifications.

TDD RED phase: all tests MUST FAIL because the production module
(src/mvp_quantum_materials/energy_profiles.py) does not yet exist.

Expected failure: ModuleNotFoundError or ImportError.

Evidence policy (ADR-010 + v0.5.6 amendment):
  - S0 TEST_ONLY: fixtures inside tests only.
  - E0 demonstrative: DEPRECATED, not operational.
  - E1 literature-informed: minimum operational.
  - E2 experimental-profile prior: conditional with metadata.
  - E3/E4: BLOCKED.

Physics scope:
  - N_it = Σ D_i × ΔE_i   [m⁻²]
  - σ_eff = s_charge × q_e × N_it × f_occ   [C·m⁻²]
  - No ρ_eff, no t_eff, no solver coupling, no C2/C3.
"""

import pytest


# ---------------------------------------------------------------------------
# Test 1: Module existence
# ---------------------------------------------------------------------------
def test_energy_profiles_module_imports():
    """The energy_profiles module must be importable.

    RED: fails with ModuleNotFoundError because the module does not exist.
    GREEN (future): will pass when energy_profiles.py is created.
    """
    from mvp_quantum_materials import energy_profiles  # noqa: F401

    assert hasattr(energy_profiles, "EnergyInterval")
    assert hasattr(energy_profiles, "PiecewiseDitProfile")
    assert hasattr(energy_profiles, "integrate_piecewise_dit")
    assert hasattr(energy_profiles, "compute_sigma_eff_from_energy_profile")


# ---------------------------------------------------------------------------
# Test 2: S0 fixture — backward compatibility with P0 constant D_it
# ---------------------------------------------------------------------------
def test_s0_fixture_constant_profile_matches_current_c1_math():
    """A single-bin S0 fixture must reproduce current C1: N_it = D_it × ΔE.

    This is NOT an operational profile — it is a mathematical verification
    fixture (S0 TEST_ONLY). It must not appear in release artifacts.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials.energy_profiles import (
        PiecewiseDitProfile,
        integrate_piecewise_dit,
    )

    # S0 fixture: single bin, constant D_it
    # D_it = 1e16 J⁻¹·m⁻², ΔE = 0.32 eV = 0.32 × 1.602176634e-19 J
    d_it_value = 1e16  # J⁻¹·m⁻²
    delta_e_j = 0.32 * 1.602176634e-19  # J

    profile = PiecewiseDitProfile(
        edges_j=[0.0, delta_e_j],
        densities_j_m2=[d_it_value],
        evidence_level="S0_TEST_ONLY",
    )

    n_it = integrate_piecewise_dit(profile)

    # Expected: D_it × ΔE = 1e16 × 5.127e-20 ≈ 5.127e-4 m⁻²
    expected = d_it_value * delta_e_j
    assert abs(n_it - expected) / expected < 1e-12


# ---------------------------------------------------------------------------
# Test 3: Core piecewise integration — multi-bin
# ---------------------------------------------------------------------------
def test_piecewise_profile_integrates_segment_sum():
    """N_it = Σ D_i × (E_{i+1} - E_i) for a multi-bin profile.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials.energy_profiles import (
        PiecewiseDitProfile,
        integrate_piecewise_dit,
    )

    ev_to_j = 1.602176634e-19

    # 3-bin profile (S0 fixture for mathematical verification)
    edges_j = [0.0, 0.1 * ev_to_j, 0.2 * ev_to_j, 0.3 * ev_to_j]
    densities = [1e15, 5e15, 2e15]  # J⁻¹·m⁻²

    profile = PiecewiseDitProfile(
        edges_j=edges_j,
        densities_j_m2=densities,
        evidence_level="S0_TEST_ONLY",
    )

    n_it = integrate_piecewise_dit(profile)

    # Expected: Σ D_i × ΔE_i
    expected = sum(d * (edges_j[i + 1] - edges_j[i]) for i, d in enumerate(densities))
    assert abs(n_it - expected) / expected < 1e-12


# ---------------------------------------------------------------------------
# Test 4: Ordered, non-overlapping edges
# ---------------------------------------------------------------------------
def test_piecewise_profile_requires_ordered_non_overlapping_edges():
    """Edges must be strictly increasing. Negative intervals are rejected.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials.energy_profiles import PiecewiseDitProfile

    ev_to_j = 1.602176634e-19

    # Non-ordered edges
    with pytest.raises(ValueError, match="[Oo]rder|[Ii]ncreas|[Mm]onoton"):
        PiecewiseDitProfile(
            edges_j=[0.2 * ev_to_j, 0.1 * ev_to_j, 0.3 * ev_to_j],
            densities_j_m2=[1e15, 1e15],
            evidence_level="S0_TEST_ONLY",
        )

    # Duplicate edges (zero-width bin)
    with pytest.raises(ValueError):
        PiecewiseDitProfile(
            edges_j=[0.0, 0.1 * ev_to_j, 0.1 * ev_to_j],
            densities_j_m2=[1e15, 1e15],
            evidence_level="S0_TEST_ONLY",
        )


# ---------------------------------------------------------------------------
# Test 5: Non-negative D_it
# ---------------------------------------------------------------------------
def test_piecewise_profile_rejects_negative_dit():
    """D_it values must be >= 0. Negative values are unphysical.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials.energy_profiles import PiecewiseDitProfile

    ev_to_j = 1.602176634e-19

    with pytest.raises(ValueError, match="[Nn]egativ|>= 0|non-negative"):
        PiecewiseDitProfile(
            edges_j=[0.0, 0.1 * ev_to_j],
            densities_j_m2=[-1e15],
            evidence_level="S0_TEST_ONLY",
        )


# ---------------------------------------------------------------------------
# Test 6: Explicit Joule units
# ---------------------------------------------------------------------------
def test_energy_units_are_explicit_joules():
    """Edge energies must be in Joules. The API must not silently accept eV.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials.energy_profiles import PiecewiseDitProfile

    # If someone passes eV-scale values (e.g., 0.3) without conversion,
    # the constructor should reject or warn because D_it units are J⁻¹·m⁻².
    # Edges in eV range (~0.1–1.0) are implausibly large for J-scale energies.
    with pytest.raises((ValueError, TypeError), match="[Jj]oule|[Uu]nit|[Ss]cale"):
        PiecewiseDitProfile(
            edges_j=[0.0, 0.3],  # 0.3 J is ~1.87 × 10¹⁸ eV — implausible
            densities_j_m2=[1e15],
            evidence_level="S0_TEST_ONLY",
        )


# ---------------------------------------------------------------------------
# Test 7: E0 operational rejection
# ---------------------------------------------------------------------------
def test_operational_profiles_reject_e0():
    """E0 demonstrative is deprecated. Operational profiles must reject it.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials.energy_profiles import PiecewiseDitProfile

    ev_to_j = 1.602176634e-19

    with pytest.raises(ValueError, match="[Ee]0|[Dd]emonstrative|[Dd]eprecated"):
        PiecewiseDitProfile(
            edges_j=[0.0, 0.1 * ev_to_j],
            densities_j_m2=[1e15],
            evidence_level="E0",
        )


# ---------------------------------------------------------------------------
# Test 8: E1 acceptance
# ---------------------------------------------------------------------------
def test_operational_profiles_accept_e1():
    """E1 literature-informed is the minimum operational evidence level.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials.energy_profiles import PiecewiseDitProfile

    ev_to_j = 1.602176634e-19

    profile = PiecewiseDitProfile(
        edges_j=[0.0, 0.1 * ev_to_j],
        densities_j_m2=[1e15],
        evidence_level="E1",
    )
    assert profile.evidence_level == "E1"


# ---------------------------------------------------------------------------
# Test 9: E2 conditional — requires metadata
# ---------------------------------------------------------------------------
def test_operational_profiles_accept_e2_only_with_metadata():
    """E2 requires complete source metadata. Missing metadata → rejection.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials.energy_profiles import PiecewiseDitProfile

    ev_to_j = 1.602176634e-19

    # E2 without metadata → rejected
    with pytest.raises(ValueError, match="[Mm]etadata|[Ss]ource|E2"):
        PiecewiseDitProfile(
            edges_j=[0.0, 0.1 * ev_to_j],
            densities_j_m2=[1e15],
            evidence_level="E2",
        )

    # E2 with complete metadata → accepted
    required_metadata = {
        "source": "Fleetwood et al., IEEE TNS, 2002",
        "technique": "charge_pumping",
        "material_stack": "Si/SiO2",
        "interface": "Si-SiO2",
        "energy_reference": "midgap",
        "units": "J-1.m-2",
        "transferability_note": "Thermal oxide only",
        "calibration_status": "not_calibrated",
    }

    profile = PiecewiseDitProfile(
        edges_j=[0.0, 0.1 * ev_to_j],
        densities_j_m2=[1e15],
        evidence_level="E2",
        metadata=required_metadata,
    )
    assert profile.evidence_level == "E2"
    assert profile.metadata["calibration_status"] == "not_calibrated"


# ---------------------------------------------------------------------------
# Test 10: E3/E4 rejection
# ---------------------------------------------------------------------------
def test_operational_profiles_reject_e3_e4():
    """E3 and E4 require a dedicated ADR and are blocked.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials.energy_profiles import PiecewiseDitProfile

    ev_to_j = 1.602176634e-19

    for level in ("E3", "E4"):
        with pytest.raises(ValueError, match=f"[Ee]3|[Ee]4|[Bb]lock"):
            PiecewiseDitProfile(
                edges_j=[0.0, 0.1 * ev_to_j],
                densities_j_m2=[1e15],
                evidence_level=level,
            )


# ---------------------------------------------------------------------------
# Test 11: σ_eff chain preservation
# ---------------------------------------------------------------------------
def test_sigma_eff_from_integrated_nit_preserves_c1_chain():
    """σ_eff = s_charge × q_e × N_it × f_occ must be preserved.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials.energy_profiles import (
        PiecewiseDitProfile,
        compute_sigma_eff_from_energy_profile,
        integrate_piecewise_dit,
    )

    ev_to_j = 1.602176634e-19
    q_e = 1.602176634e-19  # C

    # S0 fixture: single bin
    profile = PiecewiseDitProfile(
        edges_j=[0.0, 0.32 * ev_to_j],
        densities_j_m2=[1e16],
        evidence_level="S0_TEST_ONLY",
    )

    s_charge = 1
    f_occ = 0.5

    sigma_eff = compute_sigma_eff_from_energy_profile(
        profile=profile,
        s_charge=s_charge,
        f_occ=f_occ,
    )

    n_it = integrate_piecewise_dit(profile)
    expected = s_charge * q_e * n_it * f_occ

    assert abs(sigma_eff - expected) / abs(expected) < 1e-12


# ---------------------------------------------------------------------------
# Test 12: No ρ_eff, no t_eff, no solver coupling
# ---------------------------------------------------------------------------
def test_no_rho_eff_no_t_eff_no_solver_coupling():
    """The energy_profiles module must NOT expose C2+ features.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials import energy_profiles

    # Must not have ρ_eff or t_eff
    assert not hasattr(energy_profiles, "compute_rho_eff")
    assert not hasattr(energy_profiles, "convert_sigma_to_rho")
    assert not hasattr(energy_profiles, "t_eff")
    assert not hasattr(energy_profiles, "compute_t_eff")

    # Must not import poisson_solver_2d
    import inspect

    source = inspect.getsource(energy_profiles)
    assert "poisson_solver_2d" not in source
    assert "solver" not in source.lower().split("# ")[0]  # ignore comments


# ---------------------------------------------------------------------------
# Test 13: Anti-calibration metadata
# ---------------------------------------------------------------------------
def test_metadata_blocks_calibration_claims():
    """All operational profiles must maintain non-calibration status.

    RED: fails because energy_profiles module does not exist.
    """
    from mvp_quantum_materials.energy_profiles import PiecewiseDitProfile

    ev_to_j = 1.602176634e-19

    # Attempting to set calibration_status to anything other than
    # "not_calibrated" must be rejected
    with pytest.raises(ValueError, match="[Cc]alibrat"):
        PiecewiseDitProfile(
            edges_j=[0.0, 0.1 * ev_to_j],
            densities_j_m2=[1e15],
            evidence_level="E1",
            metadata={"calibration_status": "calibrated"},
        )

    # Attempting to enable physical_interpretation must be rejected
    with pytest.raises(ValueError, match="[Pp]hysical|[Ii]nterpretation"):
        PiecewiseDitProfile(
            edges_j=[0.0, 0.1 * ev_to_j],
            densities_j_m2=[1e15],
            evidence_level="E1",
            metadata={"physical_interpretation_allowed": True},
        )

    # Attempting to enable option_c must be rejected
    with pytest.raises(ValueError, match="[Oo]ption.*[Cc]|option_c"):
        PiecewiseDitProfile(
            edges_j=[0.0, 0.1 * ev_to_j],
            densities_j_m2=[1e15],
            evidence_level="E1",
            metadata={"option_c_enabled": True},
        )
