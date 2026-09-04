from __future__ import annotations

import streamlit as st


_LOGIN_STYLE = """
<style>
/* Pantalla de acceso: réplica visual del extractor-catalogos-presupuestos. */
[data-testid="stHeader"] {
    display: none !important;
}

.block-container {
    padding-top: 1rem !important;
}

.login-shell {
    max-width: 650px;
    margin: 9vh auto 0 auto;
    background: #FFFFFF;
    border: 1px solid #E7DED9;
    border-top: 6px solid #FF5E12;
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 18px 48px rgba(0, 48, 79, 0.14);
}

.login-shell h1 {
    color: #00304F;
    margin-bottom: 0.4rem;
}

.login-shell p {
    color: #362D32;
}

.login-shell .muted-note {
    color: #756B70;
    font-size: 0.86rem;
}

/* El botón usa el mismo patrón del extractor: naranja, centrado y ancho. */
[data-testid="stButton"] > button {
    background: #FF5E12 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    min-height: 2.75rem !important;
    font-weight: 700 !important;
}

[data-testid="stButton"] > button:hover {
    background: #FF7D42 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(255, 94, 18, 0.17);
}
</style>
"""


def render_login_page() -> None:
    st.markdown(_LOGIN_STYLE, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="login-shell">
            <h1>ASEG | Análisis de Ejecución</h1>
            <p>Acceso exclusivo para usuarios autorizados.</p>
            <p class="muted-note">La aplicación solamente solicitará nombre y correo verificado.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1, 1])
    with center:
        st.button(
            "Ingresar con Google",
            type="primary",
            use_container_width=True,
            on_click=st.login,
        )
