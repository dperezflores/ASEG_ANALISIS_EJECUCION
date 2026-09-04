from __future__ import annotations

from application.ports.ai_provider import AIProvider
from application.ports.prompt_repository import PromptRepository
from domain.schemas import (
    ListaComprobantes,
    ListaEstimaciones,
    ListaFacturas,
    ListaPolizas,
    ResultadoExtraccion,
)


PROMPT_POR_CATEGORIA = {
    "Estimaciones": "estimaciones",
    "Facturas": "facturas",
    "Comprobantes de Pago": "comprobantes_pago",
    "Pólizas": "polizas",
}

ESQUEMA_POR_CATEGORIA = {
    "Estimaciones": ListaEstimaciones,
    "Facturas": ListaFacturas,
    "Comprobantes de Pago": ListaComprobantes,
    "Pólizas": ListaPolizas,
}


class DocumentAnalyzer:
    def __init__(
        self,
        provider: AIProvider,
        prompt_repository: PromptRepository,
    ):
        self.provider = provider
        self.prompt_repository = prompt_repository

    def analyze(self, categoria: str, archivo_pdf) -> ResultadoExtraccion:
        if categoria not in ESQUEMA_POR_CATEGORIA:
            raise ValueError(f"Categoría no soportada: {categoria}")

        prompt = self.prompt_repository.get(PROMPT_POR_CATEGORIA[categoria])
        esquema = ESQUEMA_POR_CATEGORIA[categoria]

        return self.provider.analizar_pdf(
            archivo_pdf,
            prompt,
            esquema,
        )
