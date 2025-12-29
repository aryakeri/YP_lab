"""
Модели данных для базы данных
"""
from datetime import datetime


class Score:
    """Класс для представления результата игры"""

    def __init__(self, score_id, player_name, score, date=None):
        self.id = score_id
        self.player_name = player_name
        self.score = score
        self.date = date if date else datetime.now()

    def __repr__(self):
        return f"Score(id={self.id}, player='{self.player_name}', score={self.score}, date={self.date})"

    def to_dict(self):
        """Преобразование объекта в словарь"""
        return {
            'id': self.id,
            'player_name': self.player_name,
            'score': self.score,
            'date': self.date.isoformat() if hasattr(self.date, 'isoformat') else str(self.date)
        }

    def display_date(self):
        """Красивое отображение даты"""
        return self.date.strftime("%d.%m.%Y %H:%M")