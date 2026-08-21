"""
Runtime persistente de LangGraph para App Detección Prod.

Este módulo conecta:

- EstadoDeteccion;
- StateGraph;
- AsyncSqliteSaver;
- configurable.thread_id.

Permite:

1. ejecutar el workflow con checkpoints;
2. recuperar el último estado persistido;
3. consultar el historial de checkpoints.

La base SQLite es administrada por:

    src.persistence.langgraph_checkpointer

Este módulo NO consulta SQLite directamente.
"""

from __future__ import annotations

from typing import Any

from src.persistence.langgraph_checkpointer import (
    abrir_checkpointer_langgraph,
    crear_config_checkpoint,
)

from .graph import grafo_mcp
from .state import crear_estado_inicial


# ============================================================
# COMPILACIÓN
# ============================================================

def _compilar_grafo_persistente(
    checkpointer: Any,
):
    """
    Recompila el mismo StateGraph utilizado por la aplicación,
    agregando el checkpointer SQLite.

    El grafo funcional no se duplica:
    reutilizamos el builder de grafo_mcp.
    """

    return grafo_mcp.builder.compile(
        checkpointer=checkpointer,
    )


# ============================================================
# EJECUCIÓN PERSISTENTE
# ============================================================

async def ejecutar_persistente(
    pregunta: str,
    thread_id: str,
) -> dict[str, Any]:
    """
    Ejecuta App Detección Prod usando checkpoints persistentes.

    Cada thread_id identifica una ejecución/conversación
    persistente de LangGraph.

    Ejemplo:

        resultado = await ejecutar_persistente(
            "Cuantos dias faltan para vencer ...",
            "sala12-001",
        )
    """

    config = crear_config_checkpoint(
        thread_id
    )

    estado = crear_estado_inicial(
        pregunta,
        thread_id,
    )

    async with abrir_checkpointer_langgraph() as checkpointer:

        grafo = _compilar_grafo_persistente(
            checkpointer
        )

        resultado = await grafo.ainvoke(
            estado,
            config=config,
        )

    return dict(
        resultado
    )


# ============================================================
# RECUPERACIÓN
# ============================================================

async def recuperar_estado_persistido(
    thread_id: str,
) -> dict[str, Any]:
    """
    Recupera el último estado almacenado para un thread_id.

    IMPORTANTE:
    esta función NO vuelve a ejecutar el workflow y NO llama MCP.

    Solo consulta los checkpoints previamente almacenados
    por LangGraph.
    """

    config = crear_config_checkpoint(
        thread_id
    )

    async with abrir_checkpointer_langgraph() as checkpointer:

        grafo = _compilar_grafo_persistente(
            checkpointer
        )

        snapshot = await grafo.aget_state(
            config
        )

        if snapshot is None:
            return {}

        return dict(
            snapshot.values or {}
        )


# ============================================================
# HISTORIAL
# ============================================================

async def obtener_historial_persistido(
    thread_id: str,
) -> list[dict[str, Any]]:
    """
    Recupera el historial de checkpoints de un thread.

    Devuelve una lista ordenada según la respuesta de
    LangGraph, normalmente desde el estado más reciente
    hacia los estados anteriores.
    """

    config = crear_config_checkpoint(
        thread_id
    )

    historial: list[dict[str, Any]] = []

    async with abrir_checkpointer_langgraph() as checkpointer:

        grafo = _compilar_grafo_persistente(
            checkpointer
        )

        async for snapshot in grafo.aget_state_history(
            config
        ):

            valores = dict(
                snapshot.values or {}
            )

            historial.append(
                {
                    "values": valores,
                    "next": list(
                        snapshot.next or ()
                    ),
                    "metadata": dict(
                        snapshot.metadata or {}
                    ),
                }
            )

    return historial


# ============================================================
# EXISTENCIA DE ESTADO
# ============================================================

async def existe_estado_persistido(
    thread_id: str,
) -> bool:
    """
    Indica si LangGraph tiene un estado persistido
    asociado al thread_id indicado.
    """

    estado = await recuperar_estado_persistido(
        thread_id
    )

    return bool(
        estado
    )