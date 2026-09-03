from __future__ import annotations

import hashlib
from dataclasses import dataclass

from application.session import append_history, is_processed, mark_processed
from core.analyzers import analizar
from domain.categories import CATEGORIAS
from providers.base import AIProvider


@dataclass(slots=True)
class AnalysisBatchResult:
    exitos: int = 0
    errores: int = 0
    omitidos: int = 0


class AnalysisService:
    def __init__(self, provider: AIProvider):
        self.provider = provider

    @staticmethod
    def fingerprint(file) -> str:
        return hashlib.sha256(file.getvalue()).hexdigest()

    def processing_key(self, categoria: str, file) -> str:
        return (
            f"{categoria}:"
            f"{self.fingerprint(file)}:"
            f"{self.provider.provider_name}:"
            f"{self.provider.model_name}:"
            f"{self.provider.prompt_version}"
        )

    def process_file(self, categoria: str, file):
        if categoria not in CATEGORIAS:
            raise ValueError(f"Categoría no soportada: {categoria}")

        key = self.processing_key(categoria, file)
        if is_processed(key):
            return None, True

        result = analizar(self.provider, categoria, file)
        if result.estado == "OK":
            for record in result.datos:
                record["Archivo Origen"] = file.name
            append_history(categoria, result.datos)
            mark_processed(key)
        return result, False
