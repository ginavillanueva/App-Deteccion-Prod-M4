"""Catálogo controlado de frases para seleccionar herramientas sin IA."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from .tools import (
    LISTAR_ACCIONES_COMERCIALES_PENDIENTES,
    LISTAR_CAMBIOS_PRECIO_PENDIENTES,
    LISTAR_PRODUCTOS_PROXIMOS_A_VENCER,
)


@dataclass(frozen=True)
class KeywordMatch:
    """Coincidencia encontrada directamente en el catálogo."""

    tool_name: str
    matched_phrase: str
    path: str = "KEYWORD"


KEYWORD_CATALOG: dict[str, tuple[str, ...]] = {
    LISTAR_PRODUCTOS_PROXIMOS_A_VENCER: (
        "productos próximos a vencer",
        "producto próximo a vencer",
        "próximos a vencer",
    ),
    LISTAR_CAMBIOS_PRECIO_PENDIENTES: (
        "cambios de precio pendientes",
        "cambio de precio pendiente",
        "precios pendientes de aprobación",
    ),
    LISTAR_ACCIONES_COMERCIALES_PENDIENTES: (
        "acciones comerciales pendientes",
        "acción comercial pendiente",
        "descuentos pendientes",
        "bandeos pendientes",
    ),
}


def normalize_text(value: str) -> str:
    """
    Normaliza un texto para comparar palabras sin depender de mayúsculas,
    acentos, signos de interrogación o espacios repetidos.
    """
    decomposed = unicodedata.normalize("NFD", value.lower())

    without_accents = "".join(
        character
        for character in decomposed
        if unicodedata.category(character) != "Mn"
    )

    only_words = re.sub(
        r"[^a-z0-9ñ]+",
        " ",
        without_accents,
    )

    return " ".join(only_words.split())


def match_keyword(question: str) -> KeywordMatch | None:
    """
    Busca una frase controlada dentro de la pregunta.

    Cuando existe coincidencia, devuelve la herramienta correspondiente
    sin necesidad de invocar al modelo.
    """
    normalized_question = normalize_text(question)

    for tool_name, phrases in KEYWORD_CATALOG.items():
        normalized_phrases = sorted(
            (
                normalize_text(phrase)
                for phrase in phrases
            ),
            key=len,
            reverse=True,
        )

        for phrase in normalized_phrases:
            if phrase in normalized_question:
                return KeywordMatch(
                    tool_name=tool_name,
                    matched_phrase=phrase,
                )

    return None


def controlled_examples() -> dict[str, str]:
    """Devuelve una pregunta controlada de ejemplo por herramienta."""
    return {
        LISTAR_PRODUCTOS_PROXIMOS_A_VENCER:
            "¿Qué productos están próximos a vencer?",

        LISTAR_CAMBIOS_PRECIO_PENDIENTES:
            "¿Qué cambios de precio están pendientes?",

        LISTAR_ACCIONES_COMERCIALES_PENDIENTES:
            "¿Qué acciones comerciales están pendientes?",
    }