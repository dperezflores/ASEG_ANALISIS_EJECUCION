from __future__ import annotations

import streamlit as st

from application.session import get_history
from domain.categories import CATEGORIAS, CategoriaDocumento
from reports import excel as report_builder
from ui.components import renderizar_tabla_html


def build_reports() -> dict[str, dict]:
    reports: dict[str, dict] = {}

    for categoria in CATEGORIAS:
        data = get_history(categoria)
        if not data:
            continue

        if categoria == CategoriaDocumento.ESTIMACIONES:
            df, xls = report_builder.reporte_estimaciones(data)
            reports[categoria] = {"df": df, "xls": xls}
        elif categoria == CategoriaDocumento.FACTURAS:
            df, xls = report_builder.reporte_facturas(data)
            reports[categoria] = {"df": df, "xls": xls}
        elif categoria == CategoriaDocumento.COMPROBANTES:
            df, xls = report_builder.reporte_comprobantes(data)
            reports[categoria] = {"df": df, "xls": xls}
        elif categoria == CategoriaDocumento.POLIZAS:
            dev, pag, xls = report_builder.reporte_polizas(data)
            reports[categoria] = {"df_dev": dev, "df_pag": pag, "xls": xls}

    return reports


def render_results() -> None:
    reports = build_reports()

    if not reports:
        st.info("Cargue y analice documentos para generar los reportes.")
        return

    tabs = st.tabs([f"📊 {name}" for name in reports])

    for tab, (name, report) in zip(tabs, reports.items()):
        with tab:
            st.download_button(
                f"📥 Descargar {name}",
                data=report["xls"],
                file_name=f"Reporte_{name}.xlsx",
                key=f"descarga_{name}",
            )

            if name == CategoriaDocumento.POLIZAS:
                renderizar_tabla_html(report["df_dev"], "Pólizas Devengo")
                renderizar_tabla_html(report["df_pag"], "Pólizas Pago")
            else:
                renderizar_tabla_html(report["df"], name)
