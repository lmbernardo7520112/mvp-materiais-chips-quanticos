# ADR-002: No Quantum Coherence Prediction

**Status:** Accepted  
**Date:** 2026-05-06  
**Deciders:** L. Bernardo (principal investigator)

## Context

O MVP modela transporte de calor e difusão de uma variável proxy C.
Existe a tentação de extrapolar resultados para predições sobre
coerência quântica em dispositivos de estado sólido.

## Decision

O MVP v0.1 **não** modela nem promete predição de coerência quântica.

## Rationale

1. **Física distinta:** coerência quântica depende de interações
   spin-órbita, acoplamento hiperfino, decoerência ambiental —
   nenhuma dessas está no modelo.
2. **C é proxy adimensional:** a variável C não representa
   concentração física de defeitos calibrada.
3. **Prudência científica:** qualquer inferência sobre dispositivos
   quânticos deve ser formulada de modo prudente e não causal.
4. **Requer validação experimental:** correlação entre heterogeneidades
   simuladas e coerência quântica requer dados experimentais inexistentes
   no escopo do MVP.

## Consequences

- (+) Credibilidade científica preservada.
- (+) Nenhuma promessa indefensável.
- (-) Escopo limitado — pode parecer menos "impactante".
- A transferência é **metodológica**, não preditiva.

## Status

Aceita permanentemente para v0.1.
