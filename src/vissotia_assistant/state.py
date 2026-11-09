"""Estado compartido por el StateGraph del Asistente Vissotia."""

from __future__ import annotations

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

UserProfile = Literal["professional", "owner", "investor"]
Route = Literal[
    "rag",
    "rental_form",
    "renovate_sell_form",
    "safe_response",
    "clarify",
    "general",
]


class SourceItem(TypedDict, total=False):
    title: str
    section: str
    url: str
    source_type: str


class AgentState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    user_profile: UserProfile
    query: str
    retrieval_query: str
    route: Route
    retrieved_docs: list[dict]
    answer: str
    sources: list[SourceItem]
    ui_action: str | None
    safety_reason: str | None
    topics_covered: list[str]
