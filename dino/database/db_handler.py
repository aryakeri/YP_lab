"""Обработчик базы данных для хранения результатов игры."""

import os
import sqlite3
from typing import List, Optional

from .models import Score


class DatabaseHandler:
    """Работа с SQLite БД: сохранение и получение счетов."""

    def __init__(self, db_path: str = "dino_game.db"):
        self.db_path = db_path
        self.conn = None
        self._ensure_directory()
        self._setup()

    def _ensure_directory(self):
        directory = os.path.dirname(self.db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def _setup(self):
        """Создает таблицу scores при первом подключении."""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL DEFAULT 'Player',
                score INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def save_score(self, player_name: str, score: int) -> bool:
        """Сохраняет счет игрока. Возвращает True, если успешно."""
        if score < 10:
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO scores (player_name, score) VALUES (?, ?)",
                (player_name, score),
            )
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def get_top_scores(self, limit: int = 5):
        """Возвращает топ результатов в виде списка кортежей (name, score, date)."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT player_name, score, date FROM scores ORDER BY score DESC LIMIT ?",
            (limit,),
        )
        return cursor.fetchall()

    def get_player_scores(self, player_name: str) -> List[Score]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, player_name, score, date FROM scores WHERE player_name = ?",
            (player_name,),
        )
        rows = cursor.fetchall()
        return [Score(row[0], row[1], row[2], row[3]) for row in rows]

    def get_average_score(self) -> Optional[float]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT AVG(score) FROM scores")
        result = cursor.fetchone()
        return result[0] if result and result[0] is not None else None

    def delete_score(self, score_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM scores WHERE id = ?", (score_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def clear_all_scores(self) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM scores")
        self.conn.commit()
        return True

    def get_best_score(self) -> int:
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(score) FROM scores")
        result = cursor.fetchone()
        return result[0] if result and result[0] is not None else 0

    def close(self):
        if self.conn:
            self.conn.close()


Database = DatabaseHandler
db = DatabaseHandler()
