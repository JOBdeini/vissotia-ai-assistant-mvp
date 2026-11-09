"""Configuración central del MVP sin incluir secretos en el repositorio."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True, slots=True)
class Settings:
    """Valores configurables de la aplicación."""

    gemini_api_key: str | None
    chat_model: str
    embedding_model: str
    embedding_dimensions: int
    embedding_batch_size: int
    embedding_batch_delay_seconds: float
    chroma_collection: str
    chroma_directory: Path
    rag_top_k: int

    @classmethod
    def from_env(cls) -> Settings:
        load_dotenv(PROJECT_ROOT / ".env", override=False)
        top_k_raw = os.getenv("RAG_TOP_K", "5")
        try:
            top_k = int(top_k_raw)
        except ValueError as exc:
            raise ValueError("RAG_TOP_K debe ser un número entero.") from exc
        if top_k < 1 or top_k > 20:
            raise ValueError("RAG_TOP_K debe estar entre 1 y 20.")

        dimensions_raw = os.getenv("GEMINI_EMBEDDING_DIMENSIONS", "768")
        try:
            dimensions = int(dimensions_raw)
        except ValueError as exc:
            raise ValueError("GEMINI_EMBEDDING_DIMENSIONS debe ser un número entero.") from exc
        if dimensions not in {768, 1536, 3072}:
            raise ValueError("GEMINI_EMBEDDING_DIMENSIONS debe ser 768, 1536 o 3072.")

        batch_size = int(os.getenv("EMBEDDING_BATCH_SIZE", "50"))
        batch_delay = float(os.getenv("EMBEDDING_BATCH_DELAY_SECONDS", "31"))
        if batch_size < 1 or batch_size > 100:
            raise ValueError("EMBEDDING_BATCH_SIZE debe estar entre 1 y 100.")
        if batch_delay < 0 or batch_delay > 60:
            raise ValueError("EMBEDDING_BATCH_DELAY_SECONDS debe estar entre 0 y 60.")

        chroma_path = Path(os.getenv("CHROMA_DIRECTORY", "data/chroma"))
        if not chroma_path.is_absolute():
            chroma_path = PROJECT_ROOT / chroma_path

        return cls(
            gemini_api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"),
            chat_model=os.getenv("GEMINI_CHAT_MODEL", "gemini-3.5-flash-lite"),
            embedding_model=os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-2"),
            embedding_dimensions=dimensions,
            embedding_batch_size=batch_size,
            embedding_batch_delay_seconds=batch_delay,
            chroma_collection=os.getenv("CHROMA_COLLECTION", "vissotia_public_mvp"),
            chroma_directory=chroma_path,
            rag_top_k=top_k,
        )

    def require_api_key(self) -> str:
        """Devuelve la clave o falla con un mensaje que no revela secretos."""

        if not self.gemini_api_key:
            raise RuntimeError(
                "Falta GEMINI_API_KEY. Configúrala en .env local o en los secretos de Streamlit."
            )
        return self.gemini_api_key
