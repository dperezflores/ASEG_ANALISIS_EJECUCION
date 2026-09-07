from __future__ import annotations

import hashlib
from uuid import UUID

from application.analyzer import DocumentAnalyzer
from application.ports.analysis_repository import AnalysisRepository
from application.session import append_history, is_processed, mark_processed
from domain.categories import CATEGORIAS
from domain.schemas import ResultadoExtraccion


class AnalysisService:
    def __init__(
        self,
        analyzer: DocumentAnalyzer,
        repository: AnalysisRepository | None = None,
        work_id: UUID | None = None,
    ):
        self.analyzer = analyzer
        self.repository = repository
        self.work_id = work_id

    @staticmethod
    def fingerprint(file) -> str:
        return hashlib.sha256(file.getvalue()).hexdigest()

    def processing_key(self, categoria: str, file) -> str:
        provider = self.analyzer.provider
        prompt_signature = self.analyzer.prompt_signature(categoria)
        return (
            f"{categoria}:"
            f"{self.fingerprint(file)}:"
            f"{provider.provider_name}:"
            f"{provider.model_name}:"
            f"{provider.prompt_version}:"
            f"{prompt_signature}"
        )

    def _restore_cached_result(self, categoria: str, key: str) -> ResultadoExtraccion | None:
        if self.repository is None or self.work_id is None:
            return None

        cached = self.repository.get_by_processing_key(self.work_id, key)
        if not cached:
            return None

        datos = list(cached.get("datos") or [])
        if datos:
            append_history(categoria, datos)
        mark_processed(key)

        metadatos = dict(cached.get("metadatos") or {})
        metadatos["origen_resultado"] = "NEON"

        return ResultadoExtraccion(
            estado="OK",
            datos=datos,
            metadatos=metadatos,
        )

    def process_file(self, categoria: str, file):
        if categoria not in CATEGORIAS:
            raise ValueError(f"Categoría no soportada: {categoria}")

        key = self.processing_key(categoria, file)
        if is_processed(key):
            return None, True

        cached = self._restore_cached_result(categoria, key)
        if cached is not None:
            return cached, True

        result = self.analyzer.analyze(categoria, file)

        if result.estado == "OK":
            for record in result.datos:
                record["Archivo Origen"] = file.name

            append_history(categoria, result.datos)
            mark_processed(key)

            if self.repository is not None and self.work_id is not None:
                provider = self.analyzer.provider
                self.repository.save(
                    work_id=self.work_id,
                    categoria=categoria,
                    archivo_hash=self.fingerprint(file),
                    archivo_nombre=file.name,
                    proveedor=provider.provider_name,
                    modelo=provider.model_name,
                    version_prompt=provider.prompt_version,
                    firma_prompt=self.analyzer.prompt_signature(categoria),
                    processing_key=key,
                    datos=result.datos,
                    metadatos=result.metadatos,
                )

        return result, False
