# Checklist de Defensa Final – App Detección Prod release/2.0.0

## 1. Estructura obligatoria

- [x] `AGENTS.md` en raíz del repositorio.
- [x] `docs/DTI.md` completo y aprobado.
- [x] `docs/brd/BRD_vFinal.md`.
- [x] `docs/mrd/MRD_vFinal.md`.
- [x] `docs/prd/PRD_vFinal.md`.
- [x] `docs/fsd/FSD_vFinal.md`.
- [x] Mínimo 3 ADRs; se entregan 5 ADRs aprobados.
- [x] Mínimo 2 POCs ejecutadas con evidencia; se entregan POC-01 y POC-02.
- [x] `docs/PROMPT_MAPPING.md`.
- [x] Prompts versionados en `docs/prompts/`.
- [x] Mínimo 8 diagramas `.mmd`; se entregan 14 diagramas.
- [x] `docs/roadmap.md`.
- [x] `docs/aportes/release-2.0.0.md`.

## 2. Coherencia documental

- [x] BRD define problema, objetivos, stakeholders, KPIs y reglas de negocio.
- [x] MRD traduce el problema a oportunidad de mercado y segmentos.
- [x] PRD transforma necesidad en capacidades, épicas e historias.
- [x] FSD baja el producto a casos de uso, flujos, reglas y criterios.
- [x] ADRs justifican decisiones con trade-offs.
- [x] DTI integra producto, dominio, arquitectura, IA, AWS, POCs y roadmap.
- [x] Diagramas visualizan C4, dominio, hexagonal, eventos, AWS, IA, seguridad y POCs.
- [x] POCs validan riesgos arquitectónicos.
- [x] AGENTS gobierna el trabajo de agentes IA.
- [x] PROMPT_MAPPING gobierna prompts como contratos trazables.

## 3. Puntos críticos para defensa

### 3.1 Dashboard inmediato

Explicar que los KPIs críticos de gerencia no dependen solo de procesos asíncronos. El registro, estado, precio, cantidad, valor financiero y datos críticos se actualizan transaccionalmente. Outbox queda para alertas, auditoría enriquecida, IA e integraciones.

### 3.2 Cambio de precio

Defender que el cambio de precio es una entidad financiera auditable, no un campo simple. Debe registrar precio anterior, precio nuevo, variación, cantidad, valor intervenido, responsable, motivo, evidencia y aprobación.

### 3.3 IA gobernada

Explicar que la IA clasifica y recomienda, pero no ejecuta decisiones irreversibles. La IA no cambia precios, no aprueba descuentos, no retira productos y no cierra casos.

### 3.4 Arquitectura

Defender monolito modular evolutivo con hexagonal porque evita microservicios prematuros, protege el dominio y deja seams claros para evolución distribuida.

### 3.5 POCs

POC-01 valida el flujo transaccional + dashboard + Outbox.  
POC-02 valida scoring IA + guardrails + human-in-the-loop.

## 4. Comandos sugeridos para subir a GitHub

```bash
git checkout -b release/2.0.0
mkdir -p docs/{brd,mrd,prd,fsd,adr,diagrams,aportes,prompts,checklists} pocs
git add .
git commit -m "docs: entrega final release 2.0.0 App Deteccion Prod"
git push origin release/2.0.0
```

## 5. Revisión final antes de enviar

- [ ] Confirmar que la rama en GitHub sea `release/2.0.0`.
- [ ] Confirmar que todos los archivos estén visibles en GitHub.
- [ ] Abrir `docs/DTI.md` y verificar enlaces/rutas.
- [ ] Abrir `docs/diagrams/00_VISTA_RAPIDA_DIAGRAMAS.md`.
- [ ] Abrir `pocs/POC-01/POC-01.md` y `pocs/POC-02/POC-02.md`.
- [ ] Confirmar que `AGENTS.md` esté en la raíz.
- [ ] Confirmar que `docs/PROMPT_MAPPING.md` referencie prompts existentes.
- [ ] Confirmar que `docs/aportes/release-2.0.0.md` esté completo.
```
