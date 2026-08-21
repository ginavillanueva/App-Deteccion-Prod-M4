from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.langgraph_orchestration.graph import grafo_mcp
from src.langgraph_orchestration.persistent_runtime import (
    ejecutar_persistente,
    ejecutar_hasta_pausa,
    reanudar_persistente,
    obtener_checkpoint_persistido,
    obtener_historial_persistido,
    obtener_estado_ejecucion,
)

print("=== SMOKE TEST DEMO V2 ===")
print("ROOT:", ROOT)
print("GRAFO:", sorted(grafo_mcp.get_graph().nodes.keys()))
print("SALAS CSV:", (ROOT / "data" / "salas_empresa_demo.csv").exists())
print("PRODUCTOS CSV:", (ROOT / "data" / "productos_empresa_demo.csv").exists())
print("ANIMATED HTML:", (ROOT / "demo" / "animated_workflow.html").exists())
print("IMPORTS RUNTIME: OK")
print("SMOKE TEST: OK")
