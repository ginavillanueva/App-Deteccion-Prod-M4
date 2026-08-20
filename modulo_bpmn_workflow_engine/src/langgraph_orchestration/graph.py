"""
Primer StateGraph funcional de App Detección Prod.

Este grafo representa la primera etapa de la orquestación Nivel 5.

Flujo:

START
  ↓
validar_entrada
  ├── bloqueada → END
  └── continuar
          ↓
   clasificar_intencion
          ↓
         END

Todavía no utiliza:
- Ollama
- MCP
- SQLite de negocio
- checkpoints

El objetivo de esta etapa es demostrar:
- estado explícito;
- nodos independientes;
- routing condicional;
- ejecución reproducible mediante LangGraph.
"""

from __future__ import annotations

from typing import Literal

from langgraph.graph import END, START, StateGraph

from .nodes import clasificar_intencion, validar_entrada
from .state import EstadoDeteccion


# ============================================================
# ROUTING
# ============================================================

def ruta_despues_validacion(
    estado: EstadoDeteccion,
) -> Literal["continuar", "bloqueada"]:
    """
    Decide qué camino toma el grafo después del guardrail.

    Si la entrada está bloqueada:
        LangGraph finaliza inmediatamente.

    Si la entrada es válida:
        continúa hacia la clasificación de intención.
    """

    if estado.get("bloqueado", False):
        return "bloqueada"

    return "continuar"


# ============================================================
# CONSTRUCCIÓN DEL GRAFO
# ============================================================

def construir_grafo_basico():
    """
    Construye y compila el primer StateGraph del proyecto.

    En esta versión todavía no se utiliza un checkpointer.
    La persistencia se incorporará en una etapa posterior.
    """

    builder = StateGraph(EstadoDeteccion)

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

    # --------------------------------------------------------
    # Inicio
    # --------------------------------------------------------

    builder.add_edge(
        START,
        "validar_entrada",
    )

    # --------------------------------------------------------
    # Rama condicional
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
    # Fin de la ruta válida
    # --------------------------------------------------------

    builder.add_edge(
        "clasificar_intencion",
        END,
    )

    return builder.compile()


# ============================================================
# INSTANCIA REUTILIZABLE
# ============================================================

grafo_basico = construir_grafo_basico()
