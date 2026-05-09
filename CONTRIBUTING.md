# Contributing

Thank you for your interest in contributing to this project.

## Ground Rules

1. **All changes go through Pull Requests** — direct pushes to `main` are
   blocked by branch protection.
2. **CI must pass** — the `quality (3.11)` and `quality (3.12)` checks are
   required before merge.
3. **AI-RSE Quality Gates must pass** — scope guardrails, solver integrity,
   and private terms checks run in CI.
4. **No secrets in code** — never commit tokens, passwords, API keys, or the
   value of `PRIVATE_FORBIDDEN_TERMS_REGEX`.
5. **No scope escalation without ADR** — do not propose v0.4 physics (Poisson,
   ρ_eff, Schrödinger) without a formal Architecture Decision Record.

## Development Workflow

```bash
# 1. Create a feature branch
git checkout main
git pull origin main
git checkout -b feature/your-change

# 2. Make changes, write tests first (TDD)

# 3. Validate locally
pytest -v --tb=short
pytest --cov=mvp_quantum_materials --cov-fail-under=70
ruff check .
ruff format --check .
pyright .
PYTHONPATH=. python tools/quality_gates/run_all_quality_gates.py --require-artifacts

# 4. Commit with semantic messages
git commit -m "feat: description of change"

# 5. Push and open PR
git push -u origin feature/your-change
gh pr create --base main
```

## Commit Message Convention

Use semantic prefixes:

| Prefix | Usage |
|--------|-------|
| `feat:` | New feature or module |
| `fix:` | Bug fix |
| `test:` | New or modified tests |
| `docs:` | Documentation changes |
| `ci:` | CI/CD configuration |
| `style:` | Formatting (no logic change) |
| `chore:` | Maintenance tasks |

## Scientific Integrity

- **C** and **C_def** are dimensionless proxies — do not claim physical
  calibration.
- All parameters are toy/demonstrative.
- Separate fact, hypothesis, inference, and limitation in documentation.
- Do not make causal claims about quantum coherence or device performance.
