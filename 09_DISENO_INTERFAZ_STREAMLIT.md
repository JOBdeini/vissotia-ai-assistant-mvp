# Diseño funcional de la interfaz Streamlit

Fecha: 8 de noviembre de 2026.

## Objetivo

Ofrecer una interfaz pública, sencilla y didáctica que combine conversación, onboarding adaptativo, RAG con fuentes y simulaciones orientativas.

## Encabezado

**Nombre:** Asistente Vissotia

**Subtítulo:** Descubre cómo Vissotia conecta datos, contexto y decisiones inmobiliarias.

Se mostrará una nota breve:

> Asistente demostrativo con información pública. No accede a cuentas, clientes ni inmuebles registrados en Vissotia.

## Selector de perfil

Antes de iniciar o en la barra lateral:

- `Profesional inmobiliario`
- `Propietario particular`
- `Inversor`

El selector ajustará lenguaje, profundidad, ejemplos y sugerencias. No cambiará las reglas de seguridad ni concederá acceso a información diferente. No habrá un perfil preseleccionado silenciosamente.

## Inicio rápido

Se mostrarán preguntas opcionales:

- ¿Qué es Vissotia?
- Guíame paso a paso.
- ¿Qué aporta a un profesional inmobiliario?
- ¿Cómo ayuda a un propietario?
- ¿Cómo puede ayudar a un inversor?
- ¿Qué fuentes de información utiliza?
- Muéstrame un ejemplo simulado.
- Quiero solicitar una demo.

## Chat principal

Cada respuesta podrá contener:

1. Explicación principal.
2. Una pregunta de continuación cuando sea útil.
3. Desplegable `Fuentes consultadas` cuando se haya usado el RAG.
4. Llamada a la acción contextual, sin repetición innecesaria.

El agente responderá primero a la consulta directa. El onboarding no obligará al usuario a completar una secuencia fija.

## Simulaciones orientativas

### Activación

La intención se detectará desde el chat. Ejemplos:

- `Quiero simular una compra para alquilar.`
- `¿Cómo sería una compra, reforma y venta?`

El agente explicará brevemente la finalidad y abrirá el formulario correspondiente.

### Formulario de alquiler

Campos agrupados:

- adquisición;
- inversión inicial;
- ingresos hipotéticos;
- ocupación considerada;
- gastos anuales;
- financiación incluida, si procede.

### Formulario de compra, reforma y venta

Campos agrupados:

- adquisición;
- reforma y contingencia;
- mantenimiento y financiación;
- venta y otros costes;
- precio de venta hipotético.

### Resultado

El resultado aparecerá como un nuevo mensaje del asistente e incluirá:

- etiqueta `Simulación orientativa`;
- métricas calculadas;
- explicación sencilla;
- supuestos y operaciones desplegables;
- conceptos no incluidos;
- advertencia obligatoria.

Los datos permanecerán únicamente en la sesión y se eliminarán al reiniciar la conversación.

## Memoria y controles

- memoria temporal durante la sesión;
- botón `Nueva conversación`;
- aviso de que no se introduzcan datos personales;
- sin identificación por IP;
- sin persistencia del historial;
- sin formularios de captación dentro del chat.

## Llamadas a la acción

- `Solicitar una demo`: `https://vissotia.es/solicitar-demo`
- `Acceder / registrarse`: `https://vissotia.es/app`
- `Contactar con soporte`: `mailto:jobdelgadoi@vissotia.es`

Se abrirán como enlaces externos y no incluirán automáticamente el historial de conversación.

## Estados y errores

La interfaz distinguirá:

- generando respuesta;
- consultando el corpus;
- preparando formulario;
- calculando simulación;
- información insuficiente;
- error temporal de Gemini;
- límite de uso alcanzado.

Los mensajes serán comprensibles para usuarios no técnicos y no expondrán trazas, claves, rutas locales o detalles internos.

## Accesibilidad y claridad

- etiquetas completas y comprensibles;
- explicaciones junto a términos como rentabilidad bruta o margen;
- importes formateados en euros;
- porcentajes con denominador explícito;
- contraste suficiente;
- navegación utilizable con teclado;
- advertencias visibles sin depender solo del color;
- bloques breves y desplegables para evitar sobrecarga.

## Elementos excluidos del MVP

- carga de documentos por usuarios;
- consulta de inmuebles reales;
- conexión con la base de datos de Vissotia;
- APIs externas en tiempo real;
- autenticación;
- almacenamiento de conversaciones;
- recopilación de leads;
- cálculo automático de impuestos o hipotecas;
- panel administrativo.
