from __future__ import annotations

import streamlit as st


def render_login_page() -> None:
    st.markdown("### ASEG | Análisis de Ejecución")
    st.caption("Inicie sesión con su cuenta de Google para continuar.")
    st.button("Continuar con Google", on_click=st.login, type="primary")
