# FSD — Dos features de demo aplicada

**Producto:** App Detección Prod  
**Documento:** FSD-FEAT-001-002  
**Estado:** PARA REVISIÓN  
**Rama sugerida:** `release/4.0.0-dos-features-demo-aplicada`

## 1. Contexto funcional

El producto busca transformar el proceso actual de reportes dispersos por WhatsApp, fotos y comunicación informal en una solución digital estructurada, trazable y medible. La aplicación debe centralizar el registro de productos próximos a vencer, integrar acciones comerciales, controlar precios actuales y modificados, registrar cantidades intervenidas y generar indicadores estratégicos para supervisión y gerencia.

Esta fase toma como base la funcionalidad ya probada en la demo anterior, pero la eleva a una demo aplicada con interfaz web: el docente debe poder ver el flujo completo como producto, no solo como API.

## 2. Alcance funcional

### Incluye

- Interfaz visual de registro para mercaderista.
- Cálculo automático de riesgo y métricas comerciales.
- Bandeja visual de casos para supervisor.
- Aprobación o rechazo de caso.
- Dashboard gerencial con KPIs actualizados.
- Eventos y trazabilidad visibles.
- Tests automatizados con cobertura mínima de 90%.

### No incluye en esta fase

- Autenticación real con usuarios productivos.
- Carga real de fotografías.
- Integración con ERP, POS o sistema comercial externo.
- Deploy cloud.
- IA generativa con API externa.

## 3. Feature 1 — Registro visual de producto crítico con acción comercial y cambio de precio

### Código

`FEAT-001 / FSD-UC-001`

### Objetivo

Permitir que el mercaderista registre desde una pantalla web un producto próximo a vencer, su cantidad, acción comercial y cambio de precio, generando automáticamente métricas de impacto y riesgo.

### Actor principal

Mercaderista.

### Actores secundarios

Supervisor, vendedor canal moderno, gerencia comercial.

### Precondiciones

- La app está corriendo localmente.
- La base de datos o repositorio en memoria está inicializado.
- El usuario ingresa a `/app` o `/app/register`.

### Datos de entrada

| Campo | Tipo | Requerido | Regla |
|---|---|---:|---|
| store | texto | Sí | No vacío |
| product_name | texto | Sí | No vacío |
| batch | texto | Sí | No vacío |
| expiration_date | fecha | Sí | Formato `YYYY-MM-DD` |
| quantity | entero | Sí | Mayor a 0 |
| current_price | decimal | Sí | Mayor o igual a 0 |
| new_price | decimal | No | Mayor o igual a 0; si existe, se audita cambio |
| commercial_action | enum | Sí | DESCUENTO, BANDEO, PROMOCION, RETIRO, PENDIENTE |
| price_change_approved | booleano | Sí | Si hay cambio de precio, debe quedar explícito |
| price_change_reason | texto | Condicional | Requerido si hay cambio de precio |
| evidence_note | texto | Sí | Describe evidencia visual o documental |
| created_by | texto | Sí | Usuario que registra |

### Reglas funcionales

- Si `new_price` es menor que `current_price`, se calcula descuento porcentual.
- Si hay cambio de precio, se genera auditoría de precio.
- El valor financiero en riesgo se calcula como `quantity * current_price`.
- El valor intervenido se calcula como `quantity * abs(current_price - new_price)` cuando hay cambio de precio.
- El riesgo se calcula por vencimiento, valor financiero, acción comercial, evidencia y aprobación de precio.
- El registro genera eventos de dominio visibles en la demo.

### Flujo principal

1. El mercaderista abre la pantalla de registro.
2. Ingresa tienda, producto, lote, fecha de vencimiento, cantidad, precio actual y nuevo precio.
3. Selecciona la acción comercial.
4. Agrega motivo y nota de evidencia.
5. Presiona “Registrar caso”.
6. El sistema valida campos obligatorios.
7. El sistema calcula días al vencimiento, valor financiero, descuento, riesgo y eventos.
8. El sistema muestra una tarjeta de confirmación con el caso creado.
9. El caso queda disponible para supervisión.

### Flujos alternativos

**A1 — Sin cambio de precio**  
El usuario registra el caso con acción comercial diferente a descuento. El sistema mantiene `new_price = current_price` o nulo según diseño, sin generar evento de cambio de precio.

**A2 — Evidencia incompleta**  
El sistema permite registrar, pero marca el riesgo o advertencia de evidencia para revisión.

**A3 — Precio no aprobado**  
El sistema permite registrar, pero etiqueta el caso como “requiere validación” y lo muestra en la bandeja del supervisor.

### Excepciones

| Código | Caso | Respuesta esperada |
|---|---|---|
| FEAT001-E01 | Cantidad menor o igual a cero | Mensaje de validación en pantalla |
| FEAT001-E02 | Fecha inválida | Mensaje de validación en pantalla |
| FEAT001-E03 | Cambio de precio sin motivo | Mensaje de validación |
| FEAT001-E04 | Acción comercial inválida | Mensaje de validación |

### Postcondiciones

- Existe un caso registrado.
- El caso tiene riesgo calculado.
- El caso tiene trazabilidad de origen.
- El caso aparece en bandeja de supervisión.
- El dashboard puede reflejar el impacto.

### Eventos emitidos

| Evento | Cuándo se emite | Payload mínimo |
|---|---|---|
| ProductCaseRegistered.v1 | Al registrar caso | case_id, product_name, store, quantity, risk_level |
| PriceChangeAudited.v1 | Si hay cambio de precio | case_id, current_price, new_price, approved, diff |
| CaseRiskClassified.v1 | Después del scoring | case_id, score, level, reasons |

## 4. Feature 2 — Bandeja de supervisión + dashboard gerencial actualizado

### Código

`FEAT-002 / FSD-UC-002`

### Objetivo

Permitir que el supervisor revise casos registrados, apruebe o rechace la intervención y que gerencia visualice KPIs actualizados para decisiones operativas y estratégicas.

### Actor principal

Supervisor.

### Actor secundario

Gerencia comercial.

### Precondiciones

- Existe al menos un caso registrado.
- El usuario ingresa a `/app/supervisor` o `/app/dashboard`.

### Funcionalidades incluidas

| Vista | Función |
|---|---|
| Bandeja supervisor | Listar casos, ver riesgo, estado, tienda, producto y acción |
| Detalle de caso | Revisar datos del registro, precio, riesgo y evidencia |
| Validación | Aprobar o rechazar con comentario |
| Dashboard gerencial | Mostrar KPIs actualizados |
| Eventos y trazabilidad | Mostrar secuencia de eventos generados |

### KPIs del dashboard

| KPI | Definición |
|---|---|
| total_cases | Total de casos registrados |
| validated_cases | Casos aprobados por supervisor |
| rejected_cases | Casos rechazados |
| pending_cases | Casos pendientes de validación |
| high_risk_cases | Casos con riesgo ALTO |
| medium_risk_cases | Casos con riesgo MEDIO |
| low_risk_cases | Casos con riesgo BAJO |
| total_financial_value_at_risk | Suma de valor financiero en riesgo |
| total_intervened_quantity | Suma de unidades intervenidas |
| price_change_cases | Casos con cambio de precio |
| unapproved_price_change_cases | Casos con cambio de precio no aprobado |
| average_discount_percent | Promedio de descuento aplicado |
| actions_by_type | Conteo por acción comercial |

### Flujo principal

1. El supervisor abre la bandeja.
2. Visualiza casos pendientes y nivel de riesgo.
3. Abre el detalle de un caso.
4. Revisa evidencia, acción, precio y scoring.
5. Ingresa comentario.
6. Aprueba o rechaza.
7. El sistema actualiza estado.
8. El sistema genera evento de validación.
9. El dashboard gerencial refleja el cambio.

### Flujos alternativos

**A1 — Rechazo de caso**  
El supervisor rechaza el caso y queda visible como rechazado. El dashboard actualiza rejected_cases.

**A2 — Caso ya validado**  
Si el caso ya fue validado, el sistema bloquea doble validación y muestra mensaje claro.

**A3 — Sin casos pendientes**  
La bandeja muestra estado vacío con indicación de registrar casos.

### Excepciones

| Código | Caso | Respuesta esperada |
|---|---|---|
| FEAT002-E01 | Case ID inexistente | Mensaje “caso no encontrado” |
| FEAT002-E02 | Comentario vacío | Validación en pantalla |
| FEAT002-E03 | Decisión inválida | Validación en pantalla |

### Postcondiciones

- El caso queda aprobado o rechazado.
- El evento de validación queda registrado.
- El dashboard refleja indicadores actualizados.
- La trazabilidad muestra FSD, diseño, ADR, prompt, código y tests.

### Eventos emitidos

| Evento | Cuándo se emite | Payload mínimo |
|---|---|---|
| CaseValidated.v1 | Al aprobar caso | case_id, supervisor_user, decision, comment |
| CaseRejected.v1 | Al rechazar caso | case_id, supervisor_user, decision, comment |
| DashboardKpiUpdated.v1 | Al recalcular KPIs | total_cases, validated_cases, financial_value |

## 5. Criterios de aceptación en formato Given/When/Then

### FEAT-001 — Registro visual

```gherkin
Given que el mercaderista está en la pantalla de registro
When completa tienda, producto, vencimiento, cantidad, precio actual, nuevo precio y acción comercial
And presiona “Registrar caso”
Then el sistema registra el caso
And calcula días al vencimiento
And calcula valor financiero en riesgo
And calcula descuento porcentual
And clasifica el riesgo
And muestra el caso en la bandeja de supervisión
```

### FEAT-002 — Validación supervisor

```gherkin
Given que existe un caso registrado pendiente
When el supervisor abre la bandeja y aprueba el caso con comentario
Then el sistema cambia el estado a APROBADO
And genera el evento CaseValidated.v1
And el dashboard incrementa validated_cases
And el caso mantiene trazabilidad documental y técnica
```

### Dashboard gerencial

```gherkin
Given que existen casos registrados y validados
When la gerencia abre el dashboard
Then ve total de casos, casos validados, valor financiero en riesgo, cantidad intervenida, cambios de precio y acciones por tipo
```

## 6. Reglas de trazabilidad

Cada feature debe quedar enlazada a:

- requerimiento de negocio;
- FSD;
- documento de diseño;
- ADR;
- prompt implementation;
- prompt mapping;
- código fuente;
- tests;
- evidencia de demo;
- tutorial docente.

## 7. Definition of Done funcional

- Las dos features se ven en una interfaz web.
- La demo permite recorrer el flujo completo sin editar código.
- Los errores se muestran en pantalla.
- Los eventos son visibles.
- La trazabilidad está documentada.
- Tests ≥90%.
- Existe tutorial para docente.
- Existe PowerPoint de defensa.
- estudiante responsable aprueba antes de empaquetar el ZIP final.


---

# Addendum — Interfaz visual y dashboard avanzado para evaluación

## Mejora de interfaz

La demo se presenta como una interfaz web orientada a docente y público evaluador. No contiene instrucciones personales para la estudiante responsable; el lenguaje explica el producto, el rol del mercaderista, el rol del supervisor y la lectura gerencial.

## FEAT-001 ampliada

La pantalla de mercaderista muestra el flujo desde cero:

1. Seleccionar tienda.
2. Visualizar contexto de región, zona, canal y cadena.
3. Registrar producto, lote, vencimiento, cantidad y precio.
4. Registrar acción comercial y evidencia.
5. Calcular riesgo y mostrar variables usadas en la clasificación.

## FEAT-002 ampliada

El dashboard gerencial incorpora:

- filtros por vista nacional/regional;
- región;
- canal;
- cadena;
- riesgo;
- acción comercial;
- gráficos de riesgo, región, acción y canal;
- ranking regional;
- insights ejecutivos.

## Trazabilidad mantenida

La interfaz mejorada sigue consumiendo los mismos endpoints y casos de uso: `/cases`, `/dashboard`, `/events` y `/traceability`. Por lo tanto, no duplica reglas de negocio en la interfaz.
