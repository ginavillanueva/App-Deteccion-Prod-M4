
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.domain.clasificador_vencimientos import (
    clasificar_vencimiento,
)


async def clasificar_vencimiento_endpoint(
    request: Request,
) -> JSONResponse:
    try:
        datos = await request.json()

        if not isinstance(datos, dict):
            raise ValueError("El cuerpo debe ser un objeto JSON.")

        fecha_vencimiento = datos["fecha_vencimiento"]
        fecha_consulta = datos["fecha_consulta"]

        if not isinstance(fecha_vencimiento, str) or not isinstance(fecha_consulta, str):
            raise ValueError("Las fechas deben ser cadenas de texto.")

        resultado = clasificar_vencimiento(
            fecha_vencimiento,
            fecha_consulta,
        )

        return JSONResponse(resultado, status_code=200)

    except (ValueError, KeyError, TypeError):
        return JSONResponse(
            {
                "error": "VALIDATION_ERROR",
                "detalle": "Fechas obligatorias en formato YYYY-MM-DD.",
            },
            status_code=422,
        )


ruta_vencimientos = Route(
    "/api/v1/vencimientos/clasificar",
    clasificar_vencimiento_endpoint,
    methods=["POST"],
)
