"""
Nodos puros iniciales de LangGraph para App Detección Prod.

En esta primera etapa los nodos NO utilizan:
- Ollama
- MCP
- SQLite
- checkpoints

Su objetivo es validar la entrada y clasificar la intención
de negocio de forma determinística y verificable.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from .state import EstadoDeteccion, IntentType, nueva_traza


# ============================================================
# UTILIDADES
# ============================================================

def _normalizar_texto(texto: str) -> str:
    """
    Convierte texto a minúsculas, elimina tildes y normaliza espacios.
    """

    texto = texto.strip().lower()

    texto = "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )

    texto = re.sub(r"\s+", " ", texto)

    return texto


def _contiene_alguno(
    texto: str,
    patrones: tuple[str, ...],
) -> bool:
    """
    Indica si al menos uno de los patrones aparece en el texto.
    """

    return any(patron in texto for patron in patrones)


# ============================================================
# PATRONES DE SEGURIDAD
# ============================================================

PATRONES_INYECCION = (
    "ignora las instrucciones",
    "ignora instrucciones",
    "ignora todas las instrucciones",
    "ignore previous instructions",
    "ignore all instructions",
    "system prompt",
    "prompt del sistema",
    "revela tus instrucciones",
    "muestra tus instrucciones",
    "developer message",
    "jailbreak",
)


# ============================================================
# PATRONES DE NEGOCIO
# ============================================================

PATRONES_VENCIMIENTO = (
    "vencimiento",
    "vencer",
    "vence",
    "vencido",
    "caduca",
    "caducidad",
    "dias restantes",
    "fecha de vencimiento",
)


PATRONES_PRECIO = (
    "cambio de precio",
    "cambios de precio",
    "precio anterior",
    "precio nuevo",
    "variacion de precio",
    "variacion precio",
    "historial de precio",
)


PATRONES_ACCION = (
    "accion comercial",
    "acciones comerciales",
    "descuento",
    "promocion",
    "bandeo",
    "retiro",
    "responsable",
)


# ============================================================
# NODO 1 — VALIDAR ENTRADA
# ============================================================

def validar_entrada(
    estado: EstadoDeteccion,
) -> dict[str, Any]:
    """
    Guardrail determinístico de entrada.

    Se ejecuta antes de cualquier llamada a un modelo.

    Valida:
    - pregunta vacía;
    - intentos explícitos de prompt injection.

    Las consultas fuera del dominio no se bloquean aquí:
    serán clasificadas posteriormente como OTRO.
    """

    pregunta_original = estado.get("pregunta", "")
    pregunta = pregunta_original.strip()

    if not pregunta:
        return {
            "bloqueado": True,
            "problema": "PREGUNTA_VACIA",
            "respuesta": (
                "La consulta no puede estar vacía."
            ),
            "traza": nueva_traza(
                nodo="validar_entrada",
                tipo="guardrail",
                mensaje="Consulta bloqueada: pregunta vacía.",
                motivo="PREGUNTA_VACIA",
            ),
        }

    pregunta_normalizada = _normalizar_texto(pregunta)

    if _contiene_alguno(
        pregunta_normalizada,
        PATRONES_INYECCION,
    ):
        return {
            "bloqueado": True,
            "problema": "PROMPT_INJECTION",
            "respuesta": (
                "La consulta fue bloqueada por el control "
                "de seguridad de entrada."
            ),
            "traza": nueva_traza(
                nodo="validar_entrada",
                tipo="guardrail",
                mensaje=(
                    "Consulta bloqueada por patrón "
                    "de prompt injection."
                ),
                motivo="PROMPT_INJECTION",
            ),
        }

    return {
        "bloqueado": False,
        "problema": "",
        "traza": nueva_traza(
            nodo="validar_entrada",
            tipo="validacion",
            mensaje="Entrada validada correctamente.",
        ),
    }


# ============================================================
# NODO 2 — CLASIFICAR INTENCIÓN
# ============================================================

def clasificar_intencion(
    estado: EstadoDeteccion,
) -> dict[str, Any]:
    """
    Clasifica la consulta dentro del dominio de App Detección Prod.

    Esta primera versión es deliberadamente determinística.
    No utiliza LLM.

    Intenciones:
    - VENCIMIENTO
    - CAMBIO_PRECIO
    - ACCION_COMERCIAL
    - AUDITORIA_COMPLETA
    - OTRO
    """

    if estado.get("bloqueado", False):
        return {
            "intencion": "OTRO",
            "traza": nueva_traza(
                nodo="clasificar_intencion",
                tipo="clasificacion_omitida",
                mensaje=(
                    "No se clasificó la intención porque "
                    "la entrada estaba bloqueada."
                ),
            ),
        }

    pregunta = _normalizar_texto(
        estado.get("pregunta", "")
    )

    solicita_vencimiento = _contiene_alguno(
        pregunta,
        PATRONES_VENCIMIENTO,
    )

    solicita_precio = _contiene_alguno(
        pregunta,
        PATRONES_PRECIO,
    )

    solicita_accion = _contiene_alguno(
        pregunta,
        PATRONES_ACCION,
    )

    categorias_detectadas = sum(
        (
            solicita_vencimiento,
            solicita_precio,
            solicita_accion,
        )
    )

    intencion: IntentType

    if categorias_detectadas >= 2:
        intencion = "AUDITORIA_COMPLETA"

    elif solicita_vencimiento:
        intencion = "VENCIMIENTO"

    elif solicita_precio:
        intencion = "CAMBIO_PRECIO"

    elif solicita_accion:
        intencion = "ACCION_COMERCIAL"

    else:
        intencion = "OTRO"

    return {
        "intencion": intencion,
        "traza": nueva_traza(
            nodo="clasificar_intencion",
            tipo="clasificacion",
            mensaje=(
                f"Consulta clasificada como {intencion}."
            ),
            vencimiento=solicita_vencimiento,
            cambio_precio=solicita_precio,
            accion_comercial=solicita_accion,
            categorias_detectadas=categorias_detectadas,
        ),
    }