from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserIdentity:
    subject: str
    email: str
    name: str
    picture_url: str | None = None


@dataclass(frozen=True, slots=True)
class User:
    id: UUID
    google_sub: str
    email: str
    name: str
    picture_url: str | None
    active: bool
    created_at: datetime
    last_login_at: datetime
