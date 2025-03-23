import pygame
import json
from config.const import LOCALE_FILENAME
from config.const import (
    FOOD_IMAGE,
    POISONED_FOOD_IMAGE,
    BOMB_IMAGE,
    SPEEDUP_IMAGE,
    CLOCK_IMAGE,
    DOUBLE_POINTS_IMAGE,
    INVERTED_CONTROLS_IMAGE
)


class HelpWindow:
    def __init__(self, screen_width, screen_height, language="en"):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.language = language
        self.texts = self.load_locale()
        self.font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 60)
        self.back_button = pygame.Rect(
            screen_width // 2 - 100, screen_height - 90, 200, 50)
        self.scroll_offset = 0

        self.images = {
            "Food": pygame.image.load(FOOD_IMAGE).convert_alpha(),
            "Poisoned Food": pygame.image.load(POISONED_FOOD_IMAGE).convert_alpha(),
            "Bomb": pygame.image.load(BOMB_IMAGE).convert_alpha(),
            "Speedup": pygame.image.load(SPEEDUP_IMAGE).convert_alpha(),
            "Clock": pygame.image.load(CLOCK_IMAGE).convert_alpha(),
            "Double Points": pygame.image.load(DOUBLE_POINTS_IMAGE).convert_alpha(),
            "Inverted Controls": pygame.image.load(INVERTED_CONTROLS_IMAGE).convert_alpha(),
        }

        for key in self.images:
            self.images[key] = pygame.transform.scale(
                self.images[key], (40, 40))
        self.localized_object_names = {
            "Poisoned Food": {"en": "Poisoned Food", "ru": "Яд"},
            "Food": {"en": "Food", "ru": "Еда"},
            "Bomb": {"en": "Bomb", "ru": "Бомба"},
            "Speedup": {"en": "Speedup", "ru": "Ускорение"},
            "Clock": {"en": "Clock", "ru": "Часы"},
            "Double Points": {"en": "Double Points", "ru": "Двойные очки"},
            "Inverted Controls": {"en": "Inverted Controls", "ru": "Инверсия"},
        }

    def load_locale(self):
        with open(LOCALE_FILENAME, 'r', encoding='utf-8') as file:
            return json.load(file)[self.language]

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            if font.size(' '.join(current_line))[0] > max_width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))
        return lines

    def calculate_height(self):
        total_height = 0

        for line in self.texts["help_window"]["help_content"]:
            wrapped_lines = self.wrap_text(
                line, self.font, self.screen_width - 120)
            total_height += len(wrapped_lines) * 50

        return total_height

    def render(self, screen):
        screen.fill((0, 0, 0))
        title_text = self.title_font.render(
            self.texts["help_window"]["help_title"], True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        screen.blit(title_text, title_rect)

        scroll_area = pygame.Rect(
            50, 100, self.screen_width - 100, self.screen_height - 200)
        pygame.draw.rect(screen, (30, 30, 30), scroll_area)

        clip_rect = screen.get_clip()
        screen.set_clip(scroll_area)
        y_offset = 120 + self.scroll_offset
        for line in self.texts["help_window"]["help_content"]:
            wrapped_lines = self.wrap_text(
                line, self.font, self.screen_width - 100)
            for wrapped_line in wrapped_lines:
                is_game_object = any(
                    localized_names.get(self.language, obj_key) in wrapped_line
                    for obj_key, localized_names in self.localized_object_names.items()
                )
                if is_game_object:
                    for obj_key, localized_names in self.localized_object_names.items():
                        localized_name = localized_names.get(
                            self.language, obj_key)
                        if localized_name in wrapped_line:
                            screen.blit(self.images[obj_key], (60, y_offset))
                            wrapped_line = wrapped_line.replace(
                                localized_name, "")
                            break
                    line_surface = self.font.render(
                        wrapped_line, True, (255, 255, 255))
                    screen.blit(line_surface, (110, y_offset))
                else:
                    line_surface = self.font.render(
                        wrapped_line, True, (255, 255, 255))
                    screen.blit(line_surface, (60, y_offset))
                y_offset += 50
        screen.set_clip(clip_rect)

        mouse_pos = pygame.mouse.get_pos()
        if self.back_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (100, 100, 100),
                             self.back_button, border_radius=5)
        else:
            pygame.draw.rect(screen, (70, 70, 70),
                             self.back_button, border_radius=5)

        back_text = self.font.render(
            self.texts["buttons"]["back"], True, (255, 255, 255))
        back_rect = back_text.get_rect(center=self.back_button.center)
        screen.blit(back_text, back_rect)

    def handle_events(self, events):
        total_height = self.calculate_height()
        visible_height = self.screen_height - 200

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.collidepoint(event.pos):
                    return "menu"
            elif event.type == pygame.MOUSEWHEEL:
                self.scroll_offset += event.y * 20
                self.scroll_offset = max(
                    min(self.scroll_offset, 0),
                    min(visible_height - total_height, 0)
                )

        return None
