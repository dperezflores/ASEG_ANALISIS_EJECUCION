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

        for row in rows:
            categoria = row["categoria"]
            datos = list(row.get("datos") or [])
            history_by_category[categoria].extend(datos)
            processing_key = row.get("processing_key")
            if processing_key:
                processed_keys.add(processing_key)

        restore_persisted_history(
            str(work_id),
            dict(history_by_category),
            processed_keys,
        )
