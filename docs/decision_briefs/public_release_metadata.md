# Public Release Metadata — License and Citation Decision

> **Date:** 2026-05-09
> **Status:** ✅ ACCEPTED

## Context

The repository `mvp-materiais-chips-quanticos` was made public on 2026-05-09
to enable GitHub branch protection on the Free plan. This required formal
decisions on licensing and citation metadata.

## License Decision

| Item | Value |
|------|-------|
| **License** | MIT |
| **Decision date** | 2026-05-09 |
| **Decision by** | Repository owner (explicit confirmation) |
| **File** | `LICENSE` |
| **Scope** | All code and documentation in this repository, unless otherwise stated |

### Justification

- MIT is the most common license for academic computational science projects.
- Compatible with NumPy (BSD), Matplotlib (PSF/BSD), and SciPy (BSD) licenses.
- Permissive — allows reuse, modification, and distribution with minimal
  restrictions.
- Appropriate for a demonstrative MVP with toy parameters and no commercial IP.

### Options Considered

| License | Decision |
|---------|----------|
| **MIT** | ✅ **Selected** — simple, permissive, widely adopted |
| Apache 2.0 | Rejected — patent grant unnecessary for academic MVP |
| GPL-3.0 | Rejected — copyleft too restrictive for academic collaboration |
| CC BY 4.0 | Rejected — not recommended for software |

## Citation

- `CITATION.cff` created with preliminary metadata.
- License field: `MIT`.
- Version: `0.3.4`.
- Author: Leonardo Maximino Bernardo.

## Action Completed

- [x] License chosen: MIT.
- [x] `LICENSE` file committed.
- [x] `CITATION.cff` updated with license field.
- [x] README updated with MIT badge and license section.
