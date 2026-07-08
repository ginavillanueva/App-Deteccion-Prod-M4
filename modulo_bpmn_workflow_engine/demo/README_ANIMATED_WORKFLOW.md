# Demo animada del workflow BPMN — App Detección Prod

Este directorio contiene una demo visual y local del flujo principal del motor BPMN aplicado a App Detección Prod.

## Archivo principal

```text
animated_workflow.html
```

## Cómo abrirlo

1. Descargar o clonar el repositorio.
2. Entrar a la carpeta:

```text
modulo_bpmn_workflow_engine/demo/
```

3. Hacer doble clic en:

```text
animated_workflow.html
```

No requiere instalación, servidor, internet ni librerías externas.

## Qué muestra

- Flujo normal del caso.
- Ejecución paso a paso.
- Split paralelo entre clasificación de riesgo y validación de precio.
- Join AND antes de decidir acción comercial.
- Aprobación humana de cambio de precio.
- Ejecución en sala.
- Revisión de supervisor.
- Cierre y actualización de dashboard.
- Simulación de incidente con retorno a validación.
- Bitácora visual de ejecución.

## Relación con el código

La demo visual representa el mismo flujo implementado en:

```text
src/domain/factory.py
```

La ejecución real del motor se encuentra en:

```text
src/runtime/instances.py
src/orchestration/orchestrator.py
```

La validación está cubierta por:

```text
tests/test_required_scenarios.py
```

## Uso en defensa

Abrir este HTML al inicio de la defensa para explicar el proceso de forma visual. Luego mostrar `factory.py` para demostrar que el flujo está implementado como código ejecutable.
