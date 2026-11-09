from pathlib import Path

import pytest

from vissotia_assistant.corpus import (
    CorpusValidationError,
    build_chunks,
    parse_markdown_document,
    write_chunks_jsonl,
)


def _write_source(path: Path, *, status: str = "approved", body: str | None = None) -> None:
    content = body or "# Documento de prueba\n\n## Sección\n\nContenido público suficiente."
    path.write_text(
        f"""---
document_id: test_document
title: Documento de prueba
source_type: approved_public
source_name: Prueba
source_url: https://example.com/
retrieved_at: 2026-11-08
language: es
audience: all
scope: product
status: {status}
---

{content}
""",
        encoding="utf-8",
    )


def test_build_chunks_preserves_metadata(tmp_path: Path) -> None:
    _write_source(tmp_path / "source.md")
    chunks = build_chunks(tmp_path, chunk_size=300, chunk_overlap=30)

    assert chunks
    first = chunks[0]
    assert first.metadata["document_id"] == "test_document"
    assert first.metadata["status"] == "approved"
    assert first.metadata["chunk_id"].startswith("test_document:")
    assert "Documento de prueba" in first.page_content


def test_rejects_unapproved_document(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    _write_source(source, status="draft_review")
    with pytest.raises(CorpusValidationError, match="no está aprobado"):
        parse_markdown_document(source)


def test_rejects_local_paths(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    _write_source(source, body="# Documento\n\nRuta /Users/persona/secreto.txt")
    with pytest.raises(CorpusValidationError, match="ruta local"):
        parse_markdown_document(source)


def test_rejects_possible_secret(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    _write_source(source, body="# Documento\n\napi_key=valor-no-publicable")
    with pytest.raises(CorpusValidationError, match="posible secreto"):
        parse_markdown_document(source)


def test_write_chunks_jsonl(tmp_path: Path) -> None:
    source_root = tmp_path / "sources"
    source_root.mkdir()
    _write_source(source_root / "source.md")
    chunks = build_chunks(source_root, chunk_size=300, chunk_overlap=30)
    destination = tmp_path / "processed/chunks.jsonl"

    count = write_chunks_jsonl(chunks, destination)

    assert count == len(chunks)
    assert destination.read_text(encoding="utf-8").count("\n") == count
