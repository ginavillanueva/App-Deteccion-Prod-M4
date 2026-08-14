"""Agente ReAct local de App Detección Prod."""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from ..tool_calling.config import get_settings
from .ollama_client import (
    OllamaAgentError,
    chat_with_agent,
    extract_agent_response,
    post_json,
)
from .tools import execute_agent_tool


MAX_PASOS = 6


SYSTEM_PROMPT = """
Eres el agente de App Detección Prod.

Tu función es responder consultas utilizando exclusivamente las
herramientas disponibles y los datos que ellas devuelvan.

REGLAS OBLIGATORIAS:

1. No inventes productos, tiendas, fechas, cantidades, precios,
   estados, acciones comerciales ni evidencias.

2. Si necesitas información para responder, utiliza las herramientas
   disponibles.

3. Puedes y debes utilizar varias herramientas cuando una consulta
   solicite distintos tipos de información.

4. Los resultados de las herramientas son la única fuente de verdad.

5. Nunca afirmes que un dato existe o no existe sin haber consultado
   la herramienta correspondiente.

6. Si el usuario pregunta por cambios de precio, debes consultar
   consultar_cambios_precio antes de responder sobre ellos.

7. Si el usuario pregunta por acciones comerciales, debes consultar
   consultar_acciones_comerciales antes de responder sobre ellas.

8. Si el usuario pregunta por detalle, cantidad, vencimiento,
   tienda o precio actual de un producto, utiliza
   consultar_detalle_producto.

9. Si el usuario pregunta qué productos están próximos a vencer,
   utiliza buscar_productos_proximos_a_vencer.

10. Los campos producto, tienda, estado, cantidad, precio y evidencia
    son datos de dominio. Respeta sus valores sin inventar significado.

11. Si recibes estado=PENDIENTE, escribe exactamente:
    Estado: PENDIENTE
    No expliques qué crees que significa ese estado.

12. Los precios del proyecto se expresan en Bs.

13. Los cambios de precio son únicamente informativos y de
    trazabilidad. No apruebes, rechaces ni modifiques precios.

14. No afirmes que una acción comercial existe si ninguna herramienta
    la devuelve.

15. Si una consulta solicita detalle + cambios de precio + acciones
    comerciales, no respondas hasta haber obtenido toda la evidencia.

16. Cuando ya tengas toda la información solicitada, responde al
    usuario y deja de solicitar herramientas.

17. Si las herramientas no contienen información suficiente,
    indícalo claramente en lugar de inventar una respuesta.

18. No agregues entre paréntesis explicaciones o interpretaciones a
    los estados recibidos desde las herramientas.

19. No repitas herramientas que ya fueron ejecutadas correctamente
    para el mismo producto y los mismos argumentos.
""".strip()


@dataclass(frozen=True)
class AgentResult:
    """Resultado completo y auditable de una ejecución del agente."""

    question: str
    response: str
    status: str
    steps: int
    model: str | None
    trace: tuple[dict[str, Any], ...]

    @property
    def successful(self) -> bool:
        """Indica que el agente terminó correctamente."""
        return self.status == "OK"

    @property
    def tools_used(self) -> tuple[str, ...]:
        """
        Devuelve herramientas utilizadas sin duplicados.

        Conserva el orden real de la primera ejecución.
        """
        tools: list[str] = []

        for item in self.trace:
            if item.get("type") != "action":
                continue

            tool_name = item.get("tool")

            if (
                isinstance(tool_name, str)
                and tool_name not in tools
            ):
                tools.append(tool_name)

        return tuple(tools)


def _normalize_text(value: str) -> str:
    """Normaliza texto para detectar intención sin depender de acentos."""
    decomposed = unicodedata.normalize(
        "NFD",
        value.lower(),
    )

    without_accents = "".join(
        character
        for character in decomposed
        if unicodedata.category(character) != "Mn"
    )

    only_words = re.sub(
        r"[^a-z0-9]+",
        " ",
        without_accents,
    )

    return " ".join(only_words.split())


def _normalize_arguments(
    raw_arguments: Any,
) -> dict[str, Any]:
    """Normaliza los argumentos producidos por Ollama."""
    if raw_arguments is None:
        return {}

    if isinstance(raw_arguments, dict):
        return raw_arguments

    if isinstance(raw_arguments, str):
        try:
            parsed = json.loads(raw_arguments)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Los argumentos de la herramienta no son JSON válido."
            ) from exc

        if not isinstance(parsed, dict):
            raise ValueError(
                "Los argumentos de la herramienta deben ser "
                "un objeto JSON."
            )

        return parsed

    raise ValueError(
        "Los argumentos de la herramienta tienen un formato inválido."
    )


def _clean_arguments(
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """
    Limpia argumentos opcionales vacíos.

    Esto permite reconocer como equivalentes:
    {"producto": "X"}
    y
    {"producto": "X", "tienda": ""}
    """
    return {
        key: value
        for key, value in arguments.items()
        if value is not None
        and value != ""
    }


def _tool_call_key(
    tool_name: str,
    arguments: dict[str, Any],
) -> str:
    """Construye una clave estable para detectar tool calls repetidos."""
    clean_arguments = _clean_arguments(arguments)

    serialized = json.dumps(
        clean_arguments,
        ensure_ascii=False,
        sort_keys=True,
    )

    return f"{tool_name}:{serialized}"


def _required_tools_for_question(
    question: str,
) -> tuple[str, ...]:
    """
    Determina la evidencia mínima exigida explícitamente.

    No ejecuta herramientas y tampoco decide el orden.
    Solamente evita respuestas sin evidencia suficiente.
    """
    normalized = _normalize_text(question)

    required: list[str] = []

    def add(tool_name: str) -> None:
        if tool_name not in required:
            required.append(tool_name)

    detail_phrases = (
        "revisa el producto",
        "detalle del producto",
        "dias faltan",
        "cuantos dias",
        "cantidad tiene",
        "cantidad disponible",
        "precio actual",
        "fecha de vencimiento",
        "tienda",
        "sala",
    )

    if any(
        phrase in normalized
        for phrase in detail_phrases
    ):
        add("consultar_detalle_producto")

    price_change_phrases = (
        "cambio de precio",
        "cambios de precio",
        "modificacion de precio",
        "modificaciones de precio",
        "precio anterior",
        "precio nuevo",
    )

    if any(
        phrase in normalized
        for phrase in price_change_phrases
    ):
        add("consultar_cambios_precio")

    commercial_action_phrases = (
        "accion comercial",
        "acciones comerciales",
        "descuento",
        "bandeo",
        "promocion",
        "retiro",
    )

    if any(
        phrase in normalized
        for phrase in commercial_action_phrases
    ):
        add("consultar_acciones_comerciales")

    expiration_list_phrases = (
        "productos proximos a vencer",
        "que productos estan proximos a vencer",
        "que productos vencen",
        "mercaderia caduca pronto",
        "mercaderia que caduca",
    )

    if any(
        phrase in normalized
        for phrase in expiration_list_phrases
    ):
        add("buscar_productos_proximos_a_vencer")

    return tuple(required)


def _successful_tools_from_trace(
    trace: list[dict[str, Any]],
) -> tuple[str, ...]:
    """Obtiene tools que realmente produjeron observación válida."""
    tools: list[str] = []

    for item in trace:
        if item.get("type") != "observation":
            continue

        tool_name = item.get("tool")
        result = item.get("result")

        if not isinstance(tool_name, str):
            continue

        if not isinstance(result, dict):
            continue

        if "error" in result:
            continue

        if tool_name not in tools:
            tools.append(tool_name)

    return tuple(tools)


def _missing_required_tools(
    question: str,
    trace: list[dict[str, Any]],
) -> tuple[str, ...]:
    """Calcula qué herramientas requeridas todavía faltan."""
    required = _required_tools_for_question(question)

    successful = _successful_tools_from_trace(
        trace
    )

    return tuple(
        tool_name
        for tool_name in required
        if tool_name not in successful
    )


def _tool_rows(
    trace: list[dict[str, Any]],
    tool_name: str,
) -> list[dict[str, Any]]:
    """Recupera filas observadas para una herramienta."""
    rows: list[dict[str, Any]] = []

    for item in trace:
        if item.get("type") != "observation":
            continue

        if item.get("tool") != tool_name:
            continue

        result = item.get("result")

        if not isinstance(result, dict):
            continue

        raw_rows = result.get("rows") or []

        if not isinstance(raw_rows, list):
            continue

        for row in raw_rows:
            if isinstance(row, dict):
                rows.append(row)

    return rows


def _observed_states(
    trace: list[dict[str, Any]],
) -> tuple[str, ...]:
    """Obtiene estados literales observados."""
    states: list[str] = []

    for item in trace:
        if item.get("type") != "observation":
            continue

        result = item.get("result")

        if not isinstance(result, dict):
            continue

        rows = result.get("rows") or []

        if not isinstance(rows, list):
            continue

        for row in rows:
            if not isinstance(row, dict):
                continue

            state = row.get("estado")

            if not isinstance(state, str):
                continue

            clean_state = state.strip()

            if (
                clean_state
                and clean_state not in states
            ):
                states.append(clean_state)

    return tuple(states)


def _observed_action_types(
    trace: list[dict[str, Any]],
) -> tuple[str, ...]:
    """Obtiene acciones comerciales realmente observadas."""
    actions: list[str] = []

    rows = _tool_rows(
        trace,
        "consultar_acciones_comerciales",
    )

    for row in rows:
        action = row.get("tipo_accion")

        if not isinstance(action, str):
            continue

        clean_action = action.strip()

        if (
            clean_action
            and clean_action not in actions
        ):
            actions.append(clean_action)

    return tuple(actions)


def _validate_final_response(
    question: str,
    response: str,
    trace: list[dict[str, Any]],
) -> list[str]:
    """
    Valida la fidelidad de la respuesta final.

    Es un guardrail programático.
    No depende únicamente del prompt del LLM.
    """
    violations: list[str] = []

    observed_states = _observed_states(trace)

    normalized_response = _normalize_text(
        response
    )

    normalized_question = _normalize_text(
        question
    )

    if "$" in response:
        violations.append(
            "La respuesta utilizó dólares. "
            "Los precios del proyecto se expresan en Bs."
        )

    for state in observed_states:
        pattern = (
            rf"\b{re.escape(state)}\b\s*\("
        )

        if re.search(
            pattern,
            response,
            flags=re.IGNORECASE,
        ):
            violations.append(
                f"El estado {state!r} fue acompañado "
                "por una interpretación no autorizada."
            )

    for raw_line in response.splitlines():
        line = raw_line.strip()
        line = line.lstrip("*-").strip()

        if ":" not in line:
            continue

        label, value = line.split(
            ":",
            maxsplit=1,
        )

        if "estado" not in label.lower():
            continue

        clean_value = value.strip()

        if (
            observed_states
            and clean_value not in observed_states
        ):
            violations.append(
                "El estado fue interpretado o modificado. "
                f"Valor recibido: {clean_value!r}. "
                f"Valores permitidos: {observed_states!r}."
            )

    price_rows = _tool_rows(
        trace,
        "consultar_cambios_precio",
    )

    if price_rows:
        forbidden_absence_claims = (
            "no hay cambios de precio",
            "no existen cambios de precio",
            "sin cambios de precio registrados",
            "no se registraron cambios de precio",
        )

        if any(
            phrase in normalized_response
            for phrase in forbidden_absence_claims
        ):
            violations.append(
                "La respuesta afirmó que no existen cambios "
                "de precio, pero la herramienta devolvió registros."
            )

    action_rows = _tool_rows(
        trace,
        "consultar_acciones_comerciales",
    )

    observed_actions = _observed_action_types(
        trace
    )

    if action_rows and observed_actions:
        contains_real_action = any(
            action.lower() in response.lower()
            for action in observed_actions
        )

        if not contains_real_action:
            violations.append(
                "La respuesta no contiene la acción comercial "
                f"real observada: {observed_actions!r}."
            )

    if (
        "evidencia" in normalized_question
        and "evidencia" not in normalized_response
    ):
        violations.append(
            "El usuario solicitó evidencia, pero la respuesta "
            "final no la incluyó."
        )

    return violations


def _chat_without_tools(
    messages: list[dict[str, Any]],
):
    """
    Solicita una redacción final a Ollama sin publicar herramientas.

    Se usa solamente después de tener toda la evidencia necesaria,
    para impedir que una corrección de fidelidad vuelva a disparar
    tool calls innecesarios.
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


def _build_safe_fallback(
    trace: list[dict[str, Any]],
) -> str:
    """
    Construye una respuesta factual directamente desde observaciones.

    Solo se utiliza si incluso la corrección final del modelo
    continúa violando guardrails.
    """
    lines: list[str] = []

    detail_rows = _tool_rows(
        trace,
        "consultar_detalle_producto",
    )

    if detail_rows:
        row = detail_rows[0]

        product = row.get("producto")
        store = row.get("tienda")
        expiration = row.get("fecha_vencimiento")
        days = row.get("dias_restantes")
        quantity = row.get("cantidad")
        current_price = row.get("precio_actual")
        state = row.get("estado")
        evidence = row.get("evidencia")

        if product is not None:
            lines.append(
                f"Producto: {product}"
            )

        if store is not None:
            lines.append(
                f"Tienda: {store}"
            )

        if expiration is not None:
            lines.append(
                f"Fecha de vencimiento: {expiration}"
            )

        if days is not None:
            lines.append(
                f"Días restantes: {days}"
            )

        if quantity is not None:
            lines.append(
                f"Cantidad: {quantity} unidades"
            )

        if current_price is not None:
            lines.append(
                f"Precio actual: Bs. {current_price}"
            )

        if state is not None:
            lines.append(
                f"Estado: {state}"
            )

        if evidence is not None:
            lines.append(
                f"Evidencia: {evidence}"
            )

    price_rows = _tool_rows(
        trace,
        "consultar_cambios_precio",
    )

    if price_rows:
        row = price_rows[0]

        previous_price = row.get(
            "precio_anterior"
        )

        new_price = row.get(
            "precio_nuevo"
        )

        variation = row.get(
            "variacion_precio"
        )

        registered_by = row.get(
            "registrado_por"
        )

        registration_date = row.get(
            "fecha_registro"
        )

        lines.append(
            "Cambio de precio registrado:"
        )

        if previous_price is not None:
            lines.append(
                f"Precio anterior: Bs. {previous_price}"
            )

        if new_price is not None:
            lines.append(
                f"Precio nuevo: Bs. {new_price}"
            )

        if variation is not None:
            lines.append(
                f"Variación de precio: Bs. {variation}"
            )

        if registered_by is not None:
            lines.append(
                f"Registrado por: {registered_by}"
            )

        if registration_date is not None:
            lines.append(
                f"Fecha del registro: {registration_date}"
            )

    action_rows = _tool_rows(
        trace,
        "consultar_acciones_comerciales",
    )

    if action_rows:
        row = action_rows[0]

        action = row.get("tipo_accion")
        action_state = row.get("estado")
        responsible = row.get("responsable")
        action_date = row.get("fecha_registro")
        evidence = row.get(
            "evidencia_producto"
        )

        if action is not None:
            lines.append(
                f"Acción comercial: {action}"
            )

        if action_state is not None:
            lines.append(
                f"Estado: {action_state}"
            )

        if responsible is not None:
            lines.append(
                f"Responsable: {responsible}"
            )

        if action_date is not None:
            lines.append(
                f"Fecha de acción: {action_date}"
            )

        if evidence is not None:
            lines.append(
                f"Evidencia: {evidence}"
            )

    expiration_rows = _tool_rows(
        trace,
        "buscar_productos_proximos_a_vencer",
    )

    if expiration_rows and not detail_rows:
        lines.append(
            "Productos próximos a vencer:"
        )

        for row in expiration_rows:
            product = row.get("producto")
            days = row.get("dias_restantes")
            store = row.get("tienda")

            lines.append(
                f"- {product} | "
                f"Tienda: {store} | "
                f"Días restantes: {days}"
            )

    if not lines:
        return (
            "Las herramientas no devolvieron información "
            "suficiente para responder."
        )

    return "\n".join(lines)


def run_agent(
    question: str,
    *,
    max_steps: int = MAX_PASOS,
) -> AgentResult:
    """
    Ejecuta el bucle ReAct local.

    Ciclo:
    modelo -> acción -> observación -> modelo -> respuesta final.

    Incluye:
    - MAX_PASOS;
    - trazabilidad;
    - guardrail de cobertura;
    - guardrail de fidelidad;
    - prevención de llamadas repetidas;
    - corrección final sin tools.
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
            "content": SYSTEM_PROMPT,
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

    for step in range(
        1,
        max_steps + 1,
    ):
        try:
            model_response = chat_with_agent(
                messages
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
                    "No fue posible completar la consulta "
                    "por un error controlado del modelo."
                ),
                status="ERROR_MODELO",
                steps=step,
                model=last_model,
                trace=tuple(trace),
            )

        last_model = model_response.model

        tool_calls = model_response.tool_calls

        # =========================================================
        # EL MODELO INTENTA RESPONDER
        # =========================================================
        if not tool_calls:
            missing_tools = _missing_required_tools(
                clean_question,
                trace,
            )

            # -----------------------------------------------------
            # GUARDRAIL DE COBERTURA
            # -----------------------------------------------------
            if missing_tools:
                trace.append(
                    {
                        "step": step,
                        "type": "coverage_guardrail",
                        "missing_tools": list(
                            missing_tools
                        ),
                        "message": (
                            "El modelo intentó responder "
                            "sin consultar toda la evidencia."
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
                            "La respuesta anterior fue bloqueada "
                            "por el guardrail de cobertura. "
                            "La consulta requiere información que "
                            "todavía no fue obtenida. "
                            "Debes ejecutar mediante tool_calls las "
                            "siguientes herramientas faltantes: "
                            f"{', '.join(missing_tools)}. "
                            "No inventes resultados. "
                            "Después de recibir las observaciones, "
                            "recién puedes responder."
                        ),
                    }
                )

                continue

            final_response = (
                model_response.content
            )

            if not final_response:
                final_response = (
                    "El agente terminó sin producir "
                    "una respuesta."
                )

            violations = _validate_final_response(
                clean_question,
                final_response,
                trace,
            )

            # -----------------------------------------------------
            # GUARDRAIL DE FIDELIDAD
            # -----------------------------------------------------
            if violations:
                trace.append(
                    {
                        "step": step,
                        "type": "guardrail",
                        "violations": violations,
                    }
                )

                observed_states = (
                    _observed_states(trace)
                )

                observed_actions = (
                    _observed_action_types(trace)
                )

                correction_messages = (
                    messages
                    + [
                        model_response.message,
                        {
                            "role": "user",
                            "content": (
                                "CORRECCIÓN OBLIGATORIA "
                                "DE FIDELIDAD. "
                                "Ya dispones de todas las "
                                "observaciones necesarias. "
                                "NO vuelvas a llamar herramientas. "
                                "Reescribe únicamente la respuesta "
                                "final usando los datos que ya "
                                "están en el historial. "
                                f"Estados permitidos: "
                                f"{observed_states}. "
                                f"Acciones comerciales observadas: "
                                f"{observed_actions}. "
                                "No interpretes estados. "
                                "No inventes acciones. "
                                "Si existe DESCUENTO, escribe "
                                "DESCUENTO. "
                                "No afirmes que no existen cambios "
                                "de precio si fueron observados. "
                                "Los precios se expresan en Bs. "
                                "Incluye evidencia si fue solicitada."
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
                                "La segunda redacción "
                                "continuó violando "
                                "guardrails. Python "
                                "construyó una respuesta "
                                "segura desde observaciones."
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
                            "response": safe_response,
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

            # -----------------------------------------------------
            # RESPUESTA FINAL VÁLIDA
            # -----------------------------------------------------
            trace.append(
                {
                    "step": step,
                    "type": "final",
                    "response": final_response,
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

        # =========================================================
        # EL MODELO SOLICITA HERRAMIENTAS
        # =========================================================
        messages.append(
            model_response.message
        )

        for tool_call in tool_calls:
            function_data = tool_call.get(
                "function"
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
                            "Ollama devolvió una llamada "
                            "de herramienta inválida."
                        ),
                    }
                )

                continue

            tool_name = function_data.get(
                "name"
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
                            "La llamada no contiene un "
                            "nombre de herramienta válido."
                        ),
                    }
                )

                continue

            tool_name = tool_name.strip()

            try:
                arguments = _normalize_arguments(
                    function_data.get(
                        "arguments"
                    )
                )

            except ValueError as exc:
                trace.append(
                    {
                        "step": step,
                        "type": "error",
                        "tool": tool_name,
                        "message": str(exc),
                    }
                )

                observation = {
                    "error": str(exc),
                }

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

                continue

            arguments = _clean_arguments(
                arguments
            )

            call_key = _tool_call_key(
                tool_name,
                arguments,
            )

            # -----------------------------------------------------
            # EVITAR CONSULTA REPETIDA
            # -----------------------------------------------------
            if call_key in tool_cache:
                cached_result = (
                    tool_cache[call_key]
                )

                trace.append(
                    {
                        "step": step,
                        "type": (
                            "duplicate_tool_guardrail"
                        ),
                        "tool": tool_name,
                        "arguments": arguments,
                        "message": (
                            "La herramienta ya había "
                            "sido ejecutada con estos "
                            "argumentos. Se reutilizó "
                            "la observación existente."
                        ),
                    }
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_name": tool_name,
                        "content": json.dumps(
                            cached_result,
                            ensure_ascii=False,
                        ),
                    }
                )

                continue

            # -----------------------------------------------------
            # ACCIÓN
            # -----------------------------------------------------
            trace.append(
                {
                    "step": step,
                    "type": "action",
                    "tool": tool_name,
                    "arguments": arguments,
                }
            )

            # -----------------------------------------------------
            # EJECUCIÓN CONTROLADA
            # -----------------------------------------------------
            try:
                result = execute_agent_tool(
                    tool_name,
                    arguments,
                )

            except Exception as exc:
                result = {
                    "error": str(exc),
                }

            tool_cache[
                call_key
            ] = result

            # -----------------------------------------------------
            # OBSERVACIÓN
            # -----------------------------------------------------
            trace.append(
                {
                    "step": step,
                    "type": "observation",
                    "tool": tool_name,
                    "result": result,
                }
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False,
                    ),
                }
            )

    # =============================================================
    # MAX_PASOS
    # =============================================================
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
            "La consulta alcanzó el límite máximo "
            "de pasos sin obtener una respuesta final."
        ),
        status="LIMITE_PASOS",
        steps=max_steps,
        model=last_model,
        trace=tuple(trace),
    )