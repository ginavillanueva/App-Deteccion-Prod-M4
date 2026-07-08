# Workflow visual — App Detección Prod BPMN Engine

**Estado:** APROBADO / COMPLEMENTO VISUAL DE DEFENSA  
**Ubicación técnica relacionada:** `src/domain/factory.py`  
**Ubicación funcional relacionada:** `docs/FSD.md`  
**Propósito:** Mostrar de forma visual cómo fluye el workflow principal implementado en Python.

---

## 1. Vista ejecutiva del workflow principal

Este diagrama representa el flujo principal del motor BPMN aplicado a **App Detección Prod**. El proceso inicia cuando el mercaderista detecta un producto próximo a vencer y termina cuando el caso queda cerrado con trazabilidad y dashboard actualizado.

```mermaid
flowchart TD
    START((Inicio)) --> A[DetectProductCase<br/>Detectar producto próximo a vencer]
    A --> B[ValidateEvidence<br/>Validar evidencia y datos]

    B --> SPLIT{Split paralelo}
    SPLIT --> C[ClassifyRisk<br/>Clasificar riesgo de vencimiento]
    SPLIT --> D[ValidatePriceData<br/>Validar precio actual y precio propuesto]

    C --> JOIN{Join AND<br/>riesgo + precio validados}
    D --> JOIN

    JOIN --> E[DecideCommercialAction<br/>Definir acción comercial]
    E --> F[ApprovePriceChange<br/>Aprobar cambio de precio]
    F --> G[ExecuteRetailAction<br/>Ejecutar acción en tienda]
    G --> H[SupervisorReview<br/>Revisión del supervisor]
    H --> I[CloseCaseAndUpdateDashboard<br/>Cerrar caso y actualizar dashboard]
    I --> END((Fin exitoso))

    H -. evidencia incorrecta / rework .-> B
    G -. error de precio o ejecución .-> B
    H -. caso no recuperable .-> ERROR((Fin con error))

    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20;
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1;
    classDef gate fill:#fff8e1,stroke:#f9a825,stroke-width:2px,color:#5d4037;
    classDef error fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#b71c1c;

    class START,END startEnd;
    class A,B,C,D,E,F,G,H,I task;
    class SPLIT,JOIN gate;
    class ERROR error;
```

---

## 2. Lectura simple del flujo

| Paso | Tarea técnica | Explicación funcional |
|---:|---|---|
| 1 | `DetectProductCase` | El mercaderista registra producto, foto, vencimiento, precio y cantidad. |
| 2 | `ValidateEvidence` | Se valida que la evidencia sea usable y que los datos mínimos estén completos. |
| 3 | `ClassifyRisk` | El sistema clasifica el riesgo operativo/financiero del caso. |
| 4 | `ValidatePriceData` | Se valida precio actual, precio propuesto y datos económicos. |
| 5 | `DecideCommercialAction` | Ventas define descuento, bandeo, retiro, promoción o monitoreo. |
| 6 | `ApprovePriceChange` | Se aprueba humanamente cualquier cambio de precio. |
| 7 | `ExecuteRetailAction` | Se ejecuta la acción en tienda y se adjunta evidencia. |
| 8 | `SupervisorReview` | El supervisor revisa que la acción esté correctamente aplicada. |
| 9 | `CloseCaseAndUpdateDashboard` | Se cierra el caso y se actualizan métricas gerenciales. |

---

## 3. Vista de incidentes, rework y reintentos

El motor no solo avanza en línea recta. También permite volver atrás cuando falta evidencia, hay error de precio, hay mala ejecución o se supera el número máximo de reintentos.

```mermaid
flowchart TD
    A[Task in progress<br/>Tarea en ejecución] --> B{¿Resultado válido?}
    B -->|Sí| C[CompleteTask<br/>Completar tarea]
    C --> D[EvaluateNextTasks<br/>Evaluar siguientes tareas]
    D --> E[MoveForward<br/>Avanzar en el workflow]

    B -->|No| F[RegisterIncident<br/>Registrar incidente]
    F --> G{¿Tiene transición BACKWARD?}
    G -->|Sí| H[ResetTargetTask<br/>Resetear tarea objetivo]
    H --> I[RetryCounter + 1<br/>Incrementar reintento]
    I --> J{¿Superó máximo de reintentos?}
    J -->|No| K[ReturnToPreviousTask<br/>Volver para corrección]
    K --> A
    J -->|Sí| L[CloseWithError<br/>Cerrar con error]

    G -->|No| L

    classDef normal fill:#e3f2fd,stroke:#1565c0,color:#0d47a1;
    classDef decision fill:#fff8e1,stroke:#f9a825,color:#5d4037;
    classDef error fill:#ffebee,stroke:#c62828,color:#b71c1c;

    class A,C,D,E,H,I,K normal;
    class B,G,J decision;
    class F,L error;
```

---

## 4. Vista por capas del motor

Este diagrama muestra cómo se relaciona la documentación, el modelo de dominio, el runtime, la orquestación, la persistencia y las pruebas.

```mermaid
flowchart LR
    DOCS[docs/FSD.md<br/>Diseño funcional] --> FACTORY[src/domain/factory.py<br/>Workflow ejecutable]
    FACTORY --> DOMAIN[src/domain<br/>Task, Workflow, Gate, Resource, Worker]
    DOMAIN --> RUNTIME[src/runtime<br/>WorkflowInstance, TaskInstance, Trace]
    RUNTIME --> ORCH[src/orchestration<br/>Queue, Observer, Assignment]
    RUNTIME --> DB[src/persistence<br/>SQLiteRepository]
    ORCH --> TESTS[tests<br/>28 pruebas OK]
    DB --> TESTS

    classDef doc fill:#f3e5f5,stroke:#7b1fa2,color:#4a148c;
    classDef code fill:#e3f2fd,stroke:#1565c0,color:#0d47a1;
    classDef test fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20;

    class DOCS doc;
    class FACTORY,DOMAIN,RUNTIME,ORCH,DB code;
    class TESTS test;
```

---

## 5. Relación con el código

El diagrama principal se implementa en:

```text
src/domain/factory.py
```

La función responsable es:

```python
build_app_deteccion_workflow()
```

La equivalencia es:

| Diagrama | Código Python |
|---|---|
| Caja del workflow | `Task(...)` |
| Flecha de avance | `add_target(...)` |
| Retorno por error | `add_backward_transition(...)` |
| Compuerta lógica | `LogicGate(...)` |
| Recurso obligatorio | `ResourceSpec(...)` |
| Responsable | `WorkerType` |

---

## 6. Cómo explicarlo en defensa

> Este diagrama muestra el workflow principal implementado en Python. No es una imagen decorativa: cada bloque corresponde a una tarea `Task` dentro de `src/domain/factory.py`. Las flechas se implementan con transiciones del motor y los retornos por error se implementan con transiciones `BACKWARD`. La ventaja es que el flujo no queda solo documentado, sino que también es ejecutable y validado por pruebas automatizadas.

---

## 7. Comando de validación

Para demostrar que el workflow está implementado y probado:

```bash
python -m unittest discover -s tests
```

Resultado esperado:

```text
Ran 28 tests
OK
```
