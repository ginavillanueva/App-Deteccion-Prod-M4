"""
Grafos LangGraph de App Detección Prod.

Este módulo mantiene:

1. grafo_basico
   - validación
   - clasificación
   - routing de seguridad

2. grafo_mcp
   - validación
   - clasificación
   - extracción determinística de contexto
   - routing por intención
   - herramientas MCP reales

Flujo de vencimiento:

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
"""

from __future__ import annotations

from typing import Literal

from langgraph.graph import END, START, StateGraph

from .context_nodes import extraer_contexto
from .mcp_nodes import consultar_detalle_mcp
from .nodes import clasificar_intencion, validar_entrada
from .state import EstadoDeteccion


# ============================================================
# ROUTING DE SEGURIDAD
# ============================================================

def ruta_despues_validacion(
    estado: EstadoDeteccion,
) -> Literal["continuar", "bloqueada"]:
    """
    Decide si la consulta puede continuar.

    Las consultas bloqueadas terminan antes de ejecutar
    clasificación, MCP o cualquier herramienta.
    """

    if estado.get("bloqueado", False):
        return "bloqueada"

    return "continuar"


# ============================================================
# ROUTING DE NEGOCIO
# ============================================================

def ruta_despues_clasificacion(
    estado: EstadoDeteccion,
) -> Literal[
    "vencimiento",
    "otro",
]:
    """
    Selecciona la rama de negocio.

    Por ahora solamente VENCIMIENTO está conectado
    al flujo completo mediante MCP.
    """

    intencion = estado.get(
        "intencion",
        "OTRO",
    )

    if intencion == "VENCIMIENTO":
        return "vencimiento"

    return "otro"


# ============================================================
# ROUTING DESPUÉS DE EXTRAER CONTEXTO
# ============================================================

def ruta_despues_contexto(
    estado: EstadoDeteccion,
) -> Literal[
    "consultar",
    "sin_producto",
]:
    """
    Comprueba que exista un producto antes de llamar MCP.

    Esto evita ejecutar tools/call con argumentos incompletos.
    """

    producto = estado.get(
        "producto",
        "",
    ).strip()

    if not producto:
        return "sin_producto"

    return "consultar"


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
    StateGraph conectado al Nivel 4 mediante MCP.

    Para la intención VENCIMIENTO:

    validar_entrada
        ↓
    clasificar_intencion
        ↓
    extraer_contexto
        ↓
    consultar_detalle_mcp
        ↓
    END

    Producto y tienda se obtienen automáticamente desde
    la pregunta del usuario.

    No existe SQL dentro de esta capa.
    """

    builder = StateGraph(
        EstadoDeteccion
    )

    # --------------------------------------------------------
    # Nodos
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

    # --------------------------------------------------------
    # Inicio
    # --------------------------------------------------------

    builder.add_edge(
        START,
        "validar_entrada",
    )

    # --------------------------------------------------------
    # Guardrail de entrada
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
    # Routing según intención
    # --------------------------------------------------------

    builder.add_conditional_edges(
        "clasificar_intencion",
        ruta_despues_clasificacion,
        {
            "vencimiento": "extraer_contexto",
            "otro": END,
        },
    )

    # --------------------------------------------------------
    # Validación del contexto extraído
    # --------------------------------------------------------

    builder.add_conditional_edges(
        "extraer_contexto",
        ruta_despues_contexto,
        {
            "consultar": "consultar_detalle_mcp",
            "sin_producto": END,
        },
    )

    # --------------------------------------------------------
    # Fin de la rama MCP
    # --------------------------------------------------------

    builder.add_edge(
        "consultar_detalle_mcp",
        END,
    )

    return builder.compile()


# ============================================================
# INSTANCIAS REUTILIZABLES
# ============================================================

grafo_basico = construir_grafo_basico()

grafo_mcp = construir_grafo_mcp()