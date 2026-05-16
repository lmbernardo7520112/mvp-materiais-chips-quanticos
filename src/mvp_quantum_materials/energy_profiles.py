"""Piecewise D_it(E) energy-distribution profiles for C1 bookkeeping.

**Scope: C1 energy-distribution bookkeeping only.**

This module implements piecewise-constant D_it(E) integration:

    N_it = Σ D_i × ΔE_i   [m⁻²]

and the downstream σ_eff chain:

    σ_eff = s_charge × q_e × N_it × f_occ   [C·m⁻²]

**Non-Calibration Notice:**
- All outputs carry ``calibration_status = "not_calibrated"``.
- This module does NOT predict device behavior.
- Results are bookkeeping quantities, not physical observables.

**Governance (ADR-010 + v0.5.6 amendment):**
- S0_TEST_ONLY profiles: allowed only inside test suites.
- E0 demonstrative: DEPRECATED — not accepted as operational.
- E1 literature-informed: minimum operational evidence level.
- E2 experimental-profile prior: conditional, requires full metadata.
- E3/E4: BLOCKED — require a dedicated ADR.

**What this module does NOT provide:**
- No ρ_eff (charge density per unit volume).
- No t_eff (effective thickness).
- No Poisson equation coupling.
- No physical φ interpretation.
- No C2/C3 features.
- No calibration claims.
- No device prediction.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from mvp_quantum_materials.units import ELEMENTARY_CHARGE

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Maximum plausible edge energy in Joules.
#: Silicon bandgap ≈ 1.12 eV ≈ 1.79e-19 J. We allow up to ~10 eV
#: (1.6e-18 J) to be generous, but anything above 1e-17 J (~62 eV)
#: is clearly in eV scale passed without conversion.
_MAX_PLAUSIBLE_EDGE_ENERGY_J: float = 1.0e-17

#: Allowed evidence levels for operational profiles.
_ALLOWED_EVIDENCE_LEVELS: frozenset[str] = frozenset({"S0_TEST_ONLY", "E1", "E2"})

#: Evidence levels that are blocked and must raise ValueError.
_BLOCKED_EVIDENCE_LEVELS: frozenset[str] = frozenset({"E3", "E4"})

#: Deprecated evidence levels.
_DEPRECATED_EVIDENCE_LEVELS: frozenset[str] = frozenset({"E0", "demonstrative", "toy"})

#: Required metadata keys for E2 profiles.
_E2_REQUIRED_METADATA_KEYS: frozenset[str] = frozenset(
    {
        "source",
        "technique",
        "material_stack",
        "interface",
        "energy_reference",
        "units",
        "transferability_note",
        "calibration_status",
    }
)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EnergyInterval:
    """A single energy bin for piecewise D_it(E) integration.

    Attributes
    ----------
    e_left_j : float
        Left edge of the energy interval [J].
    e_right_j : float
        Right edge of the energy interval [J].
    dit_j_inv_m2 : float
        Interface trap density in this bin [J⁻¹·m⁻²].
    """

    e_left_j: float
    e_right_j: float
    dit_j_inv_m2: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.e_left_j):
            msg = f"e_left_j must be finite, got {self.e_left_j}"
            raise ValueError(msg)
        if not math.isfinite(self.e_right_j):
            msg = f"e_right_j must be finite, got {self.e_right_j}"
            raise ValueError(msg)
        if not math.isfinite(self.dit_j_inv_m2):
            msg = f"dit_j_inv_m2 must be finite, got {self.dit_j_inv_m2}"
            raise ValueError(msg)
        if self.e_right_j <= self.e_left_j:
            msg = (
                f"Edges must be strictly increasing: "
                f"e_right_j ({self.e_right_j}) must be > e_left_j ({self.e_left_j})"
            )
            raise ValueError(msg)
        if self.dit_j_inv_m2 < 0:
            msg = f"D_it must be non-negative (>= 0), got {self.dit_j_inv_m2}"
            raise ValueError(msg)

    @property
    def width_j(self) -> float:
        """Bin width in Joules."""
        return self.e_right_j - self.e_left_j

    @property
    def contribution_m2(self) -> float:
        """N_it contribution from this bin: D_it × ΔE [m⁻²]."""
        return self.dit_j_inv_m2 * self.width_j


@dataclass(frozen=True)
class PiecewiseDitProfile:
    """Piecewise-constant D_it(E) profile for C1 energy integration.

    Parameters
    ----------
    edges_j : list[float]
        Energy bin edges in Joules. Must be strictly increasing.
        Length = N_bins + 1.
    densities_j_m2 : list[float]
        D_it values for each bin [J⁻¹·m⁻²]. Length = N_bins.
        All values must be >= 0.
    evidence_level : str
        One of "S0_TEST_ONLY", "E1", "E2".
        "E0", "demonstrative", "toy" are deprecated.
        "E3", "E4" are blocked.
    metadata : dict[str, Any] | None
        Required for E2. Must contain all keys in _E2_REQUIRED_METADATA_KEYS.
        Must have calibration_status = "not_calibrated".

    Attributes
    ----------
    intervals : tuple[EnergyInterval, ...]
        The constructed energy intervals.
    """

    edges_j: list[float]
    densities_j_m2: list[float]
    evidence_level: str
    metadata: dict[str, Any] = field(default_factory=dict)
    intervals: tuple[EnergyInterval, ...] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        # --- Validate evidence level ---
        _validate_evidence_level(self.evidence_level, self.metadata)

        # --- Validate metadata anti-calibration guards ---
        _validate_metadata_guards(self.metadata)

        # --- Validate edges ---
        if len(self.edges_j) < 2:
            msg = "At least 2 edges are required (1 bin minimum)."
            raise ValueError(msg)

        if len(self.densities_j_m2) != len(self.edges_j) - 1:
            msg = (
                f"Number of densities ({len(self.densities_j_m2)}) must equal "
                f"number of bins ({len(self.edges_j) - 1})."
            )
            raise ValueError(msg)

        # Check strictly increasing edges
        for i in range(1, len(self.edges_j)):
            if self.edges_j[i] <= self.edges_j[i - 1]:
                msg = (
                    f"Edges must be strictly increasing (monotonically ordered): "
                    f"edge[{i}]={self.edges_j[i]} <= edge[{i - 1}]={self.edges_j[i - 1]}"
                )
                raise ValueError(msg)

        # Check Joule-scale plausibility for non-zero edges
        for i, edge in enumerate(self.edges_j):
            if abs(edge) > _MAX_PLAUSIBLE_EDGE_ENERGY_J:
                msg = (
                    f"Edge energy edge[{i}]={edge} J exceeds plausible scale. "
                    f"Energies must be in Joules (not eV). "
                    f"Use eV × 1.602176634e-19 to convert."
                )
                raise ValueError(msg)

        # Check non-negative densities
        for i, d in enumerate(self.densities_j_m2):
            if d < 0:
                msg = f"D_it must be non-negative (>= 0), got densities_j_m2[{i}]={d}"
                raise ValueError(msg)

        # --- Build intervals ---
        built = tuple(
            EnergyInterval(
                e_left_j=self.edges_j[i],
                e_right_j=self.edges_j[i + 1],
                dit_j_inv_m2=self.densities_j_m2[i],
            )
            for i in range(len(self.densities_j_m2))
        )
        # frozen=True requires object.__setattr__
        object.__setattr__(self, "intervals", built)


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def integrate_piecewise_dit(profile: PiecewiseDitProfile) -> float:
    """Compute total integrated trap density N_it from a piecewise profile.

    .. math::
        N_{it} = \\sum_i D_i \\times \\Delta E_i

    Parameters
    ----------
    profile : PiecewiseDitProfile
        A validated piecewise D_it(E) profile.

    Returns
    -------
    float
        N_it in m⁻².
    """
    n_it = sum(interval.contribution_m2 for interval in profile.intervals)

    if not math.isfinite(n_it):
        msg = f"Integrated N_it is not finite: {n_it}"
        raise ValueError(msg)

    return n_it


def compute_sigma_eff_from_energy_profile(
    *,
    profile: PiecewiseDitProfile,
    s_charge: int,
    f_occ: float,
) -> float:
    """Compute σ_eff from a piecewise D_it(E) profile.

    .. math::
        \\sigma_{eff} = s_{charge} \\times q_e \\times N_{it} \\times f_{occ}

    This preserves the C1 chain: D_it(E) → N_it → σ_eff.

    Parameters
    ----------
    profile : PiecewiseDitProfile
        A validated piecewise D_it(E) profile.
    s_charge : int
        Sign of the charge: +1 or -1.
    f_occ : float
        Fractional occupancy in [0, 1].

    Returns
    -------
    float
        σ_eff in C·m⁻².

    Notes
    -----
    # This is C1 bookkeeping only — not calibrated, not device-predictive.
    """
    if s_charge not in (-1, 1):
        msg = f"s_charge must be -1 or +1, got {s_charge}"
        raise ValueError(msg)
    if not (0.0 <= f_occ <= 1.0):
        msg = f"f_occ must be in [0, 1], got {f_occ}"
        raise ValueError(msg)

    n_it = integrate_piecewise_dit(profile)

    # σ_eff = s_charge × q_e × N_it × f_occ
    # q_e = ELEMENTARY_CHARGE [C]
    # N_it [m⁻²]
    # σ_eff [C·m⁻²]
    return s_charge * ELEMENTARY_CHARGE * n_it * f_occ


# ---------------------------------------------------------------------------
# Internal validation helpers
# ---------------------------------------------------------------------------


def _validate_evidence_level(level: str, metadata: dict[str, Any] | None) -> None:
    """Validate evidence level per ADR-010 + v0.5.6 amendment."""
    if level in _DEPRECATED_EVIDENCE_LEVELS:
        msg = (
            f"Evidence level '{level}' is deprecated (E0/demonstrative/toy). "
            f"Operational profiles require E1 or E2. "
            f"Use S0_TEST_ONLY for test fixtures only."
        )
        raise ValueError(msg)

    if level in _BLOCKED_EVIDENCE_LEVELS:
        msg = (
            f"Evidence level '{level}' is blocked (E3/E4 require a dedicated ADR). "
            f"Current roadmap authorizes only E1 and E2."
        )
        raise ValueError(msg)

    if level not in _ALLOWED_EVIDENCE_LEVELS:
        msg = f"Unknown evidence level '{level}'. Allowed: S0_TEST_ONLY, E1, E2."
        raise ValueError(msg)

    # E2 requires complete metadata
    if level == "E2":
        if metadata is None:
            msg = "E2 profiles require complete source metadata."
            raise ValueError(msg)
        missing = _E2_REQUIRED_METADATA_KEYS - set(metadata.keys())
        if missing:
            msg = f"E2 profiles require complete metadata. Missing keys: {sorted(missing)}"
            raise ValueError(msg)


def _validate_metadata_guards(metadata: dict[str, Any] | None) -> None:
    """Enforce anti-calibration guards on metadata."""
    if metadata is None:
        return

    # calibration_status must be "not_calibrated"
    if "calibration_status" in metadata and metadata["calibration_status"] != "not_calibrated":
        msg = (
            f"calibration_status must be 'not_calibrated', "
            f"got '{metadata['calibration_status']}'. "
            f"Calibration claims are not authorized."
        )
        raise ValueError(msg)

    # physical_interpretation_allowed must not be True
    if metadata.get("physical_interpretation_allowed") is True:
        msg = (
            "physical_interpretation_allowed must not be True. "
            "Physical interpretation is not authorized in C1."
        )
        raise ValueError(msg)

    # option_c_enabled must not be True
    if metadata.get("option_c_enabled") is True:
        msg = (
            "option_c_enabled must not be True. "
            "Option C is not enabled in the current configuration."
        )
        raise ValueError(msg)
