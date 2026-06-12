---
name: ai-failure-mode-review
description: >
  Review common generative-AI failure modes before commits, PRs, merges,
  and scientific implementation steps.
---

# AI Failure Mode Review

Use this skill before committing or opening a PR, especially after
AI-generated code or documentation.

## Required Checklist

Ask:

1. Did the AI invent data, sources, metrics, or claims?
2. Did the AI implement before ADR acceptance?
3. Did the AI mix RED and GREEN improperly?
4. Did the AI alter files outside the scope budget?
5. Did the AI remove forbidden terms instead of governing them?
6. Did the AI add a dependency by convenience?
7. Did the AI treat a demo as validation?
8. Did the AI create physical interpretation from bookkeeping?
9. Did the AI create calibration language?
10. Did the AI confuse local artifact with versioned repository evidence?
11. Did the AI recommend an incorrect tag or closure version?
12. Did the AI skip CI-main-before-tag discipline?
13. Did the AI underreport failures?
14. Did the AI produce optimistic summary not backed by commands?
15. Did the AI ignore human decisions?

## Required Output

Before PR or merge, report:

- failure modes checked;
- any issue found;
- mitigation;
- whether human decision is required.

## Stop Conditions

Stop if:

- overclaim exists;
- dependency added without decision;
- solver coupling appears without ADR;
- tag would be created before CI main;
- human approval required but absent.
