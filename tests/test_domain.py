"""Tests for Domain1D — T-01: domain coherence."""

import numpy as np
import pytest


def test_domain_1d_attributes():
    """T-01: Domain1D has coherent length, nx, dx, and x array."""
    from mvp_quantum_materials.domain import Domain1D

    domain = Domain1D(length=0.01, nx=101)

    assert domain.length == pytest.approx(0.01)
    assert domain.nx == 101
    assert domain.dx == pytest.approx(0.01 / (101 - 1))
    assert len(domain.x) == 101
    assert domain.x[0] == pytest.approx(0.0)
    assert domain.x[-1] == pytest.approx(0.01)


def test_domain_1d_dx_consistency():
    """T-01b: dx is consistent with length and nx."""
    from mvp_quantum_materials.domain import Domain1D

    domain = Domain1D(length=0.05, nx=51)

    expected_dx = 0.05 / (51 - 1)
    assert domain.dx == pytest.approx(expected_dx)
    assert np.allclose(np.diff(domain.x), expected_dx)
