from __future__ import annotations

import html

import streamlit as st


def render_page_hero(
    title: str,
    subtitle: str | None = None,
    eyebrow: str | None = None,
) -> None:
    eyebrow_html = (
        f'<div class="page-hero__eyebrow">{html.escape(eyebrow)}</div>'
        if eyebrow
        else ""
    )
    subtitle_html = (
        f'<p class="page-hero__subtitle">{html.escape(subtitle)}</p>'
        if subtitle
        else ""
    )
    st.markdown(
        f"""
        <section class="page-hero">
            {eyebrow_html}
            <h1>{html.escape(title)}</h1>
            {subtitle_html}
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_section_heading(title: str, description: str | None = None) -> None:
    description_html = (
        f'<p>{html.escape(description)}</p>' if description else ""
    )
    st.markdown(
        f"""
        <div class="section-heading">
            <h2>{html.escape(title)}</h2>
            {description_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
