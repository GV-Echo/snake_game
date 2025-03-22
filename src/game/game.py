import pygame
import sys
import os
import json
import time
from config.const import CELL_SIZE, GAME_SPEED, LOCALE_FILENAME, BACKGROUND_IMAGE
from src.game.snake import Snake
from src.game.game_objects import Food, PoisonedFood, Bomb, Speedup, Clock, DoublePoints, InvertedControls


class Game:
    def __init__(self, screen_width, screen_height, language="en"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = CELL_SIZE
        self.running = True
        self.clock = pygame.time.Clock()
        self.snake = Snake(
            self.cell_size, self.screen_width, self.screen_height)
        self.score = 0
        self.language = language
        self.texts = self.load_locale()
        self.font = pygame.font.Font(None, 36)
        self.active_effects = []
        self.bonus_objects = pygame.sprite.Group()
        self.game_speed = GAME_SPEED
        self.score_multiplier = 1
        self.last_spawn_time = {}

        self.background = pygame.image.load(BACKGROUND_IMAGE).convert()
        self.background = pygame.transform.scale(
            self.background, (self.screen_width, self.screen_height)
        )

    def load_locale(self):
        locale_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   "localization", LOCALE_FILENAME)
        with open(locale_path, 'r', encoding='utf-8') as file:
            localization_data = json.load(file)
            return localization_data[self.language]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
        max_count = bonus_class(
            self.cell_size, self.screen_width, self.screen_height).max_count
        if len([obj for obj in self.bonus_objects if isinstance(obj, bonus_class)]) < max_count:
            new_bonus = bonus_class(
                self.cell_size, self.screen_width, self.screen_height)
            self.bonus_objects.add(new_bonus)

    def update(self):
        self.snake.move()
        current_time = time.time()

        self.spawn_food(current_time)
        self.delete_old_food(current_time)
        self.handle_collisions()
        self.update_active_effects(current_time)

    def spawn_food(self, current_time):
        for bonus_class in [Food, PoisonedFood, Bomb, Speedup, Clock, DoublePoints, InvertedControls]:
            if bonus_class not in self.last_spawn_time:
                self.last_spawn_time[bonus_class] = 0

            spawn_interval = bonus_class(
                self.cell_size, self.screen_width, self.screen_height).spawn_interval
            if current_time - self.last_spawn_time[bonus_class] > spawn_interval:
                self.spawn_bonus(bonus_class)
                self.last_spawn_time[bonus_class] = current_time

    def delete_old_food(self, current_time):
        for obj in list(self.bonus_objects):
            if current_time - obj.spawn_time >= obj.lifetime:
                self.bonus_objects.remove(obj)

    def handle_collisions(self):
        collided_objects = pygame.sprite.spritecollide(
            self.snake, self.bonus_objects, dokill=True
        )
        for obj in collided_objects:
            if isinstance(obj, PoisonedFood):
                if len(self.snake.body) > 1:
                    removed_segment = self.snake.body.pop()
                    for sprite in self.snake.body_sprites:
                        if sprite.rect.topleft == removed_segment:
                            self.snake.body_sprites.remove(sprite)
                            break
                elif len(self.snake.body) == 1 or self.score < 0:
                    self.score = 0
                    self.running = False
                self.score -= 8

            elif isinstance(obj, Bomb):
                self.running = False
            elif isinstance(obj, Speedup):
                self.active_effects.append(("Speed Boost", time.time() + 15))
                self.game_speed *= 2
                self.score += 3 * self.score_multiplier
            elif isinstance(obj, Clock):
                self.active_effects.append(("Slow Down", time.time() + 15))
                self.game_speed //= 1.5
                self.score += 3 * self.score_multiplier
            elif isinstance(obj, DoublePoints):
                self.active_effects.append(("Double Points", time.time() + 60))
                self.score_multiplier = 2
                self.score += 5 * self.score_multiplier
            elif isinstance(obj, InvertedControls):
                self.active_effects.append(
                    ("Inverted Controls", time.time() + 15))
                self.snake.inverted_controls = True
                self.score += 9 * self.score_multiplier
            elif isinstance(obj, Food):
                self.snake.grow()
                self.score += 10 * self.score_multiplier

        if self.snake.check_self_collision():
            self.running = False

    def update_active_effects(self, current_time):
        self.active_effects = [
            effect for effect in self.active_effects if effect[1] > current_time
        ]
        if not any(effect[0] in ["Speed Boost", "Slow Down"] for effect in self.active_effects):
            self.game_speed = 10
        if not any(effect[0] == "Double Points" for effect in self.active_effects):
            self.score_multiplier = 1
        if not any(effect[0] == "Inverted Controls" for effect in self.active_effects):
            self.snake.inverted_controls = False

    def render(self, screen):
        screen.blit(self.background, (0, 0))

        self.bonus_objects.draw(screen)
        self.snake.body_sprites.draw(screen)

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
            self.clock.tick(self.game_speed)
