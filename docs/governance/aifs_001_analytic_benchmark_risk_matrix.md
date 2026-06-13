# AIFS-001 Analytic Benchmark Risk Matrix

| Risk | Severity | Failure Mode | Mitigation | Responsible Skill | Release Gate |
|------|----------|--------------|------------|-------------------|--------------|
| R1 — Analytic benchmark mistaken for project physics. | Critical | False calibration claims based on toy PDE. | Explicitly document mathematical problem is a manufactured toy. | ai-failure-mode-review | G22, G23, G24 |
| R2 — PINN implementation begins before ADR acceptance. | Critical | Unapproved runtime changes block releases. | Enforce documentation-only constraint in AIFS-001. | release-manager | G15, G16 |
| R3 — ML dependency added without dependency decision. | Critical | PyTorch/JAX bloats repository silently. | Run dependency checks in CI and quality gates. | dependency-governance | G8, G9 |
| R4 — Benchmark result interpreted as solver validation. | Critical | PINN is falsely claimed to validate the classical Poisson solver. | Explicitly state baselines are for PINN evaluation, not solver validation. | ai-failure-mode-review | G21 |
| R5 — Physical phi inferred from toy u(x). | Critical | Users treat sin(pi x) as physical potential. | Prohibit physical phi interpretation. | physics-dimensional-audit | G22 |
| R6 — C1/C2/C3 imported accidentally. | High | AIFS code couples with canonical tracks. | Isolate namespace and enforce static analysis. | scope-guardrails | G20 |
| R7 — Stochastic reproducibility ignored. | High | Benchmark passes once, fails on re-run. | Require explicit seed protocols in future spec. | tdd-red-green-release | G11 |
| R8 — Error metric omitted. | High | "Looks good" replaces quantitative L2/residual norms. | Require L2, L∞, and residual metrics in spec. | report-auditor | G11 |
| R9 — Sign convention of PDE not explicit. | High | f(x) sign flips cause inverse solutions. | Explicitly state operator convention -u'' = f. | physics-dimensional-audit | G11 |
| R10 — AIFS distracts from C3 canonical roadmap. | Medium | Core contributors abandon C3 for PINNs. | Label AIFS as slow-lane exploratory track. | release-acceleration-lanes | G1, G25 |
