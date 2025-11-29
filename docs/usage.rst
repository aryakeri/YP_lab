Использование
=============

Установка зависимостей
----------------------

Установите Sphinx для сборки документации::

   python3 -m pip install --user sphinx

Запуск приложения
-----------------

Основной сценарий использования:

.. code-block:: console

   python3 -m passgen.main generate --length 16

Доступные опции для ``generate``:

- ``--length`` — длина пароля (по умолчанию 16);
- ``--digits`` / ``--no-digits`` — включить/исключить цифры;
- ``--special`` / ``--no-special`` — включить/исключить спецсимволы;
- ``--uppercase`` / ``--no-uppercase`` — включить/исключить заглавные буквы;
- ``--lowercase`` / ``--no-lowercase`` — включить/исключить строчные буквы;
- ``--save`` — сохранить хэш пароля в JSON;
- ``--label`` — метка сохранённой записи;
- ``--storage-file`` — путь к файлу хранения.

Поиск сохранённых записей:

.. code-block:: console

   python3 -m passgen.main search --label work
   python3 -m passgen.main search --password mypassword

Сборка HTML документации
------------------------

После установки Sphinx выполните из корня репозитория:

.. code-block:: console

   sphinx-build -b html docs docs/_build/html

Готовая документация будет доступна в каталоге ``docs/_build/html``.
