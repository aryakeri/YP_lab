"""Тесты игровой логики на реальных объектах."""

import os
import sys
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from game.game_logic import check_collision  # noqa: E402
from game.game_objects import Bird, Cactus, Dino  # noqa: E402


class TestGameLogic(unittest.TestCase):
    def test_check_collision_with_cactus(self):
        dino = Dino(100, 200)
        cactus = Cactus(110, 200)  # пересекается с динозавром
        self.assertTrue(check_collision(dino, cactus))

    def test_check_collision_without_overlap(self):
        dino = Dino(100, 200)
        cactus = Cactus(300, 200)
        self.assertFalse(check_collision(dino, cactus))

    def test_check_collision_with_bird_hitbox(self):
        dino = Dino(100, 200)
        bird = Bird(115, 190)  # немного выше динозавра
        self.assertTrue(check_collision(dino, bird))


class TestDinoPhysics(unittest.TestCase):
    def test_full_jump_cycle(self):
        dino = Dino(50, 190)
        base_y = dino.y
        dino.jump()

        positions = []
        for _ in range(40):  # достаточно, чтобы завершить прыжок
            dino.update()
            positions.append(dino.y)

        self.assertEqual(dino.y, base_y)
        self.assertLess(min(positions), base_y)  # был пик прыжка выше земли
        self.assertFalse(dino.jumping)

    def test_reset(self):
        dino = Dino(50, 190)
        dino.jump()
        dino.update()
        dino.y += 10
        dino.reset()

        self.assertEqual(dino.y, dino.base_y)
        self.assertFalse(dino.jumping)
        self.assertEqual(dino.velocity, 0)


if __name__ == "__main__":
    unittest.main()
