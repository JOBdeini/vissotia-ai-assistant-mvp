# Decisiones técnicas y evolución

Fecha: 8 de noviembre de 2026.

## Proveedores confirmados

### MVP académico

- Generación: Google Gemini mediante API.
- Embeddings: Google Gemini Embeddings.
- Orquestación: LangGraph/LangChain.
- Base vectorial: ChromaDB.
- Interfaz: Streamlit.
- Memoria: temporal por sesión.

Gemini es un requisito funcional del proyecto y será el único proveedor ejecutado y documentado en la entrega académica.

### Versión real de Vissotia

- Proveedor de generación previsto: OpenAI.
- API de referencia para una implementación nueva: Responses API.
- La elección concreta del modelo, el tratamiento de datos, la retención y los límites de uso se decidirán cuando se aborde la integración real.

Esta versión futura no forma parte del alcance del MVP.

## Desacoplamiento mínimo

El MVP mantendrá una frontera sencilla entre la aplicación y el proveedor de generación. La arquitectura conceptual será:

`Streamlit -> grafo/agente -> servicio RAG -> adaptador LLM`

El adaptador expondrá una interfaz interna estable para invocar el modelo. La implementación activa será Gemini. La futura implementación OpenAI podrá sustituir el adaptador sin reescribir:

- la interfaz de Streamlit;
- el estado y los nodos de LangGraph;
- las reglas de seguridad y alcance;
- la recuperación de documentos;
- las citas de fuentes;
- la lógica de perfil de usuario y llamadas a la acción.

Se evitará una abstracción excesiva: no es necesario instalar ni configurar el SDK de OpenAI en el MVP.

## Configuración y secretos

MVP:

- `LLM_PROVIDER=gemini` como configuración explícita o valor interno por defecto;
- `GEMINI_API_KEY` almacenada solo en secretos del despliegue;
- ningún secreto incluido en Git.

Evolución futura:

- `LLM_PROVIDER=openai`;
- `OPENAI_API_KEY` almacenada en el gestor de secretos del entorno real;
- configuración de modelo separada del código.

## Embeddings e índice vectorial

El proveedor de generación y el proveedor de embeddings son decisiones distintas.

El MVP utilizará Gemini Embeddings para cumplir el enunciado. Si la versión real cambia a embeddings de OpenAI, será obligatorio volver a generar todos los vectores y reconstruir la colección de ChromaDB: embeddings de proveedores o modelos distintos no deben mezclarse en un mismo índice.

Alternativas para la versión real:

1. Conservar Gemini Embeddings y cambiar solo el modelo generativo a OpenAI.
2. Migrar generación y embeddings a OpenAI, reconstruyendo completamente el índice.

La elección se aplaza hasta disponer de requisitos reales de calidad, privacidad, coste, latencia y operación.

## Memoria y estado

En el MVP, la memoria de conversación seguirá siendo temporal y residirá en la sesión de la aplicación/LangGraph. No se utilizará la persistencia propia del proveedor.

En la futura versión con OpenAI se estudiará si el estado se mantiene en infraestructura de Vissotia o mediante capacidades de la API. No se adoptará almacenamiento persistente por defecto sin definir antes la base jurídica, la información al usuario, los plazos de conservación y los controles de borrado.

## Criterio de migración

La migración futura se considerará correcta si las pruebas de comportamiento del agente —RAG, límites, fuentes, ejemplos simulados, memoria y adaptación por perfil— siguen funcionando al cambiar el adaptador, sin alterar el corpus ni la interfaz pública salvo decisión expresa.
