# RUBRICA_DEFENSA_FINAL_AUTOEVALUACION.md

## Autoevaluación de cumplimiento — release/2.0.0

| Criterio de defensa | Evidencia en el repositorio | Estado |
|---|---|---|
| Coherencia MRD → PRD → FSD → DTI | `docs/mrd/`, `docs/prd/`, `docs/fsd/`, `docs/DTI.md`, `docs/MAPA_RAPIDO_DEFENSA.md` | Cumple |
| DTI con secciones amplias y trazabilidad | `docs/DTI.md` | Cumple |
| C4 + hexagonal + distribuido + event-driven + AWS | `docs/DTI.md`, `docs/diagrams/*.mmd`, `docs/adr/*.md` | Cumple |
| Trade-offs y ADRs | `docs/adr/0001-*.md` a `0005-*.md` | Cumple |
| AGENTS.md ejecutable y sincronizado | `AGENTS.md` | Cumple |
| ≥2 POCs ejecutadas con métricas | `pocs/POC-01/`, `pocs/POC-02/` | Cumple |
| Mapeo rápido documentado | `docs/MAPA_RAPIDO_DEFENSA.md`, `docs/PROMPT_MAPPING.md` | Cumple |
| ≥8 diagramas Mermaid versionados | `docs/diagrams/*.mmd` | Cumple |
| Roadmap final | `docs/roadmap.md` | Cumple |
| Aportes individuales | `docs/aportes/release-2.0.0.md` | Cumple |

## Riesgos controlados

| Riesgo | Control documental/técnico |
|---|---|
| Que el dashboard gerencial quede desactualizado | ADR-0003 separa dashboard crítico transaccional de procesos asíncronos. |
| Que IA cambie precios o apruebe acciones | ADR-0004, AGENTS.md y POC-02 bloquean acciones irreversibles automáticas. |
| Que los prompts sean improvisados | PROMPT_MAPPING exige prompt-contratos versionados, pruebas e invariantes. |
| Que la arquitectura sea sobreingenierizada | ADR-0001 justifica monolito modular evolutivo. |
| Que no exista evidencia ejecutada | POC-01 y POC-02 incluyen scripts, métricas, gráficos y resultados. |
