"""Password generation logic."""

from __future__ import annotations

import secrets
from typing import List

from . import utils


def generate_password(
    length: int,
    *,
    use_digits: bool = True,
    use_special: bool = True,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
) -> str:
    """Generate a password that satisfies the requested options."""
    charsets: List[str] = utils.build_charsets(
        include_lower=use_lowercase,
        include_upper=use_uppercase,
        include_digits=use_digits,
        include_special=use_special,
    )

    min_required = len(charsets)
    utils.validate_length(length, min_required=min_required)

    rng = secrets.SystemRandom()

    # Guarantee at least one character from every selected charset.
    password_chars = [rng.choice(charset) for charset in charsets]

    all_chars = "".join(charsets)
    remaining = length - len(password_chars)
    password_chars.extend(rng.choice(all_chars) for _ in range(remaining))

    rng.shuffle(password_chars)
    return "".join(password_chars)


__all__ = ["generate_password"]
