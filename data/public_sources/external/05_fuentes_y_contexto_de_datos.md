---
document_id: vissotia_05_fuentes_contexto
title: Fuentes y contexto de datos
source_type: official_external
source_name: Catastro, INE, Google Maps Platform, EMMI y Banco de España
source_url: https://www.catastro.hacienda.gob.es/es-ES/faqs.html
retrieved_at: 2026-11-08
language: es
audience: all
scope: sources
status: approved
---

# Fuentes y contexto de datos

## Por qué se combinan distintas fuentes

Una vivienda y una operación inmobiliaria no pueden comprenderse mediante un único dato. La identificación administrativa, las estadísticas territoriales, los servicios del entorno y las referencias financieras responden a preguntas diferentes.

Vissotia explica estas fuentes como capas de contexto. Una fuente no debe utilizarse para afirmar algo que queda fuera de su finalidad. Además, la fecha, la cobertura y las condiciones de acceso influyen en la interpretación.

El Asistente Vissotia del MVP no consulta estas fuentes en tiempo real. Explica qué aportan y cuáles son sus límites a partir de documentación pública fechada.

## Dirección General del Catastro

El Catastro es un registro administrativo dependiente del Ministerio de Hacienda que contiene la descripción de bienes inmuebles. Su función es diferente de la del Registro de la Propiedad.

La referencia catastral es un identificador oficial asignado a cada inmueble y permite localizarlo en la cartografía catastral. Parte de la información catastral es pública; los datos protegidos están sujetos a requisitos de acceso.

### Qué puede aportar

- identificación catastral del inmueble;
- localización en cartografía;
- descripción física y uso catastral disponible;
- superficie y otros datos no protegidos que deban contrastarse;
- una referencia común para evitar confundir inmuebles.

### Qué no debe afirmarse

- que Catastro acredita por sí solo la titularidad jurídica;
- que sustituye al Registro de la Propiedad;
- que todos sus datos describen necesariamente la situación física o jurídica actual;
- que cualquier persona puede acceder a datos protegidos.

Fuente: https://www.catastro.hacienda.gob.es/es-ES/faqs.html

## Instituto Nacional de Estadística

El Instituto Nacional de Estadística publica estadísticas oficiales sobre población, hogares, vivienda, economía y otros ámbitos. Sus datos pueden aportar contexto agregado para un municipio, distrito u otra unidad territorial cuando la operación estadística lo permita.

### Qué puede aportar

- características demográficas agregadas;
- composición y evolución de hogares;
- indicadores de vivienda y territorio;
- información sobre transmisiones y actividad, según la operación estadística;
- una referencia para comparar ámbitos y periodos.

### Cómo debe interpretarse

- un promedio de zona no describe automáticamente un inmueble concreto;
- debe comprobarse el ámbito geográfico;
- debe indicarse el periodo del dato;
- debe distinguirse entre resultados provisionales y definitivos;
- no debe extrapolarse una cifra más allá de la población o territorio cubierto.

Fuente: https://www.ine.es/

## Google Maps Platform y Places

Places API ofrece datos de ubicación sobre establecimientos, lugares geográficos y puntos de interés. Entre sus capacidades públicas se encuentran la búsqueda de lugares y la consulta de detalles mediante identificadores de lugar.

### Qué puede aportar

- establecimientos y servicios cercanos;
- categorías de lugares;
- información de ubicación;
- puntos de interés que ayuden a describir la vida cotidiana de la zona.

### Límites

- Google Places no es una fuente oficial de estadísticas inmobiliarias;
- la presencia o distancia de un servicio no demuestra por sí sola el valor de una vivienda;
- en una integración real deben respetarse las condiciones de uso, atribución, licencias y facturación;
- el MVP no realiza peticiones a la API ni utiliza una clave de Google.

Fuente: https://developers.google.com/maps/documentation/places/web-service/overview

## Euríbor y fuentes oficiales

El euríbor es un índice de referencia del mercado monetario en euros para varios vencimientos. Su administrador es el European Money Markets Institute, EMMI. En España, el euríbor a doce meses se utiliza habitualmente como referencia en préstamos hipotecarios a tipo variable.

### Jerarquía utilizada por el asistente

1. EMMI para la definición, metodología y publicación del índice.
2. Banco de España y, cuando corresponda, BOE para referencias oficiales en España.
3. Sitios informativos como euribor.com únicamente como fuentes secundarias.

### Regla de actualidad

El RAG contiene documentación fechada, no una cotización en tiempo real. Cuando el usuario necesite un valor actual, el agente debe indicar que lo compruebe en una fuente oficial. No debe presentar una cifra almacenada como si fuera vigente hoy.

### Relación con las simulaciones

Las calculadoras del MVP no obtienen automáticamente el euríbor ni calculan una hipoteca. Si una simulación incluye costes financieros, el usuario introduce un importe hipotético y la herramienta lo muestra como supuesto.

Fuentes:

- https://www.emmi-benchmarks.eu/benchmarks/euribor/
- https://www.bde.es/webbe/es/estadisticas/recursos/glosario/conceptos/euribor.html
- https://www.bde.es/wbe/es/areas-actuacion/politica-monetaria/preguntas-frecuentes/papel-tipos-interes/que-son-los-tipos-de-interes-de-referencia.html

## Trazabilidad

Cuando el agente explique una fuente, debe mostrar su nombre y enlace. Si utiliza una afirmación sobre Vissotia junto con una definición externa, debe diferenciar ambos orígenes.

La presencia de una fuente en el corpus no significa que Vissotia o el MVP la estén consultando en ese momento.
