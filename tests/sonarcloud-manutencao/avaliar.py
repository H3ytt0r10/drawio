"""Coleta exclusivamente M3.1 (Q3.1/Q3.2) e M3.2 (Q3.3), Python 3.10+."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUTPUT = ROOT / "resultados/sonarcloud-manutencao"
WORK = HERE / ".work"
HOST = "https://sonarcloud.io"
REFERENCE = "c41e8cb60d0e7ffe776a94ae24c58115f7c59f26"
GROUPS = ("importacao", "rotulos", "exportacao")


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def prepare():
    """Extrai blocos previamente fixados; não infere funções por palavras-chave."""
    scope = json.loads((HERE / "escopo.json").read_text(encoding="utf-8"))
    node = shutil.which("node")
    if not node:
        raise ValueError("Node.js necessário para validar sintaxe dos recortes (node --check).")
    evidence = {"commit": git("rev-parse", "HEAD"),
                "versao": (ROOT / "VERSION").read_text().strip(),
                "referencia_commit": REFERENCE, "componentes": {}}
    fragments = {}
    # Valida tudo antes de gravar os arquivos de análise.
    for group in GROUPS:
        records = []
        for entry in scope[group]:
            source = (ROOT / entry["arquivo"]).read_text(encoding="utf-8")
            if digest(source) != entry["sha256_lf"]:
                raise ValueError(f"Fonte alterada: {entry['arquivo']}. Revise o recorte antes de medir.")
            lines = source.splitlines(keepends=True)
            for block in entry["blocos"]:
                start, end = block["inicio"], block["fim"]
                text = "".join(lines[start - 1:end])
                if block["assinatura"] not in lines[start - 1] or not re.fullmatch(r"\s*};?\s*", lines[end - 1]):
                    raise ValueError(f"Delimitação inválida: {block}")
                if digest(text) != block["sha256_lf"]:
                    raise ValueError(f"Recorte alterado: {block['assinatura']}")
                filename = f"{len(records) + 1:03d}_{block['assinatura'].replace('.', '_')}.js"
                fragments[group, filename] = text
                records.append({"recorte": f"src/{filename}", "arquivo": entry["arquivo"], **block})
        for i, first in enumerate(records):
            for second in records[i + 1:]:
                if first["arquivo"] == second["arquivo"] and max(first["inicio"], second["inicio"]) <= min(first["fim"], second["fim"]):
                    raise ValueError(f"Recortes sobrepostos: {first['assinatura']} / {second['assinatura']}")
        evidence["componentes"][group] = records
    for (group, filename), text in fragments.items():
        target = WORK / group / "src" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
        subprocess.run([node, "--check", str(target)], check=True, capture_output=True, text=True)
    # Arquivos antigos não podem entrar em uma análise após mudança do manifesto.
    for group in GROUPS:
        expected = {name for g, name in fragments if g == group}
        actual = {p.name for p in (WORK / group / "src").glob("*")}
        if actual != expected:
            raise ValueError(f"Arquivos extras em .work/{group}/src; remova-os antes da análise.")
    write_json(OUTPUT / "recortes.json", evidence)
    return evidence


def classify(value, group):
    low, high = (5, 10) if group == "exportacao" else (10, 15)
    return "Adequado" if value <= low else "Atenção" if value <= high else "Crítico"


def calculate(group, payload):
    measures = {m["metric"]: m.get("value") for m in payload["component"]["measures"]}
    keys = ("duplicated_lines", "lines") if group == "exportacao" else ("cognitive_complexity", "functions")
    values = []
    for key in keys:
        raw = measures.get(key)
        if raw is None:
            raise ValueError(f"Métrica ausente: {key}; ausência não equivale a zero.")
        value = float(raw)
        if not math.isfinite(value) or value < 0 or not value.is_integer():
            raise ValueError(f"Métrica inválida: {key}")
        values.append(int(value))
    numerator, denominator = values
    if denominator == 0 or (group == "exportacao" and numerator > denominator):
        raise ValueError("Denominador zero ou contagem inconsistente.")
    value = numerator / denominator * (100 if group == "exportacao" else 1)
    return {"metrica": "M3.2" if group == "exportacao" else "M3.1",
            "questao": {"importacao": "Q3.1", "rotulos": "Q3.2", "exportacao": "Q3.3"}[group],
            "componentes_calculo": dict(zip(keys, values)), "valor": value,
            "julgamento": classify(value, group), "status": "medido_no_recorte"}


def api(endpoint, token, **params):
    request = Request(f"{HOST}/api/{endpoint}?{urlencode(params)}",
                      headers={"Authorization": f"Bearer {token}"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def scan(group, organization, project, token, evidence):
    scanner = shutil.which("sonar-scanner") or shutil.which("sonar-scanner.bat")
    if not scanner:
        raise ValueError("Instale SonarScanner CLI e adicione-o ao PATH.")
    base = WORK / group
    working_directory = f".scannerwork-{time.time_ns()}"
    # As propriedades não contêm credenciais. SONAR_TOKEN é herdado pelo scanner.
    properties = {"sonar.host.url": HOST, "sonar.organization": organization,
                  "sonar.projectKey": project, "sonar.projectVersion": evidence["commit"],
                  "sonar.scm.revision": evidence["commit"],
                  "sonar.sources": "src", "sonar.sourceEncoding": "UTF-8",
                  "sonar.working.directory": working_directory,
                  "sonar.scanner.skipJreProvisioning": "true",
                  "sonar.sca.enabled": "false",
                  "sonar.scm.disabled": "true", "sonar.javascript.detectBundles": "false"}
    (base / "sonar-project.properties").write_text(
        "\n".join(f"{k}={v}" for k, v in properties.items()) + "\n", encoding="utf-8")
    subprocess.run([scanner], cwd=base, check=True)
    task_file = base / working_directory / "report-task.txt"
    task = dict(line.split("=", 1) for line in task_file.read_text().splitlines() if "=" in line)
    deadline = time.monotonic() + 600
    while time.monotonic() < deadline:
        result = api("ce/task", token, id=task["ceTaskId"])
        state = result["task"]["status"]
        if state == "SUCCESS":
            break
        if state in ("FAILED", "CANCELED"):
            raise ValueError(f"Processamento SonarCloud: {state}")
        time.sleep(3)
    else:
        raise ValueError("Tempo limite aguardando processamento; nenhuma nota atribuída.")
    analysis_id = result["task"]["analysisId"]
    # Impede atribuir ao envio atual os dados de uma análise concorrente.
    analyses = api("project_analyses/search", token, project=project, ps=1)
    if not analyses.get("analyses") or analyses["analyses"][0]["key"] != analysis_id:
        raise ValueError("Análise concorrente detectada; repita a coleta isoladamente.")
    metrics = "duplicated_lines,lines" if group == "exportacao" else "cognitive_complexity,functions"
    inventory = api("components/tree", token, component=project, qualifiers="FIL", ps=500)
    expected = {r["recorte"] for r in evidence["componentes"][group]}
    actual = {r.get("path") for r in inventory.get("components", [])}
    if inventory.get("paging", {}).get("total") != len(expected) or actual != expected:
        raise ValueError("Arquivos analisados diferem do manifesto; conferir exclusões no projeto.")
    payload = api("measures/component", token, component=project, metricKeys=metrics)
    analyses_after = api("project_analyses/search", token, project=project, ps=1)
    if analyses_after["analyses"][0]["key"] != analysis_id:
        raise ValueError("Análise alterada durante a coleta; resultados descartados.")
    calculated = calculate(group, payload)
    write_json(OUTPUT / "evidencias" / f"{group}.json",
               {"task": result, "analysis": analyses, "arquivos": inventory, "medidas": payload,
                "commit": evidence["commit"], "projeto": project})
    return {**calculated, "analysis_id": analysis_id,
            "projeto": project, "dashboard": f"{HOST}/dashboard?id={project}"}


def report(evidence, results):
    data = {"data_utc": datetime.now(timezone.utc).isoformat(),
            "commit": evidence["commit"], "versao": evidence["versao"],
            "referencia_commit": REFERENCE, "resultados": results}
    write_json(OUTPUT / "resultados.json", data)
    rows = ["# Resultados de manutenibilidade", "",
            f"Código: `{data['commit']}`. Versão local: `{data['versao']}`.", "",
            "| Questão | Métrica | Componente | Cálculo | Valor | Julgamento | Situação |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for group, q, metric in [("importacao", "Q3.1", "M3.1"), ("rotulos", "Q3.2", "M3.1"), ("exportacao", "Q3.3", "M3.2")]:
        r = results[group]
        value = f"{r['valor']:.6f}" + ("%" if group == "exportacao" else "") if "valor" in r else "Não medido"
        counts = r.get("componentes_calculo", {})
        if "valor" not in r:
            formula = "—"
        elif group == "exportacao":
            formula = f"100 × {counts['duplicated_lines']} / {counts['lines']}"
        else:
            formula = f"{counts['cognitive_complexity']} / {counts['functions']}"
        rows.append(f"| {q} | {metric} | {group} | {formula} | {value} | {r.get('julgamento', 'Sem julgamento')} | {r['status']} |")
    rows += ["", "## Evidências e limites", "",
             "Os recortes e suas linhas originais constam em [recortes.json](recortes.json).",
             "Resultados pendentes não representam aprovação, reprovação nem valor zero.",
             "Não há agregação em nota G3: a referência não define essa regra.",
             "As faixas são preliminares; consulte o método e as fontes no [README](../../tests/sonarcloud-manutencao/README.md).", "",
             "A versão do ambiente de referência é 32.2.0; esta cópia é 32.6.10.",
             "Os recortes são uma delimitação operacional desta implementação, não uma lista prescrita pela equipe.",
             "A análise cobre funções selecionadas do cliente web e preserva seus ramos compartilhados.",
             "Não cobre a implementação do servidor externo de PDF nem todo o fechamento de dependências.",
             "A medição vale apenas para esses recortes; a avaliação do fluxo completo permanece parcial.", ""]
    for group in GROUPS:
        if "analysis_id" in results[group]:
            r = results[group]
            rows.append(f"- {group}: [painel SonarCloud]({r['dashboard']}), análise `{r['analysis_id']}`; [evidência bruta](evidencias/{group}.json).")
    for group in GROUPS:
        if "motivo" in results[group]:
            rows.append(f"- {group}: {results[group]['motivo']}")
    (OUTPUT / "README.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("acao", choices=("preparar", "executar"))
    args = parser.parse_args()
    evidence = prepare()
    results = {g: {"status": "pendente", "motivo": "Análise remota não executada; requer organização, três projetos, SONAR_TOKEN e SonarScanner CLI."} for g in GROUPS}
    # Invalida resultados anteriores antes de iniciar uma nova tentativa.
    report(evidence, results)
    if args.acao == "preparar":
        print("Recortes validados; resultados remotos registrados como pendentes.")
        return 0
    token, organization = os.getenv("SONAR_TOKEN"), os.getenv("SONAR_ORGANIZATION")
    projects = {g: os.getenv(f"SONAR_PROJECT_{g.upper()}") for g in GROUPS}
    if not token or not organization or not all(projects.values()):
        print("Configuração incompleta: consulte o README. Nenhuma medição realizada.", file=sys.stderr)
        return 2
    if len(set(projects.values())) != 3:
        raise ValueError("Use três projetos distintos para manter os componentes isolados.")
    for value in [organization, *projects.values()]:
        if not re.fullmatch(r"[A-Za-z0-9_.:-]+", value):
            raise ValueError("Chave inválida de organização/projeto.")
    failed = False
    for group in GROUPS:
        try:
            results[group] = scan(group, organization, projects[group], token, evidence)
        except Exception as exc:
            # Não persiste mensagens HTTP/logs que possam conter dados de autenticação.
            results[group] = {"status": "inconclusivo", "motivo": f"Falha na coleta ({type(exc).__name__}); conferir console e configuração."}
            failed = True
        report(evidence, results)
    return 2 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
