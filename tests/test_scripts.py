"""Tests for scripts — T-11, T-12."""

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
