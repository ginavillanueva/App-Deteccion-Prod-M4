from __future__ import annotations

import csv
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT_PROYECTO = Path.cwd()
ENGINE = ROOT_PROYECTO / "modulo_bpmn_workflow_engine"
EVALS_ROOT = ROOT_PROYECTO / "m7-evals-offline"

sys.path.insert(0, str(ENGINE))

from src.tool_calling.config import get_settings


DATASET_PATH = (
    EVALS_ROOT
    / "dataset"
    / "dataset_dorado.jsonl"
)

RESPUESTAS_PATH = (
    EVALS_ROOT
    / "respuestas"
    / "v2.jsonl"
)

HUMANO_PATH = (
    EVALS_ROOT
    / "dataset"
    / "etiquetas_humanas.csv"
)

RUBRICA_PATH = (
    EVALS_ROOT
    / "evals"
    / "RUBRICA_JUEZ_FIDELIDAD.md"
)

RESULTADOS_PATH = (
    EVALS_ROOT
    / "evals"
    / "calibracion_juez.jsonl"
)

RESUMEN_PATH = (
    EVALS_ROOT
    / "evals"
    / "calibracion_resumen.json"
)


RUBRICA = """
# R?brica del juez de fidelidad v3

## Objetivo

Determinar si las afirmaciones factuales de una respuesta est?n
respaldadas por:

1. CONTEXTO DORADO;
2. OBSERVACIONES MCP;
3. una REGLA o POL?TICA expl?cita del contexto.

## Procedimiento obligatorio

PASO A ? Identificar afirmaciones factuales

Separar mentalmente:

- datos sobre productos, fechas, cantidades, precios y estados;
- capacidades de herramientas;
- capacidades o prohibiciones del agente;
- afirmaciones sobre existencia o disponibilidad;
- inferencias presentadas como hechos.

NO considerar afirmaciones factuales:

- saludos;
- disculpas;
- frases de cortes?a;
- "?Hay algo m?s en lo que pueda ayudarte?".

PASO B ? Verificar respaldo

Para cada afirmaci?n factual preguntar:

"?Existe evidencia expl?cita o una pol?tica que permita afirmar esto?"

Si una sola afirmaci?n factual carece de respaldo:
NO FIEL.

PASO C ? Negativas justificadas

Una negativa es FIEL cuando la pol?tica justifica la negativa.

Ejemplos generales:

Contexto:
"El agente no modifica registros."

Respuesta:
"No puedo modificar ese registro."

Resultado:
FIEL.

Contexto:
"Las instrucciones internas no deben divulgarse."

Respuesta:
"No puedo proporcionar instrucciones internas."

Resultado:
FIEL.

La negativa NO necesita una observaci?n MCP cuando existe una
pol?tica expl?cita suficiente.

PASO D ? Herramientas y fuera de alcance

Una herramienta solo tiene las capacidades que el contexto o las
observaciones le atribuyen.

Si la respuesta afirma o sugiere que una herramienta sirve para
una finalidad no documentada:
NO FIEL.

Ejemplo general:

Contexto:
"La herramienta consulta promociones de productos."

Respuesta:
"Puedes usar esa herramienta para consultar inversiones burs?tiles."

Resultado:
NO FIEL.

PASO E ? Cambio sem?ntico de datos

Utilizar un valor verdadero con significado diferente es NO FIEL.

Ejemplo general:

Contexto:
"Fecha de vencimiento: 2026-08-28.
No existe fecha de reposici?n."

Respuesta:
"La reposici?n ser? el 2026-08-28."

Resultado:
NO FIEL.

PASO F ? Ausencia de resultados

"0 filas" significa solamente que esa consulta no devolvi? registros.

No permite afirmar autom?ticamente:

- que el producto no existe;
- que la tienda no lo posee;
- que fue eliminado;
- que est? agotado.

Agregar cualquiera de esas hip?tesis como hecho:
NO FIEL.

## Decisi?n final

FIEL:
todas las afirmaciones factuales est?n sustentadas.

NO FIEL:
existe al menos una afirmaci?n factual no sustentada.

## NO evaluar

No evaluar:

- completitud;
- utilidad;
- estilo;
- longitud;
- cortes?a;
- qu? tan buena es la respuesta.

Una respuesta puede ser incompleta pero FIEL.
""".strip()


def cargar_jsonl(path: Path) -> dict[str, dict]:
    datos = {}

    with path.open(
        "r",
        encoding="utf-8",
    ) as fh:

        for linea in fh:
            linea = linea.strip()

            if not linea:
                continue

            item = json.loads(linea)
            datos[item["id"]] = item

    return datos


def cargar_humano() -> list[dict]:
    with HUMANO_PATH.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as fh:
        return list(csv.DictReader(fh))


def extraer_json(texto: str) -> dict:
    texto = texto.strip()

    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        pass

    match = re.search(
        r"\{.*\}",
        texto,
        flags=re.DOTALL,
    )

    if not match:
        raise ValueError(
            "El juez no devolvió un objeto JSON."
        )

    return json.loads(
        match.group(0)
    )


def llamar_juez(
    *,
    pregunta: str,
    contexto: str,
    observaciones: list,
    respuesta: str,
) -> tuple[bool, str, str]:

    settings = get_settings()

    evidencia = json.dumps(
        observaciones,
        ensure_ascii=False,
        indent=2,
    )

    prompt = f"""
Eres un juez de evaluación offline.

Aplica EXCLUSIVAMENTE la rúbrica siguiente.

{RUBRICA}

CASO A EVALUAR
===============

PREGUNTA:
{pregunta}

CONTEXTO DORADO:
{contexto}

OBSERVACIONES MCP:
{evidencia if observaciones else "(sin observaciones MCP)"}

RESPUESTA DEL SISTEMA:
{respuesta}

Devuelve EXCLUSIVAMENTE JSON válido con esta forma:

{{
  "fiel": true,
  "razon": "explicación breve basada en evidencia"
}}

No incluyas markdown.
No evalúes completitud.
No conozcas ni intentes inferir la etiqueta humana.
""".strip()

    payload = {
        "model": os.getenv(
            "EVALS_JUDGE_MODEL",
            settings.ollama_model,
        ),
        "messages": [
            {
                "role": "system",
                "content": (
                    "Eres un juez de fidelidad factual. "
                    "Debes aplicar literalmente el procedimiento "
                    "de la r?brica, verificar afirmaci?n por "
                    "afirmaci?n y no penalizar cortes?a ni "
                    "negativas respaldadas por pol?ticas."
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
        timeout=120,
    ) as response:

        raw = response.read().decode(
            "utf-8"
        )

    envelope = json.loads(raw)

    contenido = (
        envelope
        .get("message", {})
        .get("content", "")
    )

    resultado = extraer_json(
        contenido
    )

    fiel = resultado.get("fiel")

    if not isinstance(fiel, bool):
        raise ValueError(
            f"'fiel' no es booleano: {resultado}"
        )

    razon = str(
        resultado.get(
            "razon",
            "",
        )
    ).strip()

    return fiel, razon, contenido


def cohen_kappa(
    humanos: list[bool],
    jueces: list[bool],
) -> tuple[float, float, float]:

    n = len(humanos)

    if n == 0:
        raise ValueError(
            "No hay etiquetas."
        )

    acuerdo = sum(
        h == j
        for h, j in zip(
            humanos,
            jueces,
        )
    ) / n

    p_h_si = sum(
        humanos
    ) / n

    p_h_no = 1 - p_h_si

    p_j_si = sum(
        jueces
    ) / n

    p_j_no = 1 - p_j_si

    esperado = (
        p_h_si * p_j_si
        +
        p_h_no * p_j_no
    )

    if esperado == 1:
        kappa = 1.0
    else:
        kappa = (
            acuerdo - esperado
        ) / (
            1 - esperado
        )

    return acuerdo, esperado, kappa


dataset = cargar_jsonl(
    DATASET_PATH
)

respuestas = cargar_jsonl(
    RESPUESTAS_PATH
)

humanas = cargar_humano()

RUBRICA_PATH.write_text(
    RUBRICA + "\n",
    encoding="utf-8",
)

settings = get_settings()

judge_model = os.getenv(
    "EVALS_JUDGE_MODEL",
    settings.ollama_model,
)

print(
    "\n=== EVALS OFFLINE | "
    "PASO 14 | CALIBRACION DEL JUEZ ==="
)

print(
    "MODELO_JUEZ:",
    judge_model
)

print(
    "TEMPERATURA_JUEZ: 0"
)

print(
    "TOTAL_CASOS_CALIBRACION:",
    len(humanas)
)

resultados = []

for indice, etiqueta in enumerate(
    humanas,
    1,
):

    id_ = etiqueta["id"]

    caso = dataset[id_]
    respuesta = respuestas[id_]

    print(
        f"\n[{indice}/{len(humanas)}] "
        f"JUZGANDO {id_}..."
    )

    try:

        juez_fiel, razon, raw = llamar_juez(
            pregunta=caso["pregunta"],
            contexto=caso["contexto"],
            observaciones=respuesta.get(
                "observaciones_mcp",
                [],
            ),
            respuesta=respuesta["respuesta"],
        )

        humano_fiel = (
            etiqueta["fiel"].strip().lower()
            == "si"
        )

        registro = {
            "id": id_,
            "tipo": caso["tipo"],
            "critico": caso["critico"],
            "humano_fiel": humano_fiel,
            "juez_fiel": juez_fiel,
            "acuerdo": (
                humano_fiel
                == juez_fiel
            ),
            "razon_juez": razon,
        }

        resultados.append(
            registro
        )

        print(
            "HUMANO:",
            "FIEL"
            if humano_fiel
            else "NO_FIEL"
        )

        print(
            "JUEZ:",
            "FIEL"
            if juez_fiel
            else "NO_FIEL"
        )

        print(
            "ACUERDO:",
            registro["acuerdo"]
        )

        print(
            "RAZON_JUEZ:",
            razon
        )

    except Exception as exc:

        print(
            "ERROR_JUEZ:",
            type(exc).__name__,
            str(exc),
        )

        raise


with RESULTADOS_PATH.open(
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


humanos_bool = [
    r["humano_fiel"]
    for r in resultados
]

jueces_bool = [
    r["juez_fiel"]
    for r in resultados
]

acuerdo, esperado, kappa = (
    cohen_kappa(
        humanos_bool,
        jueces_bool,
    )
)

acuerdos_n = sum(
    r["acuerdo"]
    for r in resultados
)

desacuerdos = [
    r["id"]
    for r in resultados
    if not r["acuerdo"]
]

resumen = {
    "total_calibracion": len(
        resultados
    ),
    "acuerdos": acuerdos_n,
    "desacuerdos": desacuerdos,
    "porcentaje_acuerdo": round(
        acuerdo * 100,
        2,
    ),
    "acuerdo_esperado": round(
        esperado,
        4,
    ),
    "cohen_kappa": round(
        kappa,
        4,
    ),
    "modelo_juez": judge_model,
    "temperatura_juez": 0,
}

RESUMEN_PATH.write_text(
    json.dumps(
        resumen,
        ensure_ascii=False,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

print(
    "\n=== RESULTADO CALIBRACION ==="
)

print(
    "TOTAL:",
    resumen["total_calibracion"]
)

print(
    "ACUERDOS:",
    resumen["acuerdos"]
)

print(
    "DESACUERDOS:",
    resumen["desacuerdos"]
)

print(
    "PORCENTAJE_ACUERDO:",
    resumen["porcentaje_acuerdo"],
    "%"
)

print(
    "ACUERDO_ESPERADO:",
    resumen["acuerdo_esperado"]
)

print(
    "COHEN_KAPPA:",
    resumen["cohen_kappa"]
)

print(
    "KAPPA_MAYOR_IGUAL_0_60:",
    kappa >= 0.60
)

print(
    "\n=== DETALLE ==="
)

for r in resultados:

    print(
        r["id"],
        "| humano=",
        "FIEL"
        if r["humano_fiel"]
        else "NO_FIEL",
        "| juez=",
        "FIEL"
        if r["juez_fiel"]
        else "NO_FIEL",
        "| acuerdo=",
        r["acuerdo"],
    )

print(
    "\nCALIBRACION_JUEZ_COMPLETADA: True"
)
