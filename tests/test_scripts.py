"""Tests for scripts — T-11, T-12, T-v0.2 result generation."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def _run_script(script_name: str, output_dir: Path) -> subprocess.CompletedProcess:
    """Run a script as subprocess with --output-dir."""
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / script_name), "--output-dir", str(output_dir)],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(REPO_ROOT),
    )


def test_scripts_execute_without_error(tmp_path: Path):
    """T-11: Main scripts execute without error."""
    for script in ["run_thermal_1d.py", "run_diffusion_1d.py", "run_sensitivity.py"]:
        result = _run_script(script, tmp_path)
        assert result.returncode == 0, (
            f"Script {script} failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )


def test_generate_all_produces_at_least_4_figures(tmp_path: Path):
    """T-12: generate_all_results.py produces >= 4 figures + CSV."""
    result = _run_script("generate_all_results.py", tmp_path)
    assert result.returncode == 0, (
        f"generate_all_results failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )

    figures = list(tmp_path.glob("*.png"))
    assert len(figures) >= 4, (
        f"Expected >= 4 figures, got {len(figures)}: {[f.name for f in figures]}"
    )

    # Verify ranking figure exists
    ranking_fig = tmp_path / "sensitivity_ranking.png"
    assert ranking_fig.exists(), "sensitivity_ranking.png not generated"


def test_generate_all_produces_sensitivity_csv(tmp_path: Path):
    """T-18: generate_all_results.py produces sensitivity CSV."""
    result = _run_script("generate_all_results.py", tmp_path)
    assert result.returncode == 0, (
        f"generate_all_results failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )

    tables_dir = tmp_path.parent / "tables"
    csv_file = tables_dir / "sensitivity_results.csv"
    assert csv_file.exists(), f"CSV not found at {csv_file}"

    # Verify CSV has content
    content = csv_file.read_text()
    lines = content.strip().split("\n")
    assert len(lines) > 1, "CSV has no data rows"
    assert "parameter" in lines[0], "CSV header missing 'parameter' column"


# ---------------------------------------------------------------------------
# v0.2 result generation tests
# ---------------------------------------------------------------------------


def test_generate_all_produces_v02_figures(tmp_path: Path):
    """v0.2: generate_all produces >= 6 figures (4 v0.1 + 2 v0.2)."""
    result = _run_script("generate_all_results.py", tmp_path)
    assert result.returncode == 0, (
        f"generate_all_results failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )

    figures = list(tmp_path.glob("*.png"))
    assert len(figures) >= 6, (
        f"Expected >= 6 figures, got {len(figures)}: {[f.name for f in figures]}"
    )

    # v0.2 specific figures
    assert (tmp_path / "thermal_2d_final.png").exists(), "thermal_2d_final.png not generated"
    assert (tmp_path / "convergence_analysis.png").exists(), (
        "convergence_analysis.png not generated"
    )


def test_generate_all_produces_convergence_csv(tmp_path: Path):
    """v0.2: generate_all produces convergence CSV."""
    result = _run_script("generate_all_results.py", tmp_path)
    assert result.returncode == 0, (
        f"generate_all_results failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )

    tables_dir = tmp_path.parent / "tables"
    csv_file = tables_dir / "convergence_results.csv"
    assert csv_file.exists(), f"Convergence CSV not found at {csv_file}"

    content = csv_file.read_text()
    lines = content.strip().split("\n")
    assert len(lines) > 1, "Convergence CSV has no data rows"
    assert "error_l2" in lines[0], "CSV header missing 'error_l2' column"


# ---------------------------------------------------------------------------
# v0.3 result generation tests
# ---------------------------------------------------------------------------


def test_generate_all_produces_v03_defect_figure(tmp_path: Path):
    """v0.3: generate_all produces defect_2d_final.png."""
    result = _run_script("generate_all_results.py", tmp_path)
    assert result.returncode == 0, (
        f"generate_all_results failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )

    assert (tmp_path / "defect_2d_final.png").exists(), "defect_2d_final.png not generated"

    # Total figures should be >= 7 (4 v0.1 + 2 v0.2 + 1 v0.3)
    figures = list(tmp_path.glob("*.png"))
    assert len(figures) >= 7, (
        f"Expected >= 7 figures, got {len(figures)}: {[f.name for f in figures]}"
    )


def test_generate_all_produces_v03_csvs(tmp_path: Path):
    """v0.3: generate_all produces defect metrics and snapshot CSVs."""
    result = _run_script("generate_all_results.py", tmp_path)
    assert result.returncode == 0, (
        f"generate_all_results failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )

    tables_dir = tmp_path.parent / "tables"

    # Metrics CSV
    metrics_csv = tables_dir / "defect_metrics.csv"
    assert metrics_csv.exists(), f"defect_metrics.csv not found at {metrics_csv}"
    content = metrics_csv.read_text()
    assert "metric" in content, "defect_metrics.csv missing header"
    assert "proxy/demonstrative" in content, "defect_metrics.csv missing nature column"

    # Snapshot CSV
    snapshot_csv = tables_dir / "defect_final_snapshot.csv"
    assert snapshot_csv.exists(), f"defect_final_snapshot.csv not found at {snapshot_csv}"
    snap_content = snapshot_csv.read_text()
    assert "C_def" in snap_content, "snapshot CSV missing C_def column"

    # Total CSVs should be >= 4
    csvs = list(tables_dir.glob("*.csv"))
    assert len(csvs) >= 4, f"Expected >= 4 CSVs, got {len(csvs)}: {[c.name for c in csvs]}"


def test_v03_snapshot_values_bounded(tmp_path: Path):
    """v0.3: C_def values in snapshot CSV are bounded in [0, 1]."""
    result = _run_script("generate_all_results.py", tmp_path)
    assert result.returncode == 0

    tables_dir = tmp_path.parent / "tables"
    snapshot_csv = tables_dir / "defect_final_snapshot.csv"
    assert snapshot_csv.exists()

    import csv

    with open(snapshot_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            val = float(row["C_def"])
            assert 0.0 <= val <= 1.0, f"C_def out of bounds: {val}"
