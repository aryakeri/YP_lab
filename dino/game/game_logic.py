"""
Логика игры и состояния
"""
from enum import Enum
import pygame


class GameState(Enum):
    """Состояния игры"""
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3


def check_collision(dino, obstacle):
    """
    Проверка столкновения между динозавром и препятствием

    Args:
        dino: объект Dinosaur
        obstacle: объект Obstacle

    Returns:
        bool: True если есть столкновение
    """
    dino_rect = dino.get_rect()
    obstacle_rect = obstacle.get_rect()

    dino_rect = dino_rect.inflate(-15, -10)

    if obstacle.type == 'bird':
        obstacle_rect = obstacle_rect.inflate(-5, -5)

    return dino_rect.colliderect(obstacle_rect)
