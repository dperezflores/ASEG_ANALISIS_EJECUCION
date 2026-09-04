from __future__ import annotations

import html
from typing import Literal

import streamlit as st


MessageKind = Literal["success", "info", "warning", "danger"]

_ICONS = {
    "success": "✓",
    "info": "i",
    "warning": "!",
    "danger": "×",
}


def show_message(message: str, kind: MessageKind = "info") -> None:
    safe_message = html.escape(str(message))
    icon = _ICONS[kind]
    st.markdown(
        f"""
        <div class="app-alert app-alert--{kind}" role="alert">
            <span class="app-alert__icon" aria-hidden="true">{icon}</span>
            <span class="app-alert__text">{safe_message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def success(message: str) -> None:
    show_message(message, "success")


def info(message: str) -> None:
    show_message(message, "info")


def warning(message: str) -> None:
    show_message(message, "warning")


def error(message: str) -> None:
    show_message(message, "danger")
