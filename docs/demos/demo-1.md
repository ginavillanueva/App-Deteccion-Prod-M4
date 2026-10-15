# Compromiso de entrega — Demo 1 | Release 8.1.0

**Proyecto:** App Detección Prod  
**Módulo:** 8 — Desarrollo Backend y APIs Escalables  
**Demo:** 1  
**Fecha prevista:** 19 de octubre de 2026  
**Responsable del compromiso:** Gina Fabiana Villanueva Viscarra  
**Estado:** Comprometido — pendiente de implementación

## 1. Funcionalidad comprometida

**FEATURE-01: Implementar alertas automáticas de productos próximos a vencer.**

**Issue de GitHub:** https://github.com/ginavillanueva/App-Deteccion-Prod-M4/issues/4

## 2. Objetivo

Implementar y demostrar una funcionalidad que identifique productos próximos a vencer y genere alertas según su fecha de vencimiento, permitiendo que supervisores y vendedores prioricen su seguimiento.

Esta funcionalidad forma parte de la gestión de productos críticos en sala y busca reducir la dependencia de controles manuales e información dispersa.

## 3. Alcance de la Demo 1

La demostración se enfocará únicamente en la detección y consulta de alertas de vencimiento.

Se contempla:
- Consultar productos y sus fechas de vencimiento.
- Calcular los días restantes hasta el vencimiento.
- Identificar y visualizar los productos que requieren atención.

No se incluyen en esta demo las modificaciones de precios ni la implementación completa del dashboard comercial.

## 4. Criterios de aceptación

- [ ] **CA-01 — Identificación:** el sistema identifica correctamente los productos próximos a vencer a partir de su fecha de vencimiento y una regla de alerta definida.

- [ ] **CA-02 — Información:** cada alerta presenta como mínimo el producto, la sala, la fecha de vencimiento, los días restantes y el nivel de prioridad.

- [ ] **CA-03 — Validación:** las pruebas automatizadas verifican la clasificación de alertas y la funcionalidad puede demostrarse con datos de ejemplo reproducibles.

## 5. Evidencias comprometidas

- Código fuente de la funcionalidad versionado en GitHub.
- Pruebas automatizadas y sus resultados.
- Capturas o registros de ejecución.
- Actualización del Issue #4 con referencia a la implementación.
- Registro de los commits correspondientes en el archivo de aportes.

## 6. Relación con el proyecto

La funcionalidad contribuye al objetivo de App Detección Prod de mejorar la detección temprana y el seguimiento de productos próximos a vencer.

**Referencia funcional:** caso de uso de detección y seguimiento de vencimientos. Su identificador exacto en el FSD deberá verificarse antes de la entrega final.

## 7. Estado y compromiso

Este documento registra una funcionalidad planificada para la Demo 1. Su publicación no acredita que la implementación ni las pruebas estén terminadas.

**Repositorio:** https://github.com/ginavillanueva/App-Deteccion-Prod-M4

**Rama de trabajo:** release/8.0.0
