from __future__ import annotations

import streamlit as st

from config.settings import get_secret
from domain.categories import CATEGORIAS


def render_sidebar() -> dict[str, list]:
    with st.sidebar:
        st.header("📂 Documentación")

        with st.expander("Configuración de IA", expanded=True):
            st.selectbox("Proveedor", ["Gemini"], disabled=True)
            st.session_state.modelo = st.text_input(
                "Modelo",
                value=st.session_state.modelo,
            )
            clave_preconfigurada = get_secret("GEMINI_API_KEY", "")
            st.session_state.api_key = st.text_input(
                "API Key",
                value=st.session_state.api_key or clave_preconfigurada,
                type="password",
                help="En esta fase la clave vive únicamente en la sesión de Streamlit.",
            )

        files_by_category: dict[str, list] = {}
        for categoria in CATEGORIAS:
            with st.expander(f"📁 {categoria}", expanded=False):
                files = st.file_uploader(
                    categoria,
                    type=["pdf"],
                    accept_multiple_files=True,
                    key=f"up_{categoria}",
                    label_visibility="collapsed",
                )
                files_by_category[categoria] = files or []
                for file in files or []:
                    st.caption(f"📄 {file.name}")

    return files_by_category
