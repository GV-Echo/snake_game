import pygame
import sys
import os
import json
import time
from config.const import LOCALE_FILENAME
from src.game.snake import Snake
from src.game.game_objects import Food, PoisonedFood, Bomb, Fan, Clock, DoublePoints, InvertedControls


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
        self.active_effects = []
        self.bonus_objects = []
        self.fps = 10
        self.score_multiplier = 1
        self.spawn_intervals = {
            "Food": 5,
            "PoisonedFood": 10,
            "Bomb": 15,
            "Fan": 20,
            "Clock": 25,
            "DoublePoints": 30,
            "InvertedControls": 35
        }
        self.last_spawn_time = {key: 0 for key in self.spawn_intervals}

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

    def spawn_bonus(self, bonus_class):
        max_count = bonus_class(self.cell_size, self.screen_width, self.screen_height).max_count
        if len([obj for obj in self.bonus_objects if isinstance(obj, bonus_class)]) < max_count:
            new_bonus = bonus_class(self.cell_size, self.screen_width, self.screen_height)
            self.bonus_objects.append(new_bonus)

    def update(self):
        self.snake.move(self.screen_width, self.screen_height)
        current_time = time.time()

        for effect in self.active_effects:
            effect_name, effect_end_time = effect
            if effect_name == "Speed Boost" and current_time < effect_end_time:
                self.fps = 20  # Ускорение в 2 раза
            elif effect_name == "Slow Down" and current_time < effect_end_time:
                self.fps = 7  # Замедление в 1.5 раза
            elif effect_name == "Double Points" and current_time < effect_end_time:
                self.score_multiplier = 2
            elif effect_name == "Inverted Controls" and current_time < effect_end_time:
                self.snake.inverted_controls = True
            else:
                self.snake.inverted_controls = False

        for bonus_type, interval in self.spawn_intervals.items():
            if current_time - self.last_spawn_time[bonus_type] > interval:
                if bonus_type == "Food":
                    self.spawn_bonus(Food)
                elif bonus_type == "PoisonedFood":
                    self.spawn_bonus(PoisonedFood)
                elif bonus_type == "Bomb" and len(self.snake.body) < 20:
                    self.spawn_bonus(Bomb)
                elif bonus_type == "Fan":
                    self.spawn_bonus(Fan)
                elif bonus_type == "Clock":
                    self.spawn_bonus(Clock)
                elif bonus_type == "DoublePoints":
                    self.spawn_bonus(DoublePoints)
                elif bonus_type == "InvertedControls":
                    self.spawn_bonus(InvertedControls)
                self.last_spawn_time[bonus_type] = current_time

        self.bonus_objects = [
            obj for obj in self.bonus_objects
            if time.time() - obj.spawn_time < obj.lifetime
        ]

        for obj in self.bonus_objects[:]:
            if self.snake.check_collision(obj.position):
                if isinstance(obj, PoisonedFood):
                    if len(self.snake.body) > 1:
                        self.snake.body.pop()
                    self.score -= 8
                elif isinstance(obj, Bomb):
                    self.running = False
                elif isinstance(obj, Fan):
                    self.active_effects.append(
                        ("Speed Boost", current_time + 15))
                    self.score += 3 * self.score_multiplier
                elif isinstance(obj, Clock):
                    self.active_effects.append(
                        ("Slow Down", current_time + 15))
                    self.score += 3 * self.score_multiplier
                elif isinstance(obj, DoublePoints):
                    self.active_effects.append(
                        ("Double Points", current_time + 60))
                    self.score += 5 * self.score_multiplier
                elif isinstance(obj, InvertedControls):
                    self.active_effects.append(
                        ("Inverted Controls", current_time + 15))
                    self.score += 9 * self.score_multiplier
                elif isinstance(obj, Food):
                    self.snake.grow()
                    self.score += 10 * self.score_multiplier
                self.bonus_objects.remove(obj)

        self.active_effects = [
            effect for effect in self.active_effects if effect[1] > current_time]
        if not any(effect[0] in ["Speed Boost", "Slow Down"] for effect in self.active_effects):
            self.fps = 10
        if not any(effect[0] in ["Double Points"] for effect in self.active_effects):
            self.score_multiplier = 1

        if self.snake.check_self_collision() or self.snake.check_wall_collision(self.screen_width, self.screen_height):
            self.running = False

    def render(self, screen):
        screen.fill((0, 0, 0))
        for obj in self.bonus_objects:
            color = (255, 0, 0)
            if isinstance(obj, PoisonedFood):
                color = (128, 0, 128)
            elif isinstance(obj, Bomb):
                color = (255, 255, 0)
            elif isinstance(obj, Fan):
                color = (0, 0, 255)
            elif isinstance(obj, Clock):
                color = (0, 255, 255)
            elif isinstance(obj, DoublePoints):
                color = (255, 165, 0)
            elif isinstance(obj, InvertedControls):
                color = (255, 20, 147)
            pygame.draw.rect(screen, color, pygame.Rect(
                obj.position[0], obj.position[1], self.cell_size, self.cell_size))

        for segment in self.snake.body:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(
                segment[0], segment[1], self.cell_size, self.cell_size))

        score_text = f"{self.texts['score_label']}: {self.score:04}"
        score_surface = self.font.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(
            topright=(self.screen_width - 10, 10))
        screen.blit(score_surface, score_rect)

        effect_font = pygame.font.Font(None, 24)
        y_offset = self.screen_height - 20
        for effect in self.active_effects:
            effect_text = effect_font.render(effect[0], True, (255, 255, 255))
            screen.blit(effect_text, (10, y_offset))
            y_offset -= 20

    def run(self, screen):
        while self.running:
            self.handle_events()
            self.update()
            self.render(screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()
        sys.exit()
