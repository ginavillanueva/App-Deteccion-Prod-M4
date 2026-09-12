# Auditoría E2E — App Detección Prod

## Criterio de auditoría

Cada test generado se revisa con las cinco preguntas exigidas:

1. ¿Usa localizadores de persona o un data-testid estable?
2. ¿Evita esperas fijas?
3. ¿Verifica lo que promete la interfaz y no la redacción de un modelo?
4. ¿Es pequeño e independiente y comienza con page.goto('/')?
5. ¿Usa datos propios del test y evita depender de otro test?

---

## Bloque 1 — Navegación y sesión

| Flujo | Caso Planner | Archivo | Veredicto | Pregunta que falló | Corrección / evidencia |
|---|---|---|---|---|---|
| NAV-01 | NAV-01 | tests/e2e/nav-01.spec.ts | ACEPTADO | Ninguna | Usa getByRole, page.goto('/'), sin esperas fijas y verifica encabezado + Salud del sistema |
| THR-01 | THR-01 | tests/e2e/thr-01.spec.ts | CORREGIDO → ACEPTADO | P1: localizador inicial del Thread ID potencialmente frágil | Se agregó data-testid="thread-id"; validación real confirmó cambio de ID y test en verde |

### Resultado ejecutado

- Tests generados en este bloque: 2
- Tests aceptados: 2
- Tests corregidos: 1
- Tests descartados: 0
- Resultado: 2 passed
- Esperas fijas: ninguna
- Thread ID hardcodeado: ninguno
- Tokens Planner: tokens no expuestos por la interfaz
- Tokens Generator: tokens no expuestos por la interfaz

## Anclas agregadas al producto

| Ancla | Pantalla | Motivo |
|---|---|---|
| data-testid="thread-id" | Barra lateral / Control | Permite localizar de forma estable el Thread ID antes y después de Nuevo thread |


---

## Bloque 2 — Contexto empresarial y producto

| Flujo | Caso Planner | Archivo | Veredicto | Pregunta que falló | Corrección / evidencia |
|---|---|---|---|---|---|
| CTX-01 | CTX-01 | tests/e2e/ctx-01.spec.ts | CORREGIDO → ACEPTADO | P1: interacción/localización estable en combobox Streamlit | Se ajustó la verificación al estado accesible real del combobox. Selección Departamento/Cadena/Sala validada y resultado Sala empresarial observable. Test en verde. |
| PRD-01 | PRD-01 | tests/e2e/prd-01.spec.ts | CORREGIDO → ACEPTADO | P1: estado observable del combobox Streamlit | Se ajustó la assertion para comprobar selección real y clasificación visible sin depender de value interno. Test en verde. |
| SRC-01 | SRC-01 | tests/e2e/src-01.spec.ts | CORREGIDO → ACEPTADO | P1: radio nativo oculto por Streamlit | Se ajustó la interacción/assertion del radio accesible para verificar CONTEXTO EMPRESARIAL seleccionado. No ejecuta workflow. Test en verde. |
| NOTE-01 | NOTE-01 | tests/e2e/note-01.spec.ts | ACEPTADO | Ninguna | Usa labels visibles, nota propia del test y comprueba que la pregunta principal conserva su valor. Test en verde. |

### Resultado ejecutado

- Casos del Planner: 4
- Tests del Generator: 4
- Tests aceptados: 4
- Tests corregidos: 3
- Tests descartados: 0
- Resultado final del bloque: 4 passed
- Tiempo de corrida de auditoría: 10.5 s
- Playwright exit code: 0
- Esperas fijas: ninguna
- Workflow ejecutado durante este bloque: no
- Tests dependientes entre sí: no
- data-testid nuevos agregados en este bloque: ninguno
- Tokens Planner: tokens no expuestos por la interfaz
- Tokens Generator: tokens no expuestos por la interfaz

### Localizadores utilizados

- CTX-01: getByLabel / roles accesibles de combobox / getByText
- PRD-01: getByLabel / getByRole('option') / getByText
- SRC-01: getByRole('radio')
- NOTE-01: getByLabel

### Observación técnica

Streamlit puede representar el estado seleccionado de ciertos combobox mediante atributos accesibles en lugar del atributo HTML value. Asimismo, algunos inputs nativos de radio permanecen ocultos y requieren interactuar con su representación accesible. Las correcciones se limitaron a los tests y no modificaron reglas de negocio ni el workflow.

