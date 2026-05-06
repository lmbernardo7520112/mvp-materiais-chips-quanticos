# Deliberação do Research Council — Evolução Process-to-Device do MVP

## Contexto

O projeto `mvp-materiais-chips-quanticos` encerrou com sucesso o ciclo v0.1. A atual versão atua como um demonstrador metodológico robusto das bases numéricas termo-difusivas (1D) regidas por rigorosas políticas de governança (SDD, TDD, Clean Code).

**Contornos da v0.1:**
- **Proxy C:** O campo de concentração ($C$) foi documentado estritamente como um proxy adimensional.
- **Limitações Deliberadas:** A simulação de processos reais de manufatura de wafer (ex: fornos Czochralski), predição de coerência quântica e predições de fidelidade de portas foram rigidamente excluídas para manter a integridade acadêmica.
- **Dívidas Assumidas:** A extensão bidimensional (2D) foi deferida via ADR-003.
- **Governança:** O branch `main` atua como SSOT (Single Source of Truth), atestada por CI verde completo.

## Pergunta Deliberativa

> *"Qual evolução de médio prazo aproximaria o MVP do objetivo de modelagem de materiais para chips quânticos sem quebrar a prudência científica?"*

## Pareceres do Conselho

### Especialista em solidificação e transporte de calor/massa
"O atual solver 1D é estável, porém academicamente trivial. O próximo passo lógico em estabilidade e modelagem não é adicionar novas equações gigantescas, mas estender o transporte térmico para domínios 2D, avaliando explicitamente a convergência $\Delta x / \Delta t$ sob discretização explícita. Não devemos tentar simular toda a câmara de crescimento Czochralski ou escoamento (Navier-Stokes) prematuramente. Foquemos no comportamento do sólido."

### Especialista em crescimento de cristais semicondutores
"Devemos parar de usar um campo 'genérico' $C$. Precisamos fazer a transição para um modelo do tipo *defect-like reaction-diffusion*. Isso significa parametrizar o modelo com termos de geração térmica $G(T)$ e recombinação $R(T, C)$ que se assemelhem às dinâmicas de vacâncias ou intersticiais em Si, mesmo mantendo a natureza adimensional por ora."

### Especialista em defeitos em silício e interfaces Si/SiO₂
"Uma vez que tenhamos a distribuição de defeitos mapeada após o processo térmico, precisamos conectar essa heterogeneidade material a um parâmetro funcional. A evolução mais segura é estabelecer uma 'carga efetiva'. Cada defeito pontual atua como uma perturbação de carga no retículo. Essa carga $\rho_{eff}$ é a ponte natural que leva o problema da engenharia de materiais para a engenharia de dispositivos."

### Especialista em TCAD, Poisson/Schrödinger e quantum dots
"Pular de um difusor 1D para uma suíte QTCAD complexa quebrará a estrutura do MVP. Precisamos evoluir para eletrostática simplificada. Uma vez mapeada a carga $\rho_{eff}$, podemos injetá-la como termo fonte em uma equação de Poisson idealizada. Posteriormente, podemos usar esse campo potencial eletrostático perturbado como o potencial de confinamento $V(x)$ em um modelo 1D ou 2D simplificado da equação de Schrödinger para extrair autovalores e autofunções (proxies de confinamento)."

### Especialista em dispositivos quânticos de estado sólido
"Nenhuma promessa de coerência ($T_1$, $T_2$) deve ser feita a curto ou médio prazo. As simulações de dispositivo devem se ater exclusivamente aos proxies de confinamento de carga (e.g., deslocamento do centro de massa da função de onda, variação de energia de ionização induzida por defeitos). Apenas prever como o ambiente eletrostático sujo perturba as métricas básicas da caixa quântica já é um feito extraordinário."

### Especialista em governança de software científico
"Cada evolução proposta adiciona camadas críticas de complexidade numérica. A rota delineada é sensata se for particionada. A versão v0.2 não deve conter física nova, mas apenas focar em blindar numericamente a base para aguentar o peso futuro das equações acopladas. Qualquer nova introdução física demandará ADRs obrigatórios."

## Diagnóstico do Estado Atual

- **Maturidade de engenharia:** Muito alta (TDD completo, integração CI, isolamento de domínios).
- **Maturidade científica:** Demonstrativa. A física é coerente, mas as variáveis e parâmetros de entrada não são calibrados nem atrelados à fenomenologia quântica.
- **Limitações do Proxy:** O uso continuado de $C$ restringe o poder de predição do modelo se não houver um mapeamento de C $\rightarrow$ variação de propriedades elétricas.
- **Riscos e Dívidas:** Pular diretamente para ferramentas pesadas (FEniCS, MOOSE) ou TCAD completo destruirá o framework construído. Construir um Czochralski real é uma tese de doutorado por si só. Não devemos fazê-lo.

## Deliberação Principal: O Pipeline Process-to-Device

O Conselho formaliza que a evolução do MVP será particionada no seguinte fluxo progressivo:

1. Processo térmico/processual
2. $\rightarrow$ Heterogeneidade material ou *defect-like state variable*
3. $\rightarrow$ Carga efetiva ou perturbação material eletrostática ($\rho_{eff}$)
4. $\rightarrow$ Eletrostática simplificada (Equação de Poisson)
5. $\rightarrow$ Proxy de confinamento/dispositivo (Schrödinger simplificado)

## Roadmap Científico Recomendado

* **v0.2 — Robustez Numérica**
  * 2D térmico simplificado.
  * Avaliação rígida de estabilidade 2D.
  * Análise de convergência dx/dt.
  * Injeção de `pytest-cov`.
  * **Zero física nova pesada**.

* **v0.3 — Defect-like Reaction-Diffusion**
  * Substituir $C$ genérico por $C_{def}$ (*defect-like state variable*).
  * Inserção de termos de geração $G(T)$ e relaxação/recombinação $R(T, C)$.
  * Integração de métricas de *freeze-in* pós-resfriamento.
  * Permanecerá adimensional e não calibrado.

* **v0.4 — Ponte Material-Eletrostática**
  * Solver Poisson 2D simplificado.
  * Definição de carga efetiva $\rho_{eff} = q_{eff} \cdot C_{def}$.
  * Domínio semicondutor/óxido idealizado (e.g., interface virtual).
  * Portões (gates) idealizados aplicando condições de contorno de potencial.
  * Novas métricas de perturbação eletrostática espacial.

* **v0.5 — Quantum Proxy**
  * Solver Schrödinger 1D/2D simplificado.
  * Resolução de autovalores/autofunções atreladas ao potencial eletrostático sujo resolvido na v0.4.
  * Avaliação de proxies de confinamento.
  * **Sem predição de coerência.**

* **v1.0 — Demonstrador Process-to-Device Completo**
  * Acoplamento final: *thermal process $\rightarrow$ defect-like map $\rightarrow$ electrostatic perturbation $\rightarrow$ confinement proxy*.
  * Geração de relatórios de aplicabilidade institucional direcionados ao CNPEM / LNNano / INCT-DQ.

## O Que NÃO Fazer Ainda

- Não simular forno Czochralski ou Bridgman real.
- Não produzir simulação industrial massiva de wafer.
- Não predizer tempo de coerência ($T_1$, $T_2$, $T_2^*$) ou fidelidade de porta quântica.
- Não investir em solvers Phase-Field ou OpenFOAM/FEniCSx/MOOSE como backends primários na infraestrutura atual.
- Não implementar suítes QTCAD ou invocar COMSOL diretamente sem uma etapa de redução fundamental em código aberto Python.
- Não embutir parâmetros reais retirados da literatura de forma mascarada, sem documentação, calibração cruzada e rastreio.

## Recomendação de Curto Prazo (v0.2)

O Conselho determina que a versão **v0.2** deve ser formalmente especificada logo após a assimilação deste relatório. Ela deve tratar a **robustez numérica bidimensional**, e não adentrar em física nova ou em fenômenos quânticos.

## Critérios de Governança para Versões Futuras

1. A introdução de toda e qualquer nova equação física exigirá uma **ADR independente**.
2. Toda nova variável fenomenológica implicará na obrigação de atualizar `docs/parameters.md`.
3. Novos solvers numéricos (e.g., Poisson, Schrödinger) precisarão de baterias completas de testes de finitude, invariância e regressão.
4. Qualquer inferência em nível de dispositivo (eletrostática, função de onda) deve ser enfaticamente classificada em relatórios como **proxy idealizado**.
5. O uso comercial, industrial ou reivindicações de fidelidade quantitativa permanecerão totalmente vetados sob a rubrica do software.

## Conclusão

A equipe conclui, por unanimidade, que adotar um pipeline *process-to-device* operando em "ondas" incrementais assegura sustentabilidade no código. Isso protege o repositório contra *feature creep* não testável, preservando a severidade metodológica comprovada durante a v0.1.
