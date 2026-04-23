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


# src/ui/components.py
# =====================
# Reusable Pygame UI elements used across multiple screens.

import pygame
from typing import Callable, Optional


class Button:
    """A clickable button with hover effects."""

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            text: str,
            font_size: int = 32,
            color: tuple = (52, 152, 219),
            hover_color: tuple = (41, 128, 185),
            text_color: tuple = (255, 255, 255),
            on_click: Optional[Callable] = None
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.on_click = on_click
        self.font = pygame.font.Font(None, font_size)
        self.enabled = True

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button on screen."""
        if not self.enabled:
            color = (100, 100, 100)
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.color

        # Draw button background
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=8)

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events. Returns True if button was clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos) and self.enabled

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.enabled:
                if self.on_click:
                    self.on_click()
                return True

        return False


class TextInput:
    """A simple text input field."""

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            placeholder: str = "",
            font_size: int = 28,
            max_length: int = 20
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.font = pygame.font.Font(None, font_size)
        self.active = False
        self.max_length = max_length
        self.cursor_visible = True
        self.cursor_timer = 0

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the input field on screen."""
        # Background
        bg_color = (255, 255, 255) if self.active else (240, 240, 240)
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=5)

        # Border
        border_color = (52, 152, 219) if self.active else (200, 200, 200)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=5)

        # Text or placeholder
        display_text = self.text if self.text else self.placeholder
        text_color = (0, 0, 0) if self.text else (150, 150, 150)
        text_surface = self.font.render(display_text, True, text_color)

        # Add cursor if active
        if self.active and self.cursor_visible and self.text:
            cursor_x = self.rect.x + 10 + text_surface.get_width()
            pygame.draw.line(
                screen,
                (0, 0, 0),
                (cursor_x, self.rect.y + 10),
                (cursor_x, self.rect.bottom - 10),
                2
            )

        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle keyboard and mouse events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif len(self.text) < self.max_length:
                if event.unicode.isprintable():
                    self.text += event.unicode

    def update(self) -> None:
        """Update cursor blink animation."""
        self.cursor_timer += 1
        if self.cursor_timer >= 30:  # Blink every 30 frames
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def get_text(self) -> str:
        """Get the current text value."""
        return self.text.strip()

    def clear(self) -> None:
        """Clear the input field."""
        self.text = ""


class CardDisplay:
    """Display a single Cluedo card."""

    def __init__(self, x: int, y: int, card_name: str, card_type: str):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 140
        self.card_name = card_name
        self.card_type = card_type

        # Card type colors
        self.type_colors = {
            "suspect": (231, 76, 60),  # Red
            "weapon": (46, 204, 113),  # Green
            "room": (155, 89, 182)  # Purple
        }

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the card on screen."""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Card background
        pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=8)

        # Card type color bar at top
        type_color = self.type_colors.get(self.card_type, (100, 100, 100))
        type_bar = pygame.Rect(self.x, self.y, self.width, 30)
        pygame.draw.rect(screen, type_color, type_bar, border_top_left_radius=8, border_top_right_radius=8)

        # Card border
        pygame.draw.rect(screen, (50, 50, 50), rect, 2, border_radius=8)

        # Card type text
        type_font = pygame.font.Font(None, 20)
        type_text = type_font.render(self.card_type.upper(), True, (255, 255, 255))
        type_rect = type_text.get_rect(center=(self.x + self.width // 2, self.y + 15))
        screen.blit(type_text, type_rect)

        # Card name (wrapped if needed)
        name_font = pygame.font.Font(None, 22)
        words = self.card_name.split()
        y_offset = self.y + 45

        for word in words:
            word_surface = name_font.render(word, True, (0, 0, 0))
            word_rect = word_surface.get_rect(center=(self.x + self.width // 2, y_offset))
            screen.blit(word_surface, word_rect)
            y_offset += 25


class DropdownMenu:
    """A dropdown menu for selecting options."""

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            options: list[str],
            label: str = "Select"
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected = None
        self.is_open = False
        self.label = label
        self.font = pygame.font.Font(None, 28)

        # Calculate dropdown panel height
        self.option_height = 40
        self.panel_height = min(len(options) * self.option_height, 300)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the dropdown menu."""
        # Main button
        bg_color = (255, 255, 255)
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (52, 152, 219), self.rect, 2, border_radius=5)

        # Display selected or label
        display_text = self.selected if self.selected else self.label
        text_surface = self.font.render(display_text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

        # Arrow
        arrow = "▼" if not self.is_open else "▲"
        arrow_surface = self.font.render(arrow, True, (0, 0, 0))
        screen.blit(arrow_surface, (self.rect.right - 30, self.rect.y + 10))

        # Dropdown panel
        if self.is_open:
            panel_rect = pygame.Rect(
                self.rect.x,
                self.rect.bottom,
                self.rect.width,
                self.panel_height
            )
            pygame.draw.rect(screen, (255, 255, 255), panel_rect)
            pygame.draw.rect(screen, (52, 152, 219), panel_rect, 2)

            # Options
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.bottom + i * self.option_height,
                    self.rect.width,
                    self.option_height
                )

                # Hover effect
                mouse_pos = pygame.mouse.get_pos()
                if option_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (230, 240, 255), option_rect)

                option_text = self.font.render(option, True, (0, 0, 0))
                screen.blit(option_text, (option_rect.x + 10, option_rect.y + 10))

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events. Returns True if selection changed."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
                return False

            elif self.is_open:
                # Check if clicking an option
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.bottom + i * self.option_height,
                        self.rect.width,
                        self.option_height
                    )
                    if option_rect.collidepoint(event.pos):
                        self.selected = option
                        self.is_open = False
                        return True

                # Clicked outside, close dropdown
                self.is_open = False

        return False

    def get_selected(self) -> Optional[str]:
        """Get the currently selected option."""
        return self.selected

    def reset(self) -> None:
        """Reset the selection."""
        self.selected = None
        self.is_open = False


class MessageBox:
    """Display a temporary message box."""

    def __init__(self, x: int, y: int, width: int, height: int, message: str, duration: int = 180):
        self.rect = pygame.Rect(x, y, width, height)
        self.message = message
        self.duration = duration
        self.timer = 0
        self.font = pygame.font.Font(None, 28)

        # Message type colors
        self.bg_color = (255, 255, 255)
        self.border_color = (52, 152, 219)
        self.text_color = (0, 0, 0)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the message box."""
        if self.timer < self.duration:
            # Background
            pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=8)
            pygame.draw.rect(screen, self.border_color, self.rect, 3, border_radius=8)

            # Message text (wrapped)
            words = self.message.split()
            lines = []
            current_line = []

            for word in words:
                test_line = ' '.join(current_line + [word])
                test_surface = self.font.render(test_line, True, self.text_color)

                if test_surface.get_width() <= self.rect.width - 20:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]

            if current_line:
                lines.append(' '.join(current_line))

            # Draw lines
            y_offset = self.rect.y + 15
            for line in lines:
                line_surface = self.font.render(line, True, self.text_color)
                screen.blit(line_surface, (self.rect.x + 10, y_offset))
                y_offset += 30

    def update(self) -> bool:
        """Update timer. Returns True if message is still visible."""
        self.timer += 1
        return self.timer < self.duration

    def is_visible(self) -> bool:
        """Check if message is still visible."""
        return self.timer < self.duration