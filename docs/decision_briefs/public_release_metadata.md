# Public Release Metadata — License and Citation Decision

> **Date:** 2026-05-09
> **Status:** PENDING USER DECISION

## Context

The repository `mvp-materiais-chips-quanticos` was made public on 2026-05-09
to enable GitHub branch protection on the Free plan. This requires formal
decisions on licensing and citation metadata.

## License

### Current State

No `LICENSE` file exists in the repository. The previous `README.md` mentioned
MIT informally in a badge, but no formal license file was committed.

### Options

| License | Pros | Cons |
|---------|------|------|
| **MIT** | Simple, permissive, widely used in academic code | No patent protection |
| **Apache 2.0** | Patent grant, permissive, compatible with MIT | Slightly more complex |
| **GPL-3.0** | Strong copyleft, ensures derivatives remain open | May discourage commercial collaboration |
| **CC BY 4.0** | Good for documentation/data | Not recommended for software |

### Recommendation

**MIT** is the most common choice for academic computational science MVPs.
It is compatible with NumPy, Matplotlib, and SciPy licenses.

> [!IMPORTANT]
> The repository owner must explicitly choose a license before it can be
> committed. Do not auto-select without user authorization.

## Citation

A `CITATION.cff` file has been created with preliminary metadata.
The owner should review and confirm:

- Author name and ORCID (if available).
- Preferred citation title.
- Whether to include institutional affiliation.

## Action Required

1. **Choose license** — confirm MIT or select alternative.
2. **Review CITATION.cff** — confirm author metadata.
3. Once confirmed, commit `LICENSE` file and finalize `CITATION.cff`.
