"""RED specifications for units module — v0.4.4 SI Constants Scaffolding.

These tests define the API contract for the units module.
They are expected to FAIL (RED) until the module is implemented.

IMPORTANT: These constants are literature values, not device-specific
calibration. Using them does not constitute calibration.
"""

import pytest


class TestPhysicalConstants:
    """Test that SI physical constants are available and correct."""

    def test_epsilon_0_exists_and_positive(self):
        from mvp_quantum_materials.units import EPSILON_0

        assert EPSILON_0 > 0

    def test_epsilon_0_value(self):
        """CODATA-recommended value (CONST_DERIVED)."""
        from mvp_quantum_materials.units import EPSILON_0

        assert abs(EPSILON_0 - 8.854_187_8128e-12) / 8.854_187_8128e-12 < 1e-6

    def test_elementary_charge_exists_and_positive(self):
        from mvp_quantum_materials.units import ELEMENTARY_CHARGE

        assert ELEMENTARY_CHARGE > 0

    def test_elementary_charge_value(self):
        """SI 2019 exact value (CONST_EXACT)."""
        from mvp_quantum_materials.units import ELEMENTARY_CHARGE

        assert ELEMENTARY_CHARGE == 1.602_176_634e-19


class TestRelativePermittivity:
    """Test material-specific relative permittivity lookup."""

    def test_si_permittivity(self):
        from mvp_quantum_materials.units import relative_permittivity

        eps_r = relative_permittivity("Si")
        assert abs(eps_r - 11.7) < 0.1

    def test_sio2_permittivity(self):
        from mvp_quantum_materials.units import relative_permittivity

        eps_r = relative_permittivity("SiO2")
        assert abs(eps_r - 3.9) < 0.1

    def test_unknown_material_raises(self):
        from mvp_quantum_materials.units import relative_permittivity

        with pytest.raises(ValueError, match="Unknown material"):
            relative_permittivity("GaN")


class TestAbsolutePermittivity:
    """Test absolute permittivity calculation ε = ε_r · ε₀."""

    def test_si_absolute_permittivity(self):
        from mvp_quantum_materials.units import EPSILON_0, absolute_permittivity

        result = absolute_permittivity(11.7)
        expected = 11.7 * EPSILON_0
        assert abs(result - expected) / expected < 1e-10

    def test_negative_epsilon_r_raises(self):
        from mvp_quantum_materials.units import absolute_permittivity

        with pytest.raises(ValueError):
            absolute_permittivity(-1.0)

    def test_zero_epsilon_r_raises(self):
        from mvp_quantum_materials.units import absolute_permittivity

        with pytest.raises(ValueError):
            absolute_permittivity(0.0)


class TestUnitsDocstrings:
    """Verify that docstrings explicitly disclaim calibration."""

    def test_module_docstring_no_calibration_claim(self):
        import mvp_quantum_materials.units as units_mod

        doc = units_mod.__doc__ or ""
        assert "calibrat" in doc.lower(), "Module docstring must mention calibration disclaimer"

    def test_relative_permittivity_docstring(self):
        from mvp_quantum_materials.units import relative_permittivity

        doc = relative_permittivity.__doc__ or ""
        assert "literature" in doc.lower() or "not.*calibrat" in doc.lower(), (
            "relative_permittivity docstring must disclaim calibration"
        )
