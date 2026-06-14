# Acceptance Gates for ADR-016 One-way Poisson Coupling

## v0.8.5 Documentation-Only Gates

The following gates must be satisfied for v0.8.5 to be merged. These verify that the release is strictly documentation-only:

| Gate | Criterion | Status |
| :--- | :--- | :--- |
| G1 | Release is documentation-only. | |
| G2 | Zero `src/` changes. | |
| G3 | Zero `tests/` changes. | |
| G4 | Zero `scripts/` changes. | |
| G5 | `pyproject.toml` unchanged. | |
| G6 | `tools/quality_gates/policy.json` unchanged. | |
| G7 | `.agent/skills/` unchanged. | |
| G8 | ADR-016 status = Proposed. | |
| G9 | No Poisson runtime. | |
| G10 | No solver coupling. | |
| G11 | No physical phi. | |
| G12 | No dummy phi. | |
| G13 | No potential grid. | |
| G14 | No calibration claims. | |
| G15 | No device prediction. | |
| G16 | No AIFS runtime. | |
| G17 | No paid API. | |
| G18 | No external SDK. | |
| G19 | No goal-like autonomous execution. | |
| G20 | BudgetOps PASS. | |
| G21 | Usage Ledger PASS. | |
| G22 | Quality gates PASS. | |
| G23 | pytest PASS. | |
| G24 | Coverage >= 70%. | |
| G25 | ruff PASS. | |
| G26 | pyright 0 errors. | |
| G27 | `generate_all_results` PASS. | |
| G28 | CI PASS. | |

## Future ADR-016 Acceptance Gates

To transition ADR-016 from `Proposed` to `Accepted`, the following additional gates must be cleared in a dedicated acceptance review release (e.g. v0.8.6):

1. **Methodological Alignment** — Confirm that one-way coupling aligns with the incremental demonstrative goals.
2. **Scientific Integrity** — Confirm Option B scale modes are correctly proposed.
3. **Risk Matrix Completeness** — Confirm all 10 risks are addressed.
4. **Process Adherence** — Confirm no implementation occurred during the Proposal phase.
5. **Council Deliberation** — Form council and record vote.

Upon acceptance, a dedicated RED phase branch may be created.
