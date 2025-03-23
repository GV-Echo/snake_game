import os
import pygame
import json
from config.scores_work import load_best_scores
from config.const import LOCALE_FILENAME


class RatingWindow:
    def __init__(self, screen_width, screen_height, language="en"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.language = language
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 80)
        self.back_button = pygame.Rect(
            screen_width // 2 - 100, screen_height - 100, 200, 50)
        self.best_scores = self.load_scores()

        with open(LOCALE_FILENAME, 'r', encoding='utf-8') as f:
            self.locale = json.load(f)

    def load_scores(self):
        scores = load_best_scores()
        sorted_scores = sorted(
            scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_scores[:8]

    def render(self, screen):
        screen.fill((0, 0, 0))

        title_text = self.locale[self.language]["rating_window"]["title"]
        back_button_text = self.locale[self.language]["rating_window"]["back_button"]

        title_surface = self.title_font.render(
            title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(
            center=(self.screen_width // 2, 50))
        screen.blit(title_surface, title_rect)

        y_offset = 100
        for i, (name, score) in enumerate(self.best_scores, start=1):
            player_text = f"{i}. {name} - {score}"
            player_surface = self.small_font.render(
                player_text, True, (255, 255, 255))
            screen.blit(player_surface, (self.screen_width // 2 -
                                         player_surface.get_width() // 2, y_offset))
            y_offset += 50

        pygame.draw.rect(screen, (70, 70, 70),
                         self.back_button, border_radius=5)
        back_surface = self.font.render(
            back_button_text, True, (255, 255, 255))
        back_rect = back_surface.get_rect(center=self.back_button.center)
        screen.blit(back_surface, back_rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.collidepoint(event.pos):
                    return "menu"

        return None
