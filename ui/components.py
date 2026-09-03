import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


def cargar_css(ruta="estilos.css"):
    try:
        with open(ruta, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except OSError:
        pass


def renderizar_tabla_html(df: pd.DataFrame, tipo_reporte: str):
    if df.empty:
        return
    if "Archivo Origen" in df.columns:
        df = df[[c for c in df.columns if c != "Archivo Origen"] + ["Archivo Origen"]].copy()
    meses = {1:'ene',2:'feb',3:'mar',4:'abr',5:'may',6:'jun',7:'jul',8:'ago',9:'sep',10:'oct',11:'nov',12:'dic'}
    def fmt_fec(d):
        if pd.isnull(d) or not hasattr(d, "year") or d.year <= 1900: return ""
        return f"{d.day:02d}-{meses[d.month]}-{d.year}"
    moneda = [c for c in df.columns if c in ["Importe sin IVA","IVA","Importe con IVA","Importe de anticipo","Amortización","Deducciones","Sancion","Retencion","Alcance neto","Monto total","Importe","Importe (Devengo)","Importe (Pago)"]]
    fechas = [c for c in df.columns if "Fecha" in c or "Periodo" in c]
    formatos = {c: "${:,.2f}" for c in moneda}
    formatos.update({c: fmt_fec for c in fechas})
    def highlight_total(row):
        es_total = any(str(v) in ["TOTAL CONSOLIDADO", "TOTAL"] for v in row.values)
        return ["font-weight:bold;background-color:#F2F2F2 !important;color:black !important;" if es_total else ""] * len(row)
    html_table = df.style.apply(highlight_total, axis=1).format(formatos, na_rep="").hide(axis="index").to_html()
    titulos = {
        "Estimaciones": "Reporte Consolidado de Estimaciones",
        "Facturas": "Reporte de Facturas",
        "Comprobantes de Pago": "Reporte Consolidado de Comprobantes de Pago",
        "Pólizas Devengo": "Análisis de Pólizas - DEVENGO",
        "Pólizas Pago": "Análisis de Pólizas - PAGO",
    }
    st.markdown(f'''<div style="padding:1px 20px;margin:10px 0 15px;background:white;border:1px solid #EAEAEA;box-shadow:inset 8px 0 0 0 #FF5E12,0 2px 5px rgba(0,0,0,.05);text-align:center"><h2 style="color:#00304F;margin:0;font-family:Arial;font-size:.8rem;font-weight:800;text-transform:uppercase">{titulos.get(tipo_reporte, tipo_reporte)}</h2></div>''', unsafe_allow_html=True)
    contenido = f'''<html><head><style>body{{font-family:Arial;margin:0}}.table-wrapper{{max-height:450px;overflow:auto;border:1px solid #D6D6D6;border-radius:6px}}table{{width:100%;border-collapse:collapse;font-size:11px;text-align:center;white-space:nowrap}}th{{background-color:#00304F!important;color:white!important;padding:10px;border-bottom:4px solid #FF5E12!important;position:sticky;top:0}}td{{padding:10px;border:1px solid #D6D6D6}}tr:nth-child(even){{background-color:#F9F9F9}}</style></head><body><div class="table-wrapper">{html_table}</div></body></html>'''
    components.html(contenido, height=min(480, ((len(df)+1)*40)+25), scrolling=False)
