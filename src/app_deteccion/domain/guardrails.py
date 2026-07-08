from app_deteccion.domain.exceptions import DomainValidationError

FORBIDDEN_INSTRUCTIONS = (
    "ignora reglas",
    "ignora las reglas",
    "olvida las reglas",
    "cambia el precio",
    "cambiar precio",
    "aprueba descuento",
    "aprobar descuento",
    "aprueba el descuento",
    "cierra el caso",
    "cerrar caso",
    "actua como gerente",
    "hazlo automaticamente",
)


def validate_human_note_is_safe(note: str | None) -> None:
    """Blocks prompt-injection-like instructions inside operational notes."""
    normalized = (note or "").lower()
    if any(pattern in normalized for pattern in FORBIDDEN_INSTRUCTIONS):
        raise DomainValidationError("La evidencia contiene una instrucción prohibida para IA/agentes")
