# AI-RSE Methodology Dossier — MVP Quantum Materials

## 1. Executive Summary

O projeto **MVP Materiais Chips Quânticos** consiste no desenvolvimento de um demonstrador computacional *process-to-device* focado em qubits de silício/CMOS. O desenvolvimento deste projeto segue uma metodologia fortemente híbrida que denominamos **AI-RSE GateOps** (AI-assisted Research Software Engineering with Evidence-Gated Scientific Governance).

A metodologia combina Specification Driven Development (SDD), Test Driven Development (TDD) estrito (ciclo RED-GREEN-REFACTOR) e Governança Científica Baseada em Evidências (Architecture Decision Records — ADRs). O principal diferencial é a integração de inteligência artificial generativa em um regime de *human-in-the-loop*, onde a IA atua como executora rápida, inspecionadora de base de código e micro-auditora, enquanto o operador humano mantém controle diretivo absoluto sobre a arquitetura física e a validade científica.

O nível de maturidade do projeto alcançou a versão `v0.8.0` (em fase de proposta ADR-013), estabelecendo um alicerce que previne regressões físicas, superalegações (*overclaims*), acoplamentos prematuros e *dependency creep*, validado localmente e via CI/CD contínuo. A tese central é que o uso de IA em software de pesquisa exige uma arquitetura de governança rígida, que impeça a IA de inventar física para agradar ao usuário, substituindo implementações cegas por deliberações documentadas (*councils*) e portões de qualidade estritos (*quality gates*).

## 2. Project Mission and Scientific Boundary

A missão do MVP é modelar, de forma *adimensional/demonstrativa* para o *proxy* reativo-difusivo e fisicamente ancorado em SI para a camada eletrostática, a cadeia *process-to-device*. O projeto é metodologicamente inspirado em Maurand et al. 2016, porém com o entendimento estrito de que Maurand serve como **âncora de dispositivo-alvo**, e **nunca** como calibração experimental preditiva neste MVP.

O MVP **faz**:
- Simulação termo-difusiva e reativo-difusiva de defeitos ($C_{def}$).
- Integração de bibliotecas de perfis de energia ($D_{it}(E)$) balanceadas entre literatura (Sze, Terman) e perfis demonstrativos.
- Mapeamento C1 de balanço de densidade superficial de carga ($\sigma_{eff}$).
- Mapeamento C2 conservativo (demo) da interface para grid volumétrico de Poisson.

O MVP **não faz e bloqueia permanentemente**:
- Simulação de decoerência ($T_1$, $T_2$).
- Predição de coerência e fidelidade operacional de qubit.
- Predição real de ruído de carga que possa ser contrastada fisicamente contra medições.
- Substituição de software TCAD comercial (ex: QTCAD ou Sentaurus).
- Alegações de "calibração" com base apenas em âncoras da literatura.

## 3. Chronological Development Map

| Release | Tipo | Objetivo / Decisão Científica | Guardrails / Resultado |
|---------|------|--------------------------------|------------------------|
| **v0.1** | Setup | Início do repositório, setup CI. | Criação do branch `main`. |
| **v0.2** | GREEN | Robustez 2D e convergência térmica. | CI configurado. |
| **v0.3** | RED/GREEN | Núcleo *defect-like* reativo-difusivo. | ADR-006 aceita. GateOps integrado. |
| **v0.4.x** | Demo | Poisson Bridge e Metadata Mode B. | ADR-007, ADR-008. Bloqueio de calibração. `policy.json` rigoroso contra "Schrodinger". |
| **v0.5.x** | Governance/GREEN | Bookkeeping de $\sigma_{eff}$ (Camada C1). | ADR-009, ADR-010. Demo de *surface charge*. Escala da literatura incorporada (v0.5.2). |
| **v0.6.x** | RED/GREEN | Library de perfis $D_{it}(E)$. | Biblioteca particionada. Council reancorou o escopo *process-to-device*. |
| **v0.7.x** | RED/GREEN/Demo | Mapeamento C2 da carga (Source Regularization). | ADR-012. Conservação de carga ($10^{-12}$). Nenhum solver coupling (bloqueado). Demo CSV/Pandas auditada. |
| **v0.8.0** | Governance | Proposição de ADR-013 (C3 Solver Coupling). | Documentação-only. Bloqueado física acoplada prematuramente. Conselho de Risco. PR #44 submetido. |

## 4. Specification Driven Development (SDD)

No modelo AI-RSE, a escrita das especificações precede qualquer código de execução. 
- **ADRs (Architecture Decision Records):** Foram a força motriz que impediu a IA de codificar predições soltas. Exemplos: a ADR-009 separou o *bookkeeping* (C1) do cálculo do potencial (C3), e a ADR-012 forçou a definição do espalhamento de carga de interface antes do acoplamento com o solver (ADR-013).
- **Decision Briefs / Research Councils:** Funcionaram como um freio *peer-review* simulado. Quando a IA sugeria uma modelagem acoplada complexa, o council recomendava separar em fases controladas.
- **Risk Matrices & Acceptance Gates:** Definiram numericamente quando o *release* estaria pronto. O código foi bloqueado se tentasse fundir *RED*, *GREEN* e *Docs* num só PR. 
- **Walkthrough:** A documentação guia funcionou como o estado vivo, impedindo *hallucinations* sobre em que etapa o projeto estava.

## 5. Test Driven Development (TDD)

A implementação de regras científicas seguiu um TDD hiperestrito (via `.agent/skills/tdd-red-green-release`).
- **RED:** O PR *RED* precisava deliberadamente falhar, geralmente com `ModuleNotFoundError` (pois os arquivos não podiam ser criados) ou `AssertionError`. Exemplo clássico foi o v0.7.2 (17 *failed* e 3 *passed*), onde a falha foi auditada para garantir que falhava *pelo motivo certo*. 
- **GREEN:** Nenhuma alteração fora do alvo de escopo era permitida. Apenas código capaz de passar nos testes criados no *RED* era acatado.
- **Exemplo de falha barrada:** Em v0.5.0, tentativas de "esconder" falhas de teste foram bloqueadas. O *GREEN* dependia obrigatoriamente de um *RED* em *commit/branch* separado e auditável.

## 6. Governance Architecture

O projeto não confiou apenas na intenção, mas codificou a governança no arquivo `tools/quality_gates/policy.json` e nos testes.
- **Forbidden Terms:** Palavras como `Schrodinger`, `TCAD`, e `fidelity prediction` configuram *hard fail* na suíte se aparecerem no código sem as devidas ressalvas documentais (via regex estrito nos *quality gates*).
- **Authorized Files:** Um portão que analisa o diff e impede que arquivos como `poisson_solver_2d.py` sejam modificados sub-repticiamente (ex: em releases da Camada C2 que não deveriam tocar no solver).
- **CI Matrix:** O GitHub Actions foi usado para validar Python 3.11 e 3.12 (Linting e Typerig com Pyright), e garantir Cobertura de 70%+. 
- **Branch/Tagging Discipline:** `merge commit` sempre no `main`. Tags só permitidas após o *Pipeline* no `main` ficar *verde*, evitando tags quebradas (como na retificação do *closure* v0.7.5 indevido).

## 7. Agent Skills / SKILL.md Usage

Em projetos assistidos por LLM, "prompts gigantes" sofrem degeneração. Foram incorporadas **Agent Skills** versionadas (`.agent/skills/`). 

1. **`ai-rse-gateops`:** Usada para inspecionar e coletar evidências de forma cirúrgica. Impediu *hallucinations* pois forçou a IA a ler o disco local via CLI.
2. **`tdd-red-green-release`:** Garante o fluxo exato, bloqueando a IA que tradicionalmente tenta implementar e testar num só comando.
3. **`physics-dimensional-audit`:** Evita confusão entre unidades adimensionais ($C_{def}$) e SI ($D_{it}$, $N_{it}$, $\sigma_{eff}$). Força a IA a reportar dimensionalidade.
4. **`scope-guardrails`:** Crucial na versão v0.7.x e v0.8.0. Impede acoplamentos que exijam ADR (ex: *C3-D self-consistency* bloqueado).
5. **`release-manager` e `report-auditor`:** Separam a verificação das alegações da escrita em si, atuando como o "revisor estrito" da matemática da IA e contagem de PRs.

As *Skills* versionadas no repositório permitem que qualquer instância de Agente IA incorpore imediatamente o escopo e estado mental do projeto, transformando um prompt frágil em um processo rastreável.

## 8. Human-in-the-Loop Responsibility

A automação cega em engenharia de software científico gera ruído acadêmico. O humano neste fluxo exerceu as seguintes responsabilidades:
- **Diretor Científico e Guardião:** Questionou o uso prematuro de pandas (gerando a decisão por csv padrão em v0.7.4 para evitar *dependency creep*).
- **Crítico de Física:** Rejeitou a calibração demonstrativa de $E_0$ proposta pela IA e proibiu o uso genérico do *t_eff*. 
- **Supervisor Metodológico:** Detectou e corrigiu recomendações apressadas de *release closure* (ex: recomendação errônea para v0.7.5 closure no meio de v0.7.4).
A IA operou comandos Git, gerou relatórios, inferiu lógica de teste a partir dos ADRs, mas a *Decisão de Aceite* pertenceu integralmente ao humano, preservando a integridade acadêmica.

## 9. Generative AI Challenges Encountered

Os seguintes desafios surgiram e foram mitigados pela metodologia:
1. **Risco de overclaim:** A IA costuma escrever `This predicts coherence`. *Mitigação*: `policy.json` com `forbidden_terms`.
2. **Risco de implementar antes da ADR:** A IA tende a dar a solução em código antes do acordo. *Mitigação*: Skill `tdd-red-green-release` e `authorized_files` restrito.
3. **Risco de dependências creep:** A IA sugeriu `pandas` para um arquivo `.csv` minúsculo. *Mitigação*: Rejeição humana, documentada como *Microaudit* em v0.7.4.
4. **Reportes otimistas:** A IA reportou PRs "fechados" prematuramente. *Mitigação*: Skill `report-auditor` forçou extração direta do `gh pr list --state all`.
5. **"Fix" pelo apagamento:** A IA contornou o `policy.json` removendo menções inteiras ao invés de codificar a isenção de forma madura. *Mitigação*: Verificação humana dos *diffs*.

## 10. Scientific Methodology and Physics Governance

O caminho *process-to-device* ($C1 \rightarrow C2 \rightarrow C3$) é metodologicamente superior a tentar codificar o solver diretamente porque respeita a **incerteza epistêmica**. 
- $D_{it}(E)$ só pôde existir após C1 definir as matrizes de ocupação.
- O mapeamento C2 (conservação de volume/sheet) foi documentado para garantir a física ($10^{-12}$ error) antes de enviar a carga cega a um *solver* numérico (C3), evitando resíduos numéricos incontrolados na aproximação de Poisson.
- Confinamento Quântico (Equação de Schrödinger) segue bloqueado, aguardando que o baseline eletrostático prove integridade total, uma vez que o acoplamento de funções de onda é o estágio mais instável de simulação.

## 11. Metrics and Evidence

| Métrica | Status / Valor | 
|---------|---------------|
| **Total de Testes** | 281 |
| **Coverage** | 88.00% |
| **Quality Gates** | 6/6 PASS |
| **Linting/Type** | ruff PASS / pyright 0 errors |
| **Output figures/csv** | 14 figures / 7 CSVs |
| **ADRs** | 13 (ADR-001 a ADR-013) |
| **Decision Briefs** | 20 |
| **Research Councils** | 16 |
| **Agent Skills** | 6 |
| **Tags** | 31 tags (até v0.7.4) |
| **Total de PRs** | 44 (1 aberto, 43 merged) |

*(Evidências extraídas do `pytest`, `gh pr list`, e `find docs/` no Passo 1/2/4).*

## 12. Methodology Scorecard

| Eixo | Nota (0-10) | Justificativa |
|---|---|---|
| **SDD Maturity** | 9/10 | Alta fidelidade; especificações geram TDD. |
| **TDD Maturity** | 9/10 | Isolamento estrito de commits RED/GREEN. Cobertura excelente (88%). |
| **Scientific Governance** | 10/10 | Bloqueios sistemáticos contra físicas mal documentadas. |
| **Human-in-the-Loop** | 9/10 | Decisões maduras; forte revisão contra *AI hallucinations*. |
| **Skill Usage Maturity** | 8/10 | Integrado profundamente, embora demande *prompts* estritos. |
| **Release Discipline** | 9/10 | Versionamento limpo (v0.x.y), proteção de branch funcional. |
| **Physics Progression** | 8/10 | Lenta porém robusta; prioriza a mecânica à pressa. |

## 13. Comparison with Professional Best Practices

Comparado com a base profissional de **Research Software Engineering (RSE)**:
- **Pontos Fortes:** O uso do *Architecture Decision Records* (ADR) associado aos portões estáticos (Lint/Policy) rivaliza com projetos de software crítico regulado, impedindo a fragilidade comum de códigos acadêmicos "espaguetes".
- **Natureza Experimental:** O uso de IA para automatizar *commits* e escrever relatórios longos (como os Councils) acelera muito, mas introduz um custo contínuo de verificação humana do contexto da conversa com o *Agent*.
- A disciplina *Trunk-based development* com PRs curtos e revisões assíncronas é idêntica ao que se vê em ambientes nativos de nuvem e engenharia Open-Source de alta escala.

## 14. Weaknesses and Open Risks

- **Ausência de Solver Coupling real:** Muito trabalho preparatório ($C1$, $C2$, $D_{it}$) mas o potencial $\Phi(x,y)$ ainda não responde fisicamente à distribuição de defeitos gerada pelo processo.
- **Fardo Burocrático:** O excesso de governança (Councils, Risk Matrices, Briefs, Acceptance Gates) gera dezenas de arquivos Markdown por release, podendo retardar avanços físicos iterativos diretos se a burocracia descolar do código real.
- **Automação dependente de contexto:** Se a conversa com a IA for limpa (clear context), ela produz maravilhas. Se for fragmentada, a IA perde rastreio e sugere ações de closure na fase errada.

## 15. Recommended Next Methodological Improvements

- **Release Methodology Checklist:** Consolidar a sequência de relatórios (Gate, Brief, Audit, Closure) num script unificado para evitar esquecimento de etapas.
- **Manter ADR-only na v0.8.0:** Validar a proposta C3 exaustivamente.
- **Dependency Template:** Exigir um *decision brief* formal para cada pacote injetado no `pyproject.toml`, formalizando a restrição ao `pandas` ou outras bibliotecas pesadas.
- **Review Review:** Adicionar explicitamente os comentários críticos do humano nos *release notes* para que os bloqueios sejam transferidos para o leitor.

## 16. Conclusion

A metodologia híbrida **AI-RSE GateOps** provou ser uma arquitetura fenomenal para gerenciar os potenciais de overclaim e imprecisão da IA Generativa aplicada à física do estado sólido computacional. O Humano conteve a entropia da automação enquanto a IA Generativa operou a força braçal do código iterativo, verificação estática, e *boilerplates* complexos de TDD. O balanço foi respeitado: a Governança bloqueou a predição vazia, o TDD construiu alicerces verificáveis, e o *process-to-device proxy* caminhou confiavelmente em direção ao solver acoplado.
