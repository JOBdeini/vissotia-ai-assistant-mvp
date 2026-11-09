"""Genera el índice Chroma del corpus público aprobado con Gemini Embeddings."""

from __future__ import annotations

import argparse
from pathlib import Path

from vissotia_assistant.config import PROJECT_ROOT, Settings
from vissotia_assistant.vectorstore import (
    create_rate_limited_gemini_embeddings,
    create_vector_store,
    load_processed_chunks,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data/processed/chunks.jsonl",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = Settings.from_env()
    documents = load_processed_chunks(args.input)

    if any(settings.chroma_directory.iterdir()) if settings.chroma_directory.exists() else False:
        raise RuntimeError(
            "El directorio Chroma ya contiene datos. Bórralo conscientemente antes de reconstruir "
            "el índice para evitar mezclar espacios vectoriales."
        )

    embeddings = create_rate_limited_gemini_embeddings(settings)
    store = create_vector_store(
        documents,
        embedding=embeddings,
        collection_name=settings.chroma_collection,
        persist_directory=settings.chroma_directory,
    )
    count = store._collection.count()
    print(f"Índice Chroma creado correctamente: {count} chunks")
    print(f"Modelo de embeddings: {settings.embedding_model}")
    print(f"Dimensiones: {settings.embedding_dimensions}")
    print(
        "Lotes: "
        f"{settings.embedding_batch_size} chunks con "
        f"{settings.embedding_batch_delay_seconds:g}s entre lotes"
    )
    print(f"Colección: {settings.chroma_collection}")


if __name__ == "__main__":
    main()
