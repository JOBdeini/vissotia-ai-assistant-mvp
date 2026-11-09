"""Prueba manual de recuperación sin invocar el modelo generativo."""

from __future__ import annotations

from vissotia_assistant.config import Settings
from vissotia_assistant.vectorstore import open_vector_store

QUERIES = (
    "¿Qué es Vissotia y qué problema resuelve?",
    "¿Catastro demuestra quién es el propietario de una vivienda?",
    "¿Cómo se crea un arquetipo de comprador sin perfilar personas reales?",
    "¿Puedes ver los inmuebles que tengo guardados?",
    "Quiero simular una compra para alquilar",
)


def main() -> None:
    settings = Settings.from_env()
    store = open_vector_store(settings=settings)

    for query in QUERIES:
        print(f"\nCONSULTA: {query}")
        for rank, (document, score) in enumerate(
            store.similarity_search_with_relevance_scores(query, k=settings.rag_top_k), start=1
        ):
            title = document.metadata.get("title", "")
            section = document.metadata.get("header_2") or document.metadata.get("header_1", "")
            document_id = document.metadata.get("document_id", "")
            print(f"{rank}. {score:.4f} | {document_id} | {title} | {section}")


if __name__ == "__main__":
    main()
