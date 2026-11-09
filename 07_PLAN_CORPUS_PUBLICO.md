# Plan definitivo del corpus público

Fecha de corte inicial: 8 de noviembre de 2026.

## Objetivo

Construir un corpus pequeño, controlado y suficiente para que el Asistente Vissotia pueda explicar el producto, guiar a profesionales y particulares y mostrar casos de uso simulados sin revelar información interna.

El corpus se redactará en Markdown para facilitar su revisión humana, versionado en GitHub, segmentación por encabezados y carga en ChromaDB.

## Principios editoriales

1. Toda afirmación sobre Vissotia debe estar respaldada por contenido público de `vissotia.es` o por texto aprobado expresamente para difusión.
2. No se trasladará contenido desde documentos internos salvo una aprobación específica y una reescritura pública independiente.
3. Los ejemplos ficticios no se usarán como evidencia de capacidades ni resultados reales.
4. No se incluirán precios, planes, integraciones, métricas, promesas o disponibilidad no publicados.
5. Cada documento tendrá fuente, URL, fecha de consulta, tipo y alcance.
6. Las fuentes externas explicarán su aportación conceptual; el MVP no consultará sus APIs.
7. Los textos se escribirán para recuperación semántica: secciones autocontenidas, títulos claros y vocabulario consistente.

## Documentos que se crearán

### 01. Qué es Vissotia

Propósito: responder qué es, a quién se dirige y qué problema general aborda.

Contenido:

- IA contextual y Single Source of Truth;
- centralización de información y operaciones inmobiliarias;
- conexión entre datos, contexto, inteligencia, decisiones y ejecución;
- audiencias públicas: agencias, agentes, propietarios e inversores;
- diferencia entre apoyo tecnológico y asesoramiento profesional.

Fuente principal: `https://vissotia.es/`.

### 02. Funcionalidades y beneficios

Propósito: explicar las capacidades comunicadas públicamente y traducirlas a beneficios comprensibles.

Contenido:

- valoración asistida por IA;
- estrategia de precio;
- contexto territorial;
- marketing inmobiliario;
- gestión documental;
- escenarios y seguimiento operativo;
- trazabilidad y supervisión humana.

El documento distinguirá siempre entre `funcionalidad`, `beneficio` y `límite`.

### 03. Guía de inicio para profesionales

Propósito: onboarding comercial y didáctico para agencias y agentes.

Secuencia pública propuesta:

1. Crear y contextualizar un proyecto inmobiliario.
2. Reunir información relevante del inmueble.
3. Completar contexto territorial y documental.
4. Revisar una valoración orientativa y escenarios.
5. Definir estrategia y audiencia.
6. Preparar contenidos con IA.
7. Revisar humanamente y avanzar en la operación.

No describirá arquitectura, prompts, modelos internos, reglas propietarias ni detalles de implementación.

**Enfoque confirmado:** onboarding conceptual. Explicará el recorrido, la finalidad y los beneficios de cada etapa, sin reproducir pantallas, botones, menús o pasos internos exactos de la aplicación.

### 04. Guía de inicio para particulares e inversores

Propósito: explicar el mismo recorrido con lenguaje cotidiano, definiciones y advertencias más explícitas.

Contenido:

- qué información ayuda a contextualizar una vivienda;
- qué puede aportar cada paso;
- qué resultados son orientativos;
- cuándo debe intervenir un profesional;
- diferencia entre una simulación y un proyecto real en Vissotia.
- recorrido específico para un propietario que estudia o prepara una venta;
- recorrido específico para un inversor que quiere estructurar y comparar información;
- límites entre análisis informativo y asesoramiento de inversión.

El recorrido de inversor cubrirá dos casuísticas confirmadas:

1. Compra para alquiler.
2. Compra, reforma y venta posterior.

Los cálculos se presentarán siempre como simulaciones orientativas, con datos ficticios, supuestos visibles y advertencias sobre costes, fiscalidad, financiación, vacancia, obra y evolución del mercado que podrían no estar incluidos.

Aplicará el mismo enfoque conceptual confirmado, con mayor apoyo didáctico y sin convertirse en un manual de interfaz.

### 05. Fuentes y contexto de datos

Propósito: explicar qué aportan distintas fuentes sin simular conexiones en tiempo real.

Secciones:

- Catastro;
- INE;
- Google Maps Platform / Places;
- EMMI, Banco de España y euríbor;
- fecha, cobertura, procedencia y limitaciones de los datos.

Fuentes primarias:

- `https://www.catastro.hacienda.gob.es/es-ES/faqs.html`
- `https://www.ine.es/`
- `https://developers.google.com/maps/documentation/places/web-service/overview`
- `https://www.emmi-benchmarks.eu/benchmarks/euribor/`
- `https://www.bde.es/webbe/es/estadisticas/recursos/glosario/conceptos/euribor.html`

`euribor.com` podrá mencionarse como recurso informativo secundario, nunca como fuente oficial del índice.

### 06. Marketing y arquetipo de comprador objetivo

Propósito: explicar cómo el contexto de un inmueble puede orientar mensajes comerciales y variantes por canal.

Contenido:

- atributos del inmueble y de su entorno;
- necesidades de uso compatibles;
- creación de un arquetipo no identificable;
- selección de beneficios, tono y canal;
- revisión humana;
- prohibición de inferir o utilizar categorías sensibles de personas reales.

### 07. Seguridad, privacidad y límites

Propósito: proporcionar respuestas consistentes sobre lo que el asistente y el MVP no hacen.

Contenido:

- sin acceso a cuentas, clientes o inmuebles registrados;
- sin conexión con la base de datos de Vissotia;
- sin recopilación de datos personales en el chat;
- memoria limitada a la sesión;
- sin asesoramiento jurídico, fiscal, técnico, financiero o inmobiliario personalizado;
- sin consultas externas en tiempo real;
- canal de demo, acceso y soporte.

### 08. Casos de uso simulados

Propósito: mejorar la comprensión y demostrar respuestas con RAG sin utilizar información real.

Incluirá al menos cuatro casos, todos marcados como `Ejemplo simulado`:

1. Agencia que prepara la comercialización de una vivienda.
2. Agente que necesita ordenar información y próximos pasos.
3. Propietario que quiere entender cómo preparar una venta.
4. Inversor que estudia una compra para alquiler.
5. Inversor que estudia una compra, reforma y venta posterior.
6. Generación de anuncios para un arquetipo de comprador objetivo.

Los casos demostrarán el flujo y los beneficios, no resultados reales obtenidos por Vissotia.

### 09. Glosario y preguntas frecuentes

Propósito: cubrir consultas breves, sinónimos y vocabulario de usuarios no expertos.

Términos iniciales:

- IA contextual;
- Single Source of Truth;
- RAG;
- valoración orientativa;
- contexto territorial;
- referencia catastral;
- euríbor;
- arquetipo de comprador;
- trazabilidad;
- supervisión humana.

Preguntas iniciales:

- ¿Qué es Vissotia?
- ¿Para quién está pensada?
- ¿Sustituye a una tasación oficial?
- ¿Puede consultar mi inmueble?
- ¿De dónde proceden los datos?
- ¿Genera anuncios inmobiliarios?
- ¿Qué diferencia hay entre la demo y la plataforma real?

## Metadatos comunes

Cada documento comenzará con un bloque de metadatos compatible con el cargador:

```yaml
---
document_id: vissotia_01_que_es
title: Qué es Vissotia
source_type: official_public | official_external | approved_public | synthetic_example
source_name: Vissotia
source_url: https://vissotia.es/
retrieved_at: 2026-11-08
language: es
audience: all | professional | owner | investor | owner_investor
scope: product | onboarding | sources | marketing | safety | examples | glossary
status: approved
---
```

Los casos ficticios usarán siempre `source_type: synthetic_example` y no contendrán `source_url`.

## Jerarquía de confianza

1. Contenido oficial público de Vissotia para afirmaciones sobre el producto.
2. Fuente oficial externa para explicar Catastro, INE, Google Places o euríbor.
3. Contenido público expresamente aprobado para onboarding y ejemplos funcionales.
4. Ejemplo sintético, únicamente para ilustrar.

Si no existe soporte en los niveles 1 a 3, el agente no presentará la afirmación como una capacidad de Vissotia.

## Estructura de carpetas prevista

```text
data/
  public_sources/
    vissotia/
    external/
    approved/
    examples/
  processed/
  chroma/
```

La colección `chroma/` se generará localmente. Antes de decidir si se publica, se comprobará que solo contenga el corpus público y que no exponga rutas o metadatos internos.

## Validación antes de embeddings

- revisión humana de las afirmaciones sobre Vissotia;
- comprobación de URLs y fechas;
- búsqueda de secretos, datos personales y referencias internas;
- detección de duplicados y contradicciones;
- aprobación del tono para profesional y particular;
- preparación de preguntas de evaluación;
- solo después, chunking y embeddings con Gemini.

## Estado de redacción

Los nueve documentos previstos fueron aprobados por el responsable del proyecto el 8 de noviembre de 2026. Su estado es `approved` y pueden utilizarse para preparar el corpus procesado, la evaluación y los embeddings del MVP.
