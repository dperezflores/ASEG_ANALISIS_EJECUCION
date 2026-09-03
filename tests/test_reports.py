from __future__ import annotations

import io
import unittest

import pandas as pd

from reports.excel import (
    COLUMNAS_COMPROBANTES,
    COLUMNAS_ESTIMACIONES,
    COLUMNAS_FACTURAS,
    COLUMNAS_POLIZAS_DEVENGO,
    COLUMNAS_POLIZAS_PAGO,
    reporte_comprobantes,
    reporte_estimaciones,
    reporte_facturas,
    reporte_polizas,
)


class ReportesTest(unittest.TestCase):
    def test_estimaciones_conservan_orden_institucional(self):
        tabla, excel = reporte_estimaciones([
            {"Numero de estimación":"EST. 2","Fecha de elaboración o de estimación":"2026-03-05","De (Periodo de ejecución)":"2026-02-01","Hasta (Periodo de ejecución)":"2026-02-28","Importe sin IVA":1000,"IVA":160,"Importe con IVA":1160,"Importe de anticipo":300,"Amortización":100,"Deducciones":20,"Sancion":0,"Retencion":10,"Archivo Origen":"2.pdf"},
            {"Numero de estimación":"EST. 1","Fecha de elaboración o de estimación":"2026-02-05","De (Periodo de ejecución)":"2026-01-01","Hasta (Periodo de ejecución)":"2026-01-31","Importe sin IVA":500,"IVA":80,"Importe con IVA":580,"Importe de anticipo":300,"Amortización":50,"Deducciones":10,"Sancion":0,"Retencion":5,"Archivo Origen":"1.pdf"},
        ])
        self.assertEqual(list(tabla.columns), COLUMNAS_ESTIMACIONES)
        self.assertEqual(list(tabla["Numero de estimación"]), ["EST. 1", "EST. 2"])
        self.assertEqual(list(pd.read_excel(io.BytesIO(excel)).columns), COLUMNAS_ESTIMACIONES)

    def test_facturas_comprobantes_y_polizas(self):
        facturas, _ = reporte_facturas([{"Folio":"F1","Descripción":"A","Fecha":"2026-01-01","Monto total":1,"Archivo Origen":"f.pdf"}])
        self.assertEqual(list(facturas.columns), COLUMNAS_FACTURAS)
        comprobantes, _ = reporte_comprobantes([{"Número":"1","Fecha de pago":"2026-01-01","Importe":1,"Archivo Origen":"c.pdf"}])
        self.assertEqual(list(comprobantes.columns), COLUMNAS_COMPROBANTES)
        dev, pag, _ = reporte_polizas([
            {"Tipo de poliza":"DEVENGO","Numero de estimacion":"EST 1","Fecha":"2026-01-01","Importe":1},
            {"Tipo de poliza":"PAGO","Numero de estimacion":"EST 1","Fecha":"2026-01-02","Importe":1},
        ])
        self.assertEqual(list(dev.columns), COLUMNAS_POLIZAS_DEVENGO)
        self.assertEqual(list(pag.columns), COLUMNAS_POLIZAS_PAGO)


if __name__ == "__main__":
    unittest.main()
