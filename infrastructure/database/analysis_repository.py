from __future__ import annotations

from uuid import UUID, uuid4

from psycopg.types.json import Jsonb

from infrastructure.database.connection import Database


class NeonAnalysisRepository:
    def __init__(self, database: Database):
        self._database = database

    def get_by_processing_key(self, work_id: UUID, processing_key: str) -> dict | None:
        sql = """
            SELECT categoria, archivo_hash, archivo_nombre, proveedor, modelo,
                   version_prompt, firma_prompt, processing_key, datos, metadatos,
                   creado_en
            FROM resultados_analisis
            WHERE obra_id = %s AND processing_key = %s
            LIMIT 1
        """
        with self._database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (work_id, processing_key))
                row = cursor.fetchone()
        return dict(row) if row else None

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
        sql = """
            INSERT INTO resultados_analisis (
                id, obra_id, categoria, archivo_hash, archivo_nombre,
                proveedor, modelo, version_prompt, firma_prompt,
                processing_key, datos, metadatos, creado_en
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (obra_id, processing_key) DO NOTHING
        """
        with self._database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    sql,
                    (
                        uuid4(),
                        work_id,
                        categoria,
                        archivo_hash,
                        archivo_nombre,
                        proveedor,
                        modelo,
                        version_prompt,
                        firma_prompt,
                        processing_key,
                        Jsonb(datos),
                        Jsonb(metadatos),
                    ),
                )
            connection.commit()

    def list_latest_for_work(self, work_id: UUID) -> list[dict]:
        sql = """
            SELECT DISTINCT ON (categoria, archivo_hash)
                   categoria, archivo_hash, archivo_nombre, proveedor, modelo,
                   version_prompt, firma_prompt, processing_key, datos, metadatos,
                   creado_en
            FROM resultados_analisis
            WHERE obra_id = %s
            ORDER BY categoria, archivo_hash, creado_en DESC
        """
        with self._database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (work_id,))
                rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def delete_file_analysis(
        self,
        work_id: UUID,
        categoria: str,
        archivo_hash: str,
    ) -> int:
        sql = """
            DELETE FROM resultados_analisis
            WHERE obra_id = %s AND categoria = %s AND archivo_hash = %s
        """
        with self._database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (work_id, categoria, archivo_hash))
                deleted = cursor.rowcount
            connection.commit()
        return deleted
