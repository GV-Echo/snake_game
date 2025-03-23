import random
import time
import pygame
from config.const import (
    FOOD_IMAGE,
    INVERTED_CONTROLS_IMAGE,
    DOUBLE_POINTS_IMAGE,
    POISONED_FOOD_IMAGE,
    SPEEDUP_IMAGE,
    BOMB_IMAGE,
    CLOCK_IMAGE
)


class GameObject(pygame.sprite.Sprite):
    def __init__(self, cell_size, screen_width, screen_height, max_count, lifetime, spawn_interval, color):
        super().__init__()
        self.cell_size = cell_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_count = max_count
        self.lifetime = lifetime
        self.spawn_interval = spawn_interval
        self.spawn_time = time.time()

        self.image = pygame.Surface((cell_size, cell_size))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.spawn([])

    def spawn(self, snake_body):
        while True:
            x = random.randint(
                0, (self.screen_width // self.cell_size) - 1) * self.cell_size
            y = random.randint(
                0, (self.screen_height // self.cell_size) - 1) * self.cell_size
            if (x, y) not in snake_body:
                self.rect.topleft = (x, y)
                break


# Еда стандартная, увелечение змейки, макс. увелечение очков
class Food(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height,
                         max_count=10, lifetime=60, spawn_interval=5, color=(255, 0, 0))
        self.image = pygame.image.load(FOOD_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))


# Яд, уменьшение змейки, макс. уменьшие очков
class PoisonedFood(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=5,
                         lifetime=15, spawn_interval=10, color=(128, 0, 128))
        self.image = pygame.image.load(POISONED_FOOD_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))


# Бомба - сразу завершает игру
class Bomb(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=3,
                         lifetime=30, spawn_interval=15, color=(255, 255, 0))
        self.image = pygame.image.load(BOMB_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))


# Ускорение змейки
class Speedup(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height,
                         max_count=3, lifetime=15, spawn_interval=20, color=(0, 0, 255))
        self.image = pygame.image.load(SPEEDUP_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))


# Замедление змейки
class Clock(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=1,
                         lifetime=15, spawn_interval=25, color=(0, 255, 255))
        self.image = pygame.image.load(CLOCK_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))


# Удвоение ПОЛУЧАЕМЫХ очков
class DoublePoints(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=1,
                         lifetime=60, spawn_interval=30, color=(255, 165, 0))
        self.image = pygame.image.load(DOUBLE_POINTS_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))


# Инвертирование управления
class InvertedControls(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=1,
                         lifetime=15, spawn_interval=35, color=(255, 20, 147))
        self.image = pygame.image.load(INVERTED_CONTROLS_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
