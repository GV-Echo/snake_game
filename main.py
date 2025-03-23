import pygame
import sys
import json
from src.game.game import Game
from src.ui.main_menu import MainMenu
from config.const import GAME_TITLE, SETTINGS_FILENAME, SOUNDTRACK_PATH


def load_settings():
    try:
        with open(SETTINGS_FILENAME, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error while loading settings: {e}")
        return {"language": "en", "border_mode": True, "sound_enabled": True}


def main():
    pygame.init()
    pygame.mixer.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(GAME_TITLE)

    settings = load_settings()
    lang = settings.get("language", "en")
    border_mode = settings.get("border_mode", True)
    sound_enabled = settings.get("sound_enabled", True)

    pygame.mixer.music.load(SOUNDTRACK_PATH)
    if sound_enabled:
        pygame.mixer.music.play(-1)

    while True:
        main_menu = MainMenu(width, height, language=lang, border_mode=border_mode)
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
                game = Game(width, height, language=main_menu.language, border_mode=main_menu.border_mode)
                result = game.run(screen)

                if result == "restart":
                    continue
                elif result == "menu":
                    break


if __name__ == "__main__":
    main()
