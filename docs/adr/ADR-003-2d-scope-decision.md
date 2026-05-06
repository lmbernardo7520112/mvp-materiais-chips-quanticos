# ADR-003: 2D Scope Decision

**Status:** Deferred to v0.2  
**Date:** 2026-05-06  
**Deciders:** L. Bernardo (principal investigator)

## Context

A especificação original incluía um caso 2D simplificado.
O plano v0.1-r2 reclassificou 2D como **stretch goal**,
condicionado a todos os 19 gates locais 1D estarem verdes.

## Decision

O caso 2D é **deferido para v0.2**.

## Rationale

1. **Qualidade sobre escopo:** o foco v0.1 é entregar 1D com qualidade
   comprovada — 19+ testes, ruff, figuras, governança completa.
2. **Stretch goal condicionado:** 2D só poderia ser implementado se
   todos os gates 1D estivessem verdes. A prioridade é garantir
   a base 1D defensável.
3. **Complexidade incremental:** 2D introduz condições de contorno
   adicionais, verificação de estabilidade em duas dimensões,
   e validação mais exigente.
4. **Risco controlado:** deferir 2D elimina o risco de degradar
   a qualidade do 1D por pressão de escopo.

## Consequences

- (+) Entrega v0.1 com qualidade comprovada.
- (+) Menor risco de bugs não cobertos.
- (-) Escopo visual menos impressionante.
- 2D será prioridade na v0.2 com base sólida.

## v0.2 Roadmap

- Domain2D com grade retangular uniforme.
- Solver térmico 2D (Euler explícito ou ADI).
- Solver difusivo 2D.
- Testes de convergência 2D.
- Visualização com contour plots.

## Status

Deferido. Não implementar em v0.1 sob nenhuma circunstância.
