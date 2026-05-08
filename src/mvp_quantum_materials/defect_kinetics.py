"""Defect kinetics functions for the v0.3 reaction-diffusion model.

Provides three thermally-activated rate functions:
- D(T): Arrhenius diffusivity
- G(T): Gaussian generation window
- R(T): Arrhenius recombination rate

Note:
    All functions are demonstrative — parameters are toy/demonstrative
    unless explicitly curated from peer-reviewed literature.
    Equation forms are structurally inspired by crystal growth literature
    (Dornberger 2001, Brown 1994, Voronkov 1999) but parameter values
    are NOT calibrated for any specific defect type.
"""

import numpy as np

from mvp_quantum_materials.config import BOLTZMANN_EV


def defect_diffusivity(T: float, D0: float, E_D: float) -> float:
    """Compute Arrhenius defect diffusivity D(T) = D0 * exp(-E_D / (k_B * T)).

    Args:
        T: Temperature [K]. Must be positive.
        D0: Pre-exponential factor [m²/s]. Must be non-negative.
        E_D: Migration energy [eV]. Non-negative.

    Returns:
        Diffusivity [m²/s].

    Raises:
        ValueError: If T <= 0 or D0 < 0.

    Note:
        Demonstrative — not calibrated. D0 and E_D are toy parameters.
    """
    if T <= 0.0:
        raise ValueError(f"T must be positive, got {T}")
    if D0 < 0.0:
        raise ValueError(f"D0 must be non-negative, got {D0}")
    if D0 == 0.0:
        return 0.0
    return float(D0 * np.exp(-E_D / (BOLTZMANN_EV * T)))


def defect_generation(T: float, A_G: float, T_G: float, sigma_G: float) -> float:
    """Compute Gaussian defect generation rate G(T).

    G(T) = A_G * exp(-(T - T_G)^2 / (2 * sigma_G^2))

    Represents preferential defect generation in a critical
    temperature window during cooling.

    Args:
        T: Temperature [K]. Must be positive.
        A_G: Generation amplitude [1/s]. Must be non-negative.
        T_G: Center temperature of generation window [K].
        sigma_G: Width of generation window [K]. Must be positive.

    Returns:
        Generation rate [1/s].

    Raises:
        ValueError: If T <= 0, A_G < 0, or sigma_G <= 0.

    Note:
        Demonstrative — not calibrated.
    """
    if T <= 0.0:
        raise ValueError(f"T must be positive, got {T}")
    if A_G < 0.0:
        raise ValueError(f"A_G must be non-negative, got {A_G}")
    if sigma_G <= 0.0:
        raise ValueError(f"sigma_G must be positive, got {sigma_G}")
    return float(A_G * np.exp(-((T - T_G) ** 2) / (2.0 * sigma_G**2)))


def defect_recombination(T: float, A_R: float, E_R: float) -> float:
    """Compute Arrhenius defect recombination rate R(T).

    R(T) = A_R * exp(-E_R / (k_B * T))

    Applied as R(T) * C_def (first-order kinetics).

    Args:
        T: Temperature [K]. Must be positive.
        A_R: Pre-exponential recombination rate [1/s]. Must be non-negative.
        E_R: Recombination activation energy [eV].

    Returns:
        Recombination rate coefficient [1/s].

    Raises:
        ValueError: If T <= 0 or A_R < 0.

    Note:
        Demonstrative — not calibrated.
    """
    if T <= 0.0:
        raise ValueError(f"T must be positive, got {T}")
    if A_R < 0.0:
        raise ValueError(f"A_R must be non-negative, got {A_R}")
    if A_R == 0.0:
        return 0.0
    return float(A_R * np.exp(-E_R / (BOLTZMANN_EV * T)))
