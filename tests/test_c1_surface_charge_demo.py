import csv
import importlib
from pathlib import Path

import pytest


def test_demo_script_module_imports():
    """Run_c1_surface_charge_demo module exists and imports successfully."""
    # RED phase: This will fail with ModuleNotFoundError or ImportError
    module = importlib.import_module("scripts.run_c1_surface_charge_demo")
    assert hasattr(module, "generate_c1_surface_charge_demo")


def test_demo_generates_expected_csv_and_figure(tmp_path: Path):
    """The demo script generates the CSV and figure artifacts."""
    from scripts.run_c1_surface_charge_demo import generate_c1_surface_charge_demo

    results = generate_c1_surface_charge_demo(tmp_path)

    assert "csv" in results
    assert "figure" in results

    csv_path = results["csv"]
    fig_path = results["figure"]

    assert csv_path.exists()
    assert fig_path.exists()
    assert csv_path.name == "c1_surface_charge_demo.csv"
    assert fig_path.name == "c1_sigma_eff_sensitivity.png"
    assert csv_path.parent.name == "tables"
    assert fig_path.parent.name == "figures"


def test_demo_csv_has_expected_columns(tmp_path: Path):
    """The generated CSV has all expected columns."""
    from scripts.run_c1_surface_charge_demo import generate_c1_surface_charge_demo

    csv_path = generate_c1_surface_charge_demo(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        assert fieldnames is not None

        expected_columns = [
            "d_it_ev_inv_cm2",
            "delta_e_window_eV",
            "delta_e_window_J",
            "f_occ",
            "s_charge",
            "d_it_si_j_inv_m2",
            "n_it_m2",
            "sigma_eff_c_m2",
            "abs_sigma_eff_c_m2",
            "c1_bookkeeping_only",
            "rho_eff_present",
            "t_eff_present",
            "solver_coupled",
            "physical_interpretation_allowed",
            "option_c_enabled",
        ]
        for col in expected_columns:
            assert col in fieldnames


def test_demo_csv_has_expected_row_count(tmp_path: Path):
    """The CSV has exactly 72 rows (3 D_it x 3 delta_E x 4 f_occ x 2 s_charge)."""
    from scripts.run_c1_surface_charge_demo import generate_c1_surface_charge_demo

    csv_path = generate_c1_surface_charge_demo(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        assert len(rows) == 72


def test_sigma_eff_sign_symmetry(tmp_path: Path):
    """sigma_eff(s_charge=+1) = -sigma_eff(s_charge=-1)."""
    from scripts.run_c1_surface_charge_demo import generate_c1_surface_charge_demo

    csv_path = generate_c1_surface_charge_demo(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Group by D_it, delta_E, f_occ
    groups = {}
    for row in rows:
        key = (row["d_it_ev_inv_cm2"], row["delta_e_window_eV"], row["f_occ"])
        if key not in groups:
            groups[key] = {}
        groups[key][int(row["s_charge"])] = float(row["sigma_eff_c_m2"])

    for _key, values in groups.items():
        assert len(values) == 2  # Must have +1 and -1
        assert values[1] == -values[-1]


def test_sigma_eff_zero_when_occupancy_zero(tmp_path: Path):
    """If f_occ = 0, sigma_eff = 0."""
    from scripts.run_c1_surface_charge_demo import generate_c1_surface_charge_demo

    csv_path = generate_c1_surface_charge_demo(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if float(row["f_occ"]) == 0.0:
                assert float(row["sigma_eff_c_m2"]) == 0.0


def test_abs_sigma_eff_monotonic_with_dit(tmp_path: Path):
    """abs(sigma_eff) increases with D_it for fixed delta_E_window, f_occ, s_charge."""
    from scripts.run_c1_surface_charge_demo import generate_c1_surface_charge_demo

    csv_path = generate_c1_surface_charge_demo(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # We need to filter for f_occ > 0 to see strictly increasing (or non-decreasing if we allow 0)
    groups = {}
    for row in rows:
        if float(row["f_occ"]) > 0:
            key = (row["delta_e_window_eV"], row["f_occ"], row["s_charge"])
            if key not in groups:
                groups[key] = []
            groups[key].append((float(row["d_it_ev_inv_cm2"]), float(row["abs_sigma_eff_c_m2"])))

    for key, pairs in groups.items():
        # Sort by D_it
        pairs.sort(key=lambda x: x[0])
        # Check monotonic increase
        for i in range(1, len(pairs)):
            assert pairs[i][1] > pairs[i - 1][1], f"Failed monotonic D_it for {key}"


def test_abs_sigma_eff_monotonic_with_energy_window(tmp_path: Path):
    """abs(sigma_eff) increases with delta_E_window for fixed D_it, f_occ, s_charge."""
    from scripts.run_c1_surface_charge_demo import generate_c1_surface_charge_demo

    csv_path = generate_c1_surface_charge_demo(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # We need to filter for f_occ > 0
    groups = {}
    for row in rows:
        if float(row["f_occ"]) > 0:
            key = (row["d_it_ev_inv_cm2"], row["f_occ"], row["s_charge"])
            if key not in groups:
                groups[key] = []
            groups[key].append((float(row["delta_e_window_eV"]), float(row["abs_sigma_eff_c_m2"])))

    for key, pairs in groups.items():
        # Sort by delta_E_window
        pairs.sort(key=lambda x: x[0])
        # Check monotonic increase
        for i in range(1, len(pairs)):
            assert pairs[i][1] > pairs[i - 1][1], f"Failed monotonic delta_E_window for {key}"


def test_demo_does_not_include_rho_eff_or_t_eff_columns(tmp_path: Path):
    """Demo CSV does not include rho_eff or t_eff columns."""
    from scripts.run_c1_surface_charge_demo import generate_c1_surface_charge_demo

    csv_path = generate_c1_surface_charge_demo(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        fieldnames = csv.DictReader(f).fieldnames
        assert fieldnames is not None
        assert "rho_eff" not in fieldnames
        assert "t_eff" not in fieldnames
        assert "rho_eff_c_m3" not in fieldnames
        assert "t_eff_m" not in fieldnames


def test_demo_metadata_blocks_physical_interpretation(tmp_path: Path):
    """All rows declare C1 physical interpretation is blocked."""
    from scripts.run_c1_surface_charge_demo import generate_c1_surface_charge_demo

    csv_path = generate_c1_surface_charge_demo(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            assert row["c1_bookkeeping_only"].lower() == "true"
            assert row["rho_eff_present"].lower() == "false"
            assert row["t_eff_present"].lower() == "false"
            assert row["solver_coupled"].lower() == "false"
            assert row["physical_interpretation_allowed"].lower() == "false"
            assert row["option_c_enabled"].lower() == "false"


def test_generate_all_results_includes_c1_demo_if_integrated(tmp_path: Path):
    """If generate_all_results.py generates C1 demo artifacts, they are correct."""
    script_path = Path("scripts/generate_all_results.py")
    if not script_path.exists():
        pytest.skip("generate_all_results.py not found")

    with open(script_path, encoding="utf-8") as f:
        content = f.read()

    if "run_c1_surface_charge_demo.py" in content:
        import subprocess

        # We must create a dummy structure so generate_all_results.py works.
        # But actually generate_all_results.py takes time to run all solvers.
        # Let's just run the full script and check if the artifacts are there.
        # Since it takes ~15 seconds, we run it in a tmp_path.
        subprocess.run(
            [
                "python",
                "scripts/generate_all_results.py",
                "--output-dir",
                str(tmp_path / "figures"),
            ],
            check=True,
        )

        assert (tmp_path / "tables" / "c1_surface_charge_demo.csv").exists()
        assert (tmp_path / "figures" / "c1_sigma_eff_sensitivity.png").exists()
    else:
        pytest.skip("generate_all_results not yet integrated with c1_surface_charge_demo")
