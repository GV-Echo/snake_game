import pygame
import json
import os
from config.const import SETTINGS_FILENAME, LOCALE_FILENAME


class DeathWindow:
    def __init__(self, width, height, score, language="en"):
        self.width = width
        self.height = height
        self.score = score
        self.language = language
        self.texts = self.load_texts()
        self.font = pygame.font.Font(None, 50)
        self.restart_button = pygame.Rect(
            width // 2 - 130, height // 2 - 60, 250, 50)
        self.menu_button = pygame.Rect(
            width // 2 - 130, height // 2 + 10, 250, 50)

    def load_texts(self):
        locale_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   "localization", LOCALE_FILENAME)
        with open(locale_path, "r", encoding="utf-8") as file:
            texts = json.load(file)
            return texts.get(self.language, texts["en"])

    def render(self, screen):
        screen.fill((0, 0, 0))
        game_over_text = self.font.render(
            self.texts["game_over"], True, (255, 255, 255))
        score_text = self.font.render(
            f"{self.texts['score_label']}: {self.score}", True, (255, 255, 255))
        restart_text = self.font.render(
            self.texts["buttons"]["restart"], True, (0, 0, 0))
        menu_text = self.font.render(
            self.texts["buttons"]["menu"], True, (0, 0, 0))

        screen.blit(game_over_text, (self.width // 2 -
                    game_over_text.get_width() // 2, self.height // 2 - 200))
        screen.blit(score_text, (self.width // 2 -
                    score_text.get_width() // 2, self.height // 2 - 150))

        pygame.draw.rect(screen, (255, 255, 255), self.restart_button)
        pygame.draw.rect(screen, (255, 255, 255), self.menu_button)

        screen.blit(restart_text, (self.restart_button.x + self.restart_button.width // 2 - restart_text.get_width() // 2,
                                   self.restart_button.y + self.restart_button.height // 2 - restart_text.get_height() // 2))
        screen.blit(menu_text, (self.menu_button.x + self.menu_button.width // 2 - menu_text.get_width() // 2,
                                self.menu_button.y + self.menu_button.height // 2 - menu_text.get_height() // 2))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.restart_button.collidepoint(event.pos):
                    return "restart"
                elif self.menu_button.collidepoint(event.pos):
                    return "menu"
        return None
