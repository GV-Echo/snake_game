import pygame
import sys
import json
import os
from config.const import LOCALE_FILENAME
from src.ui.rating_window import RatingWindow
from src.ui.help_window import HelpWindow


class MainMenu:
    def __init__(self, screen_width, screen_height, language="en", border_mode=True):
        self.border_mode = border_mode
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = []
        self.title_font = None
        self.button_font = None
        self.language = language
        self.texts = self.load_locale()
        self.start_game_flag = False
        self.open_settings_flag = False
        self.initialize()

    def load_locale(self):
        if not os.path.exists(LOCALE_FILENAME):
            print(f"File error: {LOCALE_FILENAME} not found")
            pygame.quit()
            sys.exit(1)

        try:
            with open(LOCALE_FILENAME, 'r', encoding='utf-8') as file:
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

        button_width = 220
        button_height = 50
        button_spacing = 20

        first_row_y = self.screen_height // 2 - 100
        first_row_x_start = self.screen_width // 2 - \
                            (button_width + button_spacing // 2)

        second_row_y = first_row_y + button_height + button_spacing
        second_row_x_start = self.screen_width // 2 - \
                             (button_width + button_spacing // 2)

        third_row_y = second_row_y + button_height + button_spacing
        third_row_x = self.screen_width // 2 - button_width // 2

        self.buttons = [
            {
                "rect": pygame.Rect(first_row_x_start, first_row_y, button_width, button_height),
                "text": self.texts["buttons"]["start_game"],
                "action": self.start_game
            },
            {
                "rect": pygame.Rect(first_row_x_start + button_width + button_spacing, first_row_y, button_width,
                                    button_height),
                "text": self.texts["buttons"]["settings"],
                "action": self.open_settings
            },

            {
                "rect": pygame.Rect(second_row_x_start, second_row_y, button_width, button_height),
                "text": self.texts["buttons"]["help"],
                "action": self.show_help
            },
            {
                "rect": pygame.Rect(second_row_x_start + button_width + button_spacing, second_row_y, button_width,
                                    button_height),
                "text": self.texts["buttons"]["top_players"],
                "action": self.show_top_players
            },

            {
                "rect": pygame.Rect(third_row_x, third_row_y, button_width, button_height),
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

        for i, button_id in enumerate(["start_game", "settings", "help", "top_players", "exit"]):
            self.buttons[i]["text"] = self.texts["buttons"][button_id]

    def start_game(self):
        self.start_game_flag = True

    def open_settings(self):
        self.open_settings_flag = True

    def show_help(self):
        help_window = HelpWindow(self.screen_width, self.screen_height, self.language)
        running = True

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            action = help_window.handle_events(events)
            if action == "menu":
                running = False

            help_window.render(pygame.display.get_surface())
            pygame.display.flip()

    def show_top_players(self):
        rating_window = RatingWindow(self.screen_width, self.screen_height, self.language)
        running = True

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            action = rating_window.handle_events(events)
            if action == "menu":
                running = False

            rating_window.render(pygame.display.get_surface())
            pygame.display.flip()

    def exit_game(self):
        pygame.quit()
        sys.exit()
