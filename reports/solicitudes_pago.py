from __future__ import annotations

import io

import pandas as pd


COLUMNAS_SOLICITUDES_PAGO = [
    "Número de solicitud",
    "Fecha de solicitud",
    "Estimación",
    "Archivo Origen",
]


def _ordenar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    for columna in COLUMNAS_SOLICITUDES_PAGO:
        if columna not in df.columns:
            df[columna] = "NO INDICA" if columna == "Estimación" else None
    return df[COLUMNAS_SOLICITUDES_PAGO].copy()


def reporte_solicitudes_pago(datos: list[dict]):
    df = pd.DataFrame(datos)

    if "Fecha de solicitud" in df.columns:
        df["Fecha de solicitud"] = pd.to_datetime(
            df["Fecha de solicitud"],
            errors="coerce",
        )
        df = df.sort_values(
            ["Fecha de solicitud"],
            ascending=True,
            na_position="last",
            kind="stable",
        ).reset_index(drop=True)

    if "Estimación" in df.columns:
        df["Estimación"] = df["Estimación"].fillna("NO INDICA")
        df.loc[df["Estimación"].astype(str).str.strip() == "", "Estimación"] = "NO INDICA"

    df = df.map(lambda x: x.upper() if isinstance(x, str) else x)
    df = _ordenar_columnas(df)

    output = io.BytesIO()
    with pd.ExcelWriter(
        output,
        engine="xlsxwriter",
        datetime_format="dd-mmm-yyyy",
    ) as writer:
        df.to_excel(writer, index=False, sheet_name="Solicitudes de Pago")
        ws = writer.sheets["Solicitudes de Pago"]
        formato_fecha = writer.book.add_format(
            {"num_format": "[$-es-MX]dd-mmm-yyyy;@"}
        )

        for i, columna in enumerate(df.columns):
            if columna == "Fecha de solicitud":
                ws.set_column(i, i, 18, formato_fecha)
            elif columna == "Número de solicitud":
                ws.set_column(i, i, 24)
            elif columna == "Estimación":
                ws.set_column(i, i, 20)
            else:
                ws.set_column(i, i, 32)

    return df, output.getvalue()
