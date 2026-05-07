"""Tests for Domain2D — T-2D-01: 2D domain coherence."""

import numpy as np
import pytest

from mvp_quantum_materials.domain import Domain2D


class TestDomain2DAttributes:
    """T-2D-01: Domain2D has coherent Lx, Ly, nx, ny, dx, dy, x, y."""

    def test_basic_attributes(self):
        """Domain2D stores Lx, Ly, nx, ny correctly."""
        domain = Domain2D(Lx=0.01, Ly=0.02, nx=11, ny=21)

        assert domain.Lx == pytest.approx(0.01)
        assert domain.Ly == pytest.approx(0.02)
        assert domain.nx == 11
        assert domain.ny == 21

    def test_dx_dy_consistency(self):
        """dx = Lx / (nx - 1), dy = Ly / (ny - 1)."""
        domain = Domain2D(Lx=0.01, Ly=0.02, nx=11, ny=21)

        assert domain.dx == pytest.approx(0.01 / 10)
        assert domain.dy == pytest.approx(0.02 / 20)

    def test_x_array_shape_and_endpoints(self):
        """x has shape (nx,), spans [0, Lx]."""
        domain = Domain2D(Lx=0.01, Ly=0.02, nx=11, ny=21)

        assert domain.x.shape == (11,)
        assert domain.x[0] == pytest.approx(0.0)
        assert domain.x[-1] == pytest.approx(0.01)

    def test_y_array_shape_and_endpoints(self):
        """y has shape (ny,), spans [0, Ly]."""
        domain = Domain2D(Lx=0.01, Ly=0.02, nx=11, ny=21)

        assert domain.y.shape == (21,)
        assert domain.y[0] == pytest.approx(0.0)
        assert domain.y[-1] == pytest.approx(0.02)

    def test_dx_dy_finite(self):
        """dx and dy are finite and positive."""
        domain = Domain2D(Lx=0.05, Ly=0.03, nx=51, ny=31)

        assert np.isfinite(domain.dx)
        assert np.isfinite(domain.dy)
        assert domain.dx > 0
        assert domain.dy > 0

    def test_x_uniform_spacing(self):
        """x array has uniform spacing equal to dx."""
        domain = Domain2D(Lx=0.05, Ly=0.03, nx=51, ny=31)

        assert np.allclose(np.diff(domain.x), domain.dx)

    def test_y_uniform_spacing(self):
        """y array has uniform spacing equal to dy."""
        domain = Domain2D(Lx=0.05, Ly=0.03, nx=51, ny=31)

        assert np.allclose(np.diff(domain.y), domain.dy)


class TestDomain2DValidation:
    """T-2D-01: Domain2D rejects invalid parameters."""

    def test_rejects_nx_below_minimum(self):
        """nx must be >= 3."""
        with pytest.raises(ValueError, match="nx"):
            Domain2D(Lx=0.01, Ly=0.02, nx=2, ny=11)

    def test_rejects_ny_below_minimum(self):
        """ny must be >= 3."""
        with pytest.raises(ValueError, match="ny"):
            Domain2D(Lx=0.01, Ly=0.02, nx=11, ny=2)

    def test_rejects_non_positive_lx(self):
        """Lx must be positive."""
        with pytest.raises(ValueError, match="Lx"):
            Domain2D(Lx=0.0, Ly=0.02, nx=11, ny=11)

    def test_rejects_non_positive_ly(self):
        """Ly must be positive."""
        with pytest.raises(ValueError, match="Ly"):
            Domain2D(Lx=0.01, Ly=-0.01, nx=11, ny=11)
