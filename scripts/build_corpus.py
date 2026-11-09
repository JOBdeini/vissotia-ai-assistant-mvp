"""Genera el corpus procesado que se utilizará para embeddings."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from vissotia_assistant.config import PROJECT_ROOT
from vissotia_assistant.corpus import build_chunks, write_chunks_jsonl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=PROJECT_ROOT / "data/public_sources",
        help="Directorio con los Markdown aprobados.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "data/processed/chunks.jsonl",
        help="Archivo JSONL de salida.",
    )
    parser.add_argument("--chunk-size", type=int, default=1_000)
    parser.add_argument("--chunk-overlap", type=int, default=150)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    chunks = build_chunks(
        args.source,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
    count = write_chunks_jsonl(chunks, args.output)
    by_document = Counter(str(chunk.metadata["document_id"]) for chunk in chunks)

    print(f"Corpus procesado: {count} chunks")
    for document_id, document_count in sorted(by_document.items()):
        print(f"- {document_id}: {document_count}")
    print(f"Salida: {args.output}")


if __name__ == "__main__":
    main()
