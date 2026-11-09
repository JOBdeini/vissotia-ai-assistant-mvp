"""Servicio RAG con Gemini, Chroma y citas públicas controladas."""

from __future__ import annotations

from dataclasses import dataclass

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from vissotia_assistant.config import Settings
from vissotia_assistant.state import SourceItem, UserProfile
from vissotia_assistant.vectorstore import open_vector_store, public_sources

PROFILE_INSTRUCTIONS: dict[UserProfile, str] = {
    "professional": (
        "Responde de forma directa y operativa. Puedes usar terminología inmobiliaria, "
        "pero diferencia claramente funcionalidad, beneficio y límite."
    ),
    "owner": (
        "Usa lenguaje cotidiano, define los términos y explica los pasos. No pidas dirección, "
        "referencia catastral, documentos ni datos personales."
    ),
    "investor": (
        "Separa datos, supuestos y conclusiones. Explica límites financieros de forma visible y "
        "no recomiendes comprar, vender, reformar, alquilar o financiar una operación real."
    ),
}

BASE_SYSTEM_PROMPT = """Eres el Asistente Vissotia, un asistente público y demostrativo.

Responde en español y utiliza únicamente el CONTEXTO PÚBLICO recuperado para realizar
afirmaciones sobre Vissotia, sus funciones, fuentes y límites.

Reglas obligatorias:
- No inventes funcionalidades, precios, planes, integraciones, plazos ni resultados.
- Si el contexto no responde suficientemente, dilo con claridad.
- No afirmes que puedes acceder a cuentas, clientes, proyectos o inmuebles reales.
- No solicites datos personales ni documentación de una operación real.
- Los ejemplos inmobiliarios deben identificarse como ejemplos simulados.
- No proporciones asesoramiento jurídico, fiscal, técnico, financiero o de inversión personalizado.
- No incluyas una bibliografía dentro del texto: la interfaz mostrará las fuentes por separado.
- No menciones IDs, puntuaciones, rutas locales, embeddings ni detalles internos del RAG.
- Responde primero a la pregunta y, solo si aporta valor, termina con una sugerencia breve.
- El perfil ya está seleccionado: adapta toda la respuesta a ese perfil, no vuelvas a
  preguntarlo y no sugieras recorridos ni opciones destinados a otro perfil.
- Si la consulta es una continuación breve, utiliza el historial y continúa directamente.
- No te presentes de nuevo en cada respuesta.
- No sustituyas una respuesta disponible por una descripción genérica de tus capacidades.
- Si el contexto contiene pasos útiles, explícalos sin afirmar que falta una guía completa.

INSTRUCCIÓN DE PERFIL:
{profile_instruction}

CONTEXTO PÚBLICO:
{context}
"""


@dataclass(frozen=True, slots=True)
class RagAnswer:
    text: str
    sources: list[SourceItem]
    retrieved_docs: list[dict]


def _message_text(message: AnyMessage) -> str:
    if isinstance(message.content, str):
        return message.content
    if isinstance(message.content, list):
        text_parts = []
        for block in message.content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(str(block.get("text", "")))
        return "\n".join(part for part in text_parts if part)
    return str(message.content)


def _source_type_allowed(query: str, source_type: str) -> bool:
    normalized = query.casefold()
    external_terms = ("fuente", "dato", "catastro", "ine", "google", "euríbor", "euribor")
    example_terms = ("ejemplo", "simula", "alquiler", "reforma", "caso")
    if source_type == "official_external":
        return any(term in normalized for term in external_terms)
    if source_type == "synthetic_example":
        return any(term in normalized for term in example_terms)
    return True


class RagService:
    """Recupera evidencia pública y genera una respuesta acotada."""

    def __init__(
        self,
        *,
        settings: Settings,
        relevance_threshold: float = 0.35,
    ) -> None:
        self.settings = settings
        self.store = open_vector_store(settings=settings)
        self.model = ChatGoogleGenerativeAI(
            model=settings.chat_model,
            api_key=settings.require_api_key(),
            temperature=0,
            max_retries=2,
        )
        self.relevance_threshold = relevance_threshold

    def retrieve(self, query: str) -> list[tuple[Document, float]]:
        results = self.store.similarity_search_with_relevance_scores(
            query, k=self.settings.rag_top_k
        )
        filtered = [
            (document, score)
            for document, score in results
            if score >= self.relevance_threshold
            and _source_type_allowed(query, str(document.metadata.get("source_type", "")))
        ]
        if not filtered:
            return []
        relative_floor = filtered[0][1] - 0.12
        return [(document, score) for document, score in filtered if score >= relative_floor][:4]

    def answer(
        self,
        *,
        query: str,
        profile: UserProfile,
        history: list[AnyMessage] | None = None,
        retrieval_query: str | None = None,
    ) -> RagAnswer:
        results = self.retrieve(retrieval_query or query)
        if not results:
            return RagAnswer(
                text=(
                    "No encuentro información pública suficiente para responder con seguridad. "
                    "Puedo ayudarte a reformular la consulta o indicarte cómo solicitar una demo."
                ),
                sources=[],
                retrieved_docs=[],
            )

        documents = [document for document, _ in results]
        context_blocks = []
        retrieved_docs = []
        for index, (document, score) in enumerate(results, start=1):
            title = str(document.metadata.get("title", "Fuente pública"))
            section = str(
                document.metadata.get("header_2") or document.metadata.get("header_1") or ""
            )
            context_blocks.append(
                f"[DOCUMENTO {index}]\nTítulo: {title}\nSección: {section}\n"
                f"Contenido:\n{document.page_content}"
            )
            retrieved_docs.append(
                {
                    "document_id": str(document.metadata.get("document_id", "")),
                    "title": title,
                    "section": section,
                    "score": round(float(score), 4),
                }
            )

        system_prompt = BASE_SYSTEM_PROMPT.format(
            profile_instruction=PROFILE_INSTRUCTIONS[profile],
            context="\n\n".join(context_blocks),
        )
        messages: list[AnyMessage] = [SystemMessage(content=system_prompt)]

        prior_messages = list(history or [])[-6:]
        for message in prior_messages:
            if isinstance(message, (HumanMessage, AIMessage)):
                messages.append(message)
        if not messages or not isinstance(messages[-1], HumanMessage):
            messages.append(HumanMessage(content=query))
        elif _message_text(messages[-1]).strip() != query.strip():
            messages.append(HumanMessage(content=query))

        response = self.model.invoke(messages)
        text = _message_text(response).strip()
        if not text:
            text = "No he podido generar una respuesta. Inténtalo de nuevo en unos instantes."

        return RagAnswer(
            text=text,
            sources=public_sources(documents),
            retrieved_docs=retrieved_docs,
        )
