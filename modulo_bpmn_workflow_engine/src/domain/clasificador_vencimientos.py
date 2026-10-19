
from datetime import date


def clasificar_vencimiento(
    fecha_vencimiento: str,
    fecha_consulta: str,
) -> dict:
    """Clasifica un producto según los días restantes para vencer."""

    vencimiento = date.fromisoformat(fecha_vencimiento)
    consulta = date.fromisoformat(fecha_consulta)

    dias_restantes = (vencimiento - consulta).days

    if dias_restantes < 0:
        estado = "VENCIDO"
    elif dias_restantes <= 30:
        estado = "PROXIMO_A_VENCER"
    else:
        estado = "VIGENTE"

    return {
        "dias_restantes": dias_restantes,
        "estado": estado,
    }
  