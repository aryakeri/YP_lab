"""
Простые игровые объекты
"""
import pygame
import random


class Dino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.jumping = False
        self.velocity = 0
        self.gravity = 0.8
        self.jump_power = -15
        self.base_y = y
        self.color = (100, 100, 100)

    def jump(self):
        """Прыжок"""
        if not self.jumping:
            self.jumping = True
            self.velocity = self.jump_power

    def update(self):
        """Обновление позиции"""
        if self.jumping:
            self.y += self.velocity
            self.velocity += self.gravity

            if self.y >= self.base_y:
                self.y = self.base_y
                self.jumping = False
                self.velocity = 0

    def draw(self, screen):
        """Рисование динозавра"""
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))

        head_x = self.x + self.width - 10
        head_y = self.y + 10
        pygame.draw.rect(screen, self.color,
                         (head_x, head_y, 20, 15))

        eye_x = head_x + 12
        eye_y = head_y + 5
        pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), 4)
        pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), 2)

        leg_height = 25
        pygame.draw.rect(screen, self.color,
                         (self.x + 5, self.y + self.height, 10, leg_height))
        pygame.draw.rect(screen, self.color,
                         (self.x + 25, self.y + self.height, 10, leg_height))

        tail_points = [
            (self.x, self.y + 30),
            (self.x - 20, self.y + 25),
            (self.x - 15, self.y + 35),
            (self.x, self.y + 40)
        ]
        pygame.draw.polygon(screen, self.color, tail_points)

    def reset(self):
        """Сброс позиции"""
        self.y = self.base_y
        self.jumping = False
        self.velocity = 0

    def get_rect(self):
        """Прямоугольник для коллизий"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Cactus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 40
        self.color = (0, 150, 0)
        self.type = 'cactus'

    def draw(self, screen):
        """Рисование кактуса"""
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))

        if random.random() > 0.5:
            pygame.draw.rect(screen, self.color,
                             (self.x - 10, self.y + 10, 12, 8))

        for i in range(3):
            y_pos = self.y + 10 + i * 10
            pygame.draw.line(screen, (0, 200, 0),
                             (self.x - 5, y_pos),
                             (self.x, y_pos), 2)
            pygame.draw.line(screen, (0, 200, 0),
                             (self.x + self.width, y_pos),
                             (self.x + self.width + 5, y_pos), 2)

    def get_rect(self):
        """Прямоугольник для коллизий"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.color = (255, 100, 100)
        self.wing_up = False
        self.wing_timer = 0
        self.type = 'bird'

    def draw(self, screen):
        """Рисование птицы"""
        self.wing_timer += 1
        if self.wing_timer > 10:
            self.wing_up = not self.wing_up
            self.wing_timer = 0

        pygame.draw.ellipse(screen, self.color,
                            (self.x, self.y, self.width, self.height))

        wing_y = self.y + 5 if self.wing_up else self.y + 8
        pygame.draw.ellipse(screen, (255, 150, 150),
                            (self.x + 10, wing_y, 15, 8))

        pygame.draw.circle(screen, (255, 255, 255),
                           (self.x + 30, self.y + 8), 5)
        pygame.draw.circle(screen, (0, 0, 0),
                           (self.x + 32, self.y + 8), 2)

        pygame.draw.polygon(screen, (255, 200, 0),
                            [(self.x + self.width, self.y + 7),
                             (self.x + self.width + 8, self.y + 10),
                             (self.x + self.width, self.y + 13)])

    def get_rect(self):
        """Прямоугольник для коллизий"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 30
