import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from app_deteccion.main import app

destino = ROOT / "openapi.json"
generado = json.dumps(
    app.openapi(),
    ensure_ascii=False,
    indent=2
) + "\n"

if "--check" in sys.argv:
    if not destino.exists():
        print("ERROR: falta openapi.json")
        sys.exit(1)

    if destino.read_text(encoding="utf-8") != generado:
        print("ERROR: OpenAPI desactualizado respecto al código.")
        sys.exit(1)

    print("OK: OpenAPI coincide con el código.")
else:
    destino.write_text(generado, encoding="utf-8")
    print("OK: openapi.json generado correctamente.")
