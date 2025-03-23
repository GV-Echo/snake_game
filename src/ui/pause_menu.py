import sys
import pygame
import os
import json
from config.const import LOCALE_FILENAME


class PauseMenu:
    def __init__(self, screen_width, screen_height, language="en"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.language = language
        self.texts = self.load_locale()
        self.title_font = pygame.font.Font(None, 80)
        self.button_font = pygame.font.Font(None, 50)
        self.buttons = self.initialize_buttons()

    def load_locale(self):
        locale_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   "localization", LOCALE_FILENAME)
        with open(locale_path, 'r', encoding='utf-8') as file:
            localization_data = json.load(file)
            return localization_data[self.language]

    def initialize_buttons(self):
        button_width = 250
        button_height = 50
        button_spacing = 20
        button_x_start = self.screen_width // 2 - (button_width * 2 + button_spacing) // 2
        button_y = self.screen_height // 2 + 50

        return [
            {
                "rect": pygame.Rect(button_x_start, button_y, button_width, button_height),
                "text": self.texts["buttons"]["continue"],
                "action": "resume"
            },
            {
                "rect": pygame.Rect(button_x_start + button_width + button_spacing, button_y, button_width, button_height),
                "text": self.texts["buttons"]["menu"],
                "action": "menu"
            }
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        return button["action"]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        return None

    def render(self, screen):
        screen.fill((0, 0, 0))

        title_text = self.title_font.render(self.texts["pause_title"], True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(title_text, title_rect)

        for button in self.buttons:
            mouse_pos = pygame.mouse.get_pos()
            if button["rect"].collidepoint(mouse_pos):
                pygame.draw.rect(screen, (100, 100, 100), button["rect"], border_radius=5)
            else:
                pygame.draw.rect(screen, (70, 70, 70), button["rect"], border_radius=5)

            text = self.button_font.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            screen.blit(text, text_rect)