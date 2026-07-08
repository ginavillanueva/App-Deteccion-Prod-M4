@echo off
chcp 65001 >nul
title App Deteccion Prod - Tests
cd /d "%~dp0"
echo ===============================================
echo APP DETECCION PROD - TESTS Y COBERTURA
echo ===============================================
echo.
.\.venv\Scripts\python.exe -m pytest --cov=src --cov-report=term-missing --cov-fail-under=90
echo.
pause
