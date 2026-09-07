from __future__ import annotations

import hashlib

from application.ports.ai_provider import AIProvider
from application.ports.prompt_repository import PromptRepository
from domain.schemas import (
    ListaComprobantes,
    ListaEstimaciones,
    ListaFacturas,
    ListaPolizas,
    ListaSolicitudesPago,
    ResultadoExtraccion,
)


PROMPT_POR_CATEGORIA = {
    "Estimaciones": "estimaciones",
    "Facturas": "facturas",
    "Solicitudes de Pago": "solicitudes_pago",
    "Comprobantes de Pago": "comprobantes_pago",
    "Pólizas": "polizas",
}

ESQUEMA_POR_CATEGORIA = {
    "Estimaciones": ListaEstimaciones,
    "Facturas": ListaFacturas,
    "Solicitudes de Pago": ListaSolicitudesPago,
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

    def prompt_for(self, categoria: str) -> str:
        if categoria not in PROMPT_POR_CATEGORIA:
            raise ValueError(f"Categoría no soportada: {categoria}")
        return self.prompt_repository.get(PROMPT_POR_CATEGORIA[categoria])

    def prompt_signature(self, categoria: str) -> str:
        prompt = self.prompt_for(categoria)
        return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

    def analyze(self, categoria: str, archivo_pdf) -> ResultadoExtraccion:
        if categoria not in ESQUEMA_POR_CATEGORIA:
            raise ValueError(f"Categoría no soportada: {categoria}")

        prompt = self.prompt_for(categoria)
        esquema = ESQUEMA_POR_CATEGORIA[categoria]

        return self.provider.analizar_pdf(
            archivo_pdf,
            prompt,
            esquema,
        )
