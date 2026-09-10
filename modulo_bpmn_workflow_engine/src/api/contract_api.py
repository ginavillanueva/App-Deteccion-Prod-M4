"""
Endpoint HTTP principal de App Detección Prod.

Expone el workflow existente mediante:

    POST /api/v1/deteccion

Esta capa NO implementa reglas de negocio.
Solo:

- valida el contrato HTTP;
- delega la ejecución a LangGraph;
- devuelve una respuesta estructurada.

Las reglas continúan viviendo en el workflow real.
"""

from __future__ import annotations

from typing import Any

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.langgraph_orchestration.persistent_runtime import (
    ejecutar_persistente,
)


INTENCIONES_VALIDAS = {
    "VENCIMIENTO",
    "CAMBIO_PRECIO",
    "ACCION_COMERCIAL",
    "AUDITORIA_COMPLETA",
    "OTRO",
}


def _error_422(
    mensaje: str,
) -> JSONResponse:
    """
    Construye una respuesta uniforme de validación.
    """

    return JSONResponse(
        {
            "error": "VALIDATION_ERROR",
            "detalle": mensaje,
        },
        status_code=422,
    )


def _normalizar_lista(
    valor: Any,
) -> list[Any]:
    """
    Garantiza representación de lista
    dentro de la respuesta HTTP.
    """

    if isinstance(valor, list):
        return valor

    if valor is None:
        return []

    if isinstance(valor, (tuple, set)):
        return list(valor)

    return [valor]


def construir_respuesta(
    resultado: dict[str, Any],
    thread_id: str,
) -> dict[str, Any]:
    """
    Adapta el estado interno de LangGraph
    al contrato HTTP público.

    No modifica las reglas del workflow.
    """

    intencion = str(
        resultado.get(
            "intencion",
            "OTRO",
        )
    )

    if intencion not in INTENCIONES_VALIDAS:
        intencion = "OTRO"

    return {
        "thread_id": str(
            resultado.get(
                "thread_id",
                thread_id,
            )
        ),
        "intencion": intencion,
        "producto": str(
            resultado.get(
                "producto",
                "",
            )
        ),
        "tienda": str(
            resultado.get(
                "tienda",
                "",
            )
        ),
        "bloqueado": bool(
            resultado.get(
                "bloqueado",
                False,
            )
        ),
        "problema": str(
            resultado.get(
                "problema",
                "",
            )
        ),
        "tools_usadas": _normalizar_lista(
            resultado.get(
                "tools_usadas",
                [],
            )
        ),
        "fuentes": _normalizar_lista(
            resultado.get(
                "fuentes",
                [],
            )
        ),
        "observaciones": _normalizar_lista(
            resultado.get(
                "observaciones",
                [],
            )
        ),
        "traza": _normalizar_lista(
            resultado.get(
                "traza",
                [],
            )
        ),
        "respuesta": str(
            resultado.get(
                "respuesta",
                "",
            )
        ),
    }


async def deteccion_endpoint(
    request: Request,
) -> JSONResponse:
    """
    Endpoint principal de App Detección Prod.

    Request:

        {
            "pregunta": "...",
            "thread_id": "..."
        }

    Respuestas:

        HTTP 200 -> ejecución correcta
        HTTP 422 -> request inválido
        HTTP 500 -> error interno controlado
    """

    try:
        payload = await request.json()
    except Exception:
        return _error_422(
            "El body debe ser JSON válido."
        )

    if not isinstance(payload, dict):
        return _error_422(
            "El body debe ser un objeto JSON."
        )

    pregunta = payload.get(
        "pregunta"
    )

    thread_id = payload.get(
        "thread_id"
    )

    if not isinstance(pregunta, str):
        return _error_422(
            "pregunta debe ser string."
        )

    pregunta = pregunta.strip()

    if not pregunta:
        return _error_422(
            "pregunta no puede estar vacía."
        )

    if not isinstance(thread_id, str):
        return _error_422(
            "thread_id debe ser string."
        )

    thread_id = thread_id.strip()

    if not thread_id:
        return _error_422(
            "thread_id no puede estar vacío."
        )

    try:
        resultado = await ejecutar_persistente(
            pregunta,
            thread_id,
        )
    except Exception:
        return JSONResponse(
            {
                "error": "INTERNAL_ERROR",
                "detalle": (
                    "No fue posible completar "
                    "el workflow."
                ),
            },
            status_code=500,
        )

    respuesta = construir_respuesta(
        resultado,
        thread_id,
    )

    return JSONResponse(
        respuesta,
        status_code=200,
    )


routes = [
    Route(
        "/api/v1/deteccion",
        deteccion_endpoint,
        methods=[
            "POST",
        ],
    ),
]


app = Starlette(
    debug=False,
    routes=routes,
)
