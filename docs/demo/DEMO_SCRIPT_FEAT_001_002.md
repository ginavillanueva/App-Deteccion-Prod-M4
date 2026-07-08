# Guion preliminar de demo — Dos features aplicadas

**Estado:** PARA REVISIÓN  
**Uso:** base para el tutorial docente y defensa posterior.

## Objetivo

Demostrar que App Detección Prod permite registrar un producto crítico, auditar acción comercial y precio, validar por supervisor y reflejar el resultado en dashboard gerencial.

## Guion de demo

### Paso 1 — Abrir la app

Entrar a:

```text
http://127.0.0.1:8000/app
```

Explicación:

> Esta pantalla es el inicio de la demo aplicada. Permite navegar por las dos features: registro de mercaderista y supervisión/dashboard.

### Paso 2 — Registrar producto crítico

Entrar a:

```text
/app/register
```

Datos de ejemplo:

```json
{
  "store": "Hipermaxi Sur",
  "product_name": "Yogurt Natural 1L",
  "batch": "L-2026-07",
  "expiration_date": "2026-07-20",
  "quantity": 25,
  "current_price": 18.5,
  "new_price": 14.5,
  "commercial_action": "DESCUENTO",
  "price_change_approved": true,
  "price_change_reason": "Descuento autorizado por supervisor",
  "evidence_note": "Foto clara de gondola y etiqueta de precio",
  "created_by": "mercaderista.demo"
}
```

Explicación:

> Aquí se reemplaza el reporte disperso por WhatsApp por un formulario estructurado. El registro captura vencimiento, cantidad, acción comercial, precio actual, nuevo precio y evidencia.

### Paso 3 — Ver resultado del caso

Pantalla esperada:

- ID del caso.
- Riesgo MEDIO/ALTO/BAJO.
- Valor financiero en riesgo.
- Diferencia de precio.
- Descuento porcentual.
- Eventos generados.

Explicación:

> La app transforma el dato operativo en información calculada y trazable.

### Paso 4 — Abrir bandeja supervisor

Entrar a:

```text
/app/supervisor
```

Explicación:

> El supervisor ya no busca datos entre chats; ve los casos centralizados y priorizados por riesgo.

### Paso 5 — Validar caso

Acción:

- Seleccionar caso.
- Ingresar comentario.
- Aprobar o rechazar.

Explicación:

> La validación genera responsabilidad humana y evita que decisiones comerciales queden sin control.

### Paso 6 — Ver dashboard gerencial

Entrar a:

```text
/app/dashboard
```

KPIs esperados:

- total_cases = 1
- validated_cases = 1
- total_financial_value_at_risk = 462.5
- total_intervened_quantity = 25
- price_change_cases = 1
- average_discount_percent = 21.62

Explicación:

> Gerencia ve impacto financiero y avance de gestión sin esperar consolidaciones manuales.

### Paso 7 — Ver eventos y trazabilidad

Entrar a:

```text
/app/events
/app/traceability
```

Explicación:

> La demo evidencia que cada acción genera eventos y queda conectada con documentos, código y tests.

## Cierre de demo

> Estas dos features muestran el flujo completo del producto: operación en campo, control comercial, supervisión y visibilidad gerencial. La app convierte un proceso manual y fragmentado en una gestión trazable, medible y defendible.
