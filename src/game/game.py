import pygame
import sys
import os
import json
from config.const import LOCALE_FILENAME
from src.game.snake import Snake
from src.game.game_objects import Food

class Game:
    def __init__(self, screen_width, screen_height, language="en"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = 20
        self.running = True
        self.clock = pygame.time.Clock()
        self.snake = Snake(self.cell_size)
        self.food = Food(self.cell_size, self.screen_width, self.screen_height)
        self.score = 0
        self.language = language
        self.texts = self.load_locale()
        self.font = pygame.font.Font(None, 36)

    def load_locale(self):
        locale_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   "localization", LOCALE_FILENAME)
        with open(locale_path, 'r', encoding='utf-8') as file:
            localization_data = json.load(file)
            return localization_data[self.language]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction("RIGHT")

    def update(self):
        self.snake.move(self.screen_width, self.screen_height)
        if self.snake.check_collision(self.food.position):
            self.snake.grow()
            self.food.spawn(self.snake.body)
            self.score += 1

        if self.snake.check_self_collision() or self.snake.check_wall_collision(self.screen_width, self.screen_height):
            self.running = False

    def render(self, screen):
        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
            self.food.position[0], self.food.position[1], self.cell_size, self.cell_size))

        for segment in self.snake.body:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(
                segment[0], segment[1], self.cell_size, self.cell_size))

        score_text = f"{self.texts['score_label']}: {self.score:04}"
        score_surface = self.font.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(topright=(self.screen_width - 10, 10))
        screen.blit(score_surface, score_rect)

    def run(self, screen):
        while self.running:
            self.handle_events()
            self.update()
            self.render(screen)
            pygame.display.flip()
            self.clock.tick(10)
        pygame.quit()
        sys.exit()