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

LangGraph orquesta el proceso sin duplicar la lógica
de acceso a datos implementada en el Nivel 4.

POLÍTICA DE PRECIOS
-------------------
Los cambios de precio son únicamente información de consulta,
notificación y trazabilidad.

Ningún nodo de este módulo:
- aprueba precios;
- rechaza precios;
- modifica precios;
- autoriza cambios de precio.
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

    MCP puede devolver:

        {
            "content": [...],
            "structuredContent": {...},
            "isError": False,
        }

    Si el resultado ya viene estructurado, se devuelve tal cual.
    """

    structured = respuesta_mcp.get(
        "structuredContent"
    )

    if isinstance(structured, dict):
        return structured

    return respuesta_mcp


def _extraer_fuentes(
    resultado: dict[str, Any],
) -> list[str]:
    """
    Obtiene source_tables de forma segura.
    """

    fuentes = resultado.get(
        "source_tables",
        [],
    )

    if not isinstance(fuentes, list):
        return []

    return [
        str(fuente)
        for fuente in fuentes
    ]


def _argumentos_producto_tienda(
    estado: EstadoDeteccion,
) -> tuple[str, str, dict[str, Any]]:
    """
    Construye los argumentos comunes para herramientas
    que trabajan con producto y tienda.
    """

    producto = estado.get(
        "producto",
        "",
    ).strip()

    tienda = estado.get(
        "tienda",
        "",
    ).strip()

    argumentos: dict[str, Any] = {}

    if producto:
        argumentos["producto"] = producto

    if tienda:
        argumentos["tienda"] = tienda

    return producto, tienda, argumentos


# ============================================================
# NODO MCP — DETALLE DEL PRODUCTO
# ============================================================

async def consultar_detalle_mcp(
    estado: EstadoDeteccion,
) -> dict[str, Any]:
    """
    Consulta el detalle de un producto mediante MCP.

    No contiene SQL.
    No accede directamente a SQLite.
    """

    producto, _, argumentos = (
        _argumentos_producto_tienda(
            estado
        )
    )

    # --------------------------------------------------------
    # Guardrail previo
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
    # MCP / tools/call
    # --------------------------------------------------------

    respuesta_mcp = await call_mcp_tool(
        "consultar_detalle_producto",
        argumentos,
    )

    # --------------------------------------------------------
    # Error MCP
    # --------------------------------------------------------

    if respuesta_mcp.get(
        "isError",
        False,
    ):
        return {
            "problema": "MCP_ERROR",
            "observaciones": [
                {
                    "tool_name":
                        "consultar_detalle_producto",
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
    # Resultado estructurado
    # --------------------------------------------------------

    resultado = (
        _extraer_contenido_estructurado(
            respuesta_mcp
        )
    )

    fuentes = _extraer_fuentes(
        resultado
    )

    row_count = resultado.get(
        "row_count",
        0,
    )

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
                "Detalle del producto consultado "
                "mediante MCP."
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


# ============================================================
# NODO MCP — CAMBIOS DE PRECIO
# ============================================================

async def consultar_cambios_precio_mcp(
    estado: EstadoDeteccion,
) -> dict[str, Any]:
    """
    Consulta cambios de precio registrados mediante MCP.

    IMPORTANTE:
    Este nodo es exclusivamente informativo.

    Consulta:
    - precio anterior;
    - precio nuevo;
    - variación;
    - quién registró el cambio;
    - fecha del registro.

    NO:
    - aprueba;
    - rechaza;
    - modifica;
    - autoriza precios.
    """

    producto, _, argumentos = (
        _argumentos_producto_tienda(
            estado
        )
    )

    # --------------------------------------------------------
    # Guardrail previo
    # --------------------------------------------------------

    if not producto:
        return {
            "problema": "PRODUCTO_NO_IDENTIFICADO",
            "traza": nueva_traza(
                nodo="consultar_cambios_precio_mcp",
                tipo="mcp_omitido",
                mensaje=(
                    "No se consultaron cambios de precio "
                    "porque el producto no fue identificado."
                ),
                tool="consultar_cambios_precio",
            ),
        }

    # --------------------------------------------------------
    # MCP / tools/call
    # --------------------------------------------------------

    respuesta_mcp = await call_mcp_tool(
        "consultar_cambios_precio",
        argumentos,
    )

    # --------------------------------------------------------
    # Error MCP
    # --------------------------------------------------------

    if respuesta_mcp.get(
        "isError",
        False,
    ):
        return {
            "problema": "MCP_ERROR",
            "observaciones": [
                {
                    "tool_name":
                        "consultar_cambios_precio",
                    "error": True,
                    "respuesta_mcp": respuesta_mcp,
                }
            ],
            "tools_usadas": [
                "consultar_cambios_precio",
            ],
            "traza": nueva_traza(
                nodo="consultar_cambios_precio_mcp",
                tipo="mcp_error",
                mensaje=(
                    "La consulta informativa de cambios "
                    "de precio devolvió un error MCP."
                ),
                tool="consultar_cambios_precio",
                argumentos=argumentos,
                via="MCP",
                operacion="tools/call",
            ),
        }

    # --------------------------------------------------------
    # Resultado estructurado
    # --------------------------------------------------------

    resultado = (
        _extraer_contenido_estructurado(
            respuesta_mcp
        )
    )

    fuentes = _extraer_fuentes(
        resultado
    )

    row_count = resultado.get(
        "row_count",
        0,
    )

    salida: dict[str, Any] = {
        "observaciones": [
            resultado,
        ],
        "fuentes": fuentes,
        "tools_usadas": [
            "consultar_cambios_precio",
        ],
        "traza": nueva_traza(
            nodo="consultar_cambios_precio_mcp",
            tipo="mcp_observation",
            mensaje=(
                "Cambios de precio consultados mediante MCP "
                "con finalidad informativa y de trazabilidad."
            ),
            tool="consultar_cambios_precio",
            argumentos=argumentos,
            via="MCP",
            transporte="stdio",
            operacion="tools/call",
            row_count=row_count,
            fuentes=fuentes,
            politica=(
                "CONSULTA_INFORMATIVA_SIN_APROBACION"
            ),
        ),
    }

    if row_count == 0:
        salida["problema"] = "SIN_RESULTADOS"
    else:
        salida["problema"] = ""

    return salida