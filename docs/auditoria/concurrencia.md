# Auditoría de concurrencia del backend — App Detección Prod

> **Módulo 8 · Actividad de auditoría (parte 2 de 2) · Entrega: domingo 18 de octubre de 2026, 23:59.**
> Este archivo es a la vez **las instrucciones para el asistente de IA** y **la ficha que se entrega**. El asistente lo rellena en su lugar; el grupo lo revisa, responde las preguntas y lo sube a su repositorio.

## Cómo se usa (para el grupo)

1. Copien este archivo a su repositorio como `docs/auditoria/concurrencia.md`.
2. Trabajen sobre el mismo commit que la parte 1 (`release/8.0.0`).
3. Abran su asistente con acceso al repositorio y escríbanle:
   > Sigue las instrucciones de la sección 0 de `docs/auditoria/concurrencia.md` y rellena ese archivo.
4. Respondan las preguntas que el asistente les haga al final de cada oleada. Aquí habrá más preguntas que en la parte 1, porque varios datos (cuántas réplicas corren, cuánto tarda la IA, cuánto tráfico esperan) no están en el código.
5. Revisen el resultado, confirmen la autoverificación (sección 6) y hagan los commits **cada integrante con su propia cuenta**.

**Si su asistente no tiene acceso al repositorio:** pídanle los comandos, córranlos ustedes y péguenle la salida.

**Cómo se califica la parte de preguntas:** cada pregunta debe terminar respondida o cerrada como `NO VERIFICABLE` con su motivo. **Si quedan más de 3 preguntas sin responder en este archivo, baja la nota de la actividad.** Si no tienen el dato exacto (por ejemplo, el tráfico esperado), una estimación razonada cuenta como respuesta.

---

## 0. Instrucciones para el asistente de IA (no editar esta sección)

**Rol.** Eres el asistente de auditoría de un grupo de maestría que desarrolla un backend. Vas a revisar cómo maneja la concurrencia su servicio y a **rellenar este mismo archivo**. No produces otros archivos.

**Conceptos que debes aplicar.**
- **Dónde espera una petición:** casi todo el tiempo de una API es espera (base de datos, red, servicio de IA). Saturar es que un recurso finito (hilos, conexiones del pool, el único hilo del event loop, el cupo de la API de IA) esté al 100 % y las peticiones nuevas hagan cola: primero sube la latencia y luego llegan los errores.
- **Modelos por runtime:** Node.js usa un event loop de un hilo (cualquier trabajo síncrono lo bloquea); Java 21+ con hilos virtuales permite código bloqueante que escala, pero el pool de la base de datos sigue siendo el límite; Python con `async def` bloquea el loop si llama a librerías síncronas, y las rutas `def` corren en un threadpool finito (40 hilos por defecto en AnyIO).
- **Ley de Little:** conexiones ocupadas en promedio = peticiones por segundo que usan la base de datos × tiempo medio que cada una retiene la conexión. Cada instancia tiene su propio pool: la base de datos recibe `instancias × tamaño del pool`.
- **Llamadas lentas (LLM):** necesitan timeout explícito, reintentos con backoff y jitter, límite de llamadas simultáneas y no retener una conexión de base de datos mientras se espera.

**Reglas que no puedes romper.**
1. **Solo lectura del producto.** No modificas código ni configuración; el único archivo que editas es este. No ejecutas pruebas de carga contra servicios compartidos o en producción.
2. **No inventas.** Cada estado distinto de `N/A` lleva evidencia comprobable: `ruta/archivo:línea` con el fragmento relevante, o el comando exacto y las primeras líneas de su salida. Las cifras que no salen del código (tráfico, latencias, réplicas) se preguntan, no se suponen.
3. **No copias secretos.** Rutas y líneas sí; valores de claves, nunca.
4. **Todas las comprobaciones aparecen**, una vez cada una (CON-01 a CON-05). No agregas ni quitas comprobaciones.
5. **Escribes en español** y en frases claras.

**Estados permitidos.** `OK`, `PARCIAL`, `FALLA`, `N/A` (con razón) y `NO VERIFICABLE` (con razón). Mientras trabajas puedes usar `PENDIENTE`, pero **al terminar no puede quedar ninguno**.

**Cómo preguntar sin bloquear.** Cuando te falte un dato que no está en el código:
- Marca la comprobación como `PENDIENTE`, agrega la pregunta a la sección 4 con un número (P1, P2…) y la comprobación a la que afecta, y **continúa con la siguiente**. Nunca te detengas a esperar.
- Al **terminar cada oleada**, muestra al grupo todas las preguntas nuevas juntas. Si tu herramienta permite preguntas con opciones, úsalas (por ejemplo, para el número de réplicas: 1, 2, 3 o más, no sabemos).
- Si el grupo responde, anota la respuesta y actualiza la comprobación. Si no responde, en la oleada 3 cierra la comprobación como `NO VERIFICABLE` y la pregunta como "sin respuesta".
- **Antes de preguntar, búscalo** en el README, `docker-compose`, Dockerfile, manifiestos de Kubernetes, archivos de configuración y scripts de arranque.

**Oleadas.** Trabaja en este orden y actualiza la sección 2 al terminar cada una:
- **Oleada 0 · Reconocimiento.** Rellena la sección 1: runtime y framework de cada servicio, punto de arranque, librería de acceso a datos y cliente HTTP o SDK de IA. Escribe en la sección 2 el plan (qué archivos y comandos usarás).
- **Oleada 1 · Evidencia automática.** Ejecuta los comandos de cada comprobación (adaptados a las carpetas reales) y anota la evidencia.
- **Oleada 2 · Juicio.** Decide el estado de CON-01 a CON-04 y pregunta lo que falte. Calcula con la ley de Little las conexiones necesarias cuando tengas los datos (tráfico estimado y tiempo de retención); si no los tienes, pregúntalos.
- **Oleada 3 · Cierre.** Integra las respuestas; escribe la **hipótesis de cuello de botella** (CON-05) con base en las comprobaciones anteriores; cierra lo pendiente como `NO VERIFICABLE`; escribe los hallazgos (sección 5), marca la autoverificación (sección 6) y rellena el resumen (sección 7). Termina diciendo cuántas preguntas quedaron sin respuesta.

**Si el proyecto tiene varios servicios**, evalúa cada uno y anota la evidencia por servicio; el estado es el del peor evaluado.

---

## 1. Datos del repositorio (oleada 0)

- **Grupo:** App Detección Prod.
- **Commit auditado (`release/8.0.0`):** `NO VERIFICABLE` (se recibió ZIP de `evals-offline-dia10`, sin `.git`; el equipo debe fijar y comunicar el hash).
- **Fecha de la auditoría:** 2026-10-15.
- **Servicios y runtime:** Python; servicio HTTP con Starlette (`src/api/contract_api.py`), demo UI con Streamlit (`app_demo.py`), servidor MCP con FastMCP (`src/agent_mcp/servidor_mcp.py`), motor con `ThreadPoolExecutor` y cliente Ollama HTTP. **Versiones de runtime, procesos y réplicas reales: no verificadas.**
- **Acceso a datos:** `sqlite3` en repositorio de workflow y BD local demo; `AsyncSqliteSaver` para LangGraph (checkpoints). **Base de datos:** SQLite en archivos locales.
- **Cliente HTTP o SDK de IA:** `urllib.request` en `src/llm/ollama_client.py` y `src/agent_mcp/ollama_client.py`; FastMCP como interfaz de tools.
- **Integrantes y qué revisó cada uno:** Gina Fabiana Villanueva Viscarra → CON-01 a CON-05 (revisión estática preparatoria); más integrantes no informados y autoría Git aún sin comprobar.
- **Alcance:** evidencia extraída de rama ZIP; no se ejecutaron pruebas de carga ni se inventaron mediciones, réplicas, tiempos de retención o tamaños de pool.


## 2. Plan y avance por oleadas

| Oleada | Qué se hizo | Estado |
|---|---|---|
| 0 · Reconocimiento | Se identificaron módulos Python, Starlette, FastMCP, Streamlit, SQLite, Ollama y dependencias. | REALIZADA (ZIP) |
| 1 · Evidencia | Se leyeron los archivos y números de línea relevantes; se registraron comandos para reproducir en checkout Git. | REALIZADA (estática) |
| 2 · Juicio | Se clasificaron seis factores, distinguiendo incumplimientos observables de verificaciones pendientes. | REALIZADA |
| 3 · Cierre | Se priorizaron hallazgos, cerraron preguntas sin respuesta como NO VERIFICABLE y se redactó la autoverificación. | REALIZADA CON LIMITACIONES |


## 3. Comprobaciones

### CON-01 · Modelo de concurrencia e instancias

**Evidencia:** [`modulo_bpmn_workflow_engine/src/orchestration/executor.py:63-78`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/orchestration/executor.py#L63) — Implementación de `ThreadedExecutor` con 4 workers por defecto; [`modulo_bpmn_workflow_engine/src/api/contract_api.py:22-28`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/api/contract_api.py#L22) — Servicio HTTP Starlette; [`modulo_bpmn_workflow_engine/src/agent_mcp/servidor_mcp.py:7-25`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/agent_mcp/servidor_mcp.py#L7) — Servidor MCP con FastMCP.

**Comando de auditoría (para repetir en checkout Git):** `git grep -nE "ThreadPoolExecutor|Starlette|FastMCP|workers|replicas:" -- modulo_bpmn_workflow_engine`. **Resultado local:** inspección estática de los archivos exportados en ZIP; no se ejecutó `git grep` ni se comprobó su salida en un checkout Git.

**Estado:** `PARCIAL`  
**Observación:** Se identifican modelos y componentes de ejecución, pero el número real de workers/instancias del servicio HTTP o de MCP no está acreditado. El 4 del ThreadedExecutor no debe confundirse con 4 réplicas de la API.  
**Auditó:** Gina Fabiana Villanueva Viscarra.


### CON-02 · Llamadas bloqueantes en el camino de una petición

**Evidencia:** [`modulo_bpmn_workflow_engine/src/api/contract_api.py:22-28`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/api/contract_api.py#L22) — Endpoint HTTP Starlette con delegación a runtime; [`modulo_bpmn_workflow_engine/src/llm/ollama_client.py:55-65`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/llm/ollama_client.py#L55) — `request.urlopen` es bloqueante y la llamada puede tardar hasta 300 s; [`modulo_bpmn_workflow_engine/src/tool_calling/database.py:15-25`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/tool_calling/database.py#L15) — sqlite3 sincrónico usado en el módulo de herramientas.

**Comando de auditoría (para repetir en checkout Git):** `git grep -nE "async def|urlopen|sqlite3.connect|requests\.|time.sleep" -- modulo_bpmn_workflow_engine/src`. **Resultado local:** inspección estática de los archivos exportados en ZIP; no se ejecutó `git grep` ni se comprobó su salida en un checkout Git.

**Estado:** `PARCIAL`  
**Observación:** Hay E/S sincrónica en clientes y base SQLite. Su ejecución dentro del hilo del event loop de una ruta concreta no está acreditada sin traza completa del call graph; debe revisarse especialmente cuando se invoquen desde `async def`.  
**Auditó:** Gina Fabiana Villanueva Viscarra.


### CON-03 · Pool de conexiones a la base de datos

**Evidencia:** [`modulo_bpmn_workflow_engine/src/tool_calling/database.py:15-27`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/tool_calling/database.py#L15) — `sqlite3.connect` establece conexión directa; no declara pool configurable; [`modulo_bpmn_workflow_engine/src/persistence/sqlite_repository.py:62-67`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/persistence/sqlite_repository.py#L62) — Repositorio crea conexión SQLite directa.

**Comando de auditoría (para repetir en checkout Git):** `git grep -nE "pool_size|max_overflow|pool_timeout|sqlite3.connect|AsyncSqliteSaver" -- modulo_bpmn_workflow_engine/src`. **Resultado local:** inspección estática de los archivos exportados en ZIP; no se ejecutó `git grep` ni se comprobó su salida en un checkout Git.

**Estado:** `NO VERIFICABLE`  
**Observación:** No hay pool de servidor SQL configurable en estos adaptadores SQLite. Tampoco se dispone de tasa de peticiones, retención media de conexión ni réplicas: por tanto NO se calculará un número inventado. La ley de Little queda expresada como `L = λ × W`, a completar con mediciones de S04; se debe definir además timeout de bloqueo de SQLite y manejo de saturación.  
**Auditó:** Gina Fabiana Villanueva Viscarra.


### CON-04 · Timeouts y reintentos en llamadas externas (incluida la IA)

**Evidencia:** [`modulo_bpmn_workflow_engine/src/llm/ollama_client.py:62-65`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/llm/ollama_client.py#L62) — Timeout explícito de 300 s en generación básica; [`modulo_bpmn_workflow_engine/src/agent_mcp/ollama_client.py:80-95`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/agent_mcp/ollama_client.py#L80) — Timeout de 120 s en cliente del agente; [`modulo_bpmn_workflow_engine/src/agent_mcp/agent.py:20-21`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/agent_mcp/agent.py#L20) — `MAX_PASOS = 6` limita pasos del agente, pero no demuestra límite concurrente.

**Comando de auditoría (para repetir en checkout Git):** `git grep -nE "timeout|retry|backoff|Semaphore|urlopen" -- modulo_bpmn_workflow_engine/src`. **Resultado local:** inspección estática de los archivos exportados en ZIP; no se ejecutó `git grep` ni se comprobó su salida en un checkout Git.

**Estado:** `PARCIAL`  
**Observación:** Hay timeouts de red explícitos en al menos dos clientes, pero no se demostró presupuesto extremo a extremo, reintentos con backoff y jitter, semáforo/bulkhead para peticiones LLM ni que no se retenga conexión durante esa espera.  
**Auditó:** Gina Fabiana Villanueva Viscarra.


### CON-05 · Hipótesis de cuello de botella

**Evidencia:** [`modulo_bpmn_workflow_engine/src/llm/ollama_client.py:62-65`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/llm/ollama_client.py#L62) — Espera potencial prolongada de llamada a Ollama; [`modulo_bpmn_workflow_engine/src/agent_mcp/agent.py:20-21`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/agent_mcp/agent.py#L20) — Límite de pasos por petición, no de concurrencia global; [`modulo_bpmn_workflow_engine/src/tool_calling/database.py:15-25`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/tool_calling/database.py#L15) — SQLite local con E/S sincrónica.

**Comando de auditoría (para repetir en checkout Git):** `git grep -nE "timeout=300|timeout=120|MAX_PASOS|sqlite3.connect" -- modulo_bpmn_workflow_engine/src`. **Resultado local:** inspección estática de los archivos exportados en ZIP; no se ejecutó `git grep` ni se comprobó su salida en un checkout Git.

**Estado:** `PARCIAL`  
**Observación:** Hipótesis técnicamente fundada, aún sin medición: bajo carga, probablemente se saturarán antes las llamadas concurrentes a Ollama en el flujo de consulta/agente MCP, porque su latencia puede ser elevada y no se acreditó bulkhead global (CON-04); alternativamente SQLite puede imponer bloqueos de escritura (CON-02/03). Se confirmará con k6 en S04.  
**Auditó:** Gina Fabiana Villanueva Viscarra.


## 4. Preguntas al grupo

| N.º | Comprobación | Pregunta | Respuesta del grupo | Estado (respondida / sin respuesta) |
|---|---|---|---|---|
| P1 | CON-01 | ¿Cuántos workers y réplicas se ejecutan en cada entorno (API, Streamlit, MCP)? | Se revisaron contract_api.py, package.json y el README del módulo. La API utiliza Starlette y un endpoint asíncrono; el README documenta ejecución local con Streamlit y MCP mediante stdio. No se encontró en estos archivos una configuración que confirme el número de workers o réplicas en ejecución. La cantidad real por entorno sigue pendiente de verificar. | sin respuesta |
| P2 | CON-03 | ¿Qué tráfico de consultas/seg se prevé y cuánto dura cada conexión SQLite? | Se identificó el uso de SQLite como almacenamiento local y operaciones de acceso a datos en el backend. Sin embargo, no se dispone de una estimación confirmada de consultas por segundo ni de mediciones sobre la duración de las conexiones SQLite. Estos valores deberán determinarse mediante pruebas de carga y medición de tiempos. Por tanto, la comprobación permanece pendiente de verificación. | sin respuesta |
| P3 | CON-04 | ¿Existe un límite concurrente global del LLM o un proxy/cola externo no documentado? | El agente dispone de MAX_PASOS = 6 y existen configuraciones de timeout para las llamadas al LLM. Sin embargo, estos controles no equivalen a un límite global de concurrencia. No se ha confirmado la existencia de un semáforo global, cola compartida o proxy externo que controle las solicitudes simultáneas hacia Ollama. La comprobación requiere revisar la configuración del entorno y realizar pruebas de concurrencia. | sin respuesta |

## 5. Hallazgos priorizados

| # | Comprobación | Severidad (alta / media / baja) | Qué falla | Corrección propuesta | Responsable |
|---|---|---|---|---|---|
| 1 | CON-04 | alta | No se acredita límite global a concurrencia LLM ni reintentos controlados. | Añadir bulkhead/semaphore configurable, presupuesto de timeout, backoff con jitter para errores transitorios e idempotentes. | Gina Fabiana Villanueva Viscarra |
| 2 | CON-02 | alta | Existen clientes HTTP/SQLite sincrónicos que podrían bloquear un endpoint asíncrono. | Trazar invocaciones `async`; usar cliente asíncrono o threadpool para E/S bloqueante, con pruebas de concurrencia. | Gina Fabiana Villanueva Viscarra |
| 3 | CON-03 | media | No hay datos de throughput, retención y bloqueo SQLite para dimensionar concurrencia. | Medir en S04, documentar `busy_timeout` y migración a BD compartida cuando se escale. | Gina Fabiana Villanueva Viscarra |
| 4 | CON-01 | media | Réplicas y workers del servidor desconocidos. | Registrar topología real y comandos de arranque; verificar scale-out sin estado. | Gina Fabiana Villanueva Viscarra |
| 5 | CON-05 | media | El primer cuello de botella aún es hipótesis, no una medida. | Validar con k6, p95/p99, errores, cola hacia Ollama y bloqueos SQLite. | Gina Fabiana Villanueva Viscarra |

## 6. Autoverificación (la marca el asistente; el grupo la confirma)

- [x] Las cinco comprobaciones CON-01 a CON-05 están documentadas una vez.
- [x] Ninguna quedó `PENDIENTE` ni sin estado.
- [x] Cada `PARCIAL` tiene referencias a archivos y líneas.
- [x] Cada `NO VERIFICABLE` explica lo que falta medir o confirmar.
- [x] No se inventaron tráfico, latencias, réplicas ni pool.
- [x] CON-05 incluye recurso, flujo y fundamento en CON-02/03/04; queda por validar con k6.
- [x] Las tres preguntas están cerradas como "sin respuesta" explicada.
- [x] No contiene secretos ni se modificó código del producto.
- [ ] **Pendiente de comprobar en Git:** identidad real de commits de todos los integrantes, `release/8.0.0` y hash, más ejecución de comandos en checkout real.


## 7. Resumen

| OK | PARCIAL | FALLA | N/A | NO VERIFICABLE | Preguntas sin respuesta |
|---:|---:|---:|---:|---:|---:|
| 0 | 4 | 0 | 0 | 1 | 3 |

**Hipótesis de cuello de botella (copia de CON-05):** Bajo carga se saturarán primero los cupos de ejecución hacia Ollama durante consultas del agente MCP, debido a esperas HTTP potencialmente largas y ausencia de límite concurrente global demostrado (CON-04), con riesgo secundario de contención SQLite (CON-02/CON-03). Es una hipótesis pendiente de medición en S04, no un resultado de carga.
