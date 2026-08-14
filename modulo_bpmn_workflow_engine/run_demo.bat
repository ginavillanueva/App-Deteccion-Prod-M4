@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo APP DETECCION PROD - AGENTE + MCP
echo ============================================================

if exist "..\.venv\Scripts\python.exe" (
    set PYTHON=..\.venv\Scripts\python.exe
) else if exist ".venv\Scripts\python.exe" (
    set PYTHON=.venv\Scripts\python.exe
) else (
    set PYTHON=python
)

echo Verificando Ollama...
ollama list >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Ollama no esta disponible.
    echo Inicia Ollama y vuelve a ejecutar este archivo.
    pause
    exit /b 1
)

echo Iniciando Streamlit...
%PYTHON% -m streamlit run app_demo.py

endlocal
