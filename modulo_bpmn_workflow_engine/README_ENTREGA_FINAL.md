# Entrega final aprobada — App Detección Prod BPMN Workflow Engine

Este paquete corresponde a la entrega final aprobada del proyecto **App Detección Prod BPMN Workflow Engine** para el curso **Fundamentos de Programación y Frameworks Modernos para IA**.

## Contenido principal

- `README.md`: documento principal para el docente.
- `00_PLAN_EJECUCION_APROBADO.md`: plan maestro aprobado.
- `00_CONTROL_APROBACIONES.md`: historial y estado final de aprobaciones.
- `docs/PRD.md`: Product Requirements Document aprobado.
- `docs/FSD.md`: Functional Specification Document aprobado.
- `docs/prompt_mappings.md`: trazabilidad de prompts usados con IA.
- `docs/APORTES.md`: contribución individual.
- `PR_implementation/`: documentación por feature/PR.
- `src/`: implementación Python del motor workflow.
- `tests/`: pruebas obligatorias del motor BPMN aplicado a App Detección Prod.

## Validación final

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado verificado:

```text
Ran 28 tests
OK
```

## Uso recomendado

Este paquete contiene únicamente los artefactos del proyecto final aprobado: documentación, código, pruebas, trazabilidad, prompt mappings y evidencias de aprobación.

La publicación en el repositorio se realiza fuera del paquete entregable, para que los archivos evaluados se concentren en el producto académico y técnico.
