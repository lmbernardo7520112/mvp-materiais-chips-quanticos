"""Tests for v0.7.4 C2 Charge Mapping Demo & Sanity Checks."""

import csv
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

DEMO_SCRIPT = Path("scripts/run_c2_charge_mapping_demo.py")


def _run_demo(output_dir: str) -> subprocess.CompletedProcess[str]:
    """Run the demo script with the given output directory."""
    return subprocess.run(
        [
            sys.executable,
            str(DEMO_SCRIPT),
            "--output-dir",
            output_dir,
        ],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": "."},
        check=True,
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    """Read CSV file and return list of row dicts."""
    with open(path) as f:
        reader = csv.DictReader(f)
        return list(reader)


def test_demo_script_exists():
    """Demo script must exist."""
    assert DEMO_SCRIPT.exists(), f"{DEMO_SCRIPT} does not exist"


def test_demo_script_runs_and_creates_csv():
    """Demo script must run and create CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _run_demo(tmpdir)
        csv_path = Path(tmpdir) / "csv" / "c2_charge_mapping_demo.csv"
        assert csv_path.exists(), f"CSV not found at {csv_path}"


def test_demo_csv_has_required_columns():
    """CSV must contain all required columns."""
    required = [
        "scenario_id",
        "sigma_c_per_m2",
        "sigma_sign",
        "area_m2",
        "l_reg_m",
        "rho_reg_c_per_m3",
        "volume_m3",
        "total_sheet_charge_c",
        "total_volume_charge_c",
        "relative_charge_error",
        "regularization_role",
        "not_physical_t_eff",
        "calibration_status",
        "solver_coupling_enabled",
        "physical_interpretation_allowed",
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        _run_demo(tmpdir)
        rows = _read_csv(Path(tmpdir) / "csv" / "c2_charge_mapping_demo.csv")
        assert len(rows) > 0, "CSV is empty"
        for col in required:
            assert col in rows[0], f"Missing column: {col}"


def test_demo_contains_positive_and_negative_sigma():
    """CSV must contain both positive and negative sigma values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _run_demo(tmpdir)
        rows = _read_csv(Path(tmpdir) / "csv" / "c2_charge_mapping_demo.csv")
        sigmas = [float(r["sigma_c_per_m2"]) for r in rows]
        assert any(s > 0 for s in sigmas), "No positive sigma"
        assert any(s < 0 for s in sigmas), "No negative sigma"


def test_demo_contains_multiple_l_reg_values():
    """CSV must contain at least 3 distinct l_reg values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _run_demo(tmpdir)
        rows = _read_csv(Path(tmpdir) / "csv" / "c2_charge_mapping_demo.csv")
        l_reg_vals = {r["l_reg_m"] for r in rows}
        assert len(l_reg_vals) >= 3, "Fewer than 3 l_reg values"


def test_charge_conservation_error_is_small():
    """Relative charge error must be <= 1e-12."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _run_demo(tmpdir)
        rows = _read_csv(Path(tmpdir) / "csv" / "c2_charge_mapping_demo.csv")
        max_err = max(abs(float(r["relative_charge_error"])) for r in rows)
        assert max_err <= 1e-12, f"Max charge error {max_err} > 1e-12"


def test_rho_scales_as_inverse_l_reg_for_fixed_sigma():
    """For fixed sigma, rho_reg must scale as 1/l_reg."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _run_demo(tmpdir)
        rows = _read_csv(Path(tmpdir) / "csv" / "c2_charge_mapping_demo.csv")
        first_sigma = rows[0]["sigma_c_per_m2"]
        subset = [r for r in rows if r["sigma_c_per_m2"] == first_sigma]
        if len(subset) >= 2:
            products = [float(r["rho_reg_c_per_m3"]) * float(r["l_reg_m"]) for r in subset]
            assert np.allclose(products, float(first_sigma), rtol=1e-12), (
                "rho_reg * l_reg is not constant"
            )


def test_total_charge_independent_of_l_reg():
    """For fixed sigma and area, total_volume_charge must be invariant with l_reg."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _run_demo(tmpdir)
        rows = _read_csv(Path(tmpdir) / "csv" / "c2_charge_mapping_demo.csv")
        first_sigma = rows[0]["sigma_c_per_m2"]
        subset = [r for r in rows if r["sigma_c_per_m2"] == first_sigma]
        if len(subset) >= 2:
            charges = [float(r["total_volume_charge_c"]) for r in subset]
            assert np.allclose(charges, charges[0], rtol=1e-12), (
                "Total volume charge varies with l_reg"
            )


def test_demo_flags_are_safe():
    """All rows must have safe metadata flags."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _run_demo(tmpdir)
        rows = _read_csv(Path(tmpdir) / "csv" / "c2_charge_mapping_demo.csv")
        for r in rows:
            assert r["regularization_role"] == "numerical"
            assert r["not_physical_t_eff"] == "True"
            assert r["calibration_status"] == "not_calibrated"
            assert r["solver_coupling_enabled"] == "False"
            assert r["physical_interpretation_allowed"] == "False"


def test_demo_does_not_import_solver():
    """Demo script must not import poisson_solver_2d or call solve_poisson."""
    content = DEMO_SCRIPT.read_text()
    assert "poisson_solver_2d" not in content, "Script imports poisson_solver_2d"
    assert "solve_poisson" not in content, "Script calls solve_poisson"


def test_demo_does_not_claim_physical_phi():
    """Demo script and CSV must not claim physical phi."""
    content = DEMO_SCRIPT.read_text()
    assert "phi_physical_claim = True" not in content
    assert "physical_phi" not in content
    assert "device_prediction" not in content


def test_demo_figures_created():
    """Demo must generate conservation and sensitivity figures."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _run_demo(tmpdir)
        fig_dir = Path(tmpdir) / "figures"
        assert (fig_dir / "c2_charge_conservation.png").exists()
        assert (fig_dir / "c2_l_reg_sensitivity.png").exists()


def test_demo_is_deterministic():
    """Two runs must produce identical CSVs."""
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        _run_demo(d1)
        _run_demo(d2)
        rows1 = _read_csv(Path(d1) / "csv" / "c2_charge_mapping_demo.csv")
        rows2 = _read_csv(Path(d2) / "csv" / "c2_charge_mapping_demo.csv")
        assert rows1 == rows2, "CSVs differ between runs"


def test_generate_all_results_not_modified():
    """generate_all_results.py must remain untouched by v0.7.4."""
    result = subprocess.run(
        ["git", "diff", "main", "--name-only", "--", "scripts/generate_all_results.py"],
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", "generate_all_results.py was modified"


def test_no_c1_mutation():
    """C1 modules must not be altered."""
    result = subprocess.run(
        [
            "git",
            "diff",
            "main",
            "--name-only",
            "--",
            "src/mvp_quantum_materials/surface_charge.py",
            "src/mvp_quantum_materials/energy_profiles.py",
            "src/mvp_quantum_materials/dit_profile_library.py",
        ],
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", "C1 modules were modified"
