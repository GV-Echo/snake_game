import pygame
import os
import json
from config.const import LOCALE_FILENAME, SETTINGS_FILENAME, SOUND_ICON_ON, SOUND_ICON_OFF, FLAG_ICON_EN, FLAG_ICON_RU


class SettingsMenu:
    def __init__(self, screen_width, screen_height, language="en", sound_enabled=True, username="Player", border_mode=False):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.language = language
        self.sound_enabled = sound_enabled
        self.username = username
        self.input_active = False
        self.input_text = username
        self.buttons = []
        self.title_font = None
        self.button_font = None
        self.texts = None
        self.sound_icon_on = None
        self.sound_icon_off = None
        self.flag_icon_en = None
        self.flag_icon_ru = None
        self.border_mode = border_mode
        self.load_settings()
        self.initialize()

    def load_locale(self):
        locale_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   "localization", LOCALE_FILENAME)
        with open(locale_path, 'r', encoding='utf-8') as file:
            localization_data = json.load(file)
            self.texts = localization_data[self.language]

    def load_resources(self):
        self.load_locale()
        self.sound_icon_on = pygame.image.load(SOUND_ICON_ON)
        self.sound_icon_off = pygame.image.load(SOUND_ICON_OFF)
        self.flag_icon_en = pygame.image.load(FLAG_ICON_EN)
        self.flag_icon_ru = pygame.image.load(FLAG_ICON_RU)

    def initialize(self):
        self.load_resources()

        pygame.font.init()
        self.title_font = pygame.font.Font(None, 80)
        self.button_font = pygame.font.Font(None, 50)

        button_width = 140
        button_height = 50
        button_x_start = self.screen_width // 2 - (button_width * 2 + 10) // 2
        button_y_start = self.screen_height // 2 - 150

        self.buttons = [
            {
                "rect": pygame.Rect(button_x_start, button_y_start, button_width, button_height),
                "icon": self.sound_icon_on if self.sound_enabled else self.sound_icon_off,
                "action": self.toggle_sound
            },
            {
                "rect": pygame.Rect(button_x_start + button_width + 10, button_y_start, button_width, button_height),
                "icon": self.flag_icon_en if self.language == "en" else self.flag_icon_ru,
                "action": self.toggle_language
            }
        ]

        self.input_box = pygame.Rect(
            self.screen_width // 2 - 190, button_y_start + 75, 200, button_height)

        self.apply_button = {
            "rect": pygame.Rect(self.screen_width // 2 + 20, button_y_start + 75, 190, button_height),
            "text": self.texts["buttons"]["apply_name"],
            "action": self.apply_name
        }

        self.border_mode_button = {
            "rect": pygame.Rect(self.screen_width // 2 - 190, button_y_start + 150, 400, button_height),
            "text": f"{self.texts['buttons']['border_mode']}{self.texts['buttons']['border_on'] if self.border_mode else self.texts['buttons']['border_off']}",
            "action": self.toggle_border_mode
        }

        self.buttons.append({
            "rect": pygame.Rect(self.screen_width // 2 - 75, button_y_start + 225, 150, button_height),
            "text": self.texts["buttons"]["back"],
            "action": self.go_back
        })

    def load_settings(self):
        if os.path.exists(SETTINGS_FILENAME):
            with open(SETTINGS_FILENAME, 'r', encoding='utf-8') as file:
                settings = json.load(file)
                self.language = settings.get("language", "en")
                self.sound_enabled = settings.get("sound_enabled", True)
                self.username = settings.get("username", "Player")
                self.border_mode = settings.get("border_mode", False)
                self.input_text = self.username
        else:
            self.save_settings()

    def save_settings(self):
        settings = {
            "language": self.language,
            "sound_enabled": self.sound_enabled,
            "username": self.username,
            "border_mode": self.border_mode
        }
        with open(SETTINGS_FILENAME, 'w', encoding='utf-8') as file:
            json.dump(settings, file, indent=4)

    def get_settings(self):
        return {
            "language": self.language,
            "sound_enabled": self.sound_enabled,
            "username": self.username,
            "border_mode": self.border_mode
        }

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        button["action"]()
                if self.border_mode_button["rect"].collidepoint(mouse_pos):
                    self.border_mode_button["action"]()
                if self.apply_button["rect"].collidepoint(mouse_pos):
                    self.apply_button["action"]()
                if self.input_box.collidepoint(mouse_pos):
                    self.input_active = True
                else:
                    self.input_active = False

            if event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_RETURN:
                    self.input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    if len(self.input_text) < 9 and event.unicode.isalnum():
                        self.input_text += event.unicode

    def render(self, screen):
        screen.fill((0, 0, 0))

        title_text = self.title_font.render(
            self.texts["settings_title"], True, (255, 255, 255))
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

            if "icon" in button:
                icon = button["icon"]
                icon_rect = icon.get_rect(center=button["rect"].center)
                screen.blit(icon, icon_rect)
            else:
                text = self.button_font.render(
                    button["text"], True, (255, 255, 255))
                text_rect = text.get_rect(center=button["rect"].center)
                screen.blit(text, text_rect)

        border_button = self.border_mode_button
        if border_button["rect"].collidepoint(mouse_pos):
            pygame.draw.rect(screen, (100, 100, 100),
                             border_button["rect"], border_radius=5)
        else:
            pygame.draw.rect(screen, (70, 70, 70),
                             border_button["rect"], border_radius=5)

        border_text = self.button_font.render(
            border_button["text"], True, (255, 255, 255))
        border_text_rect = border_text.get_rect(
            center=border_button["rect"].center)
        screen.blit(border_text, border_text_rect)

        if self.input_active:
            pygame.draw.rect(screen, (255, 200, 200), self.input_box, 2)
        elif self.input_box.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (200, 200, 200), self.input_box, 2)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.input_box, 1)

        input_font = pygame.font.Font(None, 40)
        input_text = self.input_text

        is_cut = False
        while input_font.size(input_text)[0] > self.input_box.width - 20:
            input_text = input_text[1:]
            is_cut = True
        if is_cut:
            input_text += "..."

        input_surface = input_font.render(input_text, True, (255, 255, 255))
        screen.blit(input_surface, (self.input_box.x +
                    10, self.input_box.y + 10))

        if self.apply_button["rect"].collidepoint(mouse_pos):
            pygame.draw.rect(screen, (100, 100, 100),
                             self.apply_button["rect"], border_radius=5)
        else:
            pygame.draw.rect(screen, (70, 70, 70),
                             self.apply_button["rect"], border_radius=5)

        apply_text = self.button_font.render(
            self.apply_button["text"], True, (255, 255, 255))
        apply_text_rect = apply_text.get_rect(
            center=self.apply_button["rect"].center)
        screen.blit(apply_text, apply_text_rect)

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.buttons[0]["icon"] = self.sound_icon_on if self.sound_enabled else self.sound_icon_off
        self.save_settings()

    def toggle_language(self):
        self.language = "ru" if self.language == "en" else "en"
        self.load_locale()
        self.buttons[1]["icon"] = self.flag_icon_en if self.language == "en" else self.flag_icon_ru
        self.apply_button["text"] = self.texts["buttons"]["apply_name"]
        self.buttons[-1]["text"] = self.texts["buttons"]["back"]
        self.border_mode_button["text"] = f"{self.texts['buttons']['border_mode']}{self.texts['buttons']['border_on'] if self.border_mode else self.texts['buttons']['border_off']}"
        self.save_settings()

    def toggle_border_mode(self):
        self.border_mode = not self.border_mode
        self.border_mode_button["text"] = f"{self.texts['buttons']['border_mode']}{self.texts['buttons']['border_on'] if self.border_mode else self.texts['buttons']['border_off']}"
        self.save_settings()

    def apply_name(self):
        self.username = self.input_text
        print(f"Username applied: {self.username}")
        self.save_settings()

    def go_back(self):
        self.running = False
