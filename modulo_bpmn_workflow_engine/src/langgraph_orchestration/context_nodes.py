"""
Extracción determinística de contexto para App Detección Prod.

Este módulo obtiene información estructurada desde
la consulta del usuario antes de ejecutar herramientas MCP.

Extrae principalmente:

- producto;
- tienda / sala.

IMPORTANTE
----------
Este módulo:

- NO utiliza LLM;
- NO consulta SQLite;
- NO ejecuta MCP;
- NO modifica datos;
- únicamente interpreta contexto de entrada.

La extracción es determinística y trazable.

Casos soportados:

- VENCIMIENTO
- CAMBIO_PRECIO
- ACCION_COMERCIAL
- AUDITORIA_COMPLETA explícita
- AUDITORIA_COMPLETA por múltiples categorías
"""

from __future__ import annotations

import re
from typing import Any

from .state import (
    EstadoDeteccion,
    nueva_traza,
)


# ============================================================
# HELPERS
# ============================================================

def _limpiar_espacios(
    texto: str,
) -> str:
    """
    Normaliza espacios consecutivos.
    """

    return re.sub(
        r"\s+",
        " ",
        texto,
    ).strip()


def _extraer_tienda(
    pregunta: str,
) -> str:
    """
    Extrae referencias de sala.

    Ejemplos:

    Sala 12
    sala 12
    SALA 12

    Devuelve:

    Sala 12
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
    Elimina la ubicación para evitar que
    forme parte del nombre del producto.

    Ejemplos:

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

    return _limpiar_espacios(
        texto
    )


def _limpiar_producto(
    producto: str,
) -> str:
    """
    Limpia el producto extraído.
    """

    producto = producto.strip()

    producto = re.sub(
        r"[¿?¡!.,;:]+$",
        "",
        producto,
    )

    return _limpiar_espacios(
        producto
    )


# ============================================================
# EXTRACCIÓN DE PRODUCTO
# ============================================================

def _extraer_producto(
    pregunta: str,
) -> str:
    """
    Extrae el producto utilizando patrones
    controlados del dominio.

    No utiliza LLM.
    """

    texto = pregunta.strip()

    # --------------------------------------------------------
    # QUITAR SIGNOS
    # --------------------------------------------------------

    texto = re.sub(
        r"[¿?¡!]+",
        "",
        texto,
    )

    # --------------------------------------------------------
    # QUITAR SALA
    # --------------------------------------------------------

    texto = _quitar_referencia_sala(
        texto
    )

    # ========================================================
    # CASO 1 — VENCIMIENTO
    #
    # Cuantos dias faltan para vencer
    # el Yogur natural 1 litro
    # ========================================================

    match = re.search(
        r"\bpara\s+vencer\s+"
        r"(?:el|la)?\s*(.+)$",
        texto,
        flags=re.IGNORECASE,
    )

    if match:
        return _limpiar_producto(
            match.group(1)
        )

    # ========================================================
    # CASO 2 — DETALLE DE PRODUCTO
    #
    # Consulta el detalle del producto
    # Yogur natural 1 litro
    # ========================================================

    match = re.search(
        r"\bproducto\s+"
        r"(?:el|la)?\s*(.+)$",
        texto,
        flags=re.IGNORECASE,
    )

    if match:
        return _limpiar_producto(
            match.group(1)
        )

    # ========================================================
    # CASO 3 — CAMBIO DE PRECIO
    #
    # El Yogur natural 1 litro
    # tuvo cambios de precio
    # ========================================================

    match = re.search(
        r"^(?:el|la)\s+(.+?)\s+"
        r"(?:tuvo|tiene|registro|registró|ha\s+tenido)\s+"
        r"(?:un\s+|algún\s+|algun\s+)?"
        r"cambios?\s+de\s+precio\b",
        texto,
        flags=re.IGNORECASE,
    )

    if match:
        return _limpiar_producto(
            match.group(1)
        )

    # ========================================================
    # CASO 4 — AUDITORIA COMPLETA EXPLÍCITA
    #
    # Necesito una auditoria completa
    # del Yogur natural 1 litro
    # ========================================================

    match = re.search(
        r"\b(?:"
        r"auditor[ií]a\s+(?:completa|integral)"
        r"|"
        r"revisi[oó]n\s+completa"
        r")"
        r"\s+(?:del|de\s+la)\s+(.+)$",
        texto,
        flags=re.IGNORECASE,
    )

    if match:
        return _limpiar_producto(
            match.group(1)
        )

    # ========================================================
    # CASO 5 — AUDITORIA POR MÚLTIPLES CATEGORÍAS
    #
    # Revisa vencimiento, cambios de precio
    # y accion comercial del Yogur natural 1 litro
    #
    # También acepta:
    # acciones comerciales del ...
    # acción comercial del ...
    # acciones comerciales de la ...
    # ========================================================

    match = re.search(
        r"\bacci[oó]n(?:es)?\s+"
        r"comercial(?:es)?\s+"
        r"(?:del|de\s+la)\s+(.+)$",
        texto,
        flags=re.IGNORECASE,
    )

    if match:
        return _limpiar_producto(
            match.group(1)
        )

    # ========================================================
    # CASO 6 — ACCIÓN COMERCIAL SIMPLE
    #
    # Que accion comercial tiene
    # el Yogur natural 1 litro
    # ========================================================

    match = re.search(
        r"\bacci[oó]n(?:es)?\s+"
        r"comercial(?:es)?"
        r".*?\btiene\s+"
        r"(?:el|la)\s+(.+)$",
        texto,
        flags=re.IGNORECASE,
    )

    if match:
        return _limpiar_producto(
            match.group(1)
        )

    # ========================================================
    # CASO 7 — FORMA ALTERNATIVA
    #
    # auditoria completa del producto
    # Yogur natural 1 litro
    # ========================================================

    match = re.search(
        r"\b(?:del|de\s+la)\s+producto\s+"
        r"(?:el|la)?\s*(.+)$",
        texto,
        flags=re.IGNORECASE,
    )

    if match:
        return _limpiar_producto(
            match.group(1)
        )

    # ========================================================
    # SIN COINCIDENCIA SEGURA
    # ========================================================

    return ""


# ============================================================
# NODO LANGGRAPH
# ============================================================

def extraer_contexto(
    estado: EstadoDeteccion,
) -> dict[str, Any]:
    """
    Extrae producto y tienda desde la pregunta.

    Flujo:

    validar_entrada
        ↓
    clasificar_intencion
        ↓
    extraer_contexto
        ↓
    nodo MCP

    Si no identifica producto registra:

    PRODUCTO_NO_IDENTIFICADO

    para evitar una llamada MCP incompleta.
    """

    pregunta = estado.get(
        "pregunta",
        "",
    ).strip()

    # --------------------------------------------------------
    # PRODUCTO
    # --------------------------------------------------------

    producto = _extraer_producto(
        pregunta
    )

    # --------------------------------------------------------
    # TIENDA
    # --------------------------------------------------------

    tienda = _extraer_tienda(
        pregunta
    )

    # --------------------------------------------------------
    # VALIDACIÓN
    # --------------------------------------------------------

    problema = ""

    if not producto:
        problema = "PRODUCTO_NO_IDENTIFICADO"

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

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
            producto_identificado=bool(
                producto
            ),
            tienda_identificada=bool(
                tienda
            ),
        ),
    }