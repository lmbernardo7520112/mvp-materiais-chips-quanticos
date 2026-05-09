# AI-RSE GateOps — Version-Aware Quality Gates

> **Status:** Active since v0.3
> **Policy:** `tools/quality_gates/policy.json`

## Purpose

AI-RSE GateOps provides **version-aware, executable quality gates** for
scientific software developed with AI assistance.

**Core principle:** Quality gates do not prevent evolution; they prevent
evolution **out of order**.

## Why Gates Exist

When AI assists in scientific software development, there is a risk of
**scope creep** — introducing physics, dependencies, or terminology that
belongs to a future version. Gates enforce stage discipline:

- Each development stage (v0.3, v0.4, ...) has its own policy.
- The policy defines what is forbidden, required, and allowed.
- Gates are **automatically enforced** in CI.
- Evolution happens **only** through ADR → policy update → PR → CI green.

## Version-Aware Gates

In v0.3, certain terms and implementations are forbidden in code because
their prerequisite infrastructure does not yet exist. For example, the
electrostatic coupling layer requires C_def (v0.3) to exist before it
can be implemented. The gate enforces this ordering.

In a future v0.4, those same terms may be **permitted**, provided:

1. A dedicated ADR (e.g., ADR-007) is accepted.
2. The policy JSON is updated via PR.
3. The `current_stage` is changed.
4. Tests and documentation are updated.
5. CI passes with the new policy.

## Gates

| Gate | Description |
|------|-------------|
| ADR status | Required ADRs must exist and have correct status |
| Scope guardrails | Forbidden terms must not appear in src/scripts/tests |
| Solver integrity | Critical solver files must not have unauthorized changes |
| Required docs | Mandatory governance documents must exist |
| Artifacts | Required figures and CSVs must be generated |
| Private terms | Terms excluded by the user (loaded from env/local file) |

## How to Run Locally

```bash
# Generate artifacts first
python scripts/generate_all_results.py --output-dir results/figures

# Run all gates
PYTHONPATH=. python tools/quality_gates/run_all_quality_gates.py --require-artifacts

# Run individual gates
PYTHONPATH=. python tools/quality_gates/check_scope_guardrails.py
PYTHONPATH=. python tools/quality_gates/check_adr_status.py
PYTHONPATH=. python tools/quality_gates/check_solver_integrity.py
PYTHONPATH=. python tools/quality_gates/check_docs_required.py
PYTHONPATH=. python tools/quality_gates/check_artifacts.py
PYTHONPATH=. python tools/quality_gates/check_private_forbidden_terms.py
```

## How to Interpret Failures

Each gate prints `PASS`, `FAIL`, or `SKIPPED`. On failure:

1. Read the violation message — it includes file, line, and term.
2. Determine if the code change is legitimate for the current stage.
3. If yes: update the policy via PR (requires ADR if scope change).
4. If no: remove the offending code.

## Strict private forbidden terms gate

Some terms must be blocked without recording them in the repository.

**Configuration:**

- The CI uses the GitHub secret `PRIVATE_FORBIDDEN_TERMS_REGEX`.
- You can verify its presence via: `gh secret list`.
- Locally, you can use `.quality_gates_forbidden_terms.local` (gitignored).

**Security Measures:**

- **No repo storage**: The real regex is never stored in files tracked by git.
- **Redacted logs**: The failure output is redacted so the matched term, the regex, and the line content are not printed to logs.
- **Testing**: Test the gate behavior locally with a fake term (e.g., `export PRIVATE_FORBIDDEN_TERMS_REGEX="BLOCKME_TEST_ONLY"`).
- **Rotation**: Rotate the secret using GitHub repo settings -> Secrets.
- **Disabling**: The gate can only be disabled by explicitly removing the `--strict-private-terms` flag in the CI workflow via PR, never by a silent hotfix.

## How to Update Gates for Future Versions

1. Propose an ADR for the new scope (e.g., ADR-007 for v0.4).
2. Get ADR accepted via PR.
3. Update `tools/quality_gates/policy.json`:
   - Change `current_stage` to the new version.
   - Add a new stage entry with updated rules.
4. Update tests in `tests/test_quality_gates.py`.
5. Submit PR. CI must pass with new policy.

## Limitations

- Gates check text patterns, not AST — false positives are possible
  in comments or strings (mitigated by EXCLUDED_FILES).
- Solver integrity uses git diff — requires main branch to exist.
- Private terms gate is opt-in — not enforced unless configured.
- Policy is per-repo, not per-branch.
