from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT_PROYECTO = Path.cwd()
ENGINE = ROOT_PROYECTO / "modulo_bpmn_workflow_engine"
EVALS_ROOT = ROOT_PROYECTO / "m7-evals-offline"

sys.path.insert(0, str(ENGINE))

import src.agent_mcp.agente_mcp as agente_mcp
from src.agent_mcp.agent import MAX_PASOS
from src.tool_calling.config import get_settings


DATASET = EVALS_ROOT / "dataset" / "dataset_dorado.jsonl"
PROMPTS = EVALS_ROOT / "prompts"
RESPUESTAS = EVALS_ROOT / "respuestas"


def cargar_dataset() -> list[dict]:
    casos = []

    with DATASET.open("r", encoding="utf-8") as fh:
        for linea in fh:
            linea = linea.strip()
            if linea:
                casos.append(json.loads(linea))

    return casos


def sha256_texto(texto: str) -> str:
    return hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()


async def generar(
    version: str,
    ids: set[str] | None = None,
) -> Path:

    prompt_path = PROMPTS / f"{version}.txt"

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"No existe {prompt_path}"
        )

    prompt_bytes = prompt_path.read_bytes()

    prompt = prompt_bytes.decode(
        "utf-8-sig"
    ).strip()

    prompt_file_hash = hashlib.sha256(
        prompt_bytes
    ).hexdigest()

    prompt_effective_hash = sha256_texto(
        prompt
    )

    # Alias conservado para compatibilidad.
    prompt_hash = prompt_effective_hash

    # Cambio experimental SOLO en memoria.
    prompt_original = agente_mcp.SYSTEM_PROMPT
    agente_mcp.SYSTEM_PROMPT = prompt

    settings = get_settings()

    casos = cargar_dataset()

    if ids:
        casos = [
            c for c in casos
            if c["id"] in ids
        ]

    RESPUESTAS.mkdir(
        parents=True,
        exist_ok=True
    )

    salida = (
        RESPUESTAS
        / (
            f"{version}.jsonl"
            if not ids
            else f"{version}_smoke.jsonl"
        )
    )

    resultados = []

    print(
        f"\n=== GENERACION {version.upper()} ==="
    )
    print(
        "MODELO:",
        settings.ollama_model
    )
    print(
        "MAX_PASOS:",
        MAX_PASOS
    )
    print(
        "PROMPT_FILE_SHA256:",
        prompt_file_hash
    )
    print(
        "PROMPT_EFFECTIVE_SHA256:",
        prompt_effective_hash
    )
    print(
        "CASOS_A_GENERAR:",
        len(casos)
    )

    try:
        for indice, caso in enumerate(casos, 1):

            print(
                f"\n[{indice}/{len(casos)}] "
                f"{caso['id']} | "
                f"{caso['tipo']} | "
                f"critico={caso['critico']}"
            )

            print(
                "PREGUNTA:",
                caso["pregunta"]
            )

            inicio = time.monotonic()

            try:
                resultado = await asyncio.wait_for(
                    agente_mcp.run_agent_mcp_async(
                        caso["pregunta"],
                        max_steps=MAX_PASOS,
                    ),
                    timeout=170,
                )

                duracion = round(
                    time.monotonic() - inicio,
                    2
                )

                trace_serializable = json.loads(
                    json.dumps(
                        list(resultado.trace or []),
                        ensure_ascii=False,
                        default=str,
                    )
                )

                observaciones_mcp = [
                    item.get("result")
                    for item in trace_serializable
                    if (
                        isinstance(item, dict)
                        and item.get("type") == "observation"
                        and item.get("via") == "MCP"
                        and item.get("result") is not None
                    )
                ]

                registro = {
                    "id": caso["id"],
                    "version": version,
                    "tipo": caso["tipo"],
                    "critico": caso["critico"],
                    "pregunta": caso["pregunta"],
                    "contexto_dorado": caso["contexto"],
                    "respuesta": resultado.response,
                    "status": resultado.status,
                    "steps": resultado.steps,
                    "model": resultado.model,
                    "tools_used": list(
                        resultado.tools_used
                    ),
                    "observaciones_mcp": observaciones_mcp,
                    "trace": trace_serializable,
                    "duracion_s": duracion,
                    "prompt_file_sha256": prompt_file_hash,
                    "prompt_effective_sha256": prompt_effective_hash,
                    "timeout": False,
                    "error": None,
                }

            except asyncio.TimeoutError:

                duracion = round(
                    time.monotonic() - inicio,
                    2
                )

                registro = {
                    "id": caso["id"],
                    "version": version,
                    "respuesta": "",
                    "status": "TIMEOUT",
                    "steps": None,
                    "model": settings.ollama_model,
                    "tools_used": [],
                    "duracion_s": duracion,
                    "prompt_sha256": prompt_hash,
                    "timeout": True,
                    "error": "timeout_170s",
                }

            except Exception as exc:

                duracion = round(
                    time.monotonic() - inicio,
                    2
                )

                registro = {
                    "id": caso["id"],
                    "version": version,
                    "respuesta": "",
                    "status": "ERROR",
                    "steps": None,
                    "model": settings.ollama_model,
                    "tools_used": [],
                    "duracion_s": duracion,
                    "prompt_sha256": prompt_hash,
                    "timeout": False,
                    "error": (
                        f"{type(exc).__name__}: {exc}"
                    ),
                }

            resultados.append(registro)

            print(
                "STATUS:",
                registro["status"]
            )
            print(
                "STEPS:",
                registro["steps"]
            )
            print(
                "TOOLS:",
                registro["tools_used"]
            )
            print(
                "DURACION_S:",
                registro["duracion_s"]
            )
            print(
                "RESPUESTA:",
                registro["respuesta"]
            )
            print(
                "OBSERVACIONES_MCP:",
                len(
                    registro.get(
                        "observaciones_mcp",
                        []
                    )
                )
            )

    finally:
        # Restaurar el prompt productivo.
        agente_mcp.SYSTEM_PROMPT = prompt_original

    with salida.open(
        "w",
        encoding="utf-8"
    ) as fh:
        for registro in resultados:
            fh.write(
                json.dumps(
                    registro,
                    ensure_ascii=False
                )
                + "\n"
            )

    print(
        "\nARCHIVO_GUARDADO:",
        salida
    )

    print(
        "TOTAL_GUARDADO:",
        len(resultados)
    )

    return salida


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "version",
        choices=["v1", "v2", "v3"],
    )

    parser.add_argument(
        "--ids",
        nargs="*",
        default=None,
    )

    args = parser.parse_args()

    asyncio.run(
        generar(
            args.version,
            set(args.ids) if args.ids else None,
        )
    )


if __name__ == "__main__":
    main()
