from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

ROOT = Path("m7-evals-offline")

DATASET = (
    ROOT
    / "dataset"
    / "dataset_dorado.jsonl"
)

RESPUESTAS = (
    ROOT
    / "respuestas"
    / "v2.jsonl"
)

SALIDA = (
    ROOT
    / "dataset"
    / "etiquetas_humanas.csv"
)

IDS = [
    "EV-001",
    "EV-008",
    "EV-009",
    "EV-010",
    "EV-012",
    "EV-014",
]

ANOTADOR = "Gina Fabiana Villanueva Viscarra"


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


dataset = cargar_jsonl(DATASET)
respuestas = cargar_jsonl(RESPUESTAS)

filas = []

print(
    "\n=== EVALS OFFLINE | "
    "ETIQUETADO HUMANO DE FIDELIDAD ==="
)

print(
    "\nREGLA:"
    "\n  s = FIEL: todo lo afirmado está respaldado."
    "\n  n = NO FIEL: existe al menos una afirmación "
    "no respaldada."
)

print(
    "\nNO evalúes aquí completitud, estilo ni utilidad."
    "\nSolo FIDELIDAD contra las fuentes.\n"
)

for indice, id_ in enumerate(IDS, 1):

    caso = dataset[id_]
    resultado = respuestas[id_]

    print("\n" + "=" * 78)

    print(
        f"CASO {indice}/6: {id_}"
    )

    print(
        "TIPO:",
        caso["tipo"]
    )

    print(
        "CRITICO:",
        caso["critico"]
    )

    print(
        "\nPREGUNTA:"
    )

    print(
        caso["pregunta"]
    )

    print(
        "\nCONTEXTO DORADO:"
    )

    print(
        caso["contexto"]
    )

    print(
        "\nOBSERVACIONES MCP REALES:"
    )

    observaciones = resultado.get(
        "observaciones_mcp",
        []
    )

    if observaciones:

        print(
            json.dumps(
                observaciones,
                ensure_ascii=False,
                indent=2,
            )
        )

    else:
        print(
            "(sin observaciones MCP; "
            "evaluar contra contexto dorado)"
        )

    print(
        "\nRESPUESTA V2:"
    )

    print(
        resultado["respuesta"]
    )

    print("\n" + "-" * 78)

    while True:

        decision = input(
            "¿La respuesta es FIEL? [s/n]: "
        ).strip().lower()

        if decision in {"s", "n"}:
            break

        print(
            "Entrada inválida. "
            "Escribe solamente s o n."
        )

    motivo = ""

    if decision == "n":

        motivo = input(
            "Motivo breve de NO fidelidad: "
        ).strip()

    else:

        motivo = input(
            "Nota opcional (Enter para omitir): "
        ).strip()

    filas.append(
        {
            "version": "v2",
            "id": id_,
            "tipo": caso["tipo"],
            "critico": (
                "si"
                if caso["critico"]
                else "no"
            ),
            "fiel": (
                "si"
                if decision == "s"
                else "no"
            ),
            "anotador": ANOTADOR,
            "motivo": motivo,
            "fecha": datetime.now().isoformat(
                timespec="seconds"
            ),
        }
    )

SALIDA.parent.mkdir(
    parents=True,
    exist_ok=True,
)

with SALIDA.open(
    "w",
    encoding="utf-8-sig",
    newline="",
) as fh:

    writer = csv.DictWriter(
        fh,
        fieldnames=[
            "version",
            "id",
            "tipo",
            "critico",
            "fiel",
            "anotador",
            "motivo",
            "fecha",
        ],
    )

    writer.writeheader()
    writer.writerows(filas)

print(
    "\n=== ETIQUETADO HUMANO COMPLETADO ==="
)

print(
    "ARCHIVO:",
    SALIDA
)

print(
    "TOTAL_ETIQUETAS:",
    len(filas)
)

print(
    "FIELES:",
    sum(
        f["fiel"] == "si"
        for f in filas
    )
)

print(
    "NO_FIELES:",
    sum(
        f["fiel"] == "no"
        for f in filas
    )
)

print(
    "\n=== RESUMEN ==="
)

for fila in filas:

    print(
        fila["id"],
        "|",
        fila["tipo"],
        "| humano=",
        fila["fiel"],
        "|",
        fila["motivo"],
    )

print(
    "\nETIQUETAS_HUMANAS: OK"
)
