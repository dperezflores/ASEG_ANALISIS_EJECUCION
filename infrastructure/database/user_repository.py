from __future__ import annotations

from uuid import uuid4

from domain.users import User, UserIdentity
from infrastructure.database.connection import Database


class NeonUserRepository:
    def __init__(self, database: Database):
        self._database = database

    def upsert_from_identity(self, identity: UserIdentity) -> User:
        user_id = uuid4()
        sql = """
            INSERT INTO usuarios (
                id, google_sub, email, nombre, picture_url, activo,
                creado_en, ultimo_acceso_en
            )
            VALUES (%s, %s, %s, %s, %s, TRUE, NOW(), NOW())
            ON CONFLICT (google_sub)
            DO UPDATE SET
                email = EXCLUDED.email,
                nombre = EXCLUDED.nombre,
                picture_url = EXCLUDED.picture_url,
                activo = TRUE,
                ultimo_acceso_en = NOW()
            RETURNING
                id, google_sub, email, nombre, picture_url, activo,
                creado_en, ultimo_acceso_en
        """
        with self._database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        user_id,
                        identity.subject,
                        identity.email,
                        identity.name,
                        identity.picture_url,
                    ),
                )
                row = cursor.fetchone()
            connection.commit()

        return User(
            id=row["id"],
            google_sub=row["google_sub"],
            email=row["email"],
            name=row["nombre"],
            picture_url=row["picture_url"],
            active=row["activo"],
            created_at=row["creado_en"],
            last_login_at=row["ultimo_acceso_en"],
        )
