"""Demostración de integración de App Detección Prod con un LLM local."""

from __future__ import annotations

from datetime import date

from src.llm.ollama_client import (
    OllamaConnectionError,
    generate_response,
)


PRODUCT_CASE = {
    "producto": "Yogur natural 1 litro",
    "tienda": "Supermercado Central - Sala 12",
    "fecha_vencimiento": "2026-08-28",
    "cantidad": 24,
    "precio_actual": 18.50,
    "accion_comercial": "Pendiente de revisión",
    "evidencia": "Fotografía del producto y fecha de vencimiento registrada",
}


def build_product_prompt(product_case: dict[str, object]) -> str:
    """Construye un prompt usando los datos de un caso de la aplicación."""
    expiration_date = date.fromisoformat(
        str(product_case["fecha_vencimiento"])
    )
    days_to_expiration = (expiration_date - date.today()).days

    return f"""
Eres un asistente de apoyo para App Detección Prod.

Analiza el siguiente producto próximo a vencer:

- Producto: {product_case["producto"]}
- Tienda: {product_case["tienda"]}
- Fecha de vencimiento: {product_case["fecha_vencimiento"]}
- Días restantes para vencer: {days_to_expiration}
- Cantidad: {product_case["cantidad"]} unidades
- Precio actual: Bs {product_case["precio_actual"]}
- Acción comercial actual: {product_case["accion_comercial"]}
- Evidencia: {product_case["evidencia"]}

Responde en español e indica:

1. Nivel de riesgo: BAJO, MEDIO o ALTO.
2. Justificación breve.
3. Acción comercial sugerida.
4. Prioridad de revisión.

La respuesta es solamente una recomendación.
No autorices descuentos ni cambies el precio automáticamente.
La decisión final debe ser realizada por una persona.
""".strip()


def main() -> None:
    """Ejecuta una llamada real al modelo local mediante Ollama."""
    prompt = build_product_prompt(PRODUCT_CASE)

    print("=" * 70)
    print("APP DETECCIÓN PROD - INVOCACIÓN DE LLM")
    print("=" * 70)
    print("\nDATO REAL ENVIADO DESDE LA APLICACIÓN:\n")
    print(prompt)
    print("\n" + "=" * 70)
    print("RESPUESTA DEL MODELO:\n")

    try:
        response = generate_response(prompt)
        print(response)
    except OllamaConnectionError as exc:
        print(f"Error de conexión: {exc}")
    except (ValueError, RuntimeError) as exc:
        print(f"Error durante la generación: {exc}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()