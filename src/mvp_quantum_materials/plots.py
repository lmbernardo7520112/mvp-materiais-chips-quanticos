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
