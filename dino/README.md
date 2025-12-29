# Chrome Dino Game Clone

Клон динозаврика из Google Chrome на Python/PyGame с сохранением рекордов в SQLite.

## Особенности
- Управление: `SPACE` — прыжок/старт/рестарт, `ESC` — выход
- Два типа препятствий (кактусы и птицы), облака и анимации
- Система рекордов на SQLite (`dino_game.db` по умолчанию)
- Звуки (можно отключить), прогрессивный рост скорости
- Тесты и документация, headless-режим для CI

## Установка и запуск
```bash
# зависимости
pip install -r requirements.txt

# запуск игры
python3 run.py
```

## Тестирование
Для работы PyGame без окна используйте dummy-драйвер видео/аудио:
```bash
cd dino
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python3 -m unittest discover
```

## База данных
- Файл по умолчанию: `dino_game.db` в корне проекта (создается автоматически).
- API: `DatabaseHandler.save_score(name, score)`, `get_top_scores(limit)`, `get_player_scores(name)`, `get_average_score()`, `get_best_score()`, `delete_score(id)`, `clear_all_scores()`.
- В игре рекорд загружается при старте и сохраняется при новом лучшем результате.

## Структура
- `run.py` — точка входа.
- `game/main.py` — игровой цикл, отрисовка, ввод.
- `game/game_objects.py` — примитивные объекты (Dino, Cactus, Bird) с хитбоксами.
- `game/game_logic.py` — функции логики (пока используется для коллизий).
- `database/db_handler.py` — работа с SQLite.
- `tests/` — модульные и интеграционные тесты, документация.
