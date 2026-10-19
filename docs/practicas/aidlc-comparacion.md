# Comparación de desarrollo con y sin AWS AI-DLC

## Datos generales

- Proyecto: App Detección de Productos
- Repositorio: https://github.com/ginavillanueva/App-Deteccion-Prod-M4
- Versión A: `feature-sin-aidlc`
- Versión B: `feature-con-aidlc`
- Herramienta evaluada: AWS AI-DLC 2.11.0, flujo Express
- Backend: Python y Starlette

## Funcionalidad desarrollada

Se implementó el endpoint `POST /api/v1/vencimientos/clasificar`.
Recibe `fecha_vencimiento` y `fecha_consulta` en formato YYYY-MM-DD.
Calcula los días restantes hasta el vencimiento y clasifica el producto.
Un resultado negativo corresponde a VENCIDO.
Entre 0 y 30 días, inclusive, corresponde a PROXIMO_A_VENCER.
Más de 30 días corresponde a VIGENTE.
Las fechas inválidas y los datos faltantes producen HTTP 422.
Se conservaron los endpoints existentes y se agregaron siete pruebas.

## Versión A: sin AWS AI-DLC

- Rama: `feature-sin-aidlc`
- Desarrollo convencional del endpoint, lógica de negocio y pruebas.
- Duración registrada: 32 minutos y 55 segundos.
- Se implementaron cuatro archivos nuevos o modificados.
- Resultado: 7 pruebas nuevas aprobadas y 5 pruebas anteriores aprobadas.
- Total comprobado: 12 pruebas aprobadas.

## Versión B: con intento de AWS AI-DLC Express

- Rama: `feature-con-aidlc`
- Se instaló y verificó AWS AI-DLC 2.11.0.
- Se generaron archivos de configuración, agentes, skills, hooks y estructura `aidlc/`.
- Se intentó iniciar `/aidlc express` mediante GitHub Copilot CLI.
- La orquestación no logró avanzar porque los hooks no se ejecutaron correctamente.
- También se observaron errores intermitentes de conexión de Copilot.
- No se registró una intención activa ni se completaron las puertas de aprobación.
- Para concluir la validación funcional, se recuperó el código de la Versión A.
- Por tanto, NO se afirma que AI-DLC haya generado el código de la Versión B.
- Resultado funcional comprobado: 7 pruebas nuevas aprobadas.
- Pruebas API combinadas: 12 aprobadas en 0.094 segundos.
- Tiempo total de desarrollo con AI-DLC: no medido de forma comparable; hubo demoras de configuración y conexión.

## Etapas y aprobaciones

| Etapa | Estado |
|---|---|
| Configuración de AWS AI-DLC | Realizada |
| Inicio de Express | Intentado, bloqueado |
| Reverse Engineering | No completada |
| Requirements Analysis | No completada |
| Code Generation mediante AI-DLC | No completada |
| Build and Test mediante AI-DLC | No completada |
| Pruebas funcionales ejecutadas manualmente | 12/12 aprobadas |
| Aprobaciones manuales de puertas | No realizadas |

## Comparación

| Criterio | Versión A | Versión B |
|---|---|---|
| Metodología | Desarrollo convencional | AI-DLC instalado; Express bloqueado |
| Tiempo | 32 min 55 s | No comparable |
| Código funcional | Sí | Sí, recuperado de A |
| Pruebas API | 12/12 | 12/12 |
| Artefactos AI-DLC | No | Configuración y registros iniciales |
| Puertas de aprobación AI-DLC | No aplica | No completadas |
| Intervención humana | Implementación y verificación | Configuración, diagnóstico, recuperación y pruebas |

## Ventajas, desventajas y conclusiones

El desarrollo convencional permitió implementar y validar el endpoint sin
depender de la disponibilidad de herramientas externas.

AWS AI-DLC ofrece una estructura de agentes, hooks, etapas y registros que
puede favorecer la trazabilidad y las revisiones del desarrollo.

En esta práctica no fue posible comprobar experimentalmente esas ventajas
en un flujo Express completo, debido a problemas de integración y conexión.
Por eso no corresponde afirmar que la metodología redujo el tiempo
ni que sus puertas de aprobación se ejecutaron exitosamente.

La principal conclusión es que ambas ramas cuentan con la funcionalidad
validada, pero solo la Versión A representa una implementación completada
mediante el proceso previsto. La Versión B conserva evidencia verificable
de la instalación, los intentos de ejecución y el bloqueo de AI-DLC.

## Evidencias

- Rama A: https://github.com/ginavillanueva/App-Deteccion-Prod-M4/tree/feature-sin-aidlc
- Rama B: https://github.com/ginavillanueva/App-Deteccion-Prod-M4/tree/feature-con-aidlc
- Registro de pruebas B: `docs/practicas/aidlc-pruebas-version-b.txt`
- Configuración y registros iniciales: `modulo_bpmn_workflow_engine/aidlc/`
- Versión: `.aidlc-version`
