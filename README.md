# Asistente Vissotia

![Asistente Qué es Vissotia: explicación para vender inmuebles con Gemini, RAG, LangGraph y Streamlit](docs/assets/github-social-preview.png)

MVP académico de un asistente público sobre Vissotia construido con Google Gemini, RAG,
ChromaDB, LangGraph y Streamlit.

El proyecto demuestra un pipeline completo de IA generativa: prepara una base documental
pública, genera embeddings, recupera contexto relevante, produce respuestas fundamentadas y
mantiene memoria temporal dentro de cada conversación.

## Estado del proyecto

El desarrollo funcional del MVP está completado y validado:

- 9 documentos públicos aprobados;
- 123 fragmentos indexados en ChromaDB;
- Gemini como LLM y modelo de embeddings;
- agente explícito en LangGraph con memoria temporal;
- interfaz Streamlit con tres perfiles;
- dos herramientas deterministas de simulación;
- notebook académico ejecutado de principio a fin;
- 50 pruebas automatizadas superadas;
- análisis estático sin errores.

El despliegue público en Streamlit Community Cloud se mantiene como una fase opcional posterior.

## Dominio y propósito

El Asistente Vissotia explica, mediante información pública:

- qué es Vissotia y qué problema ayuda a resolver;
- sus funcionalidades y beneficios comunicables;
- cómo conecta información, contexto, estrategia, contenidos y seguimiento;
- qué aportan fuentes como Catastro, INE, servicios de lugares y referencias del euríbor;
- cómo puede utilizarse mediante recorridos conceptuales y ejemplos simulados;
- cómo preparar borradores de marketing basados en un arquetipo de comprador no identificable.

La explicación se adapta a tres perfiles:

- profesional inmobiliario;
- propietario particular;
- inversor.

El perfil modifica el lenguaje y el nivel de detalle, pero no los hechos recuperados.

## Alcance y límites

El asistente puede:

- responder preguntas públicas sobre Vissotia mediante RAG;
- mostrar las fuentes utilizadas;
- mantener el contexto durante la sesión;
- explicar procesos paso a paso;
- mostrar ejemplos ficticios claramente identificados;
- calcular simulaciones orientativas de compra para alquiler y de compra, reforma y venta.

El asistente no puede:

- acceder a cuentas, clientes, proyectos o inmuebles reales;
- consultar bases de datos privadas de Vissotia;
- solicitar direcciones, referencias catastrales, documentos o datos personales;
- consultar Catastro, INE, Google Places o datos financieros en tiempo real;
- inventar precios, planes, integraciones o funcionalidades;
- emitir tasaciones o asesoramiento jurídico, fiscal, técnico, financiero o de inversión.

## Arquitectura

### Indexación

```text
Markdown público aprobado
        ↓
validación y limpieza
        ↓
chunking por encabezados + división recursiva
        ↓
Gemini Embeddings
        ↓
ChromaDB persistente
```

### Consulta

```text
pregunta + perfil + historial
        ↓
LangGraph: validación y enrutamiento
        ├── RAG + Gemini
        ├── respuesta segura
        ├── aclaración conversacional
        └── herramienta determinista
        ↓
respuesta + fuentes + memoria temporal
```

## Stack tecnológico

- Python 3.11–3.14.
- Google Gemini para generación.
- Gemini Embeddings con 768 dimensiones.
- ChromaDB mediante `langchain-chroma`.
- LangChain y LangGraph.
- Streamlit.
- Pydantic para validación de herramientas.
- Pytest y Ruff para calidad.
- `uv` como gestor recomendado.

## Instalación con `uv` — recomendada

Desde la raíz del proyecto:

```bash
uv sync --dev
cp .env.example .env
```

Añade la clave únicamente al archivo `.env` local:

```dotenv
GEMINI_API_KEY=tu_clave_local
```

El archivo `.env` está excluido de Git. No escribas la clave en el notebook, el código, las
capturas o los mensajes de commit.

## Instalación alternativa con `pip`

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

En Windows, la activación equivalente es:

```powershell
.venv\Scripts\activate
```

`pyproject.toml` es la fuente principal de dependencias y configuración. `requirements.txt`
mantiene versiones fijadas para instalaciones basadas en `pip` y futuros despliegues.

## Construcción del corpus y del índice

La primera ejecución requiere una clave de Gemini válida:

```bash
uv run python scripts/build_corpus.py
uv run python scripts/build_index.py
uv run python scripts/test_retrieval.py
```

Con `pip` y el entorno virtual activo:

```bash
python scripts/build_corpus.py
python scripts/build_index.py
python scripts/test_retrieval.py
```

El índice se guarda en `data/chroma/` y está excluido de Git. `build_index.py` se detiene si ya
existe un índice para evitar mezclar espacios vectoriales. Para reconstruirlo, conserva primero
una copia de seguridad de `data/chroma/` y ejecuta de nuevo los comandos anteriores.

## Notebook académico

El entregable principal es:

```text
notebooks/Asistente_Vissotia_Proyecto_Final.ipynb
```

Incluye:

- inspección y validación del corpus;
- estrategia de chunking;
- creación o carga de ChromaDB;
- evaluación previa del retriever;
- system prompt documentado;
- grafo LangGraph;
- función de chat;
- cinco preguntas con respuestas y fuentes;
- demostración explícita de memoria;
- casos sin información y fuera del dominio;
- dos simulaciones deterministas;
- conclusiones y limitaciones.

Para abrirlo en VS Code, selecciona como kernel el Python de `.venv`.

## Presentación

La presentación utilizada para exponer el proyecto está disponible en
[`docs/Presentacion_Asistente_Vissotia.pptx`](docs/Presentacion_Asistente_Vissotia.pptx).

## Ejecución de Streamlit

```bash
uv run streamlit run app.py
```

La aplicación estará normalmente disponible en:

```text
http://localhost:8501
```

Para detenerla, pulsa `Ctrl + C` en el terminal donde se está ejecutando.

## System prompt y justificación

El system prompt se encuentra en `src/vissotia_assistant/rag.py`. Se ha diseñado para:

1. limitar las afirmaciones sobre Vissotia al contexto público recuperado;
2. impedir la invención de precios, planes, integraciones, plazos o resultados;
3. declarar de forma transparente cuándo la información es insuficiente;
4. bloquear el acceso o la solicitud de información privada;
5. identificar los casos inmobiliarios como ejemplos simulados;
6. mantener separados respuesta y listado de fuentes;
7. adaptar el lenguaje al perfil seleccionado;
8. conservar coherencia en preguntas de seguimiento;
9. evitar repetir presentaciones y advertencias sin necesidad.

Gemini se configura con `temperature=0` para reducir la variabilidad en respuestas documentales.
La generación recibe los fragmentos recuperados dentro de un bloque delimitado de contexto y no
debe utilizar conocimiento general para completar afirmaciones no documentadas sobre Vissotia.

## Memoria conversacional

LangGraph utiliza `InMemorySaver` y un `thread_id` aleatorio por sesión.

- El historial se conserva durante la sesión activa.
- Conversaciones con identificadores diferentes permanecen separadas.
- «Nueva conversación» genera otro identificador.
- No se emplean cuentas, cookies persistentes, IP ni base de datos de conversaciones.
- La memoria desaparece al reiniciar el proceso.

## Herramientas deterministas

El MVP incorpora dos cálculos que no delegan la aritmética en Gemini:

1. compra para alquiler;
2. compra, reforma y venta.

Las entradas se validan con Pydantic. Los resultados muestran supuestos, conceptos incluidos y una
advertencia visible. No representan una valoración, previsión ni recomendación de inversión.

## Pruebas y calidad

```bash
uv run pytest
uv run ruff check .
```

Para probar manualmente la recuperación sin invocar al modelo generativo:

```bash
uv run python scripts/test_retrieval.py
```

Las pruebas cubren:

- validación y chunking del corpus;
- configuración del vector store;
- enrutamiento;
- memoria y respuestas breves con o sin contexto;
- límites de acceso a información privada;
- selección de fuentes;
- cálculos y validación de entradas.

## Estructura del repositorio

```text
.
├── app.py
├── notebooks/
│   └── Asistente_Vissotia_Proyecto_Final.ipynb
├── docs/
│   ├── assets/
│   │   └── github-social-preview.png
│   ├── project/              # Contexto, decisiones y especificaciones
│   └── Presentacion_Asistente_Vissotia.pptx
├── data/
│   ├── public_sources/       # Documentos públicos aprobados
│   ├── processed/            # Chunks auditables
│   └── chroma/               # Índice local, ignorado por Git
├── scripts/
│   ├── build_corpus.py
│   ├── build_index.py
│   └── test_retrieval.py
├── src/vissotia_assistant/
│   ├── calculators.py
│   ├── config.py
│   ├── corpus.py
│   ├── graph.py
│   ├── rag.py
│   ├── routing.py
│   ├── state.py
│   └── vectorstore.py
├── tests/
├── .env.example
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

## Seguridad y publicación

- El corpus no contiene documentación interna ni secretos industriales.
- `.env`, secretos de Streamlit, índices locales y cachés están excluidos de Git.
- Los documentos se validan antes de indexarse.
- Las fuentes públicas se conservan como metadatos legibles.
- No se publican rutas locales, IDs de Chroma, embeddings ni puntuaciones internas.
- Los ejemplos sintéticos no representan inmuebles ni clientes reales.

Antes de publicar el repositorio debe realizarse una última revisión del historial de Git, porque
añadir un archivo a `.gitignore` no elimina secretos que hubieran sido confirmados previamente.

## Variables de entorno

| Variable | Valor de ejemplo | Finalidad |
|---|---|---|
| `GEMINI_API_KEY` | sin valor | Clave local o secreto del despliegue |
| `GEMINI_CHAT_MODEL` | `gemini-3.5-flash-lite` | Modelo generativo |
| `GEMINI_EMBEDDING_MODEL` | `gemini-embedding-2` | Modelo de embeddings |
| `GEMINI_EMBEDDING_DIMENSIONS` | `768` | Dimensión de los vectores |
| `EMBEDDING_BATCH_SIZE` | `50` | Tamaño de lote durante la indexación |
| `EMBEDDING_BATCH_DELAY_SECONDS` | `31` | Pausa entre lotes |
| `CHROMA_COLLECTION` | `vissotia_public_mvp` | Nombre de la colección |
| `CHROMA_DIRECTORY` | `data/chroma` | Persistencia local del índice |
| `RAG_TOP_K` | `5` | Candidatos iniciales del retriever |

## Aviso

Este proyecto es una demostración académica. No constituye una valoración, tasación, previsión ni
recomendación inmobiliaria, jurídica, fiscal, técnica, financiera o de inversión.
