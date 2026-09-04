from __future__ import annotations

import hashlib

from application.analyzer import DocumentAnalyzer
from application.session import append_history, is_processed, mark_processed
from domain.categories import CATEGORIAS


class AnalysisService:
    def __init__(self, analyzer: DocumentAnalyzer):
        self.analyzer = analyzer

    @staticmethod
    def fingerprint(file) -> str:
        return hashlib.sha256(file.getvalue()).hexdigest()

    def processing_key(self, categoria: str, file) -> str:
        provider = self.analyzer.provider
        return (
            f"{categoria}:"
            f"{self.fingerprint(file)}:"
            f"{provider.provider_name}:"
            f"{provider.model_name}:"
            f"{provider.prompt_version}"
        )

    def process_file(self, categoria: str, file):
        if categoria not in CATEGORIAS:
            raise ValueError(f"Categoría no soportada: {categoria}")

        key = self.processing_key(categoria, file)
        if is_processed(key):
            return None, True

        result = self.analyzer.analyze(categoria, file)

        if result.estado == "OK":
            for record in result.datos:
                record["Archivo Origen"] = file.name
            append_history(categoria, result.datos)
            mark_processed(key)

        return result, False
