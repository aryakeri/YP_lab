# Документация проекта «Dino Game»

## Описание
Небольшая игра в духе динозавра из Google Chrome. Используется PyGame для визуала/звуков и SQLite для хранения рекордов.

## Архитектура
- `game/main.py` — класс `Game`: игровой цикл, ввод, отрисовка, генерация препятствий, счет/скорость. Поддерживает `headless` и `disable_audio` параметры, а также `db_path` для выбора файла БД.
- `game/game_objects.py` — примитивные объекты `Dino`, `Cactus`, `Bird` с методами `get_rect()` для коллизий.
- `game/game_logic.py` — функция `check_collision(dino, obstacle)` с уменьшенными хитбоксами.
- `database/db_handler.py` — `DatabaseHandler` для SQLite: CRUD операций над таблицей `scores`.
- `database/models.py` — модель `Score` для удобного представления записей.
- `tests/` — модульные (`test_game_logic.py`, `test_database.py`) и интеграционные (`test_integration.py`) тесты.

## Тесты (headless)
PyGame требует дисплей; в CI и локально без окна используйте dummy-драйверы:
```bash
cd dino
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python3 -m unittest discover
```

### Покрытие тестами
- `test_game_logic.py`: коллизии (кактус/птица), полный цикл прыжка, reset.
- `test_database.py`: создание схемы, сохранение/топ/минимальный порог, выборка игрока, средний/лучший счет, удаление и очистка.
- `test_integration.py`: загрузка рекорда из БД при старте `Game`, сохранение нового рекорда на `game_over` в headless-режиме.

## Использование БД
```python
from database.db_handler import DatabaseHandler

db = DatabaseHandler("my_scores.db")
db.save_score("Alice", 250)
top = db.get_top_scores(5)
best = db.get_best_score()
db.close()
```
Таблица `scores` создается автоматически с полями `id`, `player_name`, `score`, `date`.

## Запуск игры
```bash
pip install -r requirements.txt
python3 run.py
```
Управление: `SPACE` (прыжок/старт/рестарт), `ESC` (выход). Рекорд подтягивается из БД и сохраняется при новом лучшем результате.
