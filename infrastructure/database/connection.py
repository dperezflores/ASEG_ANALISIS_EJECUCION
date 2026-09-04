from __future__ import annotations

from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row


class Database:
    def __init__(self, database_url: str):
        if not database_url.strip():
            raise ValueError("DATABASE_URL no está configurada.")
        self._database_url = database_url.strip()

    @contextmanager
    def connection(self):
        with psycopg.connect(
            self._database_url,
            row_factory=dict_row,
            autocommit=False,
        ) as connection:
            yield connection
