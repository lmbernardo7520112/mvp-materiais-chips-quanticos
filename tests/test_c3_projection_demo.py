import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

# Constants
DEMO_SCRIPT_PATH = Path("scripts/run_c3_projection_demo.py")


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """Provides a temporary directory for demo outputs."""
    return tmp_path


def run_demo(out_dir: Path) -> subprocess.CompletedProcess:
    """Runs the demo script using the current Python executable."""
    return subprocess.run(
        [sys.executable, str(DEMO_SCRIPT_PATH), "--output-dir", str(out_dir)],
        capture_output=True,
        text=True,
        check=True,
    )


def test_c3_demo_script_exists():
    """1. test_c3_demo_script_exists"""
    assert DEMO_SCRIPT_PATH.exists(), "Demo script must exist."


def test_c3_demo_runs_and_writes_csv(output_dir: Path):
    """2. test_c3_demo_runs_and_writes_csv"""
    run_demo(output_dir)
    csv_file = output_dir / "c3_projection_demo.csv"
    assert csv_file.exists(), "CSV output not generated."

    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) > 0, "CSV must contain data rows."


def test_c3_demo_runs_and_writes_summary_json(output_dir: Path):
    """3. test_c3_demo_runs_and_writes_summary_json"""
    run_demo(output_dir)
    json_file = output_dir / "c3_projection_demo_summary.json"
    assert json_file.exists(), "JSON output not generated."

    with open(json_file) as f:
        summary = json.load(f)
        assert isinstance(summary, dict), "Summary must be a JSON object."


def test_c3_demo_summary_reports_charge_conservation(output_dir: Path):
    """4. test_c3_demo_summary_reports_charge_conservation"""
    run_demo(output_dir)
    json_file = output_dir / "c3_projection_demo_summary.json"
    with open(json_file) as f:
        summary = json.load(f)

    assert "total_source_charge" in summary
    assert "total_projected_charge" in summary
    assert "charge_conservation_error" in summary


def test_c3_demo_summary_reports_zero_or_tiny_conservation_error(output_dir: Path):
    """5. test_c3_demo_summary_reports_zero_or_tiny_conservation_error"""
    run_demo(output_dir)
    json_file = output_dir / "c3_projection_demo_summary.json"
    with open(json_file) as f:
        summary = json.load(f)

    error = abs(summary["charge_conservation_error"])
    assert error < 1e-10, f"Conservation error is too large: {error}"


def test_c3_demo_preserves_charge_sign(output_dir: Path):
    """6. test_c3_demo_preserves_charge_sign"""
    run_demo(output_dir)
    json_file = output_dir / "c3_projection_demo_summary.json"
    with open(json_file) as f:
        summary = json.load(f)

    assert "sign_preserved" in summary
    assert summary["sign_preserved"] is True, "Sign was not preserved."


def test_c3_demo_preserves_metadata(output_dir: Path):
    """7. test_c3_demo_preserves_metadata"""
    run_demo(output_dir)
    json_file = output_dir / "c3_projection_demo_summary.json"
    with open(json_file) as f:
        summary = json.load(f)

    assert "metadata_preserved" in summary
    assert summary["metadata_preserved"] is True, "Metadata was not preserved."


def test_c3_demo_reports_not_calibrated(output_dir: Path):
    """8. test_c3_demo_reports_not_calibrated"""
    run_demo(output_dir)
    json_file = output_dir / "c3_projection_demo_summary.json"
    with open(json_file) as f:
        summary = json.load(f)

    assert summary.get("calibration_status") == "not_calibrated", "Must be not_calibrated"


def test_c3_demo_reports_physical_interpretation_false(output_dir: Path):
    """9. test_c3_demo_reports_physical_interpretation_false"""
    run_demo(output_dir)
    json_file = output_dir / "c3_projection_demo_summary.json"
    with open(json_file) as f:
        summary = json.load(f)

    assert summary.get("physical_interpretation_allowed") is False


def test_c3_demo_reports_solver_coupling_false(output_dir: Path):
    """10. test_c3_demo_reports_solver_coupling_false"""
    run_demo(output_dir)
    json_file = output_dir / "c3_projection_demo_summary.json"
    with open(json_file) as f:
        summary = json.load(f)

    assert summary.get("solver_coupling_enabled") is False


def test_c3_demo_outputs_do_not_contain_phi_or_potential_columns(output_dir: Path):
    """11. test_c3_demo_outputs_do_not_contain_phi_or_potential_columns"""
    run_demo(output_dir)
    csv_file = output_dir / "c3_projection_demo.csv"

    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []

    forbidden = {"phi", "potential", "voltage", "electrostatic_potential"}
    for header in headers:
        assert header.lower() not in forbidden, f"Forbidden column found: {header}"


def test_c3_demo_does_not_import_poisson_solver():
    """12. test_c3_demo_does_not_import_poisson_solver"""
    with open(DEMO_SCRIPT_PATH) as f:
        content = f.read()

    assert "poisson_solver_2d" not in content, "Must not import poisson_solver_2d"
    assert "solve_poisson" not in content, "Must not call solve_poisson"


def test_c3_demo_does_not_import_ml_packages():
    """13. test_c3_demo_does_not_import_ml_packages"""
    with open(DEMO_SCRIPT_PATH) as f:
        content = f.read()

    forbidden = ["torch", "tensorflow", "jax", "sklearn"]
    for pkg in forbidden:
        assert f"import {pkg}" not in content
        assert f"from {pkg}" not in content
