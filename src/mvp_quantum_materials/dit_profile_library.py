"""Curated E1/E2 D_it(E) profile library for Si/SiO₂ interfaces.

**Scope: C1 bookkeeping input profiles only.**

This module provides a registry of curated, literature-informed
piecewise D_it(E) profiles for use with the energy_profiles API:

    D_it(E) → N_it → σ_eff

**Non-Calibration Notice:**

- All profiles carry ``calibration_status = "not_calibrated"``.
- Profiles are literature-scale approximations, NOT measured curves.
- No profile predicts device behavior or validates experimental data.

**Evidence Policy (ADR-010 + v0.5.6 amendment):**

- E1 literature-informed: minimum operational (default for curated).
- E2 experimental-profile prior: conditional, requires full metadata.
- E0 demonstrative: REJECTED — not accepted as operational.
- E3/E4: BLOCKED — require a dedicated ADR.

**Literature Basis:**

D_it ranges from ``docs/literature_review/v0.5.2_c1_literature_scale_benchmark.md``:

- Low (passivated Si/SiO₂): ~1×10¹⁰ eV⁻¹·cm⁻²
- Nominal (research-grade): ~5×10¹⁰ eV⁻¹·cm⁻²
- High (degraded): ~5×10¹¹ eV⁻¹·cm⁻²

U-shape from ``docs/literature_review/v0.5.4_energy_profile_evidence_sources.md``:

- Midgap: D_it ~ 10¹⁰ eV⁻¹·cm⁻²
- Transition: D_it ~ 5×10¹⁰ eV⁻¹·cm⁻²
- Near band edge: D_it ~ 10¹¹–10¹² eV⁻¹·cm⁻²

**What this module does NOT provide:**

- No ρ_eff (charge density per unit volume).
- No t_eff (effective thickness).
- No Poisson equation coupling.
- No quantum confinement solver.
- No C2/C3 features.
- No calibration claims.
- No device prediction.
"""

from __future__ import annotations

import copy
from collections import OrderedDict
from typing import Any

from mvp_quantum_materials.energy_profiles import PiecewiseDitProfile
from mvp_quantum_materials.units import ELEMENTARY_CHARGE

# ---------------------------------------------------------------------------
# Unit conversion helpers
# ---------------------------------------------------------------------------

# D_it conversion: eV⁻¹·cm⁻² → J⁻¹·m⁻²
# D_it_SI = D_it_eV_cm2 × 1e4 / q_e
_CM2_TO_M2: float = 1.0e4  # 1 cm⁻² = 10⁴ m⁻²


def _dit_ev_cm2_to_j_m2(dit_ev_cm2: float) -> float:
    """Convert D_it from eV⁻¹·cm⁻² to J⁻¹·m⁻²."""
    return dit_ev_cm2 * _CM2_TO_M2 / ELEMENTARY_CHARGE


def _ev_to_j(energy_ev: float) -> float:
    """Convert energy from eV to J."""
    return energy_ev * ELEMENTARY_CHARGE


# ---------------------------------------------------------------------------
# Common metadata
# ---------------------------------------------------------------------------

_BASE_E1_METADATA: dict[str, Any] = {
    "source": "Sze & Ng (2006), Physics of Semiconductor Devices, 3rd ed.",
    "source_role": "literature_scale_range",
    "material_stack": "Si/SiO2",
    "interface": "Si(100)/thermal SiO2",
    "units": "J^-1 m^-2 (internal SI), converted from eV^-1 cm^-2",
    "energy_reference": "midgap (Si bandgap ~1.12 eV)",
    "transferability_note": (
        "Used as literature-informed scale profile, not device calibration. "
        "Actual D_it(E) depends on oxidation conditions, anneal history, "
        "and specific interface preparation."
    ),
    "calibration_status": "not_calibrated",
    "profile_shape_assumption": (
        "Transparent piecewise approximation of literature U-shape, "
        "not a measured energy-resolved curve."
    ),
    "physical_interpretation_allowed": False,
    "option_c_enabled": False,
    "device_prediction_claimed": False,
}


# ---------------------------------------------------------------------------
# E2 required metadata keys (superset of E1 + technique + extraction + uncertainty)
# ---------------------------------------------------------------------------

_E2_EXTENDED_REQUIRED_KEYS: frozenset[str] = frozenset(
    {
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
)


# ---------------------------------------------------------------------------
# Profile definitions
# ---------------------------------------------------------------------------


def _build_si_sio2_nominal() -> PiecewiseDitProfile:
    """E1 nominal Si/SiO₂ literature-informed profile (3-bin U-shape).

    D_it values:
    - Near VB edge (0.0–0.2 eV from midgap): 5×10¹⁰ eV⁻¹·cm⁻²
    - Midgap region (0.2–0.4 eV from midgap): 1×10¹⁰ eV⁻¹·cm⁻²
    - Near CB edge (0.4–0.56 eV from midgap): 5×10¹⁰ eV⁻¹·cm⁻²
    """
    edges_ev = [0.0, 0.2, 0.4, 0.56]
    densities_ev_cm2 = [5e10, 1e10, 5e10]

    meta = {**_BASE_E1_METADATA}
    meta["profile_id"] = "si_sio2_literature_nominal"
    meta["profile_description"] = (
        "3-bin U-shape: higher D_it near band edges, lower at midgap. "
        "Literature-informed nominal scale for research-grade Si/SiO2."
    )

    return PiecewiseDitProfile(
        edges_j=[_ev_to_j(e) for e in edges_ev],
        densities_j_m2=[_dit_ev_cm2_to_j_m2(d) for d in densities_ev_cm2],
        evidence_level="E1",
        metadata=meta,
    )


def _build_si_sio2_high_trap() -> PiecewiseDitProfile:
    """E1 high-trap Si/SiO₂ profile (degraded/stressed interface).

    D_it values elevated by ~10× from nominal:
    - Near VB edge: 5×10¹¹ eV⁻¹·cm⁻²
    - Midgap: 1×10¹¹ eV⁻¹·cm⁻²
    - Near CB edge: 5×10¹¹ eV⁻¹·cm⁻²
    """
    edges_ev = [0.0, 0.2, 0.4, 0.56]
    densities_ev_cm2 = [5e11, 1e11, 5e11]

    meta = {**_BASE_E1_METADATA}
    meta["source"] = (
        "Sze & Ng (2006); degraded interface upper bound from v0.5.2 literature benchmark"
    )
    meta["profile_id"] = "si_sio2_literature_high_trap"
    meta["profile_description"] = (
        "3-bin U-shape with elevated D_it representing degraded or "
        "unpassivated Si/SiO2 interface. Upper range of literature values."
    )

    return PiecewiseDitProfile(
        edges_j=[_ev_to_j(e) for e in edges_ev],
        densities_j_m2=[_dit_ev_cm2_to_j_m2(d) for d in densities_ev_cm2],
        evidence_level="E1",
        metadata=meta,
    )


def _build_si_sio2_low_trap() -> PiecewiseDitProfile:
    """E1 low-trap Si/SiO₂ profile (high-quality passivated interface).

    D_it values from lower end of literature range:
    - Near VB edge: 1×10¹⁰ eV⁻¹·cm⁻²
    - Midgap: 5×10⁹ eV⁻¹·cm⁻²
    - Near CB edge: 1×10¹⁰ eV⁻¹·cm⁻²
    """
    edges_ev = [0.0, 0.2, 0.4, 0.56]
    densities_ev_cm2 = [1e10, 5e9, 1e10]

    meta = {**_BASE_E1_METADATA}
    meta["profile_id"] = "si_sio2_literature_low_trap"
    meta["profile_description"] = (
        "3-bin U-shape with lower D_it representing high-quality "
        "passivated Si/SiO2 interface. Lower range of literature values."
    )
    meta["lower_bound_assumption"] = (
        "Midgap bin uses 5e9 eV^-1 cm^-2, slightly below the documented "
        "Si/SiO2 lower bound of 1e10. This is a conservative piecewise "
        "approximation to model the U-shape minimum, not a measured value. "
        "The 5e9 scale is consistent with Si/SiGe heterostructure midgap "
        "values (Connors et al. 2022) and represents an optimistic limit."
    )

    return PiecewiseDitProfile(
        edges_j=[_ev_to_j(e) for e in edges_ev],
        densities_j_m2=[_dit_ev_cm2_to_j_m2(d) for d in densities_ev_cm2],
        evidence_level="E1",
        metadata=meta,
    )


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

# Ordered dict ensures deterministic listing order.
_CURATED_REGISTRY: OrderedDict[str, PiecewiseDitProfile] = OrderedDict()

_CURATED_REGISTRY["si_sio2_literature_nominal"] = _build_si_sio2_nominal()
_CURATED_REGISTRY["si_sio2_literature_high_trap"] = _build_si_sio2_high_trap()
_CURATED_REGISTRY["si_sio2_literature_low_trap"] = _build_si_sio2_low_trap()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def list_curated_dit_profiles() -> list[str]:
    """Return list of curated profile IDs in deterministic order.

    Returns
    -------
    list[str]
        Profile IDs.
    """
    return list(_CURATED_REGISTRY.keys())


def get_curated_dit_profile(profile_id: str) -> PiecewiseDitProfile:
    """Retrieve a curated D_it(E) profile by ID.

    Returns a deep copy to prevent mutation of the registry.

    Parameters
    ----------
    profile_id : str
        One of the IDs returned by ``list_curated_dit_profiles()``.

    Returns
    -------
    PiecewiseDitProfile
        A copy of the curated profile.

    Raises
    ------
    KeyError
        If the profile ID is not found.
    """
    if profile_id not in _CURATED_REGISTRY:
        msg = f"Unknown profile ID: '{profile_id}'. Available: {list(_CURATED_REGISTRY.keys())}"
        raise KeyError(msg)
    return copy.deepcopy(_CURATED_REGISTRY[profile_id])


def validate_curated_dit_profile(profile: PiecewiseDitProfile) -> None:
    """Validate a profile against curated library standards.

    Checks:
    - Evidence level is E1 or E2.
    - calibration_status = "not_calibrated".
    - physical_interpretation_allowed is not True.
    - option_c_enabled is not True.

    Parameters
    ----------
    profile : PiecewiseDitProfile
        The profile to validate.

    Raises
    ------
    ValueError
        If any validation check fails.
    """
    if profile.evidence_level not in ("E1", "E2"):
        msg = f"Curated profiles must be E1 or E2, got '{profile.evidence_level}'"
        raise ValueError(msg)

    meta = profile.metadata or {}

    if meta.get("calibration_status") != "not_calibrated":
        msg = "Curated profiles must declare calibration_status='not_calibrated'"
        raise ValueError(msg)

    if meta.get("physical_interpretation_allowed") is True:
        msg = "Curated profiles must not enable physical_interpretation_allowed"
        raise ValueError(msg)

    if meta.get("option_c_enabled") is True:
        msg = "Curated profiles must not enable option_c_enabled"
        raise ValueError(msg)


def build_literature_informed_profile(
    *,
    profile_id: str,
    edges_ev: list[float],
    densities_ev_cm2: list[float],
    source: str,
    material_stack: str = "Si/SiO2",
    interface: str = "Si(100)/thermal SiO2",
    energy_reference: str = "midgap (Si bandgap ~1.12 eV)",
    transferability_note: str = "Literature-informed scale profile, not device calibration.",
    profile_description: str = "",
) -> PiecewiseDitProfile:
    """Factory for E1 literature-informed profiles.

    Converts from eV/cm² convention to internal SI (J/m²).

    Parameters
    ----------
    profile_id : str
        Identifier for the profile.
    edges_ev : list[float]
        Energy bin edges in eV.
    densities_ev_cm2 : list[float]
        D_it values in eV⁻¹·cm⁻².
    source : str
        Literature source citation.
    material_stack : str
        Material stack description.
    interface : str
        Interface description.
    energy_reference : str
        Energy reference point.
    transferability_note : str
        Note on transferability.
    profile_description : str
        Description of the profile.

    Returns
    -------
    PiecewiseDitProfile
        E1 profile with SI-converted values.
    """
    meta: dict[str, Any] = {
        "source": source,
        "source_role": "literature_scale_range",
        "material_stack": material_stack,
        "interface": interface,
        "units": "J^-1 m^-2 (internal SI), converted from eV^-1 cm^-2",
        "energy_reference": energy_reference,
        "transferability_note": transferability_note,
        "calibration_status": "not_calibrated",
        "profile_id": profile_id,
        "profile_description": profile_description,
        "profile_shape_assumption": "Piecewise approximation of literature range.",
        "physical_interpretation_allowed": False,
        "option_c_enabled": False,
        "device_prediction_claimed": False,
    }

    return PiecewiseDitProfile(
        edges_j=[_ev_to_j(e) for e in edges_ev],
        densities_j_m2=[_dit_ev_cm2_to_j_m2(d) for d in densities_ev_cm2],
        evidence_level="E1",
        metadata=meta,
    )


def build_e2_experimental_prior_profile(
    *,
    edges_ev: list[float],
    densities_ev_cm2: list[float],
    metadata: dict[str, Any],
) -> PiecewiseDitProfile:
    """Factory for E2 experimental-profile-prior profiles.

    Requires complete metadata including extraction assumptions
    and uncertainty notes. Converts from eV/cm² to internal SI.

    Parameters
    ----------
    edges_ev : list[float]
        Energy bin edges in eV.
    densities_ev_cm2 : list[float]
        D_it values in eV⁻¹·cm⁻².
    metadata : dict[str, Any]
        Must contain all keys in _E2_EXTENDED_REQUIRED_KEYS.

    Returns
    -------
    PiecewiseDitProfile
        E2 profile with complete metadata.

    Raises
    ------
    ValueError
        If metadata is incomplete or calibration_status is not 'not_calibrated'.
    """
    # Validate extended E2 metadata
    missing = _E2_EXTENDED_REQUIRED_KEYS - set(metadata.keys())
    if missing:
        msg = f"E2 profiles require complete metadata. Missing keys: {sorted(missing)}"
        raise ValueError(msg)

    if metadata.get("calibration_status") != "not_calibrated":
        msg = "E2 profiles must declare calibration_status='not_calibrated'"
        raise ValueError(msg)

    # Ensure anti-calibration guards
    full_meta = dict(metadata)
    full_meta.setdefault("physical_interpretation_allowed", False)
    full_meta.setdefault("option_c_enabled", False)
    full_meta.setdefault("device_prediction_claimed", False)

    return PiecewiseDitProfile(
        edges_j=[_ev_to_j(e) for e in edges_ev],
        densities_j_m2=[_dit_ev_cm2_to_j_m2(d) for d in densities_ev_cm2],
        evidence_level="E2",
        metadata=full_meta,
    )
