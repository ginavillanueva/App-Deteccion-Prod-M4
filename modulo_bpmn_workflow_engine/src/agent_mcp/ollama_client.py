"""Cliente Ollama para el agente ReAct de App Detección Prod."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib import error, request

from ..tool_calling.config import get_settings
from .tools import AGENT_TOOL_SCHEMAS


class OllamaAgentError(RuntimeError):
    """Error controlado durante la comunicación del agente con Ollama."""


@dataclass(frozen=True)
class OllamaAgentResponse:
    """Respuesta normalizada devuelta por Ollama al agente."""

    message: dict[str, Any]
    model: str
    raw_response: dict[str, Any]

    @property
    def content(self) -> str:
        """Texto generado por el modelo."""
        return str(
            self.message.get("content") or ""
        ).strip()

    @property
    def tool_calls(self) -> list[dict[str, Any]]:
        """Llamadas a herramientas solicitadas por el modelo."""
        value = self.message.get("tool_calls") or []

        if not isinstance(value, list):
            raise OllamaAgentError(
                "Ollama devolvió tool_calls con formato inválido."
            )

        return value


def build_agent_payload(
    messages: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Construye la solicitud enviada a Ollama.

    A diferencia del selector legacy, recibe todo el historial
    de mensajes del agente.
    """
    settings = get_settings()

    return {
        "model": settings.ollama_model,
        "messages": messages,
        "tools": AGENT_TOOL_SCHEMAS,
        "stream": False,
        "options": {
            "temperature": 0,
        },
    }


def post_json(
    url: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Envía una solicitud JSON a la API local de Ollama."""
    encoded_payload = json.dumps(
        payload,
        ensure_ascii=False,
    ).encode("utf-8")

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

        raise OllamaAgentError(
            f"Ollama devolvió HTTP {exc.code}: {detail}"
        ) from exc

    except error.URLError as exc:
        raise OllamaAgentError(
            "No fue posible comunicarse con Ollama. "
            "Verifica que el servicio esté activo."
        ) from exc

    except TimeoutError as exc:
        raise OllamaAgentError(
            "Ollama excedió el tiempo máximo de respuesta."
        ) from exc

    try:
        return json.loads(response_text)

    except json.JSONDecodeError as exc:
        raise OllamaAgentError(
            "Ollama devolvió una respuesta JSON inválida."
        ) from exc


def extract_agent_response(
    response_data: dict[str, Any],
) -> OllamaAgentResponse:
    """Valida y normaliza la respuesta recibida desde Ollama."""
    message = response_data.get("message")

    if not isinstance(message, dict):
        raise OllamaAgentError(
            "La respuesta de Ollama no contiene un message válido."
        )

    settings = get_settings()

    model = str(
        response_data.get("model")
        or settings.ollama_model
    )

    return OllamaAgentResponse(
        message=message,
        model=model,
        raw_response=response_data,
    )


def chat_with_agent(
    messages: list[dict[str, Any]],
) -> OllamaAgentResponse:
    """
    Envía el historial completo del agente a Ollama.

    Puede devolver:
    - texto final en message.content;
    - una o más solicitudes en message.tool_calls.
    """
    settings = get_settings()

    if not settings.ia_habilitada:
        raise OllamaAgentError(
            "La IA está deshabilitada en la configuración."
        )

    if not messages:
        raise OllamaAgentError(
            "El historial de mensajes no puede estar vacío."
        )

    payload = build_agent_payload(messages)

    response_data = post_json(
        url=settings.ollama_api_url,
        payload=payload,
    )

    return extract_agent_response(response_data)
