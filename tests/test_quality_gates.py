"""Tests for AI-RSE GateOps version-aware quality gates."""

from pathlib import Path

import pytest
from tools.quality_gates.check_adr_status import check_adr_status
from tools.quality_gates.check_artifacts import check_artifacts
from tools.quality_gates.check_docs_required import check_docs_required
from tools.quality_gates.check_private_forbidden_terms import (
    check_private_forbidden_terms,
)
from tools.quality_gates.check_scope_guardrails import check_scope_guardrails
from tools.quality_gates.policy_loader import (
    get_active_stage,
    get_stage_name,
    load_policy,
)

REPO_ROOT = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# Policy loader tests
# ---------------------------------------------------------------------------


class TestPolicyLoader:
    """Tests for policy_loader module."""

    def test_load_default_policy(self):
        """Policy loads without error."""
        policy = load_policy()
        assert isinstance(policy, dict)
        assert "current_stage" in policy
        assert "stages" in policy

    def test_current_stage_is_v03(self):
        """Current stage is v0.3."""
        policy = load_policy()
        assert get_stage_name(policy) == "v0.3"

    def test_active_stage_has_required_keys(self):
        """Active stage has essential keys."""
        policy = load_policy()
        stage = get_active_stage(policy)
        assert "forbidden_in_code" in stage
        assert "required_adrs" in stage
        assert "required_docs" in stage
        assert "required_artifacts" in stage

    def test_v04_template_is_not_active(self):
        """v0.4_future_template is present but not active."""
        policy = load_policy()
        assert "v0.4_future_template" in policy["stages"]
        assert policy["current_stage"] != "v0.4_future_template"
        template = policy["stages"]["v0.4_future_template"]
        assert template["status"] == "template_only_not_active"

    def test_malformed_policy_raises(self, tmp_path: Path):
        """Malformed policy raises ValueError."""
        bad = tmp_path / "bad.json"
        bad.write_text('["just a list"]\n')
        with pytest.raises(ValueError):
            load_policy(bad)

    def test_missing_stage_raises(self, tmp_path: Path):
        """Missing current_stage key raises ValueError."""
        bad = tmp_path / "no_stage.json"
        bad.write_text('{"stages": {"v0.1": {"forbidden_in_code": []}}}')
        with pytest.raises(ValueError, match="current_stage"):
            load_policy(bad)


# ---------------------------------------------------------------------------
# ADR status gate tests
# ---------------------------------------------------------------------------


class TestADRStatusGate:
    """Tests for check_adr_status."""

    def test_adr_accepted_passes(self):
        """Real repo ADR-006 Accepted passes."""
        policy = load_policy()
        failures = check_adr_status(REPO_ROOT, policy)
        assert failures == []

    def test_adr_proposed_fails(self, tmp_path: Path):
        """ADR with wrong status fails."""
        adr_dir = tmp_path / "docs" / "adr"
        adr_dir.mkdir(parents=True)
        adr = adr_dir / "ADR-006-defect-like-reaction-diffusion-scope.md"
        adr.write_text("## Status\n\n**Proposed**\n\n## Date\n")

        policy = {
            "current_stage": "v0.3",
            "stages": {
                "v0.3": {
                    "required_adrs": {"ADR-006-defect-like-reaction-diffusion-scope.md": "Accepted"}
                }
            },
        }
        failures = check_adr_status(tmp_path, policy)
        assert len(failures) == 1
        assert "Proposed" in failures[0] or "Accepted" in failures[0]

    def test_adr_missing_fails(self, tmp_path: Path):
        """Missing ADR fails."""
        (tmp_path / "docs" / "adr").mkdir(parents=True)
        policy = {
            "current_stage": "v0.3",
            "stages": {"v0.3": {"required_adrs": {"ADR-999-nonexistent.md": "Accepted"}}},
        }
        failures = check_adr_status(tmp_path, policy)
        assert len(failures) == 1
        assert "missing" in failures[0].lower()


# ---------------------------------------------------------------------------
# Scope guardrails gate tests
# ---------------------------------------------------------------------------


class TestScopeGuardrails:
    """Tests for check_scope_guardrails."""

    def test_v03_blocks_forbidden_in_src(self, tmp_path: Path):
        """v0.3 policy blocks forbidden terms in src/."""
        src = tmp_path / "src"
        src.mkdir()
        (src / "bad.py").write_text("result = solve_Poisson(field)\n")

        policy = {
            "current_stage": "v0.3",
            "stages": {"v0.3": {"forbidden_in_code": ["Poisson"]}},
        }
        violations = check_scope_guardrails(tmp_path, policy)
        assert len(violations) >= 1
        assert "Poisson" in violations[0]

    def test_v03_blocks_rho_eff_in_scripts(self, tmp_path: Path):
        """v0.3 policy blocks rho_eff in scripts/."""
        scripts = tmp_path / "scripts"
        scripts.mkdir()
        (scripts / "run.py").write_text("rho_eff = compute()\n")

        policy = {
            "current_stage": "v0.3",
            "stages": {"v0.3": {"forbidden_in_code": ["rho_eff"]}},
        }
        violations = check_scope_guardrails(tmp_path, policy)
        assert len(violations) >= 1

    def test_v03_allows_in_docs(self, tmp_path: Path):
        """v0.3 does not scan docs/."""
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "plan.py").write_text("# Poisson is deferred\n")

        policy = {
            "current_stage": "v0.3",
            "stages": {"v0.3": {"forbidden_in_code": ["Poisson"]}},
        }
        violations = check_scope_guardrails(tmp_path, policy)
        assert violations == []

    def test_real_repo_passes(self):
        """Real repo passes scope guardrails for v0.3."""
        policy = load_policy()
        violations = check_scope_guardrails(REPO_ROOT, policy)
        assert violations == [], f"Unexpected violations: {violations}"


# ---------------------------------------------------------------------------
# Artifacts gate tests
# ---------------------------------------------------------------------------


class TestArtifactsGate:
    """Tests for check_artifacts."""

    def test_complete_artifacts_pass(self, tmp_path: Path):
        """All required artifacts present passes."""
        figs = tmp_path / "figures"
        tables = tmp_path / "tables"
        figs.mkdir()
        tables.mkdir()

        for i in range(9):
            (figs / f"fig_{i}.png").write_text("")
        (figs / "defect_2d_final.png").write_text("")

        for name in [
            "defect_metrics.csv",
            "defect_final_snapshot.csv",
            "sensitivity_results.csv",
            "convergence_results.csv",
        ]:
            (tables / name).write_text("")

        policy = {
            "current_stage": "v0.3",
            "stages": {
                "v0.3": {
                    "required_artifacts": {
                        "figures_min": 9,
                        "csv_min": 4,
                        "figures": ["defect_2d_final.png"],
                        "tables": [
                            "defect_metrics.csv",
                            "defect_final_snapshot.csv",
                            "sensitivity_results.csv",
                            "convergence_results.csv",
                        ],
                    }
                }
            },
        }
        failures = check_artifacts(figs, tables, policy)
        assert failures == []

    def test_missing_figure_fails(self, tmp_path: Path):
        """Missing required figure fails."""
        figs = tmp_path / "figures"
        tables = tmp_path / "tables"
        figs.mkdir()
        tables.mkdir()

        policy = {
            "current_stage": "v0.3",
            "stages": {
                "v0.3": {
                    "required_artifacts": {
                        "figures_min": 0,
                        "csv_min": 0,
                        "figures": ["defect_2d_final.png"],
                        "tables": [],
                    }
                }
            },
        }
        failures = check_artifacts(figs, tables, policy)
        assert len(failures) == 1
        assert "defect_2d_final.png" in failures[0]

    def test_csv_count_below_minimum_fails(self, tmp_path: Path):
        """CSV count below minimum fails."""
        figs = tmp_path / "figures"
        tables = tmp_path / "tables"
        figs.mkdir()
        tables.mkdir()
        (tables / "one.csv").write_text("")

        policy = {
            "current_stage": "v0.3",
            "stages": {
                "v0.3": {
                    "required_artifacts": {
                        "figures_min": 0,
                        "csv_min": 4,
                        "figures": [],
                        "tables": [],
                    }
                }
            },
        }
        failures = check_artifacts(figs, tables, policy)
        assert len(failures) == 1
        assert "4" in failures[0]


# ---------------------------------------------------------------------------
# Docs required gate tests
# ---------------------------------------------------------------------------


class TestDocsRequired:
    """Tests for check_docs_required."""

    def test_real_repo_passes(self):
        """Real repo has all required docs."""
        policy = load_policy()
        failures = check_docs_required(REPO_ROOT, policy)
        assert failures == []

    def test_missing_doc_fails(self, tmp_path: Path):
        """Missing doc fails."""
        policy = {
            "current_stage": "v0.3",
            "stages": {"v0.3": {"required_docs": ["docs/nonexistent.md"]}},
        }
        failures = check_docs_required(tmp_path, policy)
        assert len(failures) == 1


# ---------------------------------------------------------------------------
# Private forbidden terms gate tests
# ---------------------------------------------------------------------------


class TestPrivateForbiddenTerms:
    """Tests for check_private_forbidden_terms."""

    def test_detects_violation_via_env(self, tmp_path: Path):
        """Detects forbidden term from env variable."""
        src = tmp_path / "src"
        src.mkdir()
        (src / "bad.py").write_text("BLOCKME_TEST_ONLY_value = 42\n")

        violations = check_private_forbidden_terms(tmp_path, ["BLOCKME_TEST_ONLY"])
        assert len(violations) >= 1

        # Ensure it is redacted
        violation = violations[0]
        assert "BLOCKME_TEST_ONLY" not in violation
        assert "value = 42" not in violation
        assert "PRIVATE_FORBIDDEN_TERMS violation at" in violation

    def test_clean_repo_passes(self, tmp_path: Path):
        """Clean repo passes."""
        src = tmp_path / "src"
        src.mkdir()
        (src / "good.py").write_text("value = 42\n")

        violations = check_private_forbidden_terms(tmp_path, ["BLOCKME_TEST_ONLY"])
        assert violations == []

    def test_local_file_works(self, tmp_path: Path):
        """Local gitignored file works as term source."""
        src = tmp_path / "src"
        src.mkdir()
        (src / "code.py").write_text("secret_term_123 = True\n")

        violations = check_private_forbidden_terms(tmp_path, ["secret_term_123"])
        assert len(violations) >= 1
        assert "secret_term_123" not in violations[0]
