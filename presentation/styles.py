from __future__ import annotations

from pathlib import Path

import streamlit as st


ROOT_PATH = Path(__file__).resolve().parents[1]
STYLE_PATHS = (
    ROOT_PATH / "estilos.css",
    ROOT_PATH / "assets" / "ui_overrides.css",
)


def load_styles() -> None:
    css_parts: list[str] = []

    for style_path in STYLE_PATHS:
        try:
            css_parts.append(style_path.read_text(encoding="utf-8"))
        except OSError:
            continue

    if not css_parts:
        return

    st.markdown(
        f"<style>{'\n'.join(css_parts)}</style>",
        unsafe_allow_html=True,
    )
