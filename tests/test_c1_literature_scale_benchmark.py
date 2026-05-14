"""Tests for v0.5.2 C1 Literature Scale Benchmark."""

import csv
import importlib
from pathlib import Path

import pytest


def test_literature_benchmark_script_imports():
    """The benchmark script module exists and imports successfully."""
    module = importlib.import_module("scripts.run_c1_literature_scale_benchmark")
    assert hasattr(module, "generate_c1_literature_scale_benchmark")


def test_literature_benchmark_generates_csv_and_figure(tmp_path: Path):
    """The benchmark script generates the expected CSV and figure."""
    from scripts.run_c1_literature_scale_benchmark import (
        generate_c1_literature_scale_benchmark,
    )

    results = generate_c1_literature_scale_benchmark(tmp_path)

    assert "csv" in results
    assert "figure" in results

    csv_path = results["csv"]
    fig_path = results["figure"]

    assert csv_path.exists()
    assert fig_path.exists()
    assert csv_path.name == "c1_literature_scale_benchmark.csv"
    assert fig_path.name == "c1_literature_scale_positioning.png"
    assert csv_path.parent.name == "tables"
    assert fig_path.parent.name == "figures"


def test_literature_benchmark_has_required_columns(tmp_path: Path):
    """The benchmark CSV has all required columns."""
    from scripts.run_c1_literature_scale_benchmark import (
        generate_c1_literature_scale_benchmark,
    )

    csv_path = generate_c1_literature_scale_benchmark(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        assert fieldnames is not None

        required = [
            "scenario",
            "d_it_ev_inv_cm2",
            "delta_e_window_eV",
            "f_occ",
            "s_charge",
            "sigma_eff_c_m2",
            "abs_sigma_eff_c_m2",
            "scale_class",
            "evidence_tier",
            "calibration_status",
            "device_prediction_claimed",
            "solver_coupled",
            "rho_eff_present",
            "t_eff_present",
        ]
        for col in required:
            assert col in fieldnames, f"missing column: {col}"


def test_no_calibration_claims(tmp_path: Path):
    """All rows declare not_calibrated and no device prediction."""
    from scripts.run_c1_literature_scale_benchmark import (
        generate_c1_literature_scale_benchmark,
    )

    csv_path = generate_c1_literature_scale_benchmark(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            assert row["calibration_status"] == "not_calibrated"
            assert row["device_prediction_claimed"].lower() == "false"


def test_no_c2_fields(tmp_path: Path):
    """The CSV does not include C2 fields."""
    from scripts.run_c1_literature_scale_benchmark import (
        generate_c1_literature_scale_benchmark,
    )

    csv_path = generate_c1_literature_scale_benchmark(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        fieldnames = csv.DictReader(f).fieldnames
        assert fieldnames is not None
        for forbidden in ["rho_eff_c_m3", "t_eff_m", "phi", "solver_output"]:
            assert forbidden not in fieldnames, f"C2 field present: {forbidden}"


def test_scale_classes_present(tmp_path: Path):
    """At least the required scale classes are present."""
    from scripts.run_c1_literature_scale_benchmark import (
        generate_c1_literature_scale_benchmark,
    )

    csv_path = generate_c1_literature_scale_benchmark(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        classes = {row["scale_class"] for row in csv.DictReader(f)}

    required_classes = {
        "literature_plausible_low",
        "literature_plausible_nominal",
        "literature_plausible_high",
        "aggressive_upper_bound",
    }
    missing = required_classes - classes
    assert not missing, f"missing scale classes: {missing}"


def test_sigma_eff_positive_magnitude_for_positive_occupancy(tmp_path: Path):
    """abs_sigma_eff > 0 when f_occ > 0."""
    from scripts.run_c1_literature_scale_benchmark import (
        generate_c1_literature_scale_benchmark,
    )

    csv_path = generate_c1_literature_scale_benchmark(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if float(row["f_occ"]) > 0:
                assert float(row["abs_sigma_eff_c_m2"]) > 0


def test_sign_symmetry_for_selected_scenarios(tmp_path: Path):
    """For paired +1/-1 scenarios, sigma_eff signs are opposite."""
    from scripts.run_c1_literature_scale_benchmark import (
        generate_c1_literature_scale_benchmark,
    )

    csv_path = generate_c1_literature_scale_benchmark(tmp_path)["csv"]

    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Group by (d_it, delta_e, f_occ)
    groups: dict[tuple[str, str, str], dict[int, float]] = {}
    for row in rows:
        if float(row["f_occ"]) > 0:
            key = (
                row["d_it_ev_inv_cm2"],
                row["delta_e_window_eV"],
                row["f_occ"],
            )
            if key not in groups:
                groups[key] = {}
            groups[key][int(row["s_charge"])] = float(row["sigma_eff_c_m2"])

    for key, values in groups.items():
        if 1 in values and -1 in values:
            assert values[1] == pytest.approx(-values[-1], rel=1e-12), (
                f"Sign symmetry failed for {key}"
            )
