"""Demostración integral de Tool Calling para App Detección Prod."""

from __future__ import annotations

import argparse
import os
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from src.tool_calling.config import get_settings
from src.tool_calling.formatter import format_route_result
from src.tool_calling.router import route_question


@dataclass(frozen=True)
class DemoScenario:
    """Información de un escenario incluido en la demostración."""

    number: int
    title: str
    objective: str
    question: str
    expected_path: str
    ai_override: bool | None = None


SCENARIOS: tuple[DemoScenario, ...] = (
    DemoScenario(
        number=1,
        title="Pregunta controlada por catálogo",
        objective=(
            "Demostrar que una frase conocida selecciona la herramienta "
            "sin invocar al modelo."
        ),
        question="¿Qué productos están próximos a vencer?",
        expected_path="KEYWORD",
    ),
    DemoScenario(
        number=2,
        title="Paráfrasis interpretada mediante LLM",
        objective=(
            "Demostrar que el modelo comprende una redacción diferente "
            "y únicamente selecciona la herramienta."
        ),
        question="¿Qué mercadería caduca pronto?",
        expected_path="LLM",
    ),
    DemoScenario(
        number=3,
        title="Pregunta fuera del alcance",
        objective=(
            "Demostrar que el sistema rechaza una consulta para la cual "
            "no existe información ni herramienta autorizada."
        ),
        question=(
            "¿Cuál será el presupuesto de marketing "
            "de la empresa para 2027?"
        ),
        expected_path="LLM",
    ),
    DemoScenario(
        number=4,
        title="Paráfrasis con la IA deshabilitada",
        objective=(
            "Demostrar el comportamiento controlado cuando no existe "
            "coincidencia en el catálogo y el feature flag está apagado."
        ),
        question="¿Qué mercadería caduca pronto?",
        expected_path="FALLBACK",
        ai_override=False,
    ),
)


@contextmanager
def temporary_ai_flag(
    enabled: bool | None,
) -> Iterator[None]:
    """
    Aplica temporalmente un valor al feature flag.

    Se utiliza únicamente para demostrar el escenario con IA apagada.
    Al terminar, se restaura la configuración anterior.
    """
    if enabled is None:
        yield
        return

    previous_value = os.environ.get("IA_HABILITADA")
    os.environ["IA_HABILITADA"] = (
        "true" if enabled else "false"
    )

    try:
        yield

    finally:
        if previous_value is None:
            os.environ.pop("IA_HABILITADA", None)
        else:
            os.environ["IA_HABILITADA"] = previous_value


def print_demo_header() -> None:
    """Muestra la introducción general de la demostración."""
    settings = get_settings()

    print("=" * 78)
    print("APP DETECCIÓN PROD")
    print("DEMOSTRACIÓN INTEGRAL DE TOOL CALLING")
    print("=" * 78)
    print(f"Modelo configurado: {settings.ollama_model}")
    print(f"API local: {settings.ollama_api_url}")
    print(
        "IA habilitada desde configuración: "
        f"{'SI' if settings.ia_habilitada else 'NO'}"
    )
    print()
    print("Responsabilidades del proceso:")
    print("- El catálogo resuelve preguntas controladas.")
    print("- El LLM solamente selecciona una herramienta.")
    print("- Python ejecuta la herramienta autorizada.")
    print("- SQLite proporciona los datos.")
    print("- Python genera la respuesta final.")
    print("=" * 78)


def print_scenario_header(
    scenario: DemoScenario,
) -> None:
    """Muestra el título y objetivo de un escenario."""
    print()
    print("#" * 78)
    print(
        f"ESCENARIO {scenario.number}: "
        f"{scenario.title.upper()}"
    )
    print("#" * 78)
    print(f"OBJETIVO: {scenario.objective}")
    print(f"PREGUNTA: {scenario.question}")
    print(f"CAMINO ESPERADO: {scenario.expected_path}")

    if scenario.ai_override is False:
        print(
            "CONFIGURACIÓN ESPECIAL: "
            "IA_HABILITADA=false durante este escenario"
        )

    print("#" * 78)
    print()


def run_scenario(
    scenario: DemoScenario,
) -> None:
    """Ejecuta y presenta un escenario completo."""
    print_scenario_header(scenario)

    with temporary_ai_flag(scenario.ai_override):
        result = route_question(scenario.question)

    print(format_route_result(result))

    verification = (
        "APROBADO"
        if result.path == scenario.expected_path
        else "REVISAR"
    )

    print()
    print("VERIFICACIÓN AUTOMÁTICA")
    print("-" * 78)
    print(f"CAMINO ESPERADO: {scenario.expected_path}")
    print(f"CAMINO OBTENIDO: {result.path}")
    print(f"RESULTADO: {verification}")
    print("-" * 78)


def wait_before_next(
    current_index: int,
    total: int,
    no_pause: bool,
) -> None:
    """Espera confirmación antes de mostrar el siguiente escenario."""
    if no_pause or current_index >= total:
        return

    print()
    input(
        "Presiona Enter para continuar con el siguiente escenario..."
    )


def parse_arguments() -> argparse.Namespace:
    """Lee las opciones de ejecución del programa."""
    parser = argparse.ArgumentParser(
        description=(
            "Ejecuta los cuatro escenarios de Tool Calling "
            "de App Detección Prod."
        )
    )

    parser.add_argument(
        "--no-pause",
        action="store_true",
        help=(
            "Ejecuta todos los escenarios sin esperar Enter "
            "entre cada uno."
        ),
    )

    return parser.parse_args()


def main() -> int:
    """Ejecuta la demostración integral."""
    arguments = parse_arguments()
    settings = get_settings()

    if not settings.ia_habilitada:
        print(
            "No es posible iniciar la demostración completa porque "
            "IA_HABILITADA=false en el archivo .env."
        )
        print(
            "Cambia el valor a IA_HABILITADA=true y vuelve "
            "a ejecutar el programa."
        )
        return 1

    print_demo_header()

    total_scenarios = len(SCENARIOS)

    for index, scenario in enumerate(
        SCENARIOS,
        start=1,
    ):
        run_scenario(scenario)

        wait_before_next(
            current_index=index,
            total=total_scenarios,
            no_pause=arguments.no_pause,
        )

    print()
    print("=" * 78)
    print("DEMOSTRACIÓN FINALIZADA")
    print("=" * 78)
    print(f"Escenarios ejecutados: {total_scenarios}")
    print("El feature flag original fue restaurado.")
    print("No se modificó ningún dato mediante el LLM.")
    print("=" * 78)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())