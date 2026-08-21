"""
Orquestación LangGraph de App Detección Prod.

Nivel 5 de la arquitectura.

Responsabilidades:
- mantener estado explícito;
- aplicar guardrails;
- clasificar intención;
- extraer contexto;
- realizar routing condicional;
- seleccionar el nodo MCP apropiado;
- preservar trazabilidad.

IMPORTANTE
----------
LangGraph NO consulta SQLite directamente.

El recorrido de datos es:

LangGraph
    -> nodo MCP
    -> Cliente MCP
    -> tools/call
    -> Servidor MCP
    -> herramientas existentes
    -> SQLite

Ramas implementadas:
- VENCIMIENTO
- CAMBIO_PRECIO
- ACCION_COMERCIAL

POLÍTICA DE PRECIOS
-------------------
Los cambios de precio son información y trazabilidad.
El agente no aprueba, rechaza ni modifica precios.

POLÍTICA DE ACCIONES COMERCIALES
--------------------------------
Las acciones comerciales consultadas son registros existentes.
El agente no inventa, aprueba ni ejecuta autónomamente
descuentos u otras acciones.
"""

from __future__ import annotations

from typing import Literal

from langgraph.graph import END, START, StateGraph

from .context_nodes import extraer_contexto
from .mcp_nodes import (
    consultar_acciones_comerciales_mcp,
    consultar_cambios_precio_mcp,
    consultar_detalle_mcp,
)
from .nodes import (
    clasificar_intencion,
    validar_entrada,
)
from .state import EstadoDeteccion


# ============================================================
# ROUTING 1 — SEGURIDAD
# ============================================================

def ruta_despues_validacion(
    estado: EstadoDeteccion,
) -> Literal[
    "continuar",
    "bloqueada",
]:
    """
    Las entradas bloqueadas terminan antes de ejecutar
    clasificación, extracción de contexto o MCP.
    """

    if estado.get("bloqueado", False):
        return "bloqueada"

    return "continuar"


# ============================================================
# ROUTING 2 — INTENCIÓN
# ============================================================

def ruta_despues_clasificacion(
    estado: EstadoDeteccion,
) -> Literal[
    "vencimiento",
    "cambio_precio",
    "accion_comercial",
    "otro",
]:
    """
    Determina la rama de negocio.

    Las tres intenciones implementadas necesitan
    extraer primero producto y tienda.
    """

    intencion = estado.get(
        "intencion",
        "OTRO",
    )

    if intencion == "VENCIMIENTO":
        return "vencimiento"

    if intencion == "CAMBIO_PRECIO":
        return "cambio_precio"

    if intencion == "ACCION_COMERCIAL":
        return "accion_comercial"

    return "otro"


# ============================================================
# ROUTING 3 — CONTEXTO + HERRAMIENTA
# ============================================================

def ruta_despues_contexto(
    estado: EstadoDeteccion,
) -> Literal[
    "detalle",
    "precio",
    "accion",
    "sin_producto",
    "otro",
]:
    """
    Después de extraer producto y tienda, selecciona
    la herramienta MCP correspondiente.

    Nunca llama MCP si no se identificó un producto.
    """

    producto = estado.get(
        "producto",
        "",
    ).strip()

    if not producto:
        return "sin_producto"

    intencion = estado.get(
        "intencion",
        "OTRO",
    )

    if intencion == "VENCIMIENTO":
        return "detalle"

    if intencion == "CAMBIO_PRECIO":
        return "precio"

    if intencion == "ACCION_COMERCIAL":
        return "accion"

    return "otro"


# ============================================================
# GRAFO BASE
# ============================================================

def construir_grafo_basico():
    """
    Baseline del Nivel 5.

    START
      ↓
    validar_entrada
      ├── bloqueada → END
      └── continuar
              ↓
       clasificar_intencion
              ↓
             END
    """

    builder = StateGraph(
        EstadoDeteccion
    )

    builder.add_node(
        "validar_entrada",
        validar_entrada,
    )

    builder.add_node(
        "clasificar_intencion",
        clasificar_intencion,
    )

    builder.add_edge(
        START,
        "validar_entrada",
    )

    builder.add_conditional_edges(
        "validar_entrada",
        ruta_despues_validacion,
        {
            "continuar": "clasificar_intencion",
            "bloqueada": END,
        },
    )

    builder.add_edge(
        "clasificar_intencion",
        END,
    )

    return builder.compile()


# ============================================================
# GRAFO LANGGRAPH + MCP
# ============================================================

def construir_grafo_mcp():
    """
    StateGraph con tres ramas funcionales.

    ----------------------------------------------------------
    VENCIMIENTO
    ----------------------------------------------------------

    START
      ↓
    validar_entrada
      ↓
    clasificar_intencion
      ↓
    extraer_contexto
      ↓
    consultar_detalle_mcp
      ↓
    END

    ----------------------------------------------------------
    CAMBIO_PRECIO
    ----------------------------------------------------------

    START
      ↓
    validar_entrada
      ↓
    clasificar_intencion
      ↓
    extraer_contexto
      ↓
    consultar_cambios_precio_mcp
      ↓
    END

    ----------------------------------------------------------
    ACCION_COMERCIAL
    ----------------------------------------------------------

    START
      ↓
    validar_entrada
      ↓
    clasificar_intencion
      ↓
    extraer_contexto
      ↓
    consultar_acciones_comerciales_mcp
      ↓
    END
    """

    builder = StateGraph(
        EstadoDeteccion
    )

    # --------------------------------------------------------
    # NODOS
    # --------------------------------------------------------

    builder.add_node(
        "validar_entrada",
        validar_entrada,
    )

    builder.add_node(
        "clasificar_intencion",
        clasificar_intencion,
    )

    builder.add_node(
        "extraer_contexto",
        extraer_contexto,
    )

    builder.add_node(
        "consultar_detalle_mcp",
        consultar_detalle_mcp,
    )

    builder.add_node(
        "consultar_cambios_precio_mcp",
        consultar_cambios_precio_mcp,
    )

    builder.add_node(
        "consultar_acciones_comerciales_mcp",
        consultar_acciones_comerciales_mcp,
    )

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    builder.add_edge(
        START,
        "validar_entrada",
    )

    # --------------------------------------------------------
    # GUARDRAIL
    # --------------------------------------------------------

    builder.add_conditional_edges(
        "validar_entrada",
        ruta_despues_validacion,
        {
            "continuar": "clasificar_intencion",
            "bloqueada": END,
        },
    )

    # --------------------------------------------------------
    # ROUTING DE INTENCIÓN
    # --------------------------------------------------------

    builder.add_conditional_edges(
        "clasificar_intencion",
        ruta_despues_clasificacion,
        {
            "vencimiento": "extraer_contexto",
            "cambio_precio": "extraer_contexto",
            "accion_comercial": "extraer_contexto",
            "otro": END,
        },
    )

    # --------------------------------------------------------
    # CONTEXTO + SELECCIÓN DE HERRAMIENTA
    # --------------------------------------------------------

    builder.add_conditional_edges(
        "extraer_contexto",
        ruta_despues_contexto,
        {
            "detalle": "consultar_detalle_mcp",
            "precio": "consultar_cambios_precio_mcp",
            "accion": "consultar_acciones_comerciales_mcp",
            "sin_producto": END,
            "otro": END,
        },
    )

    # --------------------------------------------------------
    # FIN DE LAS RAMAS MCP
    # --------------------------------------------------------

    builder.add_edge(
        "consultar_detalle_mcp",
        END,
    )

    builder.add_edge(
        "consultar_cambios_precio_mcp",
        END,
    )

    builder.add_edge(
        "consultar_acciones_comerciales_mcp",
        END,
    )

    return builder.compile()


# ============================================================
# INSTANCIAS REUTILIZABLES
# ============================================================

grafo_basico = construir_grafo_basico()

grafo_mcp = construir_grafo_mcp()