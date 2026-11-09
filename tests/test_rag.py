from langchain_core.messages import AIMessage

from vissotia_assistant.rag import _message_text, _source_type_allowed


def test_message_text_extracts_text_blocks_without_extras() -> None:
    message = AIMessage(
        content=[{"type": "text", "text": "Respuesta pública", "extras": {"signature": "oculta"}}]
    )
    assert _message_text(message) == "Respuesta pública"


def test_message_text_accepts_plain_strings() -> None:
    assert _message_text(AIMessage(content="Respuesta")) == "Respuesta"


def test_external_sources_require_source_intent() -> None:
    assert not _source_type_allowed("¿Qué es Vissotia?", "official_external")
    assert _source_type_allowed("¿Qué fuentes de datos utiliza?", "official_external")
    assert _source_type_allowed("¿Qué aporta Catastro?", "official_external")


def test_synthetic_sources_require_example_intent() -> None:
    assert not _source_type_allowed("¿Qué es Vissotia?", "synthetic_example")
    assert _source_type_allowed("Muéstrame un ejemplo simulado", "synthetic_example")
