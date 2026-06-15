# Human Decision Log

This log captures critical human decisions made during AI-assisted development of the MVP Quantum Materials project. Each entry records the decision, rationale, rejected alternatives, and responsibility boundaries.

---

## HDL-001 — Reject operational E0 / enforce E1 minimum

- **Date:** ~v0.5.4–v0.5.6
- **Release:** v0.5.6
- **Human Decision:** Reject operational E0 demonstrative profiles; enforce E1 literature-informed as the minimum evidence tier for energy profile usage.
- **Rationale:** E0 profiles lack any literature grounding and would produce results with no scientific anchor. Using them operationally would invite overclaims about D_it(E) behavior.
- **AI Suggestion:** AI initially proposed E0 demonstrative profiles as a fast path.
- **Alternatives Rejected:** E0 operational usage; S0 operational usage.
- **Evidence:** repository narrative / prior reports; refresh if needed. See `docs/decision_briefs/v0.5.6_no_demonstrative_evidence_profiles_brief.md`.
- **Files Affected:** energy_profiles.py, dit_profile_library.py, test fixtures.
- **Future Consequence:** All operational profiles must be E1+ (literature-informed). S0 restricted to test fixtures only.
- **Reversible:** Conditional — requires ADR to promote E0.

---

## HDL-002 — Reject generic physical t_eff

- **Date:** ~v0.7.0–v0.7.2
- **Release:** v0.7.0
- **Human Decision:** Reject AI proposal for a generic physical t_eff (effective thickness) parameter. t_eff must not be used as a free calibration knob.
- **Rationale:** A generic t_eff without experimental or literature anchor would be a false degree of freedom, creating an illusion of physical grounding.
- **AI Suggestion:** AI proposed t_eff as a convenient bridge parameter.
- **Alternatives Rejected:** Free t_eff parameter; t_eff from unanchored estimation.
- **Evidence:** repository narrative / prior reports; refresh if needed. See ADR-012 discussions.
- **Files Affected:** c2_charge_mapping.py design decisions.
- **Future Consequence:** t_eff can only be introduced with explicit experimental depth prior and ADR acceptance.
- **Reversible:** Conditional — requires ADR with experimental evidence.

---

## HDL-003 — Accept depth priors only as conditional evidence, not calibration

- **Date:** ~v0.7.0
- **Release:** v0.7.0
- **Human Decision:** Depth priors from literature may inform regularization length but must never be presented as calibration data.
- **Rationale:** Literature values for interface thickness are approximations from different device contexts. Treating them as calibration would be scientifically dishonest.
- **AI Suggestion:** AI considered using literature depth values directly.
- **Alternatives Rejected:** Direct calibration from literature depth priors.
- **Evidence:** repository narrative / prior reports; refresh if needed. See `docs/decision_briefs/v0.7.0_c2_interface_source_regularization_brief.md`.
- **Files Affected:** c2_charge_mapping.py, DepthPriorMetadata design.
- **Future Consequence:** DepthPriorMetadata and ExperimentalDepthPriorMetadata exist as metadata containers, not calibration assertions.
- **Reversible:** Conditional — requires experimental data and ADR.

---

## HDL-004 — Reject pandas dependency for v0.7.4

- **Date:** ~v0.7.4
- **Release:** v0.7.4
- **Human Decision:** Reject adding pandas to pyproject.toml. Use Python stdlib csv module instead.
- **Rationale:** The demo CSV is small and deterministic. pandas would add unnecessary dependency weight, CI install time, and transitive dependencies for a trivial read/write operation.
- **AI Suggestion:** AI initially used pandas for CSV reading in tests.
- **Alternatives Rejected:** Adding pandas as runtime or dev dependency.
- **Evidence:** See `docs/decision_briefs/v0.7.4_csv_vs_pandas_dependency_decision.md`.
- **Files Affected:** test_c2_charge_mapping_demo.py, run_c2_charge_mapping_demo.py.
- **Future Consequence:** CSV operations use stdlib. pandas may be reconsidered only if complex tabular analysis becomes formal scope.
- **Reversible:** Yes — with dependency decision brief.

---

## HDL-005 — Correct v0.7.5 closure inconsistency

- **Date:** ~v0.7.4
- **Release:** v0.7.4
- **Human Decision:** Correct the AI report that incorrectly recommended "v0.7.5 closure" as the next step when the actual release being closed was v0.7.4.
- **Rationale:** The project follows strict sequential versioning. Recommending a nonexistent v0.7.5 closure during v0.7.4 audit would create confusion and an unreachable state.
- **AI Suggestion:** AI report contained "Next step: v0.7.5 closure (audit + merge + tag)".
- **Alternatives Rejected:** Accepting the incorrect version reference.
- **Evidence:** repository narrative / prior reports; refresh if needed.
- **Files Affected:** Closure report corrections.
- **Future Consequence:** Reinforced that AI-generated version numbers must be verified against actual project state.
- **Reversible:** No — correction was factual.

---

## HDL-006 — Require methodology acceleration without reducing scientific rigor

- **Date:** 2026-06-12
- **Release:** v0.7.5
- **Human Decision:** Create acceleration skills and templates to reduce bureaucratic overhead while preserving ADR/TDD/CI discipline and scientific governance.
- **Rationale:** The methodology dossier identified bureaucratic overhead as a risk. Acceleration must come from reducing redundant documentation, not from skipping scientific decision gates.
- **AI Suggestion:** N/A — this was a human-initiated decision.
- **Alternatives Rejected:** Continuing without acceleration tooling; reducing governance rigor.
- **Evidence:** See `docs/governance/ai_rse_methodology_dossier.md`, Section 14 (Weaknesses).
- **Files Affected:** New skills, templates, checklists in v0.7.5.
- **Future Consequence:** v0.8.x work can use fast lanes for documentation-only releases and slow lanes for physics-critical work.
- **Reversible:** Yes — skills are additive and can be deprecated.

---

## HDL-007 — Open AI-for-Science exploration only as a parallel governed track

- **Date:** 2026-06-12
- **Release:** v0.7.6
- **Human Decision:** Explore AI-for-Science / PINNs / surrogate models only as a documentation-first parallel track, fully isolated from the classical solver roadmap.
- **Rationale:** AI-for-Science methods may offer future value for parametric studies or inverse problems, but the classical solver is not yet coupled (C3 pending). Implementing ML now would risk overclaims, dependency bloat, and contamination of the governed classical path.
- **AI Suggestion:** N/A — this was a human-initiated decision to evaluate the topic proactively.
- **Alternatives Rejected:** Implement PINN now; add ML dependencies now; replace classical solver; claim AI-for-Science validation.
- **Evidence:** See `docs/adr/ADR-014-ai-for-science-parallel-track-governance.md`, `docs/decision_briefs/v0.7.6_ai_for_science_parallel_track_brief.md`, `docs/research_council/v0.7.6_ai_for_science_parallel_track_council.md`.
- **Files Affected:** Documentation only. Zero src/tests/scripts/pyproject changes.
- **Future Consequence:** ADR-014 proposed. No code, no dependency. Future implementation requires accepted ADR, dependency decision, analytic benchmarks, RED tests, reproducibility plan, and human approval.
- **Reversible:** Yes — through future ADR acceptance or rejection.

## HDL-008 — Resume classical C3 solver coupling strategy after opening AI-for-Science parallel track

- **Release:** v0.8.0
- **Human Decision:** keep classical C3 as primary roadmap and treat AI-for-Science as future parallel, non-blocking track
- **Rationale:** preserve solver traceability and avoid contaminating classical physics path
- **Alternatives Rejected:**
  - direct Poisson coupling now
  - implement PINN/surrogate before C3 projection
  - replace classical solver
  - claim physical phi before projection and solver gates
- **Consequence:**
  - ADR-013 Proposed
  - no code
  - no tests
  - future C3 RED requires ADR-013 acceptance
- **Reversible:** conditional, through future ADR

## HDL-009 — Decide ADR-013 acceptance scope for C3 conservative grid projection

- **Release:** v0.8.1
- **Human Decision:** accept ADR-013 only if acceptance criteria are satisfied
- **Rationale:** permit future RED while blocking implementation and solver runtime
- **Alternatives Rejected:**
  - implement C3 immediately
  - create RED before ADR acceptance
  - run Poisson from C2/C3 now
  - allow physical phi
  - involve AI-for-Science runtime
- **Consequence:**
  - if accepted, v0.8.2 may create C3 RED
  - no GREEN authorized
  - no solver runtime authorized
- **Reversible:** conditional, through future ADR amendment

## HDL-010 — Advance AI-for-Science only as analytic benchmark design

* release/package: AIFS-001
* human decision: advance AI-for-Science in parallel only through documentation-only analytic benchmark design
* rationale: allow parallel intellectual progress without contaminating C3 classical development
* alternatives rejected:
  * implement PINN now
  * add ML dependencies now
  * create notebook now
  * use C1/C2/C3 as ML benchmark now
  * replace classical solver
* consequence:
  * ADR-015 Proposed
  * benchmark design created
  * no runtime
  * no dependency
  * no C3 interaction
* reversible: yes, through future ADR

## HDL-011 — One-way Poisson Coupling Strategy (ADR-016)

* release/package: v0.8.5
* human decision: advance classical track with a one-way demonstrative coupling to the Poisson solver
* rationale: demonstrate C3 charge electrostatics without self-consistency, preserving C3 isolation and scope
* alternatives rejected:
  * self-consistent coupling
  * full drift-diffusion coupling
  * implement Poisson runtime now
  * produce physical phi now
  * claim calibration or device prediction
  * involve AI-for-Science runtime
* consequence:
  * ADR-016 Proposed
  * documentation-only phase
  * no implementation or testing authorized yet
  * no Poisson runtime
  * no physical phi
  * no solver coupling
  * no calibration claims
  * no device prediction
  * no AIFS runtime
  * BudgetOps validation required for future implementation
  * Usage Ledger validation required for future implementation
* reversible: yes, through future ADR acceptance or rejection

## HDL-012 — Accept ADR-016 for future RED planning only.

- **Date:** 2026-06-14
- **Release:** v0.8.6
- **Human Decision:** Accept ADR-016 purely for strategy and to authorize future RED planning phase.
- **Rationale:** The council unanimously recommended acceptance with strict non-physical, demonstrative boundary conditions. Risk profile is thoroughly mitigated.
- **Alternatives Rejected:** Keep Proposed; Reject; Authorize implementation directly.
- **Evidence:** `docs/decision_briefs/v0.8.6_adr016_acceptance_review.md` and `docs/research_council/v0.8.6_adr016_acceptance_council.md`.
- **Files Affected:** `docs/adr/ADR-016-one-way-poisson-coupling-strategy.md` status updated.
- **Future Consequence:** Future RED phase is allowed, but no implementation, Poisson runtime, or dummy phi output is authorized yet. BudgetOps and Usage Ledger are mandatory.
- **Reversible:** Yes — RED plans can be rejected.

## HDL-013 — Authorize assisted autonomy dry-run for v0.8.7 RED planning only

- **Date:** 2026-06-14
- **Release:** v0.8.7
- **Human Decision:** Authorize assisted autonomy dry-run for RED planning documentation.
- **Rationale:** Test the Autonomy-001/002 infrastructure in assisted mode with zero external cost.
- **Constraints:**
  * No `/goal`.
  * No goal-like autonomous execution.
  * No external SDK.
  * No paid API.
  * No implementation.
  * No tests.
  * No merge (PR only).
  * No tag.
  * External estimated cost: R$ 0.00.
- **Alternatives Rejected:** Full autonomous execution; deferred planning.
- **Evidence:** `docs/governance/v0.8.7_autonomy_usage_report.md`.
- **Files Affected:** Documentation only in `docs/`.
- **Future Consequence:** Future v0.8.8 RED tests require new human approval.
- **Reversible:** Yes — PR can be closed without merge.

## HDL-014 — Authorize v0.8.8 RED-only tests for one-way Poisson coupling

- **Date:** 2026-06-15
- **Release:** v0.8.8
- **Human Decision:** Authorize RED tests only for one-way Poisson coupling.
- **Rationale:** v0.8.7 planned 10 RED categories. v0.8.8 creates 20 concrete tests.
- **Constraints:**
  * No implementation.
  * No GREEN.
  * No Poisson runtime.
  * No physical phi.
  * No SDK.
  * No paid API.
  * No `/goal`.
  * No goal-like autonomous execution.
  * No merge (PR only).
  * No tag.
  * External estimated cost: R$ 0.00.
- **Alternatives Rejected:** Implement GREEN directly; defer RED further.
- **Evidence:** `docs/governance/v0.8.8_red_plan.md`, `tests/test_one_way_poisson_coupling_red.py`.
- **Files Affected:** `tests/test_one_way_poisson_coupling_red.py`, docs in `docs/`.
- **Future Consequence:** Future v0.8.9 GREEN requires new human approval after external audit.
- **Reversible:** Yes — PR can be closed; tests can be removed.

## HDL-015 — Ratify v0.8.8 policy exception for RED file

- **Date:** 2026-06-15
- **Release:** v0.8.8
- **Human Decision:** Ratify minimal policy exception.
- **File authorized:** `test_one_way_poisson_coupling_red.py`.
- **Policy field:** `authorized_files` only.
- **Reason:** Allow conditionally-forbidden term "Poisson" in ADR-016 RED test file.
- **Evidence:** `docs/governance/v0.8.8_policy_exception_ratification.md`, `docs/decision_briefs/v0.8.8_red_policy_exception_review.md`.
- **Constraints:**
  * No implementation authorized.
  * No GREEN authorized.
  * No Poisson runtime authorized.
  * No physical phi authorized.
  * No paid API.
  * No SDK.
  * No `/goal`.
  * External estimated cost: R$ 0.00.
- **Reversible:** Yes — file can be removed from `authorized_files` if RED is reverted.

## HDL-016 — Authorize v0.8.9 GREEN minimum for one-way Poisson coupling

- **Date:** 2026-06-15
- **Release:** v0.8.9
- **Human Decision:** Authorize GREEN minimum.
- **Scope:** Metadata-only adapter contract.
- **Constraints:**
  * No Poisson runtime.
  * No solver execution.
  * No physical phi.
  * No calibration.
  * No device prediction.
  * No paid API.
  * No SDK.
  * No `/goal`.
  * External estimated cost: R$ 0.00.
  * Merge/tag require future human approval.
- **Policy Extension:** `one_way_poisson_coupling.py` added to `authorized_files` (same pattern as `poisson_solver_2d.py`). Requires human ratification.
- **Evidence:** `src/mvp_quantum_materials/one_way_poisson_coupling.py`, `docs/governance/v0.8.9_green_plan.md`.
- **Files Affected:** 1 src file, docs in `docs/`, `policy.json` authorized_files.
- **Reversible:** Yes — module can be removed; tests will revert to RED.
