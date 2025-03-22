import random
import time

class Food:
    def __init__(self, cell_size, screen_width, screen_height):
        self.cell_size = cell_size
        self.screen_width = screen_width
        self.screen_height = screen_height
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

class PoisonedFood(Food):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height)
        self.spawn_time = time.time()

class Bomb(Food):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height)
        self.spawn_time = time.time()

class Fan(Food):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height)
        self.spawn_time = time.time()

class Clock(Food):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height)
        self.spawn_time = time.time()

class DoublePoints(Food):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height)
        self.spawn_time = time.time()

class InvertedControls(Food):
    def __init__(self, cell_size, screen_width, screen_height):
        super().__init__(cell_size, screen_width, screen_height)
        self.spawn_time = time.time()