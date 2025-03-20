import pygame
import sys
import json
from src.ui.main_menu import MainMenu
from config.const import GAME_TITLE, SETTINGS_FILENAME


def load_settings():
    try:
        with open(SETTINGS_FILENAME, 'r', encoding='utf-8') as file:
            settings = json.load(file)
            return settings.get("language", "en")
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error while loading settings: {e}")


def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(GAME_TITLE)

    language = load_settings()
    if not language:
        language = "en"

    main_menu = MainMenu(width, height, language=language)

    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        main_menu.handle_events(events)

        main_menu.render(screen)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
