import pygame
import sys
import json
import os
from pygame.font import Font
from config.const import LOCALE_FILE_NAME


class MainMenu:
    def __init__(self, screen_width, screen_height, language="en"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = []
        self.title_font = None
        self.button_font = None
        self.language = language
        self.texts = self.load_locale()
        self.initialize()

    def load_locale(self):
        locale_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   "localization", LOCALE_FILE_NAME)

        if not os.path.exists(locale_path):
            print(f"File error: {LOCALE_FILE_NAME} not found at {locale_path}")
            pygame.quit()
            sys.exit(1)

        try:
            with open(locale_path, 'r', encoding='utf-8') as file:
                localization_data = json.load(file)
                return localization_data[self.language]

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Critical error while loading localization: {e}")
            pygame.quit()
            sys.exit(1)

    def initialize(self):
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 80)
        self.button_font = pygame.font.Font(None, 50)

        button_width = 210
        button_height = 50
        button_x = self.screen_width // 2 - button_width // 2
        button_y_start = self.screen_height // 2 - 75

        self.buttons = [
            {
                "rect": pygame.Rect(button_x, button_y_start, button_width, button_height),
                "text": self.texts["buttons"]["start_game"],
                "action": self.start_game
            },
            {
                "rect": pygame.Rect(button_x, button_y_start + 75, button_width, button_height),
                "text": self.texts["buttons"]["settings"],
                "action": self.open_settings
            },
            {
                "rect": pygame.Rect(button_x, button_y_start + 150, button_width, button_height),
                "text": self.texts["buttons"]["exit"],
                "action": self.exit_game
            }
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        button["action"]()

    def render(self, screen):
        screen.fill((0, 0, 0))
        title_text = self.title_font.render(
            self.texts["title"], True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title_text, title_rect)

        for button in self.buttons:
            mouse_pos = pygame.mouse.get_pos()
            if button["rect"].collidepoint(mouse_pos):
                pygame.draw.rect(screen, (100, 100, 100),
                                 button["rect"], border_radius=5)
            else:
                pygame.draw.rect(screen, (70, 70, 70),
                                 button["rect"], border_radius=5)

            text = self.button_font.render(
                button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            screen.blit(text, text_rect)

    def change_language(self, language):
        self.language = language
        self.texts = self.load_locale()

        for i, button_id in enumerate(["start_game", "settings", "exit"]):
            self.buttons[i]["text"] = self.texts["buttons"][button_id]

    def start_game(self):
        print("Starting game...")
        # TODO: Implement game start

    def open_settings(self):
        print("Opening settings...")
        # TODO: Implement settings menu

    def exit_game(self):
        pygame.quit()
        sys.exit()
