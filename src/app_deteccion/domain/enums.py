from enum import Enum


class CommercialAction(str, Enum):
    DESCUENTO = "DESCUENTO"
    BANDEO = "BANDEO"
    PROMOCION = "PROMOCION"
    RETIRO = "RETIRO"
    PENDIENTE = "PENDIENTE"


class RiskLevel(str, Enum):
    BAJO = "BAJO"
    MEDIO = "MEDIO"
    ALTO = "ALTO"


class CaseStatus(str, Enum):
    REGISTRADO = "REGISTRADO"
    VALIDADO_SUPERVISOR = "VALIDADO_SUPERVISOR"
    ESCALADO_GERENCIA = "ESCALADO_GERENCIA"
