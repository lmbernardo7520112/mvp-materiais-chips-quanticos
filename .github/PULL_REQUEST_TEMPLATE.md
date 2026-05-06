# Pull Request Checklist

## Quality Gates

- [ ] SDD (implementation_plan.md) atualizado
- [ ] Testes criados antes/durante implementação (TDD)
- [ ] `pytest` verde
- [ ] `ruff check .` verde
- [ ] `ruff format --check .` verde
- [ ] Scripts executam com `--output-dir`
- [ ] Figuras reproduzíveis (≥3)
- [ ] Limitações declaradas (C = proxy adimensional)
- [ ] Nenhuma extrapolação científica indevida
- [ ] CI verde (GitHub Actions)
- [ ] `walkthrough.md` atualizado com evidências
- [ ] Working tree limpo (`git status`)

## Scientific Review

- [ ] Fato, hipótese, inferência e limitação separados
- [ ] Não afirma simulação industrial
- [ ] Não afirma predição de coerência quântica
- [ ] Não afirma equivalência solidificação ↔ semicondutores
- [ ] Transferência metodológica declarada

## Documentation

- [ ] `docs/parameters.md` atualizado
- [ ] `docs/hipoteses_e_limitacoes.md` atualizado
- [ ] ADRs criados para decisões técnicas relevantes
- [ ] `docs/governance/technical_debt.md` atualizado
