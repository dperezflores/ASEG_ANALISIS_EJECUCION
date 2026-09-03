from __future__ import annotations

from pathlib import Path

import streamlit as st


STYLE_PATH = Path(__file__).resolve().parents[1] / "estilos.css"


def load_styles() -> None:
    try:
        st.markdown(
            f"<style>{STYLE_PATH.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )
    except OSError:
        pass
