from __future__ import annotations

from typing import Protocol
from uuid import UUID


class AnalysisRepository(Protocol):
    def get_by_processing_key(self, work_id: UUID, processing_key: str) -> dict | None:
        ...

    def save(
        self,
        *,
        work_id: UUID,
        categoria: str,
        archivo_hash: str,
        archivo_nombre: str,
        proveedor: str,
        modelo: str,
        version_prompt: str,
        firma_prompt: str,
        processing_key: str,
        datos: list[dict],
        metadatos: dict,
    ) -> None:
        ...

    def list_latest_for_work(self, work_id: UUID) -> list[dict]:
        ...
