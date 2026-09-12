# Inventario de flujos E2E — App Detección Prod

## Alcance

Este archivo define el alcance de la suite E2E.
Cada flujo representa una acción observable realizada por una persona en la aplicación web.

Regla de auditoría:
- se verifica estado, fuente, checkpoint, herramienta o resultado visible;
- no se verifica la redacción libre de un modelo;
- cada caso aceptado deberá quedar cubierto por un test E2E independiente.

---

## 1. Navegación y sesión

| ID | Qué hace la persona | Qué debe ver al final | Test E2E |
|---|---|---|---|
| NAV-01 | Abre App Detección Prod | Título de la aplicación y salud del sistema visible | Pendiente |
| THR-01 | Pulsa Nuevo thread | Un nuevo Thread ID activo | Pendiente |

## 2. Contexto empresarial y producto

| ID | Qué hace la persona | Qué debe ver al final | Test E2E |
|---|---|---|---|
| CTX-01 | Selecciona Departamento, Cadena y Sala | Sala empresarial correspondiente reflejada en pantalla | Pendiente |
| PRD-01 | Selecciona un producto | Producto seleccionado y clasificación asociada | Pendiente |
| SRC-01 | Cambia DEMO VALIDADO / CONTEXTO EMPRESARIAL | Fuente elegida visible antes de ejecutar | Pendiente |
| NOTE-01 | Escribe una nota operativa | Nota conservada y pregunta principal sin ser reemplazada | Pendiente |

## 3. Operación y workflow

| ID | Qué hace la persona | Qué debe ver al final | Test E2E |
|---|---|---|---|
| OPE-01 | Abre un thread nuevo sin ejecutar | Estado NO_EXISTE | Pendiente |
| OPE-02 | Ejecuta VENCIMIENTO | Workflow finalizado con consulta de detalle/vencimiento registrada | Pendiente |
| OPE-03 | Ejecuta CAMBIO_PRECIO | Consulta informativa trazable, sin flujo de aprobación de precio | Pendiente |
| OPE-04 | Ejecuta ACCION_COMERCIAL | Consulta de registros comerciales sin ejecución autónoma | Pendiente |
| OPE-05 | Ejecuta AUDITORIA_COMPLETA mediante PAUSAR | Estado PAUSADO y nodo NEXT pendiente | Pendiente |
| OPE-06 | Pulsa REANUDAR sobre AUDITORIA_COMPLETA pausada | Mismo thread continúa y llega al estado esperado/final | Pendiente |
| OPE-07 | Pulsa RECUPERAR sobre un thread persistido | Estado/checkpoint del thread recuperado | Pendiente |
| OPE-08 | Ejecuta SEGURIDAD con entrada de prompt injection | PROMPT_INJECTION, TOOLS=[] y solo validación de entrada recorrida | Pendiente |

## 4. Evidencia multimodal

| ID | Qué hace la persona | Qué debe ver al final | Test E2E |
|---|---|---|---|
| EVI-01 | Sube un audio y confirma transcripción | Evidencia de audio asociada al mismo thread | Pendiente |
| EVI-02 | Sube una imagen y confirma descripción | Evidencia visual asociada al mismo thread | Pendiente |
| EVI-03 | Activa la cámara | Control de captura de foto disponible | Pendiente |

## 5. Trazabilidad

| ID | Qué hace la persona | Qué debe ver al final | Test E2E |
|---|---|---|---|
| TRZ-01 | Abre Trazabilidad en un thread nuevo | Mismo Thread ID, NO_EXISTE, checkpoint/estado vacíos y sin historial | Pendiente |
| TRZ-02 | Abre Trazabilidad después de ejecutar | Checkpoint, estado, historial y metadata del mismo thread | Pendiente |

## 6. Grafo / arquitectura

| ID | Qué hace la persona | Qué debe ver al final | Test E2E |
|---|---|---|---|
| GRA-01 | Abre Grafo / arquitectura | Grafo generado desde el código real y sección de nodos recorridos | Pendiente |
| GRA-02 | Pulsa Ejecutar flujo en BPMN animado | Avance visual y cambio del estado de la simulación | Pendiente |
| GRA-03 | Pulsa Simular incidente | Recorrido de incidente/rework visible | Pendiente |
| GRA-04 | Pulsa Reiniciar | Visualización vuelve a Listo para iniciar | Pendiente |

## 7. Guion de defensa

| ID | Qué hace la persona | Qué debe ver al final | Test E2E |
|---|---|---|---|
| GUI-01 | Abre Guion defensa | Guion express y reglas operativas visibles | Pendiente |

---

## Resumen inicial

Flujos inventariados: 24

Distribución:
- Navegación/sesión: 2
- Contexto/producto: 4
- Operación/workflow: 8
- Evidencia multimodal: 3
- Trazabilidad: 2
- Grafo/arquitectura: 4
- Guion defensa: 1

## Regla de negocio crítica

CAMBIO_PRECIO es una consulta informativa y trazable.
No representa aprobación de precio.

ACCION_COMERCIAL consulta registros.
No ejecuta acciones comerciales de forma autónoma.

La visualización BPMN es didáctica y no debe redefinir estas reglas del producto.

