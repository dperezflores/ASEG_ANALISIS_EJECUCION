from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel


class ModeloASEG(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class Estimacion(ModeloASEG):
    numero_estimacion: str = Field(alias="Numero de estimación")
    fecha_elaboracion: str = Field(alias="Fecha de elaboración o de estimación")
    periodo_de: str = Field(alias="De (Periodo de ejecución)")
    periodo_hasta: str = Field(alias="Hasta (Periodo de ejecución)")
    importe_sin_iva: float = Field(alias="Importe sin IVA", default=0.0)
    iva: float = Field(alias="IVA", default=0.0)
    importe_con_iva: float = Field(alias="Importe con IVA", default=0.0)
    importe_anticipo: float = Field(alias="Importe de anticipo", default=0.0)
    amortizacion: float = Field(alias="Amortización", default=0.0)
    deducciones: float = Field(alias="Deducciones", default=0.0)
    sancion: float = Field(alias="Sancion", default=0.0)
    retencion: float = Field(alias="Retencion", default=0.0)


class ListaEstimaciones(RootModel[list[Estimacion]]):
    pass


class Factura(ModeloASEG):
    folio: str = Field(alias="Folio")
    descripcion: str = Field(alias="Descripción")
    fecha: str = Field(alias="Fecha")
    monto_total: float = Field(alias="Monto total", default=0.0)
    orden_estimacion: int = Field(alias="Orden de estimacion", default=99)


class ListaFacturas(RootModel[list[Factura]]):
    pass


class ComprobantePago(ModeloASEG):
    numero: str = Field(alias="Número")
    fecha_pago: str = Field(alias="Fecha de pago")
    importe: float = Field(alias="Importe", default=0.0)
    cuenta_emisora: str = Field(alias="Cuenta bancaria emisora")
    clave_rastreo: str = Field(alias="Clave de rastreo")
    institucion_emisora: str = Field(alias="Institución emisora")
    institucion_receptora: str = Field(alias="Institución receptora")
    cuenta_beneficiaria: str = Field(alias="Cuenta beneficiaria")


class ListaComprobantes(RootModel[list[ComprobantePago]]):
    pass


class Poliza(ModeloASEG):
    tipo: Literal["DEVENGO", "PAGO"] = Field(alias="Tipo de poliza")
    cuenta_contable: str = Field(alias="Cuenta contable")
    numero_estimacion: str = Field(alias="Numero de estimacion")
    numero_poliza: str = Field(alias="Numero de poliza")
    fecha: str = Field(alias="Fecha")
    importe: float = Field(alias="Importe", default=0.0)
    fuente_financiamiento: str = Field(alias="Fuente de financiamiento")


class ListaPolizas(RootModel[list[Poliza]]):
    pass


class ResultadoExtraccion(ModeloASEG):
    estado: Literal["OK", "ERROR"]
    datos: list[dict[str, Any]] = Field(default_factory=list)
    errores: list[str] = Field(default_factory=list)
    advertencias: list[str] = Field(default_factory=list)
    metadatos: dict[str, Any] = Field(default_factory=dict)
