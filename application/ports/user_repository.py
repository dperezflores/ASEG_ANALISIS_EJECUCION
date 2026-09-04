from __future__ import annotations

from typing import Protocol

from domain.users import User, UserIdentity


class UserRepository(Protocol):
    def upsert_from_identity(self, identity: UserIdentity) -> User:
        ...
