"""Agente ReAct conectado a MCP para App Detección Prod."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import ClientSession
from mcp.client.stdio import stdio_client

from ..tool_calling.config import get_settings
from .agent import (
    MAX_PASOS,
    SYSTEM_PROMPT,
    AgentResult,
    _build_safe_fallback,
    _clean_arguments,
    _missing_required_tools,
    _normalize_arguments,
    _observed_action_types,
    _observed_states,
    _tool_call_key,
    _validate_final_response,
)
from .cliente_mcp import build_server_parameters
from .ollama_client import (
    OllamaAgentError,
    extract_agent_response,
    post_json,
)


def _mcp_tool_to_ollama(
    tool: Any,
) -> dict[str, Any]:
    """
    Convierte una herramienta descubierta mediante MCP
    al formato de tools que Ollama puede utilizar.

    El agente no mantiene una lista manual de herramientas.
    Las definiciones provienen de tools/list.
    """
    if hasattr(tool, "model_dump"):
        raw_tool = tool.model_dump(
            by_alias=True,
            exclude_none=True,
        )
    else:
        raw_tool = {
            "name": getattr(
                tool,
                "name",
                None,
            ),
            "description": getattr(
                tool,
                "description",
                "",
            ),
            "inputSchema": getattr(
                tool,
                "inputSchema",
                {},
            ),
        }

    tool_name = raw_tool.get("name")

    if not isinstance(tool_name, str):
        raise ValueError(
            "MCP devolvió una herramienta sin nombre válido."
        )

    input_schema = raw_tool.get(
        "inputSchema",
        raw_tool.get(
            "input_schema",
            {
                "type": "object",
                "properties": {},
            },
        ),
    )

    if not isinstance(input_schema, dict):
        input_schema = {
            "type": "object",
            "properties": {},
        }

    description = raw_tool.get(
        "description",
        "",
    )

    return {
        "type": "function",
        "function": {
            "name": tool_name,
            "description": str(
                description or ""
            ),
            "parameters": input_schema,
        },
    }


def _mcp_result_to_observation(
    result: Any,
) -> dict[str, Any]:
    """
    Convierte el resultado de tools/call en una observación
    que pueda volver al historial del agente.
    """
    if hasattr(result, "model_dump"):
        raw_result = result.model_dump(
            by_alias=True,
            exclude_none=True,
        )
    else:
        raw_result = {
            "content": getattr(
                result,
                "content",
                [],
            ),
            "structuredContent": getattr(
                result,
                "structuredContent",
                None,
            ),
            "isError": getattr(
                result,
                "isError",
                False,
            ),
        }

    if raw_result.get("isError"):
        return {
            "error": (
                "La herramienta MCP devolvió "
                "un resultado de error."
            ),
            "mcp_content": raw_result.get(
                "content",
                [],
            ),
        }

    structured_content = raw_result.get(
        "structuredContent"
    )

    if isinstance(
        structured_content,
        dict,
    ):
        return structured_content

    content = raw_result.get(
        "content",
        [],
    )

    if isinstance(content, list):
        for item in content:
            text: str | None = None

            if isinstance(item, dict):
                raw_text = item.get("text")

                if isinstance(raw_text, str):
                    text = raw_text

            else:
                raw_text = getattr(
                    item,
                    "text",
                    None,
                )

                if isinstance(raw_text, str):
                    text = raw_text

            if text:
                try:
                    parsed = json.loads(text)

                except json.JSONDecodeError:
                    continue

                if isinstance(parsed, dict):
                    return parsed

    return {
        "content": content,
    }


def _chat_with_mcp_tools(
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
):
    """
    Envía a Ollama el historial y las tools descubiertas por MCP.
    """
    settings = get_settings()

    if not settings.ia_habilitada:
        raise OllamaAgentError(
            "La IA está deshabilitada."
        )

    payload = {
        "model": settings.ollama_model,
        "messages": messages,
        "tools": tools,
        "stream": False,
        "options": {
            "temperature": 0,
        },
    }

    response_data = post_json(
        url=settings.ollama_api_url,
        payload=payload,
    )

    return extract_agent_response(
        response_data
    )


def _chat_without_tools(
    messages: list[dict[str, Any]],
):
    """
    Solicita solamente una redacción final.

    No publica tools para impedir nuevas llamadas cuando
    ya existe toda la evidencia necesaria.
    """
    settings = get_settings()

    payload = {
        "model": settings.ollama_model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0,
        },
    }

    response_data = post_json(
        url=settings.ollama_api_url,
        payload=payload,
    )

    return extract_agent_response(
        response_data
    )


async def run_agent_mcp_async(
    question: str,
    *,
    max_steps: int = MAX_PASOS,
) -> AgentResult:
    """
    Ejecuta el agente ReAct utilizando exclusivamente MCP
    para descubrir y ejecutar herramientas.

    Flujo:
    Cliente MCP
        -> initialize
        -> tools/list
        -> Ollama decide
        -> tools/call
        -> observación
        -> Ollama
        -> respuesta final.
    """
    clean_question = question.strip()

    if not clean_question:
        return AgentResult(
            question=question,
            response="La pregunta no puede estar vacía.",
            status="PREGUNTA_INVALIDA",
            steps=0,
            model=None,
            trace=(),
        )

    if max_steps < 1:
        raise ValueError(
            "max_steps debe ser mayor o igual a 1."
        )

    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                SYSTEM_PROMPT
                + "\n\n"
                + "ARQUITECTURA ACTUAL:\n"
                + "Las herramientas disponibles son "
                + "descubiertas dinámicamente mediante MCP. "
                + "Las ejecuciones se realizan mediante "
                + "tools/call sobre el servidor MCP. "
                + "No asumas herramientas que no hayan sido "
                + "publicadas por el servidor."
            ),
        },
        {
            "role": "user",
            "content": clean_question,
        },
    ]

    trace: list[dict[str, Any]] = []

    last_model: str | None = None

    tool_cache: dict[
        str,
        dict[str, Any],
    ] = {}

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
            # -------------------------------------------------
            # MCP: initialize
            # -------------------------------------------------
            await session.initialize()

            # -------------------------------------------------
            # MCP: tools/list
            # -------------------------------------------------
            tools_response = (
                await session.list_tools()
            )

            ollama_tools = [
                _mcp_tool_to_ollama(tool)
                for tool in tools_response.tools
            ]

            discovered_names = [
                tool["function"]["name"]
                for tool in ollama_tools
            ]

            trace.append(
                {
                    "step": 0,
                    "type": "mcp_discovery",
                    "transport": "stdio",
                    "operation": (
                        "initialize -> tools/list"
                    ),
                    "tools": discovered_names,
                }
            )

            for step in range(
                1,
                max_steps + 1,
            ):
                try:
                    model_response = (
                        _chat_with_mcp_tools(
                            messages,
                            ollama_tools,
                        )
                    )

                except OllamaAgentError as exc:
                    trace.append(
                        {
                            "step": step,
                            "type": "error",
                            "message": str(exc),
                        }
                    )

                    return AgentResult(
                        question=clean_question,
                        response=(
                            "No fue posible completar "
                            "la consulta por un error "
                            "controlado del modelo."
                        ),
                        status="ERROR_MODELO",
                        steps=step,
                        model=last_model,
                        trace=tuple(trace),
                    )

                last_model = (
                    model_response.model
                )

                tool_calls = (
                    model_response.tool_calls
                )

                # ==========================================
                # EL MODELO INTENTA RESPONDER
                # ==========================================
                if not tool_calls:
                    missing_tools = (
                        _missing_required_tools(
                            clean_question,
                            trace,
                        )
                    )

                    # --------------------------------------
                    # GUARDRAIL DE COBERTURA
                    # --------------------------------------
                    if missing_tools:
                        trace.append(
                            {
                                "step": step,
                                "type": (
                                    "coverage_guardrail"
                                ),
                                "missing_tools": list(
                                    missing_tools
                                ),
                                "message": (
                                    "El modelo intentó "
                                    "responder sin consultar "
                                    "toda la evidencia MCP."
                                ),
                            }
                        )

                        messages.append(
                            model_response.message
                        )

                        messages.append(
                            {
                                "role": "user",
                                "content": (
                                    "NO RESPONDAS AÚN. "
                                    "La respuesta fue "
                                    "bloqueada por cobertura. "
                                    "Debes utilizar mediante "
                                    "MCP las siguientes tools "
                                    "faltantes: "
                                    f"{', '.join(missing_tools)}. "
                                    "Ejecuta las herramientas "
                                    "mediante tool_calls y luego "
                                    "responde usando únicamente "
                                    "las observaciones obtenidas."
                                ),
                            }
                        )

                        continue

                    final_response = (
                        model_response.content
                    )

                    if not final_response:
                        final_response = (
                            "El agente terminó sin "
                            "producir una respuesta."
                        )

                    violations = (
                        _validate_final_response(
                            clean_question,
                            final_response,
                            trace,
                        )
                    )

                    # --------------------------------------
                    # GUARDRAIL DE FIDELIDAD
                    # --------------------------------------
                    if violations:
                        trace.append(
                            {
                                "step": step,
                                "type": "guardrail",
                                "violations": violations,
                            }
                        )

                        observed_states = (
                            _observed_states(
                                trace
                            )
                        )

                        observed_actions = (
                            _observed_action_types(
                                trace
                            )
                        )

                        correction_messages = (
                            messages
                            + [
                                model_response.message,
                                {
                                    "role": "user",
                                    "content": (
                                        "CORRECCIÓN "
                                        "OBLIGATORIA DE "
                                        "FIDELIDAD. "
                                        "Ya tienes todas "
                                        "las observaciones "
                                        "obtenidas mediante MCP. "
                                        "NO vuelvas a llamar "
                                        "herramientas. "
                                        "Redacta únicamente "
                                        "la respuesta final. "
                                        f"Estados permitidos: "
                                        f"{observed_states}. "
                                        f"Acciones observadas: "
                                        f"{observed_actions}. "
                                        "No interpretes estados. "
                                        "Los precios se expresan "
                                        "en Bs. "
                                        "Incluye evidencia cuando "
                                        "el usuario la solicite."
                                    ),
                                },
                            ]
                        )

                        try:
                            corrected_response = (
                                _chat_without_tools(
                                    correction_messages
                                )
                            )

                            corrected_text = (
                                corrected_response.content
                            )

                            corrected_violations = (
                                _validate_final_response(
                                    clean_question,
                                    corrected_text,
                                    trace,
                                )
                            )

                        except OllamaAgentError as exc:
                            corrected_text = ""

                            corrected_violations = [
                                str(exc)
                            ]

                        if corrected_violations:
                            safe_response = (
                                _build_safe_fallback(
                                    trace
                                )
                            )

                            trace.append(
                                {
                                    "step": step,
                                    "type": (
                                        "guardrail_fallback"
                                    ),
                                    "message": (
                                        "La redacción "
                                        "continuó violando "
                                        "guardrails. "
                                        "Python construyó "
                                        "la respuesta desde "
                                        "observaciones MCP."
                                    ),
                                    "violations": (
                                        corrected_violations
                                    ),
                                }
                            )

                            trace.append(
                                {
                                    "step": step,
                                    "type": "final",
                                    "response": (
                                        safe_response
                                    ),
                                }
                            )

                            return AgentResult(
                                question=clean_question,
                                response=safe_response,
                                status="OK",
                                steps=step,
                                model=last_model,
                                trace=tuple(trace),
                            )

                        trace.append(
                            {
                                "step": step,
                                "type": "final_rewrite",
                                "response": corrected_text,
                            }
                        )

                        trace.append(
                            {
                                "step": step,
                                "type": "final",
                                "response": corrected_text,
                            }
                        )

                        return AgentResult(
                            question=clean_question,
                            response=corrected_text,
                            status="OK",
                            steps=step,
                            model=last_model,
                            trace=tuple(trace),
                        )

                    # --------------------------------------
                    # FINAL VÁLIDO
                    # --------------------------------------
                    trace.append(
                        {
                            "step": step,
                            "type": "final",
                            "response": (
                                final_response
                            ),
                        }
                    )

                    return AgentResult(
                        question=clean_question,
                        response=final_response,
                        status="OK",
                        steps=step,
                        model=last_model,
                        trace=tuple(trace),
                    )

                # ==========================================
                # OLLAMA SOLICITA TOOLS
                # ==========================================
                messages.append(
                    model_response.message
                )

                for tool_call in tool_calls:
                    function_data = (
                        tool_call.get(
                            "function"
                        )
                    )

                    if not isinstance(
                        function_data,
                        dict,
                    ):
                        trace.append(
                            {
                                "step": step,
                                "type": "error",
                                "message": (
                                    "Ollama devolvió "
                                    "una tool call inválida."
                                ),
                            }
                        )

                        continue

                    tool_name = (
                        function_data.get(
                            "name"
                        )
                    )

                    if (
                        not isinstance(
                            tool_name,
                            str,
                        )
                        or not tool_name.strip()
                    ):
                        trace.append(
                            {
                                "step": step,
                                "type": "error",
                                "message": (
                                    "La llamada no "
                                    "contiene nombre "
                                    "de tool válido."
                                ),
                            }
                        )

                        continue

                    tool_name = (
                        tool_name.strip()
                    )

                    if (
                        tool_name
                        not in discovered_names
                    ):
                        observation = {
                            "error": (
                                "La herramienta no "
                                "fue publicada por "
                                "el servidor MCP."
                            )
                        }

                        trace.append(
                            {
                                "step": step,
                                "type": "error",
                                "tool": tool_name,
                                "message": (
                                    observation[
                                        "error"
                                    ]
                                ),
                            }
                        )

                        messages.append(
                            {
                                "role": "tool",
                                "tool_name": (
                                    tool_name
                                ),
                                "content": (
                                    json.dumps(
                                        observation,
                                        ensure_ascii=False,
                                    )
                                ),
                            }
                        )

                        continue

                    try:
                        arguments = (
                            _normalize_arguments(
                                function_data.get(
                                    "arguments"
                                )
                            )
                        )

                    except ValueError as exc:
                        observation = {
                            "error": str(exc)
                        }

                        trace.append(
                            {
                                "step": step,
                                "type": "error",
                                "tool": tool_name,
                                "message": str(exc),
                            }
                        )

                        messages.append(
                            {
                                "role": "tool",
                                "tool_name": (
                                    tool_name
                                ),
                                "content": (
                                    json.dumps(
                                        observation,
                                        ensure_ascii=False,
                                    )
                                ),
                            }
                        )

                        continue

                    arguments = (
                        _clean_arguments(
                            arguments
                        )
                    )

                    call_key = (
                        _tool_call_key(
                            tool_name,
                            arguments,
                        )
                    )

                    # --------------------------------------
                    # TOOL REPETIDA
                    # --------------------------------------
                    if call_key in tool_cache:
                        cached_result = (
                            tool_cache[
                                call_key
                            ]
                        )

                        trace.append(
                            {
                                "step": step,
                                "type": (
                                    "duplicate_tool_guardrail"
                                ),
                                "tool": tool_name,
                                "arguments": arguments,
                                "via": "MCP",
                                "message": (
                                    "La tool MCP ya "
                                    "había sido ejecutada. "
                                    "Se reutilizó la "
                                    "observación."
                                ),
                            }
                        )

                        messages.append(
                            {
                                "role": "tool",
                                "tool_name": (
                                    tool_name
                                ),
                                "content": (
                                    json.dumps(
                                        cached_result,
                                        ensure_ascii=False,
                                    )
                                ),
                            }
                        )

                        continue

                    # --------------------------------------
                    # ACCIÓN MCP
                    # --------------------------------------
                    trace.append(
                        {
                            "step": step,
                            "type": "action",
                            "tool": tool_name,
                            "arguments": arguments,
                            "via": "MCP",
                            "operation": (
                                "tools/call"
                            ),
                        }
                    )

                    try:
                        mcp_result = (
                            await session.call_tool(
                                tool_name,
                                arguments=arguments,
                            )
                        )

                        observation = (
                            _mcp_result_to_observation(
                                mcp_result
                            )
                        )

                    except Exception as exc:
                        observation = {
                            "error": str(exc)
                        }

                    if (
                        "error"
                        not in observation
                    ):
                        tool_cache[
                            call_key
                        ] = observation

                    # --------------------------------------
                    # OBSERVACIÓN MCP
                    # --------------------------------------
                    trace.append(
                        {
                            "step": step,
                            "type": "observation",
                            "tool": tool_name,
                            "result": observation,
                            "via": "MCP",
                            "transport": "stdio",
                        }
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": tool_name,
                            "content": json.dumps(
                                observation,
                                ensure_ascii=False,
                            ),
                        }
                    )

            # ==============================================
            # MAX_PASOS
            # ==============================================
            trace.append(
                {
                    "step": max_steps,
                    "type": "limit",
                    "message": (
                        f"Se alcanzó MAX_PASOS="
                        f"{max_steps}."
                    ),
                }
            )

            return AgentResult(
                question=clean_question,
                response=(
                    "La consulta alcanzó el límite "
                    "máximo de pasos sin obtener "
                    "una respuesta final."
                ),
                status="LIMITE_PASOS",
                steps=max_steps,
                model=last_model,
                trace=tuple(trace),
            )


def run_agent_mcp(
    question: str,
    *,
    max_steps: int = MAX_PASOS,
) -> AgentResult:
    """
    Ejecuta el agente MCP desde código síncrono.

    Para aplicaciones async se debe utilizar
    run_agent_mcp_async().
    """
    return asyncio.run(
        run_agent_mcp_async(
            question,
            max_steps=max_steps,
        )
    )