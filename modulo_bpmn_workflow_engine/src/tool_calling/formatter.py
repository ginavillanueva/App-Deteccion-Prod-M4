"""Formateo de respuestas y trazabilidad del módulo de tool calling."""

from __future__ import annotations

from typing import Any

from .router import RouteResult
from .tools import (
    LISTAR_ACCIONES_COMERCIALES_PENDIENTES,
    LISTAR_CAMBIOS_PRECIO_PENDIENTES,
    LISTAR_PRODUCTOS_PROXIMOS_A_VENCER,
)


def format_boolean(value: bool) -> str:
    """Representa un valor booleano de forma legible."""
    return "SI" if value else "NO"


def format_trace(result: RouteResult) -> str:
    """Construye la sección técnica y auditable de la ejecución."""
    lines = [
        "TRAZABILIDAD DE LA EJECUCIÓN",
        "-" * 72,
        f"PREGUNTA: {result.question}",
        f"IA HABILITADA: {format_boolean(result.ia_habilitada)}",
        f"CAMINO: {result.path}",
        f"LLM INVOCADO: {format_boolean(result.llm_invoked)}",
        f"MODELO: {result.model or 'N/A'}",
        f"HERRAMIENTA: {result.tool_name or 'NINGUNA'}",
        f"FUENTE: {result.source_label}",
        f"FILAS RECUPERADAS: {result.row_count}",
        f"ESTADO: {result.status}",
    ]

    if result.matched_phrase:
        lines.append(
            f"FRASE COINCIDENTE: {result.matched_phrase}"
        )

    if result.llm_raw_content:
        lines.append(
            f"CONTENIDO TEXTUAL DEL LLM: "
            f"{result.llm_raw_content}"
        )

    if result.successful:
        lines.extend(
            [
                "ROL DEL LLM: SOLO SELECCIÓN DE HERRAMIENTA",
                "ORIGEN DE LOS DATOS: SQLITE",
                "RESPUESTA FINAL GENERADA POR: PYTHON",
            ]
        )

    return "\n".join(lines)


def format_products(
    rows: tuple[dict[str, Any], ...],
) -> str:
    """Formatea productos próximos a vencer."""
    if not rows:
        return (
            "No se encontraron productos próximos a vencer "
            "dentro del periodo consultado."
        )

    lines = [
        (
            f"Se encontraron {len(rows)} productos próximos "
            "a vencer:"
        )
    ]

    for index, row in enumerate(rows, start=1):
        lines.extend(
            [
                "",
                f"{index}. {row['producto']}",
                f"   Tienda: {row['tienda']}",
                (
                    "   Fecha de vencimiento: "
                    f"{row['fecha_vencimiento']}"
                ),
                (
                    "   Días restantes: "
                    f"{row['dias_restantes']}"
                ),
                f"   Cantidad: {row['cantidad']} unidades",
                (
                    "   Precio actual: "
                    f"Bs {row['precio_actual']:.2f}"
                ),
                f"   Estado: {row['estado']}",
                f"   Evidencia: {row['evidencia']}",
            ]
        )

    return "\n".join(lines)


def format_price_changes(
    rows: tuple[dict[str, Any], ...],
) -> str:
    """Formatea solicitudes de cambio de precio pendientes."""
    if not rows:
        return (
            "No existen solicitudes de cambio de precio "
            "pendientes de aprobación."
        )

    lines = [
        (
            f"Se encontraron {len(rows)} solicitudes de cambio "
            "de precio pendientes:"
        )
    ]

    for index, row in enumerate(rows, start=1):
        lines.extend(
            [
                "",
                f"{index}. {row['producto']}",
                f"   Tienda: {row['tienda']}",
                (
                    "   Precio anterior: "
                    f"Bs {row['precio_anterior']:.2f}"
                ),
                (
                    "   Precio propuesto: "
                    f"Bs {row['precio_nuevo']:.2f}"
                ),
                (
                    "   Estado de aprobación: "
                    f"{row['estado_aprobacion']}"
                ),
                (
                    "   Solicitado por: "
                    f"{row['solicitado_por']}"
                ),
                (
                    "   Fecha de solicitud: "
                    f"{row['fecha_solicitud']}"
                ),
            ]
        )

    return "\n".join(lines)


def format_commercial_actions(
    rows: tuple[dict[str, Any], ...],
) -> str:
    """Formatea acciones comerciales pendientes."""
    if not rows:
        return (
            "No existen acciones comerciales pendientes "
            "de ejecución."
        )

    lines = [
        (
            f"Se encontraron {len(rows)} acciones comerciales "
            "pendientes:"
        )
    ]

    for index, row in enumerate(rows, start=1):
        lines.extend(
            [
                "",
                f"{index}. {row['producto']}",
                f"   Tienda: {row['tienda']}",
                f"   Tipo de acción: {row['tipo_accion']}",
                f"   Estado: {row['estado']}",
                f"   Responsable: {row['responsable']}",
                (
                    "   Fecha de registro: "
                    f"{row['fecha_registro']}"
                ),
            ]
        )

    return "\n".join(lines)


def format_business_response(result: RouteResult) -> str:
    """
    Construye la respuesta funcional usando únicamente datos
    recuperados por las herramientas Python.
    """
    if not result.successful:
        return result.message

    if (
        result.tool_name
        == LISTAR_PRODUCTOS_PROXIMOS_A_VENCER
    ):
        return format_products(result.rows)

    if (
        result.tool_name
        == LISTAR_CAMBIOS_PRECIO_PENDIENTES
    ):
        return format_price_changes(result.rows)

    if (
        result.tool_name
        == LISTAR_ACCIONES_COMERCIALES_PENDIENTES
    ):
        return format_commercial_actions(result.rows)

    return (
        "La herramienta fue ejecutada, pero no existe un "
        "formateador autorizado para presentar su resultado."
    )


def format_route_result(result: RouteResult) -> str:
    """Une la trazabilidad técnica y la respuesta funcional."""
    trace = format_trace(result)
    business_response = format_business_response(result)

    return "\n".join(
        [
            "=" * 72,
            "APP DETECCIÓN PROD - TOOL CALLING",
            "=" * 72,
            trace,
            "",
            "RESPUESTA PARA EL USUARIO",
            "-" * 72,
            business_response,
            "=" * 72,
        ]
    )
