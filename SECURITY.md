# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this repository, please report it
responsibly:

1. **Do not** open a public issue.
2. **Do not** include secret values, tokens, or regex patterns in any report.
3. Contact the repository owner directly via GitHub private vulnerability
   reporting or email.

## Security Measures

This repository uses the following security controls:

### Branch Protection

- Pull requests are required before merging to `main`.
- Required CI checks: `quality (3.11)`, `quality (3.12)`.
- Force push and branch deletion are blocked.

### Private Forbidden Terms Gate

- The CI enforces a **strict private forbidden terms gate** using the
  `PRIVATE_FORBIDDEN_TERMS_REGEX` GitHub secret.
- The gate blocks any code containing terms that match the secret pattern.
- Violation output is **redacted** — neither the matched term, the regex
  pattern, nor the full line content are exposed in CI logs.
- The secret value is **never** stored in the repository.

### Exposure Audit

- The repository has been audited for secrets, tokens, API keys, PEM keys,
  and personally identifiable information.
- Audit date: 2026-05-09.
- Result: **No secrets or tokens found.**

## What NOT to Commit

- API keys, tokens, or passwords.
- The value of `PRIVATE_FORBIDDEN_TERMS_REGEX`.
- Private SSH or PGP keys.
- Personally identifiable information (PII) beyond public author attribution.

## Supported Versions

| Version | Supported |
|---------|-----------|
| v0.3.x  | ✅ Current |
| v0.2.x  | ❌ Superseded |
| v0.1.x  | ❌ Superseded |
