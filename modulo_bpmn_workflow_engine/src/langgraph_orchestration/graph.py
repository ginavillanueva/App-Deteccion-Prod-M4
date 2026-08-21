"""
Orquestación LangGraph de App Detección Prod.

Nivel 5 de la arquitectura.

Responsabilidades de esta capa:
- mantener estado explícito;
- aplicar guardrails;
- clasificar intención;
- enrutar el flujo;
- extraer contexto;
- decidir qué herramienta MCP ejecutar;
- conservar trazabilidad.

IMPORTANTE:
LangGraph no consulta SQLite directamente.

Las consultas de negocio atraviesan:

LangGraph
    -> nodo MCP
    -> Cliente MCP
    -> tools/call
    -> Servidor MCP
    -> SQLite

POLÍTICA DE PRECIOS:
Los cambios de precio son únicamente informativos
y de trazabilidad. Este grafo no aprueba, rechaza
ni modifica precios.
"""

from __future__ import annotations

from typing import Literal

from langgraph.graph import END, START, StateGraph

from .context_nodes import extraer_contexto
from .mcp_nodes import (
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
    Detiene entradas bloqueadas antes de clasificación,
    extracción de contexto o ejecución MCP.
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
    "otro",
]:
    """
    Decide qué tipo de proceso necesita la consulta.

    VENCIMIENTO y CAMBIO_PRECIO necesitan primero
    extraer producto y tienda.

    Las demás intenciones todavía terminan en END.
    """

    intencion = estado.get(
        "intencion",
        "OTRO",
    )

    if intencion == "VENCIMIENTO":
        return "vencimiento"

    if intencion == "CAMBIO_PRECIO":
        return "cambio_precio"

    return "otro"


# ============================================================
# ROUTING 3 — CONTEXTO + HERRAMIENTA
# ============================================================

def ruta_despues_contexto(
    estado: EstadoDeteccion,
) -> Literal[
    "detalle",
    "precio",
    "sin_producto",
    "otro",
]:
    """
    Después de extraer producto y tienda decide
    qué nodo MCP debe ejecutarse.

    Nunca llama MCP si no existe producto.
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
    StateGraph con routing de negocio y MCP.

    Flujo VENCIMIENTO:

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


    Flujo CAMBIO_PRECIO:

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

    Los cambios de precio son únicamente
    informativos y de trazabilidad.
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

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    builder.add_edge(
        START,
        "validar_entrada",
    )

    # --------------------------------------------------------
    # SEGURIDAD
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
    # INTENCIÓN
    # --------------------------------------------------------

    builder.add_conditional_edges(
        "clasificar_intencion",
        ruta_despues_clasificacion,
        {
            "vencimiento": "extraer_contexto",
            "cambio_precio": "extraer_contexto",
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

    return builder.compile()


# ============================================================
# INSTANCIAS REUTILIZABLES
# ============================================================

grafo_basico = construir_grafo_basico()

grafo_mcp = construir_grafo_mcp()