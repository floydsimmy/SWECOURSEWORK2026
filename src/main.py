# src/main.py
# =============
# Entry point for the Cluedo game.
# Initializes Pygame, creates the screen manager, and runs the main game loop.

import pygame
import sys

from ui.screens import ScreenManager


def main() -> None:
    """Initialize Pygame and run the main game loop."""
    pygame.init()

    # Window configuration
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Cluedo")

    clock = pygame.time.Clock()
    screen_manager = ScreenManager(screen)

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                screen_manager.handle_event(event)

        # Update game state
        screen_manager.update()

        # Draw everything
        screen_manager.draw()

        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()