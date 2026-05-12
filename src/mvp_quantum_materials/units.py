"""SI constants scaffolding for the MVP Quantum Materials project.

This module provides physical constants and material property lookups
as part of **Option B — literature-scaled constants only** from ADR-008.

.. important::

    These constants are **dimensional scaffolding**. They do NOT calibrate
    the model. Using literature values for ε_r and ε₀ does not make the
    electrostatic potential φ physically interpretable. If δρ_eff and
    domain geometry remain demonstrative, φ must still be labeled
    demonstrative.

**What this module provides:**

- ``EPSILON_0``: vacuum permittivity (CONST_DERIVED / CODATA-recommended).
- ``ELEMENTARY_CHARGE``: elementary charge (CONST_EXACT / SI 2019).
- ``relative_permittivity(material)``: literature ε_r lookup.
- ``absolute_permittivity(epsilon_r)``: computes ε = ε_r · ε₀.

**What this module does NOT provide:**

- No D_it → D_it_SI conversion.
- No σ_eff or ρ_eff computation.
- No t_eff physical justification.
- No delta_E_window calculation.
- No device-level prediction or calibration.
- No physical interpretation of φ.

See Also
--------
ADR-008 — v0.4.2 SI Unit Conversion & Parameter Scale Audit (Accepted).
"""

# ---------------------------------------------------------------------------
# Physical Constants
# ---------------------------------------------------------------------------

ELEMENTARY_CHARGE: float = 1.602_176_634e-19
"""Elementary charge in coulombs (C).

This is a **CONST_EXACT** value as defined by the 2019 SI redefinition.
Its value is exact by definition.
"""

EPSILON_0: float = 8.854_187_8128e-12
"""Vacuum permittivity in farads per meter (F/m).

This is a **CONST_DERIVED** value recommended by CODATA. It is derived
from other SI constants and carries an uncertainty of ±0.0000000013e-12 F/m.
It is NOT exact in the same sense as the elementary charge.

Note: Using ε₀ alone does not calibrate the model.
"""

# ---------------------------------------------------------------------------
# Material Properties
# ---------------------------------------------------------------------------

_RELATIVE_PERMITTIVITY: dict[str, float] = {
    "si": 11.7,
    "silicon": 11.7,
    "sio2": 3.9,
    "sio₂": 3.9,
    "silicon dioxide": 3.9,
}
"""Literature-standard relative permittivity values.

These are well-established T2-tier values from semiconductor references
(e.g., Sze & Ng, "Physics of Semiconductor Devices"). They are NOT
device-specific calibration values.
"""


def relative_permittivity(material: str) -> float:
    """Return the relative permittivity ε_r for a known material.

    These are **literature reference values**, not device-specific
    calibration. Using them does not constitute calibration of the
    simulation model.

    Parameters
    ----------
    material : str
        Material name (case-insensitive). Supported: ``"Si"``,
        ``"silicon"``, ``"SiO2"``, ``"SiO₂"``, ``"silicon dioxide"``.

    Returns
    -------
    float
        Relative permittivity (dimensionless).

    Raises
    ------
    ValueError
        If *material* is empty or not recognized.
    """
    key = material.strip().lower()
    if not key:
        msg = "Material name must not be empty."
        raise ValueError(msg)
    if key not in _RELATIVE_PERMITTIVITY:
        msg = f"Unknown material: {material!r}. Supported: Si, SiO2."
        raise ValueError(msg)
    return _RELATIVE_PERMITTIVITY[key]


def absolute_permittivity(epsilon_r: float) -> float:
    """Compute absolute permittivity ε = ε_r · ε₀.

    This is a simple dimensional multiplication. It does NOT make the
    simulation physically predictive. The resulting ε value is only
    meaningful as **dimensional scaffolding** if the source term and
    domain geometry are also physically scaled.

    Parameters
    ----------
    epsilon_r : float
        Relative permittivity (must be positive and finite).

    Returns
    -------
    float
        Absolute permittivity in F/m.

    Raises
    ------
    ValueError
        If *epsilon_r* is not positive or not finite.
    """
    if not isinstance(epsilon_r, (int, float)) or epsilon_r != epsilon_r:
        msg = f"epsilon_r must be a finite positive number, got {epsilon_r!r}."
        raise ValueError(msg)
    if epsilon_r <= 0:
        msg = f"epsilon_r must be positive, got {epsilon_r}."
        raise ValueError(msg)
    return float(epsilon_r) * EPSILON_0
