# Decisión de tema y propuesta de corpus

Fecha: 8 de noviembre de 2026.

## Tema elegido

**Asistente público experto en producto y uso de Vissotia.**

Objetivo académico: construir un agente RAG con Gemini, Gemini Embeddings, ChromaDB, LangGraph, memoria y Streamlit.

El MVP se limita a explicar públicamente Vissotia a potenciales clientes y usuarios. No se conectará a la aplicación, a bases de datos de clientes ni a proyectos inmobiliarios reales. Cualquier adaptación al chat real de Vissotia queda fuera del alcance actual.

## Estado real del corpus

Los documentos fuente están localizados en `<LOCAL_SOURCE_MATERIALS>`.

Todavía no están preparados para embeddings. No se han copiado al proyecto académico, normalizado, deduplicado, convertido a un formato común ni etiquetado por versión. Los originales se mantendrán intactos.

**Restricción confirmada:** el repositorio de GitHub y la app Streamlit serán públicos. En consecuencia, los documentos internos descritos en este archivo son candidatos para una futura versión privada, no para publicación directa. No se copiarán a la carpeta pública del proyecto ni se incluirán en Chroma.

El usuario ha aprobado una estrategia centrada en información pública. La síntesis se reducirá al mínimo: se empleará únicamente para ejemplos, identidades, inmuebles y conversaciones ficticias. Las afirmaciones sobre Vissotia deberán proceder de fuentes públicas o de contenido expresamente autorizado para difusión.

## Corpus interno de referencia, no publicable

### 1. Estado funcional actual

**Vissotia V1 Functional Freeze**

- Formato disponible: PDF y DOCX.
- Extensión PDF: 18 páginas, aproximadamente 2.434 palabras extraíbles.
- Función en el RAG: fuente prioritaria para responder qué existe y qué pertenece a la V1 estable.
- Metadatos propuestos: `scope=current`, `version=V1`, `document_type=functional_baseline`, `priority=high`.

### 2. Visión y arquitectura futura

**Arquitectura Funcional Vissotia V2**

- Formato disponible: PDF y DOCX.
- Extensión PDF: 18 páginas, aproximadamente 2.900 palabras extraíbles.
- Función en el RAG: explicar Proyecto Vivo, estados funcionales, orquestación y evolución prevista.
- Metadatos propuestos: `scope=future`, `version=V2`, `document_type=target_architecture`, `priority=high`.

### 3. Uso operativo

**Guía de Usuario de Vissotia**

- Formato disponible: DOCX.
- Extensión: aproximadamente 1.493 palabras extraíbles.
- Función en el RAG: instrucciones de uso, creación de proyecto, carga documental, Catastro, financiación, valoración y actualización del contexto.
- Metadatos propuestos: `scope=operational`, `version=V1`, `document_type=user_guide`, `priority=high`.

### 4. Criterio de producto

**Informe interno de Dirección de Producto**

- Formato disponible: PDF y DOCX.
- Extensión PDF: 17 páginas, aproximadamente 2.984 palabras extraíbles.
- Función en el RAG: propuesta de valor, fortalezas, debilidades, flujo comercial y criterios de evolución.
- Metadatos propuestos: `scope=strategy`, `version=V1_to_V2`, `document_type=product_strategy`, `priority=medium`.

### 5. Validación operativa

**Checklist operativa - Vissotia V1 Functional Freeze**

- Formato disponible: PDF y DOCX.
- Extensión PDF: 4 páginas, aproximadamente 877 palabras extraíbles.
- Función en el RAG: pruebas operativas, áreas funcionales y resultados esperados.
- Metadatos propuestos: `scope=validation`, `version=V1`, `document_type=qa_checklist`, `priority=medium`.

## Volumen inicial

- Cuatro PDF principales: 57 páginas.
- Una guía DOCX adicional.
- Aproximadamente 10.688 palabras extraíbles en conjunto.
- Cumple sobradamente el mínimo académico de 3 documentos o unas 20 páginas.

## Documentos reservados para una segunda fase

### Auditoría Chat

- 45 páginas y unas 8.139 palabras.
- Muy valiosa, pero puede dominar la recuperación por volumen y añadir problemas históricos ya corregidos.
- Se incorporará solo tras etiquetar hallazgos como vigentes, resueltos o históricos.

### Auditoría de Google Geocoding y Places

- 10 páginas y unas 1.425 palabras.
- Adecuada para una futura especialización técnica sobre datos territoriales.

### Auditoría Tenant/Demo/Workspace

- Documento corto, unas 773 palabras.
- Útil para seguridad y aislamiento, pero no esencial para el primer MVP.

## Documentos que no deben entrar inicialmente

- El archivo original de `Guía de usuario Vissotia Onboarding` no se publicará tal cual porque contiene contenido solapado y bloques duplicados. El usuario sí autoriza usar su contenido funcional como base de una nueva guía pública, limpia y orientada a onboarding/venta, siempre que no revele cómo está construida la herramienta.
- `CAMINO AL RAG`: describe el proceso de construir un RAG, no el dominio funcional de Vissotia.
- Presentaciones de premios y material promocional: pueden introducir lenguaje comercial no verificable como si fuera realidad funcional.
- Borradores, documentos de confirmación y archivos de trabajo sin estado/versionado claro.
- Auditorías históricas completas sin clasificar la vigencia de cada hallazgo.

## Riesgo principal: mezclar V1 y V2

V1 representa la línea base funcional existente. V2 contiene una arquitectura objetivo y funcionalidades futuras. Si ambos documentos se indexan sin metadatos ni reglas de respuesta, el agente puede afirmar que una propuesta futura ya está implementada.

Medidas previstas:

1. Añadir `scope`, `version`, `document_type`, `source` y fecha a todos los chunks.
2. Priorizar V1 para preguntas sobre el estado actual.
3. Recuperar V2 solo cuando la pregunta mencione evolución, visión, futuro, Proyecto Vivo o arquitectura objetivo.
4. Exigir que la respuesta indique claramente “actual”, “previsto” o “no confirmado”.
5. Mostrar fuentes en Streamlit.

## Preparación pendiente antes de crear embeddings

1. Crear `data/public_sources/` con documentos públicos, versionados y aptos para GitHub.
2. Crear `data/processed/` con el Markdown normalizado que se indexará.
3. Convertir DOCX sin perder títulos ni listas.
4. Eliminar encabezados, pies repetidos, páginas vacías y duplicados.
5. Asignar metadatos por documento y sección.
6. Definir una jerarquía de fuentes cuando exista contradicción.
7. Probar varias configuraciones de chunking.
8. Crear preguntas de evaluación antes de indexar.
9. Generar embeddings con Gemini y persistirlos en ChromaDB.

Este proceso solo se aplicará al corpus público aprobado. No se creará una carpeta `raw` con originales internos dentro del proyecto público. El corpus interno permanecerá fuera del repositorio, de ChromaDB y del despliegue académico.

## Fuentes previstas para el corpus público

1. Web pública oficial de Vissotia.
2. Publicaciones públicas oficiales o del promotor del proyecto sobre Vissotia.
3. Nueva versión pública y depurada de la guía de onboarding, basada en funcionalidades comunicables y autorizadas.
4. Material comercial ya publicado o expresamente aprobado.
5. Datos sintéticos únicamente para demostrar conversaciones y casos de uso, nunca para inventar funcionalidades.

La web pública y una publicación pública reciente describen Vissotia como una plataforma que acompaña decisiones inmobiliarias, estructura proyectos, aporta valoración y contexto territorial, ayuda en el seguimiento comercial y genera contenidos. Estas afirmaciones deberán capturarse con su fuente y fecha al preparar el corpus.


