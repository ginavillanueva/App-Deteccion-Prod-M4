# PRD — App Detección Prod Workflow Engine BPMN 2.0

**Entregable:** 1  
**Tipo:** Product Requirements Document ligero  
**Estado:** APROBADO  
**Fecha:** 2026-07-06  
**Proyecto:** App Detección Prod — Motor de Workflow tipo BPMN 2.0  
**Curso:** Fundamentos de Programación y Frameworks Modernos para IA  
**Audiencia:** Docente, equipo académico, evaluadores técnicos  
**Idioma documentación:** Español  
**Idioma del modelo de dominio:** Inglés  

---

## 1. Resumen ejecutivo

Este PRD define el producto a construir: un **motor de workflow tipo BPMN 2.0**, implementado en **Python**, aplicado al caso de negocio **App Detección Prod**.

El producto permitirá modelar, ejecutar y auditar procesos de negocio como grafos dirigidos. En este proyecto, el proceso central será la gestión de productos próximos a vencer en canal retail, desde la detección en campo hasta el cierre del caso y actualización de indicadores.

El motor no se plantea como una simple pantalla de registro, sino como una capa programática capaz de:

- definir procesos reutilizables;
- crear instancias de ejecución;
- manejar tareas humanas y automáticas;
- validar recursos obligatorios;
- asignar workers por especialidad;
- ejecutar flujos lineales, paralelos, condicionales y cíclicos;
- soportar incidentes, reset, reintentos, SLA y trazabilidad;
- comparar su diseño conceptual con motores BPMN reales como Camunda y Activiti.

---

## 2. Contexto del problema

App Detección Prod surge para resolver una brecha operativa y estratégica en empresas distribuidoras e importadoras que operan en retail. Actualmente, los productos próximos a vencer se gestionan con reportes dispersos, WhatsApp, fotos no estandarizadas, comunicación verbal o archivos sueltos.

Esto genera:

- baja trazabilidad;
- ausencia de métricas cuantificables;
- falta de visibilidad gerencial;
- demoras en decisiones comerciales;
- control débil de precios modificados;
- dificultad para medir impacto de descuentos, bandeos o retiros;
- incremento de merma;
- desconexión entre campo, supervisión, ventas y gerencia.

El motor de workflow busca convertir este proceso fragmentado en un flujo formal, auditable y programable.

---

## 3. Problema de producto

El problema no es solo registrar productos próximos a vencer. El problema principal es que el negocio no cuenta con una estructura formal que controle **cómo avanza cada caso**, quién interviene, qué evidencia se valida, qué acción comercial se decide, cuándo se modifica el precio, qué incidentes ocurren y cómo se mide el resultado.

Sin un motor de workflow:

- un caso puede quedar detenido sin responsable claro;
- la evidencia puede validarse de forma manual y tardía;
- las acciones comerciales pueden ejecutarse sin trazabilidad;
- los cambios de precio pueden no quedar auditados;
- la gerencia puede recibir información tardía o incompleta;
- no existe una traza completa del recorrido del caso.

---

## 4. Objetivo del producto

Diseñar e implementar un motor de workflow tipo BPMN 2.0 que permita orquestar el ciclo de vida de casos de productos próximos a vencer en App Detección Prod, garantizando trazabilidad, control operativo, reglas de avance, asignación de responsables, manejo de incidentes y evidencia técnica ejecutable.

---

## 5. Objetivos específicos

1. Representar procesos de negocio como grafos dirigidos compuestos por tareas y transiciones.
2. Separar la definición del proceso (`Workflow`, `Task`) de su ejecución (`WorkflowInstance`, `TaskInstance`).
3. Ejecutar flujos lineales, paralelos, condicionales, convergentes y cíclicos.
4. Usar `LogicGate` como compuerta embebida en la tarea destino.
5. Gestionar recursos de entrada y salida, incluyendo evidencia, precio, cantidad, acción comercial y observaciones.
6. Asignar tareas a workers según especialidad y disponibilidad.
7. Orquestar tareas listas mediante una cola y patrón Observer.
8. Persistir definiciones, instancias, tareas, recursos, workers, incidentes y trazas.
9. Registrar incidentes con glosa obligatoria, reset configurable y reintentos.
10. Soportar SLA/timeout, multi-asignación y ejecución concurrente.
11. Proveer pruebas automatizadas de los escenarios obligatorios.
12. Documentar trazabilidad entre PRD, FSD, código, pruebas, prompts y decisiones de implementación.

---

## 6. Usuarios y roles

### 6.1 Roles de negocio

| Rol de negocio | Necesidad principal | Traducción al motor |
|---|---|---|
| Mercaderista | Registrar producto, evidencia, cantidad y precio en campo | `WorkerType.FIELD_MERCHANDISER` |
| Supervisor | Validar evidencia, priorizar casos, controlar SLA, revisar cierre | `WorkerType.SUPERVISOR` / `Role.ADMIN` parcial |
| Vendedor | Definir o ejecutar acción comercial | `WorkerType.SALES_REP` |
| Gerencia Comercial | Consultar KPIs, impacto financiero y trazabilidad | `Role.ADMIN` / visualización ejecutiva |
| Sistema/IA mock | Clasificar riesgo, validar reglas, simular REST/Lambda | `TaskType.SERVICE` / `TaskType.DECISION` |

### 6.2 Roles técnicos del motor

| Rol técnico | Descripción |
|---|---|
| `WORKER` | Ejecuta tareas asignadas según especialidad. |
| `ADMIN` | Puede reasignar, suspender, cancelar, revisar errores y consultar trazabilidad completa. |
| `ORCHESTRATOR` | Componente del sistema que observa la cola y asigna tareas. |
| `MOCK_SERVICE` | Simula integraciones REST/Lambda o clasificación automática. |

---

## 7. Alcance funcional del MVP

### 7.1 Incluido en el MVP

El MVP deberá incluir:

1. **Definición de workflows**
   - Crear `Workflow` con `Task`, `Transition`, `LogicGate`, `ResourceSpec` y `WorkerType`.
   - Definir tarea inicial única y una o más tareas finales.

2. **Instanciación**
   - Crear `WorkflowInstance` a partir de una definición.
   - Crear `TaskInstance` por cada `Task`.

3. **Ejecución**
   - Encolar tareas listas.
   - Asignar workers.
   - Iniciar y completar tareas.
   - Navegar a tareas destino.
   - Evaluar compuertas.

4. **Compuertas**
   - `AND`
   - `OR`
   - `XOR`
   - `COMPLEX`
   - `SCRIPT`
   - `REST` mock
   - `LAMBDA` mock

5. **Recursos**
   - Registrar recursos obligatorios y opcionales.
   - Propagar recursos entre tareas cuando exista match.
   - Bloquear finalización si falta un recurso obligatorio.

6. **Workers**
   - Registrar workers por especialidad.
   - Asignar por skill-based + least-loaded.
   - Respetar capacidad concurrente.

7. **Incidentes y rework**
   - Levantar incidente con motivo obligatorio.
   - Retornar por transición `BACKWARD`.
   - Resetear tareas aguas abajo o específicas.
   - Controlar reintentos por transición.

8. **SLA**
   - Definir `maxTimeToAssign`.
   - Definir `maxTimeToComplete`.
   - Marcar `TIMED_OUT` si se incumple el plazo.

9. **Concurrencia**
   - Ejecutar tareas paralelas mediante interfaz `Executor` y `Future`.
   - Cancelar futuros en reset por incidente.

10. **Trazabilidad**
    - Registrar `TraceEntry`.
    - Registrar incidentes.
    - Reconstruir camino completo, incluso con ciclos.

11. **Persistencia**
    - Usar SQLite para persistencia liviana y demostrable.
    - Justificar la elección en FSD.

12. **Pruebas**
    - Cubrir todos los escenarios obligatorios.

---

## 8. Fuera de alcance del MVP

Quedan fuera del MVP:

- Interfaz web completa tipo Camunda Cockpit.
- Motor BPMN 2.0 100% compatible con XML BPMN.
- Editor visual de diagramas.
- Autenticación empresarial real.
- Integración real con AWS Lambda.
- Integración real con sistemas ERP/POS.
- Modelo avanzado de DMN.
- Compensación transaccional completa.
- Multi-instance BPMN avanzado.
- Subprocesos y call activities.

Estos puntos podrán quedar como extensiones sugeridas en FSD o roadmap.

---

## 9. Workflow de referencia aplicado a App Detección Prod

### 9.1 Proceso principal

```text
DetectProductCase
→ ValidateEvidence
→ ClassifyRisk
→ DecideCommercialAction
→ ApprovePriceChange
→ ExecuteRetailAction
→ SupervisorReview
→ CloseCaseAndUpdateDashboard
```

### 9.2 Descripción de tareas

| Task | Tipo | Worker requerido | Recursos principales |
|---|---|---|---|
| `DetectProductCase` | HUMAN / START | FIELD_MERCHANDISER | product_id, store_id, expiration_date, current_price, quantity, photo |
| `ValidateEvidence` | HUMAN | SUPERVISOR | photo, expiration_date, quantity |
| `ValidatePriceData` | HUMAN/SERVICE | SUPERVISOR | current_price, proposed_price |
| `ClassifyRisk` | SERVICE/DECISION | MOCK_SERVICE | expiration_date, quantity, financial_value |
| `DecideCommercialAction` | HUMAN | SALES_REP / SUPERVISOR | risk_level, action_type |
| `ApprovePriceChange` | HUMAN | SUPERVISOR / ADMIN | current_price, proposed_price, approval_reason |
| `ExecuteRetailAction` | HUMAN | FIELD_MERCHANDISER / SALES_REP | action_type, evidence_after |
| `SupervisorReview` | HUMAN | SUPERVISOR | evidence_after, price_applied, action_status |
| `CloseCaseAndUpdateDashboard` | SERVICE / END | SYSTEM | final_status, trace, KPIs |

---

## 10. Escenarios obligatorios que debe soportar

| Escenario | Requisito funcional | Ejemplo en App Detección Prod |
|---|---|---|
| Lineal | Ejecutar A → B → C → D | Detección → validación → clasificación → decisión |
| Paralelo | Ejecutar B y C en paralelo | Validar evidencia y validar precio simultáneamente |
| Join AND | Iniciar tarea solo si todas las previas completaron | Decidir acción solo si riesgo y precio fueron validados |
| Join OR | Iniciar tarea si al menos una previa completó | Avanzar por evidencia válida o validación manual |
| Join complejo | Evaluar expresión/regla | Si riesgo alto y valor financiero alto, exigir aprobación |
| Ciclo/rework | Retornar a una tarea previa | Supervisor devuelve caso por evidencia incorrecta |
| Múltiples finales | Terminar por distintos estados | Cerrado exitoso, rechazado, vencido, error |
| Incidente con reset | Registrar incidente y resetear tareas | Precio aplicado no coincide con precio aprobado |
| Reintentos con error | Terminar en `ERROR` al superar intentos | Evidencia falla más de 3 veces |
| SLA/timeout | Marcar vencimiento de plazo | Producto crítico no atendido en 24h |
| Multi-asignación | Requerir varios workers | Supervisor + vendedor validan acción |
| Concurrencia | Ejecutar varias tareas/casos en paralelo | Múltiples productos en distintas tiendas |

---

## 11. Reglas de negocio principales

### RN-01 — Evidencia obligatoria

Una tarea de detección no puede completarse sin evidencia mínima:

- foto;
- fecha de vencimiento;
- cantidad;
- tienda;
- precio actual;
- identificador de producto.

### RN-02 — Precio trazable

Todo cambio de precio debe registrar:

- precio anterior;
- precio propuesto;
- responsable;
- motivo;
- aprobación;
- timestamp;
- evidencia.

### RN-03 — Acción comercial explícita

Todo caso debe tener una acción comercial antes del cierre:

- descuento;
- bandeo;
- promoción;
- retiro;
- seguimiento sin acción;
- rechazo justificado.

### RN-04 — Riesgo alto exige priorización

Si el caso tiene vencimiento cercano, cantidad alta o valor financiero relevante, el motor debe priorizarlo mediante clasificación de riesgo.

### RN-05 — Incidente con glosa obligatoria

No se puede devolver un caso hacia atrás sin registrar motivo claro del incidente.

### RN-06 — Reintentos máximos

Cada transición `BACKWARD` debe tener un número máximo de reintentos. Al superarlo, el workflow termina en estado `ERROR`.

### RN-07 — Trazabilidad no editable

La traza de ejecución debe ser append-only. No se elimina ni modifica el historial previo.

### RN-08 — Gerencia consume información consolidada

Gerencia no registra casos diarios; consume KPIs, estados, impactos y alertas consolidadas.

---

## 12. Requisitos no funcionales

| ID | Requisito | Criterio |
|---|---|---|
| NFR-01 | Trazabilidad | Toda transición relevante debe generar `TraceEntry`. |
| NFR-02 | Mantenibilidad | Modelo separado en `domain`, `runtime`, `orchestration`, `persistence`. |
| NFR-03 | Claridad académica | Documentación en español y modelo de objetos en inglés. |
| NFR-04 | Testabilidad | Cada escenario obligatorio debe tener prueba. |
| NFR-05 | Extensibilidad | Nuevos `GateType` no deben romper el motor. |
| NFR-06 | Concurrencia controlada | Estructuras compartidas deben protegerse con locks o estrategia documentada. |
| NFR-07 | Persistencia liviana | SQLite debe permitir reproducibilidad sin servidor externo. |
| NFR-08 | Auditabilidad | Incidentes, reintentos, workers y recursos deben quedar registrados. |

---

## 13. Criterios de éxito

El entregable será exitoso si:

1. El repositorio contiene PRD y FSD claros.
2. El modelo de dominio usa `dataclasses`, `Enum` y type hints.
3. La ejecución separa definición e instancia.
4. El workflow aplicado a App Detección Prod se puede correr mediante demo o tests.
5. Se demuestran los escenarios obligatorios.
6. Existe trazabilidad mediante `executionPath`.
7. Los incidentes y resets quedan registrados.
8. Los reintentos pueden terminar en `ERROR`.
9. La persistencia está justificada.
10. `prompt_mappings.md` registra el uso de IA.
11. `PR_implementation/` explica cada feature.
12. El docente puede entender cómo el motor se relaciona con Camunda y Activiti.

---

## 14. Métricas de producto

| Métrica | Definición | Uso |
|---|---|---|
| Tiempo de ciclo del caso | Tiempo desde detección hasta cierre | Medir eficiencia operativa |
| Casos con SLA vencido | Casos `TIMED_OUT` | Detectar cuellos de botella |
| Incidentes por tipo | QUALITY, VALIDATION, MISSING_RESOURCE, BUSINESS_RULE | Mejorar proceso |
| Reintentos promedio | Reintentos por caso | Medir calidad de datos |
| Casos por estado final | COMPLETED, CANCELLED, ERROR | Control ejecutivo |
| Valor financiero intervenido | Cantidad × diferencia de precio o valor de producto | Medir impacto |
| Casos con precio modificado | Casos con `PriceChange` | Control comercial |
| Acciones comerciales aplicadas | Descuento, bandeo, retiro, promoción | Medir estrategia |

---

## 15. Riesgos principales

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Scope demasiado grande | Alto | Mantener MVP académico y dejar extensiones en roadmap |
| Confundir BPMN estándar con simplificación del curso | Medio | Documentar que compuertas están embebidas en `Task` |
| Falta de trazabilidad | Alto | Diseñar `TraceEntry` desde el inicio |
| Persistencia excesivamente compleja | Medio | Usar SQLite |
| Concurrencia difícil de depurar | Medio | Empezar con interfaz `Executor`, luego `ThreadPoolExecutor` |
| Documentos no conectados al código | Alto | Usar `PR_implementation` y matriz de trazabilidad |
| Demo sin escenarios obligatorios | Alto | Priorizar tests de cada escenario |

---

## 16. Dependencias

- Python 3.11+ recomendado.
- Librerías estándar:
  - `dataclasses`
  - `enum`
  - `typing`
  - `uuid`
  - `datetime`
  - `sqlite3`
  - `collections.deque`
  - `concurrent.futures`
  - `unittest` o `pytest`
- No se requiere servicio externo real.
- REST/Lambda se simulan con mocks.

---

## 17. Trazabilidad PRD hacia entregables

| Requisito PRD | Entregable donde se implementa/documenta |
|---|---|
| Motor como grafo | `docs/FSD.md`, `src/domain/` |
| Definición vs instancia | `src/domain/`, `src/runtime/` |
| Compuertas | `src/domain/gates.py`, `tests/test_required_scenarios.py` |
| Recursos | `src/domain/resources.py`, `src/runtime/instances.py` |
| Workers | `src/domain/workers.py`, `src/orchestration/` |
| Cola/Observer | `src/orchestration/orchestrator.py` |
| Persistencia SQLite | `src/persistence/sqlite_repository.py` |
| Incidentes/reset | `src/domain/incidents.py`, `src/runtime/instances.py`, `tests/test_required_scenarios.py` |
| SLA/timeout | `src/runtime/instances.py`, `tests/test_required_scenarios.py` |
| Concurrencia | `src/orchestration/executor.py`, tests |
| Prompt mappings | `docs/prompt_mappings.md` |
| PR implementation | `PR_implementation/*.md` |
| Aportes | `docs/APORTES.md` |

---

## 18. Estado final del PRD

Este PRD se encuentra **APROBADO** y actúa como baseline de producto para el FSD, la implementación, las pruebas y la trazabilidad final.


---

## Registro de aprobación

**Estado final:** APROBADO  
**Evidencia:** el usuario indicó explícitamente “aprobado PRD”.  
**Uso en la siguiente entrega:** este PRD queda congelado como baseline funcional para construir el FSD, el código, las pruebas y la trazabilidad posterior.
