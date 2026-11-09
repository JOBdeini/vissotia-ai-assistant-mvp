"""Interfaz Streamlit del MVP académico Asistente Vissotia."""

from __future__ import annotations

import os
import uuid
from decimal import Decimal

import streamlit as st
from langchain_core.messages import HumanMessage

from vissotia_assistant.calculators import (
    RenovateAndSellInput,
    RentalSimulationInput,
    simulate_renovate_and_sell,
    simulate_rental_investment,
)
from vissotia_assistant.config import Settings
from vissotia_assistant.graph import build_graph
from vissotia_assistant.rag import RagService

PROFILE_LABELS = {
    "Profesional inmobiliario": "professional",
    "Propietario particular": "owner",
    "Inversor": "investor",
}
QUICK_PROMPTS = (
    "¿Qué es Vissotia?",
    "Guíame paso a paso",
    "¿Qué fuentes de información utiliza?",
    "Muéstrame un ejemplo simulado",
)


def _load_streamlit_secrets() -> None:
    for key in (
        "GEMINI_API_KEY",
        "GEMINI_CHAT_MODEL",
        "GEMINI_EMBEDDING_MODEL",
        "GEMINI_EMBEDDING_DIMENSIONS",
    ):
        try:
            value = st.secrets.get(key)
        except FileNotFoundError:
            value = None
        if value is not None and key not in os.environ:
            os.environ[key] = str(value)


@st.cache_resource
def get_runtime():
    _load_streamlit_secrets()
    settings = Settings.from_env()
    rag_service = RagService(settings=settings)
    graph = build_graph(rag_service=rag_service)
    return settings, graph


def reset_conversation() -> None:
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.chat_history = []
    st.session_state.active_form = None


def ensure_session() -> None:
    if "thread_id" not in st.session_state:
        reset_conversation()
    if "selected_profile" not in st.session_state:
        st.session_state.selected_profile = None


def format_eur(value: Decimal) -> str:
    return f"{float(value):,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def format_percentage(value: Decimal) -> str:
    return f"{value:.2f} %".replace(".", ",")


def append_message(role: str, content: str, sources: list[dict] | None = None) -> None:
    st.session_state.chat_history.append(
        {"role": role, "content": content, "sources": sources or []}
    )


def process_query(query: str) -> None:
    _, graph = get_runtime()
    profile = st.session_state.selected_profile
    append_message("user", query)
    try:
        result = graph.invoke(
            {
                "messages": [HumanMessage(content=query)],
                "query": query,
                "user_profile": profile,
            },
            {"configurable": {"thread_id": st.session_state.thread_id}},
        )
    except Exception:
        append_message(
            "assistant",
            "No he podido completar la consulta en este momento. Inténtalo de nuevo más tarde.",
        )
        return

    append_message("assistant", result.get("answer", ""), result.get("sources", []))
    st.session_state.active_form = result.get("ui_action")


def render_history() -> None:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["sources"]:
                with st.expander("Fuentes consultadas"):
                    for source in message["sources"]:
                        title = source.get("title", "Fuente")
                        section = source.get("section", "")
                        url = source.get("url", "")
                        label = f"{title} — {section}" if section else title
                        if url and url != "none":
                            st.markdown(f"- [{label}]({url})")
                        else:
                            st.markdown(f"- {label} · Ejemplo simulado")


def render_rental_form() -> None:
    with st.form("rental_simulation"):
        st.subheader("Simulación orientativa: compra para alquiler")
        st.caption("Utiliza cifras hipotéticas y no introduzcas datos personales.")
        purchase = st.number_input("Precio de compra supuesto (€)", min_value=0.0, step=1_000.0)
        acquisition = st.number_input("Gastos de adquisición incluidos (€)", min_value=0.0)
        renovation = st.number_input("Reforma y preparación inicial (€)", min_value=0.0)
        other = st.number_input("Otros costes iniciales (€)", min_value=0.0)
        rent = st.number_input("Renta mensual hipotética (€)", min_value=0.0)
        months = st.number_input(
            "Meses con ingreso al año", min_value=0.0, max_value=12.0, value=11.0
        )
        operating = st.number_input("Gastos operativos anuales incluidos (€)", min_value=0.0)
        financing = st.number_input("Costes financieros anuales incluidos (€)", min_value=0.0)
        submitted = st.form_submit_button("Calcular simulación orientativa")

    if submitted:
        try:
            result = simulate_rental_investment(
                RentalSimulationInput(
                    purchase_price=purchase,
                    acquisition_costs=acquisition,
                    renovation_costs=renovation,
                    other_initial_costs=other,
                    monthly_rent=rent,
                    occupied_months_per_year=months,
                    annual_operating_costs=operating,
                    annual_financing_costs=financing,
                )
            )
        except ValueError as exc:
            st.error(str(exc))
            return
        formatted_cash_flow = format_eur(result.annual_cash_flow_after_financing)
        formatted_gross_yield = format_percentage(result.gross_yield_pct)
        formatted_net_yield = format_percentage(result.net_yield_before_financing_pct)
        text = f"""### Simulación orientativa

- Inversión inicial total: **{format_eur(result.total_initial_investment)}**
- Ingreso bruto anual supuesto: **{format_eur(result.annual_gross_income)}**
- Ingreso neto antes de financiación: **{format_eur(result.annual_net_income_before_financing)}**
- Flujo después del coste financiero introducido: **{formatted_cash_flow}**
- Rentabilidad bruta sobre inversión inicial: **{formatted_gross_yield}**
- Rentabilidad neta antes de financiación: **{formatted_net_yield}**

{result.disclaimer}
"""
        append_message("assistant", text)
        st.session_state.active_form = None
        st.rerun()


def render_flip_form() -> None:
    with st.form("flip_simulation"):
        st.subheader("Simulación orientativa: compra, reforma y venta")
        st.caption("Utiliza cifras hipotéticas y no introduzcas datos personales.")
        purchase = st.number_input("Precio de compra supuesto (€)", min_value=0.0, step=1_000.0)
        acquisition = st.number_input("Gastos de adquisición incluidos (€)", min_value=0.0)
        renovation = st.number_input("Presupuesto de reforma (€)", min_value=0.0)
        contingency = st.number_input("Contingencia de reforma (€)", min_value=0.0)
        holding = st.number_input("Costes de mantenimiento incluidos (€)", min_value=0.0)
        financing = st.number_input("Costes de financiación incluidos (€)", min_value=0.0)
        selling = st.number_input("Comercialización y transmisión incluidas (€)", min_value=0.0)
        other = st.number_input("Otros costes (€)", min_value=0.0)
        sale = st.number_input("Precio de venta hipotético (€)", min_value=0.0, step=1_000.0)
        submitted = st.form_submit_button("Calcular simulación orientativa")

    if submitted:
        try:
            result = simulate_renovate_and_sell(
                RenovateAndSellInput(
                    purchase_price=purchase,
                    acquisition_costs=acquisition,
                    renovation_budget=renovation,
                    renovation_contingency=contingency,
                    holding_costs=holding,
                    financing_costs=financing,
                    selling_costs=selling,
                    other_costs=other,
                    estimated_sale_price=sale,
                )
            )
        except ValueError as exc:
            st.error(str(exc))
            return
        text = f"""### Simulación orientativa

- Coste total del proyecto: **{format_eur(result.total_project_cost)}**
- Precio de venta hipotético: **{format_eur(result.estimated_sale_price)}**
- Resultado orientativo: **{format_eur(result.orientative_result)}**
- Margen sobre el precio de venta: **{format_percentage(result.margin_on_sale_pct)}**
- Retorno sobre el coste total: **{format_percentage(result.return_on_total_cost_pct)}**

{result.disclaimer}
"""
        append_message("assistant", text)
        st.session_state.active_form = None
        st.rerun()


def main() -> None:
    st.set_page_config(page_title="Asistente Vissotia", page_icon="🏠", layout="centered")
    ensure_session()

    st.title("Asistente Vissotia")
    st.caption("Descubre cómo Vissotia conecta datos, contexto y decisiones inmobiliarias.")
    st.info(
        "Asistente demostrativo con información pública. No accede a cuentas, clientes ni "
        "inmuebles registrados en Vissotia."
    )

    with st.sidebar:
        st.header("Tu perfil")
        selected_label = st.selectbox(
            "Selecciona cómo quieres que adapte la explicación",
            options=list(PROFILE_LABELS),
            index=None,
            placeholder="Selecciona un perfil",
        )
        selected_profile = PROFILE_LABELS.get(selected_label) if selected_label else None
        if selected_profile != st.session_state.selected_profile:
            st.session_state.selected_profile = selected_profile
            reset_conversation()
        if st.button("Nueva conversación", use_container_width=True):
            reset_conversation()
            st.rerun()
        st.divider()
        st.caption("No introduzcas datos personales, direcciones ni documentación real.")

    if not st.session_state.selected_profile:
        st.warning("Selecciona un perfil para comenzar.")
        return

    if not st.session_state.chat_history:
        st.subheader("Puedes empezar por aquí")
        columns = st.columns(2)
        for index, prompt in enumerate(QUICK_PROMPTS):
            if columns[index % 2].button(prompt, key=f"quick_{index}", use_container_width=True):
                process_query(prompt)
                st.rerun()

    render_history()

    if st.session_state.active_form == "open_rental_form":
        render_rental_form()
    elif st.session_state.active_form == "open_renovate_sell_form":
        render_flip_form()

    if prompt := st.chat_input("Escribe tu pregunta sobre Vissotia"):
        process_query(prompt)
        st.rerun()

    st.divider()
    cta_columns = st.columns(3)
    cta_columns[0].link_button(
        "Solicitar una demo", "https://vissotia.es/solicitar-demo", use_container_width=True
    )
    cta_columns[1].link_button(
        "Acceder / registrarse", "https://vissotia.es/app", use_container_width=True
    )
    cta_columns[2].link_button(
        "Contactar con soporte", "mailto:jobdelgadoi@vissotia.es", use_container_width=True
    )


if __name__ == "__main__":
    main()
