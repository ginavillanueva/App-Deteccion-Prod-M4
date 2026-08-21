"""
Persistencia de checkpoints LangGraph para App Detección Prod.

Este módulo es independiente de SQLiteWorkflowRepository.

Responsabilidades
-----------------
SQLiteWorkflowRepository
    Persiste el estado operacional del motor BPMN:
    - definiciones;
    - instancias;
    - tareas;
    - trazas;
    - incidentes;
    - workers.

AsyncSqliteSaver
    Persiste checkpoints nativos de LangGraph:
    - estado del StateGraph;
    - historial de ejecución;
    - checkpoints;
    - continuidad por thread_id;
    - recuperación entre procesos.

La separación evita mezclar:

datos de negocio / BPMN

con

memoria interna de LangGraph.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


# ============================================================
# RUTAS
# ============================================================

# Archivo actual:
#
# src/persistence/langgraph_checkpointer.py
#
# parents[0] = persistence
# parents[1] = src
# parents[2] = raíz de modulo_bpmn_workflow_engine

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

LANGGRAPH_CHECKPOINT_DB = (
    DATA_DIR / "langgraph_checkpoints.sqlite"
)


# ============================================================
# UTILIDADES
# ============================================================

def obtener_ruta_checkpoint() -> Path:
    """
    Devuelve la ruta absoluta de la base SQLite
    utilizada exclusivamente por LangGraph.
    """

    return LANGGRAPH_CHECKPOINT_DB


def asegurar_directorio_checkpoint() -> Path:
    """
    Garantiza que exista el directorio data/.

    No crea todavía la base SQLite.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return DATA_DIR


def obtener_connection_string() -> str:
    """
    Devuelve el connection string que utilizará
    AsyncSqliteSaver.
    """

    asegurar_directorio_checkpoint()

    return str(
        LANGGRAPH_CHECKPOINT_DB
    )


# ============================================================
# CHECKPOINTER LANGGRAPH
# ============================================================

@asynccontextmanager
async def abrir_checkpointer_langgraph(
) -> AsyncIterator[AsyncSqliteSaver]:
    """
    Abre un AsyncSqliteSaver correctamente.

    Uso esperado:

        async with abrir_checkpointer_langgraph() as checkpointer:
            ...

    Dentro de este contexto el checkpointer permanece
    conectado a SQLite.

    Al salir del contexto la conexión se cierra
    correctamente.
    """

    connection_string = obtener_connection_string()

    async with AsyncSqliteSaver.from_conn_string(
        connection_string
    ) as checkpointer:

        # Inicializa las tablas internas requeridas
        # por LangGraph si todavía no existen.
        await checkpointer.setup()

        yield checkpointer


# ============================================================
# CONFIGURACIÓN LANGGRAPH
# ============================================================

def crear_config_checkpoint(
    thread_id: str,
) -> dict:
    """
    Construye la configuración requerida por LangGraph
    para asociar una ejecución a un thread persistente.

    Ejemplo resultante:

    {
        "configurable": {
            "thread_id": "sala12-001"
        }
    }
    """

    thread_limpio = thread_id.strip()

    if not thread_limpio:
        raise ValueError(
            "thread_id no puede estar vacío."
        )

    return {
        "configurable": {
            "thread_id": thread_limpio,
        }
    }