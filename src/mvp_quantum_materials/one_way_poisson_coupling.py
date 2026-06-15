"""One-way Poisson coupling — demonstrative metadata adapter (v0.8.9).

This module provides a **metadata-only** adapter contract for a future
one-way coupling from the C3 projection layer toward a Poisson-class
solver.  It does **not** contain or invoke any solver, does **not**
produce physical fields, and carries no calibration or device-prediction
claims.

Authorized by ADR-016 (Accepted).

Key safety invariants enforced at construction time:

* ``physical_phi_allowed`` must remain ``False``.
* ``solver_invocation_allowed`` must remain ``False``.
* ``calibration_status`` must remain ``"not_calibrated"``.
* ``device_prediction_enabled`` must remain ``False``.
* ``interpretation_status`` is always ``"demonstrative_only"``.
* ``physical_interpretation`` is always ``False``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# ------------------------------------------------------------------
# Public metadata types
# ------------------------------------------------------------------


@dataclass
class OneWayPoissonCouplingMetadata:
    """Demonstrative-only metadata for one-way coupling contracts.

    Construction raises ``ValueError`` when any safety invariant is
    violated (e.g. ``physical_phi_allowed=True``).
    """

    # Safety-critical defaults — callers may NOT override to ``True``
    physical_phi_allowed: bool = False
    solver_invocation_allowed: bool = False
    device_prediction_enabled: bool = False

    # Fixed demonstrative markers
    interpretation_status: str = "demonstrative_only"
    physical_interpretation: bool = False
    calibration_status: str = "not_calibrated"

    # Boundary metadata — ``None`` is explicitly rejected
    boundary_type: str | None = field(default="demonstrative")

    def __post_init__(self) -> None:  # noqa: D401
        """Validate safety invariants."""
        if self.physical_phi_allowed:
            msg = "physical_phi_allowed must remain False"
            raise ValueError(msg)
        if self.solver_invocation_allowed:
            msg = "solver_invocation_allowed must remain False"
            raise ValueError(msg)
        if self.device_prediction_enabled:
            msg = "device_prediction_enabled must remain False"
            raise ValueError(msg)
        if self.calibration_status != "not_calibrated":
            msg = f"calibration_status must be 'not_calibrated', got '{self.calibration_status}'"
            raise ValueError(msg)
        if self.boundary_type is None:
            msg = "boundary_type must not be None"
            raise ValueError(msg)
        # Force demonstrative markers
        self.interpretation_status = "demonstrative_only"
        self.physical_interpretation = False


@dataclass
class PoissonInputSource:
    """Adapter carrying projected charge data for a future solver input.

    This is a demonstrative data container — it does **not** invoke
    any solver.
    """

    source_charge: float = 0.0
    projected_charge: float = 0.0
    boundary_metadata: dict[str, Any] = field(default_factory=dict)
    c3_conservation_evidence: dict[str, Any] | None = None


# ------------------------------------------------------------------
# Public builder / adapter
# ------------------------------------------------------------------


def build_poisson_input_source(
    *,
    projected_charge: Any,
    boundary_metadata: dict[str, Any] | None = None,
    c3_conservation_evidence: Any = ...,
) -> PoissonInputSource:
    """Build a :class:`PoissonInputSource` from C3-projected data.

    Raises
    ------
    ValueError
        If *boundary_metadata* is missing or *c3_conservation_evidence*
        is explicitly ``None``.
    """
    if boundary_metadata is None:
        msg = "boundary_metadata is required"
        raise ValueError(msg)
    if c3_conservation_evidence is None:
        msg = "c3_conservation_evidence must not be None"
        raise ValueError(msg)

    charge_value = (
        sum(projected_charge) if isinstance(projected_charge, list) else float(projected_charge)
    )
    return PoissonInputSource(
        source_charge=charge_value,
        projected_charge=charge_value,
        boundary_metadata=boundary_metadata,
        c3_conservation_evidence=(
            c3_conservation_evidence if c3_conservation_evidence is not ... else {}
        ),
    )


# ------------------------------------------------------------------
# Public validators
# ------------------------------------------------------------------


def validate_no_physical_phi_claim(meta: OneWayPoissonCouplingMetadata) -> None:
    """Raise if metadata implies physical phi."""
    if meta.physical_phi_allowed:
        msg = "Physical phi claims are forbidden"
        raise ValueError(msg)


def validate_no_solver_runtime_coupling(
    meta: OneWayPoissonCouplingMetadata,
) -> None:
    """Raise if metadata implies active solver coupling."""
    if meta.solver_invocation_allowed:
        msg = "Solver runtime coupling is forbidden"
        raise ValueError(msg)
