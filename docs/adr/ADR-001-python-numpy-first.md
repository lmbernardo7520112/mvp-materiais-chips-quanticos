# ADR-001: Python/NumPy First

**Status:** Accepted  
**Date:** 2026-05-06  
**Deciders:** L. Bernardo (principal investigator)

## Context

O MVP precisa de uma plataforma para simulação numérica de transporte
de calor e difusão. Alternativas consideradas:

| Opção | Prós | Contras |
|-------|------|---------|
| Python/NumPy | Reprodutível, portátil, rápido de prototipar, CI fácil | Não escala para 3D complexo |
| OpenFOAM | Industrial, validado, 3D | Setup pesado, C++, CI difícil |
| FEniCSx | FEM robusto, Python | Dependência pesada, curva de aprendizado |
| MOOSE | Phase-field nativo | C++, infraestrutura pesada |
| PRISMS-PF | Phase-field otimizado | C++, menos portátil |

## Decision

Começar com Python/NumPy para o MVP v0.1.

## Rationale

1. **Reprodutibilidade:** pip install + pytest + CI verde em minutos.
2. **Velocidade de desenvolvimento:** protótipo funcional em dias, não semanas.
3. **Comunicação:** Python é acessível a colaboradores de diferentes áreas.
4. **Escopo de MVP:** 1D explícito não requer frameworks pesados.
5. **Migração futura:** formulação matemática é independente da implementação.

## Consequences

- (+) CI verde desde o dia 1.
- (+) Baixa barreira de entrada para revisores.
- (-) Performance limitada para problemas grandes.
- (-) Requer reimplementação para 3D/phase-field na v0.2+.

## Status

Aceita. Ferramentas pesadas serão consideradas na v0.2 conforme necessidade.
