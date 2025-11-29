"""Utility helpers for the password generator."""

from __future__ import annotations

import hashlib
import string
from datetime import datetime, timezone
from typing import List

SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.?/<>|~"


def build_charsets(
    *,
    include_lower: bool,
    include_upper: bool,
    include_digits: bool,
    include_special: bool,
) -> List[str]:
    """Вернуть список включённых наборов символов.

    Args:
        include_lower (bool): Добавить строчные буквы.
        include_upper (bool): Добавить заглавные буквы.
        include_digits (bool): Добавить цифры.
        include_special (bool): Добавить спецсимволы.

    Returns:
        List[str]: Список строковых наборов символов.

    Raises:
        ValueError: Если ни один набор не активен.
    """
    charsets: List[str] = []
    if include_lower:
        charsets.append(string.ascii_lowercase)
    if include_upper:
        charsets.append(string.ascii_uppercase)
    if include_digits:
        charsets.append(string.digits)
    if include_special:
        charsets.append(SPECIAL_CHARACTERS)

    if not charsets:
        raise ValueError("At least one character category must be enabled")
    return charsets


def validate_length(length: int, *, min_required: int = 1) -> int:
    """Проверить корректность заданной длины.

    Args:
        length (int): Запрошенная длина пароля.
        min_required (int): Минимум символов, исходя из числа наборов.

    Returns:
        int: Подтверждённая длина.

    Raises:
        ValueError: Если длина меньше требуемого минимума.
    """
    if length < min_required:
        raise ValueError(
            f"Length must be at least {min_required} when {min_required} charsets are selected"
        )
    return length


def hash_password(password: str, *, algorithm: str = "sha256") -> str:
    """Посчитать безопасный хэш пароля.

    Args:
        password (str): Пароль в открытом виде.
        algorithm (str): Алгоритм для hashlib.new.

    Returns:
        str: Hex-дigest хэша.
    """
    digest = hashlib.new(algorithm)
    digest.update(password.encode("utf-8"))
    return digest.hexdigest()


def current_timestamp() -> str:
    """Получить отметку времени в формате ISO-8601 (UTC)."""
    return datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_label() -> str:
    """Сформировать метку по умолчанию.

    Returns:
        str: Строка вида `entry-<timestamp>`.
    """
    return f"entry-{current_timestamp()}"


__all__ = [
    "SPECIAL_CHARACTERS",
    "build_charsets",
    "validate_length",
    "hash_password",
    "current_timestamp",
    "default_label",
]
