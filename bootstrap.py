from __future__ import annotations

from uuid import UUID

import streamlit as st

from application.session import clear_active_work, initialize_session
from composition import build_auth_service, build_work_service
from config.settings import get_secret, get_settings
from infrastructure.auth.streamlit_oidc import identity_from_streamlit_user
from presentation.app_header import render_app_header
from presentation.login_page import render_login_page
from presentation.main_page import render_main_page
from presentation.setup_page import render_setup_required
from presentation.styles import load_styles
from presentation.works_page import render_works_page


def _missing_runtime_secrets() -> list[str]:
    missing: list[str] = []

    if not get_secret("DATABASE_URL", "").strip():
        missing.append("DATABASE_URL")

    try:
        auth = st.secrets.get("auth", {})
    except Exception:
        auth = {}

    for key in (
        "redirect_uri",
        "cookie_secret",
        "client_id",
        "client_secret",
        "server_metadata_url",
    ):
        if not auth or not str(auth.get(key, "")).strip():
            missing.append(f"auth.{key}")

    return missing


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

    missing = _missing_runtime_secrets()
    if missing:
        render_setup_required(missing)
        return

    if not st.user.is_logged_in:
        render_login_page()
        return

    try:
        identity = identity_from_streamlit_user(st.user)
        user = build_auth_service().sync_user(identity)
        work_service = build_work_service()
    except Exception as exc:
        st.error(f"No fue posible inicializar la sesión del usuario: {exc}")
        return

    st.session_state.current_user = user
    render_app_header()

    active_work = None
    if st.session_state.active_work_id:
        try:
            active_work = work_service.get_owned(
                UUID(st.session_state.active_work_id),
                user.id,
            )
        except (TypeError, ValueError):
            active_work = None

        if active_work is None or active_work.status.value != "ACTIVA":
            clear_active_work()
            active_work = None

    if active_work is None:
        render_works_page(user, work_service)
        return

    render_main_page(active_work)
