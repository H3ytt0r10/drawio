$ErrorActionPreference = 'Stop'

# Executar somente após autorizar o envio dos recortes descritos em escopo.json.
# A credencial permanece no ambiente do processo; não é escrita em arquivo.
if (-not $env:SONAR_TOKEN) {
    $env:SONAR_TOKEN = [Environment]::GetEnvironmentVariable('SONAR_TOKEN', 'User')
}
if (-not $env:SONAR_TOKEN) {
    throw 'SONAR_TOKEN não está disponível para este usuário do Windows.'
}

$env:SONAR_ORGANIZATION = 'drawio-sonarcloud-testes-qualidade'
$env:SONAR_PROJECT_IMPORTACAO = 'lucaszg-drawio-importacao'
$env:SONAR_PROJECT_ROTULOS = 'drawio-sonarcloud-testes-qualidade_lucaszg-drawio-rotulos'
$env:SONAR_PROJECT_EXPORTACAO = 'drawio-sonarcloud-testes-qualidade_lucaszg-drawio-exportacao'

$taskSonarBin = Join-Path $PSScriptRoot '.work\tools\sonar-scanner-8.1.0.6389-windows-x64\bin'
if (Test-Path -LiteralPath (Join-Path $taskSonarBin 'sonar-scanner.bat')) {
    $env:PATH = $taskSonarBin + ';' + $env:PATH
    $env:SONAR_SCANNER_JAVA_EXE_PATH = Join-Path $taskSonarBin '..\jre\bin\java.exe'
}
if (-not (Get-Command sonar-scanner.bat -ErrorAction SilentlyContinue)) {
    throw 'Instale SonarScanner CLI no PATH ou em .work/tools conforme o README.'
}
$env:SONAR_USER_HOME = Join-Path $PSScriptRoot '.work\cache'

& python (Join-Path $PSScriptRoot 'avaliar.py') executar
exit $LASTEXITCODE
