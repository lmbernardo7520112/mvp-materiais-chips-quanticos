"""Computational domains for 1D and 2D simulations."""

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


@dataclass(frozen=True)
class Domain2D:
    """Two-dimensional computational domain with uniform rectangular grid.

    Attributes:
        Lx: Domain length in x-direction [m].
        Ly: Domain length in y-direction [m].
        nx: Number of grid nodes in x-direction (>= 3).
        ny: Number of grid nodes in y-direction (>= 3).

    Note:
        This domain is demonstrative — it does not represent a real wafer slice.
    """

    Lx: float
    Ly: float
    nx: int
    ny: int

    def __post_init__(self) -> None:
        """Validate domain parameters."""
        if self.Lx <= 0:
            raise ValueError(f"Lx must be positive, got {self.Lx}")
        if self.Ly <= 0:
            raise ValueError(f"Ly must be positive, got {self.Ly}")
        if self.nx < 3:
            raise ValueError(f"nx must be >= 3, got {self.nx}")
        if self.ny < 3:
            raise ValueError(f"ny must be >= 3, got {self.ny}")

    @property
    def dx(self) -> float:
        """Grid spacing in x-direction [m]."""
        return self.Lx / (self.nx - 1)

    @property
    def dy(self) -> float:
        """Grid spacing in y-direction [m]."""
        return self.Ly / (self.ny - 1)

    @property
    def x(self) -> npt.NDArray[np.float64]:
        """Array of node positions in x-direction [m]."""
        return np.linspace(0.0, self.Lx, self.nx)

    @property
    def y(self) -> npt.NDArray[np.float64]:
        """Array of node positions in y-direction [m]."""
        return np.linspace(0.0, self.Ly, self.ny)
