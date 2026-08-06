"""Selección de herramientas mediante tool calling de Ollama."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib import error, request

from .config import get_settings
from .tools import (
    LISTAR_ACCIONES_COMERCIALES_PENDIENTES,
    LISTAR_CAMBIOS_PRECIO_PENDIENTES,
    LISTAR_PRODUCTOS_PROXIMOS_A_VENCER,
    published_tool_names,
)


SYSTEM_PROMPT = """
Eres un selector de herramientas de App Detección Prod.

Tu única responsabilidad es elegir una herramienta autorizada.
No debes consultar datos, inventar productos ni redactar la respuesta final.

Reglas:
1. Elige como máximo una herramienta.
2. Usa LISTAR_PRODUCTOS_PROXIMOS_A_VENCER para preguntas sobre
   productos, mercadería, artículos que vencen, caducan o expiran pronto.
3. Usa LISTAR_CAMBIOS_PRECIO_PENDIENTES para preguntas sobre
   solicitudes o modificaciones de precio pendientes.
4. Usa LISTAR_ACCIONES_COMERCIALES_PENDIENTES para preguntas sobre
   descuentos, bandeos o acciones comerciales pendientes.
5. Cuando ninguna herramienta pueda responder, no llames a ninguna
   herramienta y responde exactamente: FUERA_DE_ALCANCE.
""".strip()


OLLAMA_TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": LISTAR_PRODUCTOS_PROXIMOS_A_VENCER,
            "description": (
                "Obtiene productos o mercadería que vencen, "
                "caducan o expiran dentro de los próximos 45 días."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": LISTAR_CAMBIOS_PRECIO_PENDIENTES,
            "description": (
                "Obtiene solicitudes de cambios de precio "
                "que todavía esperan aprobación."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": LISTAR_ACCIONES_COMERCIALES_PENDIENTES,
            "description": (
                "Obtiene descuentos, bandeos y otras acciones "
                "comerciales pendientes de ejecución."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
]


class OllamaToolSelectorError(RuntimeError):
    """Error controlado durante la selección de herramientas."""


@dataclass(frozen=True)
class LLMToolSelection:
    """Decisión producida por el modelo, sin ejecutar la herramienta."""

    question: str
    model: str
    tool_name: str | None
    raw_content: str
    path: str = "LLM"
    llm_invoked: bool = True

    @property
    def out_of_scope(self) -> bool:
        """Indica que el modelo no seleccionó una herramienta."""
        return self.tool_name is None


def build_payload(
    question: str,
    model: str,
) -> dict[str, Any]:
    """Construye la solicitud enviada a la API local de Ollama."""
    return {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        "tools": OLLAMA_TOOLS,
        "stream": False,
        "options": {
            "temperature": 0,
        },
    }


def post_json(
    url: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Envía una solicitud JSON a Ollama usando la biblioteca estándar."""
    encoded_payload = json.dumps(payload).encode("utf-8")

    http_request = request.Request(
        url=url,
        data=encoded_payload,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(
            http_request,
            timeout=120,
        ) as response:
            response_text = response.read().decode("utf-8")

    except error.HTTPError as exc:
        detail = exc.read().decode(
            "utf-8",
            errors="replace",
        )

        raise OllamaToolSelectorError(
            f"Ollama devolvió HTTP {exc.code}: {detail}"
        ) from exc

    except error.URLError as exc:
        raise OllamaToolSelectorError(
            "No fue posible comunicarse con Ollama. "
            "Verifica que el servicio esté activo."
        ) from exc

    except TimeoutError as exc:
        raise OllamaToolSelectorError(
            "Ollama excedió el tiempo máximo de respuesta."
        ) from exc

    try:
        return json.loads(response_text)

    except json.JSONDecodeError as exc:
        raise OllamaToolSelectorError(
            "Ollama devolvió una respuesta JSON inválida."
        ) from exc


def extract_tool_selection(
    response_data: dict[str, Any],
) -> tuple[str | None, str]:
    """Extrae y valida la herramienta seleccionada por el modelo."""
    message = response_data.get("message")

    if not isinstance(message, dict):
        raise OllamaToolSelectorError(
            "La respuesta de Ollama no contiene el campo message."
        )

    raw_content = str(message.get("content") or "").strip()
    tool_calls = message.get("tool_calls") or []

    if not isinstance(tool_calls, list):
        raise OllamaToolSelectorError(
            "El campo tool_calls tiene un formato inválido."
        )

    if len(tool_calls) > 1:
        raise OllamaToolSelectorError(
            "El modelo seleccionó más de una herramienta."
        )

    if not tool_calls:
        return None, raw_content

    function_data = tool_calls[0].get("function")

    if not isinstance(function_data, dict):
        raise OllamaToolSelectorError(
            "La llamada no contiene una función válida."
        )

    tool_name = function_data.get("name")

    if not isinstance(tool_name, str):
        raise OllamaToolSelectorError(
            "La llamada no contiene el nombre de la herramienta."
        )

    authorized_tools = published_tool_names()

    if tool_name not in authorized_tools:
        raise OllamaToolSelectorError(
            f"El modelo seleccionó una herramienta no autorizada: "
            f"{tool_name}"
        )

    return tool_name, raw_content


def select_tool_with_llm(
    question: str,
) -> LLMToolSelection:
    """
    Pide al modelo que seleccione una herramienta autorizada.

    Esta función no ejecuta la herramienta ni consulta la base de datos.
    """
    settings = get_settings()

    if not settings.ia_habilitada:
        raise OllamaToolSelectorError(
            "La selección mediante LLM está deshabilitada."
        )

    payload = build_payload(
        question=question,
        model=settings.ollama_model,
    )

    response_data = post_json(
        url=settings.ollama_api_url,
        payload=payload,
    )

    tool_name, raw_content = extract_tool_selection(
        response_data
    )

    return LLMToolSelection(
        question=question,
        model=settings.ollama_model,
        tool_name=tool_name,
        raw_content=raw_content,
    )