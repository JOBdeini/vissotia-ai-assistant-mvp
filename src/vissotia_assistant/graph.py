"""StateGraph explícito del MVP.

Los nodos de RAG y generación se completarán al construir el índice. El grafo ya
define las rutas, el estado y la memoria temporal para que puedan probarse sin API.
"""

from __future__ import annotations

from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from vissotia_assistant.rag import RagService
from vissotia_assistant.routing import (
    classify_route,
    contextualize_retrieval_query,
    is_bare_confirmation,
    is_bare_refusal,
)
from vissotia_assistant.state import AgentState, Route


def validate_input(state: AgentState) -> dict:
    query = str(state.get("query", "")).strip()
    profile = state.get("user_profile")
    if profile not in {"professional", "owner", "investor"}:
        return {
            "route": "clarify",
            "safety_reason": "missing_profile",
            "query": query,
        }
    return {"query": query}


def route_request(state: AgentState) -> dict:
    if state.get("safety_reason") == "missing_profile":
        return {"route": "clarify"}
    query = state.get("query", "")
    has_previous_answer = any(
        isinstance(message, AIMessage) for message in state.get("messages", [])
    )
    if (is_bare_confirmation(query) or is_bare_refusal(query)) and not has_previous_answer:
        return {"route": "clarify", "safety_reason": "missing_conversation_context"}
    if is_bare_refusal(query):
        return {"route": "clarify", "safety_reason": "declined_suggestion"}

    route = classify_route(query)
    update = {"route": route}
    if route == "rag":
        update["retrieval_query"] = contextualize_retrieval_query(
            query, state.get("messages", []), state.get("user_profile")
        )
    return update


def route_after_classification(state: AgentState) -> Route:
    return state.get("route", "clarify")


def prepare_rental_form(_: AgentState) -> dict:
    answer = (
        "Puedo ayudarte con una simulación orientativa de compra para alquiler. "
        "Completa el formulario con cifras hipotéticas y sin datos personales."
    )
    return {
        "answer": answer,
        "ui_action": "open_rental_form",
        "sources": [],
        "retrieved_docs": [],
        "messages": [AIMessage(content=answer)],
    }


def prepare_renovate_sell_form(_: AgentState) -> dict:
    answer = (
        "Puedo preparar una simulación orientativa de compra, reforma y venta. "
        "Completa el formulario con supuestos hipotéticos y sin datos personales."
    )
    return {
        "answer": answer,
        "ui_action": "open_renovate_sell_form",
        "sources": [],
        "retrieved_docs": [],
        "messages": [AIMessage(content=answer)],
    }


def safe_response(_: AgentState) -> dict:
    answer = (
        "Este chat público no está conectado a cuentas, clientes, proyectos ni inmuebles "
        "registrados en Vissotia. Puedo explicarte el funcionamiento mediante un ejemplo simulado."
    )
    return {
        "answer": answer,
        "sources": [],
        "retrieved_docs": [],
        "ui_action": None,
        "messages": [AIMessage(content=answer)],
    }


def clarify_request(state: AgentState) -> dict:
    if state.get("safety_reason") == "missing_profile":
        answer = "Selecciona primero si eres profesional inmobiliario, propietario o inversor."
    elif state.get("safety_reason") == "missing_conversation_context":
        answer = (
            "No tengo una pregunta o propuesta anterior a la que aplicar esa respuesta. "
            "¿Qué te gustaría saber sobre Vissotia?"
        )
    elif state.get("safety_reason") == "declined_suggestion":
        answer = "Entendido. Si quieres consultar otro tema sobre Vissotia, dime cuál."
    else:
        answer = "¿Qué te gustaría conocer sobre Vissotia?"
    return {
        "answer": answer,
        "sources": [],
        "retrieved_docs": [],
        "ui_action": None,
        "messages": [AIMessage(content=answer)],
    }


def make_rag_node(rag_service: RagService | None):
    def rag_node(state: AgentState) -> dict:
        if rag_service is None:
            answer = "El servicio RAG no está configurado en este entorno."
            return {"answer": answer, "messages": [AIMessage(content=answer)]}

        result = rag_service.answer(
            query=state.get("query", ""),
            profile=state["user_profile"],
            history=state.get("messages", []),
            retrieval_query=state.get("retrieval_query"),
        )
        return {
            "answer": result.text,
            "sources": result.sources,
            "retrieved_docs": result.retrieved_docs,
            "ui_action": None,
            "messages": [AIMessage(content=result.text)],
        }

    return rag_node


def general_response(_: AgentState) -> dict:
    answer = (
        "Soy el Asistente Vissotia. Puedo explicar el producto, sus fuentes y casos de uso, "
        "o ayudarte con una simulación orientativa."
    )
    return {
        "answer": answer,
        "sources": [],
        "retrieved_docs": [],
        "ui_action": None,
        "messages": [AIMessage(content=answer)],
    }


def build_graph(
    checkpointer: InMemorySaver | None = None,
    rag_service: RagService | None = None,
):
    """Construye y compila el grafo con memoria exclusiva del proceso."""

    builder = StateGraph(AgentState)
    builder.add_node("validate_input", validate_input)
    builder.add_node("route_request", route_request)
    builder.add_node("rag", make_rag_node(rag_service))
    builder.add_node("rental_form", prepare_rental_form)
    builder.add_node("renovate_sell_form", prepare_renovate_sell_form)
    builder.add_node("safe_response", safe_response)
    builder.add_node("clarify", clarify_request)
    builder.add_node("general", general_response)

    builder.add_edge(START, "validate_input")
    builder.add_edge("validate_input", "route_request")
    builder.add_conditional_edges(
        "route_request",
        route_after_classification,
        {
            "rag": "rag",
            "rental_form": "rental_form",
            "renovate_sell_form": "renovate_sell_form",
            "safe_response": "safe_response",
            "clarify": "clarify",
            "general": "general",
        },
    )
    for node in (
        "rag",
        "rental_form",
        "renovate_sell_form",
        "safe_response",
        "clarify",
        "general",
    ):
        builder.add_edge(node, END)

    return builder.compile(checkpointer=checkpointer or InMemorySaver())
