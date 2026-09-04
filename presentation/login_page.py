from __future__ import annotations

import streamlit as st


def render_login_page() -> None:
    st.markdown(
        """
        <div class="login-shell">
            <h1>ASEG | Análisis de Ejecución</h1>
            <p>Acceso exclusivo para usuarios autorizados.</p>
            <p class="muted-note">
                La aplicación solamente solicitará nombre y correo verificado.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.button(
            "Ingresar con Google",
            type="primary",
            use_container_width=True,
            on_click=st.login,
        )
