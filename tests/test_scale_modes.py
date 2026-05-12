"""RED specifications for scale_modes module — v0.4.4 SI Constants Scaffolding.

These tests define the API contract for the scale_modes module.
They are expected to FAIL (RED) until the module is implemented.

The scale_modes module provides metadata infrastructure to distinguish
demonstrative mode from literature-scaled constants mode. It does NOT
implement physical charge conversion (Option C).
"""


class TestScaleModeEnum:
    """Test ScaleMode enumeration exists and has required members."""

    def test_demonstrative_mode_exists(self):
        from mvp_quantum_materials.scale_modes import ScaleMode

        assert ScaleMode.DEMONSTRATIVE.value == "demonstrative"

    def test_literature_scaled_constants_mode_exists(self):
        from mvp_quantum_materials.scale_modes import ScaleMode

        assert ScaleMode.LITERATURE_SCALED_CONSTANTS.value == "literature_scaled_constants"

    def test_no_calibrated_mode(self):
        """There must be no CALIBRATED mode — it is not authorized."""
        from mvp_quantum_materials.scale_modes import ScaleMode

        members = [m.name for m in ScaleMode]
        assert "CALIBRATED" not in members
        assert "DEVICE_CALIBRATED" not in members


class TestGeometryModeEnum:
    """Test GeometryMode enumeration."""

    def test_normalized_2d_exists(self):
        from mvp_quantum_materials.scale_modes import GeometryMode

        assert GeometryMode.NORMALIZED_2D.value == "normalized_2d"


class TestPotentialInterpretationEnum:
    """Test PotentialInterpretation enumeration."""

    def test_demonstrative_exists(self):
        from mvp_quantum_materials.scale_modes import PotentialInterpretation

        assert PotentialInterpretation.DEMONSTRATIVE.value == "demonstrative"

    def test_dimensional_scaffolding_exists(self):
        from mvp_quantum_materials.scale_modes import PotentialInterpretation

        assert PotentialInterpretation.DIMENSIONAL_SCAFFOLDING.value == "dimensional_scaffolding"


class TestScaleMetadataDefaults:
    """Test ScaleMetadata default construction and safety invariants."""

    def test_default_scale_mode_is_demonstrative(self):
        from mvp_quantum_materials.scale_modes import ScaleMetadata, ScaleMode

        meta = ScaleMetadata()
        assert meta.scale_mode == ScaleMode.DEMONSTRATIVE

    def test_default_geometry_mode_is_normalized(self):
        from mvp_quantum_materials.scale_modes import GeometryMode, ScaleMetadata

        meta = ScaleMetadata()
        assert meta.geometry_mode == GeometryMode.NORMALIZED_2D

    def test_default_source_mode_is_demonstrative(self):
        from mvp_quantum_materials.scale_modes import ScaleMetadata

        meta = ScaleMetadata()
        assert meta.source_mode == "demonstrative"

    def test_default_phi_interpretation_is_demonstrative(self):
        from mvp_quantum_materials.scale_modes import PotentialInterpretation, ScaleMetadata

        meta = ScaleMetadata()
        assert meta.phi_interpretation == PotentialInterpretation.DEMONSTRATIVE

    def test_default_phi_unit_label_not_physical_volts(self):
        from mvp_quantum_materials.scale_modes import ScaleMetadata

        meta = ScaleMetadata()
        label = meta.phi_unit_label
        assert label != "V"
        assert "demonstrative" in label.lower() or "a.u." in label.lower()

    def test_default_physical_interpretation_not_allowed(self):
        from mvp_quantum_materials.scale_modes import ScaleMetadata

        meta = ScaleMetadata()
        assert meta.physical_interpretation_allowed() is False


class TestScaleMetadataLiteratureScaled:
    """Test literature-scaled constants mode behavior."""

    def test_literature_scaled_with_demonstrative_source_not_physical(self):
        """Even with ε = ε_r·ε₀, if source is demonstrative, φ is NOT physical."""
        from mvp_quantum_materials.scale_modes import ScaleMetadata, ScaleMode

        meta = ScaleMetadata(scale_mode=ScaleMode.LITERATURE_SCALED_CONSTANTS)
        assert meta.physical_interpretation_allowed() is False

    def test_literature_scaled_phi_label_includes_scaffolding(self):
        from mvp_quantum_materials.scale_modes import (
            PotentialInterpretation,
            ScaleMetadata,
            ScaleMode,
        )

        meta = ScaleMetadata(
            scale_mode=ScaleMode.LITERATURE_SCALED_CONSTANTS,
            phi_interpretation=PotentialInterpretation.DIMENSIONAL_SCAFFOLDING,
            phi_unit_label="V (scaffolding, not calibrated)",
        )
        assert "scaffolding" in meta.phi_unit_label.lower()
        assert "calibrated" in meta.phi_unit_label.lower()
        assert meta.physical_interpretation_allowed() is False


class TestScaleMetadataFields:
    """Test that ScaleMetadata exposes required fields."""

    def test_has_scale_mode_field(self):
        from mvp_quantum_materials.scale_modes import ScaleMetadata

        meta = ScaleMetadata()
        assert hasattr(meta, "scale_mode")

    def test_has_geometry_mode_field(self):
        from mvp_quantum_materials.scale_modes import ScaleMetadata

        meta = ScaleMetadata()
        assert hasattr(meta, "geometry_mode")

    def test_has_source_mode_field(self):
        from mvp_quantum_materials.scale_modes import ScaleMetadata

        meta = ScaleMetadata()
        assert hasattr(meta, "source_mode")

    def test_has_phi_interpretation_field(self):
        from mvp_quantum_materials.scale_modes import ScaleMetadata

        meta = ScaleMetadata()
        assert hasattr(meta, "phi_interpretation")

    def test_has_phi_unit_label_field(self):
        from mvp_quantum_materials.scale_modes import ScaleMetadata

        meta = ScaleMetadata()
        assert hasattr(meta, "phi_unit_label")
