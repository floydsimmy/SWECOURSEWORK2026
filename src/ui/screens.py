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

# src/ui/screens.py
# ==================
# Manages all game screens and transitions between them.

import pygame
from typing import Optional, List
from src.game.engine import (
    new_game,
    get_current_player,
    move_to_room,
    make_suggestion,
    make_accusation,
    next_turn,
    get_game_status,
    check_for_winner
)
from src.game.models import GameState, Player
from src.game.deck import SUSPECTS, WEAPONS, ROOMS
from src.ui.components import Button, TextInput, CardDisplay, DropdownMenu, MessageBox


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

        input_width = 400
        input_height = 50
        start_y = 180
        spacing = 70

        for i in range(self.max_players):
            text_input = TextInput(
                (self.width - input_width) // 2,
                start_y + i * spacing,
                input_width,
                input_height,
                placeholder=f"Player {i + 1} name" + (" (optional)" if i >= 3 else "")
            )
            self.input_fields.append(text_input)

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

        # Handle buttons
        if self.start_game_button.handle_event(event):
            return self._try_start_game()

        if self.back_button.handle_event(event):
            return "menu"

        return None

    def _try_start_game(self) -> Optional[str]:
        """Validate inputs and start game if valid."""
        player_names = [field.get_text() for field in self.input_fields if field.get_text()]

        if len(player_names) < self.min_players:
            self.error_message = f"Need at least {self.min_players} players!"
            return None

        if len(player_names) != len(set(player_names)):
            self.error_message = "Player names must be unique!"
            return None

        # Create game state and store it
        try:
            game_state = new_game(player_names)
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
        self.sidebar_width = 350
        self.main_area_x = self.sidebar_width + 20

        # Action buttons
        button_width = 180
        button_height = 45
        button_x = 20
        button_y = 400
        button_spacing = 60

        self.move_button = Button(
            button_x, button_y,
            button_width, button_height,
            "Move to Room",
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

        # Dropdown menus for actions
        dropdown_x = self.main_area_x
        dropdown_width = 250
        dropdown_height = 45

        self.room_dropdown = DropdownMenu(
            dropdown_x, 150,
            dropdown_width, dropdown_height,
            ROOMS,
            "Select Room"
        )

        self.suspect_dropdown = DropdownMenu(
            dropdown_x, 220,
            dropdown_width, dropdown_height,
            SUSPECTS,
            "Select Suspect"
        )

        self.weapon_dropdown = DropdownMenu(
            dropdown_x, 290,
            dropdown_width, dropdown_height,
            WEAPONS,
            "Select Weapon"
        )

        self.room_accusation_dropdown = DropdownMenu(
            dropdown_x, 360,
            dropdown_width, dropdown_height,
            ROOMS,
            "Select Room"
        )

        # Confirm buttons for actions
        confirm_x = dropdown_x + dropdown_width + 20
        self.confirm_move_button = Button(
            confirm_x, 150, 120, 45,
            "Confirm", font_size=24
        )

        self.confirm_suggest_button = Button(
            confirm_x, 290, 120, 45,
            "Confirm", font_size=24
        )

        self.confirm_accuse_button = Button(
            confirm_x, 360, 120, 45,
            "Confirm", font_size=24
        )

        # UI State
        self.current_action: Optional[str] = None  # "move", "suggest", "accuse"
        self.message_box: Optional[MessageBox] = None
        self.messages: List[str] = []

        self._update_button_states()

    def _update_button_states(self) -> None:
        """Update which buttons are enabled based on game state."""
        current_player = get_current_player(self.game_state)

        # Suggest only available if in a room
        self.suggest_button.enabled = current_player.current_room is not None

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

        # Handle dropdowns
        self.room_dropdown.handle_event(event)
        self.suspect_dropdown.handle_event(event)
        self.weapon_dropdown.handle_event(event)
        self.room_accusation_dropdown.handle_event(event)

        # Handle action buttons
        if self.move_button.handle_event(event):
            self.current_action = "move"
            self.room_dropdown.reset()
            return None

        if self.suggest_button.handle_event(event):
            self.current_action = "suggest"
            self.suspect_dropdown.reset()
            self.weapon_dropdown.reset()
            return None

        if self.accuse_button.handle_event(event):
            self.current_action = "accuse"
            self.suspect_dropdown.reset()
            self.weapon_dropdown.reset()
            self.room_accusation_dropdown.reset()
            return None

        if self.end_turn_button.handle_event(event):
            next_turn(self.game_state)
            self.current_action = None
            self._update_button_states()
            self._add_message(f"Turn passed to {get_current_player(self.game_state).name}")
            return None

        # Handle confirm buttons
        if self.current_action == "move" and self.confirm_move_button.handle_event(event):
            self._execute_move()
            return None

        if self.current_action == "suggest" and self.confirm_suggest_button.handle_event(event):
            self._execute_suggestion()
            return None

        if self.current_action == "accuse" and self.confirm_accuse_button.handle_event(event):
            self._execute_accusation()
            return None

        return None

    def _execute_move(self) -> None:
        """Execute move to room action."""
        room = self.room_dropdown.get_selected()
        if not room:
            self._show_message("Please select a room!", (231, 76, 60))
            return

        try:
            player = get_current_player(self.game_state)
            move_to_room(self.game_state, player, room)
            self._add_message(f"{player.name} moved to {room}")
            self.current_action = None
            self._update_button_states()
        except ValueError as e:
            self._show_message(str(e), (231, 76, 60))

    def _execute_suggestion(self) -> None:
        """Execute suggestion action."""
        suspect = self.suspect_dropdown.get_selected()
        weapon = self.weapon_dropdown.get_selected()

        if not suspect or not weapon:
            self._show_message("Please select suspect and weapon!", (231, 76, 60))
            return

        try:
            player = get_current_player(self.game_state)
            result = make_suggestion(self.game_state, player, suspect, weapon)

            room = player.current_room
            msg = f"{player.name} suggests: {suspect} with {weapon} in {room}"
            self._add_message(msg)

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
            result = make_accusation(self.game_state, player, suspect, weapon, room)

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
        return None

    def draw(self) -> None:
        self.screen.fill((236, 240, 241))

        # Draw sidebar (player info and actions)
        sidebar_rect = pygame.Rect(0, 0, self.sidebar_width, self.height)
        pygame.draw.rect(self.screen, (52, 73, 94), sidebar_rect)

        # Current player info
        current_player = get_current_player(self.game_state)

        # Player name
        name_text = self.title_font.render(current_player.name, True, (236, 240, 241))
        self.screen.blit(name_text, (20, 20))

        # Current room
        room_label = self.normal_font.render("Current Room:", True, (189, 195, 199))
        self.screen.blit(room_label, (20, 80))

        room_text = current_player.current_room if current_player.current_room else "None"
        room_value = self.normal_font.render(room_text, True, (236, 240, 241))
        self.screen.blit(room_value, (20, 110))

        # Player hand
        hand_label = self.normal_font.render("Your Cards:", True, (189, 195, 199))
        self.screen.blit(hand_label, (20, 160))

        # Draw cards in hand
        card_y = 200
        for i, card in enumerate(current_player.hand[:5]):  # Show first 5
            card_text = self.small_font.render(
                f"• {card.name} ({card.card_type})",
                True,
                (236, 240, 241)
            )
            self.screen.blit(card_text, (25, card_y + i * 25))

        if len(current_player.hand) > 5:
            more_text = self.small_font.render(
                f"... and {len(current_player.hand) - 5} more",
                True,
                (189, 195, 199)
            )
            self.screen.blit(more_text, (25, card_y + 5 * 25))

        # Action buttons
        self.move_button.draw(self.screen)
        self.suggest_button.draw(self.screen)
        self.accuse_button.draw(self.screen)
        self.end_turn_button.draw(self.screen)

        # Draw main area based on current action
        self._draw_main_area()

        # Draw message box if active
        if self.message_box:
            self.message_box.draw(self.screen)

    def _draw_main_area(self) -> None:
        """Draw the main area content based on current action."""
        # Title
        title = "Cluedo - Make Your Move"
        if self.current_action == "move":
            title = "Move to a Room"
        elif self.current_action == "suggest":
            title = "Make a Suggestion"
        elif self.current_action == "accuse":
            title = "Make an Accusation"

        title_surface = self.title_font.render(title, True, (44, 62, 80))
        self.screen.blit(title_surface, (self.main_area_x, 30))

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
        label = self.normal_font.render("Select a room to move to:", True, (52, 73, 94))
        self.screen.blit(label, (self.main_area_x, 120))

        self.room_dropdown.draw(self.screen)
        self.confirm_move_button.draw(self.screen)

    def _draw_suggest_ui(self) -> None:
        """Draw suggestion action UI."""
        current_player = get_current_player(self.game_state)

        room_label = self.normal_font.render(
            f"Room: {current_player.current_room}",
            True,
            (155, 89, 182)
        )
        self.screen.blit(room_label, (self.main_area_x, 120))

        suspect_label = self.normal_font.render("Suspect:", True, (52, 73, 94))
        self.screen.blit(suspect_label, (self.main_area_x, 190))

        weapon_label = self.normal_font.render("Weapon:", True, (52, 73, 94))
        self.screen.blit(weapon_label, (self.main_area_x, 260))

        self.suspect_dropdown.draw(self.screen)
        self.weapon_dropdown.draw(self.screen)
        self.confirm_suggest_button.draw(self.screen)

    def _draw_accuse_ui(self) -> None:
        """Draw accusation action UI."""
        warning = self.normal_font.render(
            "WARNING: Wrong accusation eliminates you!",
            True,
            (231, 76, 60)
        )
        self.screen.blit(warning, (self.main_area_x, 120))

        suspect_label = self.normal_font.render("Suspect:", True, (52, 73, 94))
        self.screen.blit(suspect_label, (self.main_area_x, 190))

        weapon_label = self.normal_font.render("Weapon:", True, (52, 73, 94))
        self.screen.blit(weapon_label, (self.main_area_x, 260))

        room_label = self.normal_font.render("Room:", True, (52, 73, 94))
        self.screen.blit(room_label, (self.main_area_x, 330))

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
            (52, 73, 94)
        )
        self.screen.blit(players_text, (self.main_area_x, info_y))

        # Message history
        history_y = 200
        history_label = self.title_font.render("Game Log:", True, (44, 62, 80))
        self.screen.blit(history_label, (self.main_area_x, history_y))

        msg_y = history_y + 60
        for message in self.messages[-8:]:  # Show last 8 messages
            msg_surface = self.small_font.render(message, True, (52, 73, 94))
            self.screen.blit(msg_surface, (self.main_area_x, msg_y))
            msg_y += 30


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