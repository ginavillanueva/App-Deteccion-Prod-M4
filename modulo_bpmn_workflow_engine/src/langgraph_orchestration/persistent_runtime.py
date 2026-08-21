"""
Runtime persistente de LangGraph para App Detección Prod.

Este módulo conecta:

- EstadoDeteccion;
- StateGraph;
- AsyncSqliteSaver;
- configurable.thread_id;
- checkpoints persistentes;
- pausa controlada;
- reanudación desde checkpoints.

Permite:

1. ejecutar el workflow con checkpoints;
2. recuperar el último estado persistido;
3. consultar el historial de checkpoints;
4. comprobar si existe estado;
5. pausar antes de un nodo específico;
6. reanudar una ejecución previamente pausada.

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
    interrupt_before: list[str] | None = None,
):
    """
    Recompila el mismo StateGraph utilizado por la aplicación
    agregando persistencia SQLite.

    Opcionalmente permite pausar el grafo antes de determinados
    nodos mediante interrupt_before.

    El grafo funcional no se duplica:
    reutilizamos el builder de grafo_mcp.
    """

    if interrupt_before:

        return grafo_mcp.builder.compile(
            checkpointer=checkpointer,
            interrupt_before=interrupt_before,
        )

    return grafo_mcp.builder.compile(
        checkpointer=checkpointer,
    )


# ============================================================
# EJECUCIÓN PERSISTENTE NORMAL
# ============================================================

async def ejecutar_persistente(
    pregunta: str,
    thread_id: str,
) -> dict[str, Any]:
    """
    Ejecuta App Detección Prod usando checkpoints persistentes.

    Cada thread_id identifica una ejecución persistente
    de LangGraph.
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
# EJECUCIÓN CON PAUSA
# ============================================================

async def ejecutar_hasta_pausa(
    pregunta: str,
    thread_id: str,
    interrupt_before: list[str],
) -> dict[str, Any]:
    """
    Ejecuta el workflow hasta alcanzar uno de los nodos
    indicados en interrupt_before.

    El estado queda persistido en SQLite y puede ser
    reanudado posteriormente desde otro proceso Python.

    Ejemplo:

        resultado = await ejecutar_hasta_pausa(
            pregunta="Cuantos dias faltan ...",
            thread_id="sala12-pausa-001",
            interrupt_before=[
                "consultar_detalle_mcp"
            ],
        )

    El nodo indicado NO se ejecuta todavía.

    La respuesta incluye:

    - values: estado persistido;
    - next: nodos pendientes;
    - metadata: metadata del checkpoint.
    """

    if not interrupt_before:
        raise ValueError(
            "interrupt_before debe contener al menos un nodo."
        )

    config = crear_config_checkpoint(
        thread_id
    )

    estado = crear_estado_inicial(
        pregunta,
        thread_id,
    )

    async with abrir_checkpointer_langgraph() as checkpointer:

        grafo = _compilar_grafo_persistente(
            checkpointer,
            interrupt_before=interrupt_before,
        )

        await grafo.ainvoke(
            estado,
            config=config,
        )

        snapshot = await grafo.aget_state(
            config
        )

        return {
            "values": dict(
                snapshot.values or {}
            ),
            "next": list(
                snapshot.next or ()
            ),
            "metadata": dict(
                snapshot.metadata or {}
            ),
        }


# ============================================================
# REANUDACIÓN
# ============================================================

async def reanudar_persistente(
    thread_id: str,
) -> dict[str, Any]:
    """
    Reanuda un workflow previamente persistido.

    IMPORTANTE:

    No crea un nuevo estado inicial.

    No vuelve a ejecutar el workflow desde __start__.

    LangGraph utiliza el checkpoint asociado al thread_id
    y continúa desde el nodo pendiente.

    Internamente se utiliza:

        await grafo.ainvoke(
            None,
            config=config,
        )
    """

    config = crear_config_checkpoint(
        thread_id
    )

    async with abrir_checkpointer_langgraph() as checkpointer:

        grafo = _compilar_grafo_persistente(
            checkpointer
        )

        snapshot_antes = await grafo.aget_state(
            config
        )

        if not snapshot_antes.values:
            raise ValueError(
                "No existe un checkpoint persistido "
                f"para thread_id={thread_id!r}."
            )

        resultado = await grafo.ainvoke(
            None,
            config=config,
        )

    return dict(
        resultado
    )


# ============================================================
# INFORMACIÓN DEL CHECKPOINT
# ============================================================

async def obtener_checkpoint_persistido(
    thread_id: str,
) -> dict[str, Any]:
    """
    Recupera el checkpoint más reciente de un thread.

    A diferencia de recuperar_estado_persistido(), esta
    función también devuelve:

    - next;
    - metadata.

    Esto permite conocer si un workflow:

    - terminó: next == [];
    - está pausado: next contiene nodos pendientes.
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

        valores = dict(
            snapshot.values or {}
        )

        if not valores:
            return {}

        return {
            "values": valores,
            "next": list(
                snapshot.next or ()
            ),
            "metadata": dict(
                snapshot.metadata or {}
            ),
        }


# ============================================================
# RECUPERACIÓN DE ESTADO
# ============================================================

async def recuperar_estado_persistido(
    thread_id: str,
) -> dict[str, Any]:
    """
    Recupera el último estado almacenado para un thread_id.

    Esta función NO vuelve a ejecutar el workflow
    y NO llama MCP.

    Solo consulta los checkpoints almacenados por LangGraph.
    """

    checkpoint = await obtener_checkpoint_persistido(
        thread_id
    )

    if not checkpoint:
        return {}

    return dict(
        checkpoint.get(
            "values",
            {},
        )
    )


# ============================================================
# HISTORIAL
# ============================================================

async def obtener_historial_persistido(
    thread_id: str,
) -> list[dict[str, Any]]:
    """
    Recupera el historial de checkpoints de un thread.

    LangGraph normalmente devuelve primero el checkpoint
    más reciente y después los anteriores.
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


# ============================================================
# ESTADO DE EJECUCIÓN
# ============================================================

async def obtener_estado_ejecucion(
    thread_id: str,
) -> str:
    """
    Indica el estado general de un workflow persistido.

    Valores posibles:

    - NO_EXISTE
    - PAUSADO
    - FINALIZADO
    """

    checkpoint = await obtener_checkpoint_persistido(
        thread_id
    )

    if not checkpoint:
        return "NO_EXISTE"

    pendientes = checkpoint.get(
        "next",
        [],
    )

    if pendientes:
        return "PAUSADO"

    return "FINALIZADO"