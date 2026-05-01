# src/ui/screens.py
# ==================
# Manages which screen is currently being shown.
#
# Screens in this file:
#   - MainMenuScreen  — the opening screen with a "Start Game" button
#   - SetupScreen     — player name entry and game configuration
#   - GameScreen      — the main gameplay view (board, player info, etc.)
#   - EndScreen       — shown when the game is won or lost
#
# ScreenManager is the object that main.py talks to. It delegates
# events, updates, and drawing to whichever screen is currently active.

# src/ui/screens.py
# ==================
# Manages all game screens and transitions between them.

import pygame
from typing import Optional, List
from game.ai import (
    AITurnResult,
    is_ai_player,
    take_ai_turn,
)
from game.engine import (
    new_game,
    get_current_player,
    legal_moves_for_roll,
    move_by_dice,
    roll_die,
    make_suggestion,
    make_accusation,
    next_turn,
    get_game_status,
    check_for_winner
)
from game.models import AI_PLAYER, Card, GameState, HUMAN_PLAYER, Player
from game.deck import SUSPECTS, WEAPONS, ROOMS
from ui.components import Button, TextInput, CardDisplay, PopupSelect, MessageBox
from ui.gui import Board


class Screen:
    """Base class for all screens."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle events. Return screen name to transition to, or None."""
        return None

    def update(self) -> Optional[str]:
        """Update screen state. Return screen name to transition to, or None."""
        return None

    def draw(self) -> None:
        """Draw the screen."""
        pass


class MainMenuScreen(Screen):
    """The opening screen with game title and start button."""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

        # Title
        self.title_font = pygame.font.Font(None, 120)
        self.subtitle_font = pygame.font.Font(None, 36)

        # Buttons
        button_width = 300
        button_height = 60
        button_x = (self.width - button_width) // 2

        self.start_button = Button(
            button_x,
            400,
            button_width,
            button_height,
            "Start New Game",
            color=(231, 76, 60),
            hover_color=(192, 57, 43)
        )

        self.quit_button = Button(
            button_x,
            500,
            button_width,
            button_height,
            "Quit",
            color=(149, 165, 166),
            hover_color=(127, 140, 141)
        )

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if self.start_button.handle_event(event):
            return "setup"
        if self.quit_button.handle_event(event):
            pygame.quit()
            exit()
        return None

    def draw(self) -> None:
        # Background gradient effect
        for y in range(self.height):
            alpha = y / self.height
            color = (
                int(44 + (52 - 44) * alpha),
                int(62 + (73 - 62) * alpha),
                int(80 + (94 - 80) * alpha)
            )
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))

        # Title
        title_text = self.title_font.render("CLUEDO", True, (236, 240, 241))
        title_rect = title_text.get_rect(center=(self.width // 2, 200))

        # Title shadow
        shadow_text = self.title_font.render("CLUEDO", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(self.width // 2 + 3, 203))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(title_text, title_rect)

        # Subtitle
        subtitle = self.subtitle_font.render("The Classic Mystery Board Game", True, (189, 195, 199))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 290))
        self.screen.blit(subtitle, subtitle_rect)

        # Buttons
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)


class SetupScreen(Screen):
    """Screen for entering player names."""

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

        self.title_font = pygame.font.Font(None, 64)
        self.label_font = pygame.font.Font(None, 32)

        # Player input fields
        self.max_players = 6
        self.min_players = 3
        self.input_fields: List[TextInput] = []
        self.player_types: List[str] = [HUMAN_PLAYER for _ in range(self.max_players)]
        self.type_buttons: List[Button] = []

        input_width = 400
        input_height = 50
        start_y = 180
        spacing = 70
        input_x = (self.width - input_width) // 2

        for i in range(self.max_players):
            text_input = TextInput(
                input_x,
                start_y + i * spacing,
                input_width,
                input_height,
                placeholder=f"Player {i + 1} name" + (" (optional)" if i >= 3 else "")
            )
            self.input_fields.append(text_input)
            self.type_buttons.append(
                Button(
                    input_x + input_width + 20,
                    start_y + i * spacing,
                    120,
                    input_height,
                    "Human",
                    font_size=24,
                    color=(52, 152, 219),
                    hover_color=(41, 128, 185),
                )
            )

        # Buttons
        button_y = start_y + self.max_players * spacing + 20
        self.start_game_button = Button(
            self.width // 2 - 250,
            button_y,
            200,
            50,
            "Start Game",
            color=(46, 204, 113),
            hover_color=(39, 174, 96)
        )

        self.back_button = Button(
            self.width // 2 + 50,
            button_y,
            200,
            50,
            "Back",
            color=(149, 165, 166),
            hover_color=(127, 140, 141)
        )

        self.error_message: Optional[str] = None

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        # Handle input fields
        for field in self.input_fields:
            field.handle_event(event)

        for index, button in enumerate(self.type_buttons):
            if button.handle_event(event):
                self._toggle_player_type(index)
                return None

        # Handle buttons
        if self.start_game_button.handle_event(event):
            return self._try_start_game()

        if self.back_button.handle_event(event):
            return "menu"

        return None

    def _toggle_player_type(self, index: int) -> None:
        """Toggle one player setup slot between human and AI."""
        button = self.type_buttons[index]
        if self.player_types[index] == HUMAN_PLAYER:
            self.player_types[index] = AI_PLAYER
            button.text = "AI"
            button.color = (111, 84, 155)
            button.hover_color = (92, 66, 137)
        else:
            self.player_types[index] = HUMAN_PLAYER
            button.text = "Human"
            button.color = (52, 152, 219)
            button.hover_color = (41, 128, 185)

    def _try_start_game(self) -> Optional[str]:
        """Validate inputs and start game if valid."""
        player_entries = [
            (field.get_text(), self.player_types[index])
            for index, field in enumerate(self.input_fields)
            if field.get_text()
        ]
        player_names = [entry[0] for entry in player_entries]
        player_types = [entry[1] for entry in player_entries]

        if len(player_names) < self.min_players:
            self.error_message = f"Need at least {self.min_players} players!"
            return None

        if len(player_names) != len(set(player_names)):
            self.error_message = "Player names must be unique!"
            return None

        # Create game state and store it
        try:
            game_state = new_game(player_names, player_types=player_types)
            # Store in a global or pass through screen manager
            ScreenManager.game_state = game_state
            return "game"
        except ValueError as e:
            self.error_message = str(e)
            return None

    def update(self) -> Optional[str]:
        for field in self.input_fields:
            field.update()
        return None

    def draw(self) -> None:
        self.screen.fill((236, 240, 241))

        # Title
        title = self.title_font.render("Game Setup", True, (44, 62, 80))
        title_rect = title.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title, title_rect)

        # Instructions
        instructions = self.label_font.render(
            f"Enter {self.min_players}-{self.max_players} player names:",
            True,
            (52, 73, 94)
        )
        instructions_rect = instructions.get_rect(center=(self.width // 2, 130))
        self.screen.blit(instructions, instructions_rect)

        # Input fields
        for field in self.input_fields:
            field.draw(self.screen)
        for button in self.type_buttons:
            button.draw(self.screen)

        # Buttons
        self.start_game_button.draw(self.screen)
        self.back_button.draw(self.screen)

        # Error message
        if self.error_message:
            error_font = pygame.font.Font(None, 28)
            error_text = error_font.render(self.error_message, True, (231, 76, 60))
            error_rect = error_text.get_rect(center=(self.width // 2, self.height - 60))
            self.screen.blit(error_text, error_rect)


class GameScreen(Screen):
    """Main gameplay screen."""

    def __init__(self, screen: pygame.Surface, game_state: GameState):
        super().__init__(screen)
        self.game_state = game_state

        self.title_font = pygame.font.Font(None, 48)
        self.normal_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)

        # UI Layout
        self.sidebar_width = 280
        self.outer_margin = 20
        self.panel_width = 250
        board_space = self.width - self.sidebar_width - self.panel_width - self.outer_margin * 3
        self.board_size = min(self.height - 70, board_space)
        self.board_x = self.sidebar_width + self.outer_margin
        self.board_y = 28
        self.panel_x = self.board_x + self.board_size + self.outer_margin
        self.main_area_x = self.panel_x
        self.board = Board(self.screen, self.board_x, self.board_y, self.board_size)

        # Action buttons
        button_width = self.sidebar_width - 48
        button_height = 44
        button_x = 24
        button_spacing = 54
        button_count = 5
        button_y = self.height - 16 - (
            button_height * button_count
            + (button_spacing - button_height) * (button_count - 1)
        )

        self.move_button = Button(
            button_x, button_y,
            button_width, button_height,
            "Roll Dice",
            font_size=24,
            color=(155, 89, 182),
            hover_color=(142, 68, 173)
        )

        self.suggest_button = Button(
            button_x, button_y + button_spacing,
            button_width, button_height,
            "Make Suggestion",
            font_size=24,
            color=(52, 152, 219),
            hover_color=(41, 128, 185)
        )

        self.accuse_button = Button(
            button_x, button_y + button_spacing * 2,
            button_width, button_height,
            "Make Accusation",
            font_size=24,
            color=(231, 76, 60),
            hover_color=(192, 57, 43)
        )

        self.end_turn_button = Button(
            button_x, button_y + button_spacing * 3,
            button_width, button_height,
            "End Turn",
            font_size=24,
            color=(46, 204, 113),
            hover_color=(39, 174, 96)
        )

        self.quit_game_button = Button(
            button_x, button_y + button_spacing * 4,
            button_width, button_height,
            "Quit to Menu",
            font_size=24,
            color=(127, 140, 141),
            hover_color=(95, 106, 106)
        )

        # Dropdown menus for actions
        dropdown_x = self.panel_x + 14
        dropdown_width = self.panel_width - 28
        dropdown_height = 45

        self.room_dropdown = PopupSelect(
            dropdown_x, 150,
            dropdown_width, dropdown_height,
            ROOMS,
            "Select Room"
        )

        self.suspect_dropdown = PopupSelect(
            dropdown_x, 220,
            dropdown_width, dropdown_height,
            SUSPECTS,
            "Select Suspect"
        )

        self.weapon_dropdown = PopupSelect(
            dropdown_x, 290,
            dropdown_width, dropdown_height,
            WEAPONS,
            "Select Weapon"
        )

        self.room_accusation_dropdown = PopupSelect(
            dropdown_x, 360,
            dropdown_width, dropdown_height,
            ROOMS,
            "Select Room"
        )

        # Confirm buttons for actions
        confirm_x = dropdown_x
        self.confirm_move_button = Button(
            confirm_x, 220, dropdown_width, 45,
            "Confirm", font_size=24
        )

        self.confirm_suggest_button = Button(
            confirm_x, 350, dropdown_width, 45,
            "Confirm", font_size=24
        )

        self.confirm_accuse_button = Button(
            confirm_x, 425, dropdown_width, 45,
            "Confirm", font_size=24
        )

        # UI State
        self.current_action: Optional[str] = None  # "move", "suggest", "accuse"
        self.message_box: Optional[MessageBox] = None
        self.messages: List[str] = []
        self.current_move_roll: Optional[int] = None
        self.legal_move_tiles: set[tuple[int, int]] = set()
        self.legal_move_rooms: set[str] = set()
        self.cards_scroll_offset = 0
        self.cards_scroll_rect = pygame.Rect(0, 0, 0, 0)
        self.card_row_height = 22

        self._update_button_states()

    def _update_button_states(self) -> None:
        """Update which buttons are enabled based on game state."""
        current_player = get_current_player(self.game_state)

        self.move_button.enabled = not current_player.is_eliminated
        self.accuse_button.enabled = not current_player.is_eliminated
        self.end_turn_button.enabled = True
        self.quit_game_button.enabled = True

        if is_ai_player(current_player):
            self.move_button.enabled = False
            self.suggest_button.enabled = False
            self.accuse_button.enabled = False
            self.end_turn_button.enabled = False
            return

        if self.game_state.has_rolled_this_turn:
            self.move_button.enabled = False

        # Suggest only available if in a room
        self.suggest_button.enabled = (
            current_player.current_room is not None and not current_player.is_eliminated
        )

        if self.current_action == "move":
            self.move_button.enabled = False
            self.suggest_button.enabled = False
            self.accuse_button.enabled = False

        # All buttons disabled if eliminated
        if current_player.is_eliminated:
            self.move_button.enabled = False
            self.suggest_button.enabled = False
            self.accuse_button.enabled = False

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        # Check for game over
        winner = check_for_winner(self.game_state)
        if self.game_state.game_over:
            ScreenManager.game_state = self.game_state
            return "end"

        if self.quit_game_button.handle_event(event):
            PopupSelect.close_active()
            self.current_action = None
            self._clear_move_choices()
            ScreenManager.game_state = None
            return "menu"

        if self.current_action == "move" and self._handle_move_click(event):
            return None

        # Handle selectors before buttons so an open popup consumes clicks.
        if self._handle_select_event(event):
            return None

        if self._handle_sidebar_scroll(event):
            return None

        # Handle action buttons
        if self.move_button.handle_event(event):
            self._start_dice_move()
            return None

        if self.suggest_button.handle_event(event):
            self.current_action = "suggest"
            self._clear_move_choices()
            self.suspect_dropdown.reset()
            self.weapon_dropdown.reset()
            return None

        if self.accuse_button.handle_event(event):
            self.current_action = "accuse"
            self._clear_move_choices()
            self.suspect_dropdown.reset()
            self.weapon_dropdown.reset()
            self.room_accusation_dropdown.reset()
            return None

        if self.end_turn_button.handle_event(event):
            next_turn(self.game_state)
            self.current_action = None
            self._clear_move_choices()
            self._update_button_states()
            self._add_message(f"Turn passed to {get_current_player(self.game_state).name}")
            return None

        if self.current_action == "suggest" and self.confirm_suggest_button.handle_event(event):
            self._execute_suggestion()
            return None

        if self.current_action == "accuse" and self.confirm_accuse_button.handle_event(event):
            self._execute_accusation()
            return None

        return None

    def _start_dice_move(self) -> None:
        """Roll the die and show board destinations for the current player."""
        try:
            PopupSelect.close_active()
            player = get_current_player(self.game_state)
            self.current_move_roll = roll_die()
            legal_moves = legal_moves_for_roll(
                self.game_state,
                player,
                self.current_move_roll,
            )
            self.legal_move_tiles = set(legal_moves["tiles"])
            self.legal_move_rooms = set(legal_moves["rooms"])
            self.current_action = "move"
            self._add_message(f"{player.name} rolled {self.current_move_roll}")

            if not self.legal_move_tiles and not self.legal_move_rooms:
                self._show_message("No legal moves for this roll", (231, 76, 60))
                self.current_action = None
                self._clear_move_choices()
            self._update_button_states()
        except ValueError as e:
            self._show_message(str(e), (231, 76, 60))

    def _handle_move_click(self, event: pygame.event.Event) -> bool:
        """Move to a highlighted tile or reachable room when the board is clicked."""
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
        if not self.board.rect.collidepoint(event.pos):
            return False

        room = self.board.room_at_point(event.pos)
        if room in self.legal_move_rooms:
            self._finish_dice_move(room)
            return True

        tile = self.board.tile_at_point(event.pos)
        if tile in self.legal_move_tiles:
            self._finish_dice_move(tile)
            return True

        self._show_message("Choose a highlighted destination", (231, 76, 60))
        return True

    def _finish_dice_move(self, destination: str | tuple[int, int]) -> None:
        """Apply a clicked dice destination."""
        if self.current_move_roll is None:
            return

        try:
            player = get_current_player(self.game_state)
            move_by_dice(self.game_state, player, self.current_move_roll, destination)
            if isinstance(destination, str):
                self._add_message(f"{player.name} moved to {destination}")
            else:
                self._add_message(
                    f"{player.name} moved to hallway {destination[0]},{destination[1]}"
                )
            self.current_action = None
            self._clear_move_choices()
            self._update_button_states()
        except ValueError as e:
            self._show_message(str(e), (231, 76, 60))

    def _clear_move_choices(self) -> None:
        """Clear any pending dice movement state."""
        self.current_move_roll = None
        self.legal_move_tiles = set()
        self.legal_move_rooms = set()

    def _execute_suggestion(self) -> None:
        """Execute suggestion action."""
        suspect = self.suspect_dropdown.get_selected()
        weapon = self.weapon_dropdown.get_selected()

        if not suspect or not weapon:
            self._show_message("Please select suspect and weapon!", (231, 76, 60))
            return

        try:
            player = get_current_player(self.game_state)
            # Build Card objects to pass to the engine.
            suspect_card = Card(card_type="suspect", name=suspect)
            weapon_card = Card(card_type="weapon", name=weapon)
            result = make_suggestion(self.game_state, player, suspect_card, weapon_card)

            room = player.current_room
            msg = f"{player.name} suggests: {suspect} with {weapon} in {room}"
            self._add_message(msg)
            # F12: show that the tokens moved into the room.
            self._add_message(
                f"  -> {suspect} token moved to {room}; {weapon} token moved to {room}"
            )

            if result.refuted:
                msg = f"{result.refuting_player} refutes! (showed {result.card_shown.name})"
                self._add_message(msg)
            else:
                self._add_message("No one could refute!")

            self.current_action = None
        except ValueError as e:
            self._show_message(str(e), (231, 76, 60))

    def _execute_accusation(self) -> None:
        """Execute accusation action."""
        suspect = self.suspect_dropdown.get_selected()
        weapon = self.weapon_dropdown.get_selected()
        room = self.room_accusation_dropdown.get_selected()

        if not suspect or not weapon or not room:
            self._show_message("Please select suspect, weapon, and room!", (231, 76, 60))
            return

        try:
            player = get_current_player(self.game_state)
            # Build Card objects to pass to the engine.
            suspect_card = Card(card_type="suspect", name=suspect)
            weapon_card = Card(card_type="weapon", name=weapon)
            room_card = Card(card_type="room", name=room)
            result = make_accusation(
                self.game_state, player, suspect_card, weapon_card, room_card
            )

            msg = f"{player.name} accuses: {suspect} with {weapon} in {room}"
            self._add_message(msg)

            if result.correct:
                self._add_message(f"CORRECT! {player.name} wins!")
            else:
                self._add_message(f"WRONG! {player.name} is eliminated!")

            self.current_action = None
            self._update_button_states()

            # Check for game over
            check_for_winner(self.game_state)

        except ValueError as e:
            self._show_message(str(e), (231, 76, 60))

    def _show_message(self, message: str, color: tuple = (52, 152, 219)) -> None:
        """Show a temporary message box."""
        self.message_box = MessageBox(
            self.width // 2 - 250,
            50,
            500,
            100,
            message
        )
        self.message_box.border_color = color

    def _add_message(self, message: str) -> None:
        """Add message to history."""
        self.messages.append(message)
        if len(self.messages) > 10:
            self.messages.pop(0)

    def update(self) -> Optional[str]:
        if self.message_box and not self.message_box.update():
            self.message_box = None
        if self.game_state.game_over:
            ScreenManager.game_state = self.game_state
            return "end"

        current_player = get_current_player(self.game_state)
        if is_ai_player(current_player):
            ai_result = take_ai_turn(self.game_state)
            self._add_ai_turn_messages(ai_result)
            self.current_action = None
            self._clear_move_choices()
            self._update_button_states()
            if self.game_state.game_over:
                ScreenManager.game_state = self.game_state
                return "end"
        return None

    def _add_ai_turn_messages(self, ai_result: AITurnResult) -> None:
        """Add public AI actions to the game log without exposing private cards."""
        if ai_result.skipped:
            self._add_message(f"{ai_result.player_name} skips normal play")
            return
        if ai_result.dice_roll is not None:
            self._add_message(f"{ai_result.player_name} rolled {ai_result.dice_roll}")
        if ai_result.moved_to:
            self._add_message(f"{ai_result.player_name} moved to {ai_result.moved_to}")
        if ai_result.suggestion:
            suggestion = ai_result.suggestion
            self._add_message(
                f"{ai_result.player_name} suggests: "
                f"{suggestion['suspect']} with {suggestion['weapon']} "
                f"in {suggestion['room']}"
            )
            if ai_result.refute_result and ai_result.refute_result.refuted:
                self._add_message(
                    f"{ai_result.refute_result.refuting_player} refutes the suggestion"
                )
            else:
                self._add_message("No one could refute!")
        if ai_result.accusation:
            accusation = ai_result.accusation
            self._add_message(
                f"{ai_result.player_name} accuses: "
                f"{accusation.suspect} with {accusation.weapon} in {accusation.room}"
            )
            if accusation.correct:
                self._add_message(f"CORRECT! {ai_result.player_name} wins!")
            else:
                self._add_message(f"WRONG! {ai_result.player_name} is eliminated!")

    def _handle_select_event(self, event: pygame.event.Event) -> bool:
        """Route events to the visible popup select controls."""
        visible_selects = self._visible_selects()
        window_rect = self.screen.get_rect()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for select in visible_selects:
                if select.rect.collidepoint(event.pos):
                    select.handle_event(event, window_rect)
                    return True

        active_select = PopupSelect.get_active()
        if active_select and active_select in visible_selects:
            return active_select.handle_event(event, window_rect)

        return False

    def _visible_selects(self) -> List[PopupSelect]:
        """Return selectors shown for the current action panel."""
        if self.current_action == "move":
            return []
        if self.current_action == "suggest":
            return [self.suspect_dropdown, self.weapon_dropdown]
        if self.current_action == "accuse":
            return [
                self.suspect_dropdown,
                self.weapon_dropdown,
                self.room_accusation_dropdown,
            ]
        return []

    def _handle_sidebar_scroll(self, event: pygame.event.Event) -> bool:
        """Scroll the current player's hand when the mouse is over the cards box."""
        if event.type != pygame.MOUSEWHEEL:
            return False
        if not self.cards_scroll_rect.collidepoint(pygame.mouse.get_pos()):
            return False

        max_offset = self._max_cards_scroll_offset()
        if max_offset <= 0:
            return False

        self.cards_scroll_offset = max(
            0,
            min(max_offset, self.cards_scroll_offset - event.y)
        )
        return True

    def _max_cards_scroll_offset(self) -> int:
        """Return the maximum card-row scroll offset for the visible card box."""
        current_player = get_current_player(self.game_state)
        visible_rows = max(1, self.cards_scroll_rect.height // self.card_row_height)
        return max(0, len(current_player.hand) - visible_rows)

    def draw(self) -> None:
        self.screen.fill((218, 211, 197))

        self._draw_sidebar()

        selected_room = None
        if self.current_action == "accuse":
            selected_room = self.room_accusation_dropdown.get_selected()

        self.board.draw(
            self.game_state,
            active_action=self.current_action,
            selected_room=selected_room,
            legal_move_tiles=self.legal_move_tiles,
            legal_move_rooms=self.legal_move_rooms,
        )

        self._draw_main_area()
        self._draw_active_select_popup()

        if self.message_box:
            self.message_box.draw(self.screen)

    def _draw_sidebar(self) -> None:
        """Draw the left-hand player and action column."""
        sidebar_rect = pygame.Rect(0, 0, self.sidebar_width, self.height)
        pygame.draw.rect(self.screen, (32, 43, 54), sidebar_rect)
        pygame.draw.line(
            self.screen,
            (98, 118, 136),
            (self.sidebar_width - 1, 0),
            (self.sidebar_width - 1, self.height),
            2,
        )

        current_player = get_current_player(self.game_state)
        padding = 16
        content_x = 24
        content_width = self.sidebar_width - 48
        section_gap = 12
        button_gap = 10
        button_height = 44
        button_count = 5
        button_area_height = button_height * button_count + button_gap * (button_count - 1)
        buttons_top = self.height - padding - button_area_height

        y = 24

        turn_label = self.small_font.render("Current Turn", True, (174, 187, 199))
        self.screen.blit(turn_label, (content_x, y))

        name = self._truncate(current_player.name, self.title_font, self.sidebar_width - 48)
        name_text = self.title_font.render(name, True, (246, 241, 224))
        self.screen.blit(name_text, (content_x, y + 24))

        location = self._player_location_label(current_player)
        location_label = self.normal_font.render("Location", True, (174, 187, 199))
        location_text = self.normal_font.render(
            self._truncate(location, self.normal_font, self.sidebar_width - 48),
            True,
            (246, 241, 224),
        )
        y += 74
        self.screen.blit(location_label, (content_x, y))
        self.screen.blit(location_text, (content_x, y + 28))

        y += 68
        hand_label = self.normal_font.render("Your Cards", True, (174, 187, 199))
        self.screen.blit(hand_label, (content_x, y))

        cards_y = y + 30
        available_middle_height = max(120, buttons_top - cards_y - section_gap)
        cards_height = min(160, max(80, int(available_middle_height * 0.45)))
        players_height = min(
            204,
            max(80, available_middle_height - cards_height - section_gap)
        )

        self.cards_scroll_rect = pygame.Rect(
            padding,
            cards_y,
            self.sidebar_width - padding * 2,
            cards_height
        )
        self._draw_cards_scroll_box(current_player)

        legend_y = self.cards_scroll_rect.bottom + section_gap
        legend_rect = pygame.Rect(
            padding,
            legend_y,
            self.sidebar_width - padding * 2,
            players_height
        )
        self.board.draw_player_legend(self.screen, legend_rect, self.game_state)

        self._position_sidebar_buttons(buttons_top)
        self.move_button.draw(self.screen)
        self.suggest_button.draw(self.screen)
        self.accuse_button.draw(self.screen)
        self.end_turn_button.draw(self.screen)
        self.quit_game_button.draw(self.screen)

    def _player_location_label(self, player: Player) -> str:
        if player.current_room:
            return player.current_room
        if player.board_position:
            return f"Hallway {player.board_position[0]},{player.board_position[1]}"
        return "Start"

    def _draw_cards_scroll_box(self, current_player: Player) -> None:
        """Draw the current player's cards inside a clipped scroll area."""
        box = self.cards_scroll_rect
        pygame.draw.rect(self.screen, (28, 38, 48), box, border_radius=8)
        pygame.draw.rect(self.screen, (93, 116, 137), box, 1, border_radius=8)

        visible_rows = max(1, box.height // self.card_row_height)
        max_offset = max(0, len(current_player.hand) - visible_rows)
        self.cards_scroll_offset = max(0, min(self.cards_scroll_offset, max_offset))

        previous_clip = self.screen.get_clip()
        inner_rect = box.inflate(-16, -10)
        self.screen.set_clip(inner_rect)

        start = self.cards_scroll_offset
        end = min(len(current_player.hand), start + visible_rows + 1)
        card_y = inner_rect.y
        for row_index, card in enumerate(current_player.hand[start:end]):
            card_line = self._truncate(
                f"- {card.name} ({card.card_type})",
                self.small_font,
                inner_rect.width - 8,
            )
            card_text = self.small_font.render(card_line, True, (236, 240, 241))
            self.screen.blit(card_text, (inner_rect.x, card_y + row_index * self.card_row_height))

        if not current_player.hand:
            empty_text = self.small_font.render("No cards", True, (174, 187, 199))
            self.screen.blit(empty_text, (inner_rect.x, inner_rect.y))

        self.screen.set_clip(previous_clip)

        if max_offset > 0:
            self._draw_cards_scrollbar(max_offset)

    def _draw_cards_scrollbar(self, max_offset: int) -> None:
        """Draw a compact scrollbar for the card list."""
        box = self.cards_scroll_rect
        track_rect = pygame.Rect(box.right - 10, box.y + 8, 5, box.height - 16)
        pygame.draw.rect(self.screen, (77, 94, 110), track_rect, border_radius=3)

        visible_rows = max(1, box.height // self.card_row_height)
        total_rows = visible_rows + max_offset
        thumb_height = max(22, int(track_rect.height * (visible_rows / total_rows)))
        travel = max(1, track_rect.height - thumb_height)
        thumb_y = track_rect.y + int(travel * (self.cards_scroll_offset / max_offset))
        thumb_rect = pygame.Rect(track_rect.x, thumb_y, track_rect.width, thumb_height)
        pygame.draw.rect(self.screen, (174, 187, 199), thumb_rect, border_radius=3)

    def _position_sidebar_buttons(self, top: int) -> None:
        """Pin action buttons to the bottom of the sidebar."""
        button_x = 24
        button_width = self.sidebar_width - 48
        button_height = 44
        button_gap = 10
        buttons = [
            self.move_button,
            self.suggest_button,
            self.accuse_button,
            self.end_turn_button,
            self.quit_game_button,
        ]
        for index, button in enumerate(buttons):
            button.rect = pygame.Rect(
                button_x,
                top + index * (button_height + button_gap),
                button_width,
                button_height
            )

    def _draw_active_select_popup(self) -> None:
        """Draw the active selector popup after the form controls."""
        active_select = PopupSelect.get_active()
        if active_select and active_select in self._visible_selects():
            active_select.draw_popup(self.screen)

    def _draw_main_area(self) -> None:
        """Draw the main area content based on current action."""
        panel_rect = pygame.Rect(self.panel_x, 28, self.panel_width, self.height - 56)
        pygame.draw.rect(self.screen, (244, 239, 226), panel_rect, border_radius=8)
        pygame.draw.rect(self.screen, (121, 103, 83), panel_rect, 2, border_radius=8)

        title = "Cluedo - Make Your Move"
        if self.current_action == "move":
            title = "Roll and Move"
        elif self.current_action == "suggest":
            title = "Make a Suggestion"
        elif self.current_action == "accuse":
            title = "Make an Accusation"

        title_y = 48
        for line in self._wrap_text(title, self.normal_font, self.panel_width - 28):
            title_surface = self.normal_font.render(line, True, (51, 43, 36))
            self.screen.blit(title_surface, (self.panel_x + 14, title_y))
            title_y += self.normal_font.get_linesize()

        # Draw appropriate UI based on action
        if self.current_action == "move":
            self._draw_move_ui()
        elif self.current_action == "suggest":
            self._draw_suggest_ui()
        elif self.current_action == "accuse":
            self._draw_accuse_ui()
        else:
            self._draw_game_info()

    def _draw_move_ui(self) -> None:
        """Draw move action UI."""
        roll = self.current_move_roll if self.current_move_roll is not None else 0
        roll_text = self.normal_font.render(
            f"Dice roll: {roll}",
            True,
            (111, 84, 155),
        )
        self.screen.blit(roll_text, (self.panel_x + 14, 118))

        line_y = 166
        destinations_text = (
            f"Legal destinations: "
            f"{len(self.legal_move_tiles) + len(self.legal_move_rooms)}"
        )
        destinations = self.small_font.render(
            destinations_text,
            True,
            (82, 70, 57),
        )
        self.screen.blit(destinations, (self.panel_x + 14, line_y))

        rooms_text = f"Reachable rooms: {len(self.legal_move_rooms)}"
        rooms = self.small_font.render(rooms_text, True, (82, 70, 57))
        self.screen.blit(rooms, (self.panel_x + 14, line_y + 28))

    def _draw_suggest_ui(self) -> None:
        """Draw suggestion action UI."""
        current_player = get_current_player(self.game_state)

        room_label = self.normal_font.render(
            self._truncate(
                f"Room: {current_player.current_room}",
                self.normal_font,
                self.panel_width - 28,
            ),
            True,
            (111, 84, 155)
        )
        self.screen.blit(room_label, (self.panel_x + 14, 118))

        suspect_label = self.small_font.render("Suspect", True, (82, 70, 57))
        self.screen.blit(suspect_label, (self.panel_x + 14, 194))

        weapon_label = self.small_font.render("Weapon", True, (82, 70, 57))
        self.screen.blit(weapon_label, (self.panel_x + 14, 264))

        self.suspect_dropdown.draw(self.screen)
        self.weapon_dropdown.draw(self.screen)
        self.confirm_suggest_button.draw(self.screen)

    def _draw_accuse_ui(self) -> None:
        """Draw accusation action UI."""
        warning = self.normal_font.render(
            self._truncate(
                "Wrong accusation eliminates you",
                self.normal_font,
                self.panel_width - 28,
            ),
            True,
            (231, 76, 60)
        )
        self.screen.blit(warning, (self.panel_x + 14, 118))

        suspect_label = self.small_font.render("Suspect", True, (82, 70, 57))
        self.screen.blit(suspect_label, (self.panel_x + 14, 194))

        weapon_label = self.small_font.render("Weapon", True, (82, 70, 57))
        self.screen.blit(weapon_label, (self.panel_x + 14, 264))

        room_label = self.small_font.render("Room", True, (82, 70, 57))
        self.screen.blit(room_label, (self.panel_x + 14, 334))

        self.suspect_dropdown.draw(self.screen)
        self.weapon_dropdown.draw(self.screen)
        self.room_accusation_dropdown.draw(self.screen)
        self.confirm_accuse_button.draw(self.screen)

    def _draw_game_info(self) -> None:
        """Draw general game information and message history."""
        # Game status
        status = get_game_status(self.game_state)

        info_y = 120
        info_font = self.normal_font

        players_text = info_font.render(
            f"Players remaining: {status['players_remaining']}",
            True,
            (82, 70, 57)
        )
        self.screen.blit(players_text, (self.panel_x + 14, info_y))

        # Message history
        history_y = 200
        history_label = self.normal_font.render("Game Log", True, (51, 43, 36))
        self.screen.blit(history_label, (self.panel_x + 14, history_y))

        msg_y = history_y + 60
        log_bottom = self.height - 48
        line_height = self.small_font.get_linesize()
        message_gap = 8

        for message in self.messages[-8:]:  # Show last 8 messages
            lines = self._wrap_text(message, self.small_font, self.panel_width - 28)
            message_height = len(lines) * line_height
            if msg_y + message_height > log_bottom:
                break

            for line in lines:
                msg_surface = self.small_font.render(line, True, (82, 70, 57))
                self.screen.blit(msg_surface, (self.panel_x + 14, msg_y))
                msg_y += line_height
            msg_y += message_gap

    def _wrap_text(
        self,
        text: str,
        font: pygame.font.Font,
        max_width: int,
    ) -> List[str]:
        """Wrap text to fit inside a UI column without shortening it."""
        if max_width <= 0:
            return [text]

        words = text.split()
        if not words:
            return [""]

        lines: List[str] = []
        current_line = ""

        for word in words:
            candidate = word if not current_line else f"{current_line} {word}"
            if font.size(candidate)[0] <= max_width:
                current_line = candidate
                continue

            if current_line:
                lines.append(current_line)
                current_line = ""

            if font.size(word)[0] <= max_width:
                current_line = word
                continue

            word_parts = self._split_word_to_width(word, font, max_width)
            lines.extend(word_parts[:-1])
            current_line = word_parts[-1]

        if current_line:
            lines.append(current_line)

        return lines

    def _split_word_to_width(
        self,
        word: str,
        font: pygame.font.Font,
        max_width: int,
    ) -> List[str]:
        """Break a single long word so it cannot overflow the log panel."""
        parts: List[str] = []
        current_part = ""

        for char in word:
            candidate = current_part + char
            if current_part and font.size(candidate)[0] > max_width:
                parts.append(current_part)
                current_part = char
            else:
                current_part = candidate

        if current_part:
            parts.append(current_part)

        return parts or [word]

    def _truncate(self, text: str, font: pygame.font.Font, max_width: int) -> str:
        """Trim text to fit a UI column."""
        if font.size(text)[0] <= max_width:
            return text

        ellipsis = "..."
        trimmed = text
        while trimmed and font.size(trimmed + ellipsis)[0] > max_width:
            trimmed = trimmed[:-1]
        return trimmed + ellipsis if trimmed else ellipsis


class EndScreen(Screen):
    """Game over screen showing winner."""

    def __init__(self, screen: pygame.Surface, game_state: GameState):
        super().__init__(screen)
        self.game_state = game_state

        self.title_font = pygame.font.Font(None, 100)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.normal_font = pygame.font.Font(None, 32)

        # Buttons
        button_width = 250
        button_height = 60
        button_x = (self.width - button_width) // 2

        self.play_again_button = Button(
            button_x, 500,
            button_width, button_height,
            "Play Again",
            color=(46, 204, 113),
            hover_color=(39, 174, 96)
        )

        self.main_menu_button = Button(
            button_x, 580,
            button_width, button_height,
            "Main Menu",
            color=(52, 152, 219),
            hover_color=(41, 128, 185)
        )

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if self.play_again_button.handle_event(event):
            return "setup"
        if self.main_menu_button.handle_event(event):
            return "menu"
        return None

    def draw(self) -> None:
        # Background
        self.screen.fill((44, 62, 80))

        # Game Over title
        title_text = self.title_font.render("GAME OVER", True, (236, 240, 241))
        title_rect = title_text.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Winner announcement
        if self.game_state.winner:
            winner_text = self.subtitle_font.render(
                f"{self.game_state.winner} WINS!",
                True,
                (46, 204, 113)
            )
            winner_rect = winner_text.get_rect(center=(self.width // 2, 250))
            self.screen.blit(winner_text, winner_rect)

            # Solution reveal
            solution = self.game_state.solution
            solution_y = 330

            solution_label = self.normal_font.render("The solution was:", True, (189, 195, 199))
            solution_label_rect = solution_label.get_rect(center=(self.width // 2, solution_y))
            self.screen.blit(solution_label, solution_label_rect)

            suspect_text = self.normal_font.render(
                f"Suspect: {solution['suspect'].name}",
                True,
                (231, 76, 60)
            )
            suspect_rect = suspect_text.get_rect(center=(self.width // 2, solution_y + 40))
            self.screen.blit(suspect_text, suspect_rect)

            weapon_text = self.normal_font.render(
                f"Weapon: {solution['weapon'].name}",
                True,
                (46, 204, 113)
            )
            weapon_rect = weapon_text.get_rect(center=(self.width // 2, solution_y + 80))
            self.screen.blit(weapon_text, weapon_rect)

            room_text = self.normal_font.render(
                f"Room: {solution['room'].name}",
                True,
                (155, 89, 182)
            )
            room_rect = room_text.get_rect(center=(self.width // 2, solution_y + 120))
            self.screen.blit(room_text, room_rect)
        else:
            draw_text = self.subtitle_font.render(
                "It's a Draw!",
                True,
                (149, 165, 166)
            )
            draw_rect = draw_text.get_rect(center=(self.width // 2, 250))
            self.screen.blit(draw_text, draw_rect)

        # Buttons
        self.play_again_button.draw(self.screen)
        self.main_menu_button.draw(self.screen)


class ScreenManager:
    """Manages screen transitions and the current active screen."""

    game_state: Optional[GameState] = None  # Shared game state

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screens = {
            "menu": MainMenuScreen(screen),
            "setup": SetupScreen(screen),
        }
        self.current_screen_name = "menu"
        self.current_screen = self.screens["menu"]

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events and screen transitions."""
        next_screen = self.current_screen.handle_event(event)
        if next_screen:
            self._change_screen(next_screen)

    def update(self) -> None:
        """Update current screen."""
        next_screen = self.current_screen.update()
        if next_screen:
            self._change_screen(next_screen)

    def draw(self) -> None:
        """Draw current screen."""
        self.current_screen.draw()

    def _change_screen(self, screen_name: str) -> None:
        """Change to a different screen."""
        # Create screen if it doesn't exist or needs fresh state
        if screen_name == "game" and ScreenManager.game_state:
            self.screens["game"] = GameScreen(self.screen, ScreenManager.game_state)
        elif screen_name == "end" and ScreenManager.game_state:
            self.screens["end"] = EndScreen(self.screen, ScreenManager.game_state)
        elif screen_name == "setup":
            self.screens["setup"] = SetupScreen(self.screen)  # Fresh setup

        if screen_name in self.screens:
            self.current_screen_name = screen_name
            self.current_screen = self.screens[screen_name]
