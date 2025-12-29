Использование
=============

Установка зависимостей
----------------------

Установите Sphinx для сборки документации::

   python3 -m pip install --user sphinx

Для работы с PostgreSQL потребуется клиентская библиотека::

   python3 -m pip install --user psycopg2-binary

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
- ``--storage-file`` — путь к файлу хранения;
- ``--storage-dsn`` — строка подключения PostgreSQL (альтернатива JSON).

Поиск сохранённых записей:

.. code-block:: console

   python3 -m passgen.main search --label work
   python3 -m passgen.main search --password mypassword

Сохранение в PostgreSQL
-----------------------

Если передать ``--storage-dsn``, вместо JSON будет использоваться PostgreSQL.
Таблица ``passgen_passwords`` создаётся автоматически.

1. Поднимите сервер PostgreSQL и создайте БД, пользователя и пароль (пример)::

      createuser YP --pwprompt
      createdb passgen_db --owner=YP

2. Сформируйте DSN (пример)::

      export PASSGEN_DSN="postgresql://YP:6969@localhost:5432/passgen_db"

3. Генерация с сохранением в БД::

      python3 -m passgen.main generate --length 12 --save --storage-dsn "$PASSGEN_DSN" --label demo

4. Поиск записей в БД::

      python3 -m passgen.main search --storage-dsn "$PASSGEN_DSN" --label demo
      python3 -m passgen.main search --storage-dsn "$PASSGEN_DSN" --password mypassword

Сборка HTML документации
------------------------

После установки Sphinx выполните из корня репозитория:

.. code-block:: console

   sphinx-build -b html docs docs/_build/html

Готовая документация будет доступна в каталоге ``docs/_build/html``.
