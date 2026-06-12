---
name: evidence-metrics-refresh
description: >
  Refresh repository metrics from commands and prevent stale, invented,
  or untraceable evidence in reports and dossiers.
---

# Evidence Metrics Refresh

Use this skill before writing reports, dossiers, release notes, scorecards,
or claims about project state.

## Core Rule

Metrics are evidence snapshots, not permanent constants.

## Required Command Evidence

For metrics, run or cite commands such as:

- pytest;
- coverage;
- ruff;
- pyright;
- quality gates;
- generate_all_results;
- git tag;
- git log;
- gh pr list;
- gh pr checks;
- find docs;
- wc -l;
- grep.

## Required Metric Metadata

Every metric table must include:

- command source;
- repository state or commit;
- date if available;
- whether value is local or CI;
- whether value is repository-reported;
- instruction to re-run commands to refresh.

## Prohibited

- invented PR counts;
- invented tag counts;
- invented test counts;
- stale coverage;
- saying "current" without command evidence;
- using local artifact report as repository evidence without checking
  versioned files.

## Report Language

Use:

"repository-reported at time of audit"

Avoid:

"permanent project value"

## Stop Conditions

Stop if:

- a metric cannot be traced;
- local artifact contradicts repository file;
- PR status is asserted without gh command;
- tag is asserted without git command.
