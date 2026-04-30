# tests/test_engine.py
# =====================
# Pytest tests for the game engine (src/game/engine.py).
# Run from the cluedo/ directory with:  pytest

import random

import pytest

from game.deck import ROOMS, SUSPECTS, WEAPONS
from game.deck import create_deck, verify_deck
from game.engine import (
    check_for_winner,
    get_current_player,
    get_game_status,
    get_turn_summary,
    legal_moves_for_roll,
    make_accusation,
    make_suggestion,
    move_by_dice,
    move_to_room,
    new_game,
    next_turn,
    reset_game,
    validate_game_state,
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


def test_make_suggestion_allows_eliminated_players_to_refute() -> None:
    """Eliminated players can still show cards when refuting a suggestion."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    bob = state.players[1]
    carol = state.players[2]

    # Bob has a matching card and is eliminated; he should still refute.
    bob.hand = [Card(card_type="weapon", name="Rope")]
    bob.is_eliminated = True
    carol.hand = []

    alice.current_room = "Study"

    result = make_suggestion(state, alice, suspect="Miss Scarlet", weapon="Rope")

    assert result.refuted is True
    assert result.refuting_player == "Bob"
    assert result.card_shown == bob.hand[0]


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


# ---------------------------------------------------------------------------
# Sprint 2 — suggestion guards
# ---------------------------------------------------------------------------


def test_suggestion_requires_room() -> None:
    """make_suggestion raises ValueError when player.current_room is None."""
    state = _make_state()
    player = state.players[0]
    player.current_room = None
    with pytest.raises(ValueError):
        make_suggestion(state, player, suspect="Miss Scarlet", weapon="Knife")


def test_suggestion_uses_current_room() -> None:
    """make_suggestion uses the player's current_room, not a passed-in room."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    bob = state.players[1]

    alice.current_room = "Kitchen"
    # Bob holds the Kitchen room card — it should be matched via alice.current_room.
    bob.hand = [Card(card_type="room", name="Kitchen")]

    result = make_suggestion(state, alice, suspect="Professor Plum", weapon="Wrench")

    assert result.refuted is True
    assert result.card_shown is not None
    assert result.card_shown.name == "Kitchen"


# ---------------------------------------------------------------------------
# Sprint 2 — refutation order and elimination interaction
# ---------------------------------------------------------------------------


def test_refutation_turn_order() -> None:
    """Refutation checks players in turn order starting immediately after the suggester."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    bob = state.players[1]
    carol = state.players[2]

    alice.current_room = "Ballroom"
    # Both Bob and Carol hold a matching card; Bob comes first — he should refute.
    bob.hand = [Card(card_type="weapon", name="Rope")]
    carol.hand = [Card(card_type="weapon", name="Rope")]

    result = make_suggestion(state, alice, suspect="Miss Scarlet", weapon="Rope")

    assert result.refuted is True
    assert result.refuting_player == "Bob"


def test_refutation_includes_eliminated_players_in_turn_order() -> None:
    """Eliminated players keep refuting but remain skipped for normal turns."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    bob = state.players[1]
    carol = state.players[2]

    alice.current_room = "Library"
    # Bob is eliminated and holds a match; Carol also holds a match.
    bob.hand = [Card(card_type="weapon", name="Knife")]
    bob.is_eliminated = True
    carol.hand = [Card(card_type="weapon", name="Knife")]

    result = make_suggestion(state, alice, suspect="Colonel Mustard", weapon="Knife")

    assert result.refuted is True
    assert result.refuting_player == "Bob"


def test_eliminated_cards_still_refute() -> None:
    """An eliminated player's hand is preserved (cards not cleared on elimination).

    Eliminated players are skipped for normal turns, but their cards remain
    available for suggestion refutation and state inspection.
    """
    state = _make_state(["Alice", "Bob", "Carol"])
    bob = state.players[1]

    knife = Card(card_type="weapon", name="Knife")
    bob.hand = [knife]

    # Advance to Bob's turn, then eliminate Bob via a wrong accusation.
    next_turn(state)  # Alice -> Bob
    sol = state.solution
    wrong_weapon = next(w for w in WEAPONS if w != sol["weapon"].name)
    make_accusation(
        state, bob,
        suspect=sol["suspect"].name,
        weapon=wrong_weapon,
        room=sol["room"].name,
    )

    assert bob.is_eliminated is True
    # Card must still be present in the hand after elimination.
    assert knife in bob.hand


# ---------------------------------------------------------------------------
# Sprint 2 — eliminated-player action guards
# ---------------------------------------------------------------------------


def test_eliminated_cannot_suggest() -> None:
    """An eliminated player raises ValueError when attempting to make a suggestion."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    alice.current_room = "Kitchen"
    alice.is_eliminated = True

    with pytest.raises(ValueError):
        make_suggestion(state, alice, suspect="Miss Scarlet", weapon="Knife")


def test_eliminated_cannot_accuse() -> None:
    """An eliminated player raises ValueError when attempting to make an accusation."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    alice.is_eliminated = True

    with pytest.raises(ValueError):
        make_accusation(
            state, alice,
            suspect="Miss Scarlet",
            weapon="Knife",
            room="Kitchen",
        )


# ---------------------------------------------------------------------------
# Sprint 2 — accusation outcomes (game_over / winner)
# ---------------------------------------------------------------------------


def test_correct_accusation_ends_game() -> None:
    """A correct accusation sets game_over=True and records the winner."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    sol = state.solution

    result = make_accusation(
        state, alice,
        suspect=sol["suspect"].name,
        weapon=sol["weapon"].name,
        room=sol["room"].name,
    )

    assert result.correct is True
    assert state.game_over is True
    assert state.winner == "Alice"


def test_wrong_accusation_eliminates() -> None:
    """A wrong accusation sets player.is_eliminated without ending the game."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    sol = state.solution

    wrong_suspect = next(s for s in SUSPECTS if s != sol["suspect"].name)
    result = make_accusation(
        state, alice,
        suspect=wrong_suspect,
        weapon=sol["weapon"].name,
        room=sol["room"].name,
    )

    assert result.correct is False
    assert alice.is_eliminated is True
    assert state.game_over is False
    assert state.winner is None


# ---------------------------------------------------------------------------
# Sprint 2 — last player standing
# ---------------------------------------------------------------------------


def test_last_player_standing_wins() -> None:
    """check_for_winner returns the sole active player and sets game_over."""
    state = _make_state(["Alice", "Bob", "Carol"])
    sol = state.solution
    wrong_weapon = next(w for w in WEAPONS if w != sol["weapon"].name)

    # Advance past Alice to Bob, then eliminate Bob and Carol in turn order.
    next_turn(state)  # Alice -> Bob (index 1)
    make_accusation(state, state.players[1], suspect=sol["suspect"].name,
                    weapon=wrong_weapon, room=sol["room"].name)
    # auto-advance: Bob eliminated -> Carol (index 2)
    make_accusation(state, state.players[2], suspect=sol["suspect"].name,
                    weapon=wrong_weapon, room=sol["room"].name)
    # auto-advance: Carol eliminated -> Alice (index 0)

    winner = check_for_winner(state)

    assert winner is not None
    assert winner.name == "Alice"
    assert state.game_over is True
    assert state.winner == "Alice"


# ---------------------------------------------------------------------------
# Sprint 2 — get_game_status
# ---------------------------------------------------------------------------


def test_get_game_status_during_play() -> None:
    """get_game_status returns correct dict while the game is in progress."""
    state = _make_state(["Alice", "Bob", "Carol"])

    status = get_game_status(state)

    assert status["current_player"] == "Alice"
    assert status["players_remaining"] == 3
    assert status["game_over"] is False
    assert status["winner"] is None


def test_get_game_status_after_win() -> None:
    """get_game_status reflects the ended state after a correct accusation."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    sol = state.solution

    make_accusation(
        state, alice,
        suspect=sol["suspect"].name,
        weapon=sol["weapon"].name,
        room=sol["room"].name,
    )

    status = get_game_status(state)

    assert status["game_over"] is True
    assert status["winner"] == "Alice"


# ---------------------------------------------------------------------------
# Sprint 2 — multi-elimination and full simulation
# ---------------------------------------------------------------------------


def test_multiple_wrong_accusations() -> None:
    """Multiple players can be eliminated sequentially; game_over stays False until a win."""
    state = _make_state(["Alice", "Bob", "Carol", "Dave"])
    sol = state.solution
    wrong_weapon = next(w for w in WEAPONS if w != sol["weapon"].name)

    make_accusation(state, state.players[0], suspect=sol["suspect"].name,
                    weapon=wrong_weapon, room=sol["room"].name)
    make_accusation(state, state.players[1], suspect=sol["suspect"].name,
                    weapon=wrong_weapon, room=sol["room"].name)
    make_accusation(state, state.players[2], suspect=sol["suspect"].name,
                    weapon=wrong_weapon, room=sol["room"].name)

    assert state.players[0].is_eliminated is True
    assert state.players[1].is_eliminated is True
    assert state.players[2].is_eliminated is True
    assert state.players[3].is_eliminated is False
    assert state.game_over is False  # Dave hasn't won yet — no correct accusation


def test_full_game_simulation() -> None:
    """Simulate a complete game: setup → moves → suggestions → correct accusation."""
    state = new_game(["Alice", "Bob", "Carol"])
    sol = state.solution

    assert state.started is True
    assert state.game_over is False
    assert len(state.players) == 3

    # --- Turn 1: Alice moves and makes a suggestion ---
    alice = get_current_player(state)
    assert alice.name == "Alice"

    move_to_room(state, alice, sol["room"].name)
    assert alice.current_room == sol["room"].name

    suggestion = make_suggestion(
        state, alice,
        suspect=sol["suspect"].name,
        weapon=sol["weapon"].name,
    )
    assert isinstance(suggestion.refuted, bool)

    next_turn(state)

    # --- Turn 2: Bob moves and makes a wrong accusation ---
    bob = get_current_player(state)
    assert bob.name == "Bob"

    wrong_weapon = next(w for w in WEAPONS if w != sol["weapon"].name)
    result_bob = make_accusation(
        state, bob,
        suspect=sol["suspect"].name,
        weapon=wrong_weapon,
        room=sol["room"].name,
    )
    assert result_bob.correct is False
    assert bob.is_eliminated is True
    assert state.game_over is False
    # make_accusation auto-advances the turn to Carol

    # --- Turn 3: Carol makes a correct accusation ---
    carol = get_current_player(state)
    assert carol.name == "Carol"

    result_carol = make_accusation(
        state, carol,
        suspect=sol["suspect"].name,
        weapon=sol["weapon"].name,
        room=sol["room"].name,
    )
    assert result_carol.correct is True
    assert state.game_over is True
    assert state.winner == "Carol"

    status = get_game_status(state)
    assert status["game_over"] is True
    assert status["winner"] == "Carol"
    assert status["players_remaining"] == 2  # Alice and Carol still active


# ---------------------------------------------------------------------------
# Sprint 3 — input validation: suspects, weapons, rooms
# ---------------------------------------------------------------------------


def test_invalid_suspect_in_suggestion() -> None:
    """make_suggestion raises ValueError for an unrecognised suspect name."""
    state = _make_state()
    player = state.players[0]
    player.current_room = "Kitchen"
    with pytest.raises(ValueError, match="suspect"):
        make_suggestion(state, player, suspect="Not A Suspect", weapon="Knife")


def test_invalid_weapon_in_suggestion() -> None:
    """make_suggestion raises ValueError for an unrecognised weapon name."""
    state = _make_state()
    player = state.players[0]
    player.current_room = "Kitchen"
    with pytest.raises(ValueError, match="weapon"):
        make_suggestion(state, player, suspect="Miss Scarlet", weapon="Bazooka")


def test_invalid_suspect_in_accusation() -> None:
    """make_accusation raises ValueError for an unrecognised suspect name."""
    state = _make_state()
    player = state.players[0]
    with pytest.raises(ValueError, match="suspect"):
        make_accusation(state, player, suspect="Nobody", weapon="Knife", room="Kitchen")


def test_invalid_weapon_in_accusation() -> None:
    """make_accusation raises ValueError for an unrecognised weapon name."""
    state = _make_state()
    player = state.players[0]
    with pytest.raises(ValueError, match="weapon"):
        make_accusation(state, player, suspect="Miss Scarlet", weapon="Tank", room="Kitchen")


def test_invalid_room_in_accusation() -> None:
    """make_accusation raises ValueError for an unrecognised room name."""
    state = _make_state()
    player = state.players[0]
    with pytest.raises(ValueError, match="room"):
        make_accusation(state, player, suspect="Miss Scarlet", weapon="Knife", room="Narnia")


# ---------------------------------------------------------------------------
# Sprint 3 — new_game() name validation
# ---------------------------------------------------------------------------


def test_duplicate_player_names() -> None:
    """new_game raises ValueError when duplicate player names are supplied."""
    with pytest.raises(ValueError):
        new_game(["Alice", "Alice", "Carol"])


def test_empty_player_name() -> None:
    """new_game raises ValueError when any player name is an empty string."""
    with pytest.raises(ValueError):
        new_game(["Alice", "", "Carol"])


# ---------------------------------------------------------------------------
# Sprint 3 — turn-order enforcement
# ---------------------------------------------------------------------------


def test_wrong_turn_suggestion() -> None:
    """make_suggestion raises ValueError when called by a player who is not current."""
    state = _make_state(["Alice", "Bob", "Carol"])
    bob = state.players[1]
    bob.current_room = "Kitchen"
    # Turn is Alice's (index 0); Bob acts out of turn.
    with pytest.raises(ValueError):
        make_suggestion(state, bob, suspect="Miss Scarlet", weapon="Knife")


def test_wrong_turn_accusation() -> None:
    """make_accusation raises ValueError when called by a player who is not current."""
    state = _make_state(["Alice", "Bob", "Carol"])
    bob = state.players[1]
    sol = state.solution
    # Turn is Alice's (index 0); Bob acts out of turn.
    with pytest.raises(ValueError):
        make_accusation(state, bob, suspect=sol["suspect"].name,
                        weapon=sol["weapon"].name, room=sol["room"].name)


def test_wrong_turn_move() -> None:
    """move_to_room raises ValueError when called by a player who is not current."""
    state = _make_state(["Alice", "Bob", "Carol"])
    bob = state.players[1]
    # Turn is Alice's (index 0); Bob acts out of turn.
    with pytest.raises(ValueError):
        move_to_room(state, bob, "Kitchen")


# ---------------------------------------------------------------------------
# Sprint 3 — action after game over
# ---------------------------------------------------------------------------


def test_action_after_game_over() -> None:
    """Any action after game_over=True raises ValueError('Game is already over')."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    sol = state.solution

    make_accusation(state, alice,
                    suspect=sol["suspect"].name,
                    weapon=sol["weapon"].name,
                    room=sol["room"].name)
    assert state.game_over is True

    # After auto-advance it is now Bob's turn; all actions should be blocked.
    bob = state.players[1]
    with pytest.raises(ValueError, match="already over"):
        make_accusation(state, bob,
                        suspect=sol["suspect"].name,
                        weapon=sol["weapon"].name,
                        room=sol["room"].name)


# ---------------------------------------------------------------------------
# Sprint 3 — draw: all players eliminated
# ---------------------------------------------------------------------------


def test_all_players_eliminated_draw() -> None:
    """game_over=True and winner=None when every player makes a wrong accusation."""
    state = _make_state(["Alice", "Bob", "Carol"])
    sol = state.solution
    wrong_weapon = next(w for w in WEAPONS if w != sol["weapon"].name)

    # Accusations in strict turn order; auto-advance moves to next player each time.
    make_accusation(state, state.players[0], suspect=sol["suspect"].name,
                    weapon=wrong_weapon, room=sol["room"].name)
    make_accusation(state, state.players[1], suspect=sol["suspect"].name,
                    weapon=wrong_weapon, room=sol["room"].name)
    make_accusation(state, state.players[2], suspect=sol["suspect"].name,
                    weapon=wrong_weapon, room=sol["room"].name)

    assert state.game_over is True
    assert state.winner is None


# ---------------------------------------------------------------------------
# Sprint 3 — turn-advance behaviour
# ---------------------------------------------------------------------------


def test_auto_advance_after_accusation() -> None:
    """Turn automatically advances to the next player after any accusation."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    sol = state.solution
    wrong_weapon = next(w for w in WEAPONS if w != sol["weapon"].name)

    assert state.current_turn_index == 0
    make_accusation(state, alice,
                    suspect=sol["suspect"].name,
                    weapon=wrong_weapon,
                    room=sol["room"].name)
    assert state.current_turn_index == 1
    assert get_current_player(state).name == "Bob"


def test_no_advance_after_suggestion() -> None:
    """Turn does NOT advance after a suggestion — the player may still accuse."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    alice.current_room = "Kitchen"

    assert state.current_turn_index == 0
    make_suggestion(state, alice, suspect="Miss Scarlet", weapon="Knife")
    assert state.current_turn_index == 0


# ---------------------------------------------------------------------------
# Sprint 3 — player-count edge cases
# ---------------------------------------------------------------------------


def test_three_player_game() -> None:
    """Full game flow works correctly with the minimum of 3 players."""
    state = new_game(["Alice", "Bob", "Carol"])
    assert len(state.players) == 3
    assert state.started is True

    alice = get_current_player(state)
    sol = state.solution
    move_to_room(state, alice, sol["room"].name)
    result = make_suggestion(state, alice, suspect=sol["suspect"].name, weapon=sol["weapon"].name)
    assert isinstance(result.refuted, bool)


def test_six_player_game() -> None:
    """Game setup works correctly with the maximum of 6 players."""
    names = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank"]
    state = new_game(names)
    assert len(state.players) == 6
    assert state.started is True
    sizes = [len(p.hand) for p in state.players]
    assert max(sizes) - min(sizes) <= 1


# ---------------------------------------------------------------------------
# Sprint 3 — get_turn_summary
# ---------------------------------------------------------------------------


def test_get_turn_summary_in_room() -> None:
    """get_turn_summary includes 'suggest' in available_actions when player is in a room."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    alice.current_room = "Kitchen"

    summary = get_turn_summary(state)

    assert summary["player_name"] == "Alice"
    assert "suggest" in summary["available_actions"]
    assert "move" in summary["available_actions"]
    assert "accuse" in summary["available_actions"]
    assert summary["room"] == "Kitchen"
    assert summary["is_eliminated"] is False
    assert isinstance(summary["cards_in_hand"], int)


def test_get_turn_summary_not_in_room() -> None:
    """get_turn_summary omits 'suggest' when the current player has no room."""
    state = _make_state(["Alice", "Bob", "Carol"])
    # Alice starts with no room.

    summary = get_turn_summary(state)

    assert summary["player_name"] == "Alice"
    assert "suggest" not in summary["available_actions"]
    assert summary["room"] is None


# ---------------------------------------------------------------------------
# Sprint 3 — turn history logging
# ---------------------------------------------------------------------------


def test_turn_history_records_actions() -> None:
    """turn_history accumulates an entry for each move and suggestion."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]

    assert len(state.turn_history) == 0

    move_to_room(state, alice, "Kitchen")
    assert len(state.turn_history) == 1
    assert state.turn_history[0]["action"] == "move"
    assert state.turn_history[0]["player"] == "Alice"

    make_suggestion(state, alice, suspect="Miss Scarlet", weapon="Knife")
    assert len(state.turn_history) == 2
    assert state.turn_history[1]["action"] == "suggestion"


# ---------------------------------------------------------------------------
# Sprint 3 — reset_game
# ---------------------------------------------------------------------------


def test_reset_game() -> None:
    """reset_game returns a fresh GameState with the same player names."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    move_to_room(state, alice, "Kitchen")

    fresh = reset_game(["Alice", "Bob", "Carol"])

    assert fresh.started is True
    assert len(fresh.players) == 3
    assert fresh.game_over is False
    assert fresh.winner is None
    assert len(fresh.turn_history) == 0
    assert fresh.players[0].current_room is None
    assert fresh.players[0].name == "Alice"


# ---------------------------------------------------------------------------
# Sprint 4 — verify_deck
# ---------------------------------------------------------------------------


def test_verify_deck() -> None:
    """verify_deck returns True for a freshly created deck."""
    deck = create_deck()
    assert verify_deck(deck) is True


def test_verify_deck_wrong_count() -> None:
    """verify_deck raises ValueError when a card is missing from the deck."""
    deck = create_deck()
    deck.pop()
    with pytest.raises(ValueError):
        verify_deck(deck)


# ---------------------------------------------------------------------------
# Sprint 4 — validate_game_state
# ---------------------------------------------------------------------------


def test_validate_game_state_valid() -> None:
    """validate_game_state returns True for a freshly created game."""
    state = _make_state()
    assert validate_game_state(state) is True


def test_validate_game_state_missing_cards() -> None:
    """validate_game_state raises ValueError when total card count is not 21."""
    state = _make_state()
    state.players[0].hand.pop()
    with pytest.raises(ValueError, match="21"):
        validate_game_state(state)


def test_validate_game_state_duplicate_cards() -> None:
    """validate_game_state raises ValueError when a card appears more than once."""
    state = _make_state()
    # Replace a card in player[1]'s hand with an identical copy of player[0]'s first card,
    # keeping the total at 21 so only the duplicate check triggers.
    original = state.players[0].hand[0]
    state.players[1].hand[0] = Card(card_type=original.card_type, name=original.name)
    with pytest.raises(ValueError, match="[Dd]uplicate"):
        validate_game_state(state)


def test_validate_game_state_bad_solution() -> None:
    """validate_game_state raises ValueError when the solution is missing a key."""
    state = _make_state()
    del state.solution["room"]
    with pytest.raises(ValueError):
        validate_game_state(state)


def test_validate_game_state_bad_turn_index() -> None:
    """validate_game_state raises ValueError when current_turn_index is out of bounds."""
    state = _make_state()
    state.current_turn_index = 99
    with pytest.raises(ValueError, match="out of bounds"):
        validate_game_state(state)


# ---------------------------------------------------------------------------
# Sprint 4 — accusation on first turn
# ---------------------------------------------------------------------------


def test_accusation_on_first_turn() -> None:
    """A correct accusation on the very first turn wins immediately."""
    state = _make_state()
    player = state.players[0]
    sol = state.solution

    result = make_accusation(
        state, player,
        suspect=sol["suspect"].name,
        weapon=sol["weapon"].name,
        room=sol["room"].name,
    )

    assert result.correct is True
    assert state.game_over is True
    assert state.winner == player.name


# ---------------------------------------------------------------------------
# Sprint 4 — suggestion edge cases
# ---------------------------------------------------------------------------


def test_suggestion_no_refutation() -> None:
    """make_suggestion returns refuted=False when no active player holds a matching card."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    for p in state.players[1:]:
        p.hand = []
    alice.current_room = "Dining Room"

    result = make_suggestion(state, alice, suspect="Professor Plum", weapon="Wrench")

    assert result.refuted is False
    assert result.refuting_player is None
    assert result.card_shown is None


def test_suggestion_last_player_refutes() -> None:
    """Refutation succeeds when only the last player checked (in turn order) holds a match."""
    state = _make_state(["Alice", "Bob", "Carol"])
    alice = state.players[0]
    bob = state.players[1]
    carol = state.players[2]

    bob.hand = []
    carol.hand = [Card(card_type="weapon", name="Rope")]
    alice.current_room = "Lounge"

    result = make_suggestion(state, alice, suspect="Miss Scarlet", weapon="Rope")

    assert result.refuted is True
    assert result.refuting_player == "Carol"


# ---------------------------------------------------------------------------
# Sprint 4 — all player counts work
# ---------------------------------------------------------------------------


def test_all_player_counts_work() -> None:
    """new_game initialises correctly for every valid player count (3–6)."""
    for count in [3, 4, 5, 6]:
        names = [chr(65 + i) for i in range(count)]
        state = new_game(names)
        assert len(state.players) == count
        assert state.started is True
        total_cards = sum(len(p.hand) for p in state.players)
        assert total_cards == 18  # 21 total − 3 solution cards


# ---------------------------------------------------------------------------
# Sprint 4 — full game regression
# ---------------------------------------------------------------------------


def test_full_game_regression() -> None:
    """End-to-end regression: 4-player game from setup through to a decisive win."""
    names = ["Alice", "Bob", "Carol", "Dave"]
    state = new_game(names)
    sol = state.solution

    assert state.started is True
    assert state.game_over is False
    assert state.winner is None
    assert len(state.players) == 4
    assert sum(len(p.hand) for p in state.players) == 18

    wrong_weapon = next(w for w in WEAPONS if w != sol["weapon"].name)

    # Turn 1: Alice moves to the solution room and makes a suggestion.
    alice = get_current_player(state)
    assert alice.name == "Alice"
    move_to_room(state, alice, sol["room"].name)
    suggestion = make_suggestion(
        state, alice,
        suspect=sol["suspect"].name,
        weapon=sol["weapon"].name,
    )
    assert isinstance(suggestion.refuted, bool)
    assert len(state.turn_history) == 2  # move + suggestion
    next_turn(state)

    # Turn 2: Bob makes a wrong accusation and is eliminated.
    bob = get_current_player(state)
    assert bob.name == "Bob"
    result_bob = make_accusation(
        state, bob,
        suspect=sol["suspect"].name,
        weapon=wrong_weapon,
        room=sol["room"].name,
    )
    assert result_bob.correct is False
    assert bob.is_eliminated is True
    assert state.game_over is False

    # Turn 3 (auto-advanced to Carol): Carol makes a wrong accusation and is eliminated.
    carol = get_current_player(state)
    assert carol.name == "Carol"
    result_carol = make_accusation(
        state, carol,
        suspect=sol["suspect"].name,
        weapon=wrong_weapon,
        room=sol["room"].name,
    )
    assert result_carol.correct is False
    assert carol.is_eliminated is True
    assert state.game_over is False

    # Turn 4 (auto-advanced to Dave): Dave makes the correct accusation and wins.
    dave = get_current_player(state)
    assert dave.name == "Dave"
    result_dave = make_accusation(
        state, dave,
        suspect=sol["suspect"].name,
        weapon=sol["weapon"].name,
        room=sol["room"].name,
    )
    assert result_dave.correct is True
    assert state.game_over is True
    assert state.winner == "Dave"

    status = get_game_status(state)
    assert status["game_over"] is True
    assert status["winner"] == "Dave"
    assert status["players_remaining"] == 2  # Alice and Dave still active


# ---------------------------------------------------------------------------
# Sprint 3 closure — F12 (domain): suggested suspect & weapon tokens move
# into the suggester's current room and STAY there after refutation.
# ---------------------------------------------------------------------------


def test_f12_suspect_token_moves_into_suggesters_room() -> None:
    """F12: a suggested suspect token is placed in the suggester's room."""
    state = new_game(["Alice", "Bob", "Carol"], seed=42)
    alice = state.players[0]
    alice.current_room = "Kitchen"

    make_suggestion(state, alice, suspect="Miss Scarlet", weapon="Knife")

    assert state.suspect_locations["Miss Scarlet"] == "Kitchen"


def test_f12_weapon_token_moves_into_suggesters_room() -> None:
    """F12: a suggested weapon token is placed in the suggester's room."""
    state = new_game(["Alice", "Bob", "Carol"], seed=42)
    alice = state.players[0]
    alice.current_room = "Library"

    make_suggestion(state, alice, suspect="Miss Scarlet", weapon="Rope")

    assert state.weapon_locations["Rope"] == "Library"


def test_f12_tokens_stay_after_refutation() -> None:
    """F12: tokens stay in the suggester's room even after a refuter shows a card."""
    state = new_game(["Alice", "Bob", "Carol"], seed=42)
    alice = state.players[0]
    bob = state.players[1]
    # Bob holds Knife so refutation will succeed.
    bob.hand = [Card(card_type="weapon", name="Knife")]
    alice.current_room = "Ballroom"

    result = make_suggestion(state, alice, suspect="Miss Scarlet", weapon="Knife")

    assert result.refuted is True
    # Tokens remain in Ballroom regardless of refutation outcome.
    assert state.suspect_locations["Miss Scarlet"] == "Ballroom"
    assert state.weapon_locations["Knife"] == "Ballroom"


def test_f12_token_locations_initialised_for_every_card() -> None:
    """F12: every suspect and weapon name is keyed in the location dicts at setup."""
    state = new_game(["Alice", "Bob", "Carol"], seed=42)
    assert set(state.suspect_locations.keys()) == set(SUSPECTS)
    assert set(state.weapon_locations.keys()) == set(WEAPONS)
    # All start unplaced.
    assert all(v is None for v in state.suspect_locations.values())
    assert all(v is None for v in state.weapon_locations.values())


# ---------------------------------------------------------------------------
# Sprint 3 closure — seeded reproducibility (§4.3 of CLAUDE.md)
# ---------------------------------------------------------------------------


def test_seeded_reproducibility() -> None:
    """new_game with the same seed produces identical solution, deals, and turn order."""
    s1 = new_game(["Alice", "Bob", "Carol"], seed=12345)
    s2 = new_game(["Alice", "Bob", "Carol"], seed=12345)

    # Solution identical (suspect / weapon / room).
    for k in ("suspect", "weapon", "room"):
        assert s1.solution[k].card_type == s2.solution[k].card_type
        assert s1.solution[k].name == s2.solution[k].name

    # Hands dealt identically, in the same order.
    for p1, p2 in zip(s1.players, s2.players):
        h1 = [(c.card_type, c.name) for c in p1.hand]
        h2 = [(c.card_type, c.name) for c in p2.hand]
        assert h1 == h2

    # Turn order is identical (player names are in the same slots).
    assert [p.name for p in s1.players] == [p.name for p in s2.players]
    assert s1.current_turn_index == s2.current_turn_index


def test_unseeded_games_can_diverge() -> None:
    """Without a seed, two games shouldn't all produce the same solution."""
    runs = [new_game(["Alice", "Bob", "Carol"]) for _ in range(8)]
    seen = {(s.solution["suspect"].name,
             s.solution["weapon"].name,
             s.solution["room"].name) for s in runs}
    assert len(seen) > 1, "8 unseeded games all produced the same solution"


# ---------------------------------------------------------------------------
# Sprint 3 closure — §5 contract: Card-typed signatures accepted
# ---------------------------------------------------------------------------


def test_card_typed_signatures_accepted_for_suggestion() -> None:
    """make_suggestion accepts Card instances as well as strings."""
    state = new_game(["Alice", "Bob", "Carol"], seed=42)
    alice = state.players[0]
    alice.current_room = "Kitchen"

    suspect_card = Card(card_type="suspect", name="Miss Scarlet")
    weapon_card = Card(card_type="weapon", name="Knife")

    result = make_suggestion(state, alice, suspect=suspect_card, weapon=weapon_card)

    # Returned a RefuteResult of either polarity (we don't care which).
    assert isinstance(result.refuted, bool)
    # F12 placement still happens when Card instances are passed.
    assert state.suspect_locations["Miss Scarlet"] == "Kitchen"
    assert state.weapon_locations["Knife"] == "Kitchen"


def test_card_typed_signatures_accepted_for_accusation() -> None:
    """make_accusation accepts Card instances per the §5 contract."""
    state = new_game(["Alice", "Bob", "Carol"], seed=42)
    alice = state.players[0]
    sol = state.solution

    suspect_card = Card(card_type="suspect", name=sol["suspect"].name)
    weapon_card = Card(card_type="weapon", name=sol["weapon"].name)
    room_card = Card(card_type="room", name=sol["room"].name)

    result = make_accusation(
        state, alice,
        suspect=suspect_card,
        weapon=weapon_card,
        room=room_card,
    )

    assert result.correct is True
    assert state.winner == "Alice"


def test_card_with_wrong_card_type_rejected() -> None:
    """Passing a Card with the wrong card_type to a slot is a clear error."""
    state = new_game(["Alice", "Bob", "Carol"], seed=42)
    alice = state.players[0]
    alice.current_room = "Kitchen"

    # A weapon card in the suspect slot is a programming error; reject it.
    wrong = Card(card_type="weapon", name="Knife")
    with pytest.raises(ValueError, match="suspect"):
        make_suggestion(state, alice, suspect=wrong, weapon="Rope")


# ---------------------------------------------------------------------------
# Dice fairness — F4 / NF2
# ---------------------------------------------------------------------------

def test_roll_die_fairness_seeded() -> None:
    """6000 seeded rolls of roll_die produce a fair-six distribution.

    Per-face count must be within 5 sigma of the expected 1000
    (sigma = sqrt(6000 * 1/6 * 5/6) ~= 28.87, so 5 sigma ~= 144).
    The chi-squared statistic across the six faces must fall below
    20.515, the 0.999 quantile of chi-squared with 5 degrees of
    freedom — a tighter cross-check that catches bias the per-bin
    bound would miss.

    Uses a seeded random.Random so the assertion is deterministic
    and zero-flakiness across runs.
    """
    from game.engine import roll_die

    rng = random.Random(20260430)
    rolls = 6000
    counts: dict[int, int] = {face: 0 for face in range(1, 7)}
    for _ in range(rolls):
        face = roll_die(rng)
        assert 1 <= face <= 6
        counts[face] += 1

    expected = rolls / 6  # 1000.0
    for face, observed in counts.items():
        assert abs(observed - expected) <= 145, (
            f"face {face} count {observed} more than 5 sigma from {expected}"
        )

    chi_squared = sum(
        (observed - expected) ** 2 / expected for observed in counts.values()
    )
    assert chi_squared < 20.515, (
        f"chi-squared {chi_squared:.3f} exceeds 0.999 quantile 20.515"
    )


# ---------------------------------------------------------------------------
# Dice-once-per-turn invariant — F4 (engine guard)
# ---------------------------------------------------------------------------


def _pick_dice_destination(state: GameState, player: Player, dice_roll: int):
    """Return any legal destination for this roll (prefers a tile, then a room).

    Helper for the dice-once-per-turn tests below — keeps the assertion
    code focused on the invariant rather than board geometry.
    """
    legal = legal_moves_for_roll(state, player, dice_roll)
    if legal["tiles"]:
        return legal["tiles"][0]
    if legal["rooms"]:
        return legal["rooms"][0]
    raise AssertionError(
        f"no legal moves for {player.name} with dice_roll={dice_roll}"
    )


def test_cannot_roll_twice_in_one_turn() -> None:
    """A player cannot call move_by_dice twice in the same turn.

    The engine tracks has_rolled_this_turn on GameState; the second
    move_by_dice before next_turn must raise ValueError.
    """
    state = new_game(["Alice", "Bob", "Carol"], seed=42)
    alice = state.players[0]

    dice_roll = 3
    first_destination = _pick_dice_destination(state, alice, dice_roll)
    move_by_dice(state, alice, dice_roll, first_destination)
    assert state.has_rolled_this_turn is True

    with pytest.raises(ValueError) as excinfo:
        move_by_dice(state, alice, dice_roll, first_destination)
    assert "already rolled" in str(excinfo.value).lower()


def test_can_roll_again_after_next_turn() -> None:
    """next_turn clears has_rolled_this_turn so the new player can roll."""
    state = new_game(["Alice", "Bob", "Carol"], seed=42)
    alice = state.players[0]

    dice_roll = 3
    first_destination = _pick_dice_destination(state, alice, dice_roll)
    move_by_dice(state, alice, dice_roll, first_destination)

    next_turn(state)
    assert state.has_rolled_this_turn is False

    bob = get_current_player(state)
    assert bob.name == "Bob"
    second_destination = _pick_dice_destination(state, bob, dice_roll)
    move_by_dice(state, bob, dice_roll, second_destination)
    assert state.has_rolled_this_turn is True
