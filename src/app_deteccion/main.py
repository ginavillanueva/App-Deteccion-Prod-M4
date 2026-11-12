from app_deteccion.adapters.api import create_app
from app_deteccion.observability import configure_observability

app = create_app()
configure_observability(app)
