# src/ui/components.py
# =====================
# Reusable Pygame UI elements used across multiple screens.
#
# Components in this file:
#   - Button      — a clickable rectangle with a text label
#   - TextInput   — a single-line editable text field
#   - CardDisplay — shows a card image or name on screen
#   - PopupSelect — a dropdown-style picker
#   - MessageBox  — a modal dialog with confirm/cancel buttons
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


class PopupSelect:
    """A dropdown menu. Only one popup is open at a time."""

    active_select = None  # current open popup, or None

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            options: list[str],
            label: str = "Select",
            max_visible_options: int = 6
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected = None
        self.label = label
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        self.is_open = False
        self.scroll_offset = 0

        self.option_height = 40
        self.max_visible_options = max(1, max_visible_options)
        self.visible_option_count = min(len(options), self.max_visible_options)
        self.popup_rect = pygame.Rect(0, 0, width, self._popup_height())

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the closed select field."""
        bg_color = (255, 255, 255)
        border_color = (41, 128, 185) if self.is_open else (52, 152, 219)
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=5)

        display_text = self.selected if self.selected else self.label
        text = self._truncate(display_text, self.font, self.rect.width - 44)
        text_color = (0, 0, 0) if self.selected else (105, 114, 124)
        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surface, text_rect)

        # Arrow
        arrow = "▼" if not self.is_open else "▲"
        arrow_surface = self.font.render(arrow, True, (0, 0, 0))
        screen.blit(arrow_surface, (self.rect.right - 30, self.rect.y + 10))
        arrow_cover = pygame.Rect(self.rect.right - 36, self.rect.y + 3, 32, self.rect.height - 6)
        pygame.draw.rect(screen, bg_color, arrow_cover)
        arrow_points = [
            (self.rect.right - 25, self.rect.centery - 4),
            (self.rect.right - 13, self.rect.centery - 4),
            (self.rect.right - 19, self.rect.centery + 5),
        ]
        pygame.draw.polygon(screen, (0, 0, 0), arrow_points)

    def draw_popup(self, screen: pygame.Surface) -> None:
        """Draw the separate popup list above the main form."""
        if not self.is_open:
            return

        popup = self.popup_rect
        shadow = popup.move(4, 4)
        pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), popup, border_radius=8)
        pygame.draw.rect(screen, (52, 73, 94), popup, 2, border_radius=8)

        header_rect = pygame.Rect(popup.x, popup.y, popup.width, 36)
        pygame.draw.rect(
            screen,
            (52, 73, 94),
            header_rect,
            border_top_left_radius=8,
            border_top_right_radius=8,
        )
        header_text = self.small_font.render(self.label, True, (236, 240, 241))
        screen.blit(header_text, (header_rect.x + 12, header_rect.y + 9))

        list_top = popup.y + 36
        option_area_width = popup.width - (14 if self._needs_scrollbar() else 0)
        visible_options = self.options[
            self.scroll_offset:self.scroll_offset + self.visible_option_count
        ]
        mouse_pos = pygame.mouse.get_pos()

        for i, option in enumerate(visible_options):
            option_rect = pygame.Rect(
                popup.x,
                list_top + i * self.option_height,
                option_area_width,
                self.option_height
            )
            if option_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (230, 240, 255), option_rect)
            if option == self.selected:
                pygame.draw.rect(screen, (213, 232, 249), option_rect)

            text = self._truncate(option, self.font, option_area_width - 20)
            option_text = self.font.render(text, True, (0, 0, 0))
            text_rect = option_text.get_rect(midleft=(option_rect.x + 10, option_rect.centery))
            screen.blit(option_text, text_rect)

        if self._needs_scrollbar():
            self._draw_scrollbar(screen)

    def handle_event(
            self,
            event: pygame.event.Event,
            window_rect: pygame.Rect
    ) -> bool:
        """Handle selector events. Returns True when the event is consumed."""
        if event.type == pygame.MOUSEWHEEL and self.is_open:
            self.scroll_offset = self._clamp_scroll_offset(self.scroll_offset - event.y)
            return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.is_open:
                    self.close()
                else:
                    self.open(window_rect)
                return True

            if self.is_open:
                if self.popup_rect.collidepoint(event.pos):
                    self._select_at(event.pos)
                else:
                    self.close()
                return True

        return False

    def get_selected(self) -> Optional[str]:
        """Get the currently selected option."""
        return self.selected

    def reset(self) -> None:
        """Reset the selection."""
        self.selected = None
        self.scroll_offset = 0
        self.close()

    def open(self, window_rect: pygame.Rect) -> None:
        """Open this selector and close any other active selector."""
        if PopupSelect.active_select and PopupSelect.active_select is not self:
            PopupSelect.active_select.close()
        self.is_open = True
        PopupSelect.active_select = self
        self.scroll_offset = self._clamp_scroll_offset(self.scroll_offset)
        self._position_popup(window_rect)

    def close(self) -> None:
        """Close the selector popup."""
        self.is_open = False
        if PopupSelect.active_select is self:
            PopupSelect.active_select = None

    @classmethod
    def get_active(cls) -> Optional["PopupSelect"]:
        """Return the currently open select, if any."""
        return cls.active_select

    @classmethod
    def close_active(cls) -> None:
        """Close whichever select is currently open."""
        if cls.active_select:
            cls.active_select.close()

    def _select_at(self, pos: tuple[int, int]) -> None:
        list_top = self.popup_rect.y + 36
        if pos[1] < list_top:
            return

        option_area_width = self.popup_rect.width - (14 if self._needs_scrollbar() else 0)
        option_area = pygame.Rect(
            self.popup_rect.x,
            list_top,
            option_area_width,
            self.visible_option_count * self.option_height
        )
        if not option_area.collidepoint(pos):
            return

        visible_index = (pos[1] - list_top) // self.option_height
        option_index = self.scroll_offset + visible_index
        if 0 <= option_index < len(self.options):
            self.selected = self.options[option_index]
            self.close()

    def _position_popup(self, window_rect: pygame.Rect) -> None:
        popup_width = max(self.rect.width, self._preferred_popup_width())
        popup_width = min(popup_width, 300, window_rect.width - 24)
        popup_height = self._popup_height()

        x = self.rect.x - popup_width - 12
        if x < window_rect.x + 12:
            x = self.rect.x
        x = min(x, window_rect.right - popup_width - 12)

        y = self.rect.y
        y = max(window_rect.y + 12, min(y, window_rect.bottom - popup_height - 12))

        self.popup_rect = pygame.Rect(x, y, popup_width, popup_height)

    def _popup_height(self) -> int:
        return 36 + self.visible_option_count * self.option_height

    def _preferred_popup_width(self) -> int:
        longest = max((self.font.size(option)[0] for option in self.options), default=0)
        return longest + 44

    def _needs_scrollbar(self) -> bool:
        return len(self.options) > self.visible_option_count

    def _max_scroll_offset(self) -> int:
        return max(0, len(self.options) - self.visible_option_count)

    def _clamp_scroll_offset(self, value: int) -> int:
        return max(0, min(value, self._max_scroll_offset()))

    def _draw_scrollbar(self, screen: pygame.Surface) -> None:
        """Draw a compact scrollbar for long option lists."""
        track_rect = pygame.Rect(
            self.popup_rect.right - 10,
            self.popup_rect.y + 42,
            6,
            self.popup_rect.height - 48
        )
        pygame.draw.rect(screen, (220, 225, 230), track_rect, border_radius=3)

        ratio = self.visible_option_count / len(self.options)
        thumb_height = max(24, int(track_rect.height * ratio))
        max_offset = self._max_scroll_offset()
        if max_offset == 0:
            thumb_y = track_rect.y
        else:
            travel = track_rect.height - thumb_height
            thumb_y = track_rect.y + int(travel * (self.scroll_offset / max_offset))

        thumb_rect = pygame.Rect(track_rect.x, thumb_y, track_rect.width, thumb_height)
        pygame.draw.rect(screen, (52, 152, 219), thumb_rect, border_radius=3)

    def _truncate(self, text: str, font: pygame.font.Font, max_width: int) -> str:
        if font.size(text)[0] <= max_width:
            return text

        ellipsis = "..."
        trimmed = text
        while trimmed and font.size(trimmed + ellipsis)[0] > max_width:
            trimmed = trimmed[:-1]
        return trimmed + ellipsis if trimmed else ellipsis


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
                if self.font.size(test_line)[0] <= self.rect.width - 20:
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
