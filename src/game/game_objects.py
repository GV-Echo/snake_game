import random
import time

class GameObject:
    def __init__(self, cell_size, screen_width, screen_height, max_count, lifetime, spawn_interval):
        self.cell_size = cell_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_count = max_count
        self.lifetime = lifetime
        self.spawn_interval = spawn_interval
        self.position = (0, 0)
        self.spawn_time = time.time()
        self.spawn([])

    def spawn(self, snake_body):
        while True:
            x = random.randint(0, (self.screen_width // self.cell_size) - 1) * self.cell_size
            y = random.randint(0, (self.screen_height // self.cell_size) - 1) * self.cell_size
            if (x, y) not in snake_body:
                self.position = (x, y)
                break


class Food(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=10, lifetime=60, spawn_interval=5)


class PoisonedFood(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=5, lifetime=15, spawn_interval=10)


class Bomb(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=3, lifetime=30, spawn_interval=15)


class Fan(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=3, lifetime=15, spawn_interval=20)


class Clock(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=1, lifetime=15, spawn_interval=25)


class DoublePoints(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=1, lifetime=60, spawn_interval=30)


class InvertedControls(GameObject):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height, max_count=1, lifetime=15, spawn_interval=35)