"""Convergence analysis using a manufactured analytical solution.

Manufactured solution for the 2D heat equation with homogeneous Dirichlet BCs:

    T(x, y, t) = sin(π·x/Lx) · sin(π·y/Ly) · exp(-α·π²·(1/Lx² + 1/Ly²)·t)

BCs: T = 0 on all boundaries.
IC: T₀(x, y) = sin(π·x/Lx) · sin(π·y/Ly).

The solution decays exponentially to zero.

Note:
    This analysis is demonstrative — not calibrated for real materials.
"""

import csv
import math
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

from mvp_quantum_materials.domain import Domain2D
from mvp_quantum_materials.thermal_solver_2d import solve_thermal_2d


def analytical_solution(
    x: npt.NDArray[np.float64],
    y: npt.NDArray[np.float64],
    t: float,
    Lx: float,
    Ly: float,
    alpha: float,
) -> npt.NDArray[np.float64]:
    """Compute the manufactured analytical solution at time t.

    Args:
        x: 1D array of x-coordinates.
        y: 1D array of y-coordinates.
        t: Time [s].
        Lx: Domain length in x [m].
        Ly: Domain length in y [m].
        alpha: Thermal diffusivity [m²/s].

    Returns:
        2D array T(x, y, t), shape (len(x), len(y)).
    """
    X, Y = np.meshgrid(x, y, indexing="ij")
    decay = math.exp(-alpha * math.pi**2 * (1.0 / Lx**2 + 1.0 / Ly**2) * t)
    return np.sin(math.pi * X / Lx) * np.sin(math.pi * Y / Ly) * decay


def run_convergence_analysis(
    nx_values: list[int] | None = None,
    alpha: float = 8.8e-5,
    Lx: float = 0.01,
    Ly: float = 0.01,
    t_final: float = 0.001,
    safety_factor: float = 0.4,
) -> list[dict]:
    """Run convergence analysis with mesh refinement.

    Args:
        nx_values: List of grid sizes (nx = ny for square domains).
        alpha: Thermal diffusivity [m²/s].
        Lx: Domain length in x [m].
        Ly: Domain length in y [m].
        t_final: Final simulation time [s].
        safety_factor: CFL safety factor.

    Returns:
        List of dicts with columns: nx, ny, dx, dy, dt, error_l2,
        error_linf, observed_order, elapsed_time.
    """
    if nx_values is None:
        nx_values = [11, 21, 41, 81]

    results: list[dict] = []

    for i, nx in enumerate(nx_values):
        ny = nx
        domain = Domain2D(Lx=Lx, Ly=Ly, nx=nx, ny=ny)

        # Initial condition: first mode of the analytical solution
        T_init = analytical_solution(domain.x, domain.y, 0.0, Lx, Ly, alpha)

        # Solve
        t_start = time.perf_counter()
        result = solve_thermal_2d(
            domain=domain,
            T_init=T_init,
            alpha=alpha,
            t_total=t_final,
            t_boundary=0.0,  # Homogeneous Dirichlet
            safety_factor=safety_factor,
        )
        elapsed = time.perf_counter() - t_start

        # Analytical solution at t_final
        T_exact = analytical_solution(domain.x, domain.y, t_final, Lx, Ly, alpha)

        # Errors (interior only, exclude boundaries)
        diff = result.T_final[1:-1, 1:-1] - T_exact[1:-1, 1:-1]
        error_l2 = float(np.sqrt(np.mean(diff**2)))
        error_linf = float(np.max(np.abs(diff)))

        # Observed order (needs previous result)
        observed_order = None
        if i > 0 and results[i - 1]["error_l2"] > 0 and error_l2 > 0:
            prev = results[i - 1]
            ratio_h = prev["dx"] / domain.dx
            ratio_e = prev["error_l2"] / error_l2
            if ratio_h > 1 and ratio_e > 1:
                observed_order = float(math.log(ratio_e) / math.log(ratio_h))

        results.append(
            {
                "nx": nx,
                "ny": ny,
                "dx": domain.dx,
                "dy": domain.dy,
                "dt": result.dt,
                "error_l2": error_l2,
                "error_linf": error_linf,
                "observed_order": observed_order,
                "elapsed_time": elapsed,
            }
        )

    return results


def export_convergence_csv(results: list[dict], output_path: Path) -> Path:
    """Export convergence results to CSV.

    Args:
        results: List of convergence results.
        output_path: Path to save CSV.

    Returns:
        Path to saved CSV.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "nx",
        "ny",
        "dx",
        "dy",
        "dt",
        "error_l2",
        "error_linf",
        "observed_order",
        "elapsed_time",
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            row = {k: r[k] for k in fieldnames}
            if row["observed_order"] is None:
                row["observed_order"] = ""
            writer.writerow(row)

    return output_path


def plot_convergence(results: list[dict], output_path: Path) -> Path:
    """Plot convergence analysis (log-log error vs dx).

    Args:
        results: List of convergence results.
        output_path: Path to save figure.

    Returns:
        Path to saved figure.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dx_vals = [r["dx"] for r in results]
    l2_vals = [r["error_l2"] for r in results]
    linf_vals = [r["error_linf"] for r in results]

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.loglog(dx_vals, l2_vals, "o-", label="L2 error", linewidth=2, markersize=8)
    ax.loglog(dx_vals, linf_vals, "s--", label="L∞ error", linewidth=2, markersize=8)

    # Reference O(dx²) line
    dx_ref = np.array(dx_vals)
    scale = l2_vals[0] / dx_ref[0] ** 2
    ax.loglog(dx_ref, scale * dx_ref**2, ":", color="gray", label="O(dx²) reference", linewidth=1.5)

    ax.set_xlabel("Grid spacing dx [m]")
    ax.set_ylabel("Error")
    ax.set_title("Convergence Analysis — 2D Heat Equation\n[demonstrativo — não calibrado]")
    ax.legend()
    ax.grid(True, alpha=0.3, which="both")

    # Annotate observed orders
    orders = [r["observed_order"] for r in results]
    for _i, (dx, e, order) in enumerate(zip(dx_vals, l2_vals, orders, strict=True)):
        if order is not None:
            ax.annotate(
                f"p={order:.2f}",
                (dx, e),
                textcoords="offset points",
                xytext=(10, 10),
                fontsize=9,
            )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path
