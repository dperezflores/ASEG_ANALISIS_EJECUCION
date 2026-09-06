from __future__ import annotations

import streamlit as st

from config.settings import get_secret
from domain.categories import CATEGORIAS


def _refresh_workspace() -> None:
    """Actualiza sólo los fragmentos vinculados a carga documental."""
    st.rerun(["sidebar_controls", "analysis_workspace"])


@st.fragment(key="sidebar_controls")
def _render_sidebar_contents() -> None:
    st.header("📂 Documentación")

    with st.expander("Configuración de IA", expanded=True):
        st.selectbox("Proveedor", ["Gemini"], disabled=True)

        st.text_input(
            "Modelo",
            key="modelo",
            on_change="ignore",
        )

        clave_preconfigurada = get_secret("GEMINI_API_KEY", "")
        if not st.session_state.get("api_key") and clave_preconfigurada:
            st.session_state.api_key = clave_preconfigurada

        st.text_input(
            "API Key",
            key="api_key",
            type="password",
            help="En esta fase la clave vive únicamente en la sesión de Streamlit.",
            on_change="ignore",
        )

    for categoria in CATEGORIAS:
        with st.expander(f"📁 {categoria}", expanded=False):
            files = st.file_uploader(
                categoria,
                type=["pdf"],
                accept_multiple_files=True,
                key=f"up_{categoria}",
                label_visibility="collapsed",
                on_change=_refresh_workspace,
            )
            for file in files or []:
                st.caption(f"📄 {file.name}")


def render_sidebar() -> None:
    with st.sidebar:
        _render_sidebar_contents()
