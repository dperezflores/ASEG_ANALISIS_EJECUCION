from __future__ import annotations

from collections import defaultdict

import streamlit as st

from application.session import clear_active_work
from composition import build_analysis_service
from domain.categories import CATEGORIAS
from domain.works import Work
from presentation.components import render_page_hero, render_section_heading
from presentation.results import render_results
from presentation.sidebar import render_sidebar


def _build_file_index(files_by_category: dict[str, list]):
    labels: list[str] = []
    index: dict[str, tuple[str, object]] = {}

    for categoria, files in files_by_category.items():
        for file in files:
            label = f"{file.name} (en {categoria})"
            labels.append(label)
            index[label] = (categoria, file)

    return labels, index


def _process_selection(selection, file_index) -> None:
    if not selection:
        st.warning("Seleccione al menos un archivo.")
        return

    if not st.session_state.api_key.strip():
        st.error("Capture una clave API de Gemini antes de procesar.")
        return

    service = build_analysis_service(
        st.session_state.api_key,
        st.session_state.modelo,
    )

    grouped = defaultdict(list)
    for label in selection:
        categoria, file = file_index[label]
        grouped[categoria].append(file)

    total_files = sum(len(files) for files in grouped.values())
    processed = 0
    successes = errors = skipped = 0
    progress = st.progress(0, text=f"Preparando {total_files} documento(s)...")

    for categoria in CATEGORIAS:
        for file in grouped.get(categoria, []):
            progress.progress(
                processed / total_files,
                text=f"🤖 Analizando ({processed + 1}/{total_files}): {file.name}",
            )
            result, was_skipped = service.process_file(categoria, file)
            processed += 1

            if was_skipped:
                skipped += 1
            elif result and result.estado == "OK":
                successes += 1
            else:
                errors += 1
                if result:
                    st.error(f"❌ {file.name}: {'; '.join(result.errores)}")

            progress.progress(
                processed / total_files,
                text=f"Procesados {processed} de {total_files} documento(s)",
            )

    progress.empty()

    if successes:
        st.success(f"✅ Documentos analizados correctamente: {successes}.")
    if errors:
        st.error(f"⚠️ Documentos con error: {errors}.")
    if skipped:
        st.info(f"ℹ️ Documentos omitidos por resultado vigente: {skipped}.")


def _logout() -> None:
    clear_active_work()
    st.logout()


def render_main_page(active_work: Work) -> None:
    title_col, change_work_col, logout_col = st.columns([5, 1, 1])

    with title_col:
        subtitle = f"Obra activa: {active_work.name}"
        if active_work.contract_number:
            subtitle += f" · Contrato: {active_work.contract_number}"
        render_page_hero(
            "Análisis documental de ejecución",
            subtitle=subtitle,
        )

    with change_work_col:
        st.write("")
        st.write("")
        if st.button("Cambiar obra", use_container_width=True):
            clear_active_work()
            st.rerun()

    with logout_col:
        st.write("")
        st.write("")
        st.button(
            "Cerrar sesión",
            on_click=_logout,
            use_container_width=True,
        )

    files_by_category = render_sidebar()
    labels, file_index = _build_file_index(files_by_category)

    if labels:
        render_section_heading(
            "Centro de análisis",
            "Seleccione los documentos cargados que desea procesar con IA.",
        )
        selection = st.multiselect(
            "Seleccione los archivos a analizar:",
            labels,
        )
        if st.button("🚀 Procesar selección", type="primary"):
            _process_selection(selection, file_index)
    else:
        st.warning("No hay documentos cargados en las carpetas de ejecución.")

    st.markdown("---")
    render_results()
