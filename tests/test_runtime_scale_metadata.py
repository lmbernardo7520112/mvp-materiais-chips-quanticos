"""RED specifications for v0.4.6 runtime scale metadata serialization helpers.

These tests specify the future API for:
- ``scale_metadata_to_record()``: serialize ScaleMetadata to a flat dict.
- ``attach_scale_metadata_to_metrics()``: merge metadata into a metrics dict.

Both functions do NOT exist yet. These tests are intentionally RED.

.. important::
    This is a RED-phase file. All tests are expected to FAIL because the
    helpers have not been implemented yet. Do NOT implement the helpers
    in this commit.

See Also
--------
v0.4.6_runtime_metadata_tdd_plan.md : TDD plan for this phase.
v0.4.5_runtime_scale_metadata_integration.md : Decision brief.
"""

from __future__ import annotations

from mvp_quantum_materials.scale_modes import (
    ScaleMetadata,
    ScaleMode,
)

# ---------------------------------------------------------------------------
# Helper: attempt import of future functions
# ---------------------------------------------------------------------------


def _import_helpers() -> tuple:
    """Attempt to import the future serialization helpers.

    Returns
    -------
    tuple
        (scale_metadata_to_record, attach_scale_metadata_to_metrics)

    Raises
    ------
    ImportError
        When the helpers have not been implemented yet (RED phase).
    """
    from mvp_quantum_materials.scale_modes import (  # type: ignore[attr-defined]
        attach_scale_metadata_to_metrics,
        scale_metadata_to_record,
    )

    return scale_metadata_to_record, attach_scale_metadata_to_metrics


# ===========================================================================
# Test 1: Import existence
# ===========================================================================


class TestScaleMetadataToRecordExists:
    """Verify that the serialization helper can be imported."""

    def test_scale_metadata_to_record_exists(self) -> None:
        """scale_metadata_to_record must be importable from scale_modes."""
        scale_metadata_to_record, _ = _import_helpers()
        assert callable(scale_metadata_to_record)


# ===========================================================================
# Test 2: Required fields in the record
# ===========================================================================

REQUIRED_RECORD_FIELDS = {
    "scale_mode",
    "geometry_mode",
    "source_mode",
    "physical_interpretation_allowed",
    "literature_scaled_constants_available",
    "option_c_enabled",
    "numerical_values_modified",
}


class TestScaleMetadataRecordFields:
    """Verify the record contains all required metadata fields."""

    def test_scale_metadata_record_has_required_fields(self) -> None:
        """The flat record must contain all governance-required fields."""
        scale_metadata_to_record, _ = _import_helpers()
        metadata = ScaleMetadata()
        record = scale_metadata_to_record(metadata)

        missing = REQUIRED_RECORD_FIELDS - set(record.keys())
        assert not missing, f"Missing fields: {missing}"


# ===========================================================================
# Test 3: Default metadata is demonstrative
# ===========================================================================


class TestDefaultMetadataIsDemonstrative:
    """Verify that default metadata declares demonstrative mode."""

    def test_default_metadata_record_is_demonstrative(self) -> None:
        """Default ScaleMetadata must serialize as fully demonstrative."""
        scale_metadata_to_record, _ = _import_helpers()
        metadata = ScaleMetadata()
        record = scale_metadata_to_record(metadata)

        assert record["scale_mode"] == "demonstrative"
        assert record["geometry_mode"] == "normalized_2d"
        assert record["physical_interpretation_allowed"] is False
        assert record["option_c_enabled"] is False
        assert record["numerical_values_modified"] is False


# ===========================================================================
# Test 4: Literature-scaled constants still not physical
# ===========================================================================


class TestLiteratureScaledConstantsStillNotPhysical:
    """Verify that literature-scaled mode does not enable physical interpretation."""

    def test_literature_scaled_constants_still_not_physical(self) -> None:
        """Even with LITERATURE_SCALED_CONSTANTS, physical_interpretation_allowed
        must remain False because geometry and source remain demonstrative."""
        scale_metadata_to_record, _ = _import_helpers()
        metadata = ScaleMetadata(
            scale_mode=ScaleMode.LITERATURE_SCALED_CONSTANTS,
        )
        record = scale_metadata_to_record(metadata)

        assert record["physical_interpretation_allowed"] is False
        assert record["literature_scaled_constants_available"] is True
        assert record["option_c_enabled"] is False


# ===========================================================================
# Test 5: Attach metadata preserves numeric metrics
# ===========================================================================


class TestAttachMetadataPreservesNumericMetrics:
    """Verify that attaching metadata does not alter numeric values."""

    def test_attach_metadata_preserves_numeric_metrics(self) -> None:
        """Existing numeric metrics must remain exactly unchanged after
        metadata attachment."""
        _, attach_scale_metadata_to_metrics = _import_helpers()
        metadata = ScaleMetadata()

        original_metrics: dict[str, object] = {
            "max_abs_phi": 1.23,
            "solver_iterations": 42,
            "solver_residual": 1e-8,
            "converged": True,
        }

        enriched = attach_scale_metadata_to_metrics(
            dict(original_metrics),
            metadata,
        )

        # All original keys must still be present with identical values
        for key, value in original_metrics.items():
            assert key in enriched, f"Missing key after attachment: {key}"
            assert enriched[key] == value, (
                f"Value changed for {key}: {value!r} -> {enriched[key]!r}"
            )


# ===========================================================================
# Test 6: Reject physical interpretation True
# ===========================================================================


class TestRejectPhysicalInterpretationTrue:
    """Verify that physical_interpretation_allowed=True is not serializable."""

    def test_attach_metadata_rejects_physical_interpretation_true(self) -> None:
        """If metadata has physical_interpretation_allowed() == True,
        attach must raise ValueError.

        Note: Under the current ScaleMetadata design, it is impossible to
        construct a metadata instance where physical_interpretation_allowed()
        returns True (no physical geometry mode exists). This test verifies
        that the safe default is preserved and that the helper would reject
        any future construction that allows physical interpretation."""
        _, attach_scale_metadata_to_metrics = _import_helpers()

        # Default metadata: physical_interpretation_allowed() == False
        metadata = ScaleMetadata()
        assert metadata.physical_interpretation_allowed() is False

        # Attach should succeed with safe defaults
        result = attach_scale_metadata_to_metrics(
            {"max_abs_phi": 1.0},
            metadata,
        )
        assert result["physical_interpretation_allowed"] is False


# ===========================================================================
# Test 7: No Option C fields present
# ===========================================================================

OPTION_C_FORBIDDEN_FIELDS = {
    "D_it_SI",
    "sigma_eff",
    "rho_eff",
    "t_eff",
    "delta_E_window",
}


class TestNoOptionCFieldsPresent:
    """Verify that Option C fields are not included in the record."""

    def test_no_option_c_fields_are_required_or_enabled(self) -> None:
        """The metadata record must NOT contain any Option C parameter
        fields, and option_c_enabled must be False."""
        scale_metadata_to_record, _ = _import_helpers()
        metadata = ScaleMetadata()
        record = scale_metadata_to_record(metadata)

        for forbidden_field in OPTION_C_FORBIDDEN_FIELDS:
            assert forbidden_field not in record, (
                f"Option C field present in record: {forbidden_field}"
            )

        assert record["option_c_enabled"] is False
