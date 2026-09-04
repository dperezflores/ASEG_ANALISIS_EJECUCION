from __future__ import annotations

from uuid import UUID, uuid4

from domain.works import NewWork, Work, WorkStatus
from infrastructure.database.connection import Database


class NeonWorkRepository:
    def __init__(self, database: Database):
        self._database = database

    @staticmethod
    def _to_work(row) -> Work:
        return Work(
            id=row["id"],
            user_id=row["usuario_id"],
            name=row["nombre"],
            contract_number=row["numero_contrato"],
            entity=row["ente"],
            contractor=row["contratista"],
            fiscal_year=row["ejercicio"],
            description=row["descripcion"],
            status=WorkStatus(row["estado"]),
            created_at=row["creado_en"],
            updated_at=row["actualizado_en"],
        )

    def list_by_user(self, user_id: UUID, status: WorkStatus = WorkStatus.ACTIVA) -> list[Work]:
        sql = """
            SELECT id, usuario_id, nombre, numero_contrato, ente, contratista,
                   ejercicio, descripcion, estado, creado_en, actualizado_en
            FROM obras
            WHERE usuario_id = %s AND estado = %s
            ORDER BY actualizado_en DESC, creado_en DESC
        """
        with self._database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (user_id, status.value))
                rows = cursor.fetchall()
        return [self._to_work(row) for row in rows]

    def get_owned(self, work_id: UUID, user_id: UUID) -> Work | None:
        sql = """
            SELECT id, usuario_id, nombre, numero_contrato, ente, contratista,
                   ejercicio, descripcion, estado, creado_en, actualizado_en
            FROM obras
            WHERE id = %s AND usuario_id = %s
        """
        with self._database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (work_id, user_id))
                row = cursor.fetchone()
        return self._to_work(row) if row else None

    def create(self, user_id: UUID, data: NewWork) -> Work:
        sql = """
            INSERT INTO obras (
                id, usuario_id, nombre, numero_contrato, ente, contratista,
                ejercicio, descripcion, estado, creado_en, actualizado_en
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'ACTIVA', NOW(), NOW())
            RETURNING id, usuario_id, nombre, numero_contrato, ente, contratista,
                      ejercicio, descripcion, estado, creado_en, actualizado_en
        """
        with self._database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        uuid4(), user_id, data.name, data.contract_number,
                        data.entity, data.contractor, data.fiscal_year,
                        data.description,
                    ),
                )
                row = cursor.fetchone()
            connection.commit()
        return self._to_work(row)

    def update_status(self, work_id: UUID, user_id: UUID, status: WorkStatus) -> Work | None:
        sql = """
            UPDATE obras
            SET estado = %s, actualizado_en = NOW()
            WHERE id = %s AND usuario_id = %s
            RETURNING id, usuario_id, nombre, numero_contrato, ente, contratista,
                      ejercicio, descripcion, estado, creado_en, actualizado_en
        """
        with self._database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (status.value, work_id, user_id))
                row = cursor.fetchone()
            connection.commit()
        return self._to_work(row) if row else None

    def delete_owned(self, work_id: UUID, user_id: UUID) -> bool:
        sql = "DELETE FROM obras WHERE id = %s AND usuario_id = %s"
        with self._database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (work_id, user_id))
                deleted = cursor.rowcount > 0
            connection.commit()
        return deleted
