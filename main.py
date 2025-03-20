import pygame
import sys
from src.ui.main_menu import MainMenu
from config.const import GAME_TITLE

def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(GAME_TITLE)
    main_menu = MainMenu(width, height, language="ru")

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
