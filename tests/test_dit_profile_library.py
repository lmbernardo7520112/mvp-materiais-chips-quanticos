"""RED tests for v0.6.2 curated D_it(E) profile library.

These tests define the contract for ``dit_profile_library.py``.
They must all FAIL in the RED phase (module does not yet exist).

Evidence policy:
- S0_TEST_ONLY: test fixtures only.
- E0 operational: rejected.
- E1: minimum operational.
- E2: conditional with complete metadata.
- E3/E4: blocked.

Scope guards:
- No ρ_eff, t_eff, solver coupling, Schrödinger.
- No calibration claims.
"""

from __future__ import annotations

import copy
import re

import pytest


# ---------------------------------------------------------------------------
# Test 1: Module imports
# ---------------------------------------------------------------------------


def test_library_module_imports():
    """The dit_profile_library module must be importable."""
    from mvp_quantum_materials import dit_profile_library  # noqa: F401


# ---------------------------------------------------------------------------
# Test 2: Registry non-empty
# ---------------------------------------------------------------------------


def test_list_curated_profiles_returns_non_empty_registry():
    """list_curated_dit_profiles() must return a non-empty list."""
    from mvp_quantum_materials.dit_profile_library import list_curated_dit_profiles

    profiles = list_curated_dit_profiles()
    assert isinstance(profiles, list)
    assert len(profiles) > 0


# ---------------------------------------------------------------------------
# Test 3: Nominal Si/SiO2 profile exists
# ---------------------------------------------------------------------------


def test_registry_contains_si_sio2_literature_nominal():
    """Registry must contain 'si_sio2_literature_nominal'."""
    from mvp_quantum_materials.dit_profile_library import list_curated_dit_profiles

    assert "si_sio2_literature_nominal" in list_curated_dit_profiles()


# ---------------------------------------------------------------------------
# Test 4: High-trap Si/SiO2 profile exists
# ---------------------------------------------------------------------------


def test_registry_contains_si_sio2_literature_high_trap():
    """Registry must contain 'si_sio2_literature_high_trap'."""
    from mvp_quantum_materials.dit_profile_library import list_curated_dit_profiles

    assert "si_sio2_literature_high_trap" in list_curated_dit_profiles()


# ---------------------------------------------------------------------------
# Test 5: All profiles are PiecewiseDitProfile
# ---------------------------------------------------------------------------


def test_all_registry_profiles_are_piecewise_dit_profiles():
    """Every curated profile must be a PiecewiseDitProfile instance."""
    from mvp_quantum_materials.dit_profile_library import (
        get_curated_dit_profile,
        list_curated_dit_profiles,
    )
    from mvp_quantum_materials.energy_profiles import PiecewiseDitProfile

    for pid in list_curated_dit_profiles():
        profile = get_curated_dit_profile(pid)
        assert isinstance(profile, PiecewiseDitProfile), f"{pid} is not PiecewiseDitProfile"


# ---------------------------------------------------------------------------
# Test 6: All operational profiles are E1 or E2
# ---------------------------------------------------------------------------


def test_all_operational_profiles_are_e1_or_e2():
    """No operational profile may be S0, E0, E3, or E4."""
    from mvp_quantum_materials.dit_profile_library import (
        get_curated_dit_profile,
        list_curated_dit_profiles,
    )

    for pid in list_curated_dit_profiles():
        profile = get_curated_dit_profile(pid)
        assert profile.evidence_level in ("E1", "E2"), (
            f"{pid} has evidence_level={profile.evidence_level}, expected E1 or E2"
        )


# ---------------------------------------------------------------------------
# Test 7: No demonstrative labels
# ---------------------------------------------------------------------------


def test_no_demonstrative_profile_ids_or_labels():
    """Profile IDs and metadata must not contain forbidden terms."""
    from mvp_quantum_materials.dit_profile_library import (
        get_curated_dit_profile,
        list_curated_dit_profiles,
    )

    forbidden = re.compile(r"demonstrative|toy|arbitrary|example.profile|E0", re.IGNORECASE)

    for pid in list_curated_dit_profiles():
        assert not forbidden.search(pid), f"Profile ID '{pid}' contains forbidden term"
        profile = get_curated_dit_profile(pid)
        for key, val in profile.metadata.items():
            if isinstance(val, str):
                assert not forbidden.search(val), (
                    f"Profile '{pid}' metadata['{key}'] contains forbidden term: {val}"
                )


# ---------------------------------------------------------------------------
# Test 8: Literature profiles have source metadata
# ---------------------------------------------------------------------------


def test_literature_profiles_have_source_metadata():
    """E1 profiles must have minimum source metadata."""
    from mvp_quantum_materials.dit_profile_library import (
        get_curated_dit_profile,
        list_curated_dit_profiles,
    )

    required_keys = {
        "source",
        "source_role",
        "material_stack",
        "interface",
        "units",
        "energy_reference",
        "transferability_note",
        "calibration_status",
    }

    for pid in list_curated_dit_profiles():
        profile = get_curated_dit_profile(pid)
        if profile.evidence_level == "E1":
            meta_keys = set(profile.metadata.keys())
            missing = required_keys - meta_keys
            assert not missing, f"Profile '{pid}' missing E1 metadata: {missing}"


# ---------------------------------------------------------------------------
# Test 9: E2 profile requires complete metadata
# ---------------------------------------------------------------------------


def test_e2_profile_requires_complete_metadata():
    """E2 must require extended metadata."""
    from mvp_quantum_materials.dit_profile_library import build_e2_experimental_prior_profile

    e2_required_keys = {
        "source",
        "technique",
        "material_stack",
        "interface",
        "energy_reference",
        "units",
        "transferability_note",
        "calibration_status",
        "extraction_assumptions",
        "uncertainty_note",
    }

    # Build with complete metadata — should succeed
    complete_meta = {
        "source": "Test source",
        "technique": "C-V conductance",
        "material_stack": "Si/SiO2",
        "interface": "Si(100)/SiO2",
        "energy_reference": "midgap",
        "units": "J^-1 m^-2 (internal SI)",
        "transferability_note": "Test only",
        "calibration_status": "not_calibrated",
        "extraction_assumptions": "Flat approximation",
        "uncertainty_note": "No uncertainty quantified",
    }

    profile = build_e2_experimental_prior_profile(
        edges_ev=[0.0, 0.2, 0.4],
        densities_ev_cm2=[1e10, 1e10],
        metadata=complete_meta,
    )

    assert profile.evidence_level == "E2"
    for k in e2_required_keys:
        assert k in profile.metadata, f"E2 profile missing key: {k}"


# ---------------------------------------------------------------------------
# Test 10: E2 fails without metadata
# ---------------------------------------------------------------------------


def test_e2_template_does_not_create_profile_without_metadata():
    """E2 factory must reject incomplete metadata."""
    from mvp_quantum_materials.dit_profile_library import build_e2_experimental_prior_profile

    incomplete_meta = {"source": "Test"}

    with pytest.raises((ValueError, TypeError)):
        build_e2_experimental_prior_profile(
            edges_ev=[0.0, 0.2, 0.4],
            densities_ev_cm2=[1e10, 1e10],
            metadata=incomplete_meta,
        )


# ---------------------------------------------------------------------------
# Test 11: Profiles integrate to positive N_it
# ---------------------------------------------------------------------------


def test_profiles_integrate_to_positive_nit():
    """All curated profiles must integrate to N_it >= 0."""
    from mvp_quantum_materials.dit_profile_library import (
        get_curated_dit_profile,
        list_curated_dit_profiles,
    )
    from mvp_quantum_materials.energy_profiles import integrate_piecewise_dit

    for pid in list_curated_dit_profiles():
        profile = get_curated_dit_profile(pid)
        n_it = integrate_piecewise_dit(profile)
        assert n_it >= 0, f"Profile '{pid}' has negative N_it: {n_it}"
        assert n_it > 0, f"Profile '{pid}' has zero N_it"


# ---------------------------------------------------------------------------
# Test 12: Profiles compute sigma_eff without solver
# ---------------------------------------------------------------------------


def test_profiles_compute_sigma_eff_without_solver():
    """Profiles must feed compute_sigma_eff_from_energy_profile."""
    from mvp_quantum_materials.dit_profile_library import (
        get_curated_dit_profile,
        list_curated_dit_profiles,
    )
    from mvp_quantum_materials.energy_profiles import compute_sigma_eff_from_energy_profile

    for pid in list_curated_dit_profiles():
        profile = get_curated_dit_profile(pid)
        sigma = compute_sigma_eff_from_energy_profile(
            profile=profile,
            s_charge=1,
            f_occ=0.5,
        )
        assert isinstance(sigma, float)
        assert sigma > 0


# ---------------------------------------------------------------------------
# Test 13: Internal units are SI
# ---------------------------------------------------------------------------


def test_literature_profile_units_are_si_internal():
    """Internally, energy edges must be in J and D_it in J^-1 m^-2."""
    from mvp_quantum_materials.dit_profile_library import (
        get_curated_dit_profile,
        list_curated_dit_profiles,
    )

    q_e = 1.602176634e-19  # C

    for pid in list_curated_dit_profiles():
        profile = get_curated_dit_profile(pid)
        # All edges must be < ~2 eV in Joules (< 3.2e-19 J)
        for edge in profile.edges_j:
            assert abs(edge) < 1e-17, f"Edge {edge} too large — likely eV not J"
        # D_it in J^-1 m^-2 should be large (D_it_eV_cm2 * 1e4 / q_e)
        # 1e10 eV^-1 cm^-2 → ~6.24e32 J^-1 m^-2
        for d in profile.densities_j_m2:
            assert d > 1e28, f"D_it={d} too small for SI J^-1 m^-2 scale"


# ---------------------------------------------------------------------------
# Test 14: Calibration status declared
# ---------------------------------------------------------------------------


def test_profile_metadata_declares_not_calibrated():
    """All curated profiles must declare not_calibrated."""
    from mvp_quantum_materials.dit_profile_library import (
        get_curated_dit_profile,
        list_curated_dit_profiles,
    )

    for pid in list_curated_dit_profiles():
        profile = get_curated_dit_profile(pid)
        assert profile.metadata.get("calibration_status") == "not_calibrated", (
            f"Profile '{pid}' must be not_calibrated"
        )


# ---------------------------------------------------------------------------
# Test 15: Device prediction blocked
# ---------------------------------------------------------------------------


def test_profile_metadata_blocks_device_prediction():
    """Profiles must not claim device prediction."""
    from mvp_quantum_materials.dit_profile_library import (
        get_curated_dit_profile,
        list_curated_dit_profiles,
    )

    for pid in list_curated_dit_profiles():
        profile = get_curated_dit_profile(pid)
        meta = profile.metadata
        # physical_interpretation_allowed must not be True
        assert meta.get("physical_interpretation_allowed") is not True
        # option_c_enabled must not be True
        assert meta.get("option_c_enabled") is not True
        # device_prediction_claimed must not be True
        assert meta.get("device_prediction_claimed") is not True


# ---------------------------------------------------------------------------
# Test 16: No rho_eff/t_eff/solver coupling
# ---------------------------------------------------------------------------


def test_no_rho_eff_no_t_eff_no_solver_coupling():
    """Module must not expose forbidden scope terms."""
    import mvp_quantum_materials.dit_profile_library as lib

    source = lib.__file__
    assert source is not None
    with open(source) as f:
        content = f.read()

    forbidden_patterns = [
        "compute_rho_eff",
        "convert_sigma_to_rho",
        "t_eff",
        "poisson_solver_2d",
        "solve_poisson",
    ]

    for pattern in forbidden_patterns:
        assert pattern not in content, (
            f"dit_profile_library.py must not reference '{pattern}'"
        )


# ---------------------------------------------------------------------------
# Test 17: Profile IDs are stable strings
# ---------------------------------------------------------------------------


def test_profile_ids_are_stable():
    """Profile IDs must be non-empty strings."""
    from mvp_quantum_materials.dit_profile_library import list_curated_dit_profiles

    ids = list_curated_dit_profiles()
    for pid in ids:
        assert isinstance(pid, str)
        assert len(pid) > 0
        assert pid == pid.strip()


# ---------------------------------------------------------------------------
# Test 18: Registry is deterministic
# ---------------------------------------------------------------------------


def test_profile_registry_is_deterministic():
    """Listing must return same order every time."""
    from mvp_quantum_materials.dit_profile_library import list_curated_dit_profiles

    a = list_curated_dit_profiles()
    b = list_curated_dit_profiles()
    assert a == b


# ---------------------------------------------------------------------------
# Test 19: Get returns independent copies
# ---------------------------------------------------------------------------


def test_profile_library_does_not_mutate_profiles():
    """get_curated_dit_profile must return independent objects."""
    from mvp_quantum_materials.dit_profile_library import (
        get_curated_dit_profile,
        list_curated_dit_profiles,
    )

    pid = list_curated_dit_profiles()[0]
    p1 = get_curated_dit_profile(pid)
    p2 = get_curated_dit_profile(pid)
    # Either they are the same frozen object (safe) or copies
    # Key: mutating p1's metadata dict must not affect p2
    if not isinstance(p1.metadata, type(None)):
        m1 = copy.deepcopy(p1.metadata)
        m2 = copy.deepcopy(p2.metadata)
        assert m1 == m2


# ---------------------------------------------------------------------------
# Test 20: Unknown ID raises error
# ---------------------------------------------------------------------------


def test_library_rejects_unknown_profile_id():
    """Unknown profile IDs must raise KeyError or ValueError."""
    from mvp_quantum_materials.dit_profile_library import get_curated_dit_profile

    with pytest.raises((KeyError, ValueError)):
        get_curated_dit_profile("nonexistent_profile_id_xyz")
