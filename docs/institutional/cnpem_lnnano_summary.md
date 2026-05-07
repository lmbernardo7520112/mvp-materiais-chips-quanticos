# Resumo Institucional — Plataforma Computacional Process-to-Device

> **Para:** Grupos de pesquisa em materiais semicondutores e dispositivos quânticos  
> **Instituições de interesse:** CNPEM, LNNano, INCT-DQ, IFGW-Unicamp  
> **Data:** 2026-05-07  
> **Contato:** Leonardo Maximino Bernardo

---

## 1. Título do Projeto

**Modelagem computacional de heterogeneidades em materiais semicondutores:
uma infraestrutura process-to-device para futura aplicação em
dispositivos quânticos de estado sólido**

---

## 2. Proponente

Engenheiro com formação em simulação numérica de solidificação,
transporte de calor/massa e métodos numéricos, em transição para
modelagem computacional de materiais semicondutores aplicáveis a
dispositivos quânticos.

---

## 3. Contexto Técnico

Dispositivos quânticos de estado sólido — como quantum dots em silício —
são extremamente sensíveis a heterogeneidades materiais: defeitos
pontuais, cargas de interface, variações de composição e gradientes
térmicos residuais do processamento.

A capacidade de **modelar computacionalmente** como o processo térmico
gera e distribui essas heterogeneidades, e como elas perturbam
propriedades elétricas e de confinamento, é fundamental para o avanço
da tecnologia de chips quânticos baseados em semicondutores.

---

## 4. O que o MVP já entrega

O projeto é uma plataforma computacional Python/NumPy, open-source
(repositório privado), com governança rigorosa:

- **56 testes automatizados** com 92% de cobertura
- **CI/CD** contínuo em Python 3.11 e 3.12
- **Releases versionadas** com tags, PRs auditados e ADRs
- **Reprodutibilidade** via tutorial e notebook demonstrativo
- **Geração automatizada** de figuras e tabelas

---

## 5. O que a v0.2.0 demonstra

A versão 0.2.0 consolidou a robustez numérica bidimensional:

| Capacidade | Descrição |
|-----------|-----------|
| Domínio 2D estruturado | Grade retangular uniforme com validação |
| Solver térmico 2D | Euler explícito, Dirichlet BCs, guard de estabilidade CFL |
| Convergência formal | Solução analítica manufaturada com observed_order ≥ 1.5 |
| Cobertura bloqueante | Gate CI a 70%, atingido 92% |
| Regressão | 21 testes v0.1 preservados intactos |

Artefatos gerados: 6 figuras PNG + 2 tabelas CSV, incluindo campo
térmico 2D e análise de convergência log-log.

---

## 6. O que ainda NÃO demonstra

O projeto é transparente sobre suas limitações:

- ❌ Não modela defeitos reais (vacâncias, intersticiais)
- ❌ Não resolve eletrostática (Poisson)
- ❌ Não resolve confinamento (Schrödinger)
- ❌ Não prediz coerência de qubits
- ❌ Não utiliza TCAD comercial
- ❌ Não simula processos industriais de fabricação de wafer
- ❌ Parâmetros são demonstrativos, não calibrados

---

## 7. Relação com Materiais Semicondutores e Dispositivos Quânticos

O projeto segue um roadmap deliberado em 5 ondas:

```
v0.1 ✅  Demonstrador térmico/difusivo 1D
v0.2 ✅  Robustez numérica 2D + convergência
v0.3     Variável tipo defeito (C_def) com reaction-diffusion
v0.4     Eletrostática simplificada (Poisson 2D)
v0.5     Proxy de confinamento (Schrödinger simplificado)
v1.0     Demonstrador process-to-device completo
```

A rota conecta:

```
Processo térmico → Heterogeneidade material → Carga efetiva
→ Perturbação eletrostática → Proxy de confinamento
```

Cada etapa é validada numericamente antes de avançar.

---

## 8. Por que isso pode interessar

Para grupos que trabalham com:

- **Defeitos em silício:** a plataforma poderá modelar distribuições
  espaciais de heterogeneidades tipo defeito em 2D, com termos de
  geração e recombinação dependentes de temperatura.

- **Interfaces Si/SiO₂:** a infraestrutura 2D permite futura
  representação de regiões com propriedades distintas e cargas
  de interface.

- **Quantum dots em silício:** o roadmap inclui resolução de
  Poisson e Schrödinger simplificados para extrair proxies de
  confinamento perturbados por defeitos.

- **Variabilidade de processo:** a plataforma já possui
  sensibilidade paramétrica e poderá avaliar como variações
  de processo afetam heterogeneidades materiais.

---

## 9. O que gostaríamos

Este projeto busca **avaliação técnica e orientação**:

1. **Avaliação da rota process-to-device** por especialistas em
   materiais semicondutores e dispositivos quânticos.

2. **Indicação de pesquisadores** nas áreas de defeitos em silício,
   interfaces, eletrostática de dispositivos ou confinamento quântico
   que possam orientar as fases v0.3–v0.5.

3. **Possibilidade de colaboração** ou residência/estágio em
   laboratório para validação experimental futura dos modelos.

4. **Curadoria bibliográfica** para parametrização dos termos de
   geração e recombinação de defeitos na fase v0.3.

---

## 10. Acesso

O repositório é privado. Acesso pode ser concedido para avaliação:

- **GitHub:** https://github.com/lmbernardo7520112/mvp-materiais-chips-quanticos
- **Release atual:** v0.2.0 (tag validada, CI verde)
- **Reprodução:** tutorial disponível em `docs/tutorials/reproduce_v0.2.0.md`
- **Notebook:** demonstração executável em `notebooks/v0.2_demo.py`

---

## 11. Nota de Prudência

Este projeto **não é** um simulador de chip quântico. É uma
infraestrutura computacional demonstrativa, em construção, com
objetivo de longo prazo em modelagem process-to-device. Nenhum
resultado deve ser interpretado como predição física quantitativa
sem calibração experimental adequada.
