import json
from pathlib import Path

import pytest
from langchain_core.embeddings import FakeEmbeddings

from vissotia_assistant.vectorstore import (
    RateLimitedEmbeddings,
    create_vector_store,
    load_processed_chunks,
    public_sources,
)


def _write_jsonl(path: Path) -> None:
    rows = [
        {
            "page_content": "Vissotia conecta datos y contexto.",
            "metadata": {
                "chunk_id": "doc:0001:abc",
                "document_id": "doc",
                "status": "approved",
                "title": "Qué es Vissotia",
                "header_2": "Descripción",
                "source_url": "https://vissotia.es/",
            },
        },
        {
            "page_content": "El Catastro no sustituye al Registro de la Propiedad.",
            "metadata": {
                "chunk_id": "doc:0002:def",
                "document_id": "doc",
                "status": "approved",
                "title": "Fuentes",
                "header_2": "Catastro",
                "source_url": "https://www.catastro.hacienda.gob.es/",
            },
        },
    ]
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8"
    )


def test_load_processed_chunks_and_create_store(tmp_path: Path) -> None:
    source = tmp_path / "chunks.jsonl"
    _write_jsonl(source)
    documents = load_processed_chunks(source)
    store = create_vector_store(
        documents,
        embedding=FakeEmbeddings(size=16),
        collection_name="test_collection",
        persist_directory=tmp_path / "chroma",
    )

    assert len(documents) == 2
    assert store._collection.count() == 2


def test_rejects_duplicate_chunk_ids(tmp_path: Path) -> None:
    source = tmp_path / "chunks.jsonl"
    _write_jsonl(source)
    rows = source.read_text(encoding="utf-8").splitlines()
    duplicate = json.loads(rows[1])
    duplicate["metadata"]["chunk_id"] = "doc:0001:abc"
    source.write_text(rows[0] + "\n" + json.dumps(duplicate) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="duplicado"):
        load_processed_chunks(source)


def test_public_sources_deduplicates_and_hides_internal_metadata(tmp_path: Path) -> None:
    source = tmp_path / "chunks.jsonl"
    _write_jsonl(source)
    documents = load_processed_chunks(source)
    sources = public_sources([documents[0], documents[0], documents[1]])

    assert len(sources) == 2
    assert set(sources[0]) == {"title", "section", "url"}


def test_rate_limited_embeddings_preserve_document_count() -> None:
    wrapper = RateLimitedEmbeddings(FakeEmbeddings(size=8), batch_size=2, delay_seconds=0)
    embeddings = wrapper.embed_documents(["uno", "dos", "tres", "cuatro", "cinco"])

    assert len(embeddings) == 5
    assert all(len(item) == 8 for item in embeddings)
