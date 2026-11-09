import pytest
from langchain_core.messages import AIMessage, HumanMessage

from vissotia_assistant.routing import (
    classify_route,
    contextualize_retrieval_query,
    is_bare_confirmation,
    is_bare_refusal,
)


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("Quiero simular una compra para alquilar", "rental_form"),
        ("Quiero calcular rentabilidad de alquiler", "rental_form"),
        ("Quiero comprar, reformar y vender", "renovate_sell_form"),
        ("¿Qué inmuebles tengo guardados?", "safe_response"),
        ("¿Qué es Vissotia?", "rag"),
        ("¿Qué aporta el Catastro?", "rag"),
        ("", "clarify"),
        ("Hola", "general"),
        ("Guíame paso a paso", "rag"),
        ("Dime cómo empiezo a trabajar con un inmueble que quiero vender", "rag"),
        ("¿Puedo generar textos para redes sociales o portales inmobiliarios?", "rag"),
        ("Sí", "rag"),
    ],
)
def test_classify_route(query: str, expected: str) -> None:
    assert classify_route(query) == expected


def test_contextualize_short_follow_up_uses_previous_assistant_question() -> None:
    messages = [
        HumanMessage(content="Dame información sobre Vissotia"),
        AIMessage(content="Vissotia organiza el contexto.\n\n¿Quieres que explique sus funciones?"),
        HumanMessage(content="Sí"),
    ]

    contextualized = contextualize_retrieval_query("Sí", messages)

    assert "Sí" in contextualized
    assert "funciones" in contextualized


def test_contextualize_substantive_query_does_not_modify_it() -> None:
    query = "¿Cómo genera contenidos para portales inmobiliarios?"
    assert contextualize_retrieval_query(query, []) == query


def test_contextualize_generic_onboarding_query_expands_it() -> None:
    expanded = contextualize_retrieval_query("Guíame paso a paso", [], "owner")
    assert "onboarding" in expanded
    assert "Vissotia" in expanded
    assert "propietario vendedor" in expanded
    assert "valoración" in expanded


@pytest.mark.parametrize("query", ["Sí", "si", "Vale", "De acuerdo"])
def test_bare_confirmation(query: str) -> None:
    assert is_bare_confirmation(query)


@pytest.mark.parametrize("query", ["No", "No gracias"])
def test_bare_refusal(query: str) -> None:
    assert is_bare_refusal(query)


def test_substantive_negative_response_is_not_bare_refusal() -> None:
    assert not is_bare_refusal("No, quiero saber cómo funciona el marketing")
