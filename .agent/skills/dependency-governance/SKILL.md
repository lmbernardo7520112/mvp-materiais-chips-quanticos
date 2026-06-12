---
name: dependency-governance
description: >
  Govern new dependencies using minimal-dependency principles, explicit
  decision briefs, and CI/reproducibility impact checks.
---

# Dependency Governance

Use this skill whenever a task suggests installing, importing, or adding a new
package.

## Core Rule

Do not add a dependency for convenience when the Python standard library or
existing dependencies are sufficient.

## Dependency Decision Required When

- pyproject.toml changes;
- lockfile changes;
- CI install time changes;
- tests import a package not already declared;
- script requires optional external library;
- notebook/data workflow introduces new package.

## Decision Brief Required Fields

- package name;
- purpose;
- why stdlib is insufficient;
- alternatives considered;
- CI impact;
- reproducibility impact;
- maintenance burden;
- security/licensing concern;
- whether dependency is runtime, dev, docs, or optional;
- rollback strategy.

## Default Preference

Prefer:

- stdlib;
- existing dependencies;
- simple deterministic formats;
- explicit adapters.

Avoid:

- pandas for tiny deterministic CSV validation;
- heavy plotting/data libraries without need;
- hidden transitive dependency expansion.

## Reconsider Dependencies When

- complex tabular analysis;
- joins;
- groupby;
- statistical processing;
- large datasets;
- DataFrame public API;
- notebook/data-science workflow becomes formal scope.

## Stop Conditions

Stop if:

- dependency is added to fix a test without decision brief;
- import appears before pyproject update;
- dependency solves only one trivial operation;
- CI fails due to missing undeclared dependency.
