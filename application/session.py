from __future__ import annotations

import streamlit as st

from config.settings import get_secret
from domain.categories import CATEGORIAS


def initialize_session() -> None:
    st.session_state.setdefault(
        "historial",
        {categoria: [] for categoria in CATEGORIAS},
    )
    st.session_state.setdefault("procesados", set())
    st.session_state.setdefault("api_key", "")
    st.session_state.setdefault(
        "modelo",
        get_secret("GEMINI_MODEL", "gemini-2.5-flash"),
    )
    st.session_state.setdefault("current_user", None)
    st.session_state.setdefault("active_work_id", None)
    st.session_state.setdefault("active_work_name", None)
    st.session_state.setdefault("hydrated_work_id", None)
    st.session_state.setdefault("saved_analyses", [])


def get_history(categoria: str) -> list[dict]:
    return st.session_state.historial.get(categoria, [])


def append_history(categoria: str, registros: list[dict]) -> None:
    st.session_state.historial[categoria].extend(registros)


def is_processed(key: str) -> bool:
    return key in st.session_state.procesados


def mark_processed(key: str) -> None:
    st.session_state.procesados.add(key)


def register_saved_analysis(record: dict) -> None:
    current = [
        item
        for item in st.session_state.saved_analyses
        if not (
            item.get("categoria") == record.get("categoria")
            and item.get("archivo_hash") == record.get("archivo_hash")
        )
    ]
    current.append(dict(record))
    current.sort(
        key=lambda item: (
            str(item.get("categoria", "")),
            str(item.get("archivo_nombre", "")),
        )
    )
    st.session_state.saved_analyses = current


def restore_persisted_history(
    work_id: str,
    history_by_category: dict[str, list[dict]],
    processed_keys: set[str],
    saved_analyses: list[dict] | None = None,
) -> None:
    st.session_state.historial = {
        categoria: list(history_by_category.get(categoria, []))
        for categoria in CATEGORIAS
    }
    st.session_state.procesados = set(processed_keys)
    st.session_state.saved_analyses = list(saved_analyses or [])
    st.session_state.hydrated_work_id = work_id


def clear_active_work() -> None:
    st.session_state.active_work_id = None
    st.session_state.active_work_name = None
    st.session_state.historial = {categoria: [] for categoria in CATEGORIAS}
    st.session_state.procesados = set()
    st.session_state.hydrated_work_id = None
    st.session_state.saved_analyses = []

    for key in list(st.session_state.keys()):
        if (
            key.startswith("up_")
            or key.startswith("confirm_delete_")
            or key.startswith("confirm_analysis_delete_")
        ):
            st.session_state.pop(key, None)
