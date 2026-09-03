from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


TABLE_STYLE_PATH = Path(__file__).resolve().parents[1] / "assets" / "table.css"

REPORT_TITLES = {
    "Estimaciones": "Reporte Consolidado de Estimaciones",
    "Facturas": "Reporte de Facturas",
    "Comprobantes de Pago": "Reporte Consolidado de Comprobantes de Pago",
    "Pólizas Devengo": "Análisis de Pólizas - DEVENGO",
    "Pólizas Pago": "Análisis de Pólizas - PAGO",
}

CURRENCY_COLUMNS = {
    "Importe sin IVA",
    "IVA",
    "Importe con IVA",
    "Importe de anticipo",
    "Amortización",
    "Deducciones",
    "Sancion",
    "Retencion",
    "Alcance neto",
    "Monto total",
    "Importe",
    "Importe (Devengo)",
    "Importe (Pago)",
}


def _format_date(value) -> str:
    months = {
        1: "ene", 2: "feb", 3: "mar", 4: "abr",
        5: "may", 6: "jun", 7: "jul", 8: "ago",
        9: "sep", 10: "oct", 11: "nov", 12: "dic",
    }
    if pd.isnull(value) or not hasattr(value, "year") or value.year <= 1900:
        return ""
    return f"{value.day:02d}-{months[value.month]}-{value.year}"


def _highlight_total(row):
    is_total = any(
        str(value) in {"TOTAL CONSOLIDADO", "TOTAL"}
        for value in row.values
    )
    style = (
        "font-weight:bold;background-color:#F2F2F2 !important;"
        "color:black !important;"
    )
    return [style if is_total else ""] * len(row)


def render_report_table(df: pd.DataFrame, report_type: str) -> None:
    if df.empty:
        return

    if "Archivo Origen" in df.columns:
        df = df[
            [c for c in df.columns if c != "Archivo Origen"] + ["Archivo Origen"]
        ].copy()

    currency = [c for c in df.columns if c in CURRENCY_COLUMNS]
    dates = [c for c in df.columns if "Fecha" in c or "Periodo" in c]
    formats = {column: "${:,.2f}" for column in currency}
    formats.update({column: _format_date for column in dates})

    html_table = (
        df.style
        .apply(_highlight_total, axis=1)
        .format(formats, na_rep="")
        .hide(axis="index")
        .to_html()
    )

    st.markdown(
        (
            '<div class="report-title">'
            f'<h2>{REPORT_TITLES.get(report_type, report_type)}</h2>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    css = TABLE_STYLE_PATH.read_text(encoding="utf-8")
    html = (
        "<html><head><style>"
        f"{css}"
        "</style></head><body>"
        f'<div class="table-wrapper">{html_table}</div>'
        "</body></html>"
    )
    components.html(
        html,
        height=min(480, ((len(df) + 1) * 40) + 25),
        scrolling=False,
    )
