# PR_07 — Documentación de contribución individual

**Feature / PR:** Individual contribution and academic accountability  
**Estado:** APROBADO / ENTREGA FINAL  
**Artefactos relacionados:** `docs/APORTES.md`, `docs/README_APORTES.md`, `docs/TRAZABILIDAD_ENTREGA_09.md`

---

## 1. Objetivo

Documentar la contribución individual asociada al proyecto **App Detección Prod — BPMN Workflow Engine**, cumpliendo el requisito de la consigna de explicitar la responsabilidad de cada integrante.

---

## 2. Decisiones tomadas

1. Registrar la contribución en `docs/APORTES.md` como documento principal.
2. Separar el aporte humano del uso de IA generativa.
3. Mapear la contribución por entregable y por capa técnica.
4. Mantener trazabilidad con `prompt_mappings.md`, `PR_implementation` y `00_CONTROL_APROBACIONES.md`.
5. Declarar explícitamente que la IA es herramienta de apoyo y no integrante del equipo.

---

## 3. Relación con PRD y FSD

| Documento | Relación |
|---|---|
| `docs/PRD.md` | Define qué se construye y los criterios de éxito que orientan los aportes. |
| `docs/FSD.md` | Define cómo funciona el motor y permite asignar responsabilidad por componentes. |
| `docs/prompt_mappings.md` | Registra apoyo de IA y mantiene trazabilidad del proceso de generación. |
| `tests/` | Sirve como evidencia objetiva de validación técnica. |

---

## 4. Resultado

Se agregó:

- `docs/APORTES.md`
- `docs/README_APORTES.md`
- `docs/TRAZABILIDAD_ENTREGA_09.md`
- actualización de `00_CONTROL_APROBACIONES.md`
- actualización de `README_REVISION.md`

---

## 5. Criterios de aceptación

| Criterio | Estado |
|---|---|
| Existe documento de aportes individuales | Cumplido |
| Se identifica al integrante documentado | Cumplido |
| Se asignan responsabilidades por componente | Cumplido |
| Se separa uso de IA de autoría académica | Cumplido |
| Se mantiene trazabilidad con PRD/FSD/código/tests | Cumplido |
| Se conserva paquete acumulado de aprobaciones | Cumplido |

---

## 6. Riesgos y mitigación

| Riesgo | Mitigación |
|---|---|
| Que el docente exija más integrantes | El documento incluye nota para completar con nombres reales si aplica. |
| Que se interprete IA como autora | Se declara explícitamente que IA fue herramienta y se remite a `prompt_mappings.md`. |
| Que el aporte parezca genérico | Se conecta con carpetas, PRs, pruebas y entregables concretos. |

---

## 7. Verificación

```bash
python -m compileall src
python -m unittest discover -s tests
```

Resultado esperado:

```text
Ran 28 tests
OK
```
