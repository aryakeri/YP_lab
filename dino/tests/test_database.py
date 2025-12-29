"""Тестирование функциональности базы данных."""

import os
import sqlite3
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from database.db_handler import DatabaseHandler
from database.models import Score


class TestDatabase(unittest.TestCase):
    """Тесты DatabaseHandler."""

    def setUp(self):
        self.test_db = "test_dino_game.db"
        self.db_handler = DatabaseHandler(self.test_db)

    def tearDown(self):
        self.db_handler.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_database_initialization(self):
        """Таблица scores создается с нужными полями."""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(scores)")
        columns = {col[1] for col in cursor.fetchall()}
        conn.close()

        expected = {"id", "player_name", "score", "date"}
        self.assertTrue(expected.issubset(columns))

    def test_save_and_top_scores(self):
        """Сохранение счета и выборка топа работают и сортируются по убыванию."""
        self.db_handler.save_score("Alice", 150)
        self.db_handler.save_score("Bob", 90)
        self.db_handler.save_score("Alice", 200)

        top_scores = self.db_handler.get_top_scores(2)
        self.assertEqual(len(top_scores), 2)
        self.assertEqual(top_scores[0][0], "Alice")
        self.assertEqual(top_scores[0][1], 200)
        self.assertEqual(top_scores[1][1], 150)

    def test_min_score_not_saved(self):
        """Счет меньше 10 не сохраняется."""
        saved = self.db_handler.save_score("Low", 5)
        self.assertFalse(saved)
        self.assertEqual(self.db_handler.get_top_scores(5), [])

    def test_get_player_scores(self):
        """Получение результатов конкретного игрока возвращает Score объекты."""
        self.db_handler.save_score("PlayerA", 100)
        self.db_handler.save_score("PlayerA", 120)
        self.db_handler.save_score("PlayerB", 80)

        player_scores = self.db_handler.get_player_scores("PlayerA")
        self.assertEqual(len(player_scores), 2)
        self.assertTrue(all(isinstance(score, Score) for score in player_scores))
        self.assertTrue(all(score.player_name == "PlayerA" for score in player_scores))

    def test_average_and_best_score(self):
        """Средний и максимальный счет рассчитываются корректно."""
        for value in (50, 100, 150):
            self.db_handler.save_score("Avg", value)

        average = self.db_handler.get_average_score()
        self.assertAlmostEqual(average, 100)
        self.assertEqual(self.db_handler.get_best_score(), 150)

    def test_delete_and_clear_scores(self):
        """Удаление конкретной записи и полной очистки таблицы."""
        self.db_handler.save_score("DeleteMe", 111)
        self.db_handler.save_score("KeepMe", 222)

        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM scores WHERE player_name = ?", ("DeleteMe",))
        score_id = cursor.fetchone()[0]
        conn.close()

        self.assertTrue(self.db_handler.delete_score(score_id))
        remaining = self.db_handler.get_top_scores(10)
        self.assertTrue(all(name != "DeleteMe" for name, _, _ in remaining))

        self.db_handler.clear_all_scores()
        self.assertEqual(self.db_handler.get_top_scores(5), [])


if __name__ == "__main__":
    unittest.main()
