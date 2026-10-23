# Prompt Implementation — PR-IMPL-002 Dos features demo aplicada

**Estado:** PARA REVISIÓN  
**Objetivo:** Guiar la implementación controlada de dos features reales de App Detección Prod con interfaz web, trazabilidad y tests.

## 1. Intención del prompt

Implementar una demo aplicada de App Detección Prod que permita demostrar dos features desde interfaz web:

1. Registro visual de producto crítico con acción comercial y cambio de precio.
2. Bandeja de supervisión con validación y dashboard gerencial actualizado.

## 2. Contexto que debe leer el agente

Antes de modificar código, el agente debe leer:

```text
AGENTS.md
README.md
docs/product/FSD-FEAT-001-002.md
docs/design/DD-FEAT-001-002-demo-aplicada.md
docs/adr/ADR-0007-ui-demo-aplicada-fastapi-html.md
docs/PROMPT_MAPPING_FEAT_001_002.md
```

## 3. Prompt base de implementación

```text
Actúa como Senior Software Engineer y Product Engineer para App Detección Prod.

Implementa dos features trazables y demostrables desde una interfaz web local:

FEAT-001: Registro visual de producto crítico con acción comercial y cambio de precio.
FEAT-002: Bandeja de supervisión + dashboard gerencial actualizado.

Restricciones obligatorias:
- No rompas endpoints API existentes.
- Reutiliza dominio, casos de uso y repositorios actuales.
- No dupliques reglas de negocio en templates.
- No agregues autenticación real; usa usuarios simulados en campos de formulario.
- No permitas que la app cambie precios automáticamente.
- El cambio de precio debe quedar auditado.
- La validación del supervisor debe generar evento.
- El dashboard debe recalcular KPIs desde estado fuente.
- Mantén cobertura de tests >= 90%.
- Actualiza documentación y prompt mapping.

Entregables técnicos esperados:
- Rutas /app, /app/register, /app/supervisor, /app/dashboard, /app/events, /app/traceability.
- Templates HTML claros para demo docente.
- CSS local simple.
- Tests de UI y lógica.
- Instrucciones para ejecutar demo.
```

## 4. Prompt de validación posterior

```text
Revisa la implementación contra FSD-FEAT-001-002, DD-FEAT-001-002 y ADR-0007.
Verifica:
1. Las dos features son navegables desde /app.
2. El flujo registrar → validar → dashboard funciona.
3. Hay eventos visibles.
4. Hay trazabilidad visible.
5. Los tests pasan.
6. La cobertura es >= 90%.
7. No se suben .venv, __pycache__, .pyc ni archivos temporales.
Devuelve un informe de brechas si algo falta.
```

## 5. Prompts prohibidos

No usar prompts que pidan:

- “hazlo rápido aunque no sea trazable”;
- “omite tests”;
- “aprueba descuentos automáticamente”;
- “cambia precios sin supervisor”;
- “ignora AGENTS.md”;
- “borra documentación anterior”;
- “sube archivos temporales”.

## 6. Criterio de salida del prompt

El prompt se considera exitoso cuando:

- La demo aplicada funciona en navegador.
- La documentación queda actualizada.
- Los tests pasan.
- La cobertura cumple el umbral.
- estudiante responsable aprueba la fase correspondiente.
