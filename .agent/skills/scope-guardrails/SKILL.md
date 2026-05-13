---
name: scope-guardrails
description: >
  Use this skill to protect the scientific and engineering scope of the MVP
  Quantum Materials project. It defines what is in-scope, what is deferred,
  and what is prohibited, ensuring no unauthorized physics or features are
  introduced without proper ADR governance.
---

# Scope Guardrails — Scientific Boundary Protection Skill

## When to Use

Activate this skill whenever you are asked to:

- Implement any new feature or physics.
- Evaluate whether a requested change is in-scope.
- Review a PR or task for scope creep.
- Decide whether to proceed with an implementation or request an ADR first.

## Project Scientific Anchors

This project is anchored in:

| Anchor | Description |
|--------|-------------|
| **Material** | Silicon (Si) / CMOS technology |
| **Context** | Spin-qubit semiconductor devices |
| **Defect model** | `C_def` — adimensional reaction-diffusion proxy |
| **Thermal model** | Explicit Euler, demonstrative parameters |
| **Electrostatic model** | Poisson Bridge — demonstrative/metadata-safe |
| **Scale mode** | Option B: metadata + literature-scaled constants |
| **Physical interpretation** | NOT authorized (demonstrative mode) |
| **Option C** | Deferred — requires dedicated ADR |

## Currently Authorized (v0.4.x)

- ✅ Demonstrative simulations with toy parameters.
- ✅ Literature-scaled SI constants (ε_r, ε₀, q_e, k_B).
- ✅ Scale mode metadata in CSV outputs.
- ✅ Documentation, governance, and infrastructure changes.
- ✅ Test additions that verify existing behavior.
- ✅ Agent Skills (Markdown-only, project-scoped).

## Explicitly Deferred (Requires ADR)

The following are **not authorized** without a dedicated ADR, decision brief,
council deliberation, and acceptance gates:

| Item | Required Governance |
|------|-------------------|
| Option C implementation | ADR amendment to ADR-008 |
| D_it → D_it_SI conversion in solver | ADR + TDD plan |
| σ_eff / ρ_eff physical computation | ADR + TDD plan |
| t_eff physical conversion | ADR + TDD plan |
| delta_E_window calculation | ADR + TDD plan |
| ε substitution in solver (ε_r·ε₀) | ADR + TDD plan |
| Physical φ interpretation | ADR + council approval |
| Poisson non-linear terms | ADR for v0.5+ |
| Self-consistency loop | ADR for v0.5+ |
| Schrödinger equation | ADR for v0.5+ |
| v0.5 features | Strategic decision |

## Absolutely Prohibited

The following are **never** permitted regardless of governance:

- Introducing physics outside silicon/CMOS scope.
- Making calibration claims without experimental data.
- Predicting device performance.
- Predicting qubit coherence or fidelity.
- Predicting charge noise as a real measurement.
- Citing forbidden terms defined in `policy.json`.
- Overclaiming model capabilities.

## Decision Flow

When a task requests something that might be out of scope:

```
Is it documentation/governance only?
├── Yes → Proceed (no physics impact)
└── No → Does it change src/ or scripts/?
    ├── No → Proceed (infrastructure only)
    └── Yes → Is it authorized by current ADR/policy?
        ├── Yes → Proceed with TDD discipline
        └── No → STOP
            ├── Create ADR/Decision Brief
            ├── Convene Council
            ├── Define Acceptance Gates
            ├── Get user approval
            └── Only then proceed
```

## Scope Violation Indicators

Watch for these red flags:

- Modifying `effective_charge.py` without ADR authorization.
- Modifying `poisson_solver_2d.py` equation terms.
- Changing `policy.json` `current_stage`.
- Setting `physical_interpretation_allowed = True`.
- Setting `option_c_enabled = True`.
- Adding new physical constants without evidence tier.
- Using calibrated language for demonstrative results.
- Implementing features labeled "v0.5+" in the roadmap.

## Response to Scope Violation

If you detect a scope violation:

1. **Stop** the current implementation.
2. **Report** the violation with specific file/line/term.
3. **Recommend** the governance path (ADR, council, etc.).
4. **Do not** proceed with the implementation.
5. **Do not** weaken guardrails to accommodate the request.
