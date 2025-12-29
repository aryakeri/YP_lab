"""
Example:
cd "/Users/aryakeri/Documents/university/5 SEMESTR/YAP/git/YP_lab"

python3 -m passgen.main generate --length 16

--length <n> — длина пароля (по умолчанию 16).
--digits / --no-digits — включить/исключить цифры.
--special / --no-special — включить/исключить спецсимволы.
--uppercase / --no-uppercase — включить/исключить заглавные.
--lowercase / --no-lowercase — включить/исключить строчные.
--label <строка> — явная метка для сохранения.
--storage-file <путь> — свой JSON вместо
--storage-dsn - сохранение в БД

cd git/YP_lab && python3 -m unittest discover -s tests -p 'test_*.py'

python3 -m unittest discover -s tests -p 'test_*.py'

Сохранение в БД
python3 -m passgen.main generate --length 12 --save --storage-dsn "$PASSGEN_DSN" --label megatest

Поиск в
python3 -m passgen.main generate --length 12 --save --storage-dsn "$PASSGEN_DSN" --label megatest
"""

from __future__ import annotations

import argparse
from typing import Optional, Sequence

try:
    from . import commands
except ImportError:
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from passgen import commands


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="passgen",
        description="Утилита для генерации безопасных паролей",
    )
    subparsers = parser.add_subparsers(dest="command")

    _build_generate_subcommand(subparsers)
    _build_search_subcommand(subparsers)
    return parser


def _build_generate_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Добавить подкоманду `generate` к парсеру.

    Args:
        subparsers (argparse._SubParsersAction): Коллекция подкоманд, созданная парсером.
    """
    generate = subparsers.add_parser(
        "generate",
        help="Сгенерировать новый пароль",
    )
    generate.add_argument(
        "--length",
        type=int,
        default=16,
        help="Длина пароля (по умолчанию 16)",
    )
    _add_boolean_pair(
        generate,
        name="digits",
        dest="use_digits",
        default=True,
        enable_help="Использовать цифры",
        disable_help="Не использовать цифры",
    )
    _add_boolean_pair(
        generate,
        name="special",
        dest="use_special",
        default=True,
        enable_help="Использовать спецсимволы",
        disable_help="Не использовать спецсимволы",
    )
    _add_boolean_pair(
        generate,
        name="uppercase",
        dest="use_uppercase",
        default=True,
        enable_help="Использовать заглавные буквы",
        disable_help="Не использовать заглавные буквы",
    )
    _add_boolean_pair(
        generate,
        name="lowercase",
        dest="use_lowercase",
        default=True,
        enable_help="Использовать строчные буквы",
        disable_help="Не использовать строчные буквы",
    )
    generate.add_argument(
        "--save",
        action="store_true",
        help="Сохранить хэш пароля в файл",
    )
    generate.add_argument(
        "--label",
        help="Метка для сохранённого пароля",
    )
    generate.add_argument(
        "--storage-file",
        help="Путь к файлу для сохранения (по умолчанию passgen/passwords.json)",
    )
    generate.add_argument(
        "--storage-dsn",
        help="Строка подключения PostgreSQL (альтернатива файлу JSON)",
    )
    generate.set_defaults(func=commands.handle_generate)


def _build_search_subcommand(subparsers: argparse._SubParsersAction) -> None:
    """Добавить подкоманду `search` к парсеру.

    Args:
        subparsers (argparse._SubParsersAction): Коллекция подкоманд, созданная парсером.
    """
    search = subparsers.add_parser(
        "search",
        help="Поиск/проверка сохранённых паролей",
    )
    search.add_argument(
        "--label",
        help="Часть метки для фильтра",
    )
    search.add_argument(
        "--password",
        help="Проверить, существует ли такой пароль (сравнение по хэшу)",
    )
    search.add_argument(
        "--storage-file",
        help="Путь к файлу хранения",
    )
    search.add_argument(
        "--storage-dsn",
        help="Строка подключения PostgreSQL (альтернатива файлу JSON)",
    )
    search.set_defaults(func=commands.handle_search)


def _add_boolean_pair(
    parser: argparse.ArgumentParser,
    *,
    name: str,
    dest: str,
    default: bool,
    enable_help: str,
    disable_help: str,
) -> None:
    """Добавить пару флагов вида --<name> / --no-<name> к парсеру.

    Args:
        parser (argparse.ArgumentParser): Активный парсер подкоманды.
        name (str): Базовое имя для флагов.
        dest (str): Имя атрибута, в который будет записан результат.
        default (bool): Значение по умолчанию.
        enable_help (str): Текст помощи для включающего флага.
        disable_help (str): Текст помощи для выключающего флага.
    """
    parser.add_argument(f"--{name}", dest=dest, action="store_true", help=enable_help)
    parser.add_argument(
        f"--no-{name}", dest=dest, action="store_false", help=disable_help
    )
    parser.set_defaults(**{dest: default})


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Точка входа CLI.

    Args:
        argv (Optional[Sequence[str]]): Список аргументов, по умолчанию sys.argv.

    Returns:
        int: Код возврата подкоманды или 1 при отсутствии команды.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
