---
name: release-acceleration-lanes
description: >
  Classify work into fast-lane or slow-lane release paths while preserving
  AI-RSE governance, scientific scope, and release discipline.
---

# Release Acceleration Lanes

Use this skill when a task asks to speed up development, reduce documentation
overhead, choose a release path, or decide whether a council/risk matrix/ADR
is required.

## Purpose

Accelerate without weakening governance.

## Core Rule

Acceleration is allowed only by reducing redundant process overhead, never by
skipping scientific decision gates.

## Lane Types

### Fast Lane A — Documentation-only Simple

Allowed when:

- zero src changes;
- zero tests changes;
- zero scripts changes;
- no policy change;
- no pyproject change;
- no skill change;
- no new physics;
- no new dependency;
- no solver coupling;
- no physical interpretation claim.

Required artifacts:

- release notes;
- walkthrough update;
- acceptance gates.

Council optional.

Risk matrix optional.

### Fast Lane B — Demo / Sanity Checks

Allowed when:

- script isolated;
- focal tests exist;
- no solver coupling;
- no physical phi;
- no calibration claims;
- no core physics mutation;
- no new dependency.

Required artifacts:

- TDD plan;
- demo tests;
- demo script;
- release notes;
- acceptance gates;
- walkthrough update.

### Fast Lane C — Refactor Safe

Allowed when:

- no output change;
- no physics change;
- no dependency change;
- tests remain green;
- scope diff is narrow.

Required artifacts:

- refactor note;
- before/after validation;
- release notes.

### Slow Lane Mandatory

Required when any of the following appears:

- new physics;
- solver coupling;
- physical phi;
- calibration language;
- new dependency;
- pyproject change;
- policy.json change;
- units/dimensional change;
- quantum confinement;
- experimental data;
- device prediction;
- self-consistency;
- boundary condition changes;
- source projection to solver.

Required artifacts:

- ADR or ADR acceptance;
- decision brief;
- council;
- risk matrix;
- acceptance gates;
- future RED plan;
- release notes.

## Scope Budget

Every release must declare:

- allowed src files;
- allowed test files;
- allowed scripts;
- allowed docs;
- policy change: yes/no;
- dependency change: yes/no;
- skill change: yes/no.

If scope exceeds the budget, split the release.

## Stop Conditions

Stop and report if:

- implementation starts before ADR acceptance;
- RED and GREEN are mixed without explicit plan;
- solver coupling appears in fast lane;
- physical interpretation appears before authorization;
- tag is attempted before CI main is green.
