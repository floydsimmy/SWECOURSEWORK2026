# tests/test_models.py
# =====================
# Pytest tests for the data models defined in src/game/models.py.
# Run from the cluedo/ directory with:  pytest

import pytest

from game.models import AccusationResult, Card, GameState, Player, RefuteResult


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------


def test_card_stores_type_and_name() -> None:
    """Card fields are set exactly as supplied."""
    card = Card(card_type="suspect", name="Miss Scarlet")
    assert card.card_type == "suspect"
    assert card.name == "Miss Scarlet"


def test_card_weapon_type() -> None:
    """Card correctly represents a weapon."""
    card = Card(card_type="weapon", name="Knife")
    assert card.card_type == "weapon"
    assert card.name == "Knife"


def test_card_room_type() -> None:
    """Card correctly represents a room."""
    card = Card(card_type="room", name="Library")
    assert card.card_type == "room"
    assert card.name == "Library"


# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------


def test_player_stores_name() -> None:
    """Player is created with the given name."""
    player = Player(name="Alice")
    assert player.name == "Alice"


def test_player_default_hand_is_empty() -> None:
    """Player starts with an empty hand when none is supplied."""
    player = Player(name="Bob")
    assert player.hand == []


def test_player_default_room_is_none() -> None:
    """Player's current_room defaults to None."""
    player = Player(name="Carol")
    assert player.current_room is None


def test_player_default_not_eliminated() -> None:
    """Player is not eliminated by default."""
    player = Player(name="Dave")
    assert player.is_eliminated is False


def test_player_hand_mutable_default_not_shared() -> None:
    """Each Player instance gets its own independent hand list."""
    p1 = Player(name="Eve")
    p2 = Player(name="Frank")
    p1.hand.append(Card(card_type="weapon", name="Rope"))
    assert p2.hand == [], "Mutating p1's hand must not affect p2's hand"


def test_player_with_explicit_hand() -> None:
    """Player stores a hand supplied at construction time."""
    cards = [Card("weapon", "Wrench"), Card("room", "Hall")]
    player = Player(name="Grace", hand=cards)
    assert len(player.hand) == 2
    assert player.hand[0].name == "Wrench"


# ---------------------------------------------------------------------------
# GameState
# ---------------------------------------------------------------------------


def test_gamestate_stores_players_and_solution() -> None:
    """GameState holds the player list and solution dict."""
    players = [Player("Alice"), Player("Bob"), Player("Carol")]
    solution = {
        "suspect": Card("suspect", "Colonel Mustard"),
        "weapon": Card("weapon", "Revolver"),
        "room": Card("room", "Study"),
    }
    state = GameState(players=players, solution=solution, current_turn_index=0)
    assert len(state.players) == 3
    assert state.solution["suspect"].name == "Colonel Mustard"
    assert state.current_turn_index == 0


def test_gamestate_started_default_false() -> None:
    """GameState.started defaults to False when not explicitly set."""
    state = GameState(players=[], solution={}, current_turn_index=0)
    assert state.started is False


# ---------------------------------------------------------------------------
# RefuteResult
# ---------------------------------------------------------------------------


def test_refute_result_refuted_true() -> None:
    """RefuteResult stores all fields when a card is shown."""
    card = Card("weapon", "Candlestick")
    result = RefuteResult(refuted=True, refuting_player="Bob", card_shown=card)
    assert result.refuted is True
    assert result.refuting_player == "Bob"
    assert result.card_shown is card


def test_refute_result_defaults_when_not_refuted() -> None:
    """RefuteResult refuting_player and card_shown default to None."""
    result = RefuteResult(refuted=False)
    assert result.refuted is False
    assert result.refuting_player is None
    assert result.card_shown is None


# ---------------------------------------------------------------------------
# AccusationResult
# ---------------------------------------------------------------------------


def test_accusation_result_correct() -> None:
    """AccusationResult stores all fields for a correct accusation."""
    result = AccusationResult(
        correct=True,
        player_name="Alice",
        suspect="Miss Scarlet",
        weapon="Rope",
        room="Kitchen",
    )
    assert result.correct is True
    assert result.player_name == "Alice"
    assert result.suspect == "Miss Scarlet"
    assert result.weapon == "Rope"
    assert result.room == "Kitchen"


def test_accusation_result_incorrect() -> None:
    """AccusationResult stores correct=False for a wrong accusation."""
    result = AccusationResult(
        correct=False,
        player_name="Bob",
        suspect="Professor Plum",
        weapon="Knife",
        room="Ballroom",
    )
    assert result.correct is False
