"""
Estado compartido del flujo LangGraph de App Detección Prod.

El estado representa la información que puede circular entre los nodos
del grafo durante una ejecución.

Las listas que deben acumular información utilizan reducers explícitos
mediante Annotated + operator.add.
"""

from __future__ import annotations

import operator
from typing import Annotated, Any, Literal, TypedDict


# ============================================================
# INTENCIONES DE NEGOCIO
# ============================================================

IntentType = Literal[
    "VENCIMIENTO",
    "CAMBIO_PRECIO",
    "ACCION_COMERCIAL",
    "AUDITORIA_COMPLETA",
    "OTRO",
]


# ============================================================
# EVENTOS DE TRAZA
# ============================================================

class TraceEvent(TypedDict, total=False):
    """
    Evento individual registrado durante la ejecución del grafo.
    """

    nodo: str
    tipo: str
    mensaje: str
    detalle: dict[str, Any]


# ============================================================
# ESTADO PRINCIPAL DE LANGGRAPH
# ============================================================

class EstadoDeteccion(TypedDict, total=False):
    """
    Estado compartido entre todos los nodos de LangGraph.

    Los campos con Annotated[..., operator.add] se acumulan
    automáticamente cuando distintos nodos devuelven nuevas listas.
    """

    # --------------------------------------------------------
    # Entrada e identificación
    # --------------------------------------------------------

    pregunta: str
    thread_id: str

    # --------------------------------------------------------
    # Información interpretada
    # --------------------------------------------------------

    intencion: IntentType
    producto: str
    tienda: str

    # --------------------------------------------------------
    # Evidencia obtenida durante el flujo
    # --------------------------------------------------------

    observaciones: Annotated[
        list[dict[str, Any]],
        operator.add,
    ]

    fuentes: Annotated[
        list[str],
        operator.add,
    ]

    tools_usadas: Annotated[
        list[str],
        operator.add,
    ]

    # --------------------------------------------------------
    # Resultado final
    # --------------------------------------------------------

    respuesta: str

    # --------------------------------------------------------
    # Información del modelo / fallback
    # --------------------------------------------------------

    modelo_usado: str
    hubo_fallback: bool

    # --------------------------------------------------------
    # Control del flujo
    # --------------------------------------------------------

    intentos: int
    bloqueado: bool
    problema: str

    # --------------------------------------------------------
    # Observabilidad
    # --------------------------------------------------------

    traza: Annotated[
        list[TraceEvent],
        operator.add,
    ]


# ============================================================
# HELPERS
# ============================================================

def crear_estado_inicial(
    pregunta: str,
    thread_id: str,
) -> EstadoDeteccion:
    """
    Construye el estado inicial de una ejecución.

    No interpreta todavía la pregunta y no llama al LLM.
    Solo inicializa la estructura que posteriormente será
    utilizada por LangGraph.
    """

    return {
        "pregunta": pregunta.strip(),
        "thread_id": thread_id.strip(),
        "intencion": "OTRO",
        "producto": "",
        "tienda": "",
        "observaciones": [],
        "fuentes": [],
        "tools_usadas": [],
        "respuesta": "",
        "modelo_usado": "",
        "hubo_fallback": False,
        "intentos": 0,
        "bloqueado": False,
        "problema": "",
        "traza": [],
    }


def nueva_traza(
    nodo: str,
    tipo: str,
    mensaje: str,
    **detalle: Any,
) -> list[TraceEvent]:
    """
    Crea una lista con un evento de traza.

    Se devuelve como lista porque LangGraph utilizará operator.add
    para acumular los eventos generados por cada nodo.
    """

    evento: TraceEvent = {
        "nodo": nodo,
        "tipo": tipo,
        "mensaje": mensaje,
    }

    if detalle:
        evento["detalle"] = detalle

    return [evento]