"""
Orquestación LangGraph de App Detección Prod.

Este módulo implementa la capa de orquestación del proyecto.

Responsabilidades principales:

- mantener estado explícito;
- aplicar guardrails;
- clasificar intención;
- extraer contexto;
- realizar routing condicional;
- seleccionar nodos MCP;
- ejecutar auditorías completas;
- preservar trazabilidad.

IMPORTANTE
----------
LangGraph NO consulta SQLite directamente.

El recorrido correcto es:

Usuario
    ↓
LangGraph
    ↓
Nodo MCP
    ↓
Cliente MCP
    ↓
tools/call
    ↓
Servidor MCP
    ↓
Herramienta publicada
    ↓
SQLite

Intenciones implementadas:

- VENCIMIENTO
- CAMBIO_PRECIO
- ACCION_COMERCIAL
- AUDITORIA_COMPLETA
- OTRO

AUDITORIA_COMPLETA
------------------
Cuando la intención es AUDITORIA_COMPLETA,
LangGraph coordina secuencialmente:

1. consulta de vencimiento / detalle;
2. consulta de cambios de precio;
3. consulta de acciones comerciales.

Esto permite demostrar una verdadera
orquestación multi-paso utilizando el mismo
estado compartido de LangGraph.

POLÍTICA DE PRECIOS
-------------------
Los cambios de precio son información y
trazabilidad.

El agente:

- NO aprueba precios;
- NO rechaza precios;
- NO modifica precios.

POLÍTICA DE ACCIONES COMERCIALES
--------------------------------
Las acciones comerciales son registros existentes.

El agente:

- NO inventa descuentos;
- NO aprueba acciones;
- NO ejecuta acciones de manera autónoma;
- NO cambia su estado.
"""

from __future__ import annotations

from typing import Literal

from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from .context_nodes import (
    extraer_contexto,
)

from .mcp_nodes import (
    consultar_acciones_comerciales_mcp,
    consultar_cambios_precio_mcp,
    consultar_detalle_mcp,
)

from .nodes import (
    clasificar_intencion,
    validar_entrada,
)

from .state import (
    EstadoDeteccion,
)


# ============================================================
# ROUTING 1
# DESPUÉS DE VALIDAR ENTRADA
# ============================================================

def ruta_despues_validacion(
    estado: EstadoDeteccion,
) -> Literal[
    "continuar",
    "bloqueada",
]:
    """
    Determina si la consulta puede continuar.

    Si el guardrail marcó la entrada como bloqueada,
    el flujo termina antes de:

    - clasificación;
    - extracción de contexto;
    - MCP;
    - SQLite.
    """

    if estado.get(
        "bloqueado",
        False,
    ):
        return "bloqueada"

    return "continuar"


# ============================================================
# ROUTING 2
# DESPUÉS DE CLASIFICAR INTENCIÓN
# ============================================================

def ruta_despues_clasificacion(
    estado: EstadoDeteccion,
) -> Literal[
    "vencimiento",
    "cambio_precio",
    "accion_comercial",
    "auditoria_completa",
    "otro",
]:
    """
    Selecciona la rama principal de negocio.
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

    if intencion == "AUDITORIA_COMPLETA":
        return "auditoria_completa"

    return "otro"


# ============================================================
# ROUTING 3
# DESPUÉS DE EXTRAER CONTEXTO
# ============================================================

def ruta_despues_contexto(
    estado: EstadoDeteccion,
) -> Literal[
    "detalle",
    "precio",
    "accion",
    "auditoria",
    "sin_producto",
    "otro",
]:
    """
    Selecciona qué nodo MCP debe ejecutarse
    después de extraer producto y tienda.

    Para AUDITORIA_COMPLETA se comienza
    por consultar_detalle_mcp.
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

    if intencion == "AUDITORIA_COMPLETA":
        return "auditoria"

    return "otro"


# ============================================================
# ROUTING 4
# DESPUÉS DE CONSULTAR DETALLE
# ============================================================

def ruta_despues_detalle(
    estado: EstadoDeteccion,
) -> Literal[
    "continuar_a_precio",
    "fin",
]:
    """
    En una consulta normal de vencimiento,
    el detalle termina el flujo.

    En AUDITORIA_COMPLETA continúa hacia
    cambios de precio.
    """

    if (
        estado.get("intencion")
        == "AUDITORIA_COMPLETA"
    ):
        return "continuar_a_precio"

    return "fin"


# ============================================================
# ROUTING 5
# DESPUÉS DE CONSULTAR CAMBIOS DE PRECIO
# ============================================================

def ruta_despues_precio(
    estado: EstadoDeteccion,
) -> Literal[
    "continuar_a_accion",
    "fin",
]:
    """
    En una consulta normal de cambio de precio,
    termina el flujo.

    En AUDITORIA_COMPLETA continúa hacia
    acciones comerciales.
    """

    if (
        estado.get("intencion")
        == "AUDITORIA_COMPLETA"
    ):
        return "continuar_a_accion"

    return "fin"


# ============================================================
# GRAFO BASE
# ============================================================

def construir_grafo_basico():
    """
    Grafo mínimo de referencia.

    START
      ↓
    validar_entrada
      ↓
    clasificar_intencion
      ↓
    END

    Se conserva como baseline técnico.
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
            "continuar":
                "clasificar_intencion",

            "bloqueada":
                END,
        },
    )

    builder.add_edge(
        "clasificar_intencion",
        END,
    )

    return builder.compile()


# ============================================================
# GRAFO PRINCIPAL
# LANGGRAPH + MCP
# ============================================================

def construir_grafo_mcp():
    """
    Construye el StateGraph principal.

    ==========================================================
    SEGURIDAD
    ==========================================================

    START
        ↓
    validar_entrada
        │
        ├── bloqueada → END
        │
        └── continuar
                ↓
        clasificar_intencion

    ==========================================================
    VENCIMIENTO
    ==========================================================

    clasificar_intencion
        ↓
    extraer_contexto
        ↓
    consultar_detalle_mcp
        ↓
    END

    ==========================================================
    CAMBIO_PRECIO
    ==========================================================

    clasificar_intencion
        ↓
    extraer_contexto
        ↓
    consultar_cambios_precio_mcp
        ↓
    END

    ==========================================================
    ACCION_COMERCIAL
    ==========================================================

    clasificar_intencion
        ↓
    extraer_contexto
        ↓
    consultar_acciones_comerciales_mcp
        ↓
    END

    ==========================================================
    AUDITORIA_COMPLETA
    ==========================================================

    clasificar_intencion
        ↓
    extraer_contexto
        ↓
    consultar_detalle_mcp
        ↓
    consultar_cambios_precio_mcp
        ↓
    consultar_acciones_comerciales_mcp
        ↓
    END
    """

    builder = StateGraph(
        EstadoDeteccion
    )

    # ========================================================
    # NODOS
    # ========================================================

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

    # ========================================================
    # START
    # ========================================================

    builder.add_edge(
        START,
        "validar_entrada",
    )

    # ========================================================
    # GUARDRAIL
    # ========================================================

    builder.add_conditional_edges(
        "validar_entrada",
        ruta_despues_validacion,
        {
            "continuar":
                "clasificar_intencion",

            "bloqueada":
                END,
        },
    )

    # ========================================================
    # CLASIFICACIÓN
    # ========================================================

    builder.add_conditional_edges(
        "clasificar_intencion",
        ruta_despues_clasificacion,
        {
            "vencimiento":
                "extraer_contexto",

            "cambio_precio":
                "extraer_contexto",

            "accion_comercial":
                "extraer_contexto",

            "auditoria_completa":
                "extraer_contexto",

            "otro":
                END,
        },
    )

    # ========================================================
    # CONTEXTO + SELECCIÓN INICIAL
    # ========================================================

    builder.add_conditional_edges(
        "extraer_contexto",
        ruta_despues_contexto,
        {
            # Consulta simple de vencimiento.
            "detalle":
                "consultar_detalle_mcp",

            # Consulta simple de precio.
            "precio":
                "consultar_cambios_precio_mcp",

            # Consulta simple de acción comercial.
            "accion":
                "consultar_acciones_comerciales_mcp",

            # Auditoría:
            # comienza por detalle.
            "auditoria":
                "consultar_detalle_mcp",

            # No llamar MCP si falta producto.
            "sin_producto":
                END,

            "otro":
                END,
        },
    )

    # ========================================================
    # DESPUÉS DE DETALLE
    # ========================================================

    builder.add_conditional_edges(
        "consultar_detalle_mcp",
        ruta_despues_detalle,
        {
            # Auditoría continúa.
            "continuar_a_precio":
                "consultar_cambios_precio_mcp",

            # Vencimiento simple termina.
            "fin":
                END,
        },
    )

    # ========================================================
    # DESPUÉS DE PRECIO
    # ========================================================

    builder.add_conditional_edges(
        "consultar_cambios_precio_mcp",
        ruta_despues_precio,
        {
            # Auditoría continúa.
            "continuar_a_accion":
                "consultar_acciones_comerciales_mcp",

            # Cambio de precio simple termina.
            "fin":
                END,
        },
    )

    # ========================================================
    # DESPUÉS DE ACCIÓN COMERCIAL
    # ========================================================

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