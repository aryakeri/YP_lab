"""Password storage helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from . import utils

DEFAULT_STORAGE_FILE = Path(__file__).resolve().parent / "passwords.json"


def resolve_storage_file(storage_file: str | None) -> Path:
    """Return the file that should be used for persisting passwords."""
    if storage_file:
        return Path(storage_file).expanduser().resolve()
    return DEFAULT_STORAGE_FILE


def _load_entries(path: Path) -> List[Dict[str, object]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        try:
            data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Cannot read storage file {path}: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError(f"Storage file {path} is corrupted; expected a list")
    return data


def _write_entries(path: Path, entries: Iterable[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(list(entries), handle, indent=2)


def store_password(
    password: str,
    *,
    label: str,
    length: int,
    options: Dict[str, bool],
    storage_file: str | None = None,
) -> Tuple[Dict[str, object], Path]:
    """Persist a hashed version of the password alongside metadata."""
    path = resolve_storage_file(storage_file)
    entries = _load_entries(path)
    entry = {
        "label": label,
        "hash": utils.hash_password(password),
        "length": length,
        "options": options,
        "created_at": utils.current_timestamp(),
    }
    entries.append(entry)
    _write_entries(path, entries)
    return entry, path


def search_passwords(
    *,
    label_query: str | None = None,
    storage_file: str | None = None,
) -> Tuple[List[Dict[str, object]], Path]:
    """Return stored entries filtered by an optional label query."""
    path = resolve_storage_file(storage_file)
    entries = _load_entries(path)
    if label_query:
        lowered = label_query.lower()
        entries = [entry for entry in entries if lowered in str(entry.get("label", "")).lower()]
    return entries, path


def verify_password(
    password: str,
    *,
    label_query: str | None = None,
    storage_file: str | None = None,
) -> Tuple[List[Dict[str, object]], Path]:
    """Return entries that match the provided plaintext password."""
    target_hash = utils.hash_password(password)
    entries, path = search_passwords(label_query=label_query, storage_file=storage_file)
    matches = [entry for entry in entries if entry.get("hash") == target_hash]
    return matches, path


__all__ = [
    "DEFAULT_STORAGE_FILE",
    "resolve_storage_file",
    "store_password",
    "search_passwords",
    "verify_password",
]
