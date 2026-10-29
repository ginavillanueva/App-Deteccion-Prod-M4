# Laboratorio S08 — Auditoría y optimización de imagen Docker

## Datos

- **Integrante:** Gina Villanueva
- **Proyecto:** App-Deteccion-Prod-M4
- **Rama del laboratorio:** `lab-s08/villanueva`, creada desde `origin/main` (`6f95de3`)
- **Opción:** A — Auditar y adelgazar la imagen de un servicio
- **Servicio:** API FastAPI `app_deteccion` con SQLite
- **Fecha de ejecución:** 29 de octubre de 2026
- **Máquina:** Windows `amd64`; Docker Desktop utilizando contenedores `linux/amd64`
- **Docker Desktop:** 4.83.0
- **Docker Client / Engine:** 29.6.2
- **Auditoría:** Trivy 0.76.1; hadolint 2.15.1
- **Uso de IA:** Sí. ChatGPT ayudó a proponer Dockerfiles, comandos de medición, interpretar errores de arranque relacionados con SQLite y redactar el informe. Las cifras y comprobaciones proceden de comandos ejecutados localmente, y no de estimaciones de IA.

## Contexto y alcance

En las ramas examinadas del repositorio no se encontraron archivos Docker registrados. La rama `main` no contenía el servicio FastAPI buscado; se incorporó a la rama del laboratorio el directorio `src/app_deteccion`, `requirements.txt` y `pyproject.toml` desde `origin/release/8.2.0` para construir la imagen de referencia. Por tanto, la comparación **antes → después** corresponde a dos imágenes construidas durante este laboratorio y no a una imagen Docker anterior publicada en el proyecto.

## Mediciones verificadas

| Métrica | Antes: `app-deteccion:antes` | Después: `app-deteccion:despues` |
|---|---|---|
| Imagen base | `python:3.11` | `python:3.11-slim` |
| Tamaño de contenido (`docker image ls`) | 431 MB | 61,8 MB |
| Uso en disco mostrado por Docker | 1,69 GB | 258 MB |
| Capas (`.RootFS.Layers`) | 11 | 9 |
| Usuario efectivo | `root`, UID 0 | `appuser`, UID 999, GID 999 |
| CVE HIGH (Trivy) | 455 | 46 |
| CVE CRITICAL (Trivy) | 16 | 0 detectadas |
| Total HIGH + CRITICAL | 471 | 46 |
| Avisos de hadolint | 0 | 0 |
| ¿Arranca y responde? | Sí: HTTP 200 en `/docs` | Sí: HTTP 200 en `/health` |

**Resultado cuantitativo:** reducción aproximada de **85,7 %** del tamaño de contenido (431 → 61,8 MB); reducción de **2 capas** (11 → 9); reducción aproximada de **90,2 %** del total de vulnerabilidades HIGH + CRITICAL detectadas (471 → 46). Son mediciones de momentos concretos; los recuentos de CVE pueden variar con la base de datos de Trivy y las versiones de paquetes.

## Hallazgos, cambios y razones

1. **Imagen base pesada:** la imagen inicial utilizó `python:3.11`. Se sustituyó por `python:3.11-slim` para reducir el contenido y los paquetes de sistema incluidos.
2. **Dependencias de ejecución:** la imagen inicial instalaba `requirements.txt`, que también incluye utilidades de pruebas (`pytest`, `pytest-cov`, `httpx`). La optimizada instala las dependencias necesarias para ejecutar la API (`fastapi`, `uvicorn[standard]`, `pydantic`) según las restricciones de versión usadas en el Dockerfile.
3. **Privilegios excesivos:** la imagen inicial se ejecutaba como `root` (UID 0). En la versión optimizada se creó un usuario y grupo de aplicación; la instrucción final es `USER 999:999`.
4. **Aviso de hadolint:** durante una versión intermedia apareció `DL3066` (usuario por nombre). Se reemplazó `USER appuser` por `USER 999:999`; hadolint no mostró avisos en la comprobación definitiva.
5. **Error de SQLite tras quitar root:** la primera ejecución de la imagen optimizada falló con `sqlite3.OperationalError: unable to open database file`. Se comprobó en el código que la ruta es configurable mediante `APP_DB_PATH`. El Dockerfile definitivo crea `/app/data` y asigna permisos al UID/GID 999, y define `APP_DB_PATH=/app/data/app_deteccion_demo.db`. Tras reconstruir, `/health` respondió HTTP 200 con `status: ok`.

## Comandos utilizados

Comandos representativos ejecutados en PowerShell para generar y verificar las mediciones:

```powershell
docker version

docker build -t app-deteccion:antes .
docker image ls app-deteccion:antes
docker image inspect app-deteccion:antes --format '{{len .RootFS.Layers}}'
docker image inspect app-deteccion:antes --format '{{.Config.User}}'
docker run --rm --entrypoint id app-deteccion:antes

docker build -t app-deteccion:despues .
docker image ls app-deteccion
docker image inspect app-deteccion:despues --format '{{len .RootFS.Layers}}'
docker run --rm --entrypoint id app-deteccion:despues

Get-Content Dockerfile | docker run --rm -i hadolint/hadolint:v2.15.1 hadolint -
```

Trivy se ejecutó primero para `app-deteccion:antes` y después para `app-deteccion:despues`, con el mismo analizador y parámetros; para facilitar el recuento, el JSON fue agrupado por severidad:

```powershell
docker run --rm `
  -v /var/run/docker.sock:/var/run/docker.sock `
  -v trivy-cache:/root/.cache `
  aquasec/trivy:0.76.1 image `
  --scanners vuln `
  --severity HIGH,CRITICAL `
  --format json `
  app-deteccion:antes |
  ConvertFrom-Json |
  ForEach-Object { $_.Results } |
  ForEach-Object { $_.Vulnerabilities } |
  Where-Object { $_ } |
  Group-Object Severity |
  Select-Object Name, Count
```

Se repitió sustituyendo `app-deteccion:antes` por `app-deteccion:despues`.

Las comprobaciones funcionales fueron:

```powershell
docker run --rm -d --name app-deteccion-s08-antes -p 18080:8000 app-deteccion:antes
curl.exe -i http://localhost:18080/docs
docker stop app-deteccion-s08-antes

docker run --rm -d --name app-deteccion-s08-despues -p 18080:8000 app-deteccion:despues
curl.exe -i http://localhost:18080/health
```

También se ejecutaron comandos de Git para preparar la rama desde `origin/main`, examinar otras ramas y recuperar los archivos FastAPI relevantes desde `origin/release/8.2.0`.

## Qué no se pudo resolver / limitaciones

- Persisten **46 vulnerabilidades HIGH** detectadas por Trivy; no se afirma que la imagen esté libre de vulnerabilidades.
- La comprobación funcional demuestra que el servicio inicia y responde por HTTP; **no** sustituye pruebas integrales de escritura/lectura ni de todos los endpoints.
- El SQLite de la demostración reside dentro del contenedor: no se configuró un volumen externo para persistencia entre recreaciones del contenedor.
- Las dependencias se instalaron con rangos de versiones; no se fijaron todas las versiones exactas. Una reproducción posterior puede dar resultados diferentes.
- No se creó una imagen Docker previa histórica; la imagen “antes” se construyó expresamente para establecer una línea base válida en este laboratorio.

## Conclusión

La imagen optimizada redujo tamaño y vulnerabilidades detectadas, pasó a ejecutarse sin privilegios de `root` y siguió respondiendo HTTP 200. La corrección del directorio SQLite fue necesaria para mantener tanto seguridad de permisos como funcionamiento. Se documentaron mediciones reales, comandos y limitaciones; las vulnerabilidades restantes requieren revisión posterior.
