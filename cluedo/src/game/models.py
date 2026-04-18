# src/game/models.py
# ===================
# Core data objects (models) used throughout the game.
# These classes hold state only — no game logic goes here.
# Logic lives in engine.py and rules.py.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Card:
    """A single Cluedo card.

    Attributes:
        card_type: Category of card — one of "suspect", "weapon", or "room".
        name: The display name of the card (e.g. "Miss Scarlet", "Knife").
    """

    card_type: str  # "suspect" | "weapon" | "room"
    name: str

    def __str__(self) -> str:
        return f"Card({self.card_type}: {self.name})"


@dataclass
class Player:
    """A participant in the game.

    Attributes:
        name: The player's display name.
        hand: The cards currently held by this player.
        current_room: The room the player is currently in, or None if not yet placed.
        is_eliminated: True if the player made a wrong accusation and is out.
    """

    name: str
    hand: list[Card] = field(default_factory=list)
    current_room: Optional[str] = None
    is_eliminated: bool = False

    def __str__(self) -> str:
        room_part = f"in {self.current_room}" if self.current_room is not None else "no room"
        return f"Player({self.name}, {len(self.hand)} cards, {room_part})"


@dataclass
class GameState:
    """Complete state of a Cluedo game at any point in time.

    Attributes:
        players: All players in turn order.
        solution: The hidden murder solution — dict with keys
                  "suspect", "weapon", and "room", each holding a Card.
        current_turn_index: Index into ``players`` for whose turn it is.
        started: Whether the game has been fully set up and started.
    """

    players: list[Player]
    solution: dict[str, Card]
    current_turn_index: int
    started: bool = False
    game_over: bool = False
    winner: Optional[str] = None
    turn_history: list = field(default_factory=list)


@dataclass
class RefuteResult:
    """Outcome of a suggestion made during a player's turn.

    Attributes:
        refuted: True if at least one other player could show a matching card.
        refuting_player: Name of the first player who refuted, or None.
        card_shown: The card that was shown to disprove the suggestion, or None.
    """

    refuted: bool
    refuting_player: Optional[str] = None
    card_shown: Optional[Card] = None


@dataclass
class AccusationResult:
    """Outcome of a formal accusation.

    Attributes:
        correct: True if the accusation matches the solution exactly.
        player_name: Name of the player who made the accusation.
        suspect: The suspected character named in the accusation.
        weapon: The suspected weapon named in the accusation.
        room: The suspected room named in the accusation.
    """

    correct: bool
    player_name: str
    suspect: str
    weapon: str
    room: str
