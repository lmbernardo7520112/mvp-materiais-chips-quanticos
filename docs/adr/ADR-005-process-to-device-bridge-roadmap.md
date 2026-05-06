# ADR-005 — Roadmap Process-to-Device Bridge

## Status
Accepted

## Context
A versão v0.1 do projeto consolidou com sucesso um demonstrador numérico termo-difusivo em 1D, servindo como alicerce metodológico para o desenvolvimento regido por SDD (Specification Driven Development) e rigorosas travas de governança.

Neste cenário consolidado:
- A variável $C$ permanece como um proxy genérico e adimensional.
- O escopo geométrico 2D foi deferido (ADR-003) para manter foco inicial na validação base.
- Existe um consenso de direcionamento e interesse em aproximar gradualmente a capacidade do software de seu objetivo real: ligar ciência de materiais ao desempenho do dispositivo final.
- Entretanto, tentar migrar bruscamente de um modelo térmico 1D abstrato para pacotes TCAD avançados, esquemas Poisson-Schrödinger maduros, simulação realista industrial (wafer) ou QTCAD direto configuraria um pulo epistemológico severo, sem garantia de estabilidade de software e violando o rastreamento TDD do MVP.

## Decision
Fica estabelecida e aprovada a rota estratégica que balizará o médio prazo através de um roadmap em estágios sucessivos (o *process-to-device bridge*):

1. **v0.2 — Robustez numérica e convergência:** Extensão para 2D térmico simplificado com foco na amarração numérica ($\Delta x, \Delta t$).
2. **v0.3 — Defect-like reaction-diffusion:** Evolução do proxy genérico para uma variável orientada a defeitos térmicos ($C_{def}$), com termos fonte/sumidouro não-lineares, mas não-calibrada.
3. **v0.4 — Eletrostática base:** Introdução do solver Poisson 2D simplificado, convertendo as heterogeneidades de defeitos em densidade efetiva de carga ($\rho_{eff}$).
4. **v0.5 — Confinamento Quântico:** Introdução do solver Schrödinger 1D/2D para extração de proxies de confinamento.
5. **v1.0 — Demonstrador Process-to-Device Institucional:** Demonstração completa e contígua do pipeline acoplado.

## Consequences

**Positivas:**
- Garantia de evolução técnica gradual e rastreável.
- Drástica redução do risco de extrapolação matemática não física.
- Maior alinhamento sistêmico com materiais semicondutores e tecnologias quânticas.
- Preservação intacta da governança (TDD / CI-CD).
- Base sólida para preparação em potenciais diálogos institucionais.

**Negativas:**
- O projeto demandará tempo substancial de desenvolvimento focado puramente em infraestrutura numérica antes de retornar valores materiais do "mundo real".
- O escopo não simulará manufatura de wafers reais num curto horizonte de tempo.
- O modelo ainda não apresentará outputs de coerência de qubits.
- Inevitável necessidade de curadoria bibliográfica profunda para parametrização teórica dos defeitos no Si e no ambiente Poisson nas fases v0.3 e v0.4.

## Guardrails
As seguintes cercas de proteção permanecem absolutas para proteger o código e o time de extrapolação desenfreada:

- O proxy $C$ não se transformará em concentração física calibrada sem providências documentais baseadas em literatura.
- A promessa de simulação/predição de *coerência quântica* real permanece sumariamente fora do escopo.
- Modelagem termo-fluida e processos de crescimento em nível de fábrica (Czochralski macro, Bridgman industrial) estão fora do escopo.
- Toda inserção de novos mecanismos físicos ou solvers forçará a abertura de uma nova ADR.
- Toda figura final ou relatório interpretativo deverá registrar explicitamente as limitações inerentes e o caráter demonstrativo dos resultados.
- Toda iteração majoritária (minor release, ex: v0.2, v0.3) precisa herdar e passar na suíte completa de testes de regressão de sua antecessora.

## Alternatives Considered

1. **Implementar 2D imediatamente sem deliberação — REJEITADO.** Perda do horizonte de longo prazo; o 2D por si só não avança o problema físico, apenas a infraestrutura geométrica.
2. **Ir direto para soluções pesadas (QTCAD/TCAD comercial) — REJEITADO.** Custo astronômico, caixa-preta na física subjacente e perda do demonstrador acadêmico *in-house*.
3. **Mergulhar imediatamente em FEniCS / OpenFOAM / COMSOL / Czochralski real — REJEITADO.** Fuga violenta do escopo de um MVP restrito e quebra da agilidade proporcionada por NumPy nativo (ADR-001).
4. **Manter o software focado apenas no toy-model 1D termo-difusivo indefinidamente — REJEITADO.** Estagna o projeto muito aquém da aplicabilidade e ambição do escopo inicial.
5. **Evoluir gradualmente através do pipeline de ponte (Process-to-Device bridge reduzido) — ACEITO.**

## Links
*Links pendentes de verificação externa; serão curados em etapa bibliográfica específica nas aproximações das versões pertinentes.*

*(Nota futura para curadoria: Buscar simulação de defeitos pontuais em Czochralski Si, crescimento cristalino multifísico em FEniCS, tutoriais base de QTCAD, caracterização de qubits de spin em silício compatíveis com integração CMOS, bibliografia básica de Poisson-Schrödinger para quantum dots, e panorama de defeitos de contorno e superfícies 2D aplicados à tecnologia de materiais para estado sólido).*
