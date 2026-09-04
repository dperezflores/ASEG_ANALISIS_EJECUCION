from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class WorkStatus(StrEnum):
    ACTIVA = "ACTIVA"
    ARCHIVADA = "ARCHIVADA"


@dataclass(frozen=True, slots=True)
class Work:
    id: UUID
    user_id: UUID
    name: str
    contract_number: str | None
    entity: str | None
    contractor: str | None
    fiscal_year: int | None
    description: str | None
    status: WorkStatus
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class NewWork:
    name: str
    contract_number: str | None = None
    entity: str | None = None
    contractor: str | None = None
    fiscal_year: int | None = None
    description: str | None = None
