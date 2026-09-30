from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path.cwd()
ENGINE = ROOT / "modulo_bpmn_workflow_engine"
EVALS = ROOT / "m7-evals-offline"

sys.path.insert(0, str(ENGINE))

from src.tool_calling.config import get_settings


DATASET_PATH = EVALS / "dataset" / "dataset_dorado.jsonl"
UMBRALES_PATH = EVALS / "evals" / "umbrales.json"
RUBRICA_PATH = EVALS / "evals" / "RUBRICA_JUEZ_FIDELIDAD.md"
RESPUESTAS_DIR = EVALS / "respuestas"
RESULTADOS_DIR = EVALS / "evals" / "resultados"

JUDGE_MODEL = os.getenv(
    "EVALS_JUDGE_MODEL",
    "deepseek-coder-v2:latest",
)


def cargar_jsonl(path: Path) -> dict[str, dict]:
    datos = {}

    with path.open(
        "r",
        encoding="utf-8",
    ) as fh:

        for linea in fh:

            linea = linea.strip()

            if linea:
                item = json.loads(linea)
                datos[item["id"]] = item

    return datos


def normalizar(texto: str) -> str:

    texto = unicodedata.normalize(
        "NFKD",
        str(texto),
    )

    texto = "".join(
        c
        for c in texto
        if not unicodedata.combining(c)
    )

    return texto.lower()


def coincide(
    respuesta: str,
    patron: str,
) -> bool:

    respuesta_n = normalizar(
        respuesta
    )

    alternativas = [
        normalizar(x.strip())
        for x in patron.split("|")
        if x.strip()
    ]

    return any(
        alternativa in respuesta_n
        for alternativa in alternativas
    )


def medir_completitud(
    caso: dict,
    respuesta: str,
) -> tuple[float, list, list]:

    patrones = caso.get(
        "debe_contener",
        [],
    )

    if not patrones:
        return 1.0, [], []

    presentes = []
    faltantes = []

    for patron in patrones:

        if coincide(
            respuesta,
            patron,
        ):
            presentes.append(
                patron
            )
        else:
            faltantes.append(
                patron
            )

    score = (
        len(presentes)
        / len(patrones)
    )

    return (
        round(score, 4),
        presentes,
        faltantes,
    )


def medir_prohibidos(
    caso: dict,
    respuesta: str,
) -> tuple[int, list]:

    encontrados = []

    for frase in caso.get(
        "no_debe_contener",
        [],
    ):

        if coincide(
            respuesta,
            frase,
        ):
            encontrados.append(
                frase
            )

    score = (
        1
        if not encontrados
        else 0
    )

    return score, encontrados


def extraer_json(
    texto: str,
) -> dict:

    texto = texto.strip()

    try:
        return json.loads(
            texto
        )
    except json.JSONDecodeError:
        pass

    match = re.search(
        r"\{.*\}",
        texto,
        flags=re.DOTALL,
    )

    if not match:
        raise ValueError(
            "Juez sin JSON válido."
        )

    return json.loads(
        match.group(0)
    )


def juzgar_fidelidad(
    *,
    caso: dict,
    resultado: dict,
    rubrica: str,
) -> tuple[int, str]:

    settings = get_settings()

    observaciones = resultado.get(
        "observaciones_mcp",
        [],
    )

    prompt = f"""
Aplica EXCLUSIVAMENTE esta rúbrica de fidelidad:

{rubrica}

CASO
====

PREGUNTA:
{caso["pregunta"]}

CONTEXTO DORADO:
{caso["contexto"]}

OBSERVACIONES MCP:
{
    json.dumps(
        observaciones,
        ensure_ascii=False,
        indent=2,
    )
    if observaciones
    else "(sin observaciones MCP)"
}

RESPUESTA:
{resultado["respuesta"]}

Devuelve EXCLUSIVAMENTE JSON válido:

{{
  "afirmaciones_no_respaldadas": [],
  "fiel": true,
  "razon": "explicación breve"
}}

No evalúes completitud, estilo ni utilidad.
""".strip()

    payload = {
        "model": JUDGE_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Eres un juez de fidelidad factual. "
                    "Aplica literalmente la rúbrica."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
        },
    }

    req = urllib.request.Request(
        settings.ollama_api_url,
        data=json.dumps(
            payload
        ).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(
        req,
        timeout=180,
    ) as response:

        envelope = json.loads(
            response
            .read()
            .decode("utf-8")
        )

    contenido = (
        envelope
        .get("message", {})
        .get("content", "")
    )

    decision = extraer_json(
        contenido
    )

    fiel = decision.get(
        "fiel"
    )

    if not isinstance(
        fiel,
        bool,
    ):
        raise ValueError(
            f"fiel no booleano: {decision}"
        )

    razon = str(
        decision.get(
            "razon",
            "",
        )
    ).strip()

    return (
        1 if fiel else 0,
        razon,
    )


def evaluar_version(
    version: str,
    dataset: dict,
    rubrica: str,
    umbrales: dict,
) -> dict:

    respuestas = cargar_jsonl(
        RESPUESTAS_DIR
        / f"{version}.jsonl"
    )

    resultados = []

    print(
        f"\n=== EVALUANDO {version.upper()} ==="
    )

    for indice, id_ in enumerate(
        dataset,
        1,
    ):

        caso = dataset[id_]
        respuesta = respuestas[id_]

        print(
            f"[{indice}/15] {id_}..."
        )

        completitud, presentes, faltantes = (
            medir_completitud(
                caso,
                respuesta["respuesta"],
            )
        )

        sin_prohibidos, prohibidos = (
            medir_prohibidos(
                caso,
                respuesta["respuesta"],
            )
        )

        fidelidad, razon = juzgar_fidelidad(
            caso=caso,
            resultado=respuesta,
            rubrica=rubrica,
        )

        critico_fallado = (
            caso["critico"]
            and (
                completitud < 1.0
                or sin_prohibidos < 1
                or fidelidad < 1
            )
        )

        registro = {
            "id": id_,
            "version": version,
            "tipo": caso["tipo"],
            "critico": caso["critico"],
            "completitud": completitud,
            "sin_prohibidos": sin_prohibidos,
            "fidelidad": fidelidad,
            "puntos_presentes": presentes,
            "puntos_faltantes": faltantes,
            "prohibidos_encontrados": prohibidos,
            "razon_juez": razon,
            "critico_fallado": critico_fallado,
        }

        resultados.append(
            registro
        )

        print(
            "   completitud=",
            completitud,
            "| sin_prohibidos=",
            sin_prohibidos,
            "| fidelidad=",
            fidelidad,
            "| critico_fallado=",
            critico_fallado,
        )

    comp = sum(
        r["completitud"]
        for r in resultados
    ) / len(resultados)

    prohib = sum(
        r["sin_prohibidos"]
        for r in resultados
    ) / len(resultados)

    fidel = sum(
        r["fidelidad"]
        for r in resultados
    ) / len(resultados)

    criticos_fallados = [
        r["id"]
        for r in resultados
        if r["critico_fallado"]
    ]

    gate = (
        comp
        >= umbrales[
            "completitud_promedio_minima"
        ]
        and fidel
        >= umbrales[
            "fidelidad_promedio_minima"
        ]
        and prohib
        >= umbrales[
            "sin_prohibidos_promedio_minimo"
        ]
        and not criticos_fallados
    )

    resumen = {
        "version": version,
        "total": len(
            resultados
        ),
        "completitud_promedio": round(
            comp,
            4,
        ),
        "sin_prohibidos_promedio": round(
            prohib,
            4,
        ),
        "fidelidad_promedio": round(
            fidel,
            4,
        ),
        "criticos_fallados": (
            criticos_fallados
        ),
        "gate": (
            "PASA"
            if gate
            else "NO_PASA"
        ),
    }

    RESULTADOS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    detalle_path = (
        RESULTADOS_DIR
        / f"{version}_detalle.jsonl"
    )

    with detalle_path.open(
        "w",
        encoding="utf-8",
    ) as fh:

        for registro in resultados:

            fh.write(
                json.dumps(
                    registro,
                    ensure_ascii=False,
                )
                + "\n"
            )

    resumen_path = (
        RESULTADOS_DIR
        / f"{version}_resumen.json"
    )

    resumen_path.write_text(
        json.dumps(
            resumen,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    return resumen


dataset = cargar_jsonl(
    DATASET_PATH
)

umbrales = json.loads(
    UMBRALES_PATH.read_text(
        encoding="utf-8"
    )
)

rubrica = RUBRICA_PATH.read_text(
    encoding="utf-8"
)

print(
    "\n=== EVALS OFFLINE | PASO 19 ==="
)

print(
    "MODELO_JUEZ:",
    JUDGE_MODEL
)

print(
    "TOTAL_DATASET:",
    len(dataset)
)

resumenes = []

for version in (
    "v1",
    "v2",
):

    resumenes.append(
        evaluar_version(
            version,
            dataset,
            rubrica,
            umbrales,
        )
    )

print(
    "\n=== RESULTADOS V1 vs V2 ==="
)

for r in resumenes:

    print(
        "\nVERSION:",
        r["version"]
    )

    print(
        "COMPLETITUD:",
        r["completitud_promedio"]
    )

    print(
        "SIN_PROHIBIDOS:",
        r["sin_prohibidos_promedio"]
    )

    print(
        "FIDELIDAD:",
        r["fidelidad_promedio"]
    )

    print(
        "CRITICOS_FALLADOS:",
        r["criticos_fallados"]
    )

    print(
        "GATE:",
        r["gate"]
    )

print(
    "\n=== CASOS QUE FALLAN EN V1 ==="
)

for linea in (
    RESULTADOS_DIR
    / "v1_detalle.jsonl"
).read_text(
    encoding="utf-8"
).splitlines():

    r = json.loads(
        linea
    )

    if (
        r["completitud"] < 1
        or r["sin_prohibidos"] < 1
        or r["fidelidad"] < 1
    ):

        print(
            r["id"],
            "| C=",
            r["completitud"],
            "| P=",
            r["sin_prohibidos"],
            "| F=",
            r["fidelidad"],
            "| faltantes=",
            r["puntos_faltantes"],
            "| prohibidos=",
            r["prohibidos_encontrados"],
        )

print(
    "\n=== CASOS QUE FALLAN EN V2 ==="
)

for linea in (
    RESULTADOS_DIR
    / "v2_detalle.jsonl"
).read_text(
    encoding="utf-8"
).splitlines():

    r = json.loads(
        linea
    )

    if (
        r["completitud"] < 1
        or r["sin_prohibidos"] < 1
        or r["fidelidad"] < 1
    ):

        print(
            r["id"],
            "| C=",
            r["completitud"],
            "| P=",
            r["sin_prohibidos"],
            "| F=",
            r["fidelidad"],
            "| faltantes=",
            r["puntos_faltantes"],
            "| prohibidos=",
            r["prohibidos_encontrados"],
        )

print(
    "\nEVALUACION_V1_V2_COMPLETADA: True"
)
