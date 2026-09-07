from __future__ import annotations

from collections import defaultdict
from uuid import UUID

from application.ports.analysis_repository import AnalysisRepository
from application.session import restore_persisted_history


class AnalysisHistoryService:
    def __init__(self, repository: AnalysisRepository):
        self._repository = repository

    def restore_work(self, work_id: UUID) -> None:
        rows = self._repository.list_latest_for_work(work_id)
        history_by_category: dict[str, list[dict]] = defaultdict(list)
        processed_keys: set[str] = set()
        saved_analyses: list[dict] = []

        for row in rows:
            categoria = row["categoria"]
            datos = list(row.get("datos") or [])
            history_by_category[categoria].extend(datos)
            processing_key = row.get("processing_key")
            if processing_key:
                processed_keys.add(processing_key)

            saved_analyses.append(
                {
                    "categoria": categoria,
                    "archivo_hash": row.get("archivo_hash"),
                    "archivo_nombre": row.get("archivo_nombre"),
                    "proveedor": row.get("proveedor"),
                    "modelo": row.get("modelo"),
                    "version_prompt": row.get("version_prompt"),
                    "firma_prompt": row.get("firma_prompt"),
                    "processing_key": processing_key,
                    "creado_en": row.get("creado_en"),
                }
            )

        restore_persisted_history(
            str(work_id),
            dict(history_by_category),
            processed_keys,
            saved_analyses,
        )

    def delete_file_analysis(
        self,
        work_id: UUID,
        categoria: str,
        archivo_hash: str,
    ) -> int:
        deleted = self._repository.delete_file_analysis(
            work_id,
            categoria,
            archivo_hash,
        )
        self.restore_work(work_id)
        return deleted
