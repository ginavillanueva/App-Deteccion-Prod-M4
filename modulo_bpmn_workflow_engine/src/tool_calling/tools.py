"""Herramientas autorizadas para consultar datos de App Detección Prod."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from .database import get_connection, initialize_database


LISTAR_PRODUCTOS_PROXIMOS_A_VENCER = (
    "LISTAR_PRODUCTOS_PROXIMOS_A_VENCER"
)

LISTAR_CAMBIOS_PRECIO_PENDIENTES = (
    "LISTAR_CAMBIOS_PRECIO_PENDIENTES"
)

LISTAR_ACCIONES_COMERCIALES_PENDIENTES = (
    "LISTAR_ACCIONES_COMERCIALES_PENDIENTES"
)


@dataclass(frozen=True)
class ToolExecution:
    """
    Resultado producido por una herramienta del sistema.

    La respuesta final será construida posteriormente por Python,
    utilizando exclusivamente las filas recuperadas desde SQLite.
    """

    tool_name: str
    source_tables: tuple[str, ...]
    rows: tuple[dict[str, Any], ...]

    @property
    def row_count(self) -> int:
        """Cantidad de registros devueltos por la herramienta."""
        return len(self.rows)

    @property
    def source_label(self) -> str:
        """Nombres de las tablas utilizados como fuente."""
        return ", ".join(self.source_tables)


def rows_to_dicts(
    rows: Iterable[Any],
) -> tuple[dict[str, Any], ...]:
    """Convierte filas SQLite en diccionarios serializables."""
    return tuple(dict(row) for row in rows)


def listar_productos_proximos_a_vencer() -> ToolExecution:
    """
    Consulta productos cuya fecha de vencimiento está dentro de 45 días.

    Herramienta:
        LISTAR_PRODUCTOS_PROXIMOS_A_VENCER

    Fuente:
        productos_vencimiento
    """
    initialize_database()

    today = date.today()
    cutoff_date = today + timedelta(days=45)

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                producto,
                tienda,
                fecha_vencimiento,
                CAST(
                    julianday(fecha_vencimiento)
                    - julianday(:today)
                    AS INTEGER
                ) AS dias_restantes,
                cantidad,
                precio_actual,
                estado,
                evidencia
            FROM productos_vencimiento
            WHERE fecha_vencimiento
                BETWEEN :today AND :cutoff_date
            ORDER BY fecha_vencimiento ASC, producto ASC
            """,
            {
                "today": today.isoformat(),
                "cutoff_date": cutoff_date.isoformat(),
            },
        ).fetchall()

    return ToolExecution(
        tool_name=LISTAR_PRODUCTOS_PROXIMOS_A_VENCER,
        source_tables=("productos_vencimiento",),
        rows=rows_to_dicts(rows),
    )


def listar_cambios_precio_pendientes() -> ToolExecution:
    """
    Consulta solicitudes de cambio de precio pendientes de aprobación.

    Herramienta:
        LISTAR_CAMBIOS_PRECIO_PENDIENTES

    Fuentes:
        cambios_precio
        productos_vencimiento
    """
    initialize_database()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                cp.id,
                pv.producto,
                pv.tienda,
                cp.precio_anterior,
                cp.precio_nuevo,
                cp.estado_aprobacion,
                cp.solicitado_por,
                cp.fecha_solicitud
            FROM cambios_precio AS cp
            INNER JOIN productos_vencimiento AS pv
                ON pv.id = cp.producto_id
            WHERE cp.estado_aprobacion = 'PENDIENTE'
            ORDER BY cp.fecha_solicitud ASC, pv.producto ASC
            """
        ).fetchall()

    return ToolExecution(
        tool_name=LISTAR_CAMBIOS_PRECIO_PENDIENTES,
        source_tables=(
            "cambios_precio",
            "productos_vencimiento",
        ),
        rows=rows_to_dicts(rows),
    )


def listar_acciones_comerciales_pendientes() -> ToolExecution:
    """
    Consulta acciones comerciales todavía pendientes de ejecución.

    Herramienta:
        LISTAR_ACCIONES_COMERCIALES_PENDIENTES

    Fuentes:
        acciones_comerciales
        productos_vencimiento
    """
    initialize_database()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                ac.id,
                pv.producto,
                pv.tienda,
                ac.tipo_accion,
                ac.estado,
                ac.responsable,
                ac.fecha_registro
            FROM acciones_comerciales AS ac
            INNER JOIN productos_vencimiento AS pv
                ON pv.id = ac.producto_id
            WHERE ac.estado = 'PENDIENTE'
            ORDER BY ac.fecha_registro ASC, pv.producto ASC
            """
        ).fetchall()

    return ToolExecution(
        tool_name=LISTAR_ACCIONES_COMERCIALES_PENDIENTES,
        source_tables=(
            "acciones_comerciales",
            "productos_vencimiento",
        ),
        rows=rows_to_dicts(rows),
    )


ToolFunction = Callable[[], ToolExecution]


PUBLISHED_TOOLS: dict[str, ToolFunction] = {
    LISTAR_PRODUCTOS_PROXIMOS_A_VENCER:
        listar_productos_proximos_a_vencer,

    LISTAR_CAMBIOS_PRECIO_PENDIENTES:
        listar_cambios_precio_pendientes,

    LISTAR_ACCIONES_COMERCIALES_PENDIENTES:
        listar_acciones_comerciales_pendientes,
}


def execute_tool(tool_name: str) -> ToolExecution:
    """
    Ejecuta únicamente una herramienta publicada y autorizada.

    El nombre debe coincidir exactamente con una herramienta
    registrada en PUBLISHED_TOOLS.
    """
    try:
        tool_function = PUBLISHED_TOOLS[tool_name]
    except KeyError as exc:
        available = ", ".join(PUBLISHED_TOOLS)

        raise ValueError(
            f"Herramienta no autorizada: {tool_name}. "
            f"Herramientas disponibles: {available}"
        ) from exc

    return tool_function()


def published_tool_names() -> tuple[str, ...]:
    """Devuelve los nombres de las herramientas publicadas."""
    return tuple(PUBLISHED_TOOLS)