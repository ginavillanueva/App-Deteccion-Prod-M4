"""Tests de integración de App Detección Prod.

Se integran piezas reales de la aplicación:

- StateGraph de LangGraph;
- validación y clasificación;
- extracción de contexto;
- nodos MCP;
- runtime persistente;
- AsyncSqliteSaver;
- checkpoints SQLite;
- pausa y reanudación.

La única frontera sustituida es call_mcp_tool para garantizar
una corrida reproducible sin modelo, red ni servidor MCP externo.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from src.langgraph_orchestration import mcp_nodes
from src.langgraph_orchestration.persistent_runtime import (
    ejecutar_hasta_pausa,
    ejecutar_persistente,
    obtener_checkpoint_persistido,
    obtener_estado_ejecucion,
    reanudar_persistente,
)
from src.persistence import langgraph_checkpointer


class LangGraphPersistenceIntegrationTest(
    unittest.IsolatedAsyncioTestCase
):
    """Integración real LangGraph + SQLite con MCP en la frontera."""

    async def asyncSetUp(self):
        self._tmp = tempfile.TemporaryDirectory()

        self.db_temporal = (
            Path(self._tmp.name)
            / "checkpoints_integration.sqlite"
        )

        self.db_patch = patch.object(
            langgraph_checkpointer,
            "LANGGRAPH_CHECKPOINT_DB",
            self.db_temporal,
        )
        self.db_patch.start()

    async def asyncTearDown(self):
        self.db_patch.stop()
        self._tmp.cleanup()

    @staticmethod
    async def _mcp_controlado(
        tool_name: str,
        arguments: dict,
    ) -> dict:
        """Respuesta determinística de la frontera MCP."""

        respuestas = {
            "consultar_detalle_producto": {
                "structuredContent": {
                    "row_count": 1,
                    "source_tables": [
                        "productos_vencimiento",
                    ],
                    "producto":
                        arguments.get("producto", ""),
                    "tienda":
                        arguments.get("tienda", ""),
                    "dias_restantes": 5,
                },
                "isError": False,
            },

            "consultar_cambios_precio": {
                "structuredContent": {
                    "row_count": 1,
                    "source_tables": [
                        "cambios_precio",
                    ],
                    "producto":
                        arguments.get("producto", ""),
                    "precio_anterior": 10.0,
                    "precio_nuevo": 9.5,
                },
                "isError": False,
            },

            "consultar_acciones_comerciales": {
                "structuredContent": {
                    "row_count": 1,
                    "source_tables": [
                        "acciones_comerciales",
                    ],
                    "producto":
                        arguments.get("producto", ""),
                    "accion": "registro_controlado",
                },
                "isError": False,
            },
        }

        if tool_name not in respuestas:
            raise AssertionError(
                f"Tool inesperada durante integración: {tool_name}"
            )

        return respuestas[tool_name]

    async def test_vencimiento_recorrido_real_y_checkpoint_temporal(
        self,
    ):
        """Entrada -> grafo -> MCP -> SQLite -> checkpoint final."""

        thread_id = "integration-vencimiento-001"

        pregunta = (
            "Cuantos dias faltan para vencer "
            "el Yogur natural 1 litro Sala 12"
        )

        mcp_mock = AsyncMock(
            side_effect=self._mcp_controlado
        )

        with patch.object(
            mcp_nodes,
            "call_mcp_tool",
            mcp_mock,
        ):
            resultado = await ejecutar_persistente(
                pregunta,
                thread_id,
            )

            checkpoint = await obtener_checkpoint_persistido(
                thread_id
            )

        self.assertEqual(
            resultado["intencion"],
            "VENCIMIENTO",
        )
        self.assertEqual(
            resultado["producto"],
            "Yogur natural 1 litro",
        )
        self.assertEqual(
            resultado["tienda"],
            "Sala 12",
        )

        self.assertEqual(
            resultado["tools_usadas"],
            ["consultar_detalle_producto"],
        )

        nodos = [
            entrada["nodo"]
            for entrada in resultado["traza"]
        ]

        self.assertEqual(
            nodos,
            [
                "validar_entrada",
                "clasificar_intencion",
                "extraer_contexto",
                "consultar_detalle_mcp",
            ],
        )

        self.assertTrue(
            checkpoint
        )
        self.assertEqual(
            checkpoint["next"],
            [],
        )
        self.assertEqual(
            checkpoint["values"]["thread_id"],
            thread_id,
        )

        self.assertTrue(
            self.db_temporal.exists()
        )

        mcp_mock.assert_awaited_once()

        self.assertEqual(
            mcp_mock.await_args.args[0],
            "consultar_detalle_producto",
        )

    async def test_auditoria_completa_recorrida_por_tres_nodos_mcp(
        self,
    ):
        """Auditoría real recorre detalle -> precio -> acción."""

        thread_id = "integration-auditoria-001"

        pregunta = (
            "Necesito una auditoria completa "
            "del Yogur natural 1 litro Sala 12"
        )

        mcp_mock = AsyncMock(
            side_effect=self._mcp_controlado
        )

        with patch.object(
            mcp_nodes,
            "call_mcp_tool",
            mcp_mock,
        ):
            resultado = await ejecutar_persistente(
                pregunta,
                thread_id,
            )

            checkpoint = await obtener_checkpoint_persistido(
                thread_id
            )

        self.assertEqual(
            resultado["intencion"],
            "AUDITORIA_COMPLETA",
        )

        self.assertEqual(
            resultado["tools_usadas"],
            [
                "consultar_detalle_producto",
                "consultar_cambios_precio",
                "consultar_acciones_comerciales",
            ],
        )

        nodos = [
            entrada["nodo"]
            for entrada in resultado["traza"]
        ]

        self.assertEqual(
            nodos,
            [
                "validar_entrada",
                "clasificar_intencion",
                "extraer_contexto",
                "consultar_detalle_mcp",
                "consultar_cambios_precio_mcp",
                "consultar_acciones_comerciales_mcp",
            ],
        )

        tools_llamadas = [
            llamada.args[0]
            for llamada in mcp_mock.await_args_list
        ]

        self.assertEqual(
            tools_llamadas,
            [
                "consultar_detalle_producto",
                "consultar_cambios_precio",
                "consultar_acciones_comerciales",
            ],
        )

        self.assertEqual(
            checkpoint["next"],
            [],
        )

        self.assertEqual(
            checkpoint["values"]["thread_id"],
            thread_id,
        )

        self.assertTrue(
            self.db_temporal.exists()
        )

    async def test_pausa_checkpoint_y_reanudacion_mismo_thread(
        self,
    ):
        """Pausa real -> checkpoint -> reanudación -> finalización."""

        thread_id = "integration-pausa-001"

        pregunta = (
            "Cuantos dias faltan para vencer "
            "el Yogur natural 1 litro Sala 12"
        )

        mcp_mock = AsyncMock(
            side_effect=self._mcp_controlado
        )

        with patch.object(
            mcp_nodes,
            "call_mcp_tool",
            mcp_mock,
        ):
            pausa = await ejecutar_hasta_pausa(
                pregunta=pregunta,
                thread_id=thread_id,
                interrupt_before=[
                    "consultar_detalle_mcp",
                ],
            )

            estado_pausa = (
                await obtener_estado_ejecucion(
                    thread_id
                )
            )

            # El nodo MCP aún NO debe haberse ejecutado.
            mcp_mock.assert_not_awaited()

            resultado_final = (
                await reanudar_persistente(
                    thread_id
                )
            )

            estado_final = (
                await obtener_estado_ejecucion(
                    thread_id
                )
            )

        self.assertEqual(
            pausa["next"],
            ["consultar_detalle_mcp"],
        )

        self.assertEqual(
            estado_pausa,
            "PAUSADO",
        )

        nodos_antes = [
            entrada["nodo"]
            for entrada in pausa["values"]["traza"]
        ]

        self.assertEqual(
            nodos_antes,
            [
                "validar_entrada",
                "clasificar_intencion",
                "extraer_contexto",
            ],
        )

        self.assertEqual(
            pausa["values"]["tools_usadas"],
            [],
        )

        self.assertEqual(
            resultado_final["tools_usadas"],
            ["consultar_detalle_producto"],
        )

        nodos_finales = [
            entrada["nodo"]
            for entrada in resultado_final["traza"]
        ]

        self.assertEqual(
            nodos_finales,
            [
                "validar_entrada",
                "clasificar_intencion",
                "extraer_contexto",
                "consultar_detalle_mcp",
            ],
        )

        self.assertEqual(
            estado_final,
            "FINALIZADO",
        )

        mcp_mock.assert_awaited_once()

        self.assertTrue(
            self.db_temporal.exists()
        )


if __name__ == "__main__":
    unittest.main()