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


# src/ui/gui.py
# ==============
# Handles drawing the Cluedo board and game pieces to the Pygame window.
#
# This module provides optional visual board representation.
# The main gameplay works through screens.py, but this provides
# additional visual context for players.
# src/ui/gui.py
# ==============
# Handles drawing the Cluedo board and game pieces to the Pygame window.
#
# This module provides optional visual board representation.
# The main gameplay works through screens.py, but this provides
# additional visual context for players.

import pygame
from typing import Optional
from game.models import GameState
from game.deck import ROOMS


class Board:
    """Visual representation of the Cluedo board."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Room positions for visualization (simplified layout)
        self.room_positions = {
            "Kitchen": (100, 100),
            "Ballroom": (400, 100),
            "Conservatory": (700, 100),
            "Dining Room": (100, 300),
            "Billiard Room": (400, 300),
            "Library": (700, 300),
            "Lounge": (100, 500),
            "Hall": (400, 500),
            "Study": (700, 500),
        }

        self.room_colors = {
            "Kitchen": (255, 193, 7),  # Amber
            "Ballroom": (156, 39, 176),  # Purple
            "Conservatory": (76, 175, 80),  # Green
            "Dining Room": (244, 67, 54),  # Red
            "Billiard Room": (3, 169, 244),  # Light Blue
            "Library": (121, 85, 72),  # Brown
            "Lounge": (233, 30, 99),  # Pink
            "Hall": (255, 152, 0),  # Orange
            "Study": (63, 81, 181),  # Indigo
        }

    def draw(self, game_state: Optional[GameState] = None) -> None:
        """Draw the simplified board representation."""
        # This is a simplified visual board
        # The actual game logic happens in screens.py

        for room, position in self.room_positions.items():
            self._draw_room(room, position, game_state)

    def _draw_room(
            self,
            room_name: str,
            position: tuple,
            game_state: Optional[GameState]
    ) -> None:
        """Draw a single room on the board."""
        x, y = position
        room_width = 180
        room_height = 120

        # Room rectangle
        color = self.room_colors.get(room_name, (150, 150, 150))
        rect = pygame.Rect(x, y, room_width, room_height)

        # Highlight if current player is in this room
        border_width = 2
        if game_state:
            from game.engine import get_current_player
            current_player = get_current_player(game_state)
            if current_player.current_room == room_name:
                border_width = 5
                color = tuple(min(c + 30, 255) for c in color)

        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, border_width, border_radius=10)

        # Room name
        font = pygame.font.Font(None, 24)
        text_lines = room_name.split()

        y_offset = y + room_height // 2 - (len(text_lines) * 12)
        for line in text_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(x + room_width // 2, y_offset))

            # Text shadow for readability
            shadow = font.render(line, True, (0, 0, 0))
            shadow_rect = shadow.get_rect(center=(x + room_width // 2 + 1, y_offset + 1))
            self.screen.blit(shadow, shadow_rect)
            self.screen.blit(text_surface, text_rect)

            y_offset += 24

    def draw_player_tokens(self, game_state: GameState) -> None:
        """Draw player tokens in their current rooms."""
        from game.engine import get_current_player

        # Group players by room
        room_players = {}
        for player in game_state.players:
            if player.current_room:
                if player.current_room not in room_players:
                    room_players[player.current_room] = []
                room_players[player.current_room].append(player)

        # Draw tokens
        token_colors = [
            (231, 76, 60),  # Red
            (52, 152, 219),  # Blue
            (46, 204, 113),  # Green
            (241, 196, 15),  # Yellow
            (155, 89, 182),  # Purple
            (230, 126, 34),  # Orange
        ]

        for room, players in room_players.items():
            if room not in self.room_positions:
                continue

            room_x, room_y = self.room_positions[room]

            # Position tokens in a small grid within the room
            for i, player in enumerate(players):
                offset_x = (i % 2) * 30 + 20
                offset_y = (i // 2) * 30 + 80

                token_x = room_x + offset_x
                token_y = room_y + offset_y

                color = token_colors[game_state.players.index(player) % len(token_colors)]

                # Draw token (circle)
                pygame.draw.circle(self.screen, color, (token_x, token_y), 12)
                pygame.draw.circle(self.screen, (255, 255, 255), (token_x, token_y), 12, 2)

                # Draw player initial
                font = pygame.font.Font(None, 20)
                initial = player.name[0].upper()
                initial_surface = font.render(initial, True, (255, 255, 255))
                initial_rect = initial_surface.get_rect(center=(token_x, token_y))
                self.screen.blit(initial_surface, initial_rect)


class MiniBoard:
    """A compact board view for the game screen sidebar."""

    def __init__(self, x: int, y: int, size: int = 200):
        self.x = x
        self.y = y
        self.size = size

        # 3x3 grid of rooms
        self.grid_rooms = [
            ["Kitchen", "Ballroom", "Conservatory"],
            ["Dining Room", "Center", "Library"],
            ["Lounge", "Hall", "Study"]
        ]

    def draw(self, screen: pygame.Surface, game_state: Optional[GameState] = None) -> None:
        """Draw a mini board view."""
        cell_size = self.size // 3

        for row in range(3):
            for col in range(3):
                room = self.grid_rooms[row][col]

                if room == "Center":
                    continue

                x = self.x + col * cell_size
                y = self.y + row * cell_size

                rect = pygame.Rect(x, y, cell_size - 2, cell_size - 2)

                # Color based on whether current player is in this room
                color = (100, 100, 100)
                if game_state:
                    from game.engine import get_current_player
                    current_player = get_current_player(game_state)
                    if current_player.current_room == room:
                        color = (52, 152, 219)

                pygame.draw.rect(screen, color, rect, border_radius=3)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1, border_radius=3)