# Auditoría 12-factor — App Detección Prod

> **Módulo 8 · Actividad de auditoría (parte 1 de 2) · Entrega: domingo 18 de octubre de 2026, 23:59.**
> Este archivo es a la vez **las instrucciones para el asistente de IA** y **la ficha que se entrega**. El asistente lo rellena en su lugar; el grupo lo revisa, responde las preguntas y lo sube a su repositorio.

## Cómo se usa (para el grupo)

1. Copien este archivo a su repositorio como `docs/auditoria/12factor.md`.
2. Creen la etiqueta o rama `release/8.0.0` sobre su rama principal actual (es el estado de partida del módulo) y trabajen sobre ese commit.
3. Abran su asistente con acceso al repositorio (Claude Code, Codex, Cursor u otro) y escríbanle:
   > Sigue las instrucciones de la sección 0 de `docs/auditoria/12factor.md` y rellena ese archivo.
4. Respondan las preguntas que el asistente les haga al final de cada oleada. Pueden contestar en el chat o escribiendo la respuesta directamente en la sección 4.
5. Revisen el resultado, corran ustedes la autoverificación (sección 6) y hagan los commits **cada integrante con su propia cuenta**.

**Si su asistente no tiene acceso al repositorio** (un chat sin herramientas): pídanle que les indique qué comandos correr, córranlos ustedes y péguenle la salida. El resto del proceso es igual.

**Cómo se califica la parte de preguntas:** cada pregunta debe terminar respondida o cerrada como `NO VERIFICABLE` con su motivo. **Si quedan más de 3 preguntas sin responder en este archivo, baja la nota de la actividad.** No saber un dato no es un error; dejar sin respuesta lo que el grupo sí podría averiguar, sí.

---

## 0. Instrucciones para el asistente de IA (no editar esta sección)

**Rol.** Eres el asistente de auditoría de un grupo de maestría que desarrolla un backend. Vas a revisar su repositorio contra seis prácticas 12-factor y a **rellenar este mismo archivo**. No produces otros archivos.

**Reglas que no puedes romper.**
1. **Solo lectura del producto.** No modificas código, configuración ni dependencias del repositorio. El único archivo que editas es este.
2. **No inventas.** Cada estado distinto de `N/A` lleva evidencia comprobable: `ruta/archivo:línea` con el fragmento relevante, o el comando exacto que ejecutaste y las primeras líneas de su salida. Si no puedes comprobar algo, no lo supones: lo preguntas o lo marcas `NO VERIFICABLE` con su motivo.
3. **No copias secretos.** Si encuentras una contraseña, token o clave, reportas la ruta y la línea, **nunca el valor**. No abras ni muestres archivos `.env` ni de claves en el chat.
4. **Todas las comprobaciones aparecen**, una vez cada una (F12-01 a F12-06), aunque el resultado sea negativo. No agregas ni quitas comprobaciones.
5. **Escribes en español** y en frases claras.

**Estados permitidos.** `OK`, `PARCIAL`, `FALLA`, `N/A` (no aplica, con razón) y `NO VERIFICABLE` (no se pudo comprobar, con razón). Mientras trabajas puedes usar `PENDIENTE`, pero **al terminar no puede quedar ninguno**.

**Cómo preguntar sin bloquear.** Cuando te falte un dato que no está en el código (por ejemplo, cómo se despliega en producción):
- Marca la comprobación como `PENDIENTE`, agrega la pregunta a la sección 4 con un número (P1, P2…) y la comprobación a la que afecta, y **continúa con la siguiente**. Nunca te detengas a esperar.
- Al **terminar cada oleada**, muestra al grupo todas las preguntas nuevas juntas, cada una con su número. Si tu herramienta permite preguntas con opciones, úsalas; si no, escríbelas en el chat.
- Si el grupo responde, anota la respuesta en la sección 4 y actualiza la comprobación. Si no responde o no lo sabe, en la oleada 3 cierra la comprobación como `NO VERIFICABLE` y la pregunta como "sin respuesta".
- Pregunta solo lo necesario: **antes de preguntar, búscalo en el repositorio** (README, `docker-compose`, Dockerfile, manifiestos, configuración, scripts).

**Oleadas.** Trabaja en este orden y actualiza la sección 2 al terminar cada una:
- **Oleada 0 · Reconocimiento.** Rellena la sección 1 (commit, stack, carpetas de código, cómo se ejecuta) y escribe en la sección 2 un plan breve: qué carpetas revisarás y qué comandos usarás para cada comprobación. No preguntes nada todavía, salvo que no encuentres el código fuente.
- **Oleada 1 · Evidencia automática.** Ejecuta los comandos de cada comprobación (adáptalos a las carpetas reales del proyecto) y anota la evidencia. No decidas estados aún.
- **Oleada 2 · Juicio.** Con la evidencia, decide el estado de cada comprobación y escribe la observación. Lo que no se pueda decidir sin un dato externo, pregúntalo como se indica arriba. Al terminar, muestra las preguntas.
- **Oleada 3 · Cierre.** Integra las respuestas recibidas; cierra lo que quede sin respuesta como `NO VERIFICABLE`; escribe los hallazgos priorizados (sección 5); marca la autoverificación (sección 6) y rellena el resumen (sección 7). Termina diciendo al grupo cuántas preguntas quedaron sin respuesta.

**Si el proyecto tiene varios servicios** (por ejemplo, un backend en NestJS y otro en Python), evalúa cada comprobación sobre todos y anota la evidencia de cada uno; el estado es el del servicio peor evaluado.

---

## 1. Datos del repositorio (oleada 0)

- **Grupo:** App Detección Prod.
- **Repositorio:** https://github.com/ginavillanueva/App-Deteccion-Prod-M4
- **Commit base auditado (`release/8.0.0`):** [`500cfdabc77ea925552264bf695a56409d534a0d`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/commit/500cfdabc77ea925552264bf695a56409d534a0d). Identificador confirmado mediante la página del commit en GitHub. Las evidencias de código de esta ficha se obtuvieron del ZIP de `evals-offline-dia10`; se recomienda cotejarlas contra este commit antes de confirmar la auditoría definitiva.
- **Referencia documental analizada:** rama `evals-offline-dia10`; revisión de código exportado, no afirmación de equivalencia con `release/8.0.0`.
- **Fecha de la auditoría:** 2026-10-15.
- **Stack detectado:** Python, Starlette (endpoint HTTP), Streamlit (demo), FastMCP, LangGraph, Ollama local y SQLite; `ThreadPoolExecutor` en el workflow. Dependencias declaradas en `modulo_bpmn_workflow_engine/requirements.txt`.
- **Carpetas de código fuente:** `modulo_bpmn_workflow_engine/src/{api,agent_mcp,tool_calling,llm,langgraph_orchestration,orchestration,persistence,runtime,domain}/`; también `modulo_bpmn_workflow_engine/demo/`.
- **Cómo se ejecuta (verificado):** **NO VERIFICABLE en este entorno**. El ZIP incluye `modulo_bpmn_workflow_engine/app_demo.py` (Streamlit) y `src/api/contract_api.py` (Starlette); no se inició servidor ni se probó Ollama.
- **Integrantes y qué revisó cada uno:** Gina Fabiana Villanueva Viscarra → F12-01 a F12-06 (análisis preparatorio). Otros integrantes: no informados; **la autoría individual de commits se debe verificar en Git**.
- **Alcance y límites:** análisis de archivos del ZIP recibido; sin historial `.git`, estado de despliegue, ejecución de contenedores o escaneo efectivo de credenciales. No se expone ningún secreto.


## 2. Plan y avance por oleadas

| Oleada | Qué se hizo | Estado |
|---|---|---|
| 0 · Reconocimiento | Se identificaron módulos Python, Starlette, FastMCP, Streamlit, SQLite, Ollama y dependencias. | REALIZADA (ZIP) |
| 1 · Evidencia | Se leyeron los archivos y números de línea relevantes; se registraron comandos para reproducir en checkout Git. | REALIZADA (estática) |
| 2 · Juicio | Se clasificaron seis factores, distinguiendo incumplimientos observables de verificaciones pendientes. | REALIZADA |
| 3 · Cierre | Se priorizaron hallazgos, cerraron preguntas sin respuesta como NO VERIFICABLE y se redactó la autoverificación. | REALIZADA CON LIMITACIONES |


## 3. Comprobaciones

### F12-01 · Configuración fuera del código (factor III)

**Evidencia:** [`modulo_bpmn_workflow_engine/src/tool_calling/config.py:54-69`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/tool_calling/config.py#L54) — Lee variables `OLLAMA_MODEL` y `OLLAMA_API_URL`, pero mantiene URL localhost como valor predeterminado; [`modulo_bpmn_workflow_engine/src/llm/ollama_client.py:10-18`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/llm/ollama_client.py#L10) — URL Ollama configurable por entorno con fallback local.

**Comando de auditoría (para repetir en checkout Git):** `git grep -nE "localhost|127\.0\.0\.1|os\.getenv" -- modulo_bpmn_workflow_engine/src`. **Resultado local:** inspección estática de los archivos exportados en ZIP; no se ejecutó `git grep` ni se comprobó su salida en un checkout Git.

**Estado:** `PARCIAL`  
**Observación:** Existe externalización parcial de parámetros; no se observa validación fail-fast de URL obligatoria y el fallback local podría enmascarar una configuración faltante. No se concluye que el valor local de desarrollo sea por sí mismo un secreto.  
**Auditó:** Gina Fabiana Villanueva Viscarra.


### F12-02 · Secretos fuera del repositorio y de su historial (factor III)

**Evidencia:** [`modulo_bpmn_workflow_engine/.gitignore:10-16`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/.gitignore#L10) — Excluye `.env`, secretos Streamlit y bases locales; [`.gitignore:1-7`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/.gitignore#L1) — La raíz excluye `.env` y bases SQLite de demo.

**Comando de auditoría (para repetir en checkout Git):** `git ls-files | grep -E "(^|/)\.env$"; git log --all --oneline -- .env; gitleaks detect --source . --redact`. **Resultado local:** inspección estática de los archivos exportados en ZIP; no se ejecutó `git grep` ni se comprobó su salida en un checkout Git.

**Estado:** `NO VERIFICABLE`  
**Observación:** La presencia de reglas de exclusión no demuestra que el historial esté libre de credenciales. Sin `.git` ni escáner ejecutado no se puede afirmar OK; escanear historial de release/8.0.0 sin copiar valores al informe.  
**Auditó:** Gina Fabiana Villanueva Viscarra.


### F12-03 · Procesos sin estado (factor VI)

**Evidencia:** [`modulo_bpmn_workflow_engine/src/tool_calling/database.py:10-25`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/tool_calling/database.py#L10) — La base de demostración se crea en ruta de disco local y se conecta mediante sqlite3; [`modulo_bpmn_workflow_engine/src/persistence/langgraph_checkpointer.py:55-61`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/persistence/langgraph_checkpointer.py#L55) — El checkpoint de LangGraph usa archivo SQLite local.

**Comando de auditoría (para repetir en checkout Git):** `git grep -nE "sqlite3.connect|langgraph_checkpoints|DATABASE_PATH|writeFile" -- modulo_bpmn_workflow_engine/src`. **Resultado local:** inspección estática de los archivos exportados en ZIP; no se ejecutó `git grep` ni se comprobó su salida en un checkout Git.

**Estado:** `FALLA`  
**Observación:** Para múltiples réplicas, persistir datos/checkpoints importantes en el filesystem del proceso no ofrece estado compartido. Debe migrarse a almacenamiento compartido o demostrarse que este servicio es solo demo de instancia única.  
**Auditó:** Gina Fabiana Villanueva Viscarra.


### F12-04 · Logs a la salida estándar (factor XI)

**Evidencia:** [`modulo_bpmn_workflow_engine/src/agent_mcp/cliente_mcp.py:146-154`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/agent_mcp/cliente_mcp.py#L146) — El cliente de demo imprime eventos a consola; no acredita logging JSON estructurado.

**Comando de auditoría (para repetir en checkout Git):** `git grep -nE "FileHandler|RotatingFileHandler|logging\.basicConfig|print\(" -- modulo_bpmn_workflow_engine/src`. **Resultado local:** inspección estática de los archivos exportados en ZIP; no se ejecutó `git grep` ni se comprobó su salida en un checkout Git.

**Estado:** `PARCIAL`  
**Observación:** Hay salida estándar en scripts de demo; falta política uniforme de logs estructurados y comprobación de captura del servicio HTTP y del MCP. La ausencia de `FileHandler` en los archivos revisados no acredita cobertura total.  
**Auditó:** Gina Fabiana Villanueva Viscarra.


### F12-05 · Servicios de apoyo intercambiables (factor IV)

**Evidencia:** [`modulo_bpmn_workflow_engine/src/tool_calling/config.py:62-69`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/tool_calling/config.py#L62) — Endpoint Ollama configurable vía variable; [`modulo_bpmn_workflow_engine/src/tool_calling/database.py:10-23`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/tool_calling/database.py#L10) — SQLite ligado a ruta concreta dentro de data/; [`modulo_bpmn_workflow_engine/src/persistence/langgraph_checkpointer.py:55-61`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/src/persistence/langgraph_checkpointer.py#L55) — Checkpointer conectado a SQLite local.

**Comando de auditoría (para repetir en checkout Git):** `git grep -nE "OLLAMA_API_URL|sqlite3.connect|DATABASE_PATH|CHECKPOINT_DB" -- modulo_bpmn_workflow_engine/src`. **Resultado local:** inspección estática de los archivos exportados en ZIP; no se ejecutó `git grep` ni se comprobó su salida en un checkout Git.

**Estado:** `PARCIAL`  
**Observación:** Ollama admite reemplazo de URL; el almacenamiento no se intercambia solamente por una URL sin cambiar adaptadores o código. Distinguir la abstracción del repositorio BPMN de la configuración efectiva de cada backing service.  
**Auditó:** Gina Fabiana Villanueva Viscarra.


### F12-06 · Construcción inmutable y apagado limpio (factores V y IX)

**Evidencia:** [`modulo_bpmn_workflow_engine/requirements.txt:1-8`](https://github.com/ginavillanueva/App-Deteccion-Prod-M4/blob/evals-offline-dia10/modulo_bpmn_workflow_engine/requirements.txt#L1) — Versiones fijadas para dependencias Python, pero no equivalen a imagen construida.

**Comando de auditoría (para repetir en checkout Git):** `git ls-files | grep -iE "dockerfile|compose"; git grep -nE "SIGTERM|lifespan|shutdown" -- modulo_bpmn_workflow_engine`. **Resultado local:** inspección estática de los archivos exportados en ZIP; no se ejecutó `git grep` ni se comprobó su salida en un checkout Git.

**Estado:** `NO VERIFICABLE`  
**Observación:** No se acreditó una imagen construida una sola vez, promoción entre entornos, ni una prueba real de SIGTERM. El ZIP no permite probar el comportamiento ante `docker stop`; se requiere artefacto de build y demostración de cierre.  
**Auditó:** Gina Fabiana Villanueva Viscarra.


## 4. Preguntas al grupo

| N.º | Comprobación | Pregunta | Respuesta del grupo | Estado (respondida / sin respuesta) |
|---|---|---|---|---|
| P1 | F12-02 | ¿Se ejecutó escaneo de secretos sobre `release/8.0.0` y su historial Git? | No consta en los ZIP; debe confirmarlo el equipo en su entorno Git/despliegue. | sin respuesta |
| P2 | F12-06 | ¿Existe Dockerfile/CI con imagen inmutable y prueba de SIGTERM para este backend? | No consta en los ZIP; debe confirmarlo el equipo en su entorno Git/despliegue. | sin respuesta |
| P3 | F12-03 | ¿El prototipo corre solo en una instancia o existe almacenamiento compartido en despliegue? | No consta en los ZIP; debe confirmarlo el equipo en su entorno Git/despliegue. | sin respuesta |

## 5. Hallazgos priorizados

| # | Comprobación | Severidad (alta / media / baja) | Qué falla | Corrección propuesta | Responsable | ¿Antes de contenedorizar (S07)? |
|---|---|---|---|---|---|---|
| 1 | F12-03 | alta | Checkpoints y base SQLite en disco local (no compartible en réplicas). | Diseñar almacenamiento persistente compartido o documentar instancia única de demo; probar reinicio y dos instancias. | Gina Fabiana Villanueva Viscarra | Sí |
| 2 | F12-02 | alta | Historial y escaneo de secretos no verificables desde ZIP. | Ejecutar escáner sobre repositorio Git completo; rotar cualquier secreto encontrado, sin publicarlo. | Gina Fabiana Villanueva Viscarra | Sí |
| 3 | F12-06 | alta | Build inmutable y apagado SIGTERM no acreditados. | Documentar Dockerfile exec-form, pipeline de imagen y prueba de apagado limpio. | Gina Fabiana Villanueva Viscarra | Sí |
| 4 | F12-01 | media | URL predeterminada local y falta evidencia de validación fail-fast. | Validar variables al iniciar y separar defaults seguros de configuración requerida. | Gina Fabiana Villanueva Viscarra | Sí |
| 5 | F12-05 | media | Backing services de datos no intercambiables por entorno. | Introducir URL/config externa y adaptadores compatibles con backend compartido. | Gina Fabiana Villanueva Viscarra | Sí |
| 6 | F12-04 | media | Logs de consola dispersos; no se comprueba esquema estructurado. | Definir logger JSON en stdout con request_id y sin datos sensibles. | Gina Fabiana Villanueva Viscarra | No (recomendable antes) |

## 6. Autoverificación (la marca el asistente; el grupo la confirma)

- [x] Las seis comprobaciones F12-01 a F12-06 aparecen exactamente una vez.
- [x] No hay `PENDIENTE`; todos los estados son permitidos.
- [x] Cada `PARCIAL`/`FALLA` tiene evidencia documental con archivo y línea.
- [x] `NO VERIFICABLE` incluye motivo y el método concreto para confirmarlo.
- [x] Las tres preguntas están cerradas como "sin respuesta" con razón explícita (no se inventaron respuestas).
- [x] Hallazgos de severidad alta tienen responsable propuesto.
- [x] No se incluyeron valores de secretos.
- [x] No se modificó código del producto: los cambios generados son solo estos informes fuera del repositorio.
- [ ] **Pendiente de comprobar por el grupo:** `git diff --stat <hash>..HEAD` al fijar release/8.0.0 y autoría individual real de commits.


## 7. Resumen

| OK | PARCIAL | FALLA | N/A | NO VERIFICABLE | Preguntas sin respuesta |
|---:|---:|---:|---:|---:|---:|
| 0 | 3 | 1 | 0 | 2 | 3 |

**Conclusión en dos líneas:** El backend evidencia separación de componentes y parte de la configuración externalizada, pero persisten dependencias de estado en SQLite local y prácticas de despliegue no verificadas. Antes de contenedorizar, asegurar persistencia compartida, escaneo real de secretos y apagado limpio, fijando primero el hash de `release/8.0.0`.
