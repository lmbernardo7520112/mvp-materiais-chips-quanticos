# ADR-013 — C3 Solver Coupling Strategy

## Status

Accepted

## Acceptance Note

Accepted in v0.8.1.

This acceptance authorizes only future RED planning for C3 conservative grid projection.

It does not authorize:

* C3 implementation;
* Poisson runtime;
* solver coupling;
* physical phi interpretation;
* quantum confinement;
* AI-for-Science runtime;
* calibration claims;
* device prediction.

Future implementation requires a separate RED phase and later GREEN phase.

## Date

2026-06-12

## Context

C1 produz sigma_eff a partir de D_it(E).
C2 mapeia sigma_eff para fonte de interface e regularização conservativa.
v0.7.4 demonstrou sanity checks do C2 isolado.
v0.7.6 abriu AI-for-Science como trilha paralela, mas o caminho clássico segue canônico.
O próximo problema clássico é decidir como C2 poderá alimentar futuramente um solver eletrostático.
Esta ADR não autoriza implementação.

## Core Question

How should C2 charge sources be projected toward a future electrostatic solver without enabling premature solver coupling, physical phi interpretation, or calibration claims?

## Current Chain

D_it(E)
→ N_it
→ sigma_eff
→ C2 InterfaceSheetSource / ConservativeVolumeRegularization

## Future C3 Boundary

C3 deve ser uma camada intermediária entre C2 e Poisson runtime.

C3 não deve resolver Poisson inicialmente.

## Options

### C3-A — Conservative Grid Projection

**Status:** Recommended as primary future RED path.

**Descrição:**

* projetar fonte C2 em uma grade discreta;
* preservar carga total;
* preservar sinal;
* preservar metadados;
* exigir domínio explícito;
* exigir cell area/volume explícito;
* exigir boundary metadata;
* manter physical_interpretation_allowed = false;
* manter solver_coupling_enabled = false.

Não resolve Poisson.

### C3-B — Interface / Jump-Condition Solver Extension

**Status:** Future high-fidelity path.

**Descrição:**

* representar fonte de interface como condição de salto no solver;
* potencialmente mais físico;
* exige alteração real do solver;
* não deve ser primeira implementação;
* requer ADR/sub-ADR própria antes de qualquer código.

### C3-C — One-Way Poisson Coupling Demonstrator

**Status:** Conditional future path.

**Descrição:**

* usar fonte projetada para alimentar uma execução Poisson;
* sem self-consistency;
* sem physical phi claim;
* sem calibração;
* permitido apenas após C3-A implementado e validado.

### C3-D — Self-Consistent Coupling

**Status:** Blocked.

**Motivo:**

* exige arquitetura, física e validação adicionais;
* risco alto de claims indevidos.

### C3-E — Device-Predictive Electrostatics

**Status:** Blocked.

**Motivo:**

* exige geometria real, parâmetros calibrados e validação experimental.

### C3-F — AI-for-Science Solver Replacement

**Status:** Blocked.

**Motivo:**

* pertence à trilha paralela ADR-014;
* não pode substituir o caminho clássico;
* requer ADR futura, dependency decision, benchmarks analíticos e isolamento.

## Decision Direction

* C3-A como caminho primário futuro.
* C3-B como caminho de alta fidelidade futuro.
* C3-C como condicional posterior.
* C3-D/E/F bloqueados.
* Nenhuma implementação nesta release.

## Not Authorized

* no code;
* no tests;
* no scripts;
* no solver coupling;
* no Poisson runtime;
* no physical phi;
* no quantum confinement;
* no self-consistency;
* no calibration;
* no device prediction;
* no AI-for-Science runtime.

## Future Sequence

* v0.8.0: ADR-013 Proposed.
* v0.8.1: ADR-013 Acceptance Review.
* v0.8.2: C3 RED only if ADR-013 Accepted.
* v0.8.3: C3 GREEN conservative projection only.
* v0.8.4: C3 projection demo/sanity checks.
* later: one-way Poisson coupling ADR.
