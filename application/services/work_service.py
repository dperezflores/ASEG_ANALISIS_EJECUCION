from __future__ import annotations

from uuid import UUID

from application.ports.work_repository import WorkRepository
from domain.works import NewWork, Work, WorkStatus


class WorkService:
    def __init__(self, works: WorkRepository):
        self._works = works

    def list_active(self, user_id: UUID) -> list[Work]:
        return self._works.list_by_user(user_id, WorkStatus.ACTIVA)

    def list_archived(self, user_id: UUID) -> list[Work]:
        return self._works.list_by_user(user_id, WorkStatus.ARCHIVADA)

    def get_owned(self, work_id: UUID, user_id: UUID) -> Work | None:
        return self._works.get_owned(work_id, user_id)

    def create(self, user_id: UUID, data: NewWork) -> Work:
        name = data.name.strip()
        if not name:
            raise ValueError("El nombre de la obra es obligatorio.")
        normalized = NewWork(
            name=name,
            contract_number=(data.contract_number or "").strip() or None,
            entity=(data.entity or "").strip() or None,
            contractor=(data.contractor or "").strip() or None,
            fiscal_year=data.fiscal_year,
            description=(data.description or "").strip() or None,
        )
        return self._works.create(user_id, normalized)

    def archive(self, work_id: UUID, user_id: UUID) -> Work | None:
        return self._works.update_status(work_id, user_id, WorkStatus.ARCHIVADA)

    def restore(self, work_id: UUID, user_id: UUID) -> Work | None:
        return self._works.update_status(work_id, user_id, WorkStatus.ACTIVA)

    def delete(self, work_id: UUID, user_id: UUID) -> bool:
        return self._works.delete_owned(work_id, user_id)
