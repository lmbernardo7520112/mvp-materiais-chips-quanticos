"""C1 surface-density bookkeeping — ADR-009 Accepted.

This module implements **only** the C1 dimensional chain:

    D_it [eV⁻¹·cm⁻²] → D_it_SI [J⁻¹·m⁻²] → N_it [m⁻²] → σ_eff [C/m²]

Scope limitations (enforced by design):

- Does **not** compute ρ_eff (volume charge density).
- Does **not** use t_eff (effective thickness).
- Does **not** couple to the PDE solver.
- Does **not** produce physical φ (potential).
- Does **not** change runtime ``option_c_enabled``.
- Does **not** calibrate device behavior.
- C2/C3 are out of scope.
"""

from __future__ import annotations

import math

from mvp_quantum_materials.units import ELEMENTARY_CHARGE

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Conversion factor: D_it [eV⁻¹·cm⁻²] → D_it_SI [J⁻¹·m⁻²].
#:
#: ``D_it_SI = D_it × 10⁴ / q_e``
#:
#: - ``10⁴`` converts cm⁻² → m⁻².
#: - ``1/q_e`` converts eV⁻¹ → J⁻¹.
DIT_EV_CM2_TO_J_M2_FACTOR: float = 1.0e4 / ELEMENTARY_CHARGE


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def convert_dit_ev_cm2_to_j_m2(d_it: float) -> float:
    """Convert interface-trap density from eV⁻¹·cm⁻² to J⁻¹·m⁻².

    Parameters
    ----------
    d_it:
        Interface-trap density in eV⁻¹·cm⁻².  Must be finite and ≥ 0.

    Returns
    -------
    float
        D_it_SI in J⁻¹·m⁻².
    """
    if not math.isfinite(d_it) or d_it < 0:
        msg = f"d_it must be finite and >= 0, got {d_it}"
        raise ValueError(msg)
    return d_it * DIT_EV_CM2_TO_J_M2_FACTOR


def compute_nit_areal_density(
    d_it_si: float,
    delta_e_window: float,
) -> float:
    """Compute areal trap density N_it = D_it_SI × δE_window.

    Parameters
    ----------
    d_it_si:
        Interface-trap density in J⁻¹·m⁻².  Must be finite and ≥ 0.
    delta_e_window:
        Energy integration window in J.  Must be explicitly provided,
        finite, and > 0.  A silent default is **never** acceptable.

    Returns
    -------
    float
        N_it in m⁻².
    """
    if not isinstance(d_it_si, (int, float)) or not math.isfinite(d_it_si):
        msg = f"d_it_si must be a finite number, got {d_it_si}"
        raise ValueError(msg)
    if d_it_si < 0:
        msg = f"d_it_si must be >= 0, got {d_it_si}"
        raise ValueError(msg)

    if delta_e_window is None:
        msg = "delta_e_window must be explicitly provided (got None)"
        raise ValueError(msg)
    if not isinstance(delta_e_window, (int, float)) or not math.isfinite(
        delta_e_window,
    ):
        msg = f"delta_e_window must be a finite number, got {delta_e_window}"
        raise ValueError(msg)
    if delta_e_window <= 0:
        msg = f"delta_e_window must be > 0, got {delta_e_window}"
        raise ValueError(msg)

    return d_it_si * delta_e_window


def compute_sigma_eff(
    n_it: float,
    s_charge: int,
    f_occ: float,
) -> float:
    """Compute effective surface charge density σ_eff = s_charge × q_e × N_it × f_occ.

    Parameters
    ----------
    n_it:
        Areal trap density in m⁻².  Must be finite and ≥ 0.
    s_charge:
        Sign convention.  Must be exactly ``-1`` or ``+1``.
    f_occ:
        Occupancy fraction.  Must be in ``[0, 1]``.

    Returns
    -------
    float
        σ_eff in C/m².
    """
    if not isinstance(n_it, (int, float)) or not math.isfinite(n_it):
        msg = f"n_it must be a finite number, got {n_it}"
        raise ValueError(msg)
    if n_it < 0:
        msg = f"n_it must be >= 0, got {n_it}"
        raise ValueError(msg)

    if s_charge not in (-1, 1) or isinstance(s_charge, bool):
        msg = f"s_charge must be exactly -1 or +1, got {s_charge}"
        raise ValueError(msg)

    if not isinstance(f_occ, (int, float)) or not math.isfinite(f_occ):
        msg = f"f_occ must be a finite number, got {f_occ}"
        raise ValueError(msg)
    if f_occ < 0 or f_occ > 1:
        msg = f"f_occ must be in [0, 1], got {f_occ}"
        raise ValueError(msg)

    return s_charge * ELEMENTARY_CHARGE * n_it * f_occ


def compute_c1_surface_charge(
    d_it: float,
    delta_e_window: float,
    s_charge: int,
    f_occ: float,
) -> float:
    """End-to-end C1 surface charge: D_it → σ_eff.

    Parameters
    ----------
    d_it:
        Interface-trap density in eV⁻¹·cm⁻².
    delta_e_window:
        Energy integration window in J.
    s_charge:
        Sign convention (``-1`` or ``+1``).
    f_occ:
        Occupancy fraction in ``[0, 1]``.

    Returns
    -------
    float
        σ_eff in C/m².
    """
    d_it_si = convert_dit_ev_cm2_to_j_m2(d_it)
    n_it = compute_nit_areal_density(d_it_si, delta_e_window)
    return compute_sigma_eff(n_it, s_charge, f_occ)
