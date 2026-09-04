from __future__ import annotations

import streamlit as st


def render_setup_required(missing: list[str]) -> None:
    st.markdown("### Configuración requerida")
    st.warning(
        "La aplicación está preparada para autenticación Google y persistencia "
        "en Neon, pero faltan secretos del despliegue."
    )
    st.write("Configure en Streamlit Cloud:")
    for item in missing:
        st.code(item)
    st.caption(
        "Los valores reales deben almacenarse en Secrets de Streamlit Cloud y "
        "nunca dentro del repositorio GitHub."
    )
