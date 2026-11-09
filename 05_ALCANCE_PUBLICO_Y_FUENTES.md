# Alcance público y fuentes de información

Fecha: 8 de noviembre de 2026.

## Propósito

Definir qué fuentes puede explicar el asistente público y cómo debe presentarlas sin atribuirles capacidades o carácter oficial que no tengan.

## Vissotia.es

Fuente pública principal para describir el producto.

URL: `https://vissotia.es/`

Contenido público verificado:

- Vissotia se presenta como una plataforma de IA contextual y Single Source of Truth para centralizar y ejecutar operaciones inmobiliarias.
- Conecta datos, contexto, inteligencia, decisiones y operaciones alrededor del proyecto inmobiliario.
- Se dirige a agencias, agentes, propietarios vendedores y, como evolución del ecosistema, otros participantes de la vivienda.
- Publica como casos de uso valoración IA, estrategia de precio, marketing inmobiliario, gestión documental y escenarios operativos.
- Describe el marketing inmobiliario como generación de mensajes y contenidos coherentes con el inmueble, la audiencia y la estrategia.
- Su página de visión menciona Catastro, INE y contexto local como datos territoriales conectados al inmueble.
- Defiende trazabilidad, origen de los datos y supervisión humana.

## Dirección General del Catastro

Fuentes públicas:

- `https://www.catastro.hacienda.gob.es/es-ES/sede.html`
- `https://www.catastro.hacienda.gob.es/es-ES/faqs.html`

Cómo se describirá:

- fuente pública de información catastral y cartográfica;
- permite localizar inmuebles por dirección o referencia catastral y consultar información no protegida;
- ciertos datos están protegidos y requieren legitimación o autorización.

Regla del agente:

- explicar la función de Catastro en el flujo;
- no consultar ni pedir datos protegidos;
- no afirmar que Catastro equivale al Registro de la Propiedad;
- no utilizar datos de un inmueble real en la demo.

## Instituto Nacional de Estadística (INE)

Fuente pública: `https://www.ine.es/`

Cómo se describirá:

- estadísticas oficiales agregadas sobre población, demografía, vivienda, transmisiones y otros indicadores territoriales;
- aporta contexto de mercado y territorio, no una valoración individual por sí sola.

Regla del agente:

- diferenciar dato estadístico agregado de dato de un inmueble;
- mencionar fecha, ámbito geográfico y carácter provisional/definitivo cuando se muestre un indicador;
- no fabricar cifras ni extrapolar más allá de la fuente.

## Google Maps Platform / Places

Fuente pública: `https://developers.google.com/maps/documentation/places/web-service/overview`

Cómo se describirá:

- servicio de información sobre lugares, establecimientos, ubicaciones y puntos de interés;
- puede aportar contexto sobre servicios y equipamientos del entorno.

Regla del agente:

- hablar de categorías y contexto de zona;
- no afirmar que Google proporciona estadísticas oficiales de vivienda;
- respetar atribución, licencias y condiciones de uso en una integración real;
- no realizar consultas live en el MVP salvo decisión posterior.

## Euríbor

Jerarquía de fuentes:

1. **EMMI**: administrador y fuente oficial de publicación del euríbor.
2. **Banco de España / BOE**: publicación de tipos oficiales de referencia en España.
3. **Euribor.com**: fuente informativa secundaria, no fuente oficial del índice.

Fuentes públicas:

- `https://www.emmi-benchmarks.eu/`
- `https://www.bde.es/webbe/es/estadisticas/recursos/glosario/conceptos/euribor.html`
- `https://www.euribor.com/`

Regla del agente:

- explicar qué es el euríbor y su papel general;
- distinguir datos oficiales de contenidos informativos;
- no garantizar actualidad de una cifra almacenada en el RAG;
- no calcular condiciones hipotecarias personalizadas;
- para cifras actuales, enlazar a una fuente oficial o indicar que deben verificarse.

## Perfilado de comprador objetivo y contenidos

El corpus explicará una funcionalidad pública de generación de contenidos orientados a una audiencia coherente con el inmueble y la estrategia.

Se utilizará el término preferente **arquetipo de comprador objetivo**, porque el MVP no analiza ni perfila personas reales.

Proceso conceptual:

1. Analizar atributos públicos/simulados del inmueble.
2. Identificar necesidades de uso y argumentos de valor compatibles.
3. Definir un arquetipo comercial no identificable.
4. Seleccionar beneficios y tono.
5. Generar variantes de anuncio por canal.
6. Mantener revisión y decisión humana.

Ejemplo permitido:

> Ejemplo simulado: una vivienda compacta, bien conectada y con servicios cercanos puede orientar su comunicación hacia personas que priorizan movilidad, comodidad cotidiana y eficiencia del espacio.

Ejemplo no permitido:

> Dirigir o excluir anuncios basándose en etnia, religión, salud, orientación sexual u otros atributos sensibles o inferidos de personas reales.

## Estado de integración en el MVP

Estas fuentes se incorporarán al corpus para explicar procedencia, utilidad y límites. El MVP RAG no consultará automáticamente sus APIs ni garantizará datos en tiempo real. Una tool live sería una ampliación separada, con control de costes, licencias, seguridad y manejo de errores.

**Decisión confirmada:** el MVP no realizará consultas en tiempo real a Catastro, INE, Google Places, EMMI, Banco de España, Euribor.com ni otros servicios externos. La aplicación explicará su aportación a Vissotia mediante documentación pública versionada y fechada.

Consecuencias de diseño:

- no habrá API keys adicionales;
- no se mostrarán cifras como si fueran actuales salvo que se indique claramente su fecha;
- no se prometerá disponibilidad en tiempo real;
- una futura integración live se tratará como extensión independiente;
- las tools del agente se limitarán al retriever y a funciones internas sin efectos externos.

