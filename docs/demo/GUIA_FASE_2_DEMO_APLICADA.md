# Guía Fase 2 — Demo aplicada en interfaz web

## Propósito para el docente

Esta demo evidencia que el producto ya tiene dos funcionalidades aplicadas en una interfaz navegable:

1. **Registro visual de producto crítico** para el mercaderista.
2. **Supervisión + dashboard gerencial** para supervisor y gerencia.

## Flujo de defensa

### 1. Inicio

Mostrar `http://127.0.0.1:8000/app`.

Explicación:

> Esta vista resume el flujo completo: registrar, calcular riesgo, auditar precio, validar y medir KPIs.

### 2. Registro mercaderista

Completar o usar los datos por defecto:

```json
{
  "store": "Hipermaxi Sur",
  "product_name": "Yogurt Natural 1L",
  "batch": "L-2026-07",
  "quantity": 25,
  "current_price": 18.5,
  "new_price": 14.5,
  "commercial_action": "DESCUENTO",
  "price_change_approved": true
}
```

Qué demuestra:

- registro estructurado;
- control de precio actual y nuevo;
- acción comercial;
- evidencia;
- cálculo automático de riesgo;
- valor financiero en riesgo;
- descuento promedio;
- eventos de dominio.

### 3. Bandeja supervisor

Seleccionar el caso registrado y presionar **Validar caso seleccionado**.

Qué demuestra:

- el supervisor ya no busca datos dispersos;
- ve el detalle del caso;
- valida con usuario, decisión y comentario;
- el caso cambia de estado;
- se genera evento de validación.

### 4. Dashboard gerencial

Mostrar los KPIs actualizados.

Qué demuestra:

- total de casos;
- casos validados;
- casos por riesgo;
- valor financiero en riesgo;
- cantidad intervenida;
- cambios de precio;
- descuento promedio;
- acciones comerciales por tipo.

### 5. Eventos y trazabilidad

Mostrar eventos y endpoint de trazabilidad.

Qué demuestra:

- ProductCaseRegistered.v1;
- PriceChanged.v1;
- CaseRiskClassified.v1;
- CaseValidatedBySupervisor.v1;
- trazabilidad FSD → DD → ADR → Prompt → Código → Tests.

## Conclusión oral sugerida

> Con esta demo ya se evidencia una aplicación funcional y no solo una API. Las dos features conectan operación, supervisión y gerencia: el mercaderista registra, el sistema calcula, el supervisor valida y gerencia mide impacto mediante KPIs.
