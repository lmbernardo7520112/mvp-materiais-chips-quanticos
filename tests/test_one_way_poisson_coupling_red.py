"""RED test suite for future one-way Poisson coupling module (v0.8.8).

This file contains RED-phase tests for the future module
``mvp_quantum_materials.one_way_poisson_coupling``, authorized by ADR-016.

**Expected behaviour during RED phase:**

* The target module does NOT exist yet.
* Most tests MUST fail with ``ModuleNotFoundError`` or ``ImportError``.
* Static guardrail tests (categories 8–10) MAY pass because they verify
  the *absence* of forbidden artefacts rather than the *presence* of new code.
* No implementation should be created to make these tests pass.
* A future GREEN phase (v0.8.9+) will provide the minimal implementation,
  only after explicit human authorization.

Target future module:
    ``src/mvp_quantum_materials/one_way_poisson_coupling.py``

Constraints:
    - No ``solve_poisson`` invocation.
    - No ``poisson_solver_2d`` import.
    - No paid API, external SDK, or goal-like autonomous execution.
    - No physical phi, calibration claims, or device prediction.
"""

from __future__ import annotations

import importlib
import pathlib
import re

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TARGET_MODULE = "mvp_quantum_materials.one_way_poisson_coupling"

_FORBIDDEN_PUBLIC_NAMES = frozenset(
    {
        "phi",
        "voltage",
        "physical_potential",
        "electrostatic_potential",
    }
)


def _import_target():
    """Attempt to import the target module; expected to fail during RED."""
    return importlib.import_module(_TARGET_MODULE)


# ===================================================================
# CATEGORY 1 — Import contract
# ===================================================================


def test_future_one_way_poisson_module_import_contract():
    """RED: the future module must be importable once implemented."""
    mod = _import_target()
    assert mod is not None, "Module should be importable"


def test_future_public_api_symbols_are_required():
    """RED: the future module must expose required public symbols."""
    mod = _import_target()
    required_symbols = [
        "OneWayPoissonCouplingMetadata",
        "PoissonInputSource",
        "build_poisson_input_source",
        "validate_no_physical_phi_claim",
        "validate_no_solver_runtime_coupling",
    ]
    for sym in required_symbols:
        assert hasattr(mod, sym), f"Module must export {sym}"


# ===================================================================
# CATEGORY 2 — Source-to-Poisson input adapter contract
# ===================================================================


def test_future_adapter_accepts_projected_c3_source_contract():
    """RED: adapter must accept C3-projected charge density."""
    mod = _import_target()
    fn = getattr(mod, "build_poisson_input_source")  # noqa: B009
    # Conceptual contract: fn must accept a dict with "projected_charge"
    assert callable(fn), "build_poisson_input_source must be callable"


def test_future_adapter_requires_boundary_metadata_contract():
    """RED: adapter must require boundary metadata."""
    mod = _import_target()
    fn = getattr(mod, "build_poisson_input_source")  # noqa: B009
    # Contract: calling without boundary metadata should raise
    with pytest.raises((TypeError, ValueError)):
        fn(projected_charge=[0.0])  # missing boundary metadata


# ===================================================================
# CATEGORY 3 — No physical phi metadata
# ===================================================================


def test_future_metadata_physical_phi_is_forbidden():
    """RED: metadata must forbid physical_phi_allowed=True."""
    mod = _import_target()
    meta_cls = getattr(mod, "OneWayPoissonCouplingMetadata")  # noqa: B009
    with pytest.raises((ValueError, TypeError)):
        meta_cls(physical_phi_allowed=True)


def test_future_metadata_requires_demonstrative_only_status():
    """RED: metadata must default to demonstrative_only."""
    mod = _import_target()
    meta_cls = getattr(mod, "OneWayPoissonCouplingMetadata")  # noqa: B009
    meta = meta_cls()
    assert getattr(meta, "interpretation_status", None) == "demonstrative_only"


# ===================================================================
# CATEGORY 4 — No calibration flags
# ===================================================================


def test_future_calibration_claims_are_forbidden():
    """RED: metadata must block calibration_status != 'not_calibrated'."""
    mod = _import_target()
    meta_cls = getattr(mod, "OneWayPoissonCouplingMetadata")  # noqa: B009
    with pytest.raises((ValueError, TypeError)):
        meta_cls(calibration_status="calibrated")


def test_future_device_prediction_claims_are_forbidden():
    """RED: metadata must block device_prediction_enabled=True."""
    mod = _import_target()
    meta_cls = getattr(mod, "OneWayPoissonCouplingMetadata")  # noqa: B009
    with pytest.raises((ValueError, TypeError)):
        meta_cls(device_prediction_enabled=True)


# ===================================================================
# CATEGORY 5 — No potential/voltage naming
# ===================================================================


def test_future_api_must_not_expose_phi_or_voltage_names():
    """RED: public API must not expose forbidden names."""
    mod = _import_target()
    public = {n for n in dir(mod) if not n.startswith("_")}
    violations = public & _FORBIDDEN_PUBLIC_NAMES
    assert not violations, f"Forbidden public names found: {violations}"


def test_future_output_metadata_must_use_source_terms_not_potential_terms():
    """RED: output metadata must use 'source'/'input' vocabulary."""
    mod = _import_target()
    source_cls = getattr(mod, "PoissonInputSource")  # noqa: B009
    instance = source_cls.__new__(source_cls)
    # Check that class attributes/fields use source terms
    fields = [f for f in dir(instance) if not f.startswith("_")]
    for f in fields:
        assert "potential" not in f.lower(), f"Field {f} uses forbidden term"
        assert "voltage" not in f.lower(), f"Field {f} uses forbidden term"


# ===================================================================
# CATEGORY 6 — Boundary metadata required
# ===================================================================


def test_future_boundary_condition_metadata_required():
    """RED: boundary condition metadata must be mandatory."""
    mod = _import_target()
    meta_cls = getattr(mod, "OneWayPoissonCouplingMetadata")  # noqa: B009
    # Contract: creating metadata without boundary_type should raise
    with pytest.raises((TypeError, ValueError)):
        meta_cls(boundary_type=None)


def test_future_boundary_metadata_must_be_non_physical_interpretation():
    """RED: boundary metadata must declare non-physical interpretation."""
    mod = _import_target()
    meta_cls = getattr(mod, "OneWayPoissonCouplingMetadata")  # noqa: B009
    meta = meta_cls(boundary_type="demonstrative")
    assert getattr(meta, "physical_interpretation", None) is False


# ===================================================================
# CATEGORY 7 — Charge conservation inherited from C3
# ===================================================================


def test_future_adapter_preserves_projected_charge_accounting_contract():
    """RED: adapter must preserve source and projected charge."""
    mod = _import_target()
    source_cls = getattr(mod, "PoissonInputSource")  # noqa: B009
    # Contract: instance must have source_charge and projected_charge
    instance = source_cls.__new__(source_cls)
    assert hasattr(instance, "source_charge"), "Must track source_charge"
    assert hasattr(instance, "projected_charge"), "Must track projected_charge"


def test_future_adapter_requires_c3_conservation_evidence():
    """RED: adapter must require C3 conservation evidence."""
    mod = _import_target()
    fn = getattr(mod, "build_poisson_input_source")  # noqa: B009
    with pytest.raises((TypeError, ValueError)):
        fn(
            projected_charge=[0.0],
            boundary_metadata={"type": "demonstrative"},
            c3_conservation_evidence=None,
        )


# ===================================================================
# CATEGORY 8 — Solver invocation blocked until GREEN
# ===================================================================


def test_future_solver_invocation_is_blocked_by_default():
    """RED: solver invocation must be blocked by default."""
    mod = _import_target()
    meta_cls = getattr(mod, "OneWayPoissonCouplingMetadata")  # noqa: B009
    meta = meta_cls()
    assert getattr(meta, "solver_invocation_allowed", True) is False


def test_future_module_must_not_import_poisson_solver_runtime():
    """Static guard: if module absent, no runtime import exists.

    This test may PASS during RED because it verifies absence.
    """
    module_path = pathlib.Path("src/mvp_quantum_materials/one_way_poisson_coupling.py")
    if not module_path.exists():
        # Module absent — static guard passes by definition
        return
    source = module_path.read_text()
    assert "solve_poisson" not in source, "Module must not import solve_poisson runtime"
    assert "from mvp_quantum_materials.poisson_solver_2d" not in source, (
        "Module must not import poisson_solver_2d"
    )


# ===================================================================
# CATEGORY 9 — generate_all_results must not emit physical artifacts
# ===================================================================


def test_generate_all_results_has_no_one_way_poisson_physical_artifact():
    """Static guard: generate_all_results must not reference physical Poisson.

    This test may PASS during RED.
    """
    script = pathlib.Path("scripts/generate_all_results.py")
    assert script.exists(), "generate_all_results.py must exist"
    source = script.read_text()
    assert "one_way_poisson_coupling" not in source, (
        "generate_all_results must not reference one_way_poisson_coupling yet"
    )


def test_results_do_not_contain_poisson_potential_artifacts():
    """Static guard: results/ must not contain potential-field artifacts.

    This test may PASS during RED.
    """
    results_dir = pathlib.Path("results/figures")
    if not results_dir.exists():
        return
    forbidden_patterns = re.compile(r"one_way_poisson|poisson_potential_field|electrostatic_output")
    for f in results_dir.iterdir():
        assert not forbidden_patterns.search(f.name), f"Forbidden artifact found: {f.name}"


# ===================================================================
# CATEGORY 10 — BudgetOps and Usage Ledger required
# ===================================================================


def test_future_red_requires_budgetops_reference():
    """Static guard: acceptance gates must reference BudgetOps.

    This test may PASS during RED.
    """
    gates_paths = [
        pathlib.Path("docs/governance/v0.8.7_red_planning_acceptance_gates.md"),
        pathlib.Path("docs/governance/v0.8.8_red_acceptance_gates.md"),
    ]
    found = False
    for p in gates_paths:
        if p.exists() and "BudgetOps" in p.read_text():
            found = True
            break
    assert found, "Acceptance gates must reference BudgetOps"


def test_future_red_requires_usage_ledger_reference():
    """Static guard: acceptance gates must reference Usage Ledger.

    This test may PASS during RED.
    """
    gates_paths = [
        pathlib.Path("docs/governance/v0.8.7_red_planning_acceptance_gates.md"),
        pathlib.Path("docs/governance/v0.8.8_red_acceptance_gates.md"),
    ]
    found = False
    for p in gates_paths:
        if p.exists() and "Usage Ledger" in p.read_text():
            found = True
            break
    assert found, "Acceptance gates must reference Usage Ledger"
