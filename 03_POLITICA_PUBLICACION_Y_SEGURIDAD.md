# Política de publicación y protección de información

Fecha: 8 de noviembre de 2026.

## Decisión

El proyecto académico se publicará en GitHub como repositorio público y la aplicación podrá desplegarse públicamente en Streamlit. La protección de secretos industriales de Vissotia es un requisito de diseño, no una tarea posterior.

## Principio fundamental

**Un documento que no puede hacerse público tampoco puede formar parte del índice vectorial de una aplicación pública.**

Ocultar el PDF o DOCX no es suficiente. Si sus chunks están en ChromaDB, el agente puede recuperarlos, resumirlos o revelarlos mediante preguntas directas, indirectas o prompt injection.

## Arquitectura de doble corpus

### Corpus público académico

Se utilizará en el repositorio y en Streamlit. Solo podrá contener:

- información ya publicada oficialmente por Vissotia;
- documentación redactada específicamente para la demo;
- ejemplos sintéticos;
- nombres, cifras y escenarios ficticios;
- explicaciones de alto nivel que no revelen arquitectura propietaria;
- contenido revisado y aprobado expresamente para difusión pública.

### Corpus privado futuro

Se reservará para una integración posterior en Vissotia. Podrá contener documentación interna, pero deberá mantenerse:

- fuera del repositorio público;
- fuera de Streamlit Community Cloud;
- fuera de artefactos Chroma distribuidos;
- en almacenamiento privado con autenticación y control de acceso;
- separado por entorno, tenant y permisos;
- sujeto a auditoría y trazabilidad.

## Contenido prohibido en el repositorio público

- API keys, tokens, contraseñas, secretos OAuth o credenciales cloud.
- `.env`, ficheros de secretos o salidas de notebooks que muestren credenciales.
- URLs internas, direcciones IP, nombres de contenedores, hosts o endpoints privados.
- Código o diagramas que revelen defensas, vulnerabilidades o arquitectura sensible.
- Auditorías internas completas.
- Hallazgos de seguridad, aislamiento tenant o controles todavía no corregidos.
- Lógica propietaria de valoración, scoring, recomendación u orquestación.
- Datos reales de clientes, agencias, inmuebles, usuarios o proyectos.
- Información personal, contractual, financiera o comercial no pública.
- Roadmap no anunciado, costes internos, estrategia comercial o decisiones confidenciales.
- Bases vectoriales generadas desde documentación privada.
- Outputs de evaluación que reproduzcan fragmentos privados.

## Estrategia recomendada para el proyecto académico

Crear desde cero un **Pack Documental Público de Vissotia Demo**, con un mínimo de tres documentos y unas veinte páginas totales. Propuesta:

1. `01_guia_publica_vissotia_demo.md`
   - Qué es Vissotia a nivel público.
   - Perfil de usuario ficticio.
   - Flujo general de trabajo.
   - Funciones demostrables sin detalles internos.

2. `02_manual_operativo_demo.md`
   - Creación de un proyecto ficticio.
   - Navegación y tareas de ejemplo.
   - Preguntas frecuentes.
   - Datos, nombres y escenarios completamente sintéticos.

3. `03_glosario_y_politicas_demo.md`
   - Glosario de conceptos inmobiliarios y del producto.
   - Límites del asistente.
   - Política de privacidad de la demo.
   - Conducta ante información no disponible.

4. Documento opcional: `04_casos_de_uso_demo.md`
   - Casos ficticios de captación, valoración, preparación comercial y seguimiento.
   - Ninguna regla propietaria ni dato real.

El contenido puede inspirarse en documentación interna, pero no debe ser una copia abreviada. Cada afirmación deberá clasificarse como pública, genérica, sintética o no publicable.

## Decisión confirmada sobre autenticidad

El usuario ha confirmado que el corpus académico se centrará en información pública. El contenido sintético tendrá la menor incidencia posible y se limitará a:

- nombres de personas y empresas de demostración;
- inmuebles, direcciones, precios y proyectos ficticios;
- preguntas de prueba y conversaciones;
- resultados simulados necesarios para explicar un flujo.

No se inventarán capacidades de Vissotia. Las funcionalidades descritas deberán estar publicadas o aprobadas expresamente para comunicación pública.

La guía de onboarding existente podrá utilizarse como base funcional autorizada para redactar un documento nuevo de onboarding y venta. El archivo original no se publicará ni se indexará directamente: primero se eliminarán duplicados, se revisará cada afirmación y se excluirán detalles internos o no confirmados.

## Separación técnica prevista

Estructura pública:

```text
data/
  public/
    raw/
    processed/
  sample/
chroma_public/        # solo si se decide versionar; preferiblemente regenerable
.env.example
```

Estructura privada local, excluida por Git:

```text
data_private/
chroma_private/
.env
```

Entradas mínimas de `.gitignore`:

```gitignore
.env
.env.*
!.env.example
data_private/
chroma_private/
*.key
*.pem
secrets.*
.streamlit/secrets.toml
```

## Controles previos a cada publicación

1. Revisar `git status` y el diff completo.
2. Buscar patrones de API keys y credenciales.
3. Revisar outputs y metadatos de notebooks.
4. Comprobar que no se versionan Chroma ni caches creadas desde datos privados.
5. Confirmar que cada documento público tiene aprobación de difusión.
6. Ejecutar preguntas adversariales contra el agente.
7. Verificar que las fuentes mostradas pertenecen únicamente al corpus público.
8. Rotar inmediatamente cualquier secreto publicado por error, aunque después se borre del historial.

## Regla de trabajo desde este momento

Los documentos internos ya identificados se utilizarán únicamente para decidir estructura, temas y terminología. No se copiarán, transformarán ni indexarán en la versión pública hasta que el usuario apruebe un proceso explícito de saneamiento y el resultado final.

## Frontera del agente web público

El agente se instalará en la web pública de Vissotia y atenderá a potenciales clientes y usuarios reales. Esta instancia tendrá una frontera de datos estricta:

- no autenticará usuarios;
- no consultará cuentas ni perfiles;
- no accederá a proyectos o inmuebles registrados;
- no conocerá `project_id`, `user_id`, tenant, agencia u otros identificadores internos;
- no dispondrá de tools de lectura o escritura sobre producción;
- no confirmará si una persona, agencia, inmueble o proyecto existe en Vissotia;
- no realizará valoraciones reales ni decisiones sobre inmuebles concretos;
- no solicitará documentación inmobiliaria, direcciones completas, datos registrales o datos personales para la demo pública.

Esta instancia **no se conectará en ningún caso a la base de datos de clientes de Vissotia**. La restricción no es temporal ni depende del entorno académico.

### Tratamiento de consultas sobre datos reales

Si el usuario pregunta por “mi vivienda”, “mi proyecto”, “mis datos” o una operación real, el agente deberá:

1. indicar que el asistente público no puede acceder a información privada;
2. no pedir identificadores ni más datos del inmueble;
3. explicar de forma genérica cómo funcionaría la característica;
4. remitir al área privada autenticada o al canal de soporte adecuado;
5. recordar que no se compartan datos sensibles en el chat público.

### Simulaciones de inmuebles

Los ejemplos deberán:

- estar marcados como `Ejemplo simulado`;
- usar nombres, direcciones, precios, referencias y características ficticias;
- evitar combinaciones que puedan identificar accidentalmente un inmueble real;
- explicar una funcionalidad, no producir una valoración o recomendación profesional real;
- mantenerse separados del conocimiento factual de Vissotia mediante metadatos como `content_type=synthetic_example`.

### Separación respecto a una futura integración privada

Una futura versión autenticada dentro de Vissotia será otro entorno, otro corpus y otra política de permisos. No se añadirá acceso privado a este agente público mediante una simple tool o variable de configuración. Requerirá diseño específico de autorización, aislamiento tenant, trazabilidad y mínimo privilegio.

## Llamadas a la acción públicas

Cuando resulte pertinente, el agente podrá ofrecer:

- solicitar una demo;
- acceder o registrarse;
- contactar con soporte.

Estas acciones se implementarán como enlaces o botones externos. El chat no recopilará nombre, email, teléfono, empresa, dirección ni otros datos de contacto. Tampoco creará leads, tickets o registros en una base de datos.

Reglas:

- no mostrar las tres opciones en cada respuesta;
- elegir la llamada a la acción según la intención del usuario;
- no interrumpir una respuesta útil con contenido comercial;
- identificar claramente que el usuario abandonará el chat o abrirá otra página;
- no enviar datos de la conversación en parámetros de URL.

## Memoria del proyecto académico

La memoria del MVP será conversacional y temporal:

- `thread_id` aleatorio, no derivado de la IP;
- contexto conservado entre turnos dentro de la misma sesión;
- almacenamiento en `InMemorySaver` y/o `st.session_state`;
- sin identificación de la persona;
- sin persistencia en base de datos;
- opción visible para borrar la conversación;
- pérdida de la memoria al finalizar o reiniciar la sesión.

Esta implementación cumple el requisito académico de demostrar coherencia entre turnos. La memoria entre sesiones no forma parte del MVP.

**Decisión confirmada:** el MVP utilizará exclusivamente esta memoria temporal de sesión. No se usará IP, cookie persistente, cuenta de usuario ni base de datos para recordar conversaciones.

## Hipótesis futura: registro de conversaciones en Vissotia

Para una futura implementación real podría ser útil conservar conversaciones, pero la IP no debe utilizarse como identificador principal del usuario.

Problemas de la IP como identidad:

- puede ser dinámica y cambiar;
- varias personas pueden compartirla mediante NAT, una oficina o una red doméstica;
- una persona puede usar varias IP por móvil, Wi-Fi, VPN o distintos dispositivos;
- proxies y CDN pueden ocultar o alterar la IP observada;
- no permite autenticación ni evita que se mezclen conversaciones;
- no ofrece un mecanismo fiable para acceso, rectificación o supresión por parte del usuario.

Además, la IP puede constituir un dato personal o identificador en línea. Vincularla a transcripciones incrementaría el riesgo y exigiría finalidad definida, base jurídica, información al usuario, plazo de conservación, medidas de seguridad, gestión de derechos y revisión del proveedor que procesa los prompts.

Arquitectura futura preferida:

1. Usuarios autenticados: asociar conversaciones a un identificador interno autorizado, no a la IP.
2. Usuarios anónimos: identificador aleatorio de conversación en cookie o almacenamiento local, con política clara y, si procede, consentimiento.
3. IP: reservarla para seguridad, prevención de abuso o rate limiting, en logs separados y con retención corta, solo si existe una necesidad documentada.
4. Separar `conversation_logging` de `agent_memory`: registrar una conversación no implica reenviar indefinidamente todo su contenido al modelo.
5. Considerar guardar resúmenes o estados mínimos en lugar de transcripciones completas.

Esta hipótesis queda fuera del alcance del proyecto académico actual y requerirá revisión jurídica y técnica específica antes de producción.

