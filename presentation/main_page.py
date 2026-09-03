from __future__ import annotations

from collections import defaultdict

import streamlit as st

from application.analysis_service import AnalysisService
from domain.categories import CATEGORIAS
from presentation.results import render_results
from presentation.sidebar import render_sidebar
from providers.gemini import GeminiProvider


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

    provider = GeminiProvider(
        st.session_state.api_key,
        st.session_state.modelo,
    )
    service = AnalysisService(provider)

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


def render_main_page() -> None:
    st.markdown("### Análisis documental de ejecución")
    st.caption(
        "Versión independiente de Estimaciones, Facturas, "
        "Comprobantes de Pago y Pólizas."
    )

    files_by_category = render_sidebar()
    labels, file_index = _build_file_index(files_by_category)

    if labels:
        st.markdown("#### Centro de análisis")
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
