# ADR-016 Risk Matrix

| Risk Category | Specific Risk | Severity | Mitigation |
| :--- | :--- | :--- | :--- |
| **Scientific Claim** | Outputting a potential that users interpret as physically predictive. | High | Explicitly mark the potential as `demonstrative` and `dummy`. No self-consistency. |
| **Scope Creep** | Adding self-consistent iterations during implementation. | High | TDD RED phase must explicitly test that self-consistency loops are NOT present or raise errors if attempted. |
| **Coupling Complexity** | Incorrect scaling between C3 projection and Poisson solver. | Medium | Use established Option B scale modes. Unit testing must verify metadata propagation and dimensional consistency. |
| **Process Deviation** | Implementing the coupling before ADR is accepted. | Medium | Strict adherence to Phase Separation (RED/GREEN). This ADR only authorizes documentation. |
