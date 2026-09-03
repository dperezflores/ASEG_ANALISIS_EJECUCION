from __future__ import annotations

import streamlit as st

from application.session import initialize_session
from config.settings import get_settings
from presentation.main_page import render_main_page
from presentation.styles import load_styles


def run() -> None:
    settings = get_settings()

    st.set_page_config(
        page_title=settings.page_title,
        page_icon=settings.page_icon,
        layout=settings.layout,
        initial_sidebar_state=settings.sidebar_state,
    )

    load_styles()
    initialize_session()
    render_main_page()
