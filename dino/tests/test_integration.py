"""Интеграционные тесты: игра + база данных в headless-режиме."""

import os
import sys
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from game.main import Game  # noqa: E402
from game.game_objects import Cactus  # noqa: E402
from database.db_handler import DatabaseHandler  # noqa: E402


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_integration.db"
        # Подготовим БД с начальными данными
        handler = DatabaseHandler(self.test_db)
        handler.save_score("Existing", 120)
        handler.close()

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_game_loads_best_score_from_db(self):
        game = Game(headless=True, disable_audio=True, db_path=self.test_db)
        self.assertEqual(game.high_score, 120)
        game.db.close()

    def test_game_saves_new_record_on_game_over(self):
        game = Game(headless=True, disable_audio=True, db_path=self.test_db)
        game.game_state = "playing"
        game.score = 200
        # Создаем препятствие на пути динозавра, чтобы вызвать столкновение
        game.obstacles = [Cactus(game.dino.x, game.dino.y)]

        game.update()

        self.assertEqual(game.game_state, "game_over")
        game.db.close()

        handler = DatabaseHandler(self.test_db)
        self.assertEqual(handler.get_best_score(), 200)
        handler.close()


if __name__ == "__main__":
    unittest.main()
