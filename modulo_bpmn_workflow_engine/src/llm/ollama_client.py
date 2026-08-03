"""Cliente para invocar un modelo de lenguaje local mediante Ollama."""

from __future__ import annotations

import json
import os
from urllib import error, request


OLLAMA_API_URL = os.getenv(
    "OLLAMA_API_URL",
    "http://localhost:11434/api/generate",
)

DEFAULT_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "deepseek-coder-v2:latest",
)


class OllamaConnectionError(RuntimeError):
    """Error producido cuando no es posible comunicarse con Ollama."""


def generate_response(
    prompt: str,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Envía un prompt a Ollama y devuelve la respuesta textual del modelo.

    Args:
        prompt: Instrucción o información enviada al modelo.
        model: Nombre del modelo instalado en Ollama.

    Returns:
        Respuesta generada por el modelo de lenguaje.

    Raises:
        ValueError: Si el prompt está vacío.
        OllamaConnectionError: Si Ollama no responde.
        RuntimeError: Si la respuesta recibida no contiene texto.
    """
    if not prompt or not prompt.strip():
        raise ValueError("El prompt no puede estar vacío.")

    payload = {
        "model": model,
        "prompt": prompt.strip(),
        "stream": False,
    }

    encoded_payload = json.dumps(payload).encode("utf-8")

    http_request = request.Request(
        OLLAMA_API_URL,
        data=encoded_payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(http_request, timeout=300) as response:
            response_data = json.loads(
                response.read().decode("utf-8")
            )
    except error.HTTPError as exc:
        raise OllamaConnectionError(
            f"Ollama respondió con el error HTTP {exc.code}."
        ) from exc
    except error.URLError as exc:
        raise OllamaConnectionError(
            "No fue posible conectarse con Ollama. "
            "Verifica que la aplicación esté ejecutándose."
        ) from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Ollama devolvió una respuesta que no es JSON válido."
        ) from exc

    generated_text = response_data.get("response", "").strip()

    if not generated_text:
        raise RuntimeError(
            "El modelo no devolvió una respuesta textual."
        )

    return generated_text