# Ejecuta la demo aplicada con interfaz web.
# Abrir luego: http://127.0.0.1:8000/app
.\.venv\Scripts\python.exe -m uvicorn app_deteccion.main:app --app-dir src --reload
