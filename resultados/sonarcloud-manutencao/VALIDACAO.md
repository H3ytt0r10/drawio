# Validação local do instrumento

Data: 08/11/2026 (America/Sao_Paulo).

Código-base: `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, `VERSION` = `32.6.10`.
Ambiente: Windows/PowerShell, Python `3.14.0`, Node.js `v22.20.0`.

Esta página registra verificações da automação de coleta. Os dados sintéticos e mocks usados nessas verificações **não são medições do draw.io** e não foram usados para julgar Q3.1, Q3.2 ou Q3.3.

| Verificação | Resultado observado |
| --- | --- |
| `python tests/sonarcloud-manutencao/avaliar.py preparar` | Concluído; hashes e delimitações validados; `node --check` aprovado nos 41 recortes: 8 de importação, 20 de rótulos e 13 de exportação. As contagens são de recortes, não do denominador F do SonarCloud. |
| Limites de classificação | 15 verificações aprovadas, incluindo zero, limites inclusivos 10/15 e 5%/10% e valores imediatamente superiores. |
| Fórmulas com medidas sintéticas | 3 verificações aprovadas: C/F de importação e rótulos, e 100 × Ld/Lt de exportação. Inclui numerador zero válido. |
| Rejeição de entradas inválidas | 7 verificações aprovadas: denominador zero, medidas ausentes, NaN, valor negativo, contagem fracionária e Ld maior que Lt. Ausência de medida não é tratada como zero. |
| Coletor com API e scanner simulados | 4 cenários aprovados: coleta válida, medida ausente, análise concorrente e arquivo excluído do escopo remoto. Executados em diretório temporário; nenhuma chamada de rede ou resultado sintético persistido nesta pasta. |
| Execução sem configuração SonarCloud | `executar` retorna código 2 e preserva as três avaliações como pendentes, sem atribuir notas ou números. |
| `git diff --check` | Sem erros de espaço em branco nos arquivos rastreados. |

Total: 25 verificações de cálculo/classificação e 4 cenários simulados do coletor, além da preparação e do tratamento de configuração ausente. São verificações do instrumento, não novos casos de avaliação do produto.

## Situação da medição remota

Concluída em 08/11/2026 após autorização explícita do usuário para os 41 recortes e os três destinos. SONAR_TOKEN foi carregado do usuário Windows lucas, sem exposição da credencial. SonarScanner CLI 8.1.0.6389 foi baixado do domínio oficial binaries.sonarsource.com e extraído em tests/sonarcloud-manutencao/.work/tools, ignorado pelo Git. A execução final retornou código 0.

Os 41 arquivos da campanha inicial somavam 203.333 bytes; o recorte de rótulos foi reduzido na retificação descrita abaixo. Foram analisados 8/8 recortes de importação, 20/20 de rótulos e 13/13 de exportação. Nenhum arquivo foi excluído pelos padrões de inclusão/exclusão. O inventário devolvido pela API foi comparado ao manifesto em cada coleta e conferido novamente ao finalizar a documentação.

| Componente | Processamento remoto | Medidas coletadas | Resultado | Julgamento |
| --- | --- | --- | --- | --- |
| Importação | SUCCESS, 08/11/2026 às 14:31:30 (America/Sao_Paulo) | C = 275; F = 25 | M3.1 = 11 | Atenção |
| Rótulos, coleta corrigida | SUCCESS, 08/11/2026 às 14:46:49 (America/Sao_Paulo) | C = 1057; F = 116 | M3.1 = 9,112068965517242 | Adequado |
| Exportação | SUCCESS, 08/11/2026 às 14:35:01 (America/Sao_Paulo) | Ld = 28; Lt = 2846 | M3.2 = 0,9838369641602248% | Adequado |

Os horários são os executedAt registrados pelo serviço, convertidos de UTC para America/Sao_Paulo. As respostas brutas, os IDs de análise e os painéis estão vinculados no [relatório](README.md). Foram conferidos novamente: estado SUCCESS, identidade entre análise submetida e consultada, commit, inventário completo, numeradores, denominadores e classificação recalculada. Não houve nova chamada remota nessa conferência final.

Na preparação do relatório acadêmico foi identificada sobreposição entre os recortes de startEditing (46070–46293) e toggleViewMode (46154–46293). O primeiro foi corrigido para 46070–46152 e somente a coleta de rótulos foi repetida. O valor original 1113/117 = 9,512820512820513 foi invalidado como resultado final. A análise corrigida é 4853c608-87f3-477c-ae03-18d6f2fab544. O [relatório portátil](RELATORIO_MANUTENIBILIDADE.md) preserva o snapshot anterior e os intervalos originais no anexo E5. O preparador agora rejeita sobreposições e aceita fechamentos de função sem ponto e vírgula. Também usa um diretório de trabalho exclusivo por execução para evitar resíduos bloqueados pelo Windows. A análise SCA foi desativada no instrumento para futuras coletas, pois não compõe as métricas M3.1/M3.2; ela permaneceu ativa nas coletas aqui registradas.

Ambiente do scanner: Java 21.0.9 Eclipse Adoptium, analisador JavaScript 14.4.0.46458 e perfil Sonar way core. A primeira tentativa parou antes da análise devido a AccessDeniedException na extração do JRE provisionado. Corrigiu-se com sonar.scanner.skipJreProvisioning=true e SONAR_SCANNER_JAVA_EXE_PATH apontando ao Java incluído no scanner portátil. A execução final também registrou falhas ao limpar diretórios temporários, depois do envio dos relatórios; o scanner terminou com EXECUTION SUCCESS e os três processamentos remotos foram confirmados pela API. Não se confundem essas falhas de limpeza com reprovação ou ausência das medidas.

Os sensores padrão do SonarCloud também produziram informações fora de G3. Elas não foram coletadas nem usadas no julgamento desta avaliação; não foi adotado o Quality Gate padrão como resultado.

As faixas e os limites de validade estão no [método](../../tests/sonarcloud-manutencao/README.md). Os resultados são restritos aos recortes e à versão local 32.6.10, com cobertura parcial do fluxo de PDF. Não se atribui nota global G3.
