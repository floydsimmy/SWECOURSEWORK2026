# src/ui/components.py
# =====================
# Reusable Pygame UI elements used across multiple screens.
#
# Components planned:
#   - Button      — a clickable rectangle with a text label
#   - CardDisplay — shows a card image or name on screen
#   - PlayerPanel — shows a player's name, character, and cards
#
# Each component is responsible for drawing itself and reporting
# whether it has been interacted with (e.g. clicked).


class Button:
    def __init__(self, x, y, width, height, label):
        self.rect = (x, y, width, height)
        self.label = label

    def draw(self, screen):
        pass  # Button drawing logic goes here

    def is_clicked(self, event):
        pass  # Click detection logic goes here
