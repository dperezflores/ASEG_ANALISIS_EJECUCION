from __future__ import annotations

from application.ports.user_repository import UserRepository
from domain.users import User, UserIdentity


class AuthService:
    def __init__(self, users: UserRepository):
        self._users = users

    def sync_user(self, identity: UserIdentity) -> User:
        return self._users.upsert_from_identity(identity)
