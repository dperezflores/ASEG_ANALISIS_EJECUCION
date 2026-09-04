from __future__ import annotations

import streamlit as st


def render_app_header() -> None:
    """Renderiza el encabezado institucional propio de la aplicación."""
    st.markdown(
        """
        <header class="app-header" role="banner">
            <div class="app-header__content">
                <span class="app-header__brand">🏗️ ASEG | Análisis de Ejecución</span>
            </div>
        </header>
        """,
        unsafe_allow_html=True,
    )
