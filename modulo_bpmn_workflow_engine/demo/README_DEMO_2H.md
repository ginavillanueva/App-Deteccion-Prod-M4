# Demo Operativa Integral V2 — plan de 2 horas

## Objetivo

Tener una demo reproducible que muestre **uso de negocio + ejecucion real + persistencia + pausa/reanudacion + MCP + seguridad + trazabilidad + evidencia multimodal**.

## Copiar al repositorio

Desde esta carpeta:

- `app_operativa_v2.py` -> `modulo_bpmn_workflow_engine/demo/app_operativa_v2.py`
- `run_demo_v2.ps1` -> `modulo_bpmn_workflow_engine/demo/run_demo_v2.ps1`
- `smoke_test_demo_v2.py` -> `modulo_bpmn_workflow_engine/demo/smoke_test_demo_v2.py`
- `salas_empresa_demo.csv` -> `modulo_bpmn_workflow_engine/data/salas_empresa_demo.csv`
- `productos_empresa_demo.csv` -> `modulo_bpmn_workflow_engine/data/productos_empresa_demo.csv`

## Prueba previa

Desde `modulo_bpmn_workflow_engine`:

```powershell
python .\demo\smoke_test_demo_v2.py
```

Debe terminar con:

```text
IMPORTS RUNTIME: OK
SMOKE TEST: OK
```

## Arranque

```powershell
.\demo\run_demo_v2.ps1
```

Si PowerShell bloquea scripts:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\demo\run_demo_v2.ps1
```

## Modo recomendado para la defensa

Mantener `Fuente de consulta MCP = DEMO VALIDADO`.

La seleccion empresarial (departamento/cadena/sala/producto) queda trazada como contexto real. El backend usa el registro tecnico ya probado (`Yogur natural 1 litro`, `Sala 12`) para garantizar datos reproducibles.

Existe tambien `CONTEXTO EMPRESARIAL`, que consulta directamente el producto y sala seleccionados; usarlo solo si previamente se sembraron esos registros en las tablas operativas.

## Flujo de 5 minutos

1. Seleccionar sala empresarial.
2. VENCIMIENTO -> EJECUTAR.
3. Mostrar tool/fuente/nodos.
4. Nuevo thread -> AUDITORIA_COMPLETA -> PAUSAR.
5. Mostrar `PAUSADO` y `NEXT`.
6. REANUDAR -> mostrar 3 tools -> FINALIZADO.
7. Nuevo thread -> SEGURIDAD -> EJECUTAR.
8. Mostrar `PROMPT_INJECTION`, `TOOLS=[]`.
9. Abrir Trazabilidad.
10. Abrir Grafo.

## Multimodal

- Foto: captura/subida real, guardada por thread con hash SHA-256.
- Audio: subida real, guardada por thread con hash SHA-256.
- Texto/transcripcion/lectura visual: confirmacion humana para no simular capacidades que no esten instaladas.

Reconocimiento automatico de voz o imagen puede agregarse solo si hay un modelo local disponible; no es requisito para que la demo principal funcione.
