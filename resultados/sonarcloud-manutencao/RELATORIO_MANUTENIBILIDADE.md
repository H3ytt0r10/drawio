  q# Avaliação de manutenibilidade do draw.io: resultados e evidências

**Data da coleta:** 08/11/2026. **Objetivo:** G3, equipe Mary Jackson. **Natureza:** análise estática de recortes de código; avaliação parcial do escopo planejado.

Este relatório reúne, em um único arquivo, método, medidas, cálculos, julgamentos, evidências de processamento e identificação do código. Pode ser copiado para `docs/fase-4/manutenibilidade.md` no repositório da documentação. Os anexos estão incorporados; não há dependência de imagens ou de arquivos locais. Os links externos identificam fontes primárias e permitem conferir o código e as análises.

## 1. Objetivo, referência e abrangência

O objetivo G3 é examinar a manutenibilidade dos componentes selecionados do draw.io, sob a perspectiva da equipe avaliadora, para apoiar a compreensão da viabilidade de manter uma versão própria. Foram operacionalizadas somente as métricas M3.1 e M3.2: complexidade cognitiva média para importação e rótulos, separadamente, e percentual de duplicação para exportação PNG/PDF/SVG, conjuntamente. Essa delimitação deriva de [R1], [R2] e [R3].

A documentação foi conferida na revisão `c41e8cb60d0e7ffe776a94ae24c58115f7c59f26`. A análise não produz julgamento de Segurança ou Eficiência de desempenho. As exigências de cinco tentativas, cargas de diagramas, latência e memória pertencem às métricas M2, não às duas medidas estáticas de G3 [R1].

**Situação de aderência:** as fórmulas, as separações entre componentes e as faixas de julgamento foram aplicadas. Entretanto, não se declara atendimento integral ao plano: o código medido é da versão 32.6.10, enquanto a Fase 3 prevê 32.2.0; a seleção de funções é operacional e a implementação do servidor de exportação não foi examinada. As consequências constam na seção 7. Os resultados são válidos como observações dos recortes identificados, sem equivaler a uma certificação do produto [R4–R6; E1–E4].

## 2. Rastreabilidade e regra de julgamento

| Questão GQM | Foco examinado | Subcaracterística | Métrica | Evidência |
| --- | --- | --- | --- | --- |
| Q3.1 | Compreensão do código de leitura e conversão de arquivos | Analisabilidade | M3.1 = C / F, importação | E1 e E4 |
| Q3.2 | Compreensão do código de edição e formatação dos rótulos | Analisabilidade | M3.1 = C / F, rótulos | E2 e E4 |
| Q3.3 | Duplicação no código de exportação PNG/PDF/SVG | Modificabilidade | M3.2 = 100 × Ld / Lt | E3 e E4 |

Fonte das associações: fichas de métricas [R1], modelo de qualidade [R6] e diagrama GQM [R7]. A tabela de rastreabilidade [R8] inverte os nomes das subcaracterísticas para Q3.1/Q3.2 e Q3.3. Esta divergência documental é explicitada; adotam-se as associações concordantes das fichas, do modelo e do diagrama, preservando os identificadores Q3 e M3.

| Métrica | Adequado | Atenção | Crítico |
| --- | --- | --- | --- |
| M3.1, por componente | valor ≤ 10 | 10 < valor ≤ 15 | valor > 15 |
| M3.2, exportação conjunta | valor ≤ 5% | 5% < valor ≤ 10% | valor > 10% |

As faixas são critérios preliminares da equipe, não limites normativos da ISO. Não se calcula nota global G3, pois a referência não estabelece uma regra de agregação [R2]. As hipóteses de [R3] apresentam texto inclusivo e expressões entre parênteses com `<`; a classificação segue a tabela explícita de [R2]. Nenhum resultado está exatamente na fronteira, portanto essa inconsistência não altera os julgamentos desta coleta.

## 3. Objeto medido e procedimento

### 3.1 Identificação do código

| Elemento | Identificação | Prova |
| --- | --- | --- |
| Repositório de código | `H3ytt0r10/drawio` | [Código na revisão medida](https://github.com/H3ytt0r10/drawio/tree/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3) |
| Revisão declarada na análise | `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3` | Campos `revision` e `projectVersion` em E1–E3 |
| Versão do código | `32.6.10` | [Arquivo VERSION na revisão medida](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/VERSION) |
| Universo operacional selecionado | 41 recortes: 8 de importação, 20 de rótulos e 13 de exportação | Manifesto E4 e inventários `arquivos.components` de E1–E3 |
| Fonte das medidas | SonarCloud, organização `drawio-sonarcloud-testes-qualidade` | `task.task.organization` em E1–E3 |

O commit identifica o código de origem, e não uma publicação dos scripts e deste relatório. A preparação e a documentação foram produzidas no ambiente local. Não se pressupõe que existam no GitHub sob esse mesmo commit.

### 3.2 Seleção e unidade de análise

As funções de importação abrangem leitura local, validação, extração e instalação do modelo. As de rótulos abrangem leitura/aplicação do texto, interação com o editor e painel de formatação. As de exportação abrangem configuração da saída, construção de requisições, canvas e SVG. A lista completa de assinaturas, arquivos e intervalos encontra-se em E4, com links para as linhas originais.

Cada intervalo foi copiado para um arquivo JavaScript distinto, com o corpo preservado, incluindo callbacks e funções internas. Não foram acrescentados wrappers nem preenchimento artificial entre intervalos. A seleção foi fixada por linhas e SHA-256; após a auditoria, a preparação passou também a rejeitar sobreposições de intervalos do mesmo arquivo. A correção aplicada a rótulos é descrita na seção 6.

O denominador F é a quantidade `functions` devolvida pelo analisador, e não o número de arquivos: funções internas também podem contribuir para a contagem. Assim, 8 recortes de importação resultaram em 25 funções, e 20 recortes de rótulos resultaram em 116 funções [E1–E2]. Para M3.1, utiliza-se a complexidade agregada dos recortes como operacionalização de C. A equivalência entre essa agregação e uma soma individual das funções no módulo original não foi verificada; essa é uma ameaça à validade de construto, não uma prova de equivalência.

### 3.3 Coleta e verificação

A coleta utilizou três projetos distintos para manter importação e rótulos separados e permitir que os recortes dos três formatos de exportação fossem analisados em conjunto [E1–E3]. O procedimento foi:

1. Fixar a revisão, verificar hashes dos intervalos e validar a sintaxe dos recortes com `node --check`.
2. Analisar somente o diretório `src` preparado para cada componente, com codificação UTF-8, SCM desativado e `projectVersion`/`revision` vinculados ao commit do código.
3. Aguardar `SUCCESS` em `api/ce/task` e registrar `analysisId`.
4. Conferir o identificador retornado por `api/project_analyses/search` antes e depois da consulta das medidas.
5. Comparar o inventário de `api/components/tree` com o manifesto e consultar somente `cognitive_complexity`/`functions` ou `duplicated_lines`/`lines`, conforme o componente.
6. Preservar as respostas e recalcular fórmulas e julgamentos a partir dos registros incorporados neste documento.

As medidas consultadas são do código total analisado, sem o prefixo `new_`. Para Lt foi utilizada `lines`, conforme a definição da densidade de duplicação; não foi usada `ncloc`. As chaves técnicas e a fórmula da densidade estão documentadas pela SonarSource [R9]. As contagens não foram estimadas por regex nem substituídas por resultados de testes sintéticos.

O ambiente registrado no console foi Windows 11, SonarScanner CLI 8.1.0.6389 e Java 21.0.9; as execuções também identificaram o analisador JavaScript 14.4.0.46458 e o perfil Sonar way core. E6 preserva os trechos do console que fundamentam essa identificação. Não se interpreta a duração de processamento como uma métrica de desempenho do draw.io.

## 4. Resultados e interpretação por questão

| Questão | Medidas do SonarCloud | Cálculo | Resultado | Julgamento | Prova |
| --- | --- | --- | --- | --- | --- |
| Q3.1 — Importação | C = 275; F = 25 | 275 / 25 | 11,0 | **Atenção** | [E1](#e1) |
| Q3.2 — Rótulos | C = 1057; F = 116 | 1057 / 116 | 9,112068965517242 | **Adequado** | [E2](#e2) |
| Q3.3 — Exportação PNG/PDF/SVG | Ld = 28; Lt = 2846 | 100 × 28 / 2846 | 0,9838369641602248% | **Adequado** | [E3](#e3) |

**Q3.1 — Importação.** A média 11 é superior ao limite 10 e não ultrapassa 15; classifica-se o recorte como **Atenção**. A hipótese H3.1 não é sustentada nesse recorte. O resultado indica prioridade relativa para revisão da compreensão do código selecionado, mas não identifica, por si só, qual função é mais complexa nem mede esforço de manutenção em horas [R2–R3; E1].

**Q3.2 — Rótulos.** Após corrigir a sobreposição de recortes, a média é 9,112068965517242; a classificação é **Adequado**. O valor é inferior a 10 e é compatível com H3.2 exclusivamente para o conjunto corrigido e para a operacionalização descrita. O número anteriormente comunicado, 9,512820512820513, foi invalidado como resultado final de Q3.2 porque incluía código contado duas vezes [E2; E5].

**Q3.3 — Exportação.** O cálculo usa 28 linhas duplicadas e 2846 linhas analisadas, produzindo 0,9838369641602248%. O valor é inferior a 5%; o recorte conjunto é classificado como **Adequado** e a observação é compatível com H3.3 nesse conjunto. Não se infere ausência de duplicação ou facilidade de alterar o servidor de PDF [R2–R3; E3].

Não se calcula média entre os três resultados nem se transforma a classificação em decisão global de adoção. A referência exige julgamento por questão, sem agregação definida para G3 [R2].

## 5. Ações de melhoria propostas

As ações abaixo são recomendações decorrentes dos resultados e limites; não são mudanças já realizadas nem novos critérios de aprovação. A inclusão de ação de melhoria acompanha o conteúdo previsto para a Fase 4 [R10].

| Prioridade | Ação proposta | Fundamentação e limite |
| --- | --- | --- |
| 1 | Consolidar o recorte da Fase 3 e repetir as medidas na versão 32.2.0, ou registrar formalmente a alteração da versão planejada | Divergência entre VERSION e ambiente previsto; não cabe ao relatório alterar unilateralmente o plano [R4–R5]. |
| 2 | Obter a distribuição de complexidade das funções de importação antes de escolher alvos de refatoração | M3.1 = 11, faixa Atenção; a média não localiza as funções responsáveis [E1]. |
| 3 | Auditar os limites dos recortes e manter a verificação de ausência de sobreposição | A sobreposição em rótulos alterou o universo contado; a correção foi necessária antes do julgamento final [E4–E5]. |
| 4 | Identificar e incluir, quando pertencente à implantação fixada, a implementação do serviço de exportação de PDF | O cliente constrói requisição para EXPORT_URL; a avaliação de dependências participantes é exigida pelo escopo [R4; seção 7]. |
| 5 | Preservar os snapshots de cada coleta ao repetir a medição | Os painéis e as consultas de medidas correntes podem refletir novas análises; o ID e o snapshot distinguem a campanha histórica [E1–E3]. |

## 6. Correção da coleta de rótulos e histórico

A auditoria identificou que o recorte original de `mxCellEditor.prototype.startEditing` ocupava as linhas 46070–46293, incluindo `toggleViewMode` (46154–46293), já selecionada em outro arquivo. O fechamento real de `startEditing` está na linha 46152 e não possui ponto e vírgula; a delimitação anterior procurava o fechamento com `};` e avançava até a função seguinte. As [linhas originais](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L46149-L46155) e o registro E5 permitem conferir a ocorrência.

Corrigiu-se o intervalo para 46070–46152 e repetiu-se somente a análise de rótulos, no mesmo projeto. O código de produção não foi modificado. Importação e exportação foram preservadas: a verificação de intervalos não identificou sobreposição nesses dois conjuntos. O manifesto E4 descreve o universo final.

| Registro | C | F | Média | Uso |
| --- | --- | --- | --- | --- |
| Rótulos original, análise `0818a1d8-7c02-44c1-8d87-8f1e44ba7756` | 1113 | 117 | 9,512820512820513 | Histórico invalidado para julgamento final |
| Rótulos corrigido, análise `4853c608-87f3-477c-ae03-18d6f2fab544` | 1057 | 116 | 9,112068965517242 | Resultado final deste relatório |

O sucesso técnico da análise original não detectava a seleção duplicada. Portanto, `SUCCESS` comprova processamento pelo serviço, mas não comprova correção metodológica do recorte.

## 7. Limitações e aderência ao planejamento

| Requisito ou limite | Situação demonstrada | Consequência para a interpretação |
| --- | --- | --- |
| Usar M3.1/M3.2, fonte SonarCloud e cálculos definidos [R1] | Atendido para os recortes; respostas e cálculos em E1–E3 | Não equivale a validar todas as propriedades de manutenibilidade. |
| Separar importação/rótulos e reunir exportação [R1] | Atendido pelos três projetos e respectivos inventários | Não combinar os resultados em uma única média. |
| Aplicar faixas e julgamento por questão [R2] | Atendido | Não atribuir nota global G3. |
| Fixar código e seleção no plano antes da análise [R4] | Parcial: commit e manifesto identificados na coleta; o plano da Fase 3 está em elaboração e o recorte foi retificado | É necessário integrar a delimitação ao plano e validar sua cobertura com a equipe. |
| Versão da Fase 3 [R5] | Não atendido nesta campanha: 32.6.10, em vez de 32.2.0 | Não transferir estes números para a versão planejada. |
| Dependências participantes da exportação [R4] | Cobertura parcial do cliente | Não generalizar M3.2 para o serviço externo ou para a implantação completa. |
| Limitar conclusões ao código selecionado [R4] | Atendido na interpretação | Não declarar manutenibilidade adequada do draw.io inteiro. |

A separação das funções remove contexto do módulo e pode alterar a agregação de complexidade; em duplicação, também pode omitir sequências que atravessem fronteiras entre funções. Os ramos compartilhados dentro das funções foram preservados, inclusive quando atendem outros formatos; sua contribuição não foi isolada. Essas condições limitam a validade de construto de M3.1/M3.2 no conjunto escolhido [E4].

No código cliente, `createDownloadRequest` devolve `new mxXmlRequest(EXPORT_URL, paramsStr)` ([linha 4150](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L4131-L4151)); `downloadRequestBuilder` trata explicitamente `format == 'pdf'` ([linhas 4180–4191](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L4180-L4191)). Isso demonstra o encaminhamento pelo cliente, não qual servidor seria efetivamente usado em uma instalação: essa implantação não foi exercitada nesta análise estática. O manifesto E4 não inclui a implementação de um servidor de exportação.

As faixas são preliminares e a média pode ocultar funções com valores muito superiores ao agregado. Não foram medidos esforço real de correção, defeitos ou tempo de manutenção. Os sensores padrão do SonarCloud não constituem critérios adicionais de G3 neste relatório. Consequentemente, o fechamento acadêmico adequado é **avaliação parcial, com resultados dos recortes e desvios de planejamento identificados**, sem declaração de conformidade integral.

## 8. Auditoria e reprodução

Cada evidência E1–E3 contém os retornos preservados de processamento (`task`), identificação da análise (`analysis`), inventário (`arquivos`) e medidas (`medidas`). Para conferir os resultados, compare `task.task.analysisId` com `analysis.analyses[0].key`, confira `revision`/`projectVersion`, conte os arquivos do inventário e recalcule a tabela da seção 4. Os horários originais estão em UTC; a tabela abaixo apresenta a conversão para America/Sao_Paulo, UTC−03:00.

| Componente | Término do processamento (UTC−03:00) | Situação | Consulta da tarefa |
| --- | --- | --- | --- |
| Importação | 08/11/2026 14:31:30 | SUCCESS | [task AaG8NwB7hQXxjEzKTt3t](https://sonarcloud.io/api/ce/task?id=AaG8NwB7hQXxjEzKTt3t) |
| Rótulos | 08/11/2026 14:46:49 | SUCCESS | [task AaG8RPSTbE9rxH86FwoI](https://sonarcloud.io/api/ce/task?id=AaG8RPSTbE9rxH86FwoI) |
| Exportação PNG/PDF/SVG | 08/11/2026 14:35:01 | SUCCESS | [task AaG8OkuaYN-65yNNqmQN](https://sonarcloud.io/api/ce/task?id=AaG8OkuaYN-65yNNqmQN) |

Os links `api/ce/task?id=...` identificam as tarefas históricas. Os painéis e `api/measures/component` exibem o estado corrente e podem mudar com nova coleta; por isso as respostas originais estão incorporadas. O acesso ao serviço pode depender de sua disponibilidade e das permissões da conta.

E4 contém os intervalos e hashes necessários para reconstruir os recortes a partir da revisão pública. Salve o JSON do anexo como `recortes.json`; o algoritmo de reconstrução é:

```python
import hashlib, json
from pathlib import Path
from urllib.request import urlopen

manifesto = json.loads(Path('recortes.json').read_text(encoding='utf-8'))
commit = manifesto['commit']
base = f'https://raw.githubusercontent.com/H3ytt0r10/drawio/{commit}/'
cache = {}
for grupo, registros in manifesto['componentes'].items():
    for r in registros:
        if r['arquivo'] not in cache:
            with urlopen(base + r['arquivo']) as resposta:
                texto = resposta.read().decode('utf-8')
            cache[r['arquivo']] = texto.replace('\r\n', '\n').replace('\r', '\n')
        linhas = cache[r['arquivo']].splitlines(keepends=True)
        trecho = ''.join(linhas[r['inicio'] - 1:r['fim']])
        assert hashlib.sha256(trecho.encode('utf-8')).hexdigest() == r['sha256_lf']
        destino = Path('reproducao') / grupo / r['recorte']
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(trecho, encoding='utf-8', newline='\n')
```

Valide os `.js` com `node --check`. Para nova coleta, em cada diretório `reproducao/<grupo>`, configure o SonarScanner com `sonar.sources=src`, `sonar.sourceEncoding=UTF-8`, `sonar.scm.disabled=true`, `sonar.javascript.detectBundles=false` e `sonar.projectVersion`/`sonar.scm.revision` iguais ao commit. Use a organização e a chave do projeto correspondente em E1–E3, com autenticação pelo ambiente (`SONAR_TOKEN`). Execute um projeto para importação, outro para rótulos e outro para os três formatos de exportação juntos. A instalação do scanner é documentada em [R11]. Esse procedimento é uma instrução de reprodução; não se afirma que uma nova versão do analisador produzirá necessariamente os mesmos valores.

Os anexos registram hashes SHA-256 do JSON canônico: chaves ordenadas, UTF-8, `ensure_ascii=False` e separadores `(',', ':')`. Eles permitem detectar alteração dos dados incorporados, mas não são uma assinatura digital do SonarCloud. Os IDs, horários e links do serviço constituem a trilha de conferência externa.

## 9. Referências

- **[R1]** Equipe Mary Jackson. [Métricas — Manutenibilidade](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-2/metricas.md#manutenibilidade-dupla-3).
- **[R2]** Equipe Mary Jackson. [Níveis e julgamento — Manutenibilidade](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-2/niveis-e-julgamento.md#manutenibilidade-dupla-3).
- **[R3]** Equipe Mary Jackson. [Objetivos, questões e hipóteses — G3](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-2/objetivos-questoes-hipoteses.md#manutenibilidade-dupla-3).
- **[R4]** Equipe Mary Jackson. [Escopo e profundidade](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-1/escopo.md).
- **[R5]** Equipe Mary Jackson. [Fase 3 e versão prevista](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-3/index.md).
- **[R6]** Equipe Mary Jackson. [Modelo de qualidade](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-1/modelo-de-qualidade.md).
- **[R7]** Equipe Mary Jackson. [Diagrama GQM](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-2/diagrama-gqm.md).
- **[R8]** Equipe Mary Jackson. [Rastreabilidade](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-2/rastreabilidade.md).
- **[R9]** SonarSource. [Definições das métricas do SonarQube Cloud](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/metric-definitions). Consulta em 08/11/2026.
- **[R10]** Equipe Mary Jackson. [Fase 4 — conteúdo previsto](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-4/index.md).
- **[R11]** SonarSource. [SonarScanner CLI](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/scanners/sonarscanner-cli). Consulta em 08/11/2026.

## 10. Evidências incorporadas

Os anexos seguintes são parte deste arquivo. Suas tabelas de inventário e seus snapshots permitem auditar a seleção, os denominadores e os estados de processamento sem transportar outros arquivos.

<a id="e1"></a>

### E1 — Importação

Projeto: `lucaszg-drawio-importacao`. [Painel](https://sonarcloud.io/dashboard?id=lucaszg-drawio-importacao). [Tarefa histórica](https://sonarcloud.io/api/ce/task?id=AaG8NwB7hQXxjEzKTt3t). Análise: `55180c38-c24b-48d4-adc7-41c45969d11a`.

SHA-256 do snapshot JSON canônico: `83f102dfa6b3f602dcfa0f108439b2c778a127ebf690b66ae0ea5650e1f2f504`.

<details markdown="1">
<summary>Abrir resposta preservada E1 (processamento, análise, inventário e medidas)</summary>

```json
{
  "task": {
    "task": {
      "id": "AaG8NwB7hQXxjEzKTt3t",
      "type": "REPORT",
      "componentId": "AaG8ICO1hQXxjEzKTtXg",
      "componentKey": "lucaszg-drawio-importacao",
      "componentName": "lucaszg-drawio-importacao",
      "componentQualifier": "TRK",
      "analysisId": "55180c38-c24b-48d4-adc7-41c45969d11a",
      "status": "SUCCESS",
      "submittedAt": "2026-11-08T17:31:23+0000",
      "submitterLogin": "lucaszg-g-0JgHv@github",
      "startedAt": "2026-11-08T17:31:23+0000",
      "executedAt": "2026-11-08T17:31:30+0000",
      "executionTimeMs": 6408,
      "logs": false,
      "hasScannerContext": true,
      "organization": "drawio-sonarcloud-testes-qualidade",
      "warningCount": 0,
      "warnings": []
    }
  },
  "analysis": {
    "paging": {
      "pageIndex": 1,
      "pageSize": 1,
      "total": 1
    },
    "analyses": [
      {
        "key": "55180c38-c24b-48d4-adc7-41c45969d11a",
        "date": "2026-11-08T17:29:58+0000",
        "events": [
          {
            "key": "AaG8Nxl3z0zoRdwyr4fC",
            "category": "VERSION",
            "name": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3"
          }
        ],
        "projectVersion": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3",
        "manualNewCodePeriodBaseline": false,
        "revision": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3"
      }
    ]
  },
  "arquivos": {
    "paging": {
      "pageIndex": 1,
      "pageSize": 500,
      "total": 8
    },
    "baseComponent": {
      "organization": "drawio-sonarcloud-testes-qualidade",
      "key": "lucaszg-drawio-importacao",
      "name": "lucaszg-drawio-importacao",
      "qualifier": "TRK",
      "tags": [],
      "visibility": "public"
    },
    "components": [
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "lucaszg-drawio-importacao:src/001_EditorUi_prototype_validateFileData.js",
        "name": "001_EditorUi_prototype_validateFileData.js",
        "qualifier": "FIL",
        "path": "src/001_EditorUi_prototype_validateFileData.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "lucaszg-drawio-importacao:src/002_EditorUi_prototype_setFileData.js",
        "name": "002_EditorUi_prototype_setFileData.js",
        "qualifier": "FIL",
        "path": "src/002_EditorUi_prototype_setFileData.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "lucaszg-drawio-importacao:src/003_EditorUi_prototype_openFiles.js",
        "name": "003_EditorUi_prototype_openFiles.js",
        "qualifier": "FIL",
        "path": "src/003_EditorUi_prototype_openFiles.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "lucaszg-drawio-importacao:src/004_EditorUi_prototype_openFileHandle.js",
        "name": "004_EditorUi_prototype_openFileHandle.js",
        "qualifier": "FIL",
        "path": "src/004_EditorUi_prototype_openFileHandle.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "lucaszg-drawio-importacao:src/005_EditorUi_prototype_openLocalFile.js",
        "name": "005_EditorUi_prototype_openLocalFile.js",
        "qualifier": "FIL",
        "path": "src/005_EditorUi_prototype_openLocalFile.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "lucaszg-drawio-importacao:src/006_Editor_extractGraphModel.js",
        "name": "006_Editor_extractGraphModel.js",
        "qualifier": "FIL",
        "path": "src/006_Editor_extractGraphModel.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "lucaszg-drawio-importacao:src/007_Editor_prototype_extractGraphModel.js",
        "name": "007_Editor_prototype_extractGraphModel.js",
        "qualifier": "FIL",
        "path": "src/007_Editor_prototype_extractGraphModel.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "lucaszg-drawio-importacao:src/008_Editor_prototype_setGraphXml.js",
        "name": "008_Editor_prototype_setGraphXml.js",
        "qualifier": "FIL",
        "path": "src/008_Editor_prototype_setGraphXml.js",
        "language": "js"
      }
    ]
  },
  "medidas": {
    "component": {
      "id": "AaG8ICO1hQXxjEzKTtXg",
      "key": "lucaszg-drawio-importacao",
      "name": "lucaszg-drawio-importacao",
      "qualifier": "TRK",
      "measures": [
        {
          "metric": "functions",
          "value": "25"
        },
        {
          "metric": "cognitive_complexity",
          "value": "275",
          "bestValue": false
        }
      ]
    }
  },
  "commit": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3",
  "projeto": "lucaszg-drawio-importacao"
}
```

</details>


<a id="e2"></a>

### E2 — Rótulos

Projeto: `drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos`. [Painel](https://sonarcloud.io/dashboard?id=drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos). [Tarefa histórica](https://sonarcloud.io/api/ce/task?id=AaG8RPSTbE9rxH86FwoI). Análise: `4853c608-87f3-477c-ae03-18d6f2fab544`.

SHA-256 do snapshot JSON canônico: `c460abbe4af3072994aa35c5fc43fc57935b7484443f59077768b228381b3aad`.

<details markdown="1">
<summary>Abrir resposta preservada E2 (processamento, análise, inventário e medidas)</summary>

```json
{
  "task": {
    "task": {
      "id": "AaG8RPSTbE9rxH86FwoI",
      "type": "REPORT",
      "componentId": "AaG8KNDIyB6rxKezFVQE",
      "componentKey": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos",
      "componentName": "lucaszg-drawio-rotulos",
      "componentQualifier": "TRK",
      "analysisId": "4853c608-87f3-477c-ae03-18d6f2fab544",
      "status": "SUCCESS",
      "submittedAt": "2026-11-08T17:46:38+0000",
      "submitterLogin": "lucaszg-g-0JgHv@github",
      "startedAt": "2026-11-08T17:46:38+0000",
      "executedAt": "2026-11-08T17:46:49+0000",
      "executionTimeMs": 11633,
      "logs": false,
      "hasScannerContext": true,
      "organization": "drawio-sonarcloud-testes-qualidade",
      "warningCount": 0,
      "warnings": []
    }
  },
  "analysis": {
    "paging": {
      "pageIndex": 1,
      "pageSize": 1,
      "total": 2
    },
    "analyses": [
      {
        "key": "4853c608-87f3-477c-ae03-18d6f2fab544",
        "date": "2026-11-08T17:43:48+0000",
        "events": [
          {
            "key": "AaG8RSDmf0qErduKDB-d",
            "category": "VERSION",
            "name": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3"
          }
        ],
        "projectVersion": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3",
        "manualNewCodePeriodBaseline": false,
        "revision": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3"
      }
    ]
  },
  "arquivos": {
    "paging": {
      "pageIndex": 1,
      "pageSize": 500,
      "total": 20
    },
    "baseComponent": {
      "organization": "drawio-sonarcloud-testes-qualidade",
      "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos",
      "name": "lucaszg-drawio-rotulos",
      "qualifier": "TRK",
      "tags": [],
      "visibility": "public"
    },
    "components": [
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/001_Graph_prototype_cellLabelChanged.js",
        "name": "001_Graph_prototype_cellLabelChanged.js",
        "qualifier": "FIL",
        "path": "src/001_Graph_prototype_cellLabelChanged.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/002_Graph_prototype_getLabel.js",
        "name": "002_Graph_prototype_getLabel.js",
        "qualifier": "FIL",
        "path": "src/002_Graph_prototype_getLabel.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/003_mxCellEditor_prototype_isContentEditing.js",
        "name": "003_mxCellEditor_prototype_isContentEditing.js",
        "qualifier": "FIL",
        "path": "src/003_mxCellEditor_prototype_isContentEditing.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/004_mxCellEditor_prototype_insertTab.js",
        "name": "004_mxCellEditor_prototype_insertTab.js",
        "qualifier": "FIL",
        "path": "src/004_mxCellEditor_prototype_insertTab.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/005_mxCellEditor_prototype_alignText.js",
        "name": "005_mxCellEditor_prototype_alignText.js",
        "qualifier": "FIL",
        "path": "src/005_mxCellEditor_prototype_alignText.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/006_mxCellEditor_prototype_saveSelection.js",
        "name": "006_mxCellEditor_prototype_saveSelection.js",
        "qualifier": "FIL",
        "path": "src/006_mxCellEditor_prototype_saveSelection.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/007_mxCellEditor_prototype_restoreSelection.js",
        "name": "007_mxCellEditor_prototype_restoreSelection.js",
        "qualifier": "FIL",
        "path": "src/007_mxCellEditor_prototype_restoreSelection.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/008_mxCellEditor_prototype_startEditing.js",
        "name": "008_mxCellEditor_prototype_startEditing.js",
        "qualifier": "FIL",
        "path": "src/008_mxCellEditor_prototype_startEditing.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/009_mxCellEditor_prototype_toggleViewMode.js",
        "name": "009_mxCellEditor_prototype_toggleViewMode.js",
        "qualifier": "FIL",
        "path": "src/009_mxCellEditor_prototype_toggleViewMode.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/010_mxCellEditor_prototype_resize.js",
        "name": "010_mxCellEditor_prototype_resize.js",
        "qualifier": "FIL",
        "path": "src/010_mxCellEditor_prototype_resize.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/011_mxCellEditor_prototype_getInitialValue.js",
        "name": "011_mxCellEditor_prototype_getInitialValue.js",
        "qualifier": "FIL",
        "path": "src/011_mxCellEditor_prototype_getInitialValue.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/012_mxCellEditor_prototype_setEditingValue.js",
        "name": "012_mxCellEditor_prototype_setEditingValue.js",
        "qualifier": "FIL",
        "path": "src/012_mxCellEditor_prototype_setEditingValue.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/013_mxCellEditor_prototype_getCurrentValue.js",
        "name": "013_mxCellEditor_prototype_getCurrentValue.js",
        "qualifier": "FIL",
        "path": "src/013_mxCellEditor_prototype_getCurrentValue.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/014_mxCellEditor_prototype_stopEditing.js",
        "name": "014_mxCellEditor_prototype_stopEditing.js",
        "qualifier": "FIL",
        "path": "src/014_mxCellEditor_prototype_stopEditing.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/015_mxCellEditor_prototype_applyValue.js",
        "name": "015_mxCellEditor_prototype_applyValue.js",
        "qualifier": "FIL",
        "path": "src/015_mxCellEditor_prototype_applyValue.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/016_TextFormatPanel.js",
        "name": "016_TextFormatPanel.js",
        "qualifier": "FIL",
        "path": "src/016_TextFormatPanel.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/017_TextFormatPanel_prototype_init.js",
        "name": "017_TextFormatPanel_prototype_init.js",
        "qualifier": "FIL",
        "path": "src/017_TextFormatPanel_prototype_init.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/018_TextFormatPanel_prototype_addFontOps.js",
        "name": "018_TextFormatPanel_prototype_addFontOps.js",
        "qualifier": "FIL",
        "path": "src/018_TextFormatPanel_prototype_addFontOps.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/019_TextFormatPanel_prototype_createLabelBackgroundOption.js",
        "name": "019_TextFormatPanel_prototype_createLabelBackgroundOption.js",
        "qualifier": "FIL",
        "path": "src/019_TextFormatPanel_prototype_createLabelBackgroundOption.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/020_TextFormatPanel_prototype_addFont.js",
        "name": "020_TextFormatPanel_prototype_addFont.js",
        "qualifier": "FIL",
        "path": "src/020_TextFormatPanel_prototype_addFont.js",
        "language": "js"
      }
    ]
  },
  "medidas": {
    "component": {
      "id": "AaG8KNDIyB6rxKezFVQE",
      "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos",
      "name": "lucaszg-drawio-rotulos",
      "qualifier": "TRK",
      "measures": [
        {
          "metric": "functions",
          "value": "116"
        },
        {
          "metric": "cognitive_complexity",
          "value": "1057",
          "bestValue": false
        }
      ]
    }
  },
  "commit": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3",
  "projeto": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos"
}
```

</details>


<a id="e3"></a>

### E3 — Exportação PNG/PDF/SVG

Projeto: `drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao`. [Painel](https://sonarcloud.io/dashboard?id=drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao). [Tarefa histórica](https://sonarcloud.io/api/ce/task?id=AaG8OkuaYN-65yNNqmQN). Análise: `932752e9-e32c-4e9f-877f-b208641f4374`.

SHA-256 do snapshot JSON canônico: `f2db1046bd89335f12c3c57c74f4de255e144c6617ef9f71099adeb53f2123e3`.

<details markdown="1">
<summary>Abrir resposta preservada E3 (processamento, análise, inventário e medidas)</summary>

```json
{
  "task": {
    "task": {
      "id": "AaG8OkuaYN-65yNNqmQN",
      "type": "REPORT",
      "componentId": "AaG8KdfFhQXxjEzKTtmb",
      "componentKey": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao",
      "componentName": "lucaszg-drawio-exportacao",
      "componentQualifier": "TRK",
      "analysisId": "932752e9-e32c-4e9f-877f-b208641f4374",
      "status": "SUCCESS",
      "submittedAt": "2026-11-08T17:34:59+0000",
      "submitterLogin": "lucaszg-g-0JgHv@github",
      "startedAt": "2026-11-08T17:35:00+0000",
      "executedAt": "2026-11-08T17:35:01+0000",
      "executionTimeMs": 1358,
      "logs": false,
      "hasScannerContext": true,
      "organization": "drawio-sonarcloud-testes-qualidade",
      "warningCount": 0,
      "warnings": []
    }
  },
  "analysis": {
    "paging": {
      "pageIndex": 1,
      "pageSize": 1,
      "total": 1
    },
    "analyses": [
      {
        "key": "932752e9-e32c-4e9f-877f-b208641f4374",
        "date": "2026-11-08T17:34:06+0000",
        "events": [
          {
            "key": "AaG8OlH2tq8cOF-nkSF3",
            "category": "VERSION",
            "name": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3"
          }
        ],
        "projectVersion": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3",
        "manualNewCodePeriodBaseline": false,
        "revision": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3"
      }
    ]
  },
  "arquivos": {
    "paging": {
      "pageIndex": 1,
      "pageSize": 500,
      "total": 13
    },
    "baseComponent": {
      "organization": "drawio-sonarcloud-testes-qualidade",
      "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao",
      "name": "lucaszg-drawio-exportacao",
      "qualifier": "TRK",
      "tags": [],
      "visibility": "public"
    },
    "components": [
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/001_EditorUi_prototype_downloadFile.js",
        "name": "001_EditorUi_prototype_downloadFile.js",
        "qualifier": "FIL",
        "path": "src/001_EditorUi_prototype_downloadFile.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/002_EditorUi_prototype_createDownloadRequest.js",
        "name": "002_EditorUi_prototype_createDownloadRequest.js",
        "qualifier": "FIL",
        "path": "src/002_EditorUi_prototype_createDownloadRequest.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/003_EditorUi_prototype_downloadRequestBuilder.js",
        "name": "003_EditorUi_prototype_downloadRequestBuilder.js",
        "qualifier": "FIL",
        "path": "src/003_EditorUi_prototype_downloadRequestBuilder.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/004_EditorUi_prototype_exportSvg.js",
        "name": "004_EditorUi_prototype_exportSvg.js",
        "qualifier": "FIL",
        "path": "src/004_EditorUi_prototype_exportSvg.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/005_EditorUi_prototype_exportImage.js",
        "name": "005_EditorUi_prototype_exportImage.js",
        "qualifier": "FIL",
        "path": "src/005_EditorUi_prototype_exportImage.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/006_EditorUi_prototype_showExportDialog.js",
        "name": "006_EditorUi_prototype_showExportDialog.js",
        "qualifier": "FIL",
        "path": "src/006_EditorUi_prototype_showExportDialog.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/007_EditorUi_prototype_showRemoteExportDialog.js",
        "name": "007_EditorUi_prototype_showRemoteExportDialog.js",
        "qualifier": "FIL",
        "path": "src/007_EditorUi_prototype_showRemoteExportDialog.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/008_ExportDialog_exportFile.js",
        "name": "008_ExportDialog_exportFile.js",
        "qualifier": "FIL",
        "path": "src/008_ExportDialog_exportFile.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/009_Editor_prototype_exportToCanvas.js",
        "name": "009_Editor_prototype_exportToCanvas.js",
        "qualifier": "FIL",
        "path": "src/009_Editor_prototype_exportToCanvas.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/010_Graph_prototype_getSvg.js",
        "name": "010_Graph_prototype_getSvg.js",
        "qualifier": "FIL",
        "path": "src/010_Graph_prototype_getSvg.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/011_Graph_prototype_getSvg.js",
        "name": "011_Graph_prototype_getSvg.js",
        "qualifier": "FIL",
        "path": "src/011_Graph_prototype_getSvg.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/012_Graph_prototype_createSvgImageExport.js",
        "name": "012_Graph_prototype_createSvgImageExport.js",
        "qualifier": "FIL",
        "path": "src/012_Graph_prototype_createSvgImageExport.js",
        "language": "js"
      },
      {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao:src/013_Graph_prototype_createSvgCanvas.js",
        "name": "013_Graph_prototype_createSvgCanvas.js",
        "qualifier": "FIL",
        "path": "src/013_Graph_prototype_createSvgCanvas.js",
        "language": "js"
      }
    ]
  },
  "medidas": {
    "component": {
      "id": "AaG8KdfFhQXxjEzKTtmb",
      "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao",
      "name": "lucaszg-drawio-exportacao",
      "qualifier": "TRK",
      "measures": [
        {
          "metric": "duplicated_lines",
          "value": "28",
          "bestValue": false
        },
        {
          "metric": "lines",
          "value": "2846"
        }
      ]
    }
  },
  "commit": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3",
  "projeto": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao"
}
```

</details>


<a id="e4"></a>

### E4 — Manifesto final e localização no código

Os intervalos são inclusivos. A coluna Arquivo identifica o módulo original; o link da assinatura aponta para suas linhas na revisão medida. O JSON contém os nomes dos arquivos enviados ao scanner e os hashes de cada recorte.

#### Importação

| Assinatura selecionada | Arquivo | Linhas |
| --- | --- | --- |
| [`EditorUi.prototype.validateFileData`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L2376-L2393) | `diagramly/EditorUi.js` | 2376–2393 |
| [`EditorUi.prototype.setFileData`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L3665-L3811) | `diagramly/EditorUi.js` | 3665–3811 |
| [`EditorUi.prototype.openFiles`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L30138-L30181) | `diagramly/EditorUi.js` | 30138–30181 |
| [`EditorUi.prototype.openFileHandle`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L29978-L30133) | `diagramly/EditorUi.js` | 29978–30133 |
| [`EditorUi.prototype.openLocalFile`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L30186-L30273) | `diagramly/EditorUi.js` | 30186–30273 |
| [`Editor.extractGraphModel`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/Editor.js#L2597-L2703) | `diagramly/Editor.js` | 2597–2703 |
| [`Editor.prototype.extractGraphModel`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/Editor.js#L4913-L4916) | `diagramly/Editor.js` | 4913–4916 |
| [`Editor.prototype.setGraphXml`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/Editor.js#L4719-L4820) | `diagramly/Editor.js` | 4719–4820 |

#### Rótulos

| Assinatura selecionada | Arquivo | Linhas |
| --- | --- | --- |
| [`Graph.prototype.cellLabelChanged`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L38187-L38244) | `grapheditor/Graph.js` | 38187–38244 |
| [`Graph.prototype.getLabel`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L15784-L15805) | `grapheditor/Graph.js` | 15784–15805 |
| [`mxCellEditor.prototype.isContentEditing`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L45120-L45125) | `grapheditor/Graph.js` | 45120–45125 |
| [`mxCellEditor.prototype.insertTab`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L45195-L45207) | `grapheditor/Graph.js` | 45195–45207 |
| [`mxCellEditor.prototype.alignText`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L45217-L45258) | `grapheditor/Graph.js` | 45217–45258 |
| [`mxCellEditor.prototype.saveSelection`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L45263-L45287) | `grapheditor/Graph.js` | 45263–45287 |
| [`mxCellEditor.prototype.restoreSelection`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L45292-L45318) | `grapheditor/Graph.js` | 45292–45318 |
| [`mxCellEditor.prototype.startEditing`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L46070-L46152) | `grapheditor/Graph.js` | 46070–46152 |
| [`mxCellEditor.prototype.toggleViewMode`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L46154-L46293) | `grapheditor/Graph.js` | 46154–46293 |
| [`mxCellEditor.prototype.resize`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L46296-L46571) | `grapheditor/Graph.js` | 46296–46571 |
| [`mxCellEditor.prototype.getInitialValue`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L46607-L46624) | `grapheditor/Graph.js` | 46607–46624 |
| [`mxCellEditor.prototype.setEditingValue`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L46627-L46644) | `grapheditor/Graph.js` | 46627–46644 |
| [`mxCellEditor.prototype.getCurrentValue`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L46647-L46700) | `grapheditor/Graph.js` | 46647–46700 |
| [`mxCellEditor.prototype.stopEditing`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L46703-L46752) | `grapheditor/Graph.js` | 46703–46752 |
| [`mxCellEditor.prototype.applyValue`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L46767-L46787) | `grapheditor/Graph.js` | 46767–46787 |
| [`TextFormatPanel`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Format.js#L4683-L4687) | `grapheditor/Format.js` | 4683–4687 |
| [`TextFormatPanel.prototype.init`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Format.js#L4694-L4698) | `grapheditor/Format.js` | 4694–4698 |
| [`TextFormatPanel.prototype.addFontOps`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Format.js#L4704-L4755) | `grapheditor/Format.js` | 4704–4755 |
| [`TextFormatPanel.prototype.createLabelBackgroundOption`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Format.js#L4769-L4865) | `grapheditor/Format.js` | 4769–4865 |
| [`TextFormatPanel.prototype.addFont`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Format.js#L4955-L6831) | `grapheditor/Format.js` | 4955–6831 |

#### Exportação PNG/PDF/SVG

| Assinatura selecionada | Arquivo | Linhas |
| --- | --- | --- |
| [`EditorUi.prototype.downloadFile`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L3977-L4128) | `diagramly/EditorUi.js` | 3977–4128 |
| [`EditorUi.prototype.createDownloadRequest`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L4131-L4151) | `diagramly/EditorUi.js` | 4131–4151 |
| [`EditorUi.prototype.downloadRequestBuilder`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L4158-L4279) | `diagramly/EditorUi.js` | 4158–4279 |
| [`EditorUi.prototype.exportSvg`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L9307-L9560) | `diagramly/EditorUi.js` | 9307–9560 |
| [`EditorUi.prototype.exportImage`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L13341-L13448) | `diagramly/EditorUi.js` | 13341–13448 |
| [`EditorUi.prototype.showExportDialog`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L11399-L12342) | `diagramly/EditorUi.js` | 11399–12342 |
| [`EditorUi.prototype.showRemoteExportDialog`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L11015-L11102) | `diagramly/EditorUi.js` | 11015–11102 |
| [`ExportDialog.exportFile`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/EditorUi.js#L39407-L39480) | `diagramly/EditorUi.js` | 39407–39480 |
| [`Editor.prototype.exportToCanvas`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/Editor.js#L7075-L7341) | `diagramly/Editor.js` | 7075–7341 |
| [`Graph.prototype.getSvg`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/diagramly/Editor.js#L10731-L10821) | `diagramly/Editor.js` | 10731–10821 |
| [`Graph.prototype.getSvg`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L40861-L41289) | `grapheditor/Graph.js` | 40861–41289 |
| [`Graph.prototype.createSvgImageExport`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L40569-L40831) | `grapheditor/Graph.js` | 40569–40831 |
| [`Graph.prototype.createSvgCanvas`](https://github.com/H3ytt0r10/drawio/blob/c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3/src/main/webapp/js/grapheditor/Graph.js#L41396-L41415) | `grapheditor/Graph.js` | 41396–41415 |

SHA-256 do manifesto JSON canônico: `7f6525111dc43d13c24676185d7da9eb5f16f10b2acfae4c60daf84b04ee8f24`.

<details markdown="1">
<summary>Abrir manifesto final recortes.json para auditoria e reprodução</summary>

```json
{
  "commit": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3",
  "versao": "32.6.10",
  "referencia_commit": "c41e8cb60d0e7ffe776a94ae24c58115f7c59f26",
  "componentes": {
    "importacao": [
      {
        "recorte": "src/001_EditorUi_prototype_validateFileData.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.validateFileData",
        "inicio": 2376,
        "fim": 2393,
        "sha256_lf": "1427aba8fdc0c4216760c6542e93b086422c35ef1d426c617a77335004a304d6"
      },
      {
        "recorte": "src/002_EditorUi_prototype_setFileData.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.setFileData",
        "inicio": 3665,
        "fim": 3811,
        "sha256_lf": "a2dddea043b711e3354b50b80f25f3447259bc221f95df82483790529f9ffce4"
      },
      {
        "recorte": "src/003_EditorUi_prototype_openFiles.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.openFiles",
        "inicio": 30138,
        "fim": 30181,
        "sha256_lf": "07bf1ae7d986f3f76b75df41cb85503b41b3533b65f0971aa4fc8d4044fdd8e8"
      },
      {
        "recorte": "src/004_EditorUi_prototype_openFileHandle.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.openFileHandle",
        "inicio": 29978,
        "fim": 30133,
        "sha256_lf": "f02adf7f6a97c9e047a6f03eb3d0b7cc5d4c37b3ccc889556457ebac5f1c7120"
      },
      {
        "recorte": "src/005_EditorUi_prototype_openLocalFile.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.openLocalFile",
        "inicio": 30186,
        "fim": 30273,
        "sha256_lf": "3c683d0fb2bae3814c1c8e86d9a0a30433a78ec4cda0c9dcd4f738c91dfd79bd"
      },
      {
        "recorte": "src/006_Editor_extractGraphModel.js",
        "arquivo": "src/main/webapp/js/diagramly/Editor.js",
        "assinatura": "Editor.extractGraphModel",
        "inicio": 2597,
        "fim": 2703,
        "sha256_lf": "02fd6ca494d9b7acc63c590b9f3be1612f84d2dc55d2eca5373ea0c4833da52d"
      },
      {
        "recorte": "src/007_Editor_prototype_extractGraphModel.js",
        "arquivo": "src/main/webapp/js/diagramly/Editor.js",
        "assinatura": "Editor.prototype.extractGraphModel",
        "inicio": 4913,
        "fim": 4916,
        "sha256_lf": "6d18dadfa83a2589894c941cf646d652975e7c80b5de32a79ca15eeaa74f0167"
      },
      {
        "recorte": "src/008_Editor_prototype_setGraphXml.js",
        "arquivo": "src/main/webapp/js/diagramly/Editor.js",
        "assinatura": "Editor.prototype.setGraphXml",
        "inicio": 4719,
        "fim": 4820,
        "sha256_lf": "ef8d11f29f1645e17ad4c27799e013bd98c403893b541d2c5cbca7ff3aa11b23"
      }
    ],
    "rotulos": [
      {
        "recorte": "src/001_Graph_prototype_cellLabelChanged.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "Graph.prototype.cellLabelChanged",
        "inicio": 38187,
        "fim": 38244,
        "sha256_lf": "e0b6b26d345075b2636228698c49319f5db72f703a5731053f9a0e9558071ee1"
      },
      {
        "recorte": "src/002_Graph_prototype_getLabel.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "Graph.prototype.getLabel",
        "inicio": 15784,
        "fim": 15805,
        "sha256_lf": "df99254146c062c711cceabe519847f7fe060f088b69068f623e74335b081f82"
      },
      {
        "recorte": "src/003_mxCellEditor_prototype_isContentEditing.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.isContentEditing",
        "inicio": 45120,
        "fim": 45125,
        "sha256_lf": "c41e081134f201ed0826f4548f351c7bac7beca2b7f1a25355218e0a5880fbe6"
      },
      {
        "recorte": "src/004_mxCellEditor_prototype_insertTab.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.insertTab",
        "inicio": 45195,
        "fim": 45207,
        "sha256_lf": "27217ee4fce92fa2176e3e768ddee8d49498fcdb5a42a754f130120061eb9a9b"
      },
      {
        "recorte": "src/005_mxCellEditor_prototype_alignText.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.alignText",
        "inicio": 45217,
        "fim": 45258,
        "sha256_lf": "41e5b13c2b1c8087e9d2cc54b2c2aedd3209f141de0e7505d31a7f9b986ef131"
      },
      {
        "recorte": "src/006_mxCellEditor_prototype_saveSelection.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.saveSelection",
        "inicio": 45263,
        "fim": 45287,
        "sha256_lf": "dda28cdd9753f9e7d27d4974591d0b49b84515aec6ac81a4212175eec3f48741"
      },
      {
        "recorte": "src/007_mxCellEditor_prototype_restoreSelection.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.restoreSelection",
        "inicio": 45292,
        "fim": 45318,
        "sha256_lf": "e087845a46c65e4cd21def88c12d5eb829727fa8b08905354a970ab6ee21af1e"
      },
      {
        "recorte": "src/008_mxCellEditor_prototype_startEditing.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.startEditing",
        "inicio": 46070,
        "fim": 46152,
        "sha256_lf": "a323e188e3d45a753eb96e745e4d0690bfba866968c318944ef2ea2a7bcd8196"
      },
      {
        "recorte": "src/009_mxCellEditor_prototype_toggleViewMode.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.toggleViewMode",
        "inicio": 46154,
        "fim": 46293,
        "sha256_lf": "309cd0ec8366b5e5738d1d825696ab28f3889503d9d7767a656d9d3cf7c568c9"
      },
      {
        "recorte": "src/010_mxCellEditor_prototype_resize.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.resize",
        "inicio": 46296,
        "fim": 46571,
        "sha256_lf": "996408c52dd0745194b882a9a1ead9edba384b42c5b7abc61da0eab19d8237ed"
      },
      {
        "recorte": "src/011_mxCellEditor_prototype_getInitialValue.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.getInitialValue",
        "inicio": 46607,
        "fim": 46624,
        "sha256_lf": "92fe4c69d76657e5bf2590c72aec7237ebb7e22ff888ea938cff413d9fc1b9f0"
      },
      {
        "recorte": "src/012_mxCellEditor_prototype_setEditingValue.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.setEditingValue",
        "inicio": 46627,
        "fim": 46644,
        "sha256_lf": "7082cfb62791452b9d9061b5b94adfe922e301da0850b346526f8af57e24baaf"
      },
      {
        "recorte": "src/013_mxCellEditor_prototype_getCurrentValue.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.getCurrentValue",
        "inicio": 46647,
        "fim": 46700,
        "sha256_lf": "e6f753ad6da90555d90e64685c60e5961fad1519bceaa25c9a86c8dcdc4016eb"
      },
      {
        "recorte": "src/014_mxCellEditor_prototype_stopEditing.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.stopEditing",
        "inicio": 46703,
        "fim": 46752,
        "sha256_lf": "39ffe6b06a4aac1ec1550cac8be9f6dafa2e161b568c1a5806d6a2a953217a51"
      },
      {
        "recorte": "src/015_mxCellEditor_prototype_applyValue.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "mxCellEditor.prototype.applyValue",
        "inicio": 46767,
        "fim": 46787,
        "sha256_lf": "796f3a5aeaa0d119f0dd59f0a190d8c20efbfde7ccf93df1d84b1a2fba9b6ade"
      },
      {
        "recorte": "src/016_TextFormatPanel.js",
        "arquivo": "src/main/webapp/js/grapheditor/Format.js",
        "assinatura": "TextFormatPanel",
        "inicio": 4683,
        "fim": 4687,
        "sha256_lf": "004290789f2eee7768fdbe029bef86d022ffb1ef35bcdd0f62e50bd69fb12f26"
      },
      {
        "recorte": "src/017_TextFormatPanel_prototype_init.js",
        "arquivo": "src/main/webapp/js/grapheditor/Format.js",
        "assinatura": "TextFormatPanel.prototype.init",
        "inicio": 4694,
        "fim": 4698,
        "sha256_lf": "e99855f0114ae6f37c9c691b9289cb51e7c09af9767b899bfd3be19548912865"
      },
      {
        "recorte": "src/018_TextFormatPanel_prototype_addFontOps.js",
        "arquivo": "src/main/webapp/js/grapheditor/Format.js",
        "assinatura": "TextFormatPanel.prototype.addFontOps",
        "inicio": 4704,
        "fim": 4755,
        "sha256_lf": "9dee6d8d3407ad4c53112127b044e84070f1d33fb387204f3789c0965853dc25"
      },
      {
        "recorte": "src/019_TextFormatPanel_prototype_createLabelBackgroundOption.js",
        "arquivo": "src/main/webapp/js/grapheditor/Format.js",
        "assinatura": "TextFormatPanel.prototype.createLabelBackgroundOption",
        "inicio": 4769,
        "fim": 4865,
        "sha256_lf": "82f1241f02aff43e2fe0370f7b4be1dd6241c6e96ef6012e59e3b9950b3ae432"
      },
      {
        "recorte": "src/020_TextFormatPanel_prototype_addFont.js",
        "arquivo": "src/main/webapp/js/grapheditor/Format.js",
        "assinatura": "TextFormatPanel.prototype.addFont",
        "inicio": 4955,
        "fim": 6831,
        "sha256_lf": "1c21e2a5499ffd425cd7aaa971d90e04429e919b5f2530fc2fe12ada0edbf54e"
      }
    ],
    "exportacao": [
      {
        "recorte": "src/001_EditorUi_prototype_downloadFile.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.downloadFile",
        "inicio": 3977,
        "fim": 4128,
        "sha256_lf": "b3747b046df02cbe94b8f32f87c7b74b533648b52a4f911c72d25ed43576ee8a"
      },
      {
        "recorte": "src/002_EditorUi_prototype_createDownloadRequest.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.createDownloadRequest",
        "inicio": 4131,
        "fim": 4151,
        "sha256_lf": "510bb269e65737450e36dbdf0dada4958aeeb31a600102c744f1c24a409d62d8"
      },
      {
        "recorte": "src/003_EditorUi_prototype_downloadRequestBuilder.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.downloadRequestBuilder",
        "inicio": 4158,
        "fim": 4279,
        "sha256_lf": "4ebd7b4530564022312616abb371c6ace7fb14cc480bfb76e6c5a59261b7c74c"
      },
      {
        "recorte": "src/004_EditorUi_prototype_exportSvg.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.exportSvg",
        "inicio": 9307,
        "fim": 9560,
        "sha256_lf": "24f0aeca6f480e8ac44313863ef85021c1e4854a2456831bd559c66339724a2f"
      },
      {
        "recorte": "src/005_EditorUi_prototype_exportImage.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.exportImage",
        "inicio": 13341,
        "fim": 13448,
        "sha256_lf": "f3c1f865b90558f5e8c9e6f010a4dfb72302d2b0a3ac381b0ce577cdf8a2b90a"
      },
      {
        "recorte": "src/006_EditorUi_prototype_showExportDialog.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.showExportDialog",
        "inicio": 11399,
        "fim": 12342,
        "sha256_lf": "37d18cf158a1521dc656a4851f7e832aa91efe9194ee741b07310513082740f0"
      },
      {
        "recorte": "src/007_EditorUi_prototype_showRemoteExportDialog.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "EditorUi.prototype.showRemoteExportDialog",
        "inicio": 11015,
        "fim": 11102,
        "sha256_lf": "69f2986eda5b1220775adae8e0d8cefccca7cc305763ec502ef05e1d52c2c3d3"
      },
      {
        "recorte": "src/008_ExportDialog_exportFile.js",
        "arquivo": "src/main/webapp/js/diagramly/EditorUi.js",
        "assinatura": "ExportDialog.exportFile",
        "inicio": 39407,
        "fim": 39480,
        "sha256_lf": "e22367d07575b86352b3c3963a02960375f9cd6e31172d018b37c0f0776630ef"
      },
      {
        "recorte": "src/009_Editor_prototype_exportToCanvas.js",
        "arquivo": "src/main/webapp/js/diagramly/Editor.js",
        "assinatura": "Editor.prototype.exportToCanvas",
        "inicio": 7075,
        "fim": 7341,
        "sha256_lf": "23f9e6629a3f572c16450b0ae0ac2a3f019390f11b29b22ffe6861bbb801e405"
      },
      {
        "recorte": "src/010_Graph_prototype_getSvg.js",
        "arquivo": "src/main/webapp/js/diagramly/Editor.js",
        "assinatura": "Graph.prototype.getSvg",
        "inicio": 10731,
        "fim": 10821,
        "sha256_lf": "98c032adf73447a3a38733f972fbcbef3dd3835e95052c4e82c1d666ebc4be56"
      },
      {
        "recorte": "src/011_Graph_prototype_getSvg.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "Graph.prototype.getSvg",
        "inicio": 40861,
        "fim": 41289,
        "sha256_lf": "9f9e784247fb31fb90eca11de047d3b9bb1cf7dd103033e5e431f3e1ccc059ea"
      },
      {
        "recorte": "src/012_Graph_prototype_createSvgImageExport.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "Graph.prototype.createSvgImageExport",
        "inicio": 40569,
        "fim": 40831,
        "sha256_lf": "8a320b0dd12892bc045dfceb3ab871fa1bd7c7065c44f844942db6b4617b897c"
      },
      {
        "recorte": "src/013_Graph_prototype_createSvgCanvas.js",
        "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
        "assinatura": "Graph.prototype.createSvgCanvas",
        "inicio": 41396,
        "fim": 41415,
        "sha256_lf": "81724def52ce6d9692508ce4b40afcd2ea5cc26b6c8ee79b4225e5ef1d860ea2"
      }
    ]
  }
}
```

</details>


<a id="e5"></a>

### E5 — Evidência da sobreposição e resultado de rótulos substituído

A resposta original permanece registrada para explicar a retificação, sem compor o resultado final. Os dois intervalos abaixo compartilham as linhas 46154–46293 do mesmo arquivo. O manifesto final E4 elimina essa interseção.

SHA-256 do registro histórico JSON canônico: `06d3043b5a30d30ab04dce73cde864cfa0d9724d746c43c14affd0cd50e3f911`.

<details markdown="1">
<summary>Abrir seleção sobreposta e snapshot da análise original de rótulos</summary>

```json
{
  "natureza": "registro original invalidado para julgamento final de Q3.2",
  "intervalos_sobrepostos": [
    {
      "recorte": "src/008_mxCellEditor_prototype_startEditing.js",
      "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
      "assinatura": "mxCellEditor.prototype.startEditing",
      "inicio": 46070,
      "fim": 46293,
      "sha256_lf": "e207ea27848fc0137722305ab1caab7877f34dc8543132fbf86a8cc8cb88ba5d"
    },
    {
      "recorte": "src/009_mxCellEditor_prototype_toggleViewMode.js",
      "arquivo": "src/main/webapp/js/grapheditor/Graph.js",
      "assinatura": "mxCellEditor.prototype.toggleViewMode",
      "inicio": 46154,
      "fim": 46293,
      "sha256_lf": "309cd0ec8366b5e5738d1d825696ab28f3889503d9d7767a656d9d3cf7c568c9"
    }
  ],
  "snapshot_original": {
    "task": {
      "task": {
        "id": "AaG8ONAbYN-65yNNqmNu",
        "type": "REPORT",
        "componentId": "AaG8KNDIyB6rxKezFVQE",
        "componentKey": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos",
        "componentName": "lucaszg-drawio-rotulos",
        "componentQualifier": "TRK",
        "analysisId": "0818a1d8-7c02-44c1-8d87-8f1e44ba7756",
        "status": "SUCCESS",
        "submittedAt": "2026-11-08T17:33:22+0000",
        "submitterLogin": "lucaszg-g-0JgHv@github",
        "startedAt": "2026-11-08T17:33:22+0000",
        "executedAt": "2026-11-08T17:33:24+0000",
        "executionTimeMs": 1789,
        "logs": false,
        "hasScannerContext": true,
        "organization": "drawio-sonarcloud-testes-qualidade",
        "warningCount": 0,
        "warnings": []
      }
    },
    "analysis": {
      "paging": {
        "pageIndex": 1,
        "pageSize": 1,
        "total": 1
      },
      "analyses": [
        {
          "key": "0818a1d8-7c02-44c1-8d87-8f1e44ba7756",
          "date": "2026-11-08T17:32:27+0000",
          "events": [
            {
              "key": "AaG8ONYff0qErduKCX35",
              "category": "VERSION",
              "name": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3"
            }
          ],
          "projectVersion": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3",
          "manualNewCodePeriodBaseline": false,
          "revision": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3"
        }
      ]
    },
    "arquivos": {
      "paging": {
        "pageIndex": 1,
        "pageSize": 500,
        "total": 20
      },
      "baseComponent": {
        "organization": "drawio-sonarcloud-testes-qualidade",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos",
        "name": "lucaszg-drawio-rotulos",
        "qualifier": "TRK",
        "tags": [],
        "visibility": "public"
      },
      "components": [
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/001_Graph_prototype_cellLabelChanged.js",
          "name": "001_Graph_prototype_cellLabelChanged.js",
          "qualifier": "FIL",
          "path": "src/001_Graph_prototype_cellLabelChanged.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/002_Graph_prototype_getLabel.js",
          "name": "002_Graph_prototype_getLabel.js",
          "qualifier": "FIL",
          "path": "src/002_Graph_prototype_getLabel.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/003_mxCellEditor_prototype_isContentEditing.js",
          "name": "003_mxCellEditor_prototype_isContentEditing.js",
          "qualifier": "FIL",
          "path": "src/003_mxCellEditor_prototype_isContentEditing.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/004_mxCellEditor_prototype_insertTab.js",
          "name": "004_mxCellEditor_prototype_insertTab.js",
          "qualifier": "FIL",
          "path": "src/004_mxCellEditor_prototype_insertTab.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/005_mxCellEditor_prototype_alignText.js",
          "name": "005_mxCellEditor_prototype_alignText.js",
          "qualifier": "FIL",
          "path": "src/005_mxCellEditor_prototype_alignText.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/006_mxCellEditor_prototype_saveSelection.js",
          "name": "006_mxCellEditor_prototype_saveSelection.js",
          "qualifier": "FIL",
          "path": "src/006_mxCellEditor_prototype_saveSelection.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/007_mxCellEditor_prototype_restoreSelection.js",
          "name": "007_mxCellEditor_prototype_restoreSelection.js",
          "qualifier": "FIL",
          "path": "src/007_mxCellEditor_prototype_restoreSelection.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/008_mxCellEditor_prototype_startEditing.js",
          "name": "008_mxCellEditor_prototype_startEditing.js",
          "qualifier": "FIL",
          "path": "src/008_mxCellEditor_prototype_startEditing.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/009_mxCellEditor_prototype_toggleViewMode.js",
          "name": "009_mxCellEditor_prototype_toggleViewMode.js",
          "qualifier": "FIL",
          "path": "src/009_mxCellEditor_prototype_toggleViewMode.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/010_mxCellEditor_prototype_resize.js",
          "name": "010_mxCellEditor_prototype_resize.js",
          "qualifier": "FIL",
          "path": "src/010_mxCellEditor_prototype_resize.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/011_mxCellEditor_prototype_getInitialValue.js",
          "name": "011_mxCellEditor_prototype_getInitialValue.js",
          "qualifier": "FIL",
          "path": "src/011_mxCellEditor_prototype_getInitialValue.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/012_mxCellEditor_prototype_setEditingValue.js",
          "name": "012_mxCellEditor_prototype_setEditingValue.js",
          "qualifier": "FIL",
          "path": "src/012_mxCellEditor_prototype_setEditingValue.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/013_mxCellEditor_prototype_getCurrentValue.js",
          "name": "013_mxCellEditor_prototype_getCurrentValue.js",
          "qualifier": "FIL",
          "path": "src/013_mxCellEditor_prototype_getCurrentValue.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/014_mxCellEditor_prototype_stopEditing.js",
          "name": "014_mxCellEditor_prototype_stopEditing.js",
          "qualifier": "FIL",
          "path": "src/014_mxCellEditor_prototype_stopEditing.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/015_mxCellEditor_prototype_applyValue.js",
          "name": "015_mxCellEditor_prototype_applyValue.js",
          "qualifier": "FIL",
          "path": "src/015_mxCellEditor_prototype_applyValue.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/016_TextFormatPanel.js",
          "name": "016_TextFormatPanel.js",
          "qualifier": "FIL",
          "path": "src/016_TextFormatPanel.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/017_TextFormatPanel_prototype_init.js",
          "name": "017_TextFormatPanel_prototype_init.js",
          "qualifier": "FIL",
          "path": "src/017_TextFormatPanel_prototype_init.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/018_TextFormatPanel_prototype_addFontOps.js",
          "name": "018_TextFormatPanel_prototype_addFontOps.js",
          "qualifier": "FIL",
          "path": "src/018_TextFormatPanel_prototype_addFontOps.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/019_TextFormatPanel_prototype_createLabelBackgroundOption.js",
          "name": "019_TextFormatPanel_prototype_createLabelBackgroundOption.js",
          "qualifier": "FIL",
          "path": "src/019_TextFormatPanel_prototype_createLabelBackgroundOption.js",
          "language": "js"
        },
        {
          "organization": "drawio-sonarcloud-testes-qualidade",
          "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos:src/020_TextFormatPanel_prototype_addFont.js",
          "name": "020_TextFormatPanel_prototype_addFont.js",
          "qualifier": "FIL",
          "path": "src/020_TextFormatPanel_prototype_addFont.js",
          "language": "js"
        }
      ]
    },
    "medidas": {
      "component": {
        "id": "AaG8KNDIyB6rxKezFVQE",
        "key": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos",
        "name": "lucaszg-drawio-rotulos",
        "qualifier": "TRK",
        "measures": [
          {
            "metric": "functions",
            "value": "117"
          },
          {
            "metric": "cognitive_complexity",
            "value": "1113",
            "bestValue": false
          }
        ]
      }
    },
    "commit": "c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3",
    "projeto": "drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos"
  }
}
```

</details>


<a id="e6"></a>

### E6 — Registro de console do ambiente de análise

Transcrição dos trechos observados nas execuções. Este registro identifica o instrumento; não substitui as respostas do serviço em E1–E3. Os horários abaixo são os apresentados pelo console local.

```text
14:43:31.064 INFO  SonarScanner CLI 8.1.0.6389
14:43:31.071 INFO  Windows 11 10.0 amd64
14:43:36.541 INFO  Java 21.0.9 Eclipse Adoptium (64-bit)
14:34:22.332 INFO  Quality profile for js: Sonar way core
14:34:41.986 INFO  Plugin version: [14.4.0.46458]
```
