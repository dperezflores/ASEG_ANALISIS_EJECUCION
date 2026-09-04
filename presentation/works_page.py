from __future__ import annotations

from datetime import datetime

import streamlit as st

from application.services.work_service import WorkService
from domain.users import User
from domain.works import NewWork, Work


def _work_label(work: Work) -> str:
    contract = work.contract_number or "Sin número de contrato"
    return f"{work.name} · {contract}"


def _render_work_card(work: Work, user: User, service: WorkService) -> None:
    with st.container(border=True):
        st.markdown(f"**{work.name}**")
        st.caption(f"Contrato: {work.contract_number or 'Sin número de contrato'}")
        if work.entity:
            st.caption(f"Ente: {work.entity}")
        if work.contractor:
            st.caption(f"Contratista: {work.contractor}")
        if work.fiscal_year:
            st.caption(f"Ejercicio: {work.fiscal_year}")

        col_open, col_archive = st.columns([1, 1])
        if col_open.button("Abrir", key=f"open_work_{work.id}", type="primary", use_container_width=True):
            st.session_state.active_work_id = str(work.id)
            st.session_state.active_work_name = work.name
            st.session_state.historial = {
                categoria: [] for categoria in st.session_state.historial
            }
            st.session_state.procesados = set()
            st.rerun()

        if col_archive.button("Archivar", key=f"archive_work_{work.id}", use_container_width=True):
            service.archive(work.id, user.id)
            st.rerun()


def _render_create_form(user: User, service: WorkService) -> None:
    with st.expander("➕ Crear nueva obra", expanded=False):
        with st.form("create_work_form", clear_on_submit=True):
            name = st.text_input("Nombre de la obra *")
            contract_number = st.text_input("Número de contrato")
            entity = st.text_input("Ente")
            contractor = st.text_input("Contratista")
            fiscal_year = st.number_input(
                "Ejercicio",
                min_value=2000,
                max_value=2100,
                value=datetime.now().year,
                step=1,
            )
            description = st.text_area("Descripción")
            submitted = st.form_submit_button("Guardar obra", type="primary")

        if submitted:
            try:
                service.create(
                    user.id,
                    NewWork(
                        name=name,
                        contract_number=contract_number,
                        entity=entity,
                        contractor=contractor,
                        fiscal_year=int(fiscal_year),
                        description=description,
                    ),
                )
                st.success("Obra registrada correctamente.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))


def _render_archived(user: User, service: WorkService) -> None:
    archived = service.list_archived(user.id)
    if not archived:
        return

    with st.expander("Obras archivadas", expanded=False):
        for work in archived:
            cols = st.columns([5, 1, 1])
            cols[0].write(_work_label(work))
            if cols[1].button("Restaurar", key=f"restore_work_{work.id}"):
                service.restore(work.id, user.id)
                st.rerun()
            if cols[2].button("Eliminar", key=f"delete_work_{work.id}"):
                st.session_state[f"confirm_delete_{work.id}"] = True

            if st.session_state.get(f"confirm_delete_{work.id}"):
                st.warning(f"Esta acción eliminará permanentemente: {work.name}")
                confirm, cancel = st.columns(2)
                if confirm.button("Confirmar eliminación", key=f"confirm_delete_btn_{work.id}"):
                    service.delete(work.id, user.id)
                    st.session_state.pop(f"confirm_delete_{work.id}", None)
                    st.rerun()
                if cancel.button("Cancelar", key=f"cancel_delete_btn_{work.id}"):
                    st.session_state.pop(f"confirm_delete_{work.id}", None)
                    st.rerun()


def render_works_page(user: User, service: WorkService) -> None:
    st.markdown("### Mis obras")
    st.caption(f"Sesión iniciada como {user.name} · {user.email}")

    col_create, col_logout = st.columns([5, 1])
    with col_logout:
        st.button("Cerrar sesión", on_click=st.logout, use_container_width=True)

    _render_create_form(user, service)

    works = service.list_active(user.id)
    if not works:
        st.info("Aún no tiene obras activas registradas.")
    else:
        for work in works:
            _render_work_card(work, user, service)

    _render_archived(user, service)
