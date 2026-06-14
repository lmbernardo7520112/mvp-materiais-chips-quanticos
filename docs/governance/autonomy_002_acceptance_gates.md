# Autonomy-002 Acceptance Gates

* **G1** — usage ledger example exists.
* **G2** — usage ledger schema exists.
* **G3** — `check_usage_ledger` exists.
* **G4** — `summarize_usage_ledger` exists.
* **G5** — `workflow_state` references usage ledger.
* **G6** — `workflow_state` schema requires usage ledger.
* **G7** — `release_rules` require ledger.
* **G8** — `budget_limits` require ledger.
* **G9** — paid API without approval fails.
* **G10** — SDK without approval fails.
* **G11** — goal mode without approval fails.
* **G12** — retries beyond budget fail.
* **G13** — CI watch beyond budget fails.
* **G14** — missing ledger fails for autonomous phase.
* **G15** — merge requires usage review.
* **G16** — tag requires usage review.
* **G17** — no scientific code changes.
* **G18** — no dependency changes.
* **G19** — no policy changes.
* **G20** — quality gates PASS.
* **G21** — pytest PASS.
* **G22** — ruff PASS.
* **G23** — pyright PASS.
* **G24** — generate_all_results PASS.
* **G25** — CI PASS.
