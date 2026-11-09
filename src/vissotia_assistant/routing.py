"""Enrutamiento inicial, determinista y comprobable del grafo."""

from __future__ import annotations

import re

from langchain_core.messages import AIMessage, AnyMessage

from vissotia_assistant.state import Route

_RENTAL_PATTERNS = (
    r"\balquil(?:ar|er)\b",
    r"\brentabilidad\b.*\balquiler\b",
    r"\bcompra\b.*\balquiler\b",
)
_FLIP_PATTERNS = (
    r"\breform(?:ar|a)\b.*\bvend(?:er|o|erla)\b",
    r"\bcompra\b.*\breforma\b.*\bventa\b",
)
_PRIVATE_DATA_PATTERNS = (
    r"\bmis?\s+(?:inmuebles?|proyectos?|clientes?)\b",
    r"\b(?:inmuebles?|proyectos?|clientes?)\s+(?:que\s+)?tengo\b",
    r"\bmi\s+cuenta\b",
    r"\bdatos?\s+(?:guardados?|registrados?)\b",
)
_RAG_PATTERNS = (
    r"\bvissotia\b",
    r"\bcatastro\b",
    r"\bine\b",
    r"\beur[ií]bor\b",
    r"\bgoogle places\b",
    r"\bvaloraci[oó]n\b",
    r"\barquetipo\b",
    r"\banuncio\b",
    r"\bpropietari[oa]\b",
    r"\binversor\b",
)
_GENERAL_FULL_PATTERNS = (
    r"(?:hola|buenas|buenos días|buenas tardes|buenas noches)[.!¡ ]*",
    r"(?:gracias|muchas gracias)[.!¡ ]*",
    r"(?:adiós|hasta luego)[.!¡ ]*",
)
_FOLLOW_UP_PATTERNS = (
    r"s[ií]",
    r"vale",
    r"de acuerdo",
    r"contin[uú]a",
    r"sigue",
    r"cu[eé]ntame m[aá]s",
    r"expl[ií]camelo",
    r"y eso",
    r"por qu[eé]",
)
_BARE_CONFIRMATION_PATTERNS = (
    r"s[ií]",
    r"vale",
    r"de acuerdo",
)
_BARE_REFUSAL_PATTERNS = (
    r"no",
    r"no gracias",
)
_ONBOARDING_PATTERNS = (
    r"gu[ií]ame",
    r"paso a paso",
    r"c[oó]mo (?:empiezo|comienzo)",
    r"por d[oó]nde empiezo",
)


def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _fullmatches_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.fullmatch(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def classify_route(query: str) -> Route:
    """Clasifica intenciones claras sin enviar datos al modelo."""

    normalized = " ".join(query.strip().split())
    if not normalized:
        return "clarify"
    if _matches_any(normalized, _PRIVATE_DATA_PATTERNS):
        return "safe_response"
    if _matches_any(normalized, _FLIP_PATTERNS):
        return "renovate_sell_form"
    if _matches_any(normalized, _RENTAL_PATTERNS):
        return "rental_form"
    if _matches_any(normalized, _RAG_PATTERNS):
        return "rag"
    if _fullmatches_any(normalized, _GENERAL_FULL_PATTERNS):
        return "general"
    # Cualquier consulta sustantiva intenta primero el corpus. Si no existe
    # evidencia suficiente, el RAG responde de forma controlada.
    return "rag"


def is_bare_confirmation(query: str) -> bool:
    """Indica si la consulta solo confirma una propuesta anterior."""

    normalized = " ".join(query.strip().split())
    return _fullmatches_any(normalized, _BARE_CONFIRMATION_PATTERNS)


def is_bare_refusal(query: str) -> bool:
    """Indica si la consulta solo rechaza una propuesta anterior."""

    normalized = " ".join(query.strip().split())
    return _fullmatches_any(normalized, _BARE_REFUSAL_PATTERNS)


def contextualize_retrieval_query(
    query: str, messages: list[AnyMessage], profile: str | None = None
) -> str:
    """Añade el último contexto del asistente cuando la consulta es una continuación corta."""

    normalized = " ".join(query.strip().split())
    if _matches_any(normalized, _ONBOARDING_PATTERNS):
        profile_context = {
            "professional": "profesional inmobiliario o agencia",
            "owner": "propietario vendedor",
            "investor": "inversor inmobiliario",
        }.get(profile or "", "usuario")
        return (
            f"{normalized}. Guía conceptual de inicio y onboarding paso a paso en Vissotia "
            f"para {profile_context}: definir objetivo, reunir información, completar contexto, "
            "revisar valoración, explorar estrategia, preparar contenidos y hacer seguimiento."
        )
    if not _fullmatches_any(normalized, _FOLLOW_UP_PATTERNS):
        return normalized

    previous_answer = next(
        (
            message.content
            for message in reversed(messages)
            if isinstance(message, AIMessage) and isinstance(message.content, str)
        ),
        "",
    )
    if not previous_answer:
        return normalized

    paragraphs = [part.strip() for part in previous_answer.split("\n\n") if part.strip()]
    last_context = paragraphs[-1] if paragraphs else previous_answer[-500:]
    return f"{normalized}. Continúa la propuesta anterior: {last_context[-500:]}"
