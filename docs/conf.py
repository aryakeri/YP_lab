"""Конфигурация Sphinx для проекта passgen."""

from __future__ import annotations

import os
import sys
from datetime import datetime

# Добавляем путь к корню репозитория, чтобы autodoc видел пакеты.
sys.path.insert(0, os.path.abspath(".."))

project = "passgen"
author = "passgen CLI"
copyright = f"{datetime.now().year}, {author}"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []
language = "ru"

html_theme = "alabaster"
html_static_path = ["_static"]
