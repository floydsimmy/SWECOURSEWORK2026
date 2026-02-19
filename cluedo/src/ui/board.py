# src/ui/board.py
# ================
# Responsible for drawing the Cluedo game board on screen.
# This includes:
#   - The board image (rooms, corridors, squares)
#   - Player tokens showing each character's current position
#   - Any visual highlights (e.g. valid moves, selected room)
#
# The Board class does NOT contain game logic — it only handles drawing.
# All rules and game state live in src/game/.


class Board:
    """Draws the Cluedo board and the pieces on top of it."""

    def __init__(self, screen):
        # 'screen' is the Pygame surface (the window) to draw onto
        self.screen = screen
        # TODO: load board image from assets/images/ here

    def draw(self):
        """Draw the board and all tokens to the screen."""
        pass  # TODO: blit the board image and player tokens onto self.screen
