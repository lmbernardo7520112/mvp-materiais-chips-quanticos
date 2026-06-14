# Autonomy-002 — Usage Ledger and Cost Accounting Governance

## Overview
Autonomy-001 introduced `BudgetOps` to define hard limits and prevent unauthorized spending or unbounded execution. Autonomy-002 introduces the **Usage Ledger**, which acts as the system of record for operational events and cost estimates.

## Core Principles
* **BudgetOps defines limits:** The maximum allowed cost, retries, and CI watch time are set in `budget_limits`.
* **Usage Ledger registers events:** Every action the agent takes (starting a phase, executing a command, running validation, watching CI) must be recorded in the JSONL ledger.
* **No automatic token metering:** The ledger does not measure real Antigravity tokens via the network. It registers estimates and operational facts.
* **Paid API is still blocked:** Use of external paid APIs remains blocked by default. If enabled in the future, the cost MUST be approved by a human and registered in the ledger.
* **Review is Mandatory:** Merge, tag, and ADR acceptance operations require human review of the ledger.
* **Ledger is a Prerequisite:** Without a valid, active ledger, no autonomous phases can be executed. "Sem ledger, sem autonomia."
