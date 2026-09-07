from __future__ import annotations

from collections import defaultdict
from uuid import UUID

import streamlit as st

from application.session import clear_active_work
from composition import build_analysis_history_service, build_analysis_service
from domain.categories import CATEGORIAS
from domain.works import Work
from presentation.components import render_page_hero, render_section_heading
from presentation.results import render_results
from presentation.sidebar import render_sidebar


def _files_by_category_from_state() -> dict[str, list]:
    return {
        categoria: list(st.session_state.get(f"up_{categoria}", []) or [])
        for categoria in CATEGORIAS
    }


def _build_file_index(files_by_category: dict[str, list]):
    labels: list[str] = []
    index: dict[str, tuple[str, object]] = {}

    for categoria, files in files_by_category.items():
        for file in files:
            label = f"{file.name} (en {categoria})"
            labels.append(label)
            index[label] = (categoria, file)

    return labels, index


def _process_selection(selection, file_index, work_id: UUID) -> None:
    if not selection:
        st.warning("Seleccione al menos un archivo.")
        return

    if not st.session_state.api_key.strip():
        st.error("Capture una clave API de Gemini antes de procesar.")
        return

    service = build_analysis_service(
        st.session_state.api_key,
        st.session_state.modelo,
        work_id,
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


def _show_analysis_delete_confirmation(categoria: str, archivo_hash: str) -> None:
    st.session_state[f"confirm_analysis_delete_{categoria}_{archivo_hash}"] = True


def _cancel_analysis_delete(categoria: str, archivo_hash: str) -> None:
    st.session_state.pop(
        f"confirm_analysis_delete_{categoria}_{archivo_hash}",
        None,
    )


def _delete_saved_analysis(
    work_id: UUID,
    categoria: str,
    archivo_hash: str,
    archivo_nombre: str,
) -> None:
    confirmation_key = f"confirm_analysis_delete_{categoria}_{archivo_hash}"
    try:
        deleted = build_analysis_history_service().delete_file_analysis(
            work_id,
            categoria,
            archivo_hash,
        )
        st.session_state.pop(confirmation_key, None)
        if deleted:
            st.session_state.analysis_delete_message = (
                "success",
                f"Análisis eliminado: {archivo_nombre}. Puede volver a procesar el documento.",
            )
        else:
            st.session_state.analysis_delete_message = (
                "warning",
                f"No se encontró un análisis persistido para {archivo_nombre}.",
            )
    except Exception as exc:
        st.session_state.analysis_delete_message = (
            "error",
            f"No fue posible eliminar el análisis de {archivo_nombre}: {exc}",
        )


def _render_saved_analyses(work_id: UUID) -> None:
    saved_analyses = list(st.session_state.get("saved_analyses", []) or [])
    if not saved_analyses:
        return

    with st.expander("Análisis guardados", expanded=False):
        st.caption(
            "Elimine un análisis si necesita volver a procesar el mismo documento. "
            "La eliminación afecta únicamente a ese archivo dentro de su categoría."
        )

        for item in saved_analyses:
            categoria = str(item.get("categoria") or "")
            archivo_hash = str(item.get("archivo_hash") or "")
            archivo_nombre = str(item.get("archivo_nombre") or "Documento")
            if not categoria or not archivo_hash:
                continue

            identity = f"{categoria}_{archivo_hash[:16]}"
            info_col, action_col = st.columns([8, 2], vertical_alignment="center")
            info_col.markdown(f"**{archivo_nombre}**  \n{categoria}")
            action_col.button(
                "Eliminar análisis",
                key=f"delete_analysis_{identity}",
                use_container_width=True,
                on_click=_show_analysis_delete_confirmation,
                args=(categoria, archivo_hash),
            )

            confirmation_key = f"confirm_analysis_delete_{categoria}_{archivo_hash}"
            if st.session_state.get(confirmation_key):
                st.warning(
                    f"Se eliminará el análisis guardado de **{archivo_nombre}** en "
                    f"**{categoria}**. Después podrá volver a procesarlo con IA."
                )
                confirm_col, cancel_col = st.columns(2)
                confirm_col.button(
                    "Confirmar eliminación",
                    key=f"confirm_delete_analysis_{identity}",
                    use_container_width=True,
                    on_click=_delete_saved_analysis,
                    args=(work_id, categoria, archivo_hash, archivo_nombre),
                )
                cancel_col.button(
                    "Cancelar",
                    key=f"cancel_delete_analysis_{identity}",
                    use_container_width=True,
                    on_click=_cancel_analysis_delete,
                    args=(categoria, archivo_hash),
                )

            st.divider()


def _logout() -> None:
    clear_active_work()
    st.logout()


@st.fragment(key="analysis_workspace")
def _render_analysis_workspace(work_id: UUID) -> None:
    delete_message = st.session_state.pop("analysis_delete_message", None)
    if delete_message:
        level, message = delete_message
        getattr(st, level)(message)

    files_by_category = _files_by_category_from_state()
    labels, file_index = _build_file_index(files_by_category)

    if labels:
        render_section_heading(
            "Centro de análisis",
            "Seleccione los documentos cargados que desea procesar con IA.",
        )
        selection = st.multiselect(
            "Seleccione los archivos a analizar:",
            labels,
            key="analysis_selection",
        )
        if st.button("🚀 Procesar selección", type="primary"):
            _process_selection(selection, file_index, work_id)
    else:
        st.warning("No hay documentos cargados en las carpetas de ejecución.")

    _render_saved_analyses(work_id)

    st.markdown("---")
    render_results()


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
        st.button(
            "Cambiar obra",
            on_click=clear_active_work,
            use_container_width=True,
        )

    with logout_col:
        st.write("")
        st.write("")
        st.button(
            "Cerrar sesión",
            key="logout_action",
            on_click=_logout,
            use_container_width=True,
        )

    render_sidebar()
    _render_analysis_workspace(active_work.id)
