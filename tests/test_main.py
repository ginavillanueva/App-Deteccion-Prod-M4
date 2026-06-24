
def test_main_exposes_fastapi_app():
    from app_deteccion.main import app

    assert app.title == "App Detección Prod — FSD-UC-001"
