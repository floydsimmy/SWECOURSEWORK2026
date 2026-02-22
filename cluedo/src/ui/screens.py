# src/ui/screens.py
# ==================
# Manages which screen is currently being shown.
#
# Screens planned:
#   - MainMenuScreen  — the opening screen with a "Start Game" button
#   - GameScreen      — the main gameplay view (board, player info, etc.)
#   - EndScreen       — shown when the game is won or lost
#
# ScreenManager is the object that main.py talks to. It delegates
# events, updates, and drawing to whichever screen is currently active.


class ScreenManager:
    def __init__(self, screen):
        self.screen = screen

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background placeholder
