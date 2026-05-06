"""Computational domain for 1D simulations."""

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True)
class Domain1D:
    """One-dimensional computational domain with uniform grid.

    Attributes:
        length: Total domain length [m].
        nx: Number of grid nodes.
        dx: Grid spacing [m] (computed).
        x: Array of node positions [m] (computed).
    """

    length: float
    nx: int

    @property
    def dx(self) -> float:
        """Grid spacing [m]."""
        return self.length / (self.nx - 1)

    @property
    def x(self) -> npt.NDArray[np.float64]:
        """Array of node positions [m]."""
        return np.linspace(0.0, self.length, self.nx)
