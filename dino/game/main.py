"""
Игра с динозавром - улучшенная версия
Управление: ПРОБЕЛ - прыжок
"""
import math
import os
import random
import sys

import pygame

from database.db_handler import DatabaseHandler
from game.game_logic import check_collision
from game.game_objects import Bird, Cactus, Dino

WIDTH = 800
HEIGHT = 300
GROUND = 250
FPS = 60


class Game:
    def __init__(self, headless: bool = False, disable_audio: bool = False, db_path: str = "dino_game.db"):
        if headless:
            os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        if disable_audio:
            os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

        pygame.init()
        if not disable_audio:
            try:
                pygame.mixer.init()
            except pygame.error:
                disable_audio = True

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chrome Dino Game")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.create_sounds(disable_audio)

        self.db = DatabaseHandler(db_path)

        self.reset_game()

        print("Игра готова! SPACE - прыжок/старт, ESC - выход")

    def create_sounds(self, disable_audio: bool):
        if disable_audio or not pygame.mixer.get_init():
            self.jump_sound = None
            self.crash_sound = None
            self.score_sound = None
            return

        try:
            self.jump_sound = pygame.mixer.Sound(self.generate_tone(600, 150))
            self.jump_sound.set_volume(0.3)

            self.crash_sound = pygame.mixer.Sound(self.generate_tone(150, 400))
            self.crash_sound.set_volume(0.4)

            self.score_sound = pygame.mixer.Sound(self.generate_tone(800, 100))
            self.score_sound.set_volume(0.2)
        except pygame.error:
            print("Звуки не созданы - игра будет без звука")
            self.jump_sound = None
            self.crash_sound = None
            self.score_sound = None

    def generate_tone(self, freq, duration):
        sample_rate = 22050
        n_samples = int(sample_rate * duration / 1000)

        buf = bytearray(n_samples * 2)

        for i in range(n_samples):
            t = float(i) / sample_rate
            sample = 32767 * 0.3 * math.sin(2 * math.pi * freq * t)
            sample *= (1.0 - float(i) / n_samples)

            val = int(sample)
            buf[2 * i] = val & 0xff
            buf[2 * i + 1] = (val >> 8) & 0xff

        return bytes(buf)

    def reset_game(self):
        self.dino = Dino(80, GROUND - 60)

        self.obstacles: list[Bird | Cactus] = []
        self.obstacle_timer = 0
        self.min_obstacle_distance = 300

        self.clouds: list[list[int]] = []

        self.score = 0
        self.high_score = self.db.get_best_score() if self.db else 0
        self.game_speed = 8
        self.game_state = "menu"

        self.frame_count = 0
        self.last_score_sound = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == "menu":
                        self.start_game()
                    elif self.game_state == "playing":
                        self.dino_jump()
                    elif self.game_state == "game_over":
                        self.start_game()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def dino_jump(self):
        if not self.dino.jumping:
            self.dino.jump()
            if self.jump_sound:
                self.jump_sound.play()

    def start_game(self):
        self.reset_game()
        self.game_state = "playing"

    def update(self):
        self.frame_count += 1

        if self.game_state != "playing":
            return

        self.dino.update()

        for cloud in self.clouds[:]:
            cloud[0] -= self.game_speed // 3
            if cloud[0] < -60:
                self.clouds.remove(cloud)

        if random.randint(0, 100) < 2:
            self.clouds.append([WIDTH, random.randint(50, 150)])

        for obstacle in self.obstacles[:]:
            obstacle.x -= self.game_speed

            if obstacle.x < -50:
                self.obstacles.remove(obstacle)
                continue

            if check_collision(self.dino, obstacle):
                if self.crash_sound:
                    self.crash_sound.play()
                self.game_state = "game_over"
                if self.score > self.high_score:
                    self.high_score = self.score
                    if self.db:
                        self.db.save_score("Player", self.score)
                break

        self.obstacle_timer += 1

        if self.obstacle_timer > 60:
            can_add = True
            if self.obstacles:
                last_obstacle = self.obstacles[-1]
                distance = WIDTH - last_obstacle.x
                if distance < self.min_obstacle_distance:
                    can_add = False

            if can_add and random.randint(0, 100) < 15:
                obstacle_type = random.choice(["cactus", "cactus", "bird"])
                if obstacle_type == "cactus":
                    obstacle = Cactus(WIDTH, GROUND - 40)
                else:
                    obstacle = Bird(WIDTH, GROUND - 80 + random.randint(-10, 10))

                self.obstacles.append(obstacle)
                self.obstacle_timer = 0
                self.min_obstacle_distance = random.randint(250, 400)

        old_score = self.score
        self.score += 1

        if old_score // 100 < self.score // 100:
            if self.score_sound and self.frame_count - self.last_score_sound > 60:
                self.score_sound.play()
                self.last_score_sound = self.frame_count

        if self.score % 500 == 0 and self.game_speed < 20:
            self.game_speed += 1

    def draw_dino(self):
        x, y = self.dino.x, self.dino.y

        body_color = (64, 120, 82)
        belly_color = (128, 176, 140)
        shadow_color = (40, 80, 60)
        eye_color = (255, 255, 255)
        pupil_color = (30, 40, 60)

        pygame.draw.ellipse(self.screen, shadow_color, (x - 10, y + 52, 70, 12))

        pygame.draw.rect(self.screen, body_color, (x, y + 10, 52, 42), border_radius=12)
        pygame.draw.ellipse(self.screen, body_color, (x, y + 5, 52, 32))
        pygame.draw.ellipse(self.screen, belly_color, (x + 8, y + 14, 36, 26))

        leg_y = y + 42
        pygame.draw.rect(self.screen, body_color, (x + 6, leg_y, 12, 22), border_radius=4)
        pygame.draw.rect(self.screen, body_color, (x + 32, leg_y + 2, 12, 20), border_radius=4)

        head_x = x + 46
        head_y = y + 8
        pygame.draw.ellipse(self.screen, body_color, (head_x - 6, head_y, 26, 24))
        pygame.draw.ellipse(self.screen, body_color, (head_x - 6, head_y + 12, 22, 14))

        pygame.draw.circle(self.screen, eye_color, (head_x + 10, head_y + 8), 6)
        pygame.draw.circle(self.screen, pupil_color, (head_x + 11, head_y + 8), 3)
        pygame.draw.circle(self.screen, (240, 240, 240), (head_x + 8, head_y + 6), 2)

        mouth_y = head_y + 18 + (2 if self.dino.jumping else 0)
        pygame.draw.line(self.screen, pupil_color, (head_x, mouth_y), (head_x + 12, mouth_y), 2)

        tail_points = [
            (x - 4, y + 32),
            (x - 18, y + 28),
            (x - 6, y + 24),
            (x - 22, y + 20),
            (x - 8, y + 18),
            (x - 2, y + 22)
        ]
        pygame.draw.polygon(self.screen, body_color, tail_points)

        for i in range(4):
            plate_x = x + 12 + i * 10
            plate_height = 10 + (i % 2) * 4
            pygame.draw.polygon(self.screen, (70, 110, 90),
                                [(plate_x, y + 8),
                                 (plate_x + 6, y - plate_height + 8),
                                 (plate_x + 12, y + 8)])

    def draw_obstacle(self, obstacle):
        x, y = obstacle.x, obstacle.y

        if obstacle.type == "cactus":
            stem_color = (0, 140, 0)
            detail_color = (0, 180, 0)

            pygame.draw.rect(self.screen, stem_color,
                             (x, y, 20, 40))

            pygame.draw.rect(self.screen, stem_color,
                             (x - 8, y + 10, 10, 8))
            pygame.draw.rect(self.screen, stem_color,
                             (x + 18, y + 25, 10, 6))

            for i in range(3):
                needle_y = y + 10 + i * 12
                pygame.draw.line(self.screen, detail_color,
                                 (x - 5, needle_y),
                                 (x, needle_y), 2)
                pygame.draw.line(self.screen, detail_color,
                                 (x + 20, needle_y),
                                 (x + 25, needle_y), 2)

        else:  # bird
            body_color = (220, 100, 100)
            wing_color = (240, 150, 150)
            beak_color = (255, 200, 100)

            pygame.draw.ellipse(self.screen, body_color,
                                (x, y, 35, 20))

            wing_offset = math.sin(self.frame_count * 0.2) * 3
            pygame.draw.ellipse(self.screen, wing_color,
                                (x + 8, y + 5 + wing_offset, 15, 10))

            pygame.draw.circle(self.screen, (255, 255, 255),
                               (x + 25, y + 8), 4)
            pygame.draw.circle(self.screen, (0, 0, 0),
                               (x + 26, y + 8), 2)

            pygame.draw.polygon(self.screen, beak_color,
                                [(x + 35, y + 8),
                                 (x + 45, y + 10),
                                 (x + 35, y + 12)])

    def draw(self):
        self.screen.fill((230, 240, 255))

        pygame.draw.circle(self.screen, (255, 255, 200),
                           (700, 80), 30)

        for cloud in self.clouds:
            x, y = cloud
            pygame.draw.ellipse(self.screen, (250, 250, 250),
                                (x, y, 60, 30))
            pygame.draw.ellipse(self.screen, (250, 250, 250),
                                (x + 15, y - 8, 40, 25))

        pygame.draw.rect(self.screen, (180, 160, 140),
                         (0, GROUND, WIDTH, HEIGHT - GROUND))

        for i in range(0, WIDTH, 20):
            height = 5 + (i % 40) // 20 * 3
            pygame.draw.line(self.screen, (140, 180, 100),
                             (i, GROUND),
                             (i + 10, GROUND - height), 2)

        for obstacle in self.obstacles:
            self.draw_obstacle(obstacle)

        self.draw_dino()

        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (20, 20))

        high_score_text = self.small_font.render(f"Best: {self.high_score}",
                                                 True, (100, 100, 100))
        self.screen.blit(high_score_text, (20, 60))

        speed_text = self.small_font.render(f"Speed: {self.game_speed}",
                                            True, (150, 100, 50))
        self.screen.blit(speed_text, (WIDTH - 120, 20))

        if self.game_state == "menu":
            title = self.font.render("CHROME DINO", True, (0, 100, 200))
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

            instruction = self.font.render("Press SPACE to START", True, (50, 150, 50))
            self.screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, 170))

            controls = self.small_font.render("SPACE: Jump  |  ESC: Exit", True, (100, 100, 100))
            self.screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, 220))

        elif self.game_state == "game_over":
            # Полупрозрачный фон
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            game_over = self.font.render("GAME OVER", True, (255, 100, 100))
            self.screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, 120))

            final_score = self.font.render(f"Score: {self.score}", True, (255, 255, 200))
            self.screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 170))

            restart = self.font.render("Press SPACE to restart", True, (150, 255, 150))
            self.screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 220))

    def run(self):
        """Главный цикл игры"""
        try:
            while True:
                self.handle_events()
                self.update()
                self.draw()

                pygame.display.flip()
                self.clock.tick(FPS)
        finally:
            if self.db:
                self.db.close()
            pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
