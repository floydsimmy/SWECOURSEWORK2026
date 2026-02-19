# src/main.py
# ============
# This is the entry point for the game — the file you run to start it.
# It sets up the Pygame window, creates the screen manager, and runs
# the main game loop that keeps the window open and responsive.

import pygame
from ui.screens import ScreenManager  # Manages which screen is currently shown


def main():
    pygame.init()  # Start up all Pygame modules (graphics, sound, input, etc.)

    # Create the game window: 1024 pixels wide, 768 pixels tall
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Cluedo")  # Title shown in the window's title bar

    # Clock limits how many times per second the loop runs (60 FPS)
    clock = pygame.time.Clock()

    # ScreenManager decides what to draw (menu, game board, end screen, etc.)
    manager = ScreenManager(screen)

    running = True  # This flag controls the main loop — set it to False to quit

    # --- Main game loop ---
    # This loop runs 60 times per second and does three things every frame:
    #   1. Handle input events (mouse clicks, keyboard presses, closing the window)
    #   2. Update game state (move pieces, check rules, etc.)
    #   3. Draw everything to the screen
    while running:
        # Check for events (user input, window close button, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # User clicked the X to close the window
                running = False
            manager.handle_event(event)   # Pass the event to the current screen

        manager.update()             # Update any game logic for this frame
        manager.draw()               # Draw the current screen contents
        pygame.display.flip()        # Push the drawn frame to the actual display
        clock.tick(60)               # Wait so we don't exceed 60 frames per second

    pygame.quit()  # Clean up and shut down Pygame before the program exits


# Only run main() if this file is executed directly (not imported by another file)
if __name__ == "__main__":
    main()
