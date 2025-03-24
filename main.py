import pygame
import sys
import json
from src.game.game import Game
from src.ui.main_menu import MainMenu
from config.const import GAME_TITLE, SETTINGS_FILENAME, SOUNDTRACK_PATH
from src.ui.settings_menu import SettingsMenu


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
    language = settings.get("language", "en")
    border_mode = settings.get("border_mode", True)
    sound_enabled = settings.get("sound_enabled", True)
    username = settings.get("username", "Player")

    pygame.mixer.music.load(SOUNDTRACK_PATH)
    pygame.mixer.music.play(-1)
    if not sound_enabled:
        pygame.mixer.music.pause()

    while True:
        main_menu = MainMenu(
            width, height, language=language, border_mode=border_mode)
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
                game = Game(width, height, language=language,
                            border_mode=border_mode)
                game.snake.username = username
                result = game.run(screen)

                if result == "restart":
                    continue
                elif result == "menu":
                    break

            if hasattr(main_menu, "open_settings_flag") and main_menu.open_settings_flag:
                settings_menu = SettingsMenu(
                    width, height, language=language, sound_enabled=sound_enabled, border_mode=border_mode)
                settings_menu_running = True

                while settings_menu_running:
                    settings_events = pygame.event.get()
                    for event in settings_events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                    settings_menu.handle_events(settings_events)
                    settings_menu.render(screen)
                    pygame.display.flip()

                    if not getattr(settings_menu, "running", True):
                        updated_settings = settings_menu.get_settings()
                        language = updated_settings["language"]
                        sound_enabled = updated_settings["sound_enabled"]
                        border_mode = updated_settings["border_mode"]
                        settings_menu_running = False
                        main_menu.open_settings_flag = False
                        running = False


if __name__ == "__main__":
    main()
