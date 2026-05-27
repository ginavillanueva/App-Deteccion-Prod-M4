# App Detección Prod — Release 2.0.0

Entrega final del proyecto **App Detección Prod**, preparada para la rama `release/2.0.0`.

## Propósito del producto

App Detección Prod transforma un proceso informal de gestión de productos próximos a vencer —basado en WhatsApp, Excel, fotografías dispersas y comunicación verbal— en una plataforma trazable, medible y orientada a decisiones. El sistema centraliza el registro operativo, la validación táctica, las acciones comerciales, el control de precios, la medición de impacto financiero, el dashboard gerencial y la asistencia IA gobernada.

## Estructura evaluable según Defensa Final

```text
/
├── AGENTS.md
├── README.md
├── MANIFEST_RELEASE_2.0.0.json
├── docs/
│   ├── DTI.md
│   ├── PROMPT_MAPPING.md
│   ├── roadmap.md
│   ├── MAPA_RAPIDO_DEFENSA.md
│   ├── brd/BRD_vFinal.md
│   ├── mrd/MRD_vFinal.md
│   ├── prd/PRD_vFinal.md
│   ├── fsd/FSD_vFinal.md
│   ├── adr/0001-*.md ... 0005-*.md
│   ├── diagrams/*.mmd
│   ├── prompts/<area>/PR-*.md
│   ├── aportes/release-2.0.0.md
│   └── checklists/
└── pocs/
    ├── POC-01/
    └── POC-02/
```

## Trazabilidad principal

```text
BRD → MRD → PRD → FSD → ADRs → DTI → Diagramas → POCs → AGENTS → PROMPT_MAPPING → Roadmap
```

## Decisiones arquitectónicas aprobadas

| ADR | Decisión |
|---|---|
| ADR-0001 | Monolito modular evolutivo con límites claros de dominio. |
| ADR-0002 | Arquitectura hexagonal para proteger dominio, casos de uso, puertos y adaptadores. |
| ADR-0003 | Event-driven + Outbox, diferenciando dashboard inmediato de procesos asíncronos. |
| ADR-0004 | IA asistiva con guardrails y human-in-the-loop. |
| ADR-0005 | Despliegue AWS, observabilidad, seguridad y evolución cloud-ready. |

## Evidencia ejecutada

| POC | Qué valida | Evidencia |
|---|---|---|
| POC-01 | Registro transaccional, dashboard inmediato y Outbox | scripts, SQLite, métricas, gráficos y trazabilidad. |
| POC-02 | IA con scoring BAJO/MEDIO/ALTO, guardrails y bloqueo adversarial | dataset, resultados, métricas, prompt tests y auditoría. |

## Indicadores críticos

- Productos próximos a vencer por sala, región, marca y estado.
- Productos sin acción comercial.
- Valor financiero en riesgo.
- Precio anterior, precio nuevo, variación y valor intervenido.
- Diferencia entre precio aprobado y precio aplicado.
- Casos con cambio de precio no aprobado.
- Frescura del dashboard gerencial.
- Eventos Outbox pendientes, procesados o fallidos.
- Casos clasificados por IA como BAJO, MEDIO o ALTO.

## Rama de entrega

La entrega debe subirse a la rama:

```bash
release/2.0.0
```

Todo lo que no esté en esa rama al momento de evaluación queda fuera de la rúbrica.
