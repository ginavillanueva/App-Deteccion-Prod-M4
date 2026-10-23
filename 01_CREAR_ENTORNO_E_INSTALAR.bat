@echo off
chcp 65001 >nul
title App Deteccion Prod - Crear entorno
cd /d "%~dp0"
echo ===============================================
echo APP DETECCION PROD - PREPARAR DEMO LOCAL
echo ===============================================
echo.
echo Creando entorno virtual .venv ...
py -3 -m venv .venv 2>nul
if errorlevel 1 python -m venv .venv
if errorlevel 1 (
  echo ERROR: No se pudo crear el entorno. Verifique que Python este instalado.
  pause
  exit /b 1
)
echo.
echo Instalando dependencias ...
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  echo ERROR: No se pudieron instalar dependencias.
  pause
  exit /b 1
)
echo.
echo LISTO: Dependencias instaladas correctamente.
echo Ahora ejecute: 02_EJECUTAR_DEMO.bat
echo.
pause
