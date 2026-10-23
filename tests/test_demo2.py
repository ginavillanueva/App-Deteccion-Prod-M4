import pytest
from fastapi.testclient import TestClient
from app_deteccion.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["openapi"].startswith("3.")


def test_listar_casos():
    response = client.get("/cases")
    assert response.status_code == 200
    assert isinstance(response.json()["cases"], list)


def test_dashboard():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_eventos():
    response = client.get("/events")
    assert response.status_code == 200
    assert "events" in response.json()


def test_trazabilidad():
    response = client.get("/traceability")
    assert response.status_code == 200


def test_endpoint_registro_documentado():
    rutas = app.openapi()["paths"]
    assert "post" in rutas["/cases"]


def test_endpoint_validacion_documentado():
    rutas = app.openapi()["paths"]
    assert "patch" in rutas["/cases/{case_id}/validate"]
