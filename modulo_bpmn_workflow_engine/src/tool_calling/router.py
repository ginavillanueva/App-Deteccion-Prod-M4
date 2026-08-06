"""Enrutador principal para seleccionar y ejecutar herramientas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .catalog import match_keyword
from .config import get_settings
from .ollama_tool_selector import (
    OllamaToolSelectorError,
    select_tool_with_llm,
)
from .tools import ToolExecution, execute_tool


@dataclass(frozen=True)
class RouteResult:
    """Resultado completo y auditable del enrutamiento."""

    question: str
    path: str
    ia_habilitada: bool
    llm_invoked: bool
    model: str | None
    tool_name: str | None
    source_tables: tuple[str, ...]
    rows: tuple[dict[str, Any], ...]
    status: str
    message: str
    matched_phrase: str | None = None
    llm_raw_content: str = ""

    @property
    def row_count(self) -> int:
        """Cantidad de filas recuperadas desde SQLite."""
        return len(self.rows)

    @property
    def source_label(self) -> str:
        """Tablas consultadas durante la ejecución."""
        if not self.source_tables:
            return "N/A"

        return ", ".join(self.source_tables)

    @property
    def out_of_scope(self) -> bool:
        """Indica que ninguna herramienta puede responder."""
        return self.status == "FUERA_DE_ALCANCE"

    @property
    def successful(self) -> bool:
        """Indica que una herramienta fue ejecutada correctamente."""
        return self.status == "OK"


def build_success_result(
    *,
    question: str,
    path: str,
    ia_habilitada: bool,
    llm_invoked: bool,
    model: str | None,
    execution: ToolExecution,
    matched_phrase: str | None = None,
    llm_raw_content: str = "",
) -> RouteResult:
    """Construye el resultado de una herramienta ejecutada."""
    return RouteResult(
        question=question,
        path=path,
        ia_habilitada=ia_habilitada,
        llm_invoked=llm_invoked,
        model=model,
        tool_name=execution.tool_name,
        source_tables=execution.source_tables,
        rows=execution.rows,
        status="OK",
        message="Herramienta ejecutada correctamente.",
        matched_phrase=matched_phrase,
        llm_raw_content=llm_raw_content,
    )


def route_question(question: str) -> RouteResult:
    """
    Selecciona y ejecuta una herramienta para una pregunta.

    Orden del proceso:
    1. Busca coincidencias en el catálogo controlado.
    2. Si no existe coincidencia y la IA está habilitada,
       solicita al LLM que seleccione una herramienta.
    3. Ejecuta la herramienta autorizada desde Python.
    4. Si ninguna herramienta aplica, devuelve un resultado controlado.
    """
    clean_question = question.strip()
    settings = get_settings()

    if not clean_question:
        return RouteResult(
            question=question,
            path="VALIDATION",
            ia_habilitada=settings.ia_habilitada,
            llm_invoked=False,
            model=None,
            tool_name=None,
            source_tables=(),
            rows=(),
            status="PREGUNTA_INVALIDA",
            message="La pregunta no puede estar vacía.",
        )

    keyword_match = match_keyword(clean_question)

    if keyword_match is not None:
        execution = execute_tool(keyword_match.tool_name)

        return build_success_result(
            question=clean_question,
            path="KEYWORD",
            ia_habilitada=settings.ia_habilitada,
            llm_invoked=False,
            model=None,
            execution=execution,
            matched_phrase=keyword_match.matched_phrase,
        )

    if not settings.ia_habilitada:
        return RouteResult(
            question=clean_question,
            path="FALLBACK",
            ia_habilitada=False,
            llm_invoked=False,
            model=None,
            tool_name=None,
            source_tables=(),
            rows=(),
            status="IA_DESHABILITADA",
            message=(
                "No puedo identificar una herramienta para esa pregunta "
                "porque la IA está deshabilitada y no existe una "
                "coincidencia en el catálogo controlado."
            ),
        )

    try:
        llm_selection = select_tool_with_llm(clean_question)

    except OllamaToolSelectorError as exc:
        return RouteResult(
            question=clean_question,
            path="LLM_ERROR",
            ia_habilitada=True,
            llm_invoked=True,
            model=settings.ollama_model,
            tool_name=None,
            source_tables=(),
            rows=(),
            status="ERROR_CONTROLADO",
            message=str(exc),
        )

    if llm_selection.out_of_scope:
        return RouteResult(
            question=clean_question,
            path="LLM",
            ia_habilitada=True,
            llm_invoked=True,
            model=llm_selection.model,
            tool_name=None,
            source_tables=(),
            rows=(),
            status="FUERA_DE_ALCANCE",
            message=(
                "No puedo responder esa pregunta porque el dato no está "
                "disponible en App Detección Prod. "
                "Puedo consultar productos próximos a vencer, cambios "
                "de precio pendientes y acciones comerciales pendientes."
            ),
            llm_raw_content=llm_selection.raw_content,
        )

    if llm_selection.tool_name is None:
        return RouteResult(
            question=clean_question,
            path="LLM_ERROR",
            ia_habilitada=True,
            llm_invoked=True,
            model=llm_selection.model,
            tool_name=None,
            source_tables=(),
            rows=(),
            status="ERROR_CONTROLADO",
            message=(
                "El modelo no devolvió una selección de herramienta válida."
            ),
            llm_raw_content=llm_selection.raw_content,
        )

    execution = execute_tool(llm_selection.tool_name)

    return build_success_result(
        question=clean_question,
        path="LLM",
        ia_habilitada=True,
        llm_invoked=True,
        model=llm_selection.model,
        execution=execution,
        llm_raw_content=llm_selection.raw_content,
    )