"""
Contract tests del endpoint principal de App Detección Prod.

Validan:
- códigos HTTP;
- campos obligatorios;
- tipos;
- catálogo de intenciones;
- JSON Schema;
- rechazo de requests inválidos.

Durante estos tests NO se encienden:
- Ollama;
- red externa;
- servidor MCP;
- SQLite productiva.

La ejecución LangGraph se sustituye solamente en la frontera
del endpoint HTTP para probar exclusivamente el contrato.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from jsonschema import ValidationError, validate
from starlette.testclient import TestClient

from src.api import contract_api


ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = (
    ROOT
    / "docs"
    / "API_CONTRACT_SCHEMA.json"
)


class ApiContractTest(unittest.TestCase):
    """Contrato HTTP de POST /api/v1/deteccion."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(
            contract_api.app
        )

        cls.schema = json.loads(
            SCHEMA_PATH.read_text(
                encoding="utf-8-sig"
            )
        )

    def test_post_deteccion_valido_cumple_schema_y_http_200(
        self,
    ):
        resultado_controlado = {
            "thread_id": "contract-001",
            "intencion": "VENCIMIENTO",
            "producto": "Yogur natural 1 litro",
            "tienda": "Sala 12",
            "bloqueado": False,
            "problema": "",
            "tools_usadas": [
                "consultar_detalle_producto",
            ],
            "fuentes": [
                "productos_vencimiento",
            ],
            "observaciones": [
                {
                    "dias_restantes": 5,
                }
            ],
            "traza": [
                {
                    "nodo": "validar_entrada",
                },
                {
                    "nodo": "clasificar_intencion",
                },
                {
                    "nodo": "extraer_contexto",
                },
                {
                    "nodo": "consultar_detalle_mcp",
                },
            ],
            "respuesta": (
                "Consulta procesada correctamente."
            ),
        }

        runtime_mock = AsyncMock(
            return_value=resultado_controlado
        )

        with patch.object(
            contract_api,
            "ejecutar_persistente",
            runtime_mock,
        ):
            response = self.client.post(
                "/api/v1/deteccion",
                json={
                    "pregunta": (
                        "Cuantos dias faltan para vencer "
                        "el Yogur natural 1 litro Sala 12"
                    ),
                    "thread_id": "contract-001",
                },
            )

        self.assertEqual(
            response.status_code,
            200,
        )

        body = response.json()

        validate(
            instance=body,
            schema=self.schema,
        )

        self.assertEqual(
            body["thread_id"],
            "contract-001",
        )

        self.assertEqual(
            body["intencion"],
            "VENCIMIENTO",
        )

        self.assertEqual(
            body["producto"],
            "Yogur natural 1 litro",
        )

        self.assertEqual(
            body["tienda"],
            "Sala 12",
        )

        self.assertIsInstance(
            body["bloqueado"],
            bool,
        )

        self.assertIsInstance(
            body["tools_usadas"],
            list,
        )

        self.assertIsInstance(
            body["fuentes"],
            list,
        )

        self.assertIsInstance(
            body["observaciones"],
            list,
        )

        self.assertIsInstance(
            body["traza"],
            list,
        )

        runtime_mock.assert_awaited_once_with(
            (
                "Cuantos dias faltan para vencer "
                "el Yogur natural 1 litro Sala 12"
            ),
            "contract-001",
        )

    def test_post_deteccion_sin_pregunta_devuelve_http_422(
        self,
    ):
        runtime_mock = AsyncMock()

        with patch.object(
            contract_api,
            "ejecutar_persistente",
            runtime_mock,
        ):
            response = self.client.post(
                "/api/v1/deteccion",
                json={
                    "thread_id": "contract-002",
                },
            )

        self.assertEqual(
            response.status_code,
            422,
        )

        body = response.json()

        self.assertEqual(
            body["error"],
            "VALIDATION_ERROR",
        )

        self.assertIn(
            "pregunta",
            body["detalle"],
        )

        runtime_mock.assert_not_awaited()

    def test_post_deteccion_thread_id_vacio_devuelve_http_422(
        self,
    ):
        runtime_mock = AsyncMock()

        with patch.object(
            contract_api,
            "ejecutar_persistente",
            runtime_mock,
        ):
            response = self.client.post(
                "/api/v1/deteccion",
                json={
                    "pregunta": "Consultar vencimiento",
                    "thread_id": "   ",
                },
            )

        self.assertEqual(
            response.status_code,
            422,
        )

        body = response.json()

        self.assertEqual(
            body["error"],
            "VALIDATION_ERROR",
        )

        self.assertIn(
            "thread_id",
            body["detalle"],
        )

        runtime_mock.assert_not_awaited()

    def test_schema_rechaza_intencion_fuera_del_catalogo(
        self,
    ):
        body_invalido = {
            "thread_id": "contract-003",
            "intencion": "INVENTADA",
            "producto": "",
            "tienda": "",
            "bloqueado": False,
            "problema": "",
            "tools_usadas": [],
            "fuentes": [],
            "observaciones": [],
            "traza": [],
            "respuesta": "",
        }

        with self.assertRaises(
            ValidationError,
        ):
            validate(
                instance=body_invalido,
                schema=self.schema,
            )

    def test_schema_rechaza_tipo_incorrecto(
        self,
    ):
        body_invalido = {
            "thread_id": "contract-004",
            "intencion": "OTRO",
            "producto": "",
            "tienda": "",
            "bloqueado": "NO",
            "problema": "",
            "tools_usadas": [],
            "fuentes": [],
            "observaciones": [],
            "traza": [],
            "respuesta": "",
        }

        with self.assertRaises(
            ValidationError,
        ):
            validate(
                instance=body_invalido,
                schema=self.schema,
            )


if __name__ == "__main__":
    unittest.main()
