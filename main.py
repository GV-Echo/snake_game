import pygame
import sys
import json
from src.game.game import Game
from src.ui.main_menu import MainMenu
from config.const import GAME_TITLE, SETTINGS_FILENAME


def load_language():
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

    lang = load_language()
    if not lang:
        lang = "en"

    while True:
        main_menu = MainMenu(width, height, language=lang)
        running = True

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            main_menu.handle_events(events)
            main_menu.render(screen)
            pygame.display.flip()

            if hasattr(main_menu, "start_game_flag") and main_menu.start_game_flag:
                game = Game(width, height, language=lang)
                result = game.run(screen)

                if result == "restart":
                    continue
                elif result == "menu":
                    break


if __name__ == "__main__":
    main()
