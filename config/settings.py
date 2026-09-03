from __future__ import annotations

import os
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class AppSettings:
    page_title: str = "ASEG - Análisis de Ejecución"
    page_icon: str = "🏗️"
    layout: str = "wide"
    sidebar_state: str = "expanded"
    default_gemini_model: str = "gemini-2.5-flash"


def get_secret(name: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return os.getenv(name, default)


def get_settings() -> AppSettings:
    return AppSettings()
