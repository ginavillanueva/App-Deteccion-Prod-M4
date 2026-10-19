
import unittest

from starlette.testclient import TestClient

from src.api.contract_api import app


class TestVencimientosAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def consultar(self, vencimiento, consulta):
        return self.client.post(
            "/api/v1/vencimientos/clasificar",
            json={
                "fecha_vencimiento": vencimiento,
                "fecha_consulta": consulta,
            },
        )

    def test_producto_vencido(self):
        response = self.consultar("2026-10-10", "2026-10-19")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["estado"], "VENCIDO")
        self.assertEqual(response.json()["dias_restantes"], -9)

    def test_producto_proximo_a_vencer(self):
        response = self.consultar("2026-11-10", "2026-10-19")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["estado"], "PROXIMO_A_VENCER")
        self.assertEqual(response.json()["dias_restantes"], 22)

    def test_producto_vigente(self):
        response = self.consultar("2026-12-18", "2026-10-19")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["estado"], "VIGENTE")
        self.assertEqual(response.json()["dias_restantes"], 60)

    def test_producto_vence_hoy(self):
        response = self.consultar("2026-10-19", "2026-10-19")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["estado"], "PROXIMO_A_VENCER")
        self.assertEqual(response.json()["dias_restantes"], 0)

    def test_fecha_invalida(self):
        response = self.consultar("fecha-invalida", "2026-10-19")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"], "VALIDATION_ERROR")

    def test_falta_fecha_vencimiento(self):
        response = self.client.post(
            "/api/v1/vencimientos/clasificar",
            json={"fecha_consulta": "2026-10-19"},
        )
        self.assertEqual(response.status_code, 422)

    def test_body_no_es_objeto(self):
        response = self.client.post(
            "/api/v1/vencimientos/clasificar",
            json=["2026-11-10", "2026-10-19"],
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
