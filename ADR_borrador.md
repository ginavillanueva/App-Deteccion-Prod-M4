
# ADR-001 — Arquitectura Mobile + Backend Cloud

## Contexto

**Problema**: El personal operativo trabaja en movilidad y requiere acceso distribuido y centralizado.

## Decisión Tentativa

Implementar una aplicación móvil conectada a servicios backend cloud.

## Justificación Técnica

Esta solución permite escalabilidad, acceso remoto, sincronización centralizada y soporte multiusuario. El modelo mobile + backend cloud asegura la disponibilidad de datos en tiempo real, sin importar la conectividad.

## Impacto Esperado

- Alta disponibilidad.
- Acceso en tiempo real para usuarios móviles.
- Reducción de la dependencia de canales informales de comunicación.
- Flexibilidad para integrar nuevas funcionalidades.

---

# ADR-002 — Estrategia Offline-First

## Contexto

**Problema**: Los mercaderistas trabajan en zonas con conectividad variable.

## Decisión Tentativa

Permitir almacenamiento local temporal y sincronización diferida, en caso de falta de conexión.

## Justificación Técnica

La estrategia offline-first ofrece continuidad operativa en áreas con conexión limitada. Esta arquitectura permite que los usuarios trabajen sin problemas incluso sin acceso a internet, garantizando que toda la información se sincronice cuando la conexión se restablezca.

## Impacto Esperado

- Mejora la experiencia del usuario en campo.
- Reduce la dependencia de la conectividad constante.
- Menor riesgo de pérdida de datos.

---

# ADR-003 — Evidencia Fotográfica Obligatoria

## Contexto

**Problema**: Los reportes actuales carecen de validación visual estructurada.

## Decisión Tentativa

Exigir al menos una fotografía por registro de producto, con instrucciones claras sobre la calidad y la visibilidad del producto.

## Justificación Técnica

La evidencia fotográfica aumenta la trazabilidad y permite realizar auditorías visuales para garantizar la precisión del registro. Esto también facilita la verificación a distancia por supervisores o gerentes.

## Impacto Esperado

- Reducción de errores en los registros.
- Mejora en la confianza y confiabilidad de la información.
- Trazabilidad mejorada para auditorías y decisiones estratégicas.

---

# ADR-004 — Sistema de Notificaciones en Tiempo Real

## Contexto

**Problema**: Las decisiones tardías incrementan pérdidas por vencimiento de productos.

## Decisión Tentativa

Implementar alertas automáticas basadas en eventos críticos, como productos próximos a vencer o acciones comerciales pendientes.

## Justificación Técnica

Las notificaciones en tiempo real permiten que los usuarios (mercaderistas, supervisores, etc.) reaccionen rápidamente ante eventos críticos. Esto mejora la eficiencia operativa y minimiza la pérdida de oportunidades.

## Impacto Esperado

- Mejora en la velocidad de toma de decisiones.
- Reducción de la merma por productos vencidos.
- Mejor respuesta ante situaciones de emergencia operativa.

---

# ADR-005 — Base de Datos Centralizada

## Contexto

**Problema**: La información actual está fragmentada entre múltiples canales de comunicación.

## Decisión Tentativa

Consolidar toda la información operativa y comercial en una base de datos única que esté accesible para todos los actores del sistema.

## Justificación Técnica

Una base de datos centralizada garantiza que todos los usuarios tengan acceso a la misma información actualizada en tiempo real. Esto mejora la consistencia y la trazabilidad de los datos.

## Impacto Esperado

- Mayor consistencia y precisión de los datos.
- Acceso rápido y seguro a la información.
- Mejora en la eficiencia operativa.

---

# ADR-006 — Gestión de Roles y Autenticación

## Contexto

**Problema**: Cada actor dentro del sistema requiere distintos niveles de acceso y visualización según su rol.

## Decisión Tentativa

Implementar un sistema de control de acceso basado en roles (RBAC) para gestionar la autenticación de usuarios y su acceso a funcionalidades específicas del sistema.

## Justificación Técnica

El sistema RBAC asegura que los usuarios solo puedan acceder a las funcionalidades y datos necesarios para su rol, garantizando la seguridad y la correcta distribución de permisos.

## Impacto Esperado

- Mayor seguridad en la plataforma.
- Garantía de que solo los usuarios autorizados accedan a información sensible.
- Flexibilidad para gestionar permisos de manera eficiente.

---

# ADR-007 — Motor de Sincronización Offline

## Contexto

**Problema**: Existe el riesgo de inconsistencias entre los datos locales de los usuarios y los datos centrales debido a la falta de sincronización automática cuando hay conectividad limitada.

## Decisión Tentativa

Desarrollar un motor de sincronización que permita resolver conflictos y asegurar la integridad de los datos entre dispositivos locales y el sistema central.

## Justificación Técnica

Un sistema de sincronización confiable asegura que los datos locales y centrales se mantengan consistentes y evita pérdidas de información cuando los usuarios trabajan en modo offline. Este sistema debe ser capaz de detectar y resolver conflictos de manera eficiente.

## Impacto Esperado

- Garantía de la integridad de los datos.
- Sincronización eficiente en escenarios de conectividad intermitente.
- Mejor experiencia de usuario en áreas con baja conectividad.

---

# ADR-008 — Dashboard Analítico Estratégico

## Contexto

**Problema**: La gerencia necesita métricas consolidadas y visibilidad ejecutiva sobre el desempeño de los productos y las acciones comerciales.

## Decisión Tentativa

Desarrollar un dashboard centralizado para visualizar KPIs estratégicos y métricas clave.

## Justificación Técnica

Los dashboards permiten la visualización clara de los datos clave, facilitando la toma de decisiones estratégicas basadas en métricas reales y actualizadas.

## Impacto Esperado

- Mejora en la toma de decisiones estratégicas.
- Incremento de la visibilidad de los KPIs de negocio.
- Facilitación de la toma de decisiones proactivas por parte de la gerencia.

