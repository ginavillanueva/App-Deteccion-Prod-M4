"""Cliente MCP de App Detección Prod."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from mcp import (
    ClientSession,
    StdioServerParameters,
)
from mcp.client.stdio import stdio_client


MODULE_ROOT = Path(__file__).resolve().parents[2]

SERVER_MODULE = "src.agent_mcp.servidor_mcp"


def build_server_parameters() -> StdioServerParameters:
    """
    Configura el servidor MCP que será lanzado como proceso hijo.

    Se utiliza el mismo Python del entorno virtual activo.
    """
    return StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            SERVER_MODULE,
        ],
        cwd=str(MODULE_ROOT),
    )


def tool_to_dict(tool: Any) -> dict[str, Any]:
    """Convierte una definición MCP de tool en un diccionario."""
    if hasattr(tool, "model_dump"):
        return tool.model_dump(
            by_alias=True,
            exclude_none=True,
        )

    return {
        "name": getattr(
            tool,
            "name",
            None,
        ),
        "description": getattr(
            tool,
            "description",
            None,
        ),
        "inputSchema": getattr(
            tool,
            "inputSchema",
            {},
        ),
    }


def result_to_dict(result: Any) -> dict[str, Any]:
    """Convierte el resultado de tools/call a un diccionario."""
    if hasattr(result, "model_dump"):
        return result.model_dump(
            by_alias=True,
            exclude_none=True,
        )

    return {
        "content": getattr(
            result,
            "content",
            [],
        ),
        "isError": getattr(
            result,
            "isError",
            False,
        ),
    }


async def discover_tools() -> list[dict[str, Any]]:
    """
    Ejecuta initialize + tools/list contra el servidor MCP.
    """
    server_parameters = (
        build_server_parameters()
    )

    async with stdio_client(
        server_parameters
    ) as streams:
        read_stream, write_stream = streams

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            await session.initialize()

            response = await session.list_tools()

            return [
                tool_to_dict(tool)
                for tool in response.tools
            ]


async def call_mcp_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """
    Ejecuta una herramienta mediante tools/call.
    """
    server_parameters = (
        build_server_parameters()
    )

    async with stdio_client(
        server_parameters
    ) as streams:
        read_stream, write_stream = streams

        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments=arguments,
            )

            return result_to_dict(result)


async def demo_list_tools() -> None:
    """Muestra todas las tools descubiertas por MCP."""
    tools = await discover_tools()

    print("=" * 72)
    print("APP DETECCIÓN PROD - CLIENTE MCP")
    print("=" * 72)
    print("OPERACIÓN: initialize -> tools/list")
    print(f"TOTAL TOOLS: {len(tools)}")
    print("-" * 72)

    for index, tool in enumerate(
        tools,
        start=1,
    ):
        print()
        print(
            f"{index}. {tool.get('name')}"
        )

        print(
            "   DESCRIPCIÓN:",
            tool.get(
                "description",
                "",
            ),
        )

        print(
            "   INPUT SCHEMA:"
        )

        print(
            json.dumps(
                tool.get(
                    "inputSchema",
                    {},
                ),
                indent=2,
                ensure_ascii=False,
            )
        )

    print()
    print("=" * 72)


async def demo_call_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> None:
    """Ejecuta una tool y muestra el resultado MCP."""
    result = await call_mcp_tool(
        tool_name,
        arguments,
    )

    print("=" * 72)
    print("APP DETECCIÓN PROD - CLIENTE MCP")
    print("=" * 72)
    print("OPERACIÓN: initialize -> tools/call")
    print(f"TOOL: {tool_name}")
    print(
        "ARGUMENTOS:",
        json.dumps(
            arguments,
            ensure_ascii=False,
        ),
    )

    print("-" * 72)

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )

    print("=" * 72)


def parse_arguments() -> argparse.Namespace:
    """Lee opciones de línea de comandos."""
    parser = argparse.ArgumentParser(
        description=(
            "Cliente MCP de App Detección Prod."
        )
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help=(
            "Inicializa la sesión y ejecuta tools/list."
        ),
    )

    parser.add_argument(
        "--call",
        type=str,
        help=(
            "Nombre de una herramienta MCP."
        ),
    )

    parser.add_argument(
        "--args",
        type=str,
        default="{}",
        help=(
            "Argumentos JSON para tools/call."
        ),
    )

    return parser.parse_args()


async def async_main() -> int:
    """Ejecuta el cliente MCP."""
    arguments = parse_arguments()

    if arguments.list:
        await demo_list_tools()
        return 0

    if arguments.call:
        try:
            tool_arguments = json.loads(
                arguments.args
            )

        except json.JSONDecodeError as exc:
            print(
                "ERROR: --args debe contener "
                "un objeto JSON válido."
            )
            print(exc)
            return 1

        if not isinstance(
            tool_arguments,
            dict,
        ):
            print(
                "ERROR: --args debe ser "
                "un objeto JSON."
            )
            return 1

        await demo_call_tool(
            arguments.call,
            tool_arguments,
        )

        return 0

    print(
        "Debes utilizar --list "
        "o --call."
    )

    return 1


def main() -> int:
    """Punto de entrada síncrono."""
    return asyncio.run(
        async_main()
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )