# ADR-0006 — Implementar FSD-UC-001 como monolito modular con FastAPI y adaptador SQLite

## Estado
Aceptado.

## Contexto
La consigna exige desarrollar una funcionalidad del FSD y presentar una demo. El repositorio M4 tiene una base documental fuerte, pero necesita una implementación ejecutable, testeable y trazable.

La funcionalidad elegida es `FSD-UC-001`, porque concentra el valor del proyecto: registro estructurado, acción comercial, control de precio, riesgo y dashboard.

## Decisión
Implementar la UC como monolito modular en Python/FastAPI, con repositorio in-memory para tests y adaptador SQLite para demo local.

## Razones
- Permite demostrar una funcionalidad completa sin intentar construir toda la plataforma.
- Mantiene separación de capas coherente con arquitectura hexagonal.
- Permite cobertura de tests ≥90%.
- Permite demo local simple.
- Evita sobredimensionar con microservicios para una sola UC.

## Consecuencias positivas
- Demo clara y defendible.
- Trazabilidad completa PRD → FSD → DD → ADR → Prompt → Código → Tests → DTP.
- Bajo costo de ejecución.
- Fácil de subir al repositorio.

## Consecuencias negativas
- SQLite no representa la persistencia productiva final.
- No incluye autenticación enterprise completa.
- No incluye frontend visual completo.

## Guardrails
- La IA no cambia precios automáticamente.
- La IA no aprueba descuentos.
- La IA no cierra casos.
- Los cambios de precio quedan auditados.

## Trazabilidad
- PRD-REQ-001, PRD-REQ-002, PRD-REQ-003, PRD-REQ-004
- FSD-UC-001
- DD-UC-001
- PR-IMPL-001
