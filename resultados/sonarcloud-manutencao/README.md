# Resultados de manutenibilidade

Código: `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`. Versão local: `32.6.10`.

| Questão | Métrica | Componente | Cálculo | Valor | Julgamento | Situação |
| --- | --- | --- | --- | --- | --- | --- |
| Q3.1 | M3.1 | importacao | 275 / 25 | 11.000000 | Atenção | medido_no_recorte |
| Q3.2 | M3.1 | rotulos | 1057 / 116 | 9.112069 | Adequado | medido_no_recorte |
| Q3.3 | M3.2 | exportacao | 100 × 28 / 2846 | 0.983837% | Adequado | medido_no_recorte |

## Evidências e limites

Os recortes e suas linhas originais constam em [recortes.json](recortes.json).
Resultados pendentes não representam aprovação, reprovação nem valor zero.
Não há agregação em nota G3: a referência não define essa regra.
As faixas são preliminares; consulte o método e as fontes no [README](../../tests/sonarcloud-manutencao/README.md).

A versão do ambiente de referência é 32.2.0; esta cópia é 32.6.10.
Os recortes são uma delimitação operacional desta implementação, não uma lista prescrita pela equipe.
A análise cobre funções selecionadas do cliente web e preserva seus ramos compartilhados.
Não cobre a implementação do servidor externo de PDF nem todo o fechamento de dependências.
A medição vale apenas para esses recortes; a avaliação do fluxo completo permanece parcial.

- importacao: [painel SonarCloud](https://sonarcloud.io/dashboard?id=lucaszg-drawio-importacao), análise `55180c38-c24b-48d4-adc7-41c45969d11a`; [evidência bruta](evidencias/importacao.json).
- rotulos: [painel SonarCloud](https://sonarcloud.io/dashboard?id=drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos), análise `4853c608-87f3-477c-ae03-18d6f2fab544`; [evidência bruta](evidencias/rotulos.json).
- exportacao: [painel SonarCloud](https://sonarcloud.io/dashboard?id=drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao), análise `932752e9-e32c-4e9f-877f-b208641f4374`; [evidência bruta](evidencias/exportacao.json).
