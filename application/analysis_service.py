from __future__ import annotations

import hashlib
from uuid import UUID

from application.analyzer import DocumentAnalyzer
from application.ports.analysis_repository import AnalysisRepository
from application.session import (
    append_history,
    is_processed,
    mark_processed,
    register_saved_analysis,
)
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

    def processing_key(
        self,
        categoria: str,
        file,
        file_hash: str | None = None,
    ) -> str:
        provider = self.analyzer.provider
        prompt_signature = self.analyzer.prompt_signature(categoria)
        return (
            f"{categoria}:"
            f"{file_hash or self.fingerprint(file)}:"
            f"{provider.provider_name}:"
            f"{provider.model_name}:"
            f"{provider.prompt_version}:"
            f"{prompt_signature}"
        )

    def _register_cached_analysis(self, cached: dict) -> None:
        register_saved_analysis(
            {
                "categoria": cached.get("categoria"),
                "archivo_hash": cached.get("archivo_hash"),
                "archivo_nombre": cached.get("archivo_nombre"),
                "proveedor": cached.get("proveedor"),
                "modelo": cached.get("modelo"),
                "version_prompt": cached.get("version_prompt"),
                "firma_prompt": cached.get("firma_prompt"),
                "processing_key": cached.get("processing_key"),
                "creado_en": cached.get("creado_en"),
            }
        )

    def _restore_cached_result(self, categoria: str, key: str) -> ResultadoExtraccion | None:
        if self.repository is None or self.work_id is None:
            return None

        try:
            cached = self.repository.get_by_processing_key(self.work_id, key)
        except Exception:
            return None

        if not cached:
            return None

        datos = list(cached.get("datos") or [])
        if datos:
            append_history(categoria, datos)
        mark_processed(key)
        self._register_cached_analysis(cached)

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

        file_hash = self.fingerprint(file)
        key = self.processing_key(categoria, file, file_hash)
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
                prompt_signature = self.analyzer.prompt_signature(categoria)
                try:
                    self.repository.save(
                        work_id=self.work_id,
                        categoria=categoria,
                        archivo_hash=file_hash,
                        archivo_nombre=file.name,
                        proveedor=provider.provider_name,
                        modelo=provider.model_name,
                        version_prompt=provider.prompt_version,
                        firma_prompt=prompt_signature,
                        processing_key=key,
                        datos=result.datos,
                        metadatos=result.metadatos,
                    )
                    register_saved_analysis(
                        {
                            "categoria": categoria,
                            "archivo_hash": file_hash,
                            "archivo_nombre": file.name,
                            "proveedor": provider.provider_name,
                            "modelo": provider.model_name,
                            "version_prompt": provider.prompt_version,
                            "firma_prompt": prompt_signature,
                            "processing_key": key,
                            "creado_en": None,
                        }
                    )
                except Exception:
                    pass

        return result, False
