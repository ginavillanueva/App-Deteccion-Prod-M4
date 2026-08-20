"""
Extracción determinística de contexto para App Detección Prod.

Este módulo obtiene información estructurada de la pregunta
antes de ejecutar herramientas MCP.

En esta etapa extrae:

- producto
- tienda / sala

No utiliza LLM.
No consulta SQLite.
No ejecuta MCP.

La estrategia determinística se utiliza porque las consultas
del dominio contienen estructuras suficientemente claras,
por ejemplo:

    "Cuantos dias faltan para vencer el Yogur natural 1 litro
     de la Sala 12"

Si en etapas posteriores una consulta no puede interpretarse
de forma segura, podrá incorporarse un fallback controlado.
"""

from __future__ import annotations

import re
from typing import Any

from .state import EstadoDeteccion, nueva_traza


# ============================================================
# HELPERS
# ============================================================

def _limpiar_espacios(texto: str) -> str:
    """Normaliza espacios consecutivos."""

    return re.sub(
        r"\s+",
        " ",
        texto,
    ).strip()


def _extraer_tienda(
    pregunta: str,
) -> str:
    """
    Extrae expresiones como:

        Sala 12
        sala 7
        SALA 3

    y devuelve siempre:

        Sala <numero>
    """

    match = re.search(
        r"\bsala\s*(\d+)\b",
        pregunta,
        flags=re.IGNORECASE,
    )

    if not match:
        return ""

    return f"Sala {match.group(1)}"


def _quitar_referencia_sala(
    texto: str,
) -> str:
    """
    Elimina del texto expresiones de ubicación como:

        de la Sala 12
        en la Sala 12
        de Sala 12
        en Sala 12
    """

    texto = re.sub(
        r"\s+(?:de|en)\s+(?:la\s+)?sala\s*\d+\b",
        "",
        texto,
        flags=re.IGNORECASE,
    )

    return _limpiar_espacios(texto)


def _extraer_producto(
    pregunta: str,
) -> str:
    """
    Extrae el producto utilizando patrones de las consultas
    reales del proyecto.

    La función no intenta comprender lenguaje arbitrario.
    Solo reconoce estructuras controladas del dominio.
    """

    texto = pregunta.strip()

    texto = re.sub(
        r"[¿?¡!]+",
        "",
        texto,
    )

    texto = _quitar_referencia_sala(
        texto
    )

    # --------------------------------------------------------
    # Caso:
    # "Cuantos dias faltan para vencer el Yogur natural 1 litro"
    # --------------------------------------------------------

    match = re.search(
        r"\bpara\s+vencer\s+(?:el|la)?\s*(.+)$",
        texto,
        flags=re.IGNORECASE,
    )

    if match:
        return _limpiar_espacios(
            match.group(1)
        )

    # --------------------------------------------------------
    # Caso:
    # "Revisa el producto Yogur natural 1 litro"
    # "Consulta el detalle del producto Yogur natural 1 litro"
    # --------------------------------------------------------

    match = re.search(
        r"\bproducto\s+(?:el|la)?\s*(.+)$",
        texto,
        flags=re.IGNORECASE,
    )

    if match:
        return _limpiar_espacios(
            match.group(1)
        )

    # --------------------------------------------------------
    # Caso:
    # "El Yogur natural 1 litro tuvo cambios de precio"
    # --------------------------------------------------------

    match = re.search(
        r"^(?:el|la)\s+(.+?)\s+"
        r"(?:tuvo|tiene|registro|registró|ha tenido)\s+"
        r"(?:un\s+|algún\s+|algun\s+)?"
        r"cambios?\s+de\s+precio\b",
        texto,
        flags=re.IGNORECASE,
    )

    if match:
        return _limpiar_espacios(
            match.group(1)
        )

    # --------------------------------------------------------
    # Caso:
    # "Que accion comercial tiene el Yogur natural 1 litro"
    # --------------------------------------------------------

    match = re.search(
        r"\b(?:tiene|tiene registrada|tiene registrado)\s+"
        r"(?:el|la)\s+(.+)$",
        texto,
        flags=re.IGNORECASE,
    )

    if match:
        return _limpiar_espacios(
            match.group(1)
        )

    return ""


# ============================================================
# NODO LANGGRAPH
# ============================================================

def extraer_contexto(
    estado: EstadoDeteccion,
) -> dict[str, Any]:
    """
    Extrae producto y tienda desde la consulta del usuario.

    Este nodo es determinístico y se ejecuta antes de MCP.
    """

    pregunta = estado.get(
        "pregunta",
        "",
    ).strip()

    producto = _extraer_producto(
        pregunta
    )

    tienda = _extraer_tienda(
        pregunta
    )

    problema = ""

    if not producto:
        problema = "PRODUCTO_NO_IDENTIFICADO"

    return {
        "producto": producto,
        "tienda": tienda,
        "problema": problema,
        "traza": nueva_traza(
            nodo="extraer_contexto",
            tipo="extraccion_contexto",
            mensaje=(
                "Contexto de negocio extraído "
                "de forma determinística."
            ),
            producto=producto,
            tienda=tienda,
            metodo="deterministico",
            producto_identificado=bool(producto),
            tienda_identificada=bool(tienda),
        ),
    }