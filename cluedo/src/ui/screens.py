# src/ui/screens.py
# ==================
# Manages which "screen" the player is currently looking at.
# A screen is a full page of the game — for example:
#   - The main menu (start game, quit)
#   - The game board (where you play)
#   - The end screen (who won, play again?)
#
# ScreenManager is the controller: it holds the active screen and forwards
# input events, update calls, and draw calls to it each frame.


class ScreenManager:
    """Controls which screen is currently active and displayed."""

    def __init__(self, screen):
        # 'screen' is the Pygame surface (the window) passed in from main.py
        self.screen = screen
        # TODO: initialise the starting screen here (e.g. a MainMenuScreen)

    def handle_event(self, event):
        """Called once per Pygame event (key press, mouse click, etc.).
        Forward the event to whichever screen is currently active."""
        pass  # TODO: call self.current_screen.handle_event(event)

    def update(self):
        """Called once per frame to update game logic on the current screen."""
        pass  # TODO: call self.current_screen.update()

    def draw(self):
        """Called once per frame to draw the current screen to the window."""
        self.screen.fill((0, 0, 0))  # Fill the window with black (placeholder background)
        # TODO: call self.current_screen.draw()
