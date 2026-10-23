# Tutorial para el docente — Demo aplicada de dos features

## Propósito
Este tutorial permite entender y reproducir la demo aplicada de App Detección Prod. La demo implementa dos features trazables:

- **FEAT-001:** Registro visual de producto crítico con acción comercial y cambio de precio.
- **FEAT-002:** Bandeja de supervisión + dashboard gerencial actualizado.

## Problema que resuelve
El proceso actual se apoya en WhatsApp, fotos dispersas y Excel, lo que genera falta de trazabilidad, ausencia de métricas, control débil de precios y baja visibilidad gerencial.

## Cómo ejecutar

```powershell
.\.venv\Scripts\python.exe -m uvicorn app_deteccion.main:app --app-dir src --reload
```

Luego abrir:

```text
http://127.0.0.1:8000/app
```

## Secuencia de demo

1. Entrar a **Inicio** y reiniciar la demo.
2. Ir a **Registro mercaderista**.
3. Registrar producto crítico.
4. Revisar cálculo de riesgo, valor financiero, descuento y cambio de precio.
5. Ir a **Bandeja supervisor**.
6. Seleccionar caso y validarlo.
7. Ir a **Dashboard gerencial** y verificar KPIs.
8. Ir a **Eventos y trazabilidad** y explicar la cadena documental.
9. Ejecutar tests con cobertura mínima de 90%.

## Comando de pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

Resultado esperado:

```text
50 tests passed
Cobertura total: 100.00%
```

## Lectura pedagógica
La demo no reemplaza toda la plataforma final. Es un **vertical slice funcional** que conecta operación de campo, validación táctica y visibilidad gerencial.
