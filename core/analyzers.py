from __future__ import annotations

from core.schemas import (
    ListaComprobantes,
    ListaEstimaciones,
    ListaFacturas,
    ListaPolizas,
    ResultadoExtraccion,
)


PROMPTS = {
    "Estimaciones": """
    Actúa como auditor de obra pública. Localiza todas las carátulas de estimación
    contenidas en el PDF y extrae un registro por cada una.

    Reglas:
    - Conserva el número de estimación exactamente como aparece.
    - Usa fechas en formato YYYY-MM-DD; si no existe una fecha usa 1900-01-01.
    - Importe de anticipo es el total otorgado para el contrato.
    - Amortización es únicamente el descuento aplicado en esa estimación.
    - No repitas un mismo importe entre deducciones, sanción y retención.
    - Si no aparece el importe con IVA, calcúlalo como importe sin IVA más IVA.
    - Para importes inexistentes utiliza 0.0.
    """,
    "Facturas": """
    Actúa como auditor de obra pública. Localiza todas las facturas o CFDI del PDF
    y extrae un registro por comprobante.

    Usa el UUID como folio, fechas YYYY-MM-DD y montos numéricos con IVA incluido.
    Para el orden de estimación usa el número identificado; usa 0 para anticipo y
    99 cuando el documento no permita determinarlo.
    """,
    "Comprobantes de Pago": """
    Actúa como auditor de obra pública y analista financiero. Localiza todos los
    comprobantes de pago, transferencias, cheques o SPEI del PDF.

    Extrae fecha efectiva de pago, importe, cuenta emisora, clave de rastreo,
    instituciones emisora y receptora y cuenta beneficiaria. Usa YYYY-MM-DD para
    fechas, 1900-01-01 si no existe, N/A para texto ausente y 0.0 para importes
    inexistentes.
    """,
    "Pólizas": """
    Actúa como auditor de obra pública y contador. Analiza todas las pólizas del
    PDF y clasifica cada registro como DEVENGO o PAGO.

    Para DEVENGO evita duplicar importes entre cuentas transitorias terminadas en
    09 y cuentas definitivas terminadas en 00. Prefiere la cuenta 00; usa la 09
    solamente cuando no exista la 00 e indícalo en el texto de la cuenta. Conserva
    registros separados cuando existan fondos distintos.

    Para PAGO toma el importe de la salida de bancos cuya cuenta inicia en 1112.
    Conserva ceros iniciales del número de póliza. Obtén el número de estimación de
    la referencia y usa NO INDICA cuando esté vacío. Usa fechas YYYY-MM-DD.
    """,
}

ESQUEMAS = {
    "Estimaciones": ListaEstimaciones,
    "Facturas": ListaFacturas,
    "Comprobantes de Pago": ListaComprobantes,
    "Pólizas": ListaPolizas,
}


def analizar(provider, categoria: str, archivo_pdf) -> ResultadoExtraccion:
    if categoria not in PROMPTS:
        raise ValueError(f"Categoría no soportada: {categoria}")
    return provider.analizar_pdf(archivo_pdf, PROMPTS[categoria], ESQUEMAS[categoria])
