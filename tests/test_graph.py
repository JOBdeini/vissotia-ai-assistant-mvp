from langchain_core.messages import AIMessage, HumanMessage

from vissotia_assistant.graph import build_graph


def test_graph_routes_to_rental_form() -> None:
    graph = build_graph()
    result = graph.invoke(
        {
            "messages": [HumanMessage(content="Quiero simular un alquiler")],
            "query": "Quiero simular una compra para alquilar",
            "user_profile": "investor",
        },
        {"configurable": {"thread_id": "test-rental"}},
    )
    assert result["route"] == "rental_form"
    assert result["ui_action"] == "open_rental_form"


def test_graph_blocks_private_account_request() -> None:
    graph = build_graph()
    result = graph.invoke(
        {
            "messages": [HumanMessage(content="¿Qué inmuebles tengo guardados?")],
            "query": "¿Qué inmuebles tengo guardados?",
            "user_profile": "professional",
        },
        {"configurable": {"thread_id": "test-private"}},
    )
    assert result["route"] == "safe_response"
    assert "no está conectado" in result["answer"]


def test_graph_requires_profile() -> None:
    graph = build_graph()
    result = graph.invoke(
        {"messages": [], "query": "¿Qué es Vissotia?"},
        {"configurable": {"thread_id": "test-profile"}},
    )
    assert result["route"] == "clarify"
    assert "Selecciona primero" in result["answer"]


def test_graph_clarifies_isolated_confirmation_without_sources() -> None:
    graph = build_graph()
    result = graph.invoke(
        {
            "messages": [HumanMessage(content="Sí")],
            "query": "Sí",
            "user_profile": "owner",
        },
        {"configurable": {"thread_id": "test-isolated-yes"}},
    )

    assert result["route"] == "clarify"
    assert "No tengo una pregunta" in result["answer"]
    assert result["sources"] == []
    assert result["ui_action"] is None


def test_graph_clarifies_isolated_refusal_without_sources() -> None:
    graph = build_graph()
    result = graph.invoke(
        {
            "messages": [HumanMessage(content="No")],
            "query": "No",
            "user_profile": "owner",
        },
        {"configurable": {"thread_id": "test-isolated-no"}},
    )

    assert result["route"] == "clarify"
    assert "No tengo una pregunta" in result["answer"]
    assert result["sources"] == []


def test_graph_handles_contextual_refusal_without_rag_sources() -> None:
    graph = build_graph()
    result = graph.invoke(
        {
            "messages": [
                AIMessage(content="¿Quieres que continúe?"),
                HumanMessage(content="No"),
            ],
            "query": "No",
            "user_profile": "owner",
        },
        {"configurable": {"thread_id": "test-contextual-no"}},
    )

    assert result["route"] == "clarify"
    assert result["answer"].startswith("Entendido")
    assert result["sources"] == []
