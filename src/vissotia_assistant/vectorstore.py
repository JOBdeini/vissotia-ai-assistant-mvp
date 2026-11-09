"""Creación y consulta del índice Chroma con embeddings de Gemini."""

from __future__ import annotations

import json
import time
from collections.abc import Iterable
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from vissotia_assistant.config import Settings


class RateLimitedEmbeddings(Embeddings):
    """Divide embeddings documentales para respetar cuotas por minuto.

    Las consultas individuales se delegan sin espera. Esta envoltura se usa solo
    durante la construcción del índice en el plan gratuito de Gemini.
    """

    def __init__(self, base: Embeddings, *, batch_size: int, delay_seconds: float) -> None:
        self.base = base
        self.batch_size = batch_size
        self.delay_seconds = delay_seconds

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings: list[list[float]] = []
        batches = [
            texts[index : index + self.batch_size]
            for index in range(0, len(texts), self.batch_size)
        ]
        for index, batch in enumerate(batches):
            if index:
                time.sleep(self.delay_seconds)
            embeddings.extend(self.base.embed_documents(batch))
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        return self.base.embed_query(text)


def load_processed_chunks(path: Path) -> list[Document]:
    """Carga el JSONL auditado y valida identificadores imprescindibles."""

    if not path.is_file():
        raise FileNotFoundError(f"No existe el corpus procesado: {path}")

    documents: list[Document] = []
    seen_ids: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON inválido en la línea {line_number}.") from exc

        content = str(row.get("page_content", "")).strip()
        metadata = row.get("metadata")
        if not content or not isinstance(metadata, dict):
            raise ValueError(f"Chunk incompleto en la línea {line_number}.")
        chunk_id = str(metadata.get("chunk_id", "")).strip()
        if not chunk_id:
            raise ValueError(f"Falta chunk_id en la línea {line_number}.")
        if chunk_id in seen_ids:
            raise ValueError(f"chunk_id duplicado: {chunk_id}")
        if metadata.get("status") != "approved":
            raise ValueError(f"El chunk {chunk_id} no está aprobado.")

        seen_ids.add(chunk_id)
        documents.append(Document(page_content=content, metadata=metadata))

    if not documents:
        raise ValueError("El corpus procesado no contiene documentos.")
    return documents


def create_gemini_embeddings(settings: Settings) -> GoogleGenerativeAIEmbeddings:
    """Inicializa Gemini Embeddings sin registrar la clave."""

    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.require_api_key(),
        output_dimensionality=settings.embedding_dimensions,
    )


def create_rate_limited_gemini_embeddings(settings: Settings) -> RateLimitedEmbeddings:
    """Configura lotes compatibles con la cuota gratuita de embeddings."""

    return RateLimitedEmbeddings(
        create_gemini_embeddings(settings),
        batch_size=settings.embedding_batch_size,
        delay_seconds=settings.embedding_batch_delay_seconds,
    )


def create_vector_store(
    documents: list[Document],
    *,
    embedding: Embeddings,
    collection_name: str,
    persist_directory: Path,
) -> Chroma:
    """Crea una colección nueva a partir de chunks deterministas."""

    persist_directory.mkdir(parents=True, exist_ok=True)
    ids = [str(document.metadata["chunk_id"]) for document in documents]
    return Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        ids=ids,
        collection_name=collection_name,
        persist_directory=str(persist_directory),
    )


def open_vector_store(*, settings: Settings, embedding: Embeddings | None = None) -> Chroma:
    """Abre la colección persistida para recuperación."""

    return Chroma(
        collection_name=settings.chroma_collection,
        embedding_function=embedding or create_gemini_embeddings(settings),
        persist_directory=str(settings.chroma_directory),
    )


def public_sources(documents: Iterable[Document]) -> list[dict[str, str]]:
    """Extrae citas públicas deduplicadas sin rutas ni IDs internos."""

    result: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for document in documents:
        metadata = document.metadata
        item = (
            str(metadata.get("title", "Fuente pública")),
            str(metadata.get("header_2") or metadata.get("header_1") or ""),
            str(metadata.get("source_url", "")),
        )
        if item in seen:
            continue
        seen.add(item)
        result.append({"title": item[0], "section": item[1], "url": item[2]})
    return result
