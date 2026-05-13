"""Scale mode metadata infrastructure for the MVP Quantum Materials project.

This module provides enumerations and a metadata dataclass to distinguish
**demonstrative mode** (default) from **literature-scaled constants mode**
(Option B from ADR-008).

.. important::

    This is **scale metadata only** — Option B scaffolding. It does NOT:

    - Implement D_it → D_it_SI conversion.
    - Implement σ_eff or ρ_eff physical computation.
    - Implement t_eff physical conversion.
    - Provide calibrated device electrostatics.
    - Authorize physical interpretation of φ.

    Literature-scaled constants (ε = ε_r · ε₀) change the solver
    permittivity coefficient but do **not** make φ physically interpretable if
    δρ_eff and domain geometry remain demonstrative.

    **Demonstrative mode is preserved as the default.** Any code that
    does not explicitly opt into a different mode will use demonstrative
    defaults where physical interpretation is disallowed.

See Also
--------
ADR-008 — v0.4.2 SI Unit Conversion & Parameter Scale Audit (Accepted).
units : SI constants scaffolding module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ScaleMode(Enum):
    """Operating scale mode for the simulation.

    - ``DEMONSTRATIVE``: all parameters at placeholder/unit values.
      This is the default and does not claim physical meaning.
    - ``LITERATURE_SCALED_CONSTANTS``: physical constants (ε₀, ε_r)
      at literature values, but source term and geometry remain
      demonstrative. This is **dimensional scaffolding only** —
      it does not constitute calibration.

    There is intentionally **no** ``CALIBRATED`` or ``DEVICE_CALIBRATED``
    mode. Device-level calibration is not authorized by ADR-008.
    """

    DEMONSTRATIVE = "demonstrative"
    LITERATURE_SCALED_CONSTANTS = "literature_scaled_constants"


class GeometryMode(Enum):
    """Domain geometry classification.

    - ``NORMALIZED_2D``: domain is [0, 1] × [0, 1], dimensionless.
      This is the only mode currently implemented.

    Future modes (e.g., physical 2D cross-section) would require
    a dedicated ADR and implementation PR.
    """

    NORMALIZED_2D = "normalized_2d"


class PotentialInterpretation(Enum):
    """Classification of the electrostatic potential φ output.

    - ``DEMONSTRATIVE``: φ has no physical meaning; arbitrary units.
    - ``DIMENSIONAL_SCAFFOLDING``: φ has SI-consistent dimensions (volts)
      but must not be interpreted as a physical device prediction.
      The magnitude is only meaningful as an order-of-magnitude check.
    """

    DEMONSTRATIVE = "demonstrative"
    DIMENSIONAL_SCAFFOLDING = "dimensional_scaffolding"


@dataclass
class ScaleMetadata:
    """Metadata record describing the scale regime of a simulation run.

    All defaults are **safe demonstrative values**. Physical interpretation
    of φ is disallowed unless all of scale mode, geometry, and source are
    physically scaled — which is not possible in v0.4.x (Option B only).

    Parameters
    ----------
    scale_mode : ScaleMode
        The operating scale mode. Default: ``DEMONSTRATIVE``.
    geometry_mode : GeometryMode
        The domain geometry classification. Default: ``NORMALIZED_2D``.
    source_mode : str
        Description of the charge source regime. Default: ``"demonstrative"``.
    phi_interpretation : PotentialInterpretation
        How φ should be interpreted. Default: ``DEMONSTRATIVE``.
    phi_unit_label : str
        Human-readable label for φ units. Default: ``"demonstrative (a.u.)"``.
    """

    scale_mode: ScaleMode = field(default=ScaleMode.DEMONSTRATIVE)
    geometry_mode: GeometryMode = field(default=GeometryMode.NORMALIZED_2D)
    source_mode: str = field(default="demonstrative")
    phi_interpretation: PotentialInterpretation = field(
        default=PotentialInterpretation.DEMONSTRATIVE,
    )
    phi_unit_label: str = field(default="demonstrative (a.u.)")

    def physical_interpretation_allowed(self) -> bool:
        """Return whether φ may be given a physical interpretation.

        Physical interpretation requires **all** of:

        1. Scale mode is not demonstrative.
        2. Geometry mode is not normalized (i.e., physical domain).
        3. Source mode is not demonstrative.

        In v0.4.x (Option B), this always returns ``False`` because
        even with literature-scaled constants, the source term and/or
        geometry remain demonstrative.

        Returns
        -------
        bool
            ``True`` only if all three conditions are met.
            Currently always ``False`` under Option B.
        """
        if self.scale_mode == ScaleMode.DEMONSTRATIVE:
            return False
        if self.geometry_mode == GeometryMode.NORMALIZED_2D:
            return False
        return self.source_mode != "demonstrative"


def scale_metadata_to_record(metadata: ScaleMetadata) -> dict[str, object]:
    """Serialize a :class:`ScaleMetadata` instance to a flat dict.

    The returned dict contains only governance-safe metadata fields
    suitable for inclusion in CSV headers, JSON records, or audit logs.
    No Option C fields are included.

    Parameters
    ----------
    metadata : ScaleMetadata
        The metadata instance to serialize.

    Returns
    -------
    dict[str, object]
        Flat record with the following keys:

        - ``scale_mode`` — string value of the scale mode enum.
        - ``geometry_mode`` — string value of the geometry mode enum.
        - ``source_mode`` — source regime description.
        - ``physical_interpretation_allowed`` — bool, always ``False``
          under Option B.
        - ``literature_scaled_constants_available`` — bool, ``True``
          if the scaffolding module is present.
        - ``option_c_enabled`` — bool, always ``False``.
        - ``numerical_values_modified`` — bool, always ``False``
          (metadata-only integration does not change numerics).

    .. important::
        This is metadata-only serialization. It does NOT imply
        calibration, physical interpretation, or Option C enablement.
    """
    return {
        "scale_mode": metadata.scale_mode.value,
        "geometry_mode": metadata.geometry_mode.value,
        "source_mode": metadata.source_mode,
        "physical_interpretation_allowed": metadata.physical_interpretation_allowed(),
        "literature_scaled_constants_available": True,
        "option_c_enabled": False,
        "numerical_values_modified": False,
    }


def attach_scale_metadata_to_metrics(
    metrics: dict[str, object],
    metadata: ScaleMetadata,
) -> dict[str, object]:
    """Merge scale metadata into a metrics dict without mutating the original.

    This produces a new dict containing all original metric keys with their
    exact values, plus the governance-safe metadata fields from
    :func:`scale_metadata_to_record`.

    Parameters
    ----------
    metrics : dict[str, object]
        Original metrics dict (not mutated).
    metadata : ScaleMetadata
        The metadata instance to attach.

    Returns
    -------
    dict[str, object]
        New dict with original metrics preserved and metadata appended.

    Raises
    ------
    ValueError
        If ``metadata.physical_interpretation_allowed()`` returns ``True``.
        Physical interpretation is not authorized under Option B.

    .. important::
        Numeric values in *metrics* are never modified. The returned dict
        is a new object — the original *metrics* dict is not mutated.
    """
    if metadata.physical_interpretation_allowed():
        msg = (
            "Cannot attach metadata with physical_interpretation_allowed=True. "
            "Physical interpretation is not authorized under Option B."
        )
        raise ValueError(msg)

    result = dict(metrics)
    result.update(scale_metadata_to_record(metadata))
    return result
