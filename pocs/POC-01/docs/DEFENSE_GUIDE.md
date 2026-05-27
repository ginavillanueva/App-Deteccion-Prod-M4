# Guía de defensa oral — POC-01

## 1. Explicación en 60 segundos

Esta POC valida el flujo crítico de App Detección Prod: registrar productos próximos a vencer, registrar cambio de precio, actualizar el dashboard gerencial de forma inmediata y dejar eventos confiables en Outbox. Sirve para demostrar que gerencia puede tomar decisiones con información actualizada, y que el sistema puede generar trazabilidad para alertas, auditoría e IA sin introducir microservicios prematuros.

## 2. Cómo defender la decisión síncrona/asíncrona

- Síncrono/transaccional: estado del caso, precio anterior, precio nuevo, cantidad, KPIs críticos del dashboard.
- Asíncrono/Outbox: alertas, notificaciones, auditoría enriquecida, IA, analytics histórico e integraciones futuras.

Frase clave:

> El dashboard gerencial no puede depender únicamente de eventos asíncronos porque se usa para decisiones inmediatas. Por eso la POC actualiza KPIs críticos dentro de la transacción y usa Outbox para procesos derivados.

## 3. Preguntas probables

| Pregunta | Respuesta |
|---|---|
| ¿Por qué esta POC es necesaria? | Porque valida el punto más riesgoso: consistencia entre registro, precio, dashboard y eventos. |
| ¿Por qué no todo asíncrono? | Porque gerencia necesita datos actualizados para decidir. |
| ¿Qué aporta Outbox? | Garantiza eventos confiables sin perder trazabilidad y sin microservicios prematuros. |
| ¿Qué prueba el KPI de precio? | Que precio anterior, precio nuevo y valor intervenido pueden auditarse y medirse. |
| ¿Qué no prueba? | No prueba UI, concurrencia real, AWS real ni IA. Eso se cubre en otros artefactos/POCs. |

## 4. Frase final de defensa

La POC confirma que la arquitectura propuesta no es solo conceptual: puede sostener el flujo crítico del negocio con evidencia medible, trazabilidad y un camino claro de evolución a AWS y event-driven distribuido.
