"""Draw the Cluedo board with rooms, doors, and player tokens."""

from __future__ import annotations

from typing import Optional

import pygame

from game.deck import ROOMS
from game.models import GameState, Player


GRID_SIZE = 24


ROOM_LAYOUT: dict[str, tuple[int, int, int, int]] = {
    "Kitchen": (0, 0, 6, 6),
    "Ballroom": (7, 0, 10, 7),
    "Conservatory": (18, 0, 6, 6),
    "Dining Room": (0, 8, 7, 8),
    "Billiard Room": (17, 7, 7, 5),
    "Library": (17, 13, 7, 4),
    "Lounge": (0, 18, 7, 6),
    "Hall": (9, 18, 7, 6),
    "Study": (18, 18, 6, 6),
}

CENTER_AREA = (8, 9, 8, 6)

DOORS: dict[str, list[tuple[str, int]]] = {
    "Kitchen": [("bottom", 4)],
    "Ballroom": [("bottom", 2), ("bottom", 7), ("left", 5), ("right", 5)],
    "Conservatory": [("bottom", 1)],
    "Dining Room": [("right", 2), ("right", 6)],
    "Billiard Room": [("left", 1), ("bottom", 3)],
    "Library": [("left", 1), ("left", 3)],
    "Lounge": [("top", 5)],
    "Hall": [("top", 1), ("top", 5)],
    "Study": [("top", 1)],
}

ROOM_COLORS: dict[str, tuple[int, int, int]] = {
    "Kitchen": (197, 116, 56),
    "Ballroom": (111, 84, 155),
    "Conservatory": (74, 135, 92),
    "Dining Room": (145, 55, 60),
    "Billiard Room": (46, 119, 132),
    "Library": (121, 86, 64),
    "Lounge": (155, 72, 98),
    "Hall": (183, 132, 59),
    "Study": (74, 86, 132),
}

PLAYER_COLORS: list[tuple[int, int, int]] = [
    (206, 50, 55),
    (38, 111, 188),
    (41, 156, 96),
    (229, 181, 57),
    (136, 83, 171),
    (230, 119, 49),
]


class Board:
    """Top-down Cluedo board renderer."""

    def __init__(
        self,
        screen: pygame.Surface,
        x: int = 0,
        y: int = 0,
        size: Optional[int] = None,
    ):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font_title = pygame.font.Font(None, 26)
        self.font_room = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.font_tiny = pygame.font.Font(None, 16)
        self.player_colors = PLAYER_COLORS

        default_size = min(self.width - x, self.height - y)
        self.set_bounds(x, y, size or default_size)

    def set_bounds(self, x: int, y: int, size: int) -> None:
        """Set the square board area."""
        self.x = x
        self.y = y
        self.size = size
        self.tile_size = size / GRID_SIZE
        self.rect = pygame.Rect(x, y, size, size)

    def draw(
        self,
        game_state: Optional[GameState] = None,
        active_action: Optional[str] = None,
        selected_room: Optional[str] = None,
        legal_move_tiles: Optional[set[tuple[int, int]]] = None,
        legal_move_rooms: Optional[set[str]] = None,
    ) -> None:
        """Draw the board, rooms, corridors, doors, passages, and tokens."""
        self._draw_board_foundation()

        active_room = None
        if game_state is not None:
            from game.engine import get_current_player

            active_room = get_current_player(game_state).current_room

        move_options = set(legal_move_rooms or set()) if active_action == "move" else set()
        hover_room = self.room_at_point(pygame.mouse.get_pos())
        if active_action == "move":
            self._draw_legal_move_tiles(legal_move_tiles or set())

        for room in ROOMS:
            self._draw_room(
                room,
                is_active_room=room == active_room,
                is_move_option=room in move_options,
                is_selected=room == selected_room,
                is_hovered=room == hover_room and room in move_options,
            )

        self._draw_center_area()
        self._draw_doors()

        if game_state is not None:
            self._draw_secret_passages(game_state)
            self.draw_player_tokens(game_state)

        pygame.draw.rect(self.screen, (43, 35, 30), self.rect, 3, border_radius=6)

    def room_at_point(self, pos: tuple[int, int]) -> Optional[str]:
        """Return the room under the mouse, if any."""
        for room, layout in ROOM_LAYOUT.items():
            if self._grid_rect(layout).collidepoint(pos):
                return room
        return None

    def tile_at_point(self, pos: tuple[int, int]) -> Optional[tuple[int, int]]:
        """Return the board tile under the mouse, if the point is on the board."""
        if not self.rect.collidepoint(pos):
            return None
        col = int((pos[0] - self.x) // self.tile_size)
        row = int((pos[1] - self.y) // self.tile_size)
        tile = (col, row)
        return tile if self._tile_in_bounds(tile) else None

    def draw_player_tokens(self, game_state: GameState) -> None:
        """Draw player tokens using current room or optional tile fields."""
        from game.engine import get_current_player

        current_player = get_current_player(game_state)
        room_players = {}
        tile_players = {}

        for index, player in enumerate(game_state.players):
            if player.current_room in ROOM_LAYOUT:
                if player.current_room not in room_players:
                    room_players[player.current_room] = []
                room_players[player.current_room].append((index, player))
                continue

            tile = self._read_player_tile(player)
            if tile is None:
                tile = self._start_tile(index)
            if tile not in tile_players:
                tile_players[tile] = []
            tile_players[tile].append((index, player))

        for room, players in room_players.items():
            for slot_index, (player_index, player) in enumerate(players):
                center = self._room_token_center(room, slot_index, len(players))
                self._draw_token(
                    center,
                    player,
                    player_index,
                    is_active=player is current_player,
                )

        for tile, players in tile_players.items():
            for slot_index, (player_index, player) in enumerate(players):
                center = self._tile_token_center(tile, slot_index, len(players))
                self._draw_token(
                    center,
                    player,
                    player_index,
                    is_active=player is current_player,
                )

    def draw_player_legend(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        game_state: GameState,
    ) -> None:
        """Draw a compact player/token legend."""
        from game.engine import get_current_player

        current_player = get_current_player(game_state)

        pygame.draw.rect(screen, (31, 43, 56), rect, border_radius=8)
        pygame.draw.rect(screen, (93, 116, 137), rect, 1, border_radius=8)

        title = self.font_title.render("Players", True, (236, 240, 241))
        screen.blit(title, (rect.x + 14, rect.y + 10))

        row_y = rect.y + 42
        row_height = 26
        for index, player in enumerate(game_state.players):
            row_rect = pygame.Rect(rect.x + 8, row_y - 3, rect.width - 16, row_height)
            if player is current_player:
                pygame.draw.rect(screen, (55, 79, 98), row_rect, border_radius=6)

            color = self.player_colors[index % len(self.player_colors)]
            token_center = (rect.x + 24, row_y + 9)
            pygame.draw.circle(screen, color, token_center, 9)
            pygame.draw.circle(screen, (255, 255, 255), token_center, 9, 1)

            initial = self._initials(player.name)
            initials_text = self.font_tiny.render(
                initial,
                True,
                self._contrast_text_color(color),
            )
            initials_rect = initials_text.get_rect(center=token_center)
            screen.blit(initials_text, initials_rect)

            location = player.current_room or self._player_tile_label(player)
            if player.is_eliminated:
                location = "Eliminated"
            label = self._truncate(f"{player.name} - {location}", self.font_small, rect.width - 52)
            color_text = (236, 240, 241) if not player.is_eliminated else (154, 164, 174)
            name_surface = self.font_small.render(label, True, color_text)
            screen.blit(name_surface, (rect.x + 42, row_y))

            row_y += row_height

    def _draw_board_foundation(self) -> None:
        pygame.draw.rect(self.screen, (205, 188, 156), self.rect, border_radius=6)

        occupied = self._occupied_cells()
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if (col, row) in occupied:
                    continue
                tile_rect = self._tile_rect(col, row, pad=1)
                color = (232, 221, 196) if (row + col) % 2 == 0 else (221, 208, 181)
                pygame.draw.rect(self.screen, color, tile_rect)
                pygame.draw.rect(self.screen, (177, 159, 128), tile_rect, 1)

    def _draw_room(
        self,
        room: str,
        *,
        is_active_room: bool,
        is_move_option: bool,
        is_selected: bool,
        is_hovered: bool,
    ) -> None:
        rect = self._grid_rect(ROOM_LAYOUT[room], inset=2)
        base = ROOM_COLORS.get(room, (112, 112, 112))
        color = self._brighten(base, 30 if is_active_room or is_hovered else 0)

        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, (58, 45, 38), rect, 3, border_radius=8)

        if is_move_option:
            pygame.draw.rect(self.screen, (238, 213, 116), rect.inflate(-8, -8), 2, border_radius=6)
        if is_selected:
            pygame.draw.rect(self.screen, (255, 248, 206), rect.inflate(-14, -14), 3, border_radius=6)
        if is_active_room:
            pygame.draw.rect(self.screen, (255, 255, 255), rect.inflate(-18, -18), 3, border_radius=6)

        self._draw_room_label(room, rect)

    def _draw_room_label(self, room: str, rect: pygame.Rect) -> None:
        words = room.split()
        lines = words if len(words) > 1 else [room]
        line_height = 21
        start_y = rect.centery - (len(lines) * line_height) // 2

        for i, line in enumerate(lines):
            shadow = self.font_room.render(line.upper(), True, (31, 25, 22))
            text = self.font_room.render(line.upper(), True, (248, 244, 232))
            center = (rect.centerx, start_y + i * line_height)
            shadow_rect = shadow.get_rect(center=(center[0] + 1, center[1] + 1))
            text_rect = text.get_rect(center=center)
            self.screen.blit(shadow, shadow_rect)
            self.screen.blit(text, text_rect)

    def _draw_center_area(self) -> None:
        rect = self._grid_rect(CENTER_AREA, inset=3)
        pygame.draw.rect(self.screen, (94, 77, 63), rect, border_radius=8)
        pygame.draw.rect(self.screen, (45, 36, 30), rect, 2, border_radius=8)

        text = self.font_title.render("CASE FILE", True, (248, 244, 232))
        text_rect = text.get_rect(center=(rect.centerx, rect.centery - 8))
        self.screen.blit(text, text_rect)

        sub = self.font_small.render("Evidence", True, (221, 209, 185))
        sub_rect = sub.get_rect(center=(rect.centerx, rect.centery + 16))
        self.screen.blit(sub, sub_rect)

    def _draw_legal_move_tiles(self, tiles: set[tuple[int, int]]) -> None:
        for tile in tiles:
            if not self._tile_in_bounds(tile):
                continue
            rect = self._tile_rect(tile[0], tile[1], pad=4)
            pygame.draw.rect(self.screen, (80, 167, 112), rect, border_radius=4)
            pygame.draw.rect(self.screen, (31, 92, 54), rect, 2, border_radius=4)

    def _draw_doors(self) -> None:
        for room, doors in DOORS.items():
            col, row, width, height = ROOM_LAYOUT[room]
            for side, offset in doors:
                door_rect = self._door_rect(col, row, width, height, side, offset)
                pygame.draw.rect(self.screen, (237, 188, 82), door_rect, border_radius=3)
                pygame.draw.rect(self.screen, (88, 61, 28), door_rect, 1, border_radius=3)

    def _draw_secret_passages(self, game_state: GameState) -> None:
        for first, second in self._extract_secret_passages(game_state):
            if first not in ROOM_LAYOUT or second not in ROOM_LAYOUT:
                continue
            start = self._grid_rect(ROOM_LAYOUT[first]).center
            end = self._grid_rect(ROOM_LAYOUT[second]).center
            self._draw_dashed_line(start, end, (246, 222, 141), width=3)

    def _room_token_center(
        self,
        room: str,
        index: int,
        total: int,
    ) -> tuple[int, int]:
        rect = self._grid_rect(ROOM_LAYOUT[room], inset=14)
        columns = min(3, max(1, total))
        rows = (total + columns - 1) // columns
        spacing_x = min(34, max(24, rect.width // (columns + 1)))
        spacing_y = min(30, max(22, rect.height // (rows + 2)))

        col = index % columns
        row = index // columns
        start_x = rect.centerx - ((columns - 1) * spacing_x) // 2
        start_y = rect.centery + 18 - ((rows - 1) * spacing_y) // 2
        return (start_x + col * spacing_x, start_y + row * spacing_y)

    def _tile_token_center(
        self,
        tile: tuple[int, int],
        index: int,
        total: int,
    ) -> tuple[int, int]:
        rect = self._tile_rect(tile[0], tile[1], pad=2)
        offsets = {
            1: [(0, 0)],
            2: [(-6, -5), (6, 5)],
            3: [(-7, -6), (7, -6), (0, 7)],
            4: [(-7, -7), (7, -7), (-7, 7), (7, 7)],
        }
        offset = offsets.get(min(total, 4), [(0, 0)])[min(index, 3)]
        return (rect.centerx + offset[0], rect.centery + offset[1])

    def _draw_token(
        self,
        center: tuple[int, int],
        player: Player,
        player_index: int,
        *,
        is_active: bool,
    ) -> None:
        color = self.player_colors[player_index % len(self.player_colors)]
        if player.is_eliminated:
            color = self._desaturate(color)

        radius = max(10, int(self.tile_size * 0.38))
        if is_active:
            pygame.draw.circle(self.screen, (255, 245, 181), center, radius + 6)
            pygame.draw.circle(self.screen, (92, 66, 28), center, radius + 6, 2)

        pygame.draw.circle(self.screen, color, center, radius)
        pygame.draw.circle(self.screen, (255, 255, 255), center, radius, 2)

        initials = self.font_small.render(
            self._initials(player.name),
            True,
            self._contrast_text_color(color),
        )
        initials_rect = initials.get_rect(center=center)
        self.screen.blit(initials, initials_rect)

        if player.is_eliminated:
            slash_start = (center[0] - radius + 2, center[1] + radius - 2)
            slash_end = (center[0] + radius - 2, center[1] - radius + 2)
            pygame.draw.line(self.screen, (30, 30, 30), slash_start, slash_end, 3)

    def _grid_rect(
        self,
        layout: tuple[int, int, int, int],
        *,
        inset: int = 0,
    ) -> pygame.Rect:
        col, row, width, height = layout
        x = round(self.x + col * self.tile_size) + inset
        y = round(self.y + row * self.tile_size) + inset
        w = round(width * self.tile_size) - inset * 2
        h = round(height * self.tile_size) - inset * 2
        return pygame.Rect(x, y, w, h)

    def _tile_rect(self, col: int, row: int, *, pad: int = 0) -> pygame.Rect:
        x = round(self.x + col * self.tile_size) + pad
        y = round(self.y + row * self.tile_size) + pad
        size = max(1, round(self.tile_size) - pad * 2)
        return pygame.Rect(x, y, size, size)

    def _door_rect(
        self,
        col: int,
        row: int,
        width: int,
        height: int,
        side: str,
        offset: int,
    ) -> pygame.Rect:
        thickness = max(5, int(self.tile_size * 0.24))
        length = max(16, int(self.tile_size * 0.9))

        if side == "top":
            x = round(self.x + (col + offset) * self.tile_size)
            y = round(self.y + row * self.tile_size - thickness // 2)
            return pygame.Rect(x, y, length, thickness)
        if side == "bottom":
            x = round(self.x + (col + offset) * self.tile_size)
            y = round(self.y + (row + height) * self.tile_size - thickness // 2)
            return pygame.Rect(x, y, length, thickness)
        if side == "left":
            x = round(self.x + col * self.tile_size - thickness // 2)
            y = round(self.y + (row + offset) * self.tile_size)
            return pygame.Rect(x, y, thickness, length)

        x = round(self.x + (col + width) * self.tile_size - thickness // 2)
        y = round(self.y + (row + offset) * self.tile_size)
        return pygame.Rect(x, y, thickness, length)

    def _occupied_cells(self) -> set[tuple[int, int]]:
        occupied: set[tuple[int, int]] = set()
        for layout in list(ROOM_LAYOUT.values()) + [CENTER_AREA]:
            col, row, width, height = layout
            for occupied_col in range(col, col + width):
                for occupied_row in range(row, row + height):
                    occupied.add((occupied_col, occupied_row))
        return occupied

    def _start_tile(self, index: int) -> tuple[int, int]:
        start_tiles = [(7, 23), (7, 17), (23, 17), (17, 0), (23, 6), (6, 0)]
        return start_tiles[index % len(start_tiles)]

    def _read_player_tile(self, player: Player) -> Optional[tuple[int, int]]:
        """Read the player's tile coordinates if they are set and in bounds."""
        value = player.board_position
        if self._is_tile_pair(value):
            tile = (int(value[0]), int(value[1]))
            if self._tile_in_bounds(tile):
                return tile
        return None

    def _player_tile_label(self, player: Player) -> str:
        tile = self._read_player_tile(player)
        if tile is None:
            return "Start"
        return f"Hallway {tile[0]},{tile[1]}"

    def _extract_secret_passages(self, game_state: GameState) -> list[tuple[str, str]]:
        """Secret passages are out of scope, so there are never any to draw."""
        return []

    def _draw_dashed_line(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        color: tuple[int, int, int],
        *,
        width: int = 2,
        dash_length: int = 14,
    ) -> None:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = max(1, int((dx * dx + dy * dy) ** 0.5))
        steps = max(1, distance // dash_length)

        for step in range(0, steps, 2):
            segment_start = (
                round(start[0] + dx * step / steps),
                round(start[1] + dy * step / steps),
            )
            segment_end = (
                round(start[0] + dx * min(step + 1, steps) / steps),
                round(start[1] + dy * min(step + 1, steps) / steps),
            )
            pygame.draw.line(self.screen, color, segment_start, segment_end, width)

    def _initials(self, name: str) -> str:
        parts = [part for part in name.split() if part]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    def _truncate(self, text: str, font: pygame.font.Font, max_width: int) -> str:
        if font.size(text)[0] <= max_width:
            return text
        ellipsis = "..."
        trimmed = text
        while trimmed and font.size(trimmed + ellipsis)[0] > max_width:
            trimmed = trimmed[:-1]
        return trimmed + ellipsis if trimmed else ellipsis

    def _brighten(self, color: tuple[int, int, int], amount: int) -> tuple[int, int, int]:
        return tuple(min(255, channel + amount) for channel in color)

    def _desaturate(self, color: tuple[int, int, int]) -> tuple[int, int, int]:
        grey = sum(color) // 3
        return tuple((channel + grey) // 2 for channel in color)

    def _contrast_text_color(self, color: tuple[int, int, int]) -> tuple[int, int, int]:
        # If the colour is bright, use dark text; otherwise use white.
        brightness = sum(color) // 3
        return (22, 24, 28) if brightness > 150 else (255, 255, 255)

    def _is_tile_pair(self, value: object) -> bool:
        return (
            isinstance(value, (tuple, list))
            and len(value) == 2
            and isinstance(value[0], int)
            and isinstance(value[1], int)
        )

    def _tile_in_bounds(self, tile: tuple[int, int]) -> bool:
        return 0 <= tile[0] < GRID_SIZE and 0 <= tile[1] < GRID_SIZE

    def _is_room_pair(self, value: object) -> bool:
        return (
            isinstance(value, (tuple, list))
            and len(value) == 2
            and isinstance(value[0], str)
            and isinstance(value[1], str)
        )
