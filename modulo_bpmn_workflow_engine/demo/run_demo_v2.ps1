$ErrorActionPreference = "Stop"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " APP DETECCION PROD - DEMO OPERATIVA INTEGRAL V2" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

if (-not (Test-Path ".\src")) {
    Write-Host "ERROR: Ejecuta este script desde modulo_bpmn_workflow_engine" -ForegroundColor Red
    exit 1
}

Write-Host "[1/5] Python..." -ForegroundColor Yellow
python --version

Write-Host "[2/5] Runtime LangGraph persistente..." -ForegroundColor Yellow
python -c "from src.langgraph_orchestration.persistent_runtime import ejecutar_persistente, ejecutar_hasta_pausa, reanudar_persistente, obtener_checkpoint_persistido, obtener_historial_persistido, obtener_estado_ejecucion; print('RUNTIME OK')"

Write-Host "[3/5] Grafo y MCP..." -ForegroundColor Yellow
python -c "from src.langgraph_orchestration.graph import grafo_mcp; print('GRAFO OK:', sorted(grafo_mcp.get_graph().nodes.keys()))"

Write-Host "[4/5] Streamlit..." -ForegroundColor Yellow
python -c "import streamlit; print('STREAMLIT', streamlit.__version__)"

if (-not (Test-Path ".\data\salas_empresa_demo.csv")) {
    Write-Host "AVISO: Falta data\salas_empresa_demo.csv" -ForegroundColor Yellow
}
if (-not (Test-Path ".\data\productos_empresa_demo.csv")) {
    Write-Host "AVISO: Falta data\productos_empresa_demo.csv; se usara fallback embebido" -ForegroundColor Yellow
}

Write-Host "[5/5] Iniciando interfaz..." -ForegroundColor Green
streamlit run .\demo\app_operativa_v2.py
