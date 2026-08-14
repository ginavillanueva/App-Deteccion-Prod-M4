"""Servidor MCP de App Detección Prod."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .tools import (
    buscar_productos_proximos_a_vencer as local_buscar_vencimientos,
)
from .tools import (
    consultar_acciones_comerciales as local_consultar_acciones,
)
from .tools import (
    consultar_cambios_precio as local_consultar_precios,
)
from .tools import (
    consultar_detalle_producto as local_consultar_detalle,
)


mcp = FastMCP(
    "app-deteccion-prod"
)


@mcp.tool()
def buscar_productos_proximos_a_vencer(
    dias: int = 45,
    tienda: str | None = None,
) -> dict[str, Any]:
    """
    Consulta productos próximos a vencer en App Detección Prod.

    Utiliza los registros reales almacenados en SQLite y devuelve
    producto, tienda, fecha de vencimiento, días restantes, cantidad,
    precio actual, estado y evidencia.

    Args:
        dias:
            Cantidad de días hacia adelante que se deben revisar.
            El valor predeterminado es 45.

        tienda:
            Nombre opcional de una tienda o sala para limitar
            la consulta.

    Esta herramienta es únicamente de lectura.
    No modifica productos, precios ni acciones comerciales.
    """
    return local_buscar_vencimientos(
        dias=dias,
        tienda=tienda,
    )


@mcp.tool()
def consultar_detalle_producto(
    producto: str,
    tienda: str | None = None,
) -> dict[str, Any]:
    """
    Consulta el detalle registrado de un producto específico.

    Devuelve información real de App Detección Prod como tienda,
    fecha de vencimiento, días restantes, cantidad, precio actual,
    estado y evidencia.

    Args:
        producto:
            Nombre del producto que se desea consultar.

        tienda:
            Nombre opcional de la tienda o sala.

    Esta herramienta es de lectura y no modifica información.
    """
    return local_consultar_detalle(
        producto=producto,
        tienda=tienda,
    )


@mcp.tool()
def consultar_cambios_precio(
    producto: str,
    tienda: str | None = None,
) -> dict[str, Any]:
    """
    Consulta cambios de precio registrados para un producto.

    Devuelve precio anterior, precio nuevo, variación, persona que
    registró el cambio y fecha del registro.

    Args:
        producto:
            Nombre del producto cuyos cambios de precio se desean
            consultar.

        tienda:
            Nombre opcional de la tienda o sala.

    IMPORTANTE:
    Esta herramienta es únicamente informativa y de trazabilidad.
    No aprueba, rechaza ni modifica precios.
    """
    return local_consultar_precios(
        producto=producto,
        tienda=tienda,
    )


@mcp.tool()
def consultar_acciones_comerciales(
    producto: str,
    tienda: str | None = None,
    estado: str | None = None,
) -> dict[str, Any]:
    """
    Consulta acciones comerciales registradas para un producto.

    Puede devolver descuentos, bandeos, promociones, retiros u otras
    acciones almacenadas en App Detección Prod, junto con su estado,
    responsable, fecha y evidencia.

    Args:
        producto:
            Nombre del producto.

        tienda:
            Nombre opcional de la tienda o sala.

        estado:
            Estado opcional de la acción comercial, por ejemplo
            PENDIENTE o COMPLETADA.

    Esta herramienta consulta información registrada.
    No ejecuta automáticamente una acción comercial.
    """
    return local_consultar_acciones(
        producto=producto,
        tienda=tienda,
        estado=estado,
    )


def main() -> None:
    """
    Inicia el servidor MCP utilizando transporte stdio.

    El cliente MCP ejecutará este programa como proceso hijo y
    se comunicará mediante entrada y salida estándar.
    """
    mcp.run(
        transport="stdio"
    )


if __name__ == "__main__":
    main()