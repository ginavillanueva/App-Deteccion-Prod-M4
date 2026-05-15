### BRD.md – Business Requirements Document

# BRD – App Detección Prod

## 0. Metadatos

| Campo              | Valor                                                                                     |
| ------------------ | ----------------------------------------------------------------------------------------- |
| Producto           | App Detección Prod                                                                        |
| Grupo              | G07                                                                                       |
| Versión            | v0.1                                                                                      |
| Fecha              | 14/05/2026                                                                                |
| Sponsor de negocio | Gerencia Comercial                                                                        |
| Stakeholders       | Mercaderistas, Supervisores, Vendedores, Gerencia Comercial, Operaciones, Trade Marketing |
| Autores            | Gina Fabiana Villanueva Viscarra                                                          |
| Revisores          | Docente + 1 grupo par                                                                     |
| Estado             | Borrador                                                                                  |

## 1. Resumen ejecutivo

App Detección Prod es una plataforma de trazabilidad comercial y operativa para distribuidoras e importadoras en canal moderno. Centraliza la información sobre productos críticos próximos a vencer, acciones comerciales, precios y promociones, permitiendo generar indicadores estratégicos en tiempo real, reducir pérdidas y mejorar la eficiencia operativa.

## 2. Contexto del negocio

* Organización: Distribuidoras e importadoras en canal moderno.
* Procesos afectados: Gestión de productos críticos, control de vencimientos, gestión de promociones y descuentos, validación operativa, seguimiento comercial.
* Estrategia: Reducir pérdidas, mejorar trazabilidad, optimizar decisiones, incrementar eficiencia operativa.

## 3. Problema y oportunidad

### Problema

Procesos manuales dispersos provocan errores, duplicación de acciones, pérdidas económicas y baja visibilidad estratégica.

### Oportunidad

Centralizar información, mejorar coordinación, incrementar velocidad de respuesta y profesionalizar la gestión operativa.

## 4. Usuarios objetivo / Personas clave

* **Mercaderista**: registra productos, reporta vencimientos, aplica promociones.
* **Supervisor Regional**: valida información operativa, controla acciones comerciales.

## 5. Propuesta de valor

* Plataforma centralizada de trazabilidad comercial y operativa.
* Reducción de pérdidas, visibilidad estratégica y alertas en tiempo real.

## 6. Panorama competitivo

* WhatsApp + Excel (do-nothing), ERP empresarial, supervisión manual, apps de auditoría retail.

## 7. Business Model Canvas

| Bloque                | Elementos                                                           |
| --------------------- | ------------------------------------------------------------------- |
| Segmentos de clientes | Distribuidoras / Importadoras / Áreas comerciales                   |
| Propuesta de valor    | Centralización / Reducción de pérdidas / Visibilidad estratégica    |
| Canales               | App móvil / Dashboard / Alertas                                     |
| Relación con clientes | Seguimiento continuo / Experiencia por rol / Trazabilidad           |
| Fuentes de ingresos   | Suscripción / Licenciamiento / Capacitación                         |
| Recursos clave        | Información centralizada / Operación en campo / Conocimiento retail |
| Actividades clave     | Monitoreo / Gestión comercial / Indicadores                         |
| Socios clave          | Supermercados / Farmacias / Áreas internas                          |
| Estructura de costos  | Implementación / Operación / Soporte                                |

## 8. Métricas clave de éxito

| ID     | KPI                       | North Star? | Meta  |
| ------ | ------------------------- | ----------- | ----- |
| KPI-01 | Reducción de devoluciones | Sí          | -30 % |
| KPI-02 | Tiempo de validación      | No          | -60 % |
| KPI-03 | Gestión preventiva        | No          | 80 %  |

## 9. Objetivos SMART

| ID    | Objetivo                       | Meta  |
| ----- | ------------------------------ | ----- |
| BO-01 | Reducir devoluciones y cambios | -30 % |
| BO-02 | Reducir tiempo de validación   | -60 % |
| BO-03 | Incrementar gestión preventiva | 80 %  |

## 10. Stakeholders y roles (RACI)

| Stakeholder         | Rol |
| ------------------- | --- |
| Gerencia Comercial  | A   |
| Supervisor Regional | R   |
| Mercaderista        | C   |
| Vendedor            | C   |
| Operaciones         | I   |

## 11. Requerimientos de negocio

| ID     | Requerimiento                         |
| ------ | ------------------------------------- |
| BR-001 | Registrar productos críticos          |
| BR-002 | Registrar vencimientos y evidencia    |
| BR-003 | Registrar acciones comerciales        |
| BR-004 | Controlar cambios de precio           |
| BR-005 | Visualizar información en tiempo real |
| BR-006 | Generar alertas operativas            |
| BR-007 | Generar indicadores estratégicos      |
| BR-008 | Centralizar trazabilidad              |

## 12. Reglas de negocio

| ID    | Regla                                                     |
| ----- | --------------------------------------------------------- |
| RB-01 | Ningún producto crítico puede quedar sin acción comercial |
| RB-02 | Toda modificación de precio debe registrar responsable    |
| RB-03 | Todo producto crítico debe tener evidencia fotográfica    |
| RB-04 | Toda acción debe mantener historial                       |

## 13. Supuestos, restricciones y dependencias

* Supuestos: usuarios con smartphones, adopción del sistema centralizado.
* Restricciones: conectividad variable, diferencias de nivel digital.
* Dependencias: participación de stakeholders y coordinación entre áreas.

## 14. Alcance de negocio

* En alcance: registro productos críticos, control vencimientos, registro promociones, control de precios, dashboard estratégico, alertas operativas.
* Fuera de alcance: inventario completo, facturación, ERP financiero, logística avanzada.

## 15. Beneficios esperados

* Reducción de devoluciones, ahorro operativo, inversión y operación estimadas año 1-3.

## 16. Riesgos de negocio

* Baja adopción, resistencia al cambio, información inconsistente.

## 17. Criterios de éxito

* Cumplimiento objetivos SMART, reducción de devoluciones, centralización operativa, mejora en trazabilidad y visibilidad estratégica.

## 18. Trazabilidad a documentos hijos

| BRD ID | MRD    | PRD    | FSD        |
| ------ | ------ | ------ | ---------- |
| BR-001 | MRD-01 | PRD-01 | FSD-UC-001 |

## 19. Aprobaciones

| Rol        | Nombre    | Firma | Fecha |
| ---------- | --------- | ----- | ----- |
| Sponsor    | Pendiente |       |       |
| PM         | Pendiente |       |       |
| Arquitecto | Pendiente |       |       |

## 20. Registro de cambios

| Versión | Fecha      | Autor                            | Cambio          |
| ------- | ---------- | -------------------------------- | --------------- |
| v0.1    | 14/05/2026 | Gina Fabiana Villanueva Viscarra | Versión inicial |
