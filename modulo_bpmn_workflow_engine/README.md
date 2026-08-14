# App Detección Prod — BPMN Workflow Engine + Agente MCP

**Curso:** Fundamentos de Programación y Frameworks Modernos para IA  
**Proyecto:** App Detección Prod  
**Integrante:** Gina Fabiana Villanueva Viscarra  
**Stack:** Python · SQLite · Ollama · MCP · FastMCP · Streamlit · dataclasses · Enum · type hints · unittest  
**Estado:** ✅ Avance funcional integrado  
**Última actualización:** 2026-08-13  

---

## 1. Resumen ejecutivo

**App Detección Prod** es una solución orientada a gestionar y dar trazabilidad a productos detectados en sala, especialmente productos próximos a vencer, información de precios, evidencias y acciones comerciales.

El proyecto comenzó con la construcción de un **motor de workflow inspirado en BPMN 2.0**, encargado de representar y ejecutar procesos de negocio mediante tareas, transiciones, compuertas, instancias, workers, incidentes, reintentos, SLA, persistencia y trazabilidad.

Sobre esa base se incorporó posteriormente un nuevo módulo de **Agente + MCP (Model Context Protocol)**.

Esta nueva arquitectura permite que un agente basado en un LLM local:

- interprete la consulta realizada por el usuario;
- descubra las herramientas disponibles mediante MCP;
- seleccione las herramientas necesarias;
- ejecute una o varias herramientas;
- observe los resultados reales recuperados desde SQLite;
- aplique controles y guardrails;
- genere una respuesta final trazable;
- muestre todo el proceso mediante una interfaz Streamlit.

La aplicación dispone actualmente de una demo visual donde pueden observarse el agente ReAct, Ollama, el cliente MCP, el servidor MCP, las herramientas descubiertas, las llamadas `tools/call`, las observaciones, los guardrails y la respuesta final.

---

# 2. Módulo Agente + MCP

## 2.1 Objetivo

El objetivo de este avance es evolucionar **App Detección Prod** desde un sistema con Tool Calling local hacia una arquitectura desacoplada basada en:

```text
Agente
   ↓
Model Context Protocol
   ↓
Herramientas
   ↓
Fuente de datos
```

El agente no conoce directamente la implementación interna de las herramientas.

En cambio, utiliza un cliente MCP que se comunica mediante `stdio` con un servidor MCP.

El servidor publica las herramientas disponibles y permite que cualquier cliente compatible pueda descubrirlas e invocarlas.

---

## 2.2 Compromiso funcional del módulo

Las capacidades desarrolladas para el módulo Agente + MCP son:

### Productos próximos a vencer

El agente puede consultar productos detectados en sala junto con información como:

- producto;
- tienda o sala;
- fecha de vencimiento;
- días restantes;
- cantidad;
- precio actual;
- estado;
- evidencia registrada.

### Cambios de precio en sala

El agente puede consultar cambios de precio registrados y mostrar:

- producto;
- tienda;
- precio anterior;
- precio nuevo;
- variación;
- persona que registró el cambio;
- fecha del registro.

> **Importante:** esta funcionalidad es únicamente informativa y de trazabilidad.

El agente:

```text
NO aprueba precios
NO rechaza precios
NO modifica precios
NO autoriza cambios de precio
```

La herramienta únicamente informa sobre modificaciones que ya se encuentran registradas en el sistema.

### Acciones comerciales

El agente puede consultar acciones comerciales registradas sobre los productos, por ejemplo:

- descuentos;
- bandeos;
- promociones;
- retiros;
- otras acciones comerciales.

También puede recuperar su estado, responsable, fecha y evidencia.

---

# 3. Arquitectura Agente + MCP

La arquitectura implementada es:

```text
┌───────────────────────────────┐
│            USUARIO            │
└───────────────┬───────────────┘
                │
                │ consulta
                ▼
┌───────────────────────────────┐
│      INTERFAZ STREAMLIT       │
│          app_demo.py          │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│         AGENTE ReAct          │
│         MAX_PASOS = 6         │
│          Guardrails           │
└───────────────┬───────────────┘
                │
                │ messages + tools
                ▼
┌───────────────────────────────┐
│            OLLAMA             │
│       Tool Calling local      │
└───────────────┬───────────────┘
                │
                │ tool_calls
                ▼
┌───────────────────────────────┐
│         CLIENTE MCP           │
│       initialize              │
│       tools/list              │
│       tools/call              │
└───────────────┬───────────────┘
                │
                │ stdio / JSON-RPC
                ▼
┌───────────────────────────────┐
│         SERVIDOR MCP          │
│           FastMCP             │
│          @mcp.tool()          │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│     HERRAMIENTAS PYTHON       │
│                               │
│ vencimientos                  │
│ detalle de producto           │
│ cambios de precio             │
│ acciones comerciales          │
└───────────────┬───────────────┘
                │
                │ SQL
                ▼
┌───────────────────────────────┐
│            SQLITE             │
│      Fuente de datos demo     │
└───────────────────────────────┘
```

---

# 4. Comunicación MCP

La comunicación MCP se realiza mediante **entrada/salida estándar (`stdio`)**.

No se utiliza un puerto HTTP entre el cliente MCP y el servidor MCP.

El cliente inicia el servidor como un proceso hijo.

El flujo inicial es:

```text
Cliente MCP
    ↓
lanza servidor_mcp.py
    ↓
initialize
    ↓
sesión MCP creada
    ↓
tools/list
    ↓
servidor devuelve herramientas + schemas
```

Cuando el agente necesita ejecutar una herramienta:

```text
Agente
   ↓
selecciona tool + arguments
   ↓
Cliente MCP
   ↓
tools/call
   ↓
Servidor MCP
   ↓
Python
   ↓
SQLite
   ↓
resultado
   ↓
Observación MCP
   ↓
Agente
```

---

# 5. Herramientas publicadas mediante MCP

El servidor MCP publica actualmente cuatro herramientas.

## 5.1 `buscar_productos_proximos_a_vencer`

Consulta productos cuya fecha de vencimiento se encuentra dentro del rango solicitado.

Ejemplo de información recuperada:

```text
Producto
Tienda
Fecha de vencimiento
Días restantes
Cantidad
Precio actual
Estado
Evidencia
```

Ejemplo de consulta:

```text
¿Qué productos están próximos a vencer?
```

---

## 5.2 `consultar_detalle_producto`

Consulta toda la información registrada para un producto específico.

Ejemplo:

```text
Consulta el detalle del producto Yogur natural 1 litro.
```

Puede devolver:

```text
Producto: Yogur natural 1 litro
Tienda: Supermercado Central - Sala 12
Fecha de vencimiento: 2026-08-28
Días restantes: 15
Cantidad: 24 unidades
Precio actual: Bs. 18.5
Estado: PENDIENTE
Evidencia: Fotografía del producto y fecha de vencimiento registrada
```

---

## 5.3 `consultar_cambios_precio`

Consulta cambios de precio ya registrados para un producto.

Ejemplo:

```text
Precio anterior: Bs. 18.5
Precio nuevo: Bs. 15.5
Variación de precio: Bs. -3.0
Registrado por: Vendedor sala 12
Fecha del registro: 2026-08-05
```

Esta herramienta es:

```text
READ ONLY
INFORMATIVA
DE TRAZABILIDAD
```

No aprueba ni modifica precios.

---

## 5.4 `consultar_acciones_comerciales`

Consulta acciones comerciales asociadas a un producto.

Ejemplo:

```text
Acción comercial: DESCUENTO
Estado: PENDIENTE
Responsable: Vendedor sala 12
Fecha de acción: 2026-08-05
Evidencia: Fotografía del producto y fecha de vencimiento registrada
```

---

# 6. Agente ReAct

El nuevo agente implementa un comportamiento tipo ReAct:

```text
Pensar
   ↓
Actuar
   ↓
Observar
   ↓
Pensar nuevamente
   ↓
Responder
```

El agente puede realizar una o varias llamadas a herramientas antes de responder.

Ejemplo multipaso:

```text
Usuario:
"Revisa el Yogur natural 1 litro de la Sala 12.
Dime vencimiento, cantidad, precio, cambios de precio
y acción comercial."

                ↓

Agente

                ↓

consultar_detalle_producto

                ↓

Observación

                ↓

consultar_cambios_precio

                ↓

Observación

                ↓

consultar_acciones_comerciales

                ↓

Observación

                ↓

Respuesta final
```

---

# 7. MAX_PASOS

El agente dispone de un límite:

```python
MAX_PASOS = 6
```

Este límite funciona como mecanismo de seguridad.

Evita que un agente confundido pueda entrar en un bucle indefinido ejecutando herramientas repetidamente.

---

# 8. Guardrails

El agente no entrega automáticamente cualquier texto generado por el LLM.

La respuesta es validada contra las observaciones obtenidas desde MCP.

Se implementaron diferentes controles.

## 8.1 Guardrail de cobertura

Comprueba que el agente haya consultado las herramientas necesarias para responder lo solicitado.

Ejemplo:

```text
Usuario solicita:

detalle
+
cambio de precio
+
acción comercial
```

Si el modelo intenta responder utilizando solamente:

```text
consultar_detalle_producto
```

el sistema detecta que faltan herramientas.

La traza registra:

```text
coverage_guardrail
```

---

## 8.2 Guardrail de fidelidad

Comprueba que el modelo no cambie datos recuperados desde SQLite.

Ejemplo:

SQLite devuelve:

```text
estado = PENDIENTE
```

Si el modelo escribe:

```text
Pendiente
```

o intenta interpretar ese estado, el guardrail puede detectar la modificación.

---

## 8.3 Control de herramientas duplicadas

Si el modelo intenta volver a ejecutar una misma herramienta con los mismos argumentos, el sistema puede reutilizar la observación anterior.

La traza registra:

```text
duplicate_tool_guardrail
```

---

## 8.4 Fallback seguro

Si la respuesta del LLM continúa violando las validaciones, Python puede generar una respuesta directamente desde las observaciones MCP.

La traza registra:

```text
guardrail_fallback
```

Así se evita entregar una respuesta inventada o incompleta.

---

# 9. Trazabilidad Agente + MCP

La ejecución genera una traza completa.

Ejemplo:

```json
[
  {
    "step": 0,
    "type": "mcp_discovery",
    "transport": "stdio",
    "operation": "initialize -> tools/list"
  },
  {
    "step": 1,
    "type": "action",
    "tool": "consultar_detalle_producto",
    "via": "MCP",
    "operation": "tools/call"
  },
  {
    "step": 1,
    "type": "observation",
    "tool": "consultar_detalle_producto",
    "via": "MCP",
    "transport": "stdio"
  },
  {
    "step": 2,
    "type": "final"
  }
]
```

Esta traza permite demostrar:

```text
qué pidió el usuario
qué decidió el agente
qué herramienta seleccionó
qué argumentos utilizó
cómo se ejecutó por MCP
qué datos devolvió SQLite
qué guardrails se activaron
qué respuesta final se entregó
```

---

# 10. Demo visual con Streamlit

Se desarrolló una interfaz visual para facilitar la demostración del proyecto.

Archivo:

```text
app_demo.py
```

La interfaz permite mostrar:

```text
Estado de Ollama
Estado de MCP
Cantidad de tools descubiertas
Estado de SQLite
Arquitectura
Consulta del usuario
Respuesta final
Cantidad de pasos
Tools utilizadas
Proceso ReAct
tools/list
tools/call
Observaciones
Guardrails
Traza JSON
Arquitectura técnica
```

---

# 11. Ejecutar la demo

Desde:

```text
modulo_bpmn_workflow_engine
```

ejecutar:

```powershell
python -m streamlit run app_demo.py
```

Streamlit mostrará una dirección similar a:

```text
Local URL: http://localhost:8501
```

Abrir en el navegador:

```text
http://localhost:8501
```

También se incluye:

```text
run_demo.bat
```

para simplificar el inicio de la demostración en Windows.

---

# 12. Ejemplo de demostración multipaso

Consulta recomendada para la defensa:

```text
Revisa el producto Yogur natural 1 litro de la Sala 12.
Dime cuántos días faltan para vencer, qué cantidad tiene
y cuál es su precio actual.

Además, dime si tuvo cambios de precio registrados y qué
acción comercial tiene registrada, incluyendo su estado
y evidencia.
```

Resultado esperado de la demostración:

```text
Producto: Yogur natural 1 litro
Tienda: Supermercado Central - Sala 12
Fecha de vencimiento: 2026-08-28
Días restantes: 15
Cantidad: 24 unidades
Precio actual: Bs. 18.5
Estado: PENDIENTE
Evidencia: Fotografía del producto y fecha de vencimiento registrada

Cambio de precio registrado:
Precio anterior: Bs. 18.5
Precio nuevo: Bs. 15.5
Variación de precio: Bs. -3.0
Registrado por: Vendedor sala 12
Fecha del registro: 2026-08-05

Acción comercial: DESCUENTO
Estado: PENDIENTE
Responsable: Vendedor sala 12
Fecha de acción: 2026-08-05
Evidencia: Fotografía del producto y fecha de vencimiento registrada
```

---

# 13. Archivos principales del módulo Agente + MCP

```text
modulo_bpmn_workflow_engine/
│
├── app_demo.py
├── requirements.txt
├── .env.example
├── .gitignore
├── run_demo.bat
│
├── src/
│   └── agent_mcp/
│       ├── __init__.py
│       ├── agent.py
│       ├── agente_mcp.py
│       ├── cliente_mcp.py
│       ├── ollama_client.py
│       ├── servidor_mcp.py
│       └── tools.py
│
└── docs/
    ├── Avance_Entregable_Agente_MCP_App_Deteccion_Prod.docx
    └── evidencias/
```

---

# 14. Evidencias

Las capturas de la implementación se encuentran en:

```text
docs/evidencias/
```

Actualmente incluyen:

```text
01_tool_calling_herramientas.png
02_sqlite_schema.png
03_sqlite_registros.png
04_mcp_instalado_fastmcp.png
05_agente_mcp_codigo.png
06_streamlit_inicio.png
07_streamlit_traza_mcp.png
08_streamlit_tools_descubiertas.png
09_streamlit_resultado_tabs.png
README_EVIDENCIAS.txt
```

Estas evidencias permiten demostrar desde la evolución inicial de Tool Calling hasta la interfaz final con Agente + MCP.

---

# 15. Documento académico del avance

Se incluye el documento:

```text
docs/Avance_Entregable_Agente_MCP_App_Deteccion_Prod.docx
```

El documento reúne:

```text
objetivo
compromiso del módulo
arquitectura
implementación
Tool Calling
SQLite
Ollama
Agente ReAct
MCP
FastMCP
cliente MCP
servidor MCP
tools/list
tools/call
guardrails
demo Streamlit
pruebas
capturas
estado del avance
```

GitHub puede no mostrar una previsualización del archivo `.docx` debido a su tamaño.

En ese caso puede descargarse directamente desde el repositorio.

---

# 16. Estado del módulo Agente + MCP

| Componente | Estado |
|---|---|
| Python | ✅ |
| SQLite | ✅ |
| Ollama local | ✅ |
| Tool Calling | ✅ |
| Agente ReAct | ✅ |
| MAX_PASOS | ✅ |
| Ejecución multipaso | ✅ |
| Servidor MCP | ✅ |
| FastMCP | ✅ |
| Cliente MCP | ✅ |
| Transporte `stdio` | ✅ |
| JSON-RPC | ✅ |
| `initialize` | ✅ |
| `tools/list` | ✅ |
| `tools/call` | ✅ |
| Descubrimiento dinámico de tools | ✅ |
| Guardrail de cobertura | ✅ |
| Guardrail de fidelidad | ✅ |
| Control de tools duplicadas | ✅ |
| Fallback seguro | ✅ |
| Traza auditable | ✅ |
| Streamlit | ✅ |
| Evidencias | ✅ |
| Documento de avance | ✅ |
| GitHub | ✅ |

---

# 17. Motor BPMN desarrollado previamente

Además del módulo Agente + MCP, el repositorio contiene el motor de workflow inspirado en BPMN 2.0 desarrollado previamente para App Detección Prod.

Su propósito académico es demostrar cómo un proceso de negocio puede representarse como un grafo dirigido con:

```text
tareas
transiciones
compuertas
recursos
workers
instancias
trazas
incidentes
reintentos
SLA
multi-asignación
concurrencia
persistencia
```

La implementación no pretende reemplazar motores BPMN industriales como Camunda o Activiti.

---

# 18. Problema de negocio aplicado

En App Detección Prod, el problema central es la falta de una plataforma estructurada para controlar productos próximos a vencer y registrar las acciones realizadas en sala.

El proceso puede depender de:

```text
reportes informales
fotografías dispersas
WhatsApp
Excel
validaciones manuales
información no centralizada
```

Esto puede producir:

```text
falta de trazabilidad
pérdida de visibilidad
dificultad para validar información
acciones comerciales no medibles
cambios de precio con baja trazabilidad
riesgo de merma
decisiones tardías
```

El motor de workflow estructura este proceso mediante tareas, estados, compuertas, workers, incidentes y trazas.

El módulo Agente + MCP agrega posteriormente una capa de consulta inteligente desacoplada.

---

# 19. Workflow BPMN principal

El workflow desarrollado previamente contempla:

```text
DetectProductCase
        ↓
ValidateEvidence
        ↓
ClassifyRisk
        ↓
ValidatePriceData
        ↓
DecideCommercialAction
        ↓
ApprovePriceChange
        ↓
ExecuteRetailAction
        ↓
SupervisorReview
        ↓
CloseCaseAndUpdateDashboard
```

## Aclaración sobre `ApprovePriceChange`

`ApprovePriceChange` pertenece al **workflow BPMN desarrollado en una etapa anterior del proyecto**.

Esto no debe confundirse con el nuevo módulo Agente + MCP.

En el módulo Agente + MCP:

```text
consultar_cambios_precio
```

es una herramienta exclusivamente:

```text
informativa
de lectura
de trazabilidad
```

El agente MCP **no ejecuta `ApprovePriceChange` y no aprueba precios**.

---

# 20. Variantes BPMN soportadas

```text
Flujo lineal:
A → B → C → D


Split paralelo:
A → {B, C}


Join AND:
{B, C} → D cuando ambas tareas están completadas


Join OR:
{B, C} → D cuando al menos una rama habilita el avance


Rework:
SupervisorReview → ValidateEvidence


Incidente:
ExecuteRetailAction → ValidateEvidence


Error por reintentos agotados:
WorkflowInstance.status = ERROR


Múltiples finales:
CloseCaseSuccessfully
CloseCaseWithRejectedAction
CloseCaseWithExpiredProduct
CloseCaseWithErrorAfterRetries
```

---

# 21. Componentes principales del motor BPMN

## 21.1 Dominio

Ubicación:

```text
src/domain/
```

Incluye entidades como:

```text
Workflow
Task
LogicGate
Transition
ResourceSpec
Worker
Incident
```

Además de enums relacionados con estados, tareas, compuertas, roles, recursos y políticas de completado.

---

## 21.2 Runtime

Ubicación:

```text
src/runtime/
```

Incluye:

```text
WorkflowInstance
TaskInstance
ResourceInstance
TraceEntry
```

El runtime administra:

```text
navegación
estados
trazas
incidentes
resets
reintentos
finalización
```

---

## 21.3 Orquestación

Ubicación:

```text
src/orchestration/
```

Incluye:

```text
cola de tareas listas
Observer
asignación de workers
executor
concurrencia
orquestación
```

---

## 21.4 Persistencia

Ubicación:

```text
src/persistence/
```

Se utiliza SQLite para persistir información como:

```text
definiciones de workflow
instancias
task instances
trazas
incidentes
workers
```

La documentación correspondiente se encuentra en:

```text
docs/README_PERSISTENCE.md
docs/FSD.md
```

---

# 22. Relación con la consigna BPMN

| Requisito | Implementación |
|---|---|
| Motor de workflow inspirado en BPMN 2.0 | `src/domain/`, `src/runtime/`, `src/orchestration/` |
| Python con dataclasses, Enum y type hints | Modelo de dominio y runtime |
| Modelo de objetos en inglés | `Workflow`, `Task`, `LogicGate`, etc. |
| Documentación en español | `docs/` y README |
| Separación definición / instancia | `Workflow` / `WorkflowInstance` |
| Compuertas | `LogicGate` |
| Flujo lineal | Tests |
| Paralelismo | Tests + orquestación |
| AND / OR | Tests |
| Ciclos / rework | Runtime + tests |
| Incidentes | Runtime |
| Reset | Runtime |
| Reintentos | Runtime |
| SLA | Runtime |
| Multi-asignación | CompletionPolicy |
| Concurrencia | Executor |
| Persistencia | SQLite |
| Observer + cola | Orquestación |
| Trazabilidad | Documentación + runtime |

---

# 23. Estructura general del repositorio

```text
modulo_bpmn_workflow_engine/
│
├── README.md
├── app_demo.py
├── requirements.txt
├── run_demo.bat
├── .env.example
│
├── 00_CONTROL_APROBACIONES.md
├── 00_PLAN_EJECUCION_APROBADO.md
│
├── data/
│
├── demo/
│   ├── animated_workflow.html
│   └── README_ANIMATED_WORKFLOW.md
│
├── docs/
│   ├── PRD.md
│   ├── FSD.md
│   ├── APORTES.md
│   ├── INTEGRACION_LLM_OLLAMA.md
│   ├── Avance_Entregable_Agente_MCP_App_Deteccion_Prod.docx
│   │
│   └── evidencias/
│
├── PR_implementation/
│
├── src/
│   ├── agent_mcp/
│   ├── domain/
│   ├── llm/
│   ├── orchestration/
│   ├── persistence/
│   ├── runtime/
│   └── tool_calling/
│
└── tests/
```

---

# 24. Instalación

## 24.1 Requisitos generales

Se recomienda:

```text
Python 3.12
Git
Ollama
```

Crear o activar un entorno virtual.

En Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 24.2 Instalar dependencias

Desde:

```text
modulo_bpmn_workflow_engine
```

ejecutar:

```powershell
python -m pip install -r requirements.txt
```

---

# 25. Configuración de Ollama

El módulo utiliza un LLM local mediante Ollama.

La configuración utilizada durante la demostración fue:

```text
OLLAMA_MODEL=llama3.2:3b-instruct-q4_K_M
OLLAMA_API_URL=http://localhost:11434/api/chat
IA_HABILITADA=true
```

Existe una plantilla de variables de entorno en:

```text
.env.example
```

El archivo real:

```text
.env
```

no debe publicarse en GitHub.

---

# 26. Verificar Ollama

Ejecutar:

```powershell
ollama list
```

Debe aparecer el modelo configurado.

Ejemplo:

```text
llama3.2:3b-instruct-q4_K_M
```

---

# 27. Ejecutar pruebas del motor BPMN

Validar sintaxis:

```powershell
python -m compileall src
```

Ejecutar pruebas:

```powershell
python -m unittest discover -s tests
```

---

# 28. Probar descubrimiento MCP

El cliente MCP puede utilizarse para demostrar:

```text
initialize
   ↓
tools/list
```

Ejemplo:

```powershell
python -m src.agent_mcp.cliente_mcp --list
```

La salida debe mostrar las herramientas publicadas por el servidor MCP.

---

# 29. Ejecutar interfaz Streamlit

Desde:

```text
modulo_bpmn_workflow_engine
```

ejecutar:

```powershell
python -m streamlit run app_demo.py
```

o utilizar:

```text
run_demo.bat
```

---

# 30. Qué mostrar en una defensa

Una demostración recomendada sigue este orden:

```text
1. GitHub
      ↓
2. README
      ↓
3. src/agent_mcp/
      ↓
4. servidor_mcp.py
      ↓
5. cliente_mcp.py
      ↓
6. app_demo.py
      ↓
7. Ejecutar Streamlit
      ↓
8. Mostrar estado de arquitectura
      ↓
9. Ejecutar consulta multipaso
      ↓
10. Mostrar respuesta
      ↓
11. Mostrar Proceso visual
      ↓
12. Mostrar Tools MCP
      ↓
13. Mostrar Observaciones
      ↓
14. Mostrar Traza JSON
      ↓
15. Mostrar docs/evidencias
      ↓
16. Mostrar documento Word
```

---

# 31. Explicación breve para defensa

> App Detección Prod comenzó con un motor de workflow inspirado en BPMN 2.0 que estructura el proceso de negocio mediante tareas, transiciones, estados, compuertas, persistencia y trazabilidad.
>
> Sobre ese desarrollo se incorporó un módulo de Agente + MCP. El agente utiliza Ollama como LLM local y un comportamiento ReAct multipaso. Las herramientas ya no se ejecutan directamente desde el agente, sino que son publicadas por un servidor MCP y descubiertas dinámicamente mediante `initialize` y `tools/list`.
>
> Cuando el agente necesita información genera una llamada de herramienta. El cliente MCP la convierte en `tools/call`, el servidor ejecuta la herramienta autorizada, consulta SQLite y devuelve la observación.
>
> Python mantiene el control de la ejecución y aplica guardrails para impedir que la respuesta final cambie u omita datos importantes.
>
> Los cambios de precio en el módulo MCP son exclusivamente informativos y de trazabilidad. El agente no aprueba, rechaza ni modifica precios.
>
> Finalmente, Streamlit permite visualizar todo el proceso desde una interfaz: estado de la arquitectura, herramientas descubiertas, tools utilizadas, observaciones, guardrails y traza completa.

---

# 32. Decisiones técnicas defendibles

| Decisión | Justificación |
|---|---|
| Python | Permite integrar dominio, runtime, MCP, SQLite y demo en un mismo stack |
| SQLite | Fuente ligera y auditable para la demostración |
| Ollama | Permite utilizar un LLM local |
| MCP | Separa al agente de la implementación de las herramientas |
| `stdio` | Transporte simple y adecuado para servidor MCP local |
| FastMCP | Facilita publicación estructurada de herramientas |
| ReAct | Permite ciclos de decisión, acción y observación |
| `MAX_PASOS` | Evita ejecuciones infinitas |
| Guardrails | Protegen fidelidad y cobertura de las respuestas |
| Streamlit | Proporciona una demo visual y fácil de probar |
| `unittest` | Permite validar el motor sin depender de frameworks externos |

---

# 33. Diferencia entre Tool Calling y MCP

La evolución del proyecto puede resumirse de la siguiente manera.

## Tool Calling inicial

```text
Usuario
   ↓
Router / agente
   ↓
Ollama
   ↓
Tool Python local
   ↓
SQLite
```

Las herramientas se encontraban conectadas directamente al mismo código.

## Agente + MCP

```text
Usuario
   ↓
Agente
   ↓
Ollama
   ↓
Cliente MCP
   ↓
tools/list / tools/call
   ↓
Servidor MCP
   ↓
Tools
   ↓
SQLite
```

MCP desacopla el cliente de las herramientas.

El agente puede descubrir capacidades mediante un protocolo estándar.

---

# 34. Seguridad y separación de responsabilidades

La arquitectura separa responsabilidades:

```text
OLLAMA
Decide qué herramienta necesita.


AGENTE
Controla el ciclo ReAct.


CLIENTE MCP
Descubre e invoca herramientas.


SERVIDOR MCP
Publica herramientas autorizadas.


TOOLS
Implementan consultas de dominio.


SQLITE
Contiene los datos.


PYTHON / GUARDRAILS
Valida cobertura y fidelidad.


STREAMLIT
Presenta la demostración.
```

---

# 35. Datos de la demostración

La base SQLite utilizada para la demo contiene registros de prueba asociados a:

```text
productos_vencimiento
cambios_precio
acciones_comerciales
```

Estos registros permiten ejecutar la demostración de forma reproducible.

No representan necesariamente información productiva real.

---

# 36. Evidencia de ejecución MCP

Durante las pruebas se confirmó una traza similar a:

```text
STATUS: OK

mcp_discovery
transport: stdio
operation: initialize -> tools/list

action
tool: consultar_detalle_producto
via: MCP
operation: tools/call

observation
via: MCP
transport: stdio

action
tool: consultar_cambios_precio
via: MCP
operation: tools/call

observation

action
tool: consultar_acciones_comerciales
via: MCP
operation: tools/call

observation

guardrail

final
```

Esto demuestra una ejecución completa:

```text
Agente
→ MCP
→ Tool
→ SQLite
→ Observación
→ Guardrail
→ Respuesta final
```

---

# 37. Documentación adicional

El repositorio contiene documentación técnica adicional en:

```text
docs/
```

Entre otros:

```text
PRD.md
FSD.md
APORTES.md
INTEGRACION_LLM_OLLAMA.md
README_DOMAIN_MODEL.md
README_RUNTIME_ENGINE.md
README_ORCHESTRATION.md
README_PERSISTENCE.md
README_TESTS.md
```

También existen artefactos relacionados con entregas anteriores y trazabilidad del proyecto.

---

# 38. Repositorio y rama de trabajo

Repositorio:

```text
App-Deteccion-Prod-M4
```

Rama utilizada para este avance:

```text
modulo-bpmn-workflow-engine
```

Dentro de esta rama se encuentra integrado el módulo Agente + MCP y la demo Streamlit.

---

# 39. Estado actual del proyecto

El avance actual permite demostrar de manera funcional:

```text
BPMN Workflow Engine
        +
Tool Calling
        +
Ollama local
        +
Agente ReAct
        +
MCP
        +
FastMCP
        +
Cliente MCP
        +
Servidor MCP
        +
SQLite
        +
Guardrails
        +
Streamlit
        +
Trazabilidad
        +
Documentación
        +
Evidencias
```

---

# 40. Resultado

El proyecto demuestra la evolución de **App Detección Prod** desde un motor de workflow orientado a procesos hacia una arquitectura con capacidades de IA desacopladas mediante MCP.

La solución permite que el agente consulte información real de la demostración, seleccione herramientas de manera dinámica, ejecute múltiples acciones y mantenga trazabilidad completa de cada paso.

La interfaz Streamlit facilita la revisión técnica y académica mostrando visualmente:

```text
Usuario
→ Agente
→ Ollama
→ MCP
→ Tools
→ SQLite
→ Observaciones
→ Guardrails
→ Respuesta final
```

El módulo de precios mantiene explícitamente su objetivo de **consulta, notificación y trazabilidad**, sin delegar al agente ninguna aprobación o modificación de precios.

---

## Autora

**Gina Fabiana Villanueva Viscarra**

**Proyecto:** App Detección Prod  
**Módulo:** Agente + MCP  
**Rama:** `modulo-bpmn-workflow-engine`  
**Última actualización:** 13 de agosto de 2026