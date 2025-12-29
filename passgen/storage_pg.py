"""Хранилище паролей в PostgreSQL."""

from __future__ import annotations

import json
from typing import Dict, List, Tuple

from . import utils


def _get_connection(dsn: str):
    """Создать подключение к БД."""
    try:
        import psycopg2  # type: ignore
    except ImportError as exc:
        raise ImportError("Установите пакет psycopg2-binary для хранения в PostgreSQL") from exc
    return psycopg2.connect(dsn)


def _ensure_schema(conn) -> None:
    """Создать таблицу при первом использовании."""
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS passgen_passwords (
                    id SERIAL PRIMARY KEY,
                    label TEXT,
                    hash TEXT NOT NULL,
                    length INTEGER NOT NULL,
                    options JSONB NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL
                )
                """
            )


def store_password_postgres(
    password: str,
    *,
    label: str,
    length: int,
    options: Dict[str, bool],
    dsn: str,
) -> Tuple[Dict[str, object], str]:
    """Сохранить хэш пароля и метаданные в PostgreSQL."""
    conn = _get_connection(dsn)
    try:
        _ensure_schema(conn)
        entry = {
            "label": label,
            "hash": utils.hash_password(password),
            "length": length,
            "options": options,
            "created_at": utils.current_timestamp(),
        }
        with conn:
            with conn.cursor() as cur:
                from psycopg2.extras import Json  # type: ignore

                cur.execute(
                    """
                    INSERT INTO passgen_passwords (label, hash, length, options, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING label, hash, length, options, created_at
                    """,
                    (
                        entry["label"],
                        entry["hash"],
                        entry["length"],
                        Json(entry["options"]),
                        entry["created_at"],
                    ),
                )
                row = cur.fetchone()
        if row:
            entry = {
                "label": row[0],
                "hash": row[1],
                "length": row[2],
                "options": row[3],
                "created_at": row[4].isoformat().replace("+00:00", "Z") if hasattr(row[4], "isoformat") else row[4],
            }
        return entry, dsn
    finally:
        conn.close()


def search_passwords_postgres(
    *,
    label_query: str | None = None,
    dsn: str,
) -> Tuple[List[Dict[str, object]], str]:
    """Получить записи из PostgreSQL с фильтром по метке."""
    conn = _get_connection(dsn)
    try:
        _ensure_schema(conn)
        with conn.cursor() as cur:
            if label_query:
                cur.execute(
                    """
                    SELECT label, hash, length, options, created_at
                    FROM passgen_passwords
                    WHERE label ILIKE %s
                    """,
                    (f"%{label_query}%",),
                )
            else:
                cur.execute(
                    "SELECT label, hash, length, options, created_at FROM passgen_passwords"
                )
            rows = cur.fetchall()
        entries = [
            {
                "label": row[0],
                "hash": row[1],
                "length": row[2],
                "options": row[3],
                "created_at": row[4].isoformat().replace("+00:00", "Z") if hasattr(row[4], "isoformat") else row[4],
            }
            for row in rows
        ]
        return entries, dsn
    finally:
        conn.close()


def verify_password_postgres(
    password: str,
    *,
    label_query: str | None = None,
    dsn: str,
) -> Tuple[List[Dict[str, object]], str]:
    """Найти записи по совпадающему хэшу пароля."""
    target_hash = utils.hash_password(password)
    conn = _get_connection(dsn)
    try:
        _ensure_schema(conn)
        with conn.cursor() as cur:
            if label_query:
                cur.execute(
                    """
                    SELECT label, hash, length, options, created_at
                    FROM passgen_passwords
                    WHERE hash = %s AND label ILIKE %s
                    """,
                    (target_hash, f"%{label_query}%",),
                )
            else:
                cur.execute(
                    """
                    SELECT label, hash, length, options, created_at
                    FROM passgen_passwords
                    WHERE hash = %s
                    """,
                    (target_hash,),
                )
            rows = cur.fetchall()
        entries = [
            {
                "label": row[0],
                "hash": row[1],
                "length": row[2],
                "options": row[3],
                "created_at": row[4].isoformat().replace("+00:00", "Z") if hasattr(row[4], "isoformat") else row[4],
            }
            for row in rows
        ]
        return entries, dsn
    finally:
        conn.close()


__all__ = [
    "store_password_postgres",
    "search_passwords_postgres",
    "verify_password_postgres",
]
