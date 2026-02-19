# src/ui/components.py
# =====================
# Reusable UI building blocks that can be used across multiple screens.
# Instead of rewriting the same button code everywhere, we define it once here
# and import it wherever needed.
#
# Currently contains:
#   - Button: a clickable rectangle with a text label


class Button:
    """A clickable button with a position, size, and text label."""

    def __init__(self, x, y, width, height, label):
        # Store the button's position and size as a tuple (x, y, width, height)
        self.rect = (x, y, width, height)
        self.label = label   # The text shown on the button (e.g. "Start Game")

    def draw(self, screen):
        """Draw the button rectangle and its label onto the given screen surface."""
        pass  # TODO: use pygame.draw.rect() for the box and a font surface for the text

    def is_clicked(self, event):
        """Return True if the given Pygame event is a mouse click inside this button."""
        pass  # TODO: check event.type == pygame.MOUSEBUTTONDOWN and point-in-rect test
