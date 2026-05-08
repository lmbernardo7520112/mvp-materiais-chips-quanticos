"""Plot generation for thermal-diffusive model results.

Generates publication-quality figures saved to disk.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend for headless generation
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

from mvp_quantum_materials.diffusion_solver import DiffusionResult
from mvp_quantum_materials.thermal_solver import ThermalResult


def plot_thermal_evolution(
    x: npt.NDArray[np.float64],
    result: ThermalResult,
    output_path: Path,
) -> Path:
    """Plot thermal field evolution over time.

    Args:
        x: Spatial coordinates [m].
        result: Thermal solver result.
        output_path: Path to save figure.

    Returns:
        Path to saved figure.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    n_curves = min(len(result.T_history), 6)
    indices = np.linspace(0, len(result.T_history) - 1, n_curves, dtype=int)

    for i in indices:
        t_time = result.times[i] if i < len(result.times) else 0.0
        ax.plot(x * 1e3, result.T_history[i], label=f"t = {t_time:.3f} s")

    ax.set_xlabel("Position [mm]")
    ax.set_ylabel("Temperature [K]")
    ax.set_title("Thermal Field Evolution (1D)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_diffusion_evolution(
    x: npt.NDArray[np.float64],
    result: DiffusionResult,
    output_path: Path,
) -> Path:
    """Plot concentration field evolution over time.

    Args:
        x: Spatial coordinates [m].
        result: Diffusion solver result.
        output_path: Path to save figure.

    Returns:
        Path to saved figure.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    n_curves = min(len(result.C_history), 6)
    indices = np.linspace(0, len(result.C_history) - 1, n_curves, dtype=int)

    for i in indices:
        t_time = result.times[i] if i < len(result.times) else 0.0
        ax.plot(x * 1e3, result.C_history[i], label=f"t = {t_time:.3f} s")

    ax.set_xlabel("Position [mm]")
    ax.set_ylabel("C (adimensional proxy)")
    ax.set_title(
        "Concentration Proxy Evolution (1D)\n"
        "[C is adimensional — not calibrated physical concentration]"
    )
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_sensitivity_results(
    results: list[dict],
    output_path: Path,
) -> Path:
    """Plot sensitivity analysis results as grouped bar chart.

    Args:
        results: List of sensitivity results from run_sensitivity_analysis.
        output_path: Path to save figure.

    Returns:
        Path to saved figure.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Group by parameter
    params = sorted(set(r["parameter"] for r in results))
    colors = plt.cm.Set2(np.linspace(0, 1, len(params)))

    for i, param in enumerate(params):
        param_results = [r for r in results if r["parameter"] == param]
        values = [r["value"] for r in param_results]
        metrics = [r["metric_value"] for r in param_results]

        ax.plot(range(len(values)), metrics, "o-", color=colors[i], label=param, linewidth=2)

    ax.set_xlabel("Parameter Variation Index")
    ax.set_ylabel("Global C Integral (primary metric)")
    ax.set_title("Parametric Sensitivity Analysis\n[C is adimensional proxy]")
    ax.legend(title="Parameter")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_sensitivity_ranking(
    ranking: list[dict],
    output_path: Path,
) -> Path:
    """Plot sensitivity ranking as horizontal bar chart.

    Args:
        ranking: List of dicts from compute_sensitivity_ranking.
        output_path: Path to save figure.

    Returns:
        Path to saved figure.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    params = [r["parameter"] for r in ranking]
    sensitivities = [r["sensitivity"] for r in ranking]
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(params)))

    bars = ax.barh(params, sensitivities, color=colors, edgecolor="gray", linewidth=0.5)

    # Add value labels
    for bar, val in zip(bars, sensitivities, strict=True):
        ax.text(
            bar.get_width() + 0.01 * max(sensitivities),
            bar.get_y() + bar.get_height() / 2,
            f"{val:.3f}",
            va="center",
            fontsize=9,
        )

    ax.set_xlabel("Normalized Sensitivity (demonstrative)")
    ax.set_title(
        "Parameter Sensitivity Ranking\n"
        "[Normalized range: S = (max-min)/|mean| — demonstrative, not calibrated]"
    )
    ax.invert_yaxis()
    ax.grid(True, axis="x", alpha=0.3)

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


# ---------------------------------------------------------------------------
# 2D Plot Functions (v0.2)
# ---------------------------------------------------------------------------


def plot_thermal_2d_final(
    x: npt.NDArray[np.float64],
    y: npt.NDArray[np.float64],
    T_final: npt.NDArray[np.float64],
    output_path: Path,
) -> Path:
    """Plot final 2D thermal field as contour/heatmap.

    Args:
        x: x-coordinates [m].
        y: y-coordinates [m].
        T_final: Final temperature field, shape (nx, ny) [K].
        output_path: Path to save figure.

    Returns:
        Path to saved figure.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    X, Y = np.meshgrid(x * 1e3, y * 1e3, indexing="ij")
    cf = ax.contourf(X, Y, T_final, levels=20, cmap="inferno")
    fig.colorbar(cf, ax=ax, label="Temperature [K]")

    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.set_title("2D Thermal Field (Final State)\n[demonstrativo — não calibrado]")
    ax.set_aspect("equal")

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


# ---------------------------------------------------------------------------
# Defect 2D Plot Functions (v0.3)
# ---------------------------------------------------------------------------


def plot_defect_2d_final(
    x: npt.NDArray[np.float64],
    y: npt.NDArray[np.float64],
    C_def_final: npt.NDArray[np.float64],
    output_path: Path,
) -> Path:
    """Plot final 2D defect-like field as contour/heatmap.

    Args:
        x: x-coordinates [m].
        y: y-coordinates [m].
        C_def_final: Final C_def field, shape (nx, ny). Adimensional.
        output_path: Path to save figure.

    Returns:
        Path to saved figure.

    Note:
        C_def is adimensional — demonstrative, not calibrated.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    X, Y = np.meshgrid(x * 1e3, y * 1e3, indexing="ij")
    cf = ax.contourf(X, Y, C_def_final, levels=20, cmap="viridis")
    fig.colorbar(cf, ax=ax, label="C_def (adimensional proxy)")

    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.set_title("2D Defect-like Field C_def (Final State)\n[demonstrative — not calibrated]")
    ax.set_aspect("equal")

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path
