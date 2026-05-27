# Diagramas Mermaid — App Detección Prod

**Versión:** v1.4 profesional para revisión  
**Rama sugerida:** `release/2.0.0`  
**Ubicación sugerida:** `docs/diagrams/`

Este paquete contiene diagramas `.mmd` profesionales, visualmente más claros y trazables con los documentos aprobados: BRD, MRD, PRD, FSD, DTI y ADR-0001 a ADR-0005. Los diagramas están diseñados para defender la arquitectura final del proyecto App Detección Prod, incluyendo C4, arquitectura hexagonal, event-driven/outbox, dashboard gerencial inmediato, control de cambio de precio, IA con guardrails, AWS y trazabilidad documental.

## Cómo visualizar los diagramas

### Opción 1 — GitHub
GitHub renderiza Mermaid dentro de archivos Markdown. Para una vista rápida, abre:

`00_VISTA_RAPIDA_DIAGRAMAS.md`

Ese archivo contiene todos los diagramas embebidos en bloques `mermaid`.

### Opción 2 — Mermaid Live Editor
1. Entra a Mermaid Live Editor.
2. Abre cualquier archivo `.mmd` de este paquete.
3. Copia todo el contenido.
4. Pégalo en el editor.
5. Exporta como PNG, SVG o PDF si necesitas evidencias visuales.

### Opción 3 — Visual Studio Code
1. Instala la extensión **Markdown Preview Mermaid Support** o **Mermaid Preview**.
2. Abre los `.mmd` o `00_VISTA_RAPIDA_DIAGRAMAS.md`.
3. Usa vista previa (`Ctrl+Shift+V` o `Cmd+Shift+V`).

### Opción 4 — Documentación del repo
Sube estos archivos a:

```text
docs/diagrams/
```

Y referencia los diagramas desde `docs/DTI.md`.

## Criterios cubiertos

- C4 Nivel 1, 2 y 3.
- Arquitectura hexagonal.
- Modelo de dominio.
- Secuencias funcionales críticas.
- Cambio de precio auditado.
- Dashboard gerencial inmediato.
- Event-driven + Outbox.
- IA con guardrails y human-in-the-loop.
- Deployment AWS.
- Observabilidad, seguridad y trazabilidad.
- Relación BRD → MRD → PRD → FSD → ADRs → DTI → POCs.

## Archivos

| Archivo | Propósito |
|---|---|
| `01_c4_context_profesional.mmd` | Contexto C4: actores, sistema y sistemas externos. |
| `02_c4_container_profesional.mmd` | Contenedores: frontend, API modular, DB, outbox, dashboard, IA, AWS. |
| `03_c4_component_core_profesional.mmd` | Componentes internos del core. |
| `04_hexagonal_core_profesional.mmd` | Puertos, adaptadores y dominio protegido. |
| `05_domain_model_profesional.mmd` | Modelo de dominio y relaciones clave. |
| `06_sequence_registro_producto_profesional.mmd` | Registro y validación de producto próximo a vencer. |
| `07_sequence_cambio_precio_profesional.mmd` | Cambio de precio auditado y KPI inmediato. |
| `08_event_driven_outbox_dashboard_profesional.mmd` | Outbox, eventos, dashboard inmediato y procesos asíncronos. |
| `09_ai_guardrails_human_loop_profesional.mmd` | IA asistiva con límites y control humano. |
| `10_aws_deployment_profesional.mmd` | Despliegue cloud en AWS. |
| `11_state_lifecycle_alerta_profesional.mmd` | Ciclo de vida del caso/alerta. |
| `12_traceability_map_profesional.mmd` | Trazabilidad documental. |
| `13_observability_security_profesional.mmd` | Seguridad, auditoría y observabilidad. |
| `14_poc_validation_map_profesional.mmd` | Relación entre riesgos, POCs y evidencias. |
