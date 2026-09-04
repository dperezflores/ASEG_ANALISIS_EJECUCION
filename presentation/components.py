from __future__ import annotations

import html

import streamlit as st


def render_page_hero(
    title: str,
    subtitle: str | None = None,
    eyebrow: str | None = None,
) -> None:
    del eyebrow
    subtitle_html = (
        f"<p>{html.escape(subtitle)}</p>" if subtitle else ""
    )
    st.markdown(
        f"""
        <section class="institutional-header">
            <h1>{html.escape(title)}</h1>
            {subtitle_html}
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_section_heading(title: str, description: str | None = None) -> None:
    description_html = (
        f"<p>{html.escape(description)}</p>" if description else ""
    )
    st.markdown(
        f"""
        <div class="aseg-section-heading">
            <h3>{html.escape(title)}</h3>
            {description_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
