# PROMPT_MAPPING.md – Mapeo de Prompts

## 0. Metadatos
| Campo | Valor |
|-------|-------|
| Versión | 1.0 |
| Fecha | 14/05/2026 |
| Autor | Gina Fabiana Villanueva Viscarra |
| Estado | Completo |
| Branch | release/1.0.0 |
| Relación | FSD, PRD, POCs, AGENTS.md |

## 1. Propósito
Este documento registra todos los **prompt-contracts** utilizados en la App Detección Prod. Cada prompt está asociado a un **Caso de Uso (UC)** crítico o POC, con los 6 elementos obligatorios, invariantes y failure modes, para garantizar trazabilidad y reproducibilidad de la inteligencia artificial en el sistema.

## 2. Mapeo de prompts por UC

| UC / POC | Prompt ID | Artefacto origen | Propósito | Modelo recomendado | Temperatura | Failure modes / Invariants | Observaciones |
|-----------|-----------|----------------|-----------|-----------------|------------|---------------------------|---------------|
| FSD-UC-001 | PR-UC-001 | FSD-UC-001 | Registro de producto crítico con alertas | Sonnet | 0.0 | Validar campos obligatorios, prevenir duplicados, no exponer PII | Asociado a agent-orchestrator y rag-service |
| FSD-UC-002 | PR-UC-002 | FSD-UC-002 | Consolidación y ejecución de acciones comerciales | Sonnet | 0.1 | Validar consistencia de datos, aplicar reglas RB-01 a RB-04 | Asociado a model-router y prompt-validator |
| FSD-UC-003 | PR-UC-003 | FSD-UC-003 | Validación de reportes y control SLA | Sonnet | 0.0 | Detectar desviaciones, registrar auditoría, no modificar datos históricos | Asociado a alerting-agent y analytics-agent |
| FSD-UC-004 | PR-UC-004 | FSD-UC-004 | Visualización de KPIs estratégicos | Sonnet | 0.1 | Validar consistencia y latencia < 2 seg, no exponer PII | Asociado a analytics-agent |
| POC-01 | PR-POC-01 | POC-01 | Validación de alertas predictivas | Sonnet | 0.0 | Garantizar detección ≥80%, latencia <500 ms, prevenir falsos positivos | Asociado a agent-orchestrator y rag-service |
| POC-02 | PR-POC-02 | POC-02 | Visualización KPIs en tiempo real | Sonnet | 0.0 | Latencia < 2 seg, datos consistentes, prevenir pérdida de eventos | Asociado a KPIService y dashboards |

## 3. Invariantes y Failure Modes generales
- Todos los prompts deben **respetar el esquema definido en FSD-UC**.
- Los prompts no deben exponer información sensible ni PII.
- Deben generar outputs consistentes para entradas idénticas.
- Si un prompt falla en la validación, la ejecución se detiene y se registra el error.
- Los prompts de POCs deben tener métricas de latencia y cobertura claramente definidas.

## 4. Flujo de uso
```mermaid
flowchart LR
  UC1[FSD-UC-001] --> PR1[PR-UC-001 Prompt]
  UC2[FSD-UC-002] --> PR2[PR-UC-002 Prompt]
  UC3[FSD-UC-003] --> PR3[PR-UC-003 Prompt]
  UC4[FSD-UC-004] --> PR4[PR-UC-004 Prompt]
  POC1[POC-01] --> PR5[PR-POC-01 Prompt]
  POC2[POC-02] --> PR6[PR-POC-02 Prompt]

## 5. Observaciones
Todos los prompts están versionados y referenciados en AGENTS.md para su ejecución.
Se asegura trazabilidad completa entre FSD → PRD → POC → Prompt → AGENTS.
Permite auditoría y replicabilidad de la ejecución de cada UC crítico.

## 6. Historial
| Versión | Fecha      | Autor        | Cambio                                                         |
| ------- | ---------- | ------------ | -------------------------------------------------------------- |
| 1.0     | 14/05/2026 | Gina Fabiana | Creación del PROMPT_MAPPING.md completo con UC y POC asociados |
