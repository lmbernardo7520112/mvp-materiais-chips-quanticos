"""RED specifications for v0.4.6 runtime metadata CSV integration.

These tests specify that in a future GREEN phase, the Poisson Bridge CSV
output (``poisson_bridge_metrics.csv``) must include safe metadata columns
declaring the current scale regime, WITHOUT altering any existing numeric
columns or values.

.. important::
    This is a RED-phase file. Tests that check for new metadata columns
    are expected to FAIL because the CSV does not yet contain them.
    Tests that verify existing columns should PASS (non-regression).

See Also
--------
v0.4.6_runtime_metadata_tdd_plan.md : TDD plan for this phase.
v0.4.5_runtime_scale_metadata_integration.md : Decision brief.
scripts/run_poisson_bridge.py : The bridge script that produces the CSV.
"""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Existing numeric columns that must never be removed or renamed
# ---------------------------------------------------------------------------

EXISTING_NUMERIC_COLUMNS = {
    "max_abs_delta_rho_eff",
    "mean_delta_rho_eff",
    "max_abs_phi",
    "solver_iterations",
    "solver_residual",
    "converged",
}

# ---------------------------------------------------------------------------
# Future metadata columns expected after GREEN implementation
# ---------------------------------------------------------------------------

FUTURE_METADATA_COLUMNS = {
    "scale_mode",
    "geometry_mode",
    "source_mode",
    "physical_interpretation_allowed",
    "literature_scaled_constants_available",
    "option_c_enabled",
    "numerical_values_modified",
}

# ---------------------------------------------------------------------------
# Forbidden fields that must never appear in the CSV
# ---------------------------------------------------------------------------

FORBIDDEN_PHYSICAL_DECLARATIONS = {
    "phi_unit_label_V_physical",
    "calibrated",
}


def _run_bridge_and_read_csv(tmp_path: Path) -> tuple[list[str], dict[str, str]]:
    """Run the Poisson Bridge script and return (headers, first_row_dict).

    Parameters
    ----------
    tmp_path : Path
        Temporary directory for output.

    Returns
    -------
    tuple
        (list of column headers, dict mapping header -> value for first row)
    """
    figures_dir = tmp_path / "figures"
    tables_dir = tmp_path / "tables"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_poisson_bridge.py",
            "--output-dir",
            str(figures_dir),
            "--tables-dir",
            str(tables_dir),
        ],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(Path(__file__).resolve().parent.parent),
    )

    assert result.returncode == 0, (
        f"Bridge script failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )

    csv_path = tables_dir / "poisson_bridge_metrics.csv"
    assert csv_path.exists(), f"CSV not generated at {csv_path}"

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    assert len(rows) >= 1, "CSV has no data rows"

    return list(headers), rows[0]


# ===========================================================================
# Test 1: CSV contains runtime metadata fields (RED expected)
# ===========================================================================


class TestBridgeMetricsCsvContainsRuntimeMetadata:
    """Verify that the bridge CSV includes metadata columns."""

    def test_bridge_metrics_csv_contains_runtime_metadata_fields(
        self, tmp_path: Path
    ) -> None:
        """The bridge CSV must contain all future metadata columns.

        RED expected: columns do not exist yet."""
        headers, _ = _run_bridge_and_read_csv(tmp_path)

        missing = FUTURE_METADATA_COLUMNS - set(headers)
        assert not missing, (
            f"Missing metadata columns in CSV: {sorted(missing)}"
        )


# ===========================================================================
# Test 2: CSV keeps existing numeric columns (should PASS)
# ===========================================================================


class TestBridgeMetricsCsvKeepsExistingColumns:
    """Verify that existing numeric columns are preserved."""

    def test_bridge_metrics_csv_keeps_existing_numeric_columns(
        self, tmp_path: Path
    ) -> None:
        """All original numeric columns must still be present in the CSV."""
        headers, _ = _run_bridge_and_read_csv(tmp_path)

        missing = EXISTING_NUMERIC_COLUMNS - set(headers)
        assert not missing, (
            f"Missing existing numeric columns: {sorted(missing)}"
        )


# ===========================================================================
# Test 3: Runtime metadata declares demonstrative mode (RED expected)
# ===========================================================================


class TestRuntimeMetadataDeclaresDemonstrativeMode:
    """Verify that metadata values declare demonstrative mode."""

    def test_runtime_metadata_declares_demonstrative_mode(
        self, tmp_path: Path
    ) -> None:
        """Metadata fields in the CSV must declare demonstrative mode.

        RED expected: metadata columns do not exist yet."""
        headers, row = _run_bridge_and_read_csv(tmp_path)

        # First check columns exist (this is the primary RED failure point)
        for col in ["scale_mode", "geometry_mode", "physical_interpretation_allowed",
                     "option_c_enabled", "numerical_values_modified"]:
            assert col in headers, f"Metadata column '{col}' not in CSV"

        assert row["scale_mode"] == "demonstrative"
        assert row["geometry_mode"] == "normalized_2d"
        assert row["physical_interpretation_allowed"].lower() == "false"
        assert row["option_c_enabled"].lower() == "false"
        assert row["numerical_values_modified"].lower() == "false"


# ===========================================================================
# Test 4: Runtime metadata does not enable physical phi (RED expected)
# ===========================================================================


class TestRuntimeMetadataDoesNotEnablePhysicalPhi:
    """Verify that no field declares physical phi interpretation."""

    def test_runtime_metadata_does_not_enable_physical_phi(
        self, tmp_path: Path
    ) -> None:
        """No CSV field must declare physical phi interpretation, calibration,
        or physical voltage units.

        RED expected for metadata check; the existing CSV should not have
        these fields at all."""
        headers, row = _run_bridge_and_read_csv(tmp_path)

        # No forbidden physical declaration columns
        for col in FORBIDDEN_PHYSICAL_DECLARATIONS:
            assert col not in headers, (
                f"Forbidden physical declaration column present: {col}"
            )

        # If metadata columns exist, verify they do not enable physics
        if "physical_interpretation_allowed" in headers:
            assert row["physical_interpretation_allowed"].lower() != "true", (
                "physical_interpretation_allowed must not be true"
            )


# ===========================================================================
# Test 5: Metadata-only integration does not change existing schema names
# ===========================================================================


class TestMetadataOnlyDoesNotChangeExistingSchemaNames:
    """Verify that the existing numeric column names are unchanged."""

    def test_metadata_only_integration_does_not_change_existing_numeric_schema_names(
        self, tmp_path: Path
    ) -> None:
        """All original column names must be present with exact spelling.
        New metadata columns may be appended but must not replace originals."""
        headers, _ = _run_bridge_and_read_csv(tmp_path)

        for col in EXISTING_NUMERIC_COLUMNS:
            assert col in headers, (
                f"Existing column '{col}' was renamed or removed"
            )
