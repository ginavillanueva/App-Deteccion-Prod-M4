"""Configuración del módulo de tool calling."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = REPOSITORY_ROOT / ".env"


def load_env_file(env_path: Path = ENV_FILE) -> None:
    """
    Carga variables desde un archivo .env sin usar librerías externas.

    Las variables que ya existan en el sistema operativo no se reemplazan.
    """
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", maxsplit=1)
        os.environ.setdefault(key.strip(), value.strip())


def parse_boolean(value: str) -> bool:
    """Convierte un texto de configuración en un valor booleano."""
    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
        "si",
        "sí",
    }


@dataclass(frozen=True)
class ToolCallingSettings:
    """Configuración inmutable para la selección de herramientas."""

    ia_habilitada: bool
    ollama_model: str
    ollama_api_url: str


def get_settings() -> ToolCallingSettings:
    """Devuelve la configuración actual del módulo."""
    load_env_file()

    return ToolCallingSettings(
        ia_habilitada=parse_boolean(
            os.getenv("IA_HABILITADA", "false")
        ),
        ollama_model=os.getenv(
            "OLLAMA_MODEL",
            "llama3.2:3b-instruct-q4_K_M",
        ),
        ollama_api_url=os.getenv(
            "OLLAMA_API_URL",
            "http://localhost:11434/api/chat",
        ),
    )