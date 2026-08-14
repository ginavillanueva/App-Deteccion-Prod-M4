"""Interfaz demostrativa de App Detección Prod - Agente + MCP."""

from __future__ import annotations

import asyncio
import html
import json
from urllib import error, request

import streamlit as st

from src.agent_mcp.agent import MAX_PASOS
from src.agent_mcp.agente_mcp import run_agent_mcp
from src.agent_mcp.cliente_mcp import discover_tools
from src.tool_calling.config import get_settings
from src.tool_calling.database import (
    DATABASE_PATH,
    initialize_database,
    table_counts,
)


# ================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ================================================================

st.set_page_config(
    page_title="App Detección Prod | Agente + MCP",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ================================================================
# ESTILOS
# ================================================================

st.markdown(
    """
    <style>
        .main > div {
            padding-top: 1.5rem;
        }

        .hero {
            padding: 1.4rem 1.6rem;
            border: 1px solid rgba(120, 120, 120, 0.25);
            border-radius: 18px;
            margin-bottom: 1.2rem;
            background:
                linear-gradient(
                    135deg,
                    rgba(15, 61, 115, 0.10),
                    rgba(0, 150, 136, 0.06)
                );
        }

        .hero-title {
            font-size: 2rem;
            font-weight: 750;
            margin-bottom: 0.25rem;
        }

        .hero-subtitle {
            font-size: 1rem;
            opacity: 0.8;
        }

        .status-card {
            border: 1px solid rgba(120, 120, 120, 0.24);
            border-radius: 14px;
            padding: 0.9rem 1rem;
            min-height: 105px;
        }

        .status-title {
            font-size: 0.85rem;
            opacity: 0.72;
            margin-bottom: 0.35rem;
        }

        .status-value {
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .status-detail {
            font-size: 0.78rem;
            opacity: 0.75;
        }

        .flow-box {
            border: 1px solid rgba(120, 120, 120, 0.25);
            border-radius: 12px;
            padding: 0.7rem;
            text-align: center;
            font-weight: 650;
            min-height: 85px;
        }

        .section-card {
            border: 1px solid rgba(120, 120, 120, 0.22);
            border-radius: 14px;
            padding: 1rem;
            margin-bottom: 0.8rem;
        }

        .small-note {
            font-size: 0.82rem;
            opacity: 0.72;
        }

        div[data-testid="stMetric"] {
            border: 1px solid rgba(120, 120, 120, 0.20);
            border-radius: 12px;
            padding: 0.7rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ================================================================
# FUNCIONES DE ESTADO
# ================================================================


def check_ollama() -> tuple[bool, str]:
    """Comprueba que Ollama esté respondiendo localmente."""
    settings = get_settings()

    try:
        base_url = settings.ollama_api_url.split(
            "/api/",
            maxsplit=1,
        )[0]

        tags_url = (
            base_url.rstrip("/")
            + "/api/tags"
        )

        http_request = request.Request(
            tags_url,
            method="GET",
        )

        with request.urlopen(
            http_request,
            timeout=3,
        ) as response:
            if response.status == 200:
                return (
                    True,
                    settings.ollama_model,
                )

    except (
        error.URLError,
        error.HTTPError,
        TimeoutError,
        OSError,
    ) as exc:
        return (
            False,
            str(exc),
        )

    return (
        False,
        "Ollama no respondió correctamente.",
    )


@st.cache_data(
    ttl=15,
    show_spinner=False,
)
def load_system_status() -> dict:
    """Obtiene el estado general de la arquitectura."""
    settings = get_settings()

    ollama_ok, ollama_detail = (
        check_ollama()
    )

    try:
        initialize_database()

        counts = table_counts()

        database_ok = True
        database_error = ""

    except Exception as exc:
        counts = {}
        database_ok = False
        database_error = str(exc)

    try:
        discovered_tools = asyncio.run(
            discover_tools()
        )

        mcp_ok = (
            len(discovered_tools) > 0
        )

        mcp_error = ""

    except Exception as exc:
        discovered_tools = []
        mcp_ok = False
        mcp_error = str(exc)

    return {
        "ollama_ok": ollama_ok,
        "ollama_detail": ollama_detail,
        "model": settings.ollama_model,
        "mcp_ok": mcp_ok,
        "mcp_error": mcp_error,
        "tools": discovered_tools,
        "database_ok": database_ok,
        "database_error": database_error,
        "counts": counts,
        "database_path": str(
            DATABASE_PATH
        ),
    }


def status_card(
    title: str,
    ok: bool,
    value: str,
    detail: str,
) -> None:
    """Muestra una tarjeta de estado."""
    icon = "✅" if ok else "⚠️"

    safe_title = html.escape(title)
    safe_value = html.escape(value)
    safe_detail = html.escape(detail)

    st.markdown(
        f"""
        <div class="status-card">
            <div class="status-title">
                {safe_title}
            </div>
            <div class="status-value">
                {icon} {safe_value}
            </div>
            <div class="status-detail">
                {safe_detail}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ================================================================
# FUNCIONES DE PRESENTACIÓN DE TRAZA
# ================================================================


TRACE_LABELS = {
    "mcp_discovery":
        "🔌 Descubrimiento MCP",
    "action":
        "▶️ Acción",
    "observation":
        "📥 Observación",
    "coverage_guardrail":
        "🛡️ Guardrail de cobertura",
    "guardrail":
        "🛡️ Guardrail de fidelidad",
    "guardrail_fallback":
        "🔒 Fallback seguro",
    "duplicate_tool_guardrail":
        "♻️ Tool reutilizada",
    "final_rewrite":
        "✍️ Reescritura final",
    "final":
        "✅ Respuesta final",
    "error":
        "❌ Error",
    "limit":
        "⛔ Límite de pasos",
}


def event_title(
    event: dict,
) -> str:
    """Construye el título visual de un evento."""
    event_type = event.get(
        "type",
        "evento",
    )

    label = TRACE_LABELS.get(
        event_type,
        f"• {event_type}",
    )

    step = event.get(
        "step",
        "?",
    )

    tool = event.get(
        "tool",
    )

    if tool:
        return (
            f"Paso {step} · "
            f"{label} · {tool}"
        )

    return (
        f"Paso {step} · {label}"
    )


def render_trace_event(
    event: dict,
) -> None:
    """Renderiza un evento de la traza ReAct/MCP."""
    event_type = event.get(
        "type",
        "",
    )

    expanded = event_type in {
        "mcp_discovery",
        "action",
        "coverage_guardrail",
        "guardrail",
        "guardrail_fallback",
        "final",
    }

    with st.expander(
        event_title(event),
        expanded=expanded,
    ):
        if event_type == "mcp_discovery":
            st.write(
                "**Transporte:**",
                event.get(
                    "transport",
                    "N/A",
                ),
            )

            st.write(
                "**Operación:**",
                event.get(
                    "operation",
                    "N/A",
                ),
            )

            st.write(
                "**Tools descubiertas:**"
            )

            tools = event.get(
                "tools",
                [],
            )

            if tools:
                st.code(
                    "\n".join(
                        f"• {tool}"
                        for tool in tools
                    ),
                    language="text",
                )

        elif event_type == "action":
            st.write(
                "**Herramienta:**",
                event.get(
                    "tool",
                    "N/A",
                ),
            )

            st.write(
                "**Vía:**",
                event.get(
                    "via",
                    "LOCAL",
                ),
            )

            st.write(
                "**Operación:**",
                event.get(
                    "operation",
                    "N/A",
                ),
            )

            st.write(
                "**Argumentos:**"
            )

            st.json(
                event.get(
                    "arguments",
                    {},
                )
            )

        elif event_type == "observation":
            result = event.get(
                "result",
                {},
            )

            st.write(
                "**Vía:**",
                event.get(
                    "via",
                    "LOCAL",
                ),
            )

            st.write(
                "**Transporte:**",
                event.get(
                    "transport",
                    "N/A",
                ),
            )

            if isinstance(
                result,
                dict,
            ):
                source_tables = (
                    result.get(
                        "source_tables",
                        [],
                    )
                )

                row_count = result.get(
                    "row_count",
                )

                if source_tables:
                    st.write(
                        "**Fuente SQLite:**",
                        ", ".join(
                            source_tables
                        ),
                    )

                if row_count is not None:
                    st.write(
                        "**Registros:**",
                        row_count,
                    )

                rows = result.get(
                    "rows",
                    [],
                )

                if rows:
                    st.dataframe(
                        rows,
                        use_container_width=True,
                    )
                else:
                    st.json(result)
            else:
                st.write(result)

        elif event_type in {
            "coverage_guardrail",
            "guardrail",
        }:
            st.warning(
                event.get(
                    "message",
                    "El guardrail bloqueó "
                    "una respuesta.",
                )
            )

            missing_tools = (
                event.get(
                    "missing_tools",
                    [],
                )
            )

            if missing_tools:
                st.write(
                    "**Herramientas faltantes:**"
                )

                st.code(
                    "\n".join(
                        missing_tools
                    ),
                    language="text",
                )

            violations = event.get(
                "violations",
                [],
            )

            if violations:
                st.write(
                    "**Violaciones detectadas:**"
                )

                for violation in violations:
                    st.error(
                        violation
                    )

        elif event_type == (
            "guardrail_fallback"
        ):
            st.warning(
                event.get(
                    "message",
                    (
                        "Python construyó una "
                        "respuesta segura."
                    ),
                )
            )

            violations = event.get(
                "violations",
                [],
            )

            for violation in violations:
                st.write(
                    "•",
                    violation,
                )

        elif event_type == (
            "duplicate_tool_guardrail"
        ):
            st.info(
                event.get(
                    "message",
                    (
                        "Se reutilizó una "
                        "observación."
                    ),
                )
            )

            st.write(
                "**Tool:**",
                event.get(
                    "tool",
                    "N/A",
                ),
            )

            st.json(
                event.get(
                    "arguments",
                    {},
                )
            )

        elif event_type in {
            "final_rewrite",
            "final",
        }:
            st.success(
                "Respuesta validada."
            )

            response = event.get(
                "response",
                "",
            )

            if response:
                st.markdown(
                    response.replace(
                        "\n",
                        "  \n",
                    )
                )

        elif event_type == "error":
            st.error(
                event.get(
                    "message",
                    "Error no especificado.",
                )
            )

        elif event_type == "limit":
            st.error(
                event.get(
                    "message",
                    (
                        "Se alcanzó el límite "
                        "de pasos."
                    ),
                )
            )

        else:
            st.json(event)


def observation_events(
    trace: list[dict],
) -> list[dict]:
    """Obtiene únicamente observaciones."""
    return [
        event
        for event in trace
        if event.get("type")
        == "observation"
    ]


# ================================================================
# CABECERA
# ================================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            🤖 App Detección Prod — Agente + MCP
        </div>
        <div class="hero-subtitle">
            Demo técnica del agente ReAct conectado a un servidor MCP
            mediante stdio, con herramientas descubiertas dinámicamente,
            trazabilidad, guardrails y datos SQLite.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ================================================================
# SIDEBAR
# ================================================================

st.sidebar.title(
    "⚙️ Configuración"
)

st.sidebar.markdown(
    "**Arquitectura**"
)

st.sidebar.code(
    """
Usuario
  ↓
Agente ReAct
  ↓
Ollama
  ↓
Cliente MCP
  ↓
stdio / JSON-RPC
  ↓
Servidor MCP
  ↓
SQLite
""".strip(),
    language="text",
)

st.sidebar.markdown(
    "---"
)

st.sidebar.write(
    "**MAX_PASOS:**",
    MAX_PASOS,
)

st.sidebar.caption(
    "Los cambios de precio son "
    "informativos y de trazabilidad. "
    "El agente no aprueba ni modifica precios."
)


# ================================================================
# ESTADO DEL SISTEMA
# ================================================================

with st.spinner(
    "Verificando Ollama, MCP y SQLite..."
):
    system_status = (
        load_system_status()
    )

st.subheader(
    "Estado de la arquitectura"
)

status_columns = st.columns(4)

with status_columns[0]:
    status_card(
        "LLM local",
        system_status[
            "ollama_ok"
        ],
        (
            "Ollama activo"
            if system_status[
                "ollama_ok"
            ]
            else "Ollama no disponible"
        ),
        system_status[
            "model"
        ],
    )

with status_columns[1]:
    tool_count = len(
        system_status[
            "tools"
        ]
    )

    status_card(
        "Servidor MCP",
        system_status[
            "mcp_ok"
        ],
        (
            f"{tool_count} tools"
            if system_status[
                "mcp_ok"
            ]
            else "Sin conexión"
        ),
        (
            "stdio · initialize · tools/list"
            if system_status[
                "mcp_ok"
            ]
            else system_status[
                "mcp_error"
            ]
        ),
    )

with status_columns[2]:
    counts = system_status[
        "counts"
    ]

    total_records = sum(
        counts.values()
    ) if counts else 0

    status_card(
        "Base de datos",
        system_status[
            "database_ok"
        ],
        (
            f"{total_records} registros"
            if system_status[
                "database_ok"
            ]
            else "SQLite no disponible"
        ),
        (
            "tool_calling_demo.db"
            if system_status[
                "database_ok"
            ]
            else system_status[
                "database_error"
            ]
        ),
    )

with status_columns[3]:
    all_ok = (
        system_status[
            "ollama_ok"
        ]
        and system_status[
            "mcp_ok"
        ]
        and system_status[
            "database_ok"
        ]
    )

    status_card(
        "Demo",
        all_ok,
        (
            "Lista para ejecutar"
            if all_ok
            else "Revisar servicios"
        ),
        "Agente ReAct + MCP",
    )


# ================================================================
# FLUJO VISUAL
# ================================================================

st.markdown("---")

st.subheader(
    "Flujo de ejecución"
)

flow_columns = st.columns(6)

flow_data = (
    (
        "👤",
        "Usuario",
        "Consulta",
    ),
    (
        "🧠",
        "Agente ReAct",
        "Decide",
    ),
    (
        "🤖",
        "Ollama",
        "Tool calling",
    ),
    (
        "🔌",
        "Cliente MCP",
        "tools/list",
    ),
    (
        "🛠️",
        "Servidor MCP",
        "tools/call",
    ),
    (
        "🗄️",
        "SQLite",
        "Datos reales",
    ),
)

for column, data in zip(
    flow_columns,
    flow_data,
):
    icon, title, subtitle = data

    with column:
        st.markdown(
            f"""
            <div class="flow-box">
                <div style="font-size:1.4rem">
                    {icon}
                </div>
                <div>{title}</div>
                <div class="small-note">
                    {subtitle}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ================================================================
# CONSULTA
# ================================================================

st.markdown("---")

st.subheader(
    "Probar el agente"
)

example_questions = {
    "Multipaso completo":
        (
            "Revisa el producto Yogur natural 1 litro "
            "de la Sala 12. Dime cuántos días faltan "
            "para vencer, qué cantidad tiene y cuál es "
            "su precio actual. Además, dime si tuvo "
            "cambios de precio registrados y qué acción "
            "comercial tiene registrada, incluyendo su "
            "estado y evidencia."
        ),

    "Detalle de producto":
        (
            "Consulta el detalle del producto "
            "Yogur natural 1 litro."
        ),

    "Cambios de precio":
        (
            "Consulta los cambios de precio registrados "
            "para el producto Yogur natural 1 litro "
            "de la Sala 12."
        ),

    "Acción comercial":
        (
            "Consulta qué acción comercial tiene "
            "registrada el Yogur natural 1 litro "
            "de la Sala 12."
        ),

    "Próximos a vencer":
        (
            "¿Qué productos están próximos a vencer "
            "en los próximos 45 días?"
        ),
}

selected_example = st.selectbox(
    "Escenario de demostración",
    options=list(
        example_questions
    ),
)

question = st.text_area(
    "Consulta",
    value=example_questions[
        selected_example
    ],
    height=145,
)

button_columns = st.columns(
    [1, 1, 5]
)

with button_columns[0]:
    execute_button = st.button(
        "▶ Ejecutar agente",
        type="primary",
    )

with button_columns[1]:
    clear_button = st.button(
        "🧹 Limpiar",
    )


if (
    "last_agent_result"
    not in st.session_state
):
    st.session_state[
        "last_agent_result"
    ] = None


if clear_button:
    st.session_state[
        "last_agent_result"
    ] = None


if execute_button:
    if not question.strip():
        st.warning(
            "Escribe una consulta."
        )

    elif not all_ok:
        st.error(
            "La arquitectura no está completamente "
            "disponible. Revisa Ollama, MCP y SQLite."
        )

    else:
        with st.spinner(
            (
                "Ejecutando Agente + MCP... "
                "Ollama puede tardar algunos segundos."
            )
        ):
            try:
                result = run_agent_mcp(
                    question
                )

                st.session_state[
                    "last_agent_result"
                ] = {
                    "question":
                        result.question,
                    "status":
                        result.status,
                    "steps":
                        result.steps,
                    "model":
                        result.model,
                    "tools_used":
                        list(
                            result.tools_used
                        ),
                    "response":
                        result.response,
                    "trace":
                        list(
                            result.trace
                        ),
                }

            except Exception as exc:
                st.session_state[
                    "last_agent_result"
                ] = None

                st.error(
                    f"Error durante la ejecución: {exc}"
                )


# ================================================================
# RESULTADOS
# ================================================================

result_data = st.session_state[
    "last_agent_result"
]

if result_data is not None:
    st.markdown("---")

    st.header(
        "Resultado de la ejecución"
    )

    metric_columns = st.columns(4)

    with metric_columns[0]:
        st.metric(
            "Estado",
            result_data[
                "status"
            ],
        )

    with metric_columns[1]:
        st.metric(
            "Pasos",
            result_data[
                "steps"
            ],
        )

    with metric_columns[2]:
        st.metric(
            "Tools utilizadas",
            len(
                result_data[
                    "tools_used"
                ]
            ),
        )

    with metric_columns[3]:
        st.metric(
            "MAX_PASOS",
            MAX_PASOS,
        )

    st.subheader(
        "Respuesta final"
    )

    if (
        result_data[
            "status"
        ] == "OK"
    ):
        st.success(
            "Ejecución completada correctamente."
        )
    else:
        st.warning(
            (
                "La ejecución terminó con estado: "
                f"{result_data['status']}"
            )
        )

    st.markdown(
        result_data[
            "response"
        ].replace(
            "\n",
            "  \n",
        )
    )

    st.caption(
        (
            f"Modelo: "
            f"{result_data['model']}"
        )
    )

    tools_used = result_data[
        "tools_used"
    ]

    if tools_used:
        st.write(
            "**Herramientas utilizadas:**"
        )

        st.code(
            "\n".join(
                (
                    f"{index}. {tool}"
                    for index, tool
                    in enumerate(
                        tools_used,
                        start=1,
                    )
                )
            ),
            language="text",
        )

    # ------------------------------------------------------------
    # TABS
    # ------------------------------------------------------------

    (
        process_tab,
        tools_tab,
        observations_tab,
        json_tab,
        architecture_tab,
    ) = st.tabs(
        [
            "🧭 Proceso visual",
            "🛠️ Tools MCP",
            "🗄️ Observaciones",
            "🧾 Traza JSON",
            "🏗️ Arquitectura",
        ]
    )

    # ------------------------------------------------------------
    # PROCESO VISUAL
    # ------------------------------------------------------------

    with process_tab:
        st.subheader(
            "Traza ReAct + MCP"
        )

        st.caption(
            (
                "Cada evento muestra una decisión, "
                "ejecución, observación o control."
            )
        )

        trace = result_data[
            "trace"
        ]

        for event in trace:
            render_trace_event(
                event
            )

    # ------------------------------------------------------------
    # TOOLS MCP
    # ------------------------------------------------------------

    with tools_tab:
        st.subheader(
            "Herramientas descubiertas"
        )

        st.write(
            (
                "Estas herramientas provienen de "
                "`initialize → tools/list`."
            )
        )

        discovered_tools = (
            system_status[
                "tools"
            ]
        )

        st.metric(
            "Total publicado por MCP",
            len(
                discovered_tools
            ),
        )

        for index, tool in enumerate(
            discovered_tools,
            start=1,
        ):
            tool_name = tool.get(
                "name",
                f"Tool {index}",
            )

            with st.expander(
                (
                    f"{index}. "
                    f"{tool_name}"
                )
            ):
                description = tool.get(
                    "description",
                    "",
                )

                if description:
                    st.write(
                        description
                    )

                schema = tool.get(
                    "inputSchema",
                    tool.get(
                        "input_schema",
                        {},
                    ),
                )

                st.write(
                    "**Input schema**"
                )

                st.json(schema)

    # ------------------------------------------------------------
    # OBSERVACIONES
    # ------------------------------------------------------------

    with observations_tab:
        st.subheader(
            "Datos obtenidos mediante MCP"
        )

        observations = (
            observation_events(
                result_data[
                    "trace"
                ]
            )
        )

        if not observations:
            st.info(
                "No se registraron observaciones."
            )

        for observation in observations:
            tool_name = observation.get(
                "tool",
                "Tool",
            )

            with st.expander(
                (
                    "📥 "
                    f"{tool_name}"
                ),
                expanded=True,
            ):
                result = observation.get(
                    "result",
                    {},
                )

                if isinstance(
                    result,
                    dict,
                ):
                    st.write(
                        "**Fuente:**",
                        ", ".join(
                            result.get(
                                "source_tables",
                                [],
                            )
                        )
                        or "N/A",
                    )

                    st.write(
                        "**Registros:**",
                        result.get(
                            "row_count",
                            "N/A",
                        ),
                    )

                    rows = result.get(
                        "rows",
                        [],
                    )

                    if rows:
                        st.dataframe(
                            rows,
                            use_container_width=True,
                        )
                    else:
                        st.json(
                            result
                        )

    # ------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------

    with json_tab:
        st.subheader(
            "Traza técnica completa"
        )

        st.caption(
            (
                "Esta vista sirve como evidencia "
                "técnica y de auditoría."
            )
        )

        st.json(
            result_data[
                "trace"
            ]
        )

        trace_json = json.dumps(
            result_data[
                "trace"
            ],
            indent=2,
            ensure_ascii=False,
        )

        st.download_button(
            "⬇ Descargar traza JSON",
            data=trace_json,
            file_name=(
                "traza_agente_mcp.json"
            ),
            mime="application/json",
        )

    # ------------------------------------------------------------
    # ARQUITECTURA
    # ------------------------------------------------------------

    with architecture_tab:
        st.subheader(
            "Arquitectura demostrada"
        )

        st.code(
            """
┌───────────────────────────────┐
│            USUARIO            │
└───────────────┬───────────────┘
                │ consulta
                ▼
┌───────────────────────────────┐
│       AGENTE ReAct            │
│       MAX_PASOS = 6           │
│       Guardrails              │
└───────────────┬───────────────┘
                │ messages + tools
                ▼
┌───────────────────────────────┐
│            OLLAMA             │
│       Tool Calling            │
└───────────────┬───────────────┘
                │ tool_calls
                ▼
┌───────────────────────────────┐
│         CLIENTE MCP           │
│ initialize → tools/list       │
│ tools/call                    │
└───────────────┬───────────────┘
                │ stdio
                │ JSON-RPC
                ▼
┌───────────────────────────────┐
│         SERVIDOR MCP          │
│          FastMCP              │
│         @mcp.tool()           │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        TOOLS DE DOMINIO       │
│ vencimientos                  │
│ detalle                       │
│ cambios de precio             │
│ acciones comerciales          │
└───────────────┬───────────────┘
                │ SQL
                ▼
┌───────────────────────────────┐
│            SQLITE             │
│   fuente de datos real demo   │
└───────────────────────────────┘
""".strip(),
            language="text",
        )

        st.markdown(
            """
            **Responsabilidades**

            - **Ollama:** decide qué herramientas necesita.
            - **Agente:** mantiene el ciclo ReAct y aplica guardrails.
            - **Cliente MCP:** descubre e invoca herramientas.
            - **Servidor MCP:** publica capacidades mediante `stdio`.
            - **Python:** controla ejecución, validación y trazabilidad.
            - **SQLite:** es la fuente de datos de la demostración.
            """
        )


# ================================================================
# INFORMACIÓN TÉCNICA INFERIOR
# ================================================================

st.markdown("---")

with st.expander(
    "ℹ️ Información técnica del entorno"
):
    st.write(
        "**Modelo Ollama:**",
        system_status[
            "model"
        ],
    )

    st.write(
        "**Base SQLite:**",
        system_status[
            "database_path"
        ],
    )

    st.write(
        "**Registros por tabla:**"
    )

    st.json(
        system_status[
            "counts"
        ]
    )

    st.write(
        "**Transporte MCP:** stdio"
    )

    st.write(
        "**Flujo MCP:** "
        "initialize → tools/list → tools/call"
    )

    st.write(
        "**Política de precios:** "
        "consulta/notificación y trazabilidad; "
        "sin aprobación ni modificación automática."
    )