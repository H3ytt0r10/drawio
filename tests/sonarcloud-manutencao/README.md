# Avaliação de manutenibilidade com SonarCloud

Implementação restrita a **M3.1 e M3.2**, do objetivo G3 da equipe Mary Jackson. São análises estáticas, não testes funcionais de abrir, editar ou exportar. Não são acrescentados critérios de cobertura, bugs, segurança, desempenho, dívida técnica ou Quality Gate.

## Rastreabilidade e critérios

A referência foi consultada no commit `c41e8cb60d0e7ffe776a94ae24c58115f7c59f26`:

- [Métricas, seção Manutenibilidade](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-2/metricas.md).
- [Níveis e julgamento, seção Manutenibilidade](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-2/niveis-e-julgamento.md).
- [Objetivos, questões e hipóteses, G3](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-2/objetivos-questoes-hipoteses.md).
- [Delimitação do escopo](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-1/escopo.md) e [ambiente previsto](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/c41e8cb60d0e7ffe776a94ae24c58115f7c59f26/docs/fase-3/ambiente-drawio.md).

| Avaliação | Coleta SonarCloud | Cálculo | Adequado | Atenção | Crítico |
| --- | --- | --- | --- | --- | --- |
| Q3.1 / M3.1, importação | `cognitive_complexity` = C; `functions` = F | C / F | ≤ 10 | > 10 e ≤ 15 | > 15 |
| Q3.2 / M3.1, rótulos | `cognitive_complexity` = C; `functions` = F | C / F | ≤ 10 | > 10 e ≤ 15 | > 15 |
| Q3.3 / M3.2, exportação PNG/PDF/SVG conjunta | `duplicated_lines` = Ld; `lines` = Lt | 100 × Ld / Lt | ≤ 5% | > 5% e ≤ 10% | > 10% |

Os limites são preliminares, propostos pela equipe; não são exigências da ISO. Não existe regra de nota global G3. A página das hipóteses contém texto inclusivo e parênteses com `<`; esta implementação segue as faixas explícitas de **níveis e julgamento**, incluindo os valores 10 e 5%. Classifica-se o valor sem arredondamento; o Markdown exibe seis casas decimais, e o JSON preserva o valor calculado.

## Delimitação operacional

A referência ainda deixa a identificação dos arquivos/funções para a Fase 3. Portanto, [escopo.json](escopo.json) fixa uma seleção operacional para esta cópia, com assinaturas, linhas inclusivas e SHA-256 do conteúdo normalizado em LF. Essa seleção **não foi prescrita pela documentação** e deve ser revisada pela equipe antes de usar a medição para uma conclusão acadêmica sobre o componente inteiro.

| Componente | Trechos selecionados | Motivo |
| --- | --- | --- |
| Importação | 8 funções em `diagramly/EditorUi.js` e `diagramly/Editor.js` | Leitura local com FileReader (`openFiles`), encaminhamento (`openFileHandle`/`openLocalFile`), validação e substituição dos dados (`validateFileData`/`setFileData`), extração e instalação do modelo (`extractGraphModel`/`setGraphXml`). |
| Rótulos | 20 funções em `grapheditor/Graph.js` e `grapheditor/Format.js` | Leitura e aplicação do rótulo, início/fim da edição, valor HTML/texto, seleção, alinhamento, dimensionamento e painel de fonte/cor. |
| Exportação | 13 funções em `diagramly/EditorUi.js`, `diagramly/Editor.js` e `grapheditor/Graph.js` | Diálogos, montagem de requisição de download/exportação PDF, exportação PNG por canvas e geração SVG. Todas são analisadas juntas, permitindo duplicações entre formatos e arquivos. |

Não se incluem os arquivos inteiros `EditorUi.js`, `Graph.js` ou `Format.js`: isso misturaria milhares de linhas de funcionalidades externas ao recorte. Também não se incluem bibliotecas de terceiros, builds, plugins, importadores de outros formatos ou implementações de armazenamento em nuvem como componentes independentes.

O preparador copia **cada função inteira para um arquivo JS separado**, sem alterar seu corpo e sem inserir wrappers, comentários ou linhas vazias artificiais. Preserva funções anônimas/callbacks internos; F vem do SonarCloud e **não** é a contagem de assinaturas do manifesto. Os ramos compartilhados de uma função (por exemplo, outros formatos de exportação) são preservados para não modificar sua complexidade. O código de produção permanece intacto. `recortes.json` permite converter uma linha do recorte à original: `linha_original = inicio + linha_recorte - 1`.

Limites metodológicos:

- Trata-se de medição de **recortes**, não de toda a aplicação ou de todo o fechamento de dependências dos componentes. A separação de funções remove o contexto do módulo; deve-se conferir os avisos do analisador antes de aceitar os números. A complexidade agregada pode diferir da análise dos arquivos originais.
- A separação também pode deixar de reconhecer blocos duplicados que atravessem fronteiras entre funções. Não extrapolar M3.2 para os arquivos originais completos. A duplicação considera somente os recortes de exportação, em conjunto, com os limiares padrão do SonarCloud; não se ajustam os limiares CPD para produzir um resultado desejado.
- Lt corresponde a `lines` dos recortes, incluindo suas linhas em branco/comentários internos. Não usar `ncloc`, quantidade de tokens ou média de percentuais por arquivo como substitutos.
- Parte da exportação PDF usa o serviço indicado por `EXPORT_URL`; a implementação desse servidor não está incluída aqui. A medição do cliente não comprova a manutenibilidade desse servidor. O fluxo completo permanece parcialmente coberto.
- A instalação de referência está fixada em **32.2.0**, enquanto esta cópia informa **32.6.10** em `VERSION`. Não atribuir os resultados desta cópia à versão 32.2.0.
- Se o código mudar, a preparação recusa os hashes diferentes. Revise explicitamente assinaturas, linhas, hashes e justificativas antes de uma nova campanha. Não atualize hashes apenas para suprimir o erro.

## Preparar e validar localmente

Requisitos: Python 3.10+, Node.js e Git no PATH. Não há dependências Python externas nem execução do editor. Na raiz do repositório:

```powershell
python tests/sonarcloud-manutencao/avaliar.py preparar
```

O comando verifica a integridade dos recortes e executa `node --check` em cada um. Gera os arquivos de entrada em `.work/`, ignorada pelo Git, e grava a documentação em [resultados/sonarcloud-manutencao](../../resultados/sonarcloud-manutencao/README.md). **Preparar não executa o SonarCloud** e registra os três resultados como pendentes. Cada nova campanha substitui o relatório anterior; preserve os resultados de uma campanha medida antes de iniciar outra.

## Executar no SonarCloud

1. Criar uma conta e organização no [SonarCloud](https://sonarcloud.io), e três projetos distintos para importação, rótulos e exportação. Registrar as chaves reais, não apenas os nomes de exibição. Configurar análise por CI/CLI, desativando Automatic Analysis se estiver habilitada. Não reutilizar projetos com análises de arquivos inteiros ou com envios concorrentes durante esta coleta.
2. Instalar o [SonarScanner CLI](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/scanners/sonarscanner-cli) e disponibilizar `sonar-scanner` no PATH. Usar a região europeia (`https://sonarcloud.io`), fixada neste script.
3. Gerar um token com permissão de análise e leitura dos três projetos e configurar `SONAR_TOKEN` **fora dos arquivos versionados**, pelo ambiente local ou gerenciador de segredos. Não colar o token no chat nem incluí-lo em comandos registrados na documentação.
4. Configurar as demais variáveis com as chaves reais e executar:

```powershell
$env:SONAR_ORGANIZATION = 'chave-real-da-organizacao'
$env:SONAR_PROJECT_IMPORTACAO = 'chave-real-importacao'
$env:SONAR_PROJECT_ROTULOS = 'chave-real-rotulos'
$env:SONAR_PROJECT_EXPORTACAO = 'chave-real-exportacao'
python tests/sonarcloud-manutencao/avaliar.py executar
```

O script prepara novamente os recortes, executa um scanner por componente e espera o processamento remoto (até 10 minutos por projeto). Verifica o identificador da análise antes e depois de buscar as medidas para evitar misturar análises concorrentes. Falhas e métricas ausentes não são convertidas em zero nem em aprovação. Código de saída 0 indica coleta concluída; 2 indica configuração incompleta ou coleta inconclusiva, não um julgamento de qualidade. `Crítico` é um resultado válido de coleta e aparece no relatório.

Para os três projetos já criados nesta organização, existe um comando pronto que carrega `SONAR_TOKEN` do ambiente ou do usuário Windows atual, configura as chaves reais e usa o scanner portátil, se instalado:

```powershell
.\tests\sonarcloud-manutencao\executar.ps1
```

O envio dos 41 recortes para esses três destinos foi autorizado pelo usuário nesta conversa. O launcher usa o Java incluído no scanner. O provisionamento automático de JRE foi desativado (`sonar.scanner.skipJreProvisioning=true`) após uma falha de permissão na extração do JRE no Windows. Para executar diretamente o Python com outro scanner, forneça Java 21+ pelo PATH ou por `SONAR_SCANNER_JAVA_EXE_PATH`.

Somente as medidas da tabela são solicitadas pela coleta. O scanner pode produzir outras medidas e issues por padrão; elas não constituem avaliações adicionais neste trabalho e não são utilizadas no julgamento. Não se usa o Quality Gate padrão do projeto como resultado de G3.

## Artefatos

- `resultados/sonarcloud-manutencao/README.md`: relatório legível, com as três situações e os limites de validade.
- `resultados/sonarcloud-manutencao/resultados.json`: medidas, cálculos, classificações e identificação do código.
- `resultados/sonarcloud-manutencao/recortes.json`: vínculo entre cada entrada do scanner e o código original.
- `resultados/sonarcloud-manutencao/evidencias/*.json`: respostas brutas das medidas e identificação da análise, criadas **somente depois de uma coleta remota válida**. Arquivos antigos nessa pasta não demonstram sucesso da campanha atual: confira `analysis_id`, commit e situação no relatório atual.

Coleta remota concluída em 08/11/2026, após autorização explícita do usuário para o envio dos recortes aos três projetos. O comando [executar.ps1](executar.ps1) está configurado com as chaves reais e carrega a credencial sem exibi-la. O conteúdo está delimitado em [escopo.json](escopo.json) e mapeado em [recortes.json](../../resultados/sonarcloud-manutencao/recortes.json). A auditoria documental corrigiu uma sobreposição no recorte de startEditing e repetiu somente rótulos: o resultado válido passou de 9,512820512820513 para 9,112068965517242, mantendo a classificação Adequado. A preparação agora verifica ausência de sobreposição, e o instrumento desativa SCA em futuras coletas por não compor G3. Os três resultados válidos têm processamento SUCCESS. O [relatório portátil em arquivo único](../../resultados/sonarcloud-manutencao/RELATORIO_MANUTENIBILIDADE.md) inclui snapshots, manifesto, referências e histórico da retificação. As verificações locais e remotas estão registradas em [VALIDACAO.md](../../resultados/sonarcloud-manutencao/VALIDACAO.md).

As chaves técnicas das medidas e a fórmula de densidade estão documentadas pela [SonarSource](https://docs.sonarsource.com/sonarqube-server/user-guide/code-metrics/metrics-definition). O acesso às medidas usa a [Web API do SonarCloud](https://sonarcloud.io/web_api).
