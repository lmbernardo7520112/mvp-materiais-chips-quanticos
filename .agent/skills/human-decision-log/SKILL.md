---
name: human-decision-log
description: >
  Capture critical human decisions, rationale, rejected alternatives,
  and responsibility boundaries in AI-assisted scientific software
  development.
---

# Human Decision Log

Use this skill when a human makes or challenges a scientific,
methodological, dependency, release, or scope decision.

## Purpose

Preserve human responsibility in AI-assisted development.

## When to Record

Record when the human:

- rejects AI suggestion;
- accepts ADR;
- blocks overclaim;
- rejects dependency;
- changes roadmap;
- questions physical validity;
- approves merge/tag;
- requests council;
- redefines scope;
- insists on rigor over speed;
- authorizes a new implementation phase.

## Required Fields

- decision id;
- date;
- release;
- human decision;
- rationale;
- alternatives rejected;
- AI suggestion, if relevant;
- files affected;
- evidence;
- future consequence;
- whether decision is reversible.

## Suggested File

docs/governance/human_decision_log.md

## Rules

- Do not frame AI as final authority.
- Do not hide human override.
- Do not convert human judgment into fake consensus.
- Keep concise but traceable.
