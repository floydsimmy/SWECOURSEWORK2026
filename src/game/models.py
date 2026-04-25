"""Data models for the Cluedo game.

Holds the dataclasses that describe game state. All gameplay rules live
in `engine.py`; these types are pure data and have no behaviour beyond
their own representation.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Card:
    """A single Cluedo card.

    `card_type` is one of "suspect", "weapon", or "room". `name` is the
    display name (e.g. "Miss Scarlet", "Knife", "Kitchen").
    """

    card_type: str
    name: str

    def __str__(self) -> str:
        return f"{self.name} ({self.card_type})"


@dataclass
class Player:
    """A player at the table.

    `current_room` is None until the player moves into a room.
    `is_eliminated` flips to True after a wrong accusation; their hand
    stays intact so they can still refute future suggestions.
    """

    name: str
    hand: list[Card] = field(default_factory=list)
    current_room: str | None = None
    is_eliminated: bool = False

    def __str__(self) -> str:
        room = self.current_room if self.current_room else "no room"
        return f"{self.name} (in {room})"


@dataclass
class GameState:
    """Whole-game state passed between engine functions.

    `suspect_locations` and `weapon_locations` track where each suspect
    or weapon TOKEN currently sits on the board, keyed by card name.
    A value of None means the token has not yet been placed in a room.
    Required by F12 (domain): a suggestion moves the named suspect and
    weapon tokens into the suggester's current room and leaves them
    there.
    """

    players: list[Player]
    solution: dict[str, Card]
    current_turn_index: int
    started: bool = False
    game_over: bool = False
    winner: str | None = None
    turn_history: list[dict] = field(default_factory=list)
    suspect_locations: dict[str, str | None] = field(default_factory=dict)
    weapon_locations: dict[str, str | None] = field(default_factory=dict)


@dataclass
class RefuteResult:
    """Outcome of a suggestion's refutation pass."""

    refuted: bool
    refuting_player: str | None = None
    card_shown: Card | None = None


@dataclass
class AccusationResult:
    """Outcome of an accusation."""

    correct: bool
    player_name: str
    suspect: str
    weapon: str
    room: str
