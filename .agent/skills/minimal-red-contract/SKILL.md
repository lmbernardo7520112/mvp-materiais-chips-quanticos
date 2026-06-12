---
name: minimal-red-contract
description: >
  Design minimal sufficient RED tests that encode physical, dimensional,
  computational, and governance contracts without bloating the test suite.
---

# Minimal RED Contract

Use this skill before writing RED tests.

## Purpose

Prevent oversized or weak RED phases.

## RED Test Principle

A RED suite must be sufficient, not maximal.

It must fail for the right reason.

## Required Contract Table

Before creating tests, define:

| Contract Type | Required Question |
|---|---|
| Physical contract | What physical claim is allowed? |
| Dimensional contract | What units must be preserved? |
| Computational contract | What API behavior is required? |
| Governance contract | What must remain blocked? |
| Non-goal contract | What must not be implemented? |

## Good RED Failures

Allowed:

- ModuleNotFoundError;
- ImportError;
- AssertionError from missing contract;
- explicit validation failure.

Not allowed:

- SyntaxError;
- fixture setup errors;
- hidden dependency failures;
- tests passing without checking future contract;
- tests that require unauthorized implementation.

## Test Count Guidance

Prefer 8–15 focused tests for a new module.

Use more only if:

- multiple APIs;
- physical/dimensional boundary;
- security/safety boundary;
- metadata/evidence boundary.

## RED Audit

Every RED report must include:

- number of tests;
- failed/passed/skipped counts;
- reason for each non-failing test;
- confirmation no production code exists;
- confirmation target module absent;
- confirmation no scope leak.
