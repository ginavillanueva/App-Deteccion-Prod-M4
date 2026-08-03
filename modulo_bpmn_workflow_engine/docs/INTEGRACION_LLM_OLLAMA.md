# Integración con un LLM mediante Ollama

## 1. Objetivo

Este componente demuestra la invocación de un modelo de lenguaje desde el código de App Detección Prod, sin utilizar un chat web.

La integración cumple con los siguientes requisitos:

- Existe una función que recibe un prompt.
- La función invoca un modelo de lenguaje.
- El modelo devuelve una respuesta textual.
- La ejecución se realiza desde Python.
- El prompt utiliza datos relacionados con un producto próximo a vencer.
- No se almacena ninguna clave dentro del código ni del repositorio.

## 2. Tecnología utilizada

- Lenguaje: Python 3.12
- Motor local de modelos: Ollama
- Modelo: `deepseek-coder-v2:latest`
- API local: `http://localhost:11434/api/generate`

Ollama se ejecuta localmente, por lo que esta demostración no necesita una API key.

## 3. Archivos agregados

```text
modulo_bpmn_workflow_engine/
├── demo_llm.py
└── src/
    └── llm/
        ├── __init__.py
        └── ollama_client.py
```

### `src/llm/ollama_client.py`

Contiene la función:

```python
generate_response(prompt)
```

Esta función:

1. Recibe un prompt.
2. Construye una solicitud HTTP en formato JSON.
3. Invoca la API local de Ollama.
4. Recibe la respuesta del modelo.
5. Devuelve el texto generado.

### `demo_llm.py`

Contiene una ejecución demostrativa basada en un caso de App Detección Prod.

Los datos utilizados incluyen:

- producto;
- tienda;
- fecha de vencimiento;
- cantidad;
- precio actual;
- acción comercial;
- evidencia.

El programa calcula los días restantes para el vencimiento, construye el prompt y solicita al modelo:

1. Nivel de riesgo.
2. Justificación.
3. Acción comercial sugerida.
4. Prioridad de revisión.

## 4. Seguridad

El repositorio incluye un archivo `.gitignore` con las siguientes exclusiones:

```text
.venv/
.env
__pycache__/
*.py[cod]
```

Por esta razón:

- el entorno virtual no se sube a GitHub;
- cualquier archivo `.env` queda protegido;
- los archivos temporales de Python no se versionan;
- ninguna clave se incluye en el código.

Aunque esta implementación local no utiliza API key, la configuración permite utilizar variables de entorno:

```text
OLLAMA_API_URL
OLLAMA_MODEL
```

## 5. Requisitos para ejecutar

Ollama debe estar instalado y el modelo debe estar disponible localmente.

Verificar Ollama:

```powershell
ollama --version
```

Verificar modelos instalados:

```powershell
ollama list
```

## 6. Ejecución

Desde la raíz del repositorio:

```powershell
python .\modulo_bpmn_workflow_engine\demo_llm.py
```

## 7. Flujo de la integración

```text
Dato de App Detección Prod
            |
            v
Construcción del prompt en demo_llm.py
            |
            v
generate_response(prompt)
            |
            v
POST http://localhost:11434/api/generate
            |
            v
Modelo deepseek-coder-v2:latest
            |
            v
Respuesta mostrada en la terminal
```

## 8. Resultado obtenido

La ejecución mostró correctamente:

- el dato enviado desde la aplicación;
- el prompt construido en Python;
- la respuesta generada por el modelo;
- el nivel de riesgo;
- la justificación;
- la acción comercial sugerida;
- la prioridad de revisión.

La respuesta del modelo es una recomendación y no una decisión automática.

El modelo no está autorizado para:

- cambiar precios;
- aprobar descuentos;
- cerrar casos;
- ejecutar acciones comerciales.

La decisión final debe ser tomada por una persona.

## 9. Conclusión

La prueba demuestra que App Detección Prod puede invocar un modelo de lenguaje directamente desde su propio código.

Esto constituye el nivel inicial necesario para evolucionar posteriormente hacia:

- respuestas estructuradas;
- endpoints;
- tool calling;
- agentes;
- comparación entre modelos;
- integración con el workflow BPMN.