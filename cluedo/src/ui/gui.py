# src/ui/gui.py
# ==============
# Handles drawing the Cluedo board and game pieces to the Pygame window.
#
# Responsibilities:
#   - Rendering the board grid and rooms
#   - Drawing player tokens at their current positions
#   - Drawing weapon tokens
#
# This file contains only drawing logic — no game rules or state
# changes happen here. It reads from the game models and draws them.


class Board:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        pass  # Board drawing logic goes here
