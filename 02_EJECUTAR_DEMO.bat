@echo off
chcp 65001 >nul
title App Deteccion Prod - Demo visual
cd /d "%~dp0"
echo ===============================================
echo APP DETECCION PROD - DEMO VISUAL LOCAL
echo ===============================================
echo.
echo Cuando vea Uvicorn running, abra en Chrome:
echo http://127.0.0.1:8000/app
echo.
echo No cierre esta ventana mientras use la demo.
echo.
.\.venv\Scripts\python.exe -m uvicorn app_deteccion.main:app --app-dir src --reload
pause
