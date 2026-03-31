# tests/test_engine.py
# =====================
# Pytest tests for the game engine (src/game/engine.py).
# Run from the cluedo/ directory with:  pytest

import pytest

from game.deck import ROOMS, SUSPECTS, WEAPONS
from game.engine import (
    get_current_player,
    make_accusation,
    make_suggestion,
    move_to_room,
    new_game,
    next_turn,
)
from game.models import Card, GameState, Player


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_state(player_names: list[str] | None = None) -> GameState:
    """Return a fresh GameState for the given player names (default 3)."""
    if player_names is None:
        player_names = ["Alice", "Bob", "Carol"]
    return new_game(player_names)


# ---------------------------------------------------------------------------
# F1 — Solution contains exactly one suspect, weapon, and room
# ---------------------------------------------------------------------------


def test_solution_has_one_suspect() -> None:
    """F1: Solution contains exactly one suspect card."""
    state = _make_state()
    assert state.solution["suspect"].card_type == "suspect"
    assert state.solution["suspect"].name in SUSPECTS


def test_solution_has_one_weapon() -> None:
    """F1: Solution contains exactly one weapon card."""
    state = _make_state()
    assert state.solution["weapon"].card_type == "weapon"
    assert state.solution["weapon"].name in WEAPONS


def test_solution_has_one_room() -> None:
    """F1: Solution contains exactly one room card."""
    state = _make_state()
    assert state.solution["room"].card_type == "room"
    assert state.solution["room"].name in ROOMS


def test_solution_has_exactly_three_keys() -> None:
    """F1: Solution dict has exactly the keys 'suspect', 'weapon', 'room'."""
    state = _make_state()
    assert set(state.solution.keys()) == {"suspect", "weapon", "room"}


# ---------------------------------------------------------------------------
# F2 — All remaining cards are dealt; no card is lost or duplicated
# ---------------------------------------------------------------------------


def test_all_cards_dealt_no_loss() -> None:
    """F2: Total cards in all hands plus solution equals the full deck size."""
    state = _make_state()
    total_in_hands = sum(len(p.hand) for p in state.players)
    # Full deck = 6 suspects + 6 weapons + 9 rooms = 21; solution removes 3
    assert total_in_hands == 21 - 3


def test_no_duplicate_cards_in_hands() -> None:
    """F2: No card appears in more than one player's hand."""
    state = _make_state(["Alice", "Bob", "Carol", "Dave"])
    all_cards = [card for p in state.players for card in p.hand]
    names_and_types = [(c.card_type, c.name) for c in all_cards]
    assert len(names_and_types) == len(set(names_and_types)), (
        "Duplicate card found across player hands"
    )


def test_solution_cards_not_in_any_hand() -> None:
    """F2: The three solution cards do not appear in any player's hand."""
    state = _make_state()
    solution_ids = {
        (c.card_type, c.name) for c in state.solution.values()
    }
    for player in state.players:
        for card in player.hand:
            assert (card.card_type, card.name) not in solution_ids, (
                f"Solution card {card} found in {player.name}'s hand"
            )


# ---------------------------------------------------------------------------
# F3 — next_turn() cycles correctly and skips eliminated players
# ---------------------------------------------------------------------------


def test_next_turn_advances_index() -> None:
    """F3: next_turn increments current_turn_index by 1 for active players."""
    state = _make_state()
    assert state.current_turn_index == 0
    next_turn(state)
    assert state.current_turn_index == 1


def test_next_turn_wraps_around() -> None:
    """F3: next_turn wraps back to index 0 after the last player."""
    state = _make_state(["Alice", "Bob", "Carol"])
    state.current_turn_index = 2
    next_turn(state)
    assert state.current_turn_index == 0


def test_next_turn_skips_eliminated_player() -> None:
    """F3: next_turn skips a player whose is_eliminated flag is True."""
    state = _make_state(["Alice", "Bob", "Carol"])
    # Eliminate Bob (index 1) so turn should jump from Alice (0) to Carol (2)
    state.players[1].is_eliminated = True
    state.current_turn_index = 0
    next_turn(state)
    assert state.current_turn_index == 2


def test_next_turn_skips_multiple_eliminated_players() -> None:
    """F3: next_turn skips a run of consecutive eliminated players."""
    state = _make_state(["Alice", "Bob", "Carol", "Dave"])
    # Eliminate Bob and Carol so turn goes Alice -> Dave
    state.players[1].is_eliminated = True
    state.players[2].is_eliminated = True
    state.current_turn_index = 0
    next_turn(state)
    assert state.current_turn_index == 3


# ---------------------------------------------------------------------------
# Deal fairness — hand sizes differ by at most 1
# ---------------------------------------------------------------------------


def test_deal_fairness_three_players() -> None:
    """Hand sizes for 3 players differ by at most 1 card."""
    state = _make_state(["A", "B", "C"])
    sizes = [len(p.hand) for p in state.players]
    assert max(sizes) - min(sizes) <= 1


def test_deal_fairness_six_players() -> None:
    """Hand sizes for 6 players differ by at most 1 card."""
    state = _make_state(["A", "B", "C", "D", "E", "F"])
    sizes = [len(p.hand) for p in state.players]
    assert max(sizes) - min(sizes) <= 1


# ---------------------------------------------------------------------------
# Validation — new_game() rejects invalid player counts
# ---------------------------------------------------------------------------


def test_new_game_rejects_fewer_than_three_players() -> None:
    """new_game raises ValueError for fewer than 3 players."""
    with pytest.raises(ValueError):
        new_game(["Alice", "Bob"])


def test_new_game_rejects_more_than_six_players() -> None:
    """new_game raises ValueError for more than 6 players."""
    with pytest.raises(ValueError):
        new_game(["A", "B", "C", "D", "E", "F", "G"])


def test_new_game_accepts_exactly_three_players() -> None:
    """new_game accepts exactly 3 players without raising."""
    state = new_game(["A", "B", "C"])
    assert len(state.players) == 3


def test_new_game_accepts_exactly_six_players() -> None:
    """new_game accepts exactly 6 players without raising."""
    state = new_game(["A", "B", "C", "D", "E", "F"])
    assert len(state.players) == 6


# ---------------------------------------------------------------------------
# get_current_player
# ---------------------------------------------------------------------------


def test_get_current_player_returns_correct_player() -> None:
    """get_current_player returns the player at current_turn_index."""
    state = _make_state(["Alice", "Bob", "Carol"])
    state.current_turn_index = 1
    assert get_current_player(state).name == "Bob"


# ---------------------------------------------------------------------------
# move_to_room
# ---------------------------------------------------------------------------


def test_move_to_room_valid() -> None:
    """move_to_room sets the player's current_room for a valid room."""
    state = _make_state()
    player = state.players[0]
    move_to_room(state, player, "Kitchen")
    assert player.current_room == "Kitchen"


def test_move_to_room_invalid_raises() -> None:
    """move_to_room raises ValueError for an unrecognised room name."""
    state = _make_state()
    player = state.players[0]
    with pytest.raises(ValueError):
        move_to_room(state, player, "Narnia")


# ---------------------------------------------------------------------------
# make_suggestion
# ---------------------------------------------------------------------------


def test_make_suggestion_finds_refuter() -> None:
    """make_suggestion returns refuted=True when another player holds a match."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    bob = state.players[1]

    # Place a known weapon card in Bob's hand and clear others to avoid noise.
    target_card = Card(card_type="weapon", name="Knife")
    bob.hand = [target_card]

    # Give Alice a room so she can make a suggestion.
    alice.current_room = "Kitchen"

    result = make_suggestion(state, alice, suspect="Miss Scarlet", weapon="Knife")

    assert result.refuted is True
    assert result.refuting_player == "Bob"
    assert result.card_shown == target_card


def test_make_suggestion_no_refuter() -> None:
    """make_suggestion returns refuted=False when no one holds a matching card."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]

    # Clear all other players' hands so no match is possible.
    for p in state.players[1:]:
        p.hand = []

    alice.current_room = "Ballroom"

    result = make_suggestion(state, alice, suspect="Professor Plum", weapon="Wrench")

    assert result.refuted is False
    assert result.refuting_player is None
    assert result.card_shown is None


def test_make_suggestion_requires_room() -> None:
    """make_suggestion raises ValueError if the player is not in a room."""
    state = _make_state()
    player = state.players[0]
    player.current_room = None
    with pytest.raises(ValueError):
        make_suggestion(state, player, suspect="Miss Scarlet", weapon="Knife")


def test_make_suggestion_skips_eliminated_players() -> None:
    """make_suggestion skips eliminated players when looking for a refuter."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    bob = state.players[1]
    carol = state.players[2]

    # Bob has a matching card but is eliminated; Carol has nothing.
    bob.hand = [Card(card_type="weapon", name="Rope")]
    bob.is_eliminated = True
    carol.hand = []

    alice.current_room = "Study"

    result = make_suggestion(state, alice, suspect="Miss Scarlet", weapon="Rope")

    assert result.refuted is False


# ---------------------------------------------------------------------------
# make_accusation
# ---------------------------------------------------------------------------


def test_make_accusation_correct() -> None:
    """make_accusation returns correct=True when all three parts match."""
    state = _make_state()
    player = state.players[0]
    sol = state.solution

    result = make_accusation(
        state,
        player,
        suspect=sol["suspect"].name,
        weapon=sol["weapon"].name,
        room=sol["room"].name,
    )

    assert result.correct is True
    assert player.is_eliminated is False


def test_make_accusation_wrong_eliminates_player() -> None:
    """make_accusation returns correct=False and eliminates the player on a wrong guess."""
    state = _make_state()
    player = state.players[0]
    sol = state.solution

    # Guarantee the weapon is wrong by picking something not in the solution.
    wrong_weapon = next(w for w in WEAPONS if w != sol["weapon"].name)

    result = make_accusation(
        state,
        player,
        suspect=sol["suspect"].name,
        weapon=wrong_weapon,
        room=sol["room"].name,
    )

    assert result.correct is False
    assert player.is_eliminated is True


def test_make_accusation_result_records_player_name_and_guess() -> None:
    """AccusationResult stores the player name and every part of the guess."""
    state = _make_state(["Alice", "Bob", "Carol"])
    player = state.players[0]

    result = make_accusation(
        state, player,
        suspect="Miss Scarlet",
        weapon="Candlestick",
        room="Kitchen",
    )

    assert result.player_name == "Alice"
    assert result.suspect == "Miss Scarlet"
    assert result.weapon == "Candlestick"
    assert result.room == "Kitchen"
