"""Carga, validación y segmentación reproducible del corpus público."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

REQUIRED_METADATA = {
    "document_id",
    "title",
    "source_type",
    "source_name",
    "source_url",
    "retrieved_at",
    "language",
    "audience",
    "scope",
    "status",
}
ALLOWED_SOURCE_TYPES = {
    "official_public",
    "official_external",
    "approved_public",
    "synthetic_example",
}
FRONT_MATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)
LOCAL_PATH_PATTERN = re.compile(r"/(?:Users|home|var|tmp)/[^\s)]+", re.IGNORECASE)
SECRET_PATTERN = re.compile(
    r"(?:AIza[0-9A-Za-z_-]{20,}|sk-[0-9A-Za-z_-]{20,}|(?:api[_-]?key|password|secret)\s*[:=]\s*\S+)",
    re.IGNORECASE,
)


class CorpusValidationError(ValueError):
    """Error de validación que identifica un documento público no indexable."""


def _scalar_metadata(value: Any) -> str | int | float | bool:
    """Normaliza metadatos al conjunto escalar aceptado por ChromaDB."""

    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple, set)):
        return "|".join(str(item) for item in value)
    return str(value)


def parse_markdown_document(path: Path) -> tuple[dict[str, Any], str]:
    """Separa el front matter YAML del contenido Markdown y lo valida."""

    raw = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_PATTERN.match(raw)
    if not match:
        raise CorpusValidationError(f"{path.name}: falta front matter YAML válido.")

    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise CorpusValidationError(f"{path.name}: el front matter debe ser un objeto.")

    missing = sorted(REQUIRED_METADATA - metadata.keys())
    if missing:
        raise CorpusValidationError(f"{path.name}: faltan metadatos: {', '.join(missing)}.")
    if metadata["status"] != "approved":
        raise CorpusValidationError(f"{path.name}: el documento no está aprobado.")
    if metadata["source_type"] not in ALLOWED_SOURCE_TYPES:
        raise CorpusValidationError(f"{path.name}: source_type no permitido.")

    body = match.group(2).strip()
    if not body:
        raise CorpusValidationError(f"{path.name}: el contenido está vacío.")
    if LOCAL_PATH_PATTERN.search(body):
        raise CorpusValidationError(f"{path.name}: contiene una ruta local no publicable.")
    if SECRET_PATTERN.search(raw):
        raise CorpusValidationError(f"{path.name}: posible secreto detectado.")

    return metadata, body


def discover_approved_sources(source_root: Path) -> list[Path]:
    """Devuelve los Markdown públicos en un orden estable."""

    return sorted(path for path in source_root.rglob("*.md") if path.is_file())


def _contextual_text(content: str, metadata: dict[str, Any]) -> str:
    headings = [
        str(metadata.get("header_1", "")).strip(),
        str(metadata.get("header_2", "")).strip(),
        str(metadata.get("header_3", "")).strip(),
    ]
    prefix = " > ".join(heading for heading in headings if heading)
    return f"{prefix}\n\n{content}" if prefix else content


def build_chunks(
    source_root: Path,
    *,
    chunk_size: int = 1_000,
    chunk_overlap: int = 150,
) -> list[Document]:
    """Construye chunks autocontenidos con identificadores deterministas."""

    if chunk_size < 200:
        raise ValueError("chunk_size debe ser al menos 200.")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap debe ser positivo y menor que chunk_size.")

    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "header_1"), ("##", "header_2"), ("###", "header_3")],
        strip_headers=True,
    )
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks: list[Document] = []
    seen_content_hashes: set[str] = set()

    for path in discover_approved_sources(source_root):
        base_metadata, body = parse_markdown_document(path)
        normalized_base = {key: _scalar_metadata(value) for key, value in base_metadata.items()}
        normalized_base["relative_path"] = path.relative_to(source_root).as_posix()

        sections = header_splitter.split_text(body)
        split_sections = recursive_splitter.split_documents(sections)

        for document in split_sections:
            content = _contextual_text(document.page_content.strip(), document.metadata)
            if not content:
                continue
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            if content_hash in seen_content_hashes:
                continue
            seen_content_hashes.add(content_hash)

            metadata = {**normalized_base}
            metadata.update(
                {key: _scalar_metadata(value) for key, value in document.metadata.items()}
            )
            metadata["content_hash"] = content_hash
            metadata["is_synthetic"] = metadata["source_type"] == "synthetic_example"
            metadata["contains_warning"] = any(
                term in content.casefold()
                for term in ("no constituye", "no sustituye", "límite", "advertencia")
            )
            if str(metadata.get("header_2", "")).startswith("Caso "):
                metadata["case_id"] = (
                    str(metadata["header_2"]).split(".", 1)[0].lower().replace(" ", "_")
                )

            chunks.append(Document(page_content=content, metadata=metadata))

    for index, document in enumerate(chunks):
        document.metadata["chunk_index"] = index
        document.metadata["chunk_id"] = (
            f"{document.metadata['document_id']}:{index:04d}:"
            f"{str(document.metadata['content_hash'])[:12]}"
        )

    if not chunks:
        raise CorpusValidationError("No se generó ningún chunk aprobado.")
    return chunks


def write_chunks_jsonl(chunks: Iterable[Document], destination: Path) -> int:
    """Escribe JSONL estable, legible y apto para auditoría pública."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with destination.open("w", encoding="utf-8") as output:
        for document in chunks:
            row = {"page_content": document.page_content, "metadata": document.metadata}
            output.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count
