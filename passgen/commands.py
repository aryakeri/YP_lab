"""Command handlers for the CLI."""

from __future__ import annotations

import sys
from typing import Any, Dict

from .generator import generate_password
from . import storage, utils


def handle_generate(args) -> int:
    """Обработчик подкоманды `generate`.

    Args:
        args: Пространство имён argparse с аргументами подкоманды.

    Returns:
        int: Код возврата 0 при успехе или 1 при ошибке валидации.
    """
    use_digits = args.use_digits
    use_special = args.use_special
    use_uppercase = args.use_uppercase
    use_lowercase = args.use_lowercase

    try:
        password = generate_password(
            args.length,
            use_digits=use_digits,
            use_special=use_special,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
        )
    except ValueError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1

    print(password)

    if args.save:
        label = args.label or utils.default_label()
        options = {
            "digits": use_digits,
            "special": use_special,
            "uppercase": use_uppercase,
            "lowercase": use_lowercase,
        }
        if getattr(args, "storage_dsn", None):
            from . import storage_pg

            entry, path = storage_pg.store_password_postgres(
                password,
                label=label,
                length=args.length,
                options=options,
                dsn=args.storage_dsn,
            )
        else:
            entry, path = storage.store_password(
                password,
                label=label,
                length=args.length,
                options=options,
                storage_file=args.storage_file,
            )
        print(
            "Хэш сохранён:",
            f"label={entry['label']} file={path}"
        )
    return 0


def handle_search(args) -> int:
    """Обработчик подкоманды `search`.

    Args:
        args: Пространство имён argparse с аргументами подкоманды.

    Returns:
        int: Код возврата подкоманды, всегда 0.
    """
    use_pg = getattr(args, "storage_dsn", None)
    if args.password:
        if use_pg:
            from . import storage_pg

            entries, path = storage_pg.verify_password_postgres(
                args.password,
                label_query=args.label,
                dsn=use_pg,
            )
        else:
            entries, path = storage.verify_password(
                args.password,
                label_query=args.label,
                storage_file=args.storage_file,
            )
    else:
        if use_pg:
            from . import storage_pg

            entries, path = storage_pg.search_passwords_postgres(
                label_query=args.label,
                dsn=use_pg,
            )
        else:
            entries, path = storage.search_passwords(
                label_query=args.label,
                storage_file=args.storage_file,
            )

    if not entries:
        print("Ничего не найдено")
        return 0

    for entry in entries:
        _print_entry(entry, path)
    return 0


def _print_entry(entry: Dict[str, Any], path) -> None:
    """Вывести одну запись на stdout.

    Args:
        entry (Dict[str, Any]): Словарь с полями сохранённого пароля.
        path (Path): Файл, из которого была прочитана запись.
    """
    options = entry.get("options", {})
    enabled = ", ".join([name for name, enabled in options.items() if enabled])
    print(
        f"label: {entry.get('label')}\n"
        f"  hash: {entry.get('hash')}\n"
        f"  length: {entry.get('length')}\n"
        f"  options: {enabled or '—'}\n"
        f"  created_at: {entry.get('created_at')}"
    )


__all__ = ["handle_generate", "handle_search"]
