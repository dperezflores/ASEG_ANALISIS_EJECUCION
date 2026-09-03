from __future__ import annotations

from enum import StrEnum


class CategoriaDocumento(StrEnum):
    ESTIMACIONES = "Estimaciones"
    FACTURAS = "Facturas"
    COMPROBANTES = "Comprobantes de Pago"
    POLIZAS = "Pólizas"


CATEGORIAS = tuple(categoria.value for categoria in CategoriaDocumento)
