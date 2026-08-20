"""
Nodos LangGraph que reutilizan las herramientas MCP existentes.

IMPORTANTE
----------
Este módulo NO consulta SQLite directamente.

El recorrido es:

LangGraph
    -> nodo MCP
    -> call_mcp_tool(...)
    -> Cliente MCP
    -> tools/call
    -> Servidor MCP
    -> herramienta existente
    -> SQLite

De esta forma, LangGraph orquesta el proceso sin duplicar
la lógica de acceso a datos implementada en el Nivel 4.
"""

from __future__ import annotations

from typing import Any

from src.agent_mcp.cliente_mcp import call_mcp_tool

from .state import EstadoDeteccion, nueva_traza


# ============================================================
# HELPERS
# ============================================================

def _extraer_contenido_estructurado(
    respuesta_mcp: dict[str, Any],
) -> dict[str, Any]:
    """
    Obtiene el contenido estructurado devuelto por MCP.

    El cliente MCP puede devolver el resultado envuelto como:

        {
            "content": [...],
            "structuredContent": {...},
            "isError": False,
        }

    Si ya recibimos directamente el resultado estructurado,
    se devuelve tal cual.
    """

    structured = respuesta_mcp.get("structuredContent")

    if isinstance(structured, dict):
        return structured

    return respuesta_mcp


def _extraer_fuentes(
    resultado: dict[str, Any],
) -> list[str]:
    """
    Obtiene source_tables del resultado MCP de forma segura.
    """

    fuentes = resultado.get("source_tables", [])

    if not isinstance(fuentes, list):
        return []

    return [
        str(fuente)
        for fuente in fuentes
    ]


# ============================================================
# NODO MCP 1 — DETALLE DEL PRODUCTO
# ============================================================

async def consultar_detalle_mcp(
    estado: EstadoDeteccion,
) -> dict[str, Any]:
    """
    Consulta el detalle de un producto utilizando MCP.

    Este nodo:
    - lee producto y tienda desde el estado;
    - llama a consultar_detalle_producto mediante MCP;
    - registra la observación;
    - registra las fuentes;
    - registra la tool utilizada;
    - agrega trazabilidad.

    NO contiene SQL.
    NO importa directamente la base de datos.
    """

    producto = estado.get("producto", "").strip()
    tienda = estado.get("tienda", "").strip()

    # --------------------------------------------------------
    # Guardrail previo a MCP
    # --------------------------------------------------------

    if not producto:
        return {
            "problema": "PRODUCTO_NO_IDENTIFICADO",
            "traza": nueva_traza(
                nodo="consultar_detalle_mcp",
                tipo="mcp_omitido",
                mensaje=(
                    "No se ejecutó MCP porque el producto "
                    "no fue identificado."
                ),
                tool="consultar_detalle_producto",
            ),
        }

    # --------------------------------------------------------
    # Argumentos de tools/call
    # --------------------------------------------------------

    argumentos: dict[str, Any] = {
        "producto": producto,
    }

    if tienda:
        argumentos["tienda"] = tienda

    # --------------------------------------------------------
    # Ejecución MCP REAL
    # --------------------------------------------------------

    respuesta_mcp = await call_mcp_tool(
        "consultar_detalle_producto",
        argumentos,
    )

    # --------------------------------------------------------
    # Error MCP
    # --------------------------------------------------------

    if respuesta_mcp.get("isError", False):
        return {
            "problema": "MCP_ERROR",
            "observaciones": [
                {
                    "tool_name": "consultar_detalle_producto",
                    "error": True,
                    "respuesta_mcp": respuesta_mcp,
                }
            ],
            "tools_usadas": [
                "consultar_detalle_producto",
            ],
            "traza": nueva_traza(
                nodo="consultar_detalle_mcp",
                tipo="mcp_error",
                mensaje=(
                    "La herramienta MCP devolvió un error."
                ),
                tool="consultar_detalle_producto",
                argumentos=argumentos,
                via="MCP",
                operacion="tools/call",
            ),
        }

    # --------------------------------------------------------
    # Contenido estructurado
    # --------------------------------------------------------

    resultado = _extraer_contenido_estructurado(
        respuesta_mcp
    )

    fuentes = _extraer_fuentes(
        resultado
    )

    row_count = resultado.get(
        "row_count",
        0,
    )

    # --------------------------------------------------------
    # Resultado del nodo
    # --------------------------------------------------------

    salida: dict[str, Any] = {
        "observaciones": [
            resultado,
        ],
        "fuentes": fuentes,
        "tools_usadas": [
            "consultar_detalle_producto",
        ],
        "traza": nueva_traza(
            nodo="consultar_detalle_mcp",
            tipo="mcp_observation",
            mensaje=(
                "Detalle del producto consultado mediante MCP."
            ),
            tool="consultar_detalle_producto",
            argumentos=argumentos,
            via="MCP",
            transporte="stdio",
            operacion="tools/call",
            row_count=row_count,
            fuentes=fuentes,
        ),
    }

    if row_count == 0:
        salida["problema"] = "SIN_RESULTADOS"
    else:
        salida["problema"] = ""

    return salida