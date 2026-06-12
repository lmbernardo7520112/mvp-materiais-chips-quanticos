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
