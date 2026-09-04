from __future__ import annotations

from typing import Protocol
from uuid import UUID

from domain.works import NewWork, Work, WorkStatus


class WorkRepository(Protocol):
    def list_by_user(self, user_id: UUID, status: WorkStatus = WorkStatus.ACTIVA) -> list[Work]:
        ...

    def get_owned(self, work_id: UUID, user_id: UUID) -> Work | None:
        ...

    def create(self, user_id: UUID, data: NewWork) -> Work:
        ...

    def update_status(self, work_id: UUID, user_id: UUID, status: WorkStatus) -> Work | None:
        ...

    def delete_owned(self, work_id: UUID, user_id: UUID) -> bool:
        ...
