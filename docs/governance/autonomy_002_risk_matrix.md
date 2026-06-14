# Autonomy-002 Risk Matrix

| Risk ID | Severity | Failure Mode | Mitigation | Gate |
|:---:|:---:|:---|:---|:---|
| R1 | High | Ledger ausente durante execução autônoma. | State validator exige `usage_ledger.enabled = true`. | G5, G6, G14 |
| R2 | High | Custo estimado omitido. | Schema exige `estimated_cost_brl` em todos os eventos. | G2, G3 |
| R3 | Critical | Paid API usada sem registro de aprovação humana. | `check_usage_ledger` falha se `paid_api_used=true` sem `human_approval_granted`. | G9 |
| R4 | Critical | SDK usado sem registro de aprovação humana. | `check_usage_ledger` falha se `external_sdk_used=true` sem `human_approval_granted`. | G10 |
| R5 | Critical | `/goal` mode usado sem registro de aprovação. | `check_usage_ledger` falha se `goal_mode_used=true` sem `human_approval_granted`. | G11 |
| R6 | Medium | Retries não contabilizados e excedendo budget. | Validator soma retries e falha se > budget. | G12 |
| R7 | Medium | CI watch não contabilizado e excedendo budget. | Validator soma tempo e falha se > budget. | G13 |
| R8 | Low | Artefatos grandes não registrados. | Validator checa contagem de artefatos. | G3, G14 |
| R9 | High | Ledger manipulado após execução. | Auditoria humana no Pull Request obrigatória. | G15, G16 |
| R10 | High | Aprovação humana registrada sem evidência. | Humano revisa o histórico de aprovações no PR. | G15, G16 |
| R11 | Medium | Tokens reais confundidos com estimativa. | Documentação esclarece que é estimativa offline. | G2 |
| R12 | Medium | Usuário interpreta estimativa como cobrança exata. | Sumário e logs indicam ser custo estimado. | G4, G2 |
