# Policy v0.4

> **Date:** 2026-05-10
> **Status:** ACTIVATED

## v0.4 policy activation record

- A policy real foi ativada (`current_stage: v0.4`).
- Isso NÃO implementa Poisson.
- Isso NÃO implementa rho_eff.
- Isso apenas prepara os gates para a fase de implementação.
- A implementação futura deverá vir através de um PR estruturado via TDD.

---

## Authorized policy.json Settings

```json
{
  "current_stage": "v0.4",
  "stages": {
    "v0.4": {
      "adr_required": "ADR-007",
      "adr_status_required": "Accepted",
      "scope_allowed_in_code": [
        "poisson_solver_2d.py",
        "effective_charge.py",
        "test_poisson_solver_2d.py",
        "test_effective_charge.py",
        "run_poisson_bridge.py"
      ],
      "terms_allowed_in_authorized_files": [
        "poisson",
        "rho_eff",
        "delta_rho_eff",
        "effective_charge",
        "poisson_solver"
      ],
      "terms_forbidden_everywhere": [
        "schrodinger",
        "schroedinger",
        "tcad",
        "qtcad",
        "coherence_time",
        "t1_time",
        "t2_time",
        "gate_fidelity",
        "charge_noise_psd"
      ],
      "terms_forbidden_in_src_except_authorized": [
        "poisson",
        "rho_eff"
      ],
      "documentation_required": [
        "docs/adr/ADR-007-v0.4-poisson-bridge-scope.md",
        "docs/decision_briefs/v0.4_boussinesq_inspired_charge_closure.md",
        "docs/parameters.md",
        "docs/hipoteses_e_limitacoes.md"
      ],
      "required_artifacts": {
        "figures_minimum": 10,
        "csv_minimum": 4
      },
      "coverage_minimum": 70,
      "overclaim_gates": {
        "require_delta_rho_documentation": true,
        "require_general_poisson_form_in_docs": true,
        "block_device_predictions": true,
        "block_calibration_claims": true
      }
    }
  }
}
```

---

## Gate Updates

### Scope Guardrails

| Scope | v0.3 (current) | v0.4 (proposed) |
|-------|-----------------|-----------------|
| `poisson` in src/ | ❌ Forbidden | ✅ Allowed in authorized files |
| `rho_eff` in src/ | ❌ Forbidden | ✅ Allowed in authorized files |
| `schrodinger` in src/ | ❌ Forbidden | ❌ Forbidden |
| `tcad` in src/ | ❌ Forbidden | ❌ Forbidden |
| `poisson` in docs/ | ✅ Allowed | ✅ Allowed |
| `rho_eff` in docs/ | ✅ Allowed | ✅ Allowed |

### Documentation Requirements

When using the homogeneous-permittivity form ∇²φ = −δρ_eff/ε:
- **Must** include a note: "homogeneous-permittivity simplification."
- **Must** reference the general form ∇·(ε∇φ) = −δρ_eff.

### Overclaim Prevention

- No output may be labeled "predicted charge density" or "device potential."
- All charge-related parameters must have tier classification.
- README must disclaim physical accuracy.
