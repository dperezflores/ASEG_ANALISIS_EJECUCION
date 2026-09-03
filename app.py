from __future__ import annotations

import hashlib
import os

import streamlit as st

from core.analyzers import analizar
from providers.gemini import GeminiProvider
from reports import excel as generador_excel
from ui.components import cargar_css, renderizar_tabla_html


st.set_page_config(
    page_title="ASEG - Análisis de Ejecución",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)
cargar_css()

CATEGORIAS = ["Estimaciones", "Facturas", "Comprobantes de Pago", "Pólizas"]


def _secreto(nombre: str, default: str = "") -> str:
    try:
        return str(st.secrets.get(nombre, default))
    except Exception:
        return os.getenv(nombre, default)


def _huella(archivo) -> str:
    return hashlib.sha256(archivo.getvalue()).hexdigest()


def _estado_inicial():
    st.session_state.setdefault("historial", {categoria: [] for categoria in CATEGORIAS})
    st.session_state.setdefault("procesados", set())
    st.session_state.setdefault("api_key", "")
    st.session_state.setdefault("modelo", _secreto("GEMINI_MODEL", "gemini-2.5-flash"))


def _procesar_categoria(categoria: str, archivos, provider: GeminiProvider):
    pendientes = []
    omitidos = 0
    for archivo in archivos:
        clave = f"{categoria}:{_huella(archivo)}:{provider.model_name}"
        if clave in st.session_state.procesados:
            omitidos += 1
        else:
            pendientes.append((archivo, clave))

    if not pendientes:
        if omitidos:
            st.info(f"{omitidos} archivo(s) ya tenían un resultado vigente en esta sesión.")
        return

    barra = st.progress(0, text=f"Preparando {len(pendientes)} documento(s)...")
    exitos = errores = 0
    for i, (archivo, clave) in enumerate(pendientes, start=1):
        barra.progress((i - 1) / len(pendientes), text=f"🤖 Analizando ({i}/{len(pendientes)}): {archivo.name}")
        resultado = analizar(provider, categoria, archivo)
        if resultado.estado != "OK":
            st.error(f"❌ {archivo.name}: {'; '.join(resultado.errores)}")
            errores += 1
            continue
        for registro in resultado.datos:
            registro["Archivo Origen"] = archivo.name
        st.session_state.historial[categoria].extend(resultado.datos)
        st.session_state.procesados.add(clave)
        exitos += 1
        barra.progress(i / len(pendientes), text=f"Procesados {i} de {len(pendientes)} documento(s)")
    barra.empty()
    if exitos:
        st.success(f"✅ Documentos analizados correctamente: {exitos}.")
    if errores:
        st.error(f"⚠️ Documentos con error: {errores}.")
    if omitidos:
        st.info(f"ℹ️ Documentos omitidos por resultado vigente: {omitidos}.")


def _mostrar_resultados():
    resultados = {}
    for categoria in CATEGORIAS:
        datos = st.session_state.historial.get(categoria, [])
        if not datos:
            continue
        if categoria == "Estimaciones":
            df, xls = generador_excel.reporte_estimaciones(datos)
            resultados[categoria] = {"df": df, "xls": xls}
        elif categoria == "Facturas":
            df, xls = generador_excel.reporte_facturas(datos)
            resultados[categoria] = {"df": df, "xls": xls}
        elif categoria == "Comprobantes de Pago":
            df, xls = generador_excel.reporte_comprobantes(datos)
            resultados[categoria] = {"df": df, "xls": xls}
        else:
            dev, pag, xls = generador_excel.reporte_polizas(datos)
            resultados[categoria] = {"df_dev": dev, "df_pag": pag, "xls": xls}

    if not resultados:
        st.info("Cargue y analice documentos para generar los reportes.")
        return

    tabs = st.tabs([f"📊 {nombre}" for nombre in resultados])
    for tab, (nombre, reporte) in zip(tabs, resultados.items()):
        with tab:
            st.download_button(
                f"📥 Descargar {nombre}",
                data=reporte["xls"],
                file_name=f"Reporte_{nombre}.xlsx",
                key=f"descarga_{nombre}",
            )
            if nombre == "Pólizas":
                renderizar_tabla_html(reporte["df_dev"], "Pólizas Devengo")
                renderizar_tabla_html(reporte["df_pag"], "Pólizas Pago")
            else:
                renderizar_tabla_html(reporte["df"], nombre)


def main():
    _estado_inicial()
    st.markdown("### Análisis documental de ejecución")
    st.caption("Versión independiente de Estimaciones, Facturas, Comprobantes de Pago y Pólizas.")

    with st.sidebar:
        st.header("📂 Documentación")
        with st.expander("⚙️ Configuración de IA", expanded=True):
            st.selectbox("Proveedor", ["Gemini"], disabled=True)
            st.session_state.modelo = st.text_input("Modelo", value=st.session_state.modelo)
            clave_preconfigurada = _secreto("GEMINI_API_KEY", "")
            st.session_state.api_key = st.text_input(
                "API Key",
                value=st.session_state.api_key or clave_preconfigurada,
                type="password",
                help="En esta fase la clave vive únicamente en la sesión de Streamlit.",
            )

        archivos_por_categoria = {}
        for categoria in CATEGORIAS:
            with st.expander(f"📁 {categoria}", expanded=False):
                archivos = st.file_uploader(
                    categoria,
                    type=["pdf"],
                    accept_multiple_files=True,
                    key=f"up_{categoria}",
                    label_visibility="collapsed",
                )
                archivos_por_categoria[categoria] = archivos or []
                for archivo in archivos or []:
                    st.caption(f"📄 {archivo.name}")

    seleccionables = []
    indice_archivos = {}
    for categoria, archivos in archivos_por_categoria.items():
        for archivo in archivos:
            etiqueta = f"{archivo.name} (en {categoria})"
            seleccionables.append(etiqueta)
            indice_archivos[etiqueta] = (categoria, archivo)

    if seleccionables:
        st.markdown("#### Centro de análisis")
        seleccion = st.multiselect("Seleccione los archivos a analizar:", seleccionables)
        if st.button("🚀 Procesar selección", type="primary"):
            if not seleccion:
                st.warning("Seleccione al menos un archivo.")
            elif not st.session_state.api_key.strip():
                st.error("Capture una clave API de Gemini antes de procesar.")
            else:
                provider = GeminiProvider(st.session_state.api_key, st.session_state.modelo)
                agrupados = {categoria: [] for categoria in CATEGORIAS}
                for etiqueta in seleccion:
                    categoria, archivo = indice_archivos[etiqueta]
                    agrupados[categoria].append(archivo)
                for categoria, archivos in agrupados.items():
                    if archivos:
                        _procesar_categoria(categoria, archivos, provider)
    else:
        st.warning("No hay documentos cargados en las carpetas de ejecución.")

    st.markdown("---")
    _mostrar_resultados()


if __name__ == "__main__":
    main()
