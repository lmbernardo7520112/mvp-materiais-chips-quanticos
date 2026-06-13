# ADR-016 Risk Matrix

| ID | Risk Category | Specific Risk | Severity | Mitigation |
| :--- | :--- | :--- | :--- | :--- |
| R1 | **Premature Implementation** | Poisson runtime implemented before ADR-016 acceptance. | Critical | ADR-016 must be Accepted via formal review before any RED phase. Non-Authorization Clause enforced. |
| R2 | **Scientific Claim** | Numerical output misread as physical phi. | Critical | All future solver output must carry `demonstrative` and `not_for_physical_interpretation` flags. No `phi`, `potential`, or `voltage` keys allowed in outputs until authorized. |
| R3 | **False Validation** | Demo coupling mistaken for validation of the physical pipeline. | High | Documentation must explicitly state that one-way coupling is architectural, not physically validated. |
| R4 | **Boundary Condition Leakage** | Boundary conditions create false physical meaning in solver output. | High | Future RED tests must verify BCs are demonstrative and do not encode specific device geometry. |
| R5 | **Potential Grid Leakage** | Potential grid appears in outputs before authorization. | High | CI must verify no `phi`, `potential`, `voltage`, or `electrostatic_potential` keys in any CSV/JSON output until ADR acceptance and GREEN phase. |
| R6 | **Calibration Claims** | Calibration claims inferred from numerical solver results. | Critical | Forced `calibration_status: not_calibrated`. No calibration language in any documentation or output metadata. |
| R7 | **Device Prediction** | Device prediction inferred from demonstrative coupling output. | Critical | Scope guardrails prohibit device prediction. Outputs must carry `demonstrative` metadata. |
| R8 | **AIFS Runtime Confusion** | AI-for-Science runtime confused with classical one-way coupling. | Medium | AIFS track remains parallel, documentation-only. No ML imports or dependencies in classical path. |
| R9 | **C3 Guardrail Bypass** | Solver coupling bypasses C3 projection guardrails. | High | Future implementation must route through `project_c2_source_to_grid` only. Direct C2-to-Poisson coupling prohibited. |
| R10 | **Artifact Contamination** | `generate_all_results` starts producing physical-looking artifacts from coupling. | Medium | Future integration must carry `demonstrative` flag in all CSV headers and figure titles. No physical units on axes. |
