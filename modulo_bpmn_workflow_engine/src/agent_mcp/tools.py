"""Herramientas locales del agente de App Detección Prod."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date, timedelta
from typing import Any

from ..tool_calling.database import (
    get_connection,
    initialize_database,
)


ToolResult = dict[str, Any]
ToolFunction = Callable[..., ToolResult]


def _rows_to_dicts(rows: Any) -> list[dict[str, Any]]:
    """Convierte filas SQLite en diccionarios serializables."""
    return [dict(row) for row in rows]


def _build_result(
    *,
    tool_name: str,
    source_tables: tuple[str, ...],
    rows: Any,
) -> ToolResult:
    """Construye una respuesta homogénea para todas las herramientas."""
    serialized_rows = _rows_to_dicts(rows)

    return {
        "tool_name": tool_name,
        "source_tables": list(source_tables),
        "row_count": len(serialized_rows),
        "rows": serialized_rows,
    }


def buscar_productos_proximos_a_vencer(
    dias: int = 45,
    tienda: str | None = None,
) -> ToolResult:
    """
    Consulta productos que vencerán dentro del número de días indicado.

    Puede limitar opcionalmente la consulta a una tienda o sala.
    """
    if dias < 1 or dias > 365:
        raise ValueError(
            "El parámetro dias debe estar entre 1 y 365."
        )

    initialize_database()

    today = date.today()
    cutoff_date = today + timedelta(days=dias)

    conditions = [
        "fecha_vencimiento BETWEEN :today AND :cutoff_date"
    ]

    parameters: dict[str, Any] = {
        "today": today.isoformat(),
        "cutoff_date": cutoff_date.isoformat(),
    }

    if tienda and tienda.strip():
        conditions.append(
            "LOWER(tienda) LIKE LOWER(:tienda)"
        )
        parameters["tienda"] = f"%{tienda.strip()}%"

    where_clause = " AND ".join(conditions)

    with get_connection() as connection:
        rows = connection.execute(
            f"""
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
            WHERE {where_clause}
            ORDER BY fecha_vencimiento ASC, producto ASC
            """,
            parameters,
        ).fetchall()

    return _build_result(
        tool_name="buscar_productos_proximos_a_vencer",
        source_tables=("productos_vencimiento",),
        rows=rows,
    )


def consultar_detalle_producto(
    producto: str,
    tienda: str | None = None,
) -> ToolResult:
    """
    Consulta el detalle registrado de un producto específico.

    Devuelve tienda, vencimiento, cantidad, precio actual,
    estado y evidencia disponible.
    """
    clean_product = producto.strip()

    if not clean_product:
        raise ValueError(
            "El nombre del producto no puede estar vacío."
        )

    initialize_database()

    conditions = [
        "LOWER(producto) LIKE LOWER(:producto)"
    ]

    parameters: dict[str, Any] = {
        "producto": f"%{clean_product}%",
        "today": date.today().isoformat(),
    }

    if tienda and tienda.strip():
        conditions.append(
            "LOWER(tienda) LIKE LOWER(:tienda)"
        )
        parameters["tienda"] = f"%{tienda.strip()}%"

    where_clause = " AND ".join(conditions)

    with get_connection() as connection:
        rows = connection.execute(
            f"""
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
            WHERE {where_clause}
            ORDER BY producto ASC, tienda ASC
            """,
            parameters,
        ).fetchall()

    return _build_result(
        tool_name="consultar_detalle_producto",
        source_tables=("productos_vencimiento",),
        rows=rows,
    )


def consultar_cambios_precio(
    producto: str,
    tienda: str | None = None,
) -> ToolResult:
    """
    Consulta cambios de precio registrados para un producto.

    Es una herramienta únicamente informativa y de trazabilidad.
    No aprueba, rechaza ni modifica precios.
    """
    clean_product = producto.strip()

    if not clean_product:
        raise ValueError(
            "El nombre del producto no puede estar vacío."
        )

    initialize_database()

    conditions = [
        "LOWER(pv.producto) LIKE LOWER(:producto)"
    ]

    parameters: dict[str, Any] = {
        "producto": f"%{clean_product}%"
    }

    if tienda and tienda.strip():
        conditions.append(
            "LOWER(pv.tienda) LIKE LOWER(:tienda)"
        )
        parameters["tienda"] = f"%{tienda.strip()}%"

    where_clause = " AND ".join(conditions)

    with get_connection() as connection:
        rows = connection.execute(
            f"""
            SELECT
                cp.id,
                pv.producto,
                pv.tienda,
                cp.precio_anterior,
                cp.precio_nuevo,
                ROUND(
                    cp.precio_nuevo - cp.precio_anterior,
                    2
                ) AS variacion_precio,
                cp.solicitado_por AS registrado_por,
                cp.fecha_solicitud AS fecha_registro
            FROM cambios_precio AS cp
            INNER JOIN productos_vencimiento AS pv
                ON pv.id = cp.producto_id
            WHERE {where_clause}
            ORDER BY cp.fecha_solicitud DESC, cp.id DESC
            """,
            parameters,
        ).fetchall()

    return _build_result(
        tool_name="consultar_cambios_precio",
        source_tables=(
            "cambios_precio",
            "productos_vencimiento",
        ),
        rows=rows,
    )


def consultar_acciones_comerciales(
    producto: str,
    tienda: str | None = None,
    estado: str | None = None,
) -> ToolResult:
    """
    Consulta acciones comerciales registradas para un producto.

    Incluye descuentos, bandeos, retiros u otras acciones,
    junto con su estado, responsable, fecha y evidencia disponible.
    """
    clean_product = producto.strip()

    if not clean_product:
        raise ValueError(
            "El nombre del producto no puede estar vacío."
        )

    initialize_database()

    conditions = [
        "LOWER(pv.producto) LIKE LOWER(:producto)"
    ]

    parameters: dict[str, Any] = {
        "producto": f"%{clean_product}%"
    }

    if tienda and tienda.strip():
        conditions.append(
            "LOWER(pv.tienda) LIKE LOWER(:tienda)"
        )
        parameters["tienda"] = f"%{tienda.strip()}%"

    if estado and estado.strip():
        conditions.append(
            "LOWER(ac.estado) = LOWER(:estado)"
        )
        parameters["estado"] = estado.strip()

    where_clause = " AND ".join(conditions)

    with get_connection() as connection:
        rows = connection.execute(
            f"""
            SELECT
                ac.id,
                pv.producto,
                pv.tienda,
                ac.tipo_accion,
                ac.estado,
                ac.responsable,
                ac.fecha_registro,
                pv.evidencia AS evidencia_producto
            FROM acciones_comerciales AS ac
            INNER JOIN productos_vencimiento AS pv
                ON pv.id = ac.producto_id
            WHERE {where_clause}
            ORDER BY ac.fecha_registro DESC, ac.id DESC
            """,
            parameters,
        ).fetchall()

    return _build_result(
        tool_name="consultar_acciones_comerciales",
        source_tables=(
            "acciones_comerciales",
            "productos_vencimiento",
        ),
        rows=rows,
    )


AGENT_TOOL_FUNCTIONS: dict[str, ToolFunction] = {
    "buscar_productos_proximos_a_vencer":
        buscar_productos_proximos_a_vencer,
    "consultar_detalle_producto":
        consultar_detalle_producto,
    "consultar_cambios_precio":
        consultar_cambios_precio,
    "consultar_acciones_comerciales":
        consultar_acciones_comerciales,
}


AGENT_TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "buscar_productos_proximos_a_vencer",
            "description": (
                "Consulta productos próximos a vencer. "
                "Devuelve vencimiento, días restantes, cantidad, "
                "precio actual, tienda, estado y evidencia."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "dias": {
                        "type": "integer",
                        "description": (
                            "Cantidad de días hacia adelante. "
                            "Por defecto 45."
                        ),
                        "minimum": 1,
                        "maximum": 365,
                    },
                    "tienda": {
                        "type": "string",
                        "description": (
                            "Nombre opcional de tienda o sala."
                        ),
                    },
                },
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_detalle_producto",
            "description": (
                "Consulta el registro de un producto específico, "
                "incluyendo vencimiento, cantidad, precio actual, "
                "estado, tienda y evidencia."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "producto": {
                        "type": "string",
                        "description": (
                            "Nombre del producto que se desea consultar."
                        ),
                    },
                    "tienda": {
                        "type": "string",
                        "description": (
                            "Nombre opcional de tienda o sala."
                        ),
                    },
                },
                "required": ["producto"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_cambios_precio",
            "description": (
                "Consulta cambios de precio ya registrados en sala "
                "para un producto. Es solo informativa y de "
                "trazabilidad. No aprueba, rechaza ni modifica precios."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "producto": {
                        "type": "string",
                        "description": (
                            "Nombre del producto cuyos cambios "
                            "de precio se desean consultar."
                        ),
                    },
                    "tienda": {
                        "type": "string",
                        "description": (
                            "Nombre opcional de tienda o sala."
                        ),
                    },
                },
                "required": ["producto"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_acciones_comerciales",
            "description": (
                "Consulta acciones comerciales registradas para "
                "un producto, como descuentos, bandeos o retiros, "
                "junto con estado, responsable y evidencia."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "producto": {
                        "type": "string",
                        "description": (
                            "Nombre del producto."
                        ),
                    },
                    "tienda": {
                        "type": "string",
                        "description": (
                            "Nombre opcional de tienda o sala."
                        ),
                    },
                    "estado": {
                        "type": "string",
                        "description": (
                            "Estado opcional de la acción comercial, "
                            "por ejemplo PENDIENTE o COMPLETADA."
                        ),
                    },
                },
                "required": ["producto"],
                "additionalProperties": False,
            },
        },
    },
]


def execute_agent_tool(
    tool_name: str,
    arguments: dict[str, Any] | None = None,
) -> ToolResult:
    """Ejecuta únicamente una herramienta publicada del agente."""
    try:
        tool_function = AGENT_TOOL_FUNCTIONS[tool_name]
    except KeyError as exc:
        available = ", ".join(AGENT_TOOL_FUNCTIONS)

        raise ValueError(
            f"Herramienta no autorizada: {tool_name}. "
            f"Disponibles: {available}"
        ) from exc

    safe_arguments = arguments or {}

    if not isinstance(safe_arguments, dict):
        raise ValueError(
            "Los argumentos de la herramienta deben ser un objeto JSON."
        )

    return tool_function(**safe_arguments)


def published_agent_tool_names() -> tuple[str, ...]:
    """Devuelve los nombres de las herramientas del nuevo agente."""
    return tuple(AGENT_TOOL_FUNCTIONS)