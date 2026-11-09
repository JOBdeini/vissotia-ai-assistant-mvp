# Especificación de herramientas de simulación

Fecha: 8 de noviembre de 2026.

## Decisión confirmada

El MVP incorporará dos herramientas deterministas integradas en el flujo de LangGraph:

1. Simulación orientativa de compra para alquiler.
2. Simulación orientativa de compra, reforma y venta posterior.

Las operaciones se realizarán mediante código. Gemini podrá solicitar los datos que falten y explicar la salida, pero no calculará ni completará importes por su cuenta.

## Reglas comunes

- Toda salida comenzará con la etiqueta `Simulación orientativa`.
- Solo se aceptarán valores numéricos introducidos para la simulación o incluidos en un caso ficticio del corpus.
- No se consultarán precios, impuestos, tipos de interés o datos de mercado en tiempo real.
- No se aplicarán porcentajes fiscales automáticos.
- Los importes no facilitados no se estimarán silenciosamente.
- La herramienta devolverá una lista de conceptos incluidos y no incluidos.
- Los porcentajes indicarán claramente su denominador.
- Los resultados no se presentarán como previsión, tasación o recomendación.
- La aplicación no conservará los datos después de finalizar la sesión.
- Se validarán valores negativos, divisiones por cero, campos incoherentes y magnitudes no razonables.

## Herramienta 1: compra para alquiler

Nombre técnico provisional: `simulate_rental_investment`.

### Finalidad

Mostrar cómo cambian una rentabilidad y un flujo anual orientativos a partir de supuestos explícitos.

### Entradas

Entradas mínimas:

- `purchase_price`: precio de compra supuesto.
- `acquisition_costs`: suma introducida para impuestos y gastos de adquisición incluidos.
- `renovation_costs`: reforma o preparación inicial incluida.
- `other_initial_costs`: otros costes iniciales incluidos.
- `monthly_rent`: renta mensual hipotética.
- `occupied_months_per_year`: meses con ingreso considerados, entre 0 y 12.
- `annual_operating_costs`: gastos anuales incluidos, sin financiación.

Entrada opcional:

- `annual_financing_costs`: coste financiero anual introducido para la simulación. No se calculará una hipoteca dentro de esta herramienta.

Todos los campos monetarios se expresarán en euros. No se asignarán valores por defecto a impuestos, reforma, gastos, vacancia o financiación.

### Operaciones

```text
total_initial_investment =
  purchase_price
  + acquisition_costs
  + renovation_costs
  + other_initial_costs

annual_gross_income =
  monthly_rent * occupied_months_per_year

annual_net_income_before_financing =
  annual_gross_income - annual_operating_costs

annual_cash_flow_after_financing =
  annual_net_income_before_financing - annual_financing_costs

gross_yield_pct =
  annual_gross_income / total_initial_investment * 100

net_yield_before_financing_pct =
  annual_net_income_before_financing / total_initial_investment * 100
```

La rentabilidad neta se denominará siempre `antes de financiación`, porque el denominador representa la inversión inicial total y no el capital propio aportado.

### Salida estructurada

- inversión inicial total;
- ingreso bruto anual supuesto;
- ingreso neto anual antes de financiación;
- flujo anual después del coste financiero introducido;
- rentabilidad bruta sobre inversión inicial;
- rentabilidad neta antes de financiación sobre inversión inicial;
- supuestos utilizados;
- conceptos declarados como no incluidos;
- advertencia normalizada.

### Conceptos que deben advertirse si no están incluidos

- impuestos y gastos de adquisición;
- reforma y mobiliario;
- comunidad, seguros, mantenimiento y gestión;
- periodos sin alquiler;
- impagos;
- fiscalidad de los ingresos;
- financiación;
- reparaciones extraordinarias;
- cambios de renta o de valor del inmueble.

## Herramienta 2: compra, reforma y venta

Nombre técnico provisional: `simulate_renovate_and_sell`.

### Finalidad

Mostrar un resultado orientativo de proyecto a partir de un precio de venta hipotético y costes explícitos.

### Entradas

- `purchase_price`: precio de compra supuesto.
- `acquisition_costs`: impuestos y gastos de adquisición incluidos como suma introducida.
- `renovation_budget`: presupuesto de reforma incluido.
- `renovation_contingency`: margen adicional de reforma introducido como importe, no calculado automáticamente.
- `holding_costs`: costes de mantenimiento durante el periodo incluidos.
- `financing_costs`: costes de financiación incluidos.
- `selling_costs`: costes de comercialización y transmisión incluidos.
- `other_costs`: otros costes incluidos.
- `estimated_sale_price`: precio de venta hipotético.

La duración del proyecto podrá mostrarse como dato descriptivo, pero el MVP no calculará automáticamente intereses, inflación o apreciación a partir del tiempo.

### Operaciones

```text
total_project_cost =
  purchase_price
  + acquisition_costs
  + renovation_budget
  + renovation_contingency
  + holding_costs
  + financing_costs
  + selling_costs
  + other_costs

orientative_result =
  estimated_sale_price - total_project_cost

margin_on_sale_pct =
  orientative_result / estimated_sale_price * 100

return_on_total_cost_pct =
  orientative_result / total_project_cost * 100
```

Se mostrarán los dos porcentajes con nombres completos para no confundir margen sobre venta con retorno sobre coste total.

### Salida estructurada

- coste total del proyecto;
- precio de venta hipotético;
- resultado orientativo;
- margen sobre el precio de venta;
- retorno sobre el coste total;
- desglose de costes incluidos;
- conceptos no incluidos;
- advertencia normalizada.

### Conceptos que deben advertirse si no están incluidos

- impuestos y gastos de adquisición;
- licencias, técnicos y desviaciones de obra;
- costes de financiación;
- suministros, comunidad y mantenimiento;
- comercialización y transmisión;
- fiscalidad del resultado;
- ampliación del plazo de obra o venta;
- diferencia entre precio anunciado y precio efectivo;
- cambios de mercado.

## Validaciones

La implementación rechazará:

- importes negativos;
- `occupied_months_per_year` fuera del intervalo 0–12;
- inversión o coste total igual a cero cuando sea denominador;
- precio de venta igual a cero cuando se calcule margen sobre venta;
- texto libre en campos numéricos;
- valores no finitos;
- llamadas sin los datos mínimos necesarios.

Cuando falten datos, el agente formulará una única pregunta breve que agrupe los campos imprescindibles pendientes. No solicitará dirección, referencia catastral, identidad, cuenta bancaria ni otra información personal.

## Presentación en Streamlit

**Diseño confirmado:** interacción híbrida entre chat y formulario.

1. El usuario expresa en el chat que quiere realizar una simulación.
2. El agente identifica si corresponde a alquiler o a compra-reforma-venta.
3. Streamlit abre el formulario estructurado adecuado dentro de la experiencia conversacional.
4. El formulario muestra qué campos son obligatorios, permite introducir cero cuando un concepto se ha considerado expresamente y ofrece una opción para marcar conceptos como no incluidos.
5. Al enviar el formulario, LangGraph llama a la herramienta determinista.
6. El resultado vuelve al chat, donde Gemini lo explica sin modificar las cifras calculadas.

La respuesta mostrará:

1. Etiqueta visible `Simulación orientativa`.
2. Resumen de resultados.
3. Desplegable `Supuestos y operaciones`.
4. Desplegable `Conceptos no incluidos`.
5. Advertencia: `Este ejemplo no constituye una valoración, previsión ni recomendación de inversión. Verifica los datos y consulta a profesionales cualificados antes de tomar una decisión real.`

El botón de envío utilizará una etiqueta explícita, como `Calcular simulación orientativa`, y no `Calcular rentabilidad real` o `Evaluar inversión`.

El formulario no solicitará dirección, referencia catastral, nombre, correo electrónico, teléfono ni documentación. Se indicará al usuario que utilice cifras hipotéticas y que no introduzca datos personales.

## Integración con LangGraph

El grafo podrá enrutar una consulta a:

- `retrieve_public_knowledge`, para explicar Vissotia y sus fuentes;
- `simulate_rental_investment`, para compra destinada al alquiler;
- `simulate_renovate_and_sell`, para compra, reforma y venta;
- `clarify_request`, cuando falten datos o la intención sea ambigua;
- `safe_response`, cuando el usuario solicite asesoramiento personalizado o una garantía.

La explicación final combinará únicamente:

- el resultado estructurado de la herramienta;
- las reglas públicas del corpus;
- las advertencias y límites aprobados.

No se utilizará el RAG para inventar los datos numéricos de una simulación.

## Pruebas mínimas

Para cada herramienta se comprobará:

- un caso válido;
- un caso con campos ausentes;
- un caso con valor negativo;
- un caso con denominador cero;
- un caso con resultado negativo;
- redondeo consistente;
- presencia de etiqueta, supuestos y advertencia;
- ausencia de afirmaciones que garanticen resultados.
