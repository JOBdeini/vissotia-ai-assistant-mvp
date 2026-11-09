# Proyecto de IA Generativa - contexto y requisitos

Fecha de consolidación inicial: 8 de noviembre de 2026.

## Ruta oficial de trabajo

`<PROJECT_ROOT>`

Todo el desarrollo nuevo, documentación, corpus, notebooks finales y entregables se organizará dentro de esta ruta. Los materiales de clase permanecen en sus carpetas originales y se usarán como referencias de solo lectura.

## Objetivo

Construir un asistente experto en un dominio delimitado, con una base de conocimiento propia y respuestas mediante RAG. El asistente debe utilizar Google Gemini, mantener memoria conversacional y funcionar desde un notebook.

## Dominio elegido

**Experto interno en producto y operaciones de Vissotia.**

El agente se diseña como una base reutilizable que, después del proyecto académico, pueda integrarse en Vissotia. Su función será responder preguntas internas sobre el producto, sus módulos, flujos de trabajo, estado funcional, arquitectura operativa y evolución prevista, diferenciando siempre entre funcionalidades actuales y propuestas futuras.

## Público objetivo

- **Principal:** profesionales inmobiliarios y equipo comercial/onboarding de Vissotia.
- **Secundario:** usuarios particulares.

El contenido factual procederá del mismo corpus público, pero la presentación se adaptará al perfil. Para profesionales se podrá utilizar terminología sectorial y respuestas operativas concisas. Para particulares se empleará lenguaje sencillo, explicación de conceptos, pasos numerados, ejemplos y advertencias cuando una decisión requiera asesoramiento profesional.

## Canal y frontera de datos

El agente se desplegará en la web pública para resolver dudas de potenciales clientes y usuarios. No será un agente autenticado de la aplicación ni tendrá acceso a cuentas, proyectos, inmuebles, tenants, CRM, bases de datos o herramientas internas.

Toda conversación sobre inmuebles será una simulación didáctica del uso de Vissotia. No se mostrará, buscará, inferirá ni confirmará información de inmuebles o proyectos registrados por usuarios reales.

## Condición de publicación

El proyecto académico se publicará en un repositorio público de GitHub y podrá desplegarse públicamente con Streamlit. Por tanto, ningún documento interno original, secreto industrial, credencial, dato personal, detalle de seguridad, auditoría interna ni arquitectura sensible de Vissotia puede formar parte del repositorio, de la base Chroma distribuida o de las respuestas de la aplicación pública.

Se adoptará una arquitectura de doble corpus:

- **Corpus público académico:** documentos saneados, sintéticos o ya públicos, expresamente aprobados para GitHub y Streamlit.
- **Corpus privado futuro:** documentación interna real, fuera del repositorio y de la demo pública, para una posterior integración controlada en Vissotia.

## Requisitos oficiales consolidados

- LLM: Google Gemini.
- Embeddings: Google Gemini Embeddings.
- Base vectorial: ChromaDB.
- Agente: LangGraph con LangChain como base.
- Entorno: Jupyter Notebook o Google Colab.
- Corpus: al menos 3 documentos sustanciales o unas 20 páginas equivalentes.
- System prompt personalizado y justificado.
- Memoria conversacional entre turnos.
- Interacción textual desde el notebook.
- Al menos 5 preguntas y respuestas documentadas.
- Al menos una prueba explícita de memoria entre turnos.
- README con dominio, instalación, ejecución, dependencias, API key y justificación del prompt.
- Presentación oral de 5 a 10 minutos con demo.
- Streamlit y despliegue público: bonus, no requisito del MVP.

## Criterio de diseño adoptado

El PDF oficial es la fuente normativa. Las notas y notebooks de clase enriquecen la solución, pero no pueden rebajar sus requisitos.

Aunque una clase menciona otros LLM y presenta RAG condicional, la implementación final usará Gemini. Si se implementa enrutamiento, toda pregunta factual del dominio que necesite información deberá consultar la base; las rutas alternativas se reservarán para preguntas fuera de dominio, aclaraciones o respuestas de control.

Esta elección corresponde al MVP académico. La futura versión integrada en `vissotia.es` utilizará OpenAI. Para facilitar esa evolución, el código separará la lógica de negocio, el RAG y el grafo del adaptador del proveedor de modelos, sin incorporar OpenAI como dependencia operativa del MVP.

## Errata conocida del enunciado

Los contenidos de los pasos 2 y 3 aparecen intercambiados: bajo el diseño del system prompt figuran tareas de creación de la base, y bajo la creación de la base aparecen tareas de diseño del prompt. Se conservarán todas las tareas en su orden lógico.

## Arquitectura de referencia

Indexación:

`documentos -> carga -> limpieza -> chunks + metadatos -> Gemini Embeddings -> ChromaDB persistente`

Consulta:

`pregunta + historial -> estado LangGraph -> recuperación -> contexto -> prompt delimitado -> Gemini -> respuesta + fuentes -> memoria`

## Evidencias mínimas del notebook final

1. Instalación e importaciones reproducibles.
2. Carga segura de secretos.
3. Inspección y descripción del corpus.
4. Limpieza y chunking justificados.
5. Creación o carga de ChromaDB persistente.
6. Pruebas del retriever antes de conectar el LLM.
7. System prompt documentado.
8. Estado, nodos y aristas de LangGraph.
9. RAG con Gemini.
10. Dos herramientas deterministas para simulaciones orientativas de inversión: compra para alquiler y compra-reforma-venta.
10. Memoria con conversaciones separadas por identificador.
11. Celda o función de chat.
12. Cinco ejemplos documentados.
13. Prueba de seguimiento que dependa de un turno anterior.
14. Casos sin respuesta y fuera de dominio.

## Principios técnicos que se conservarán

- Temperatura baja para respuestas documentales.
- Contexto recuperado claramente delimitado y tratado como datos, no como instrucciones.
- Prohibición explícita de inventar información.
- Respuesta controlada cuando el corpus no contiene soporte suficiente.
- Metadatos de fuente, página o sección conservados en los chunks.
- Evaluación del retriever independiente de la generación.
- Ajuste razonado de tamaño de chunk, solapamiento y `k`.
- Una sola convención de variable de entorno para la API key.
- Ninguna credencial en código, notebooks, salidas o repositorio.
- Dependencias fijadas y namespaces de LangChain coherentes.
- Notebook ejecutable de principio a fin sin estado oculto.

## Estado

- Enunciado oficial y cinco resúmenes de clase estudiados.
- Dos remesas, con 22 notebooks y una presentación, registradas en `01_INVENTARIO_MATERIALES_CLASE.md`.
- Ya se dispone de ejemplos explícitos de LangGraph, tools, Agentic RAG, memoria, guardrails, evaluación y pipelines ML + GenAI.
- Pendiente recibir cualquier material docente adicional que el usuario quiera incorporar.
- Dominio decidido: experto interno en Vissotia.
- Corpus candidato identificado y auditado a nivel inicial; pendiente confirmar si el alcance incluirá únicamente V1 o también la visión V2.
- Condición de seguridad añadida: el repositorio y la app serán públicos; el corpus interno localizado no se publicará ni se indexará en la demo hasta completar saneamiento y aprobación.

