import random

from game.ai import (
    RandomAIPlayerStrategy,
    choose_refutation_card,
    is_ai_player,
    record_suggestion_result,
    run_ai_simulation,
    take_ai_turn,
)
from game.deck import ROOMS, SUSPECTS, WEAPONS
from game.engine import get_current_player, make_accusation, new_game
from game.models import AI_PLAYER, HUMAN_PLAYER, Card, RefuteResult


def test_new_game_marks_ai_players_and_initialises_private_notes() -> None:
    state = new_game(
        ["Human", "AI 1", "AI 2"],
        seed=1,
        player_types=[HUMAN_PLAYER, AI_PLAYER, AI_PLAYER],
    )

    assert state.players[0].player_type == HUMAN_PLAYER
    assert state.players[0].ai_notes is None
    assert is_ai_player(state.players[1])
    assert state.players[1].ai_notes is not None

    ai_player = state.players[1]
    owned = {(card.card_type, card.name) for card in ai_player.hand}
    assert owned <= ai_player.ai_notes.owned_cards
    assert owned <= ai_player.ai_notes.known_not_in_envelope


def test_ai_dice_rolls_are_one_to_six() -> None:
    strategy = RandomAIPlayerStrategy(random.Random(4))

    rolls = [strategy.roll_die() for _ in range(100)]

    assert all(1 <= roll <= 6 for roll in rolls)
    assert set(rolls) <= {1, 2, 3, 4, 5, 6}


def test_ai_can_take_full_turn_without_crashing() -> None:
    state = new_game(
        ["AI", "Bob", "Carol"],
        seed=2,
        player_types=[AI_PLAYER, HUMAN_PLAYER, HUMAN_PLAYER],
    )

    result = take_ai_turn(state, RandomAIPlayerStrategy(random.Random(2)))

    assert result.player_name == "AI"
    assert result.dice_roll is not None
    assert result.moved_to in ROOMS
    assert result.suggestion is not None
    assert result.suggestion["room"] == result.moved_to
    assert get_current_player(state).name == "Bob"


def test_ai_uses_only_legal_room_moves() -> None:
    state = new_game(
        ["AI", "Bob", "Carol"],
        seed=3,
        player_types=[AI_PLAYER, HUMAN_PLAYER, HUMAN_PLAYER],
    )

    result = take_ai_turn(state, RandomAIPlayerStrategy(random.Random(3)))

    assert result.moved_to in ROOMS
    assert state.players[0].current_room in ROOMS


def test_ai_suggestion_uses_current_room() -> None:
    state = new_game(
        ["AI", "Bob", "Carol"],
        seed=4,
        player_types=[AI_PLAYER, HUMAN_PLAYER, HUMAN_PLAYER],
    )

    result = take_ai_turn(state, RandomAIPlayerStrategy(random.Random(4)))

    assert result.suggestion is not None
    assert result.suggestion["room"] == state.players[0].current_room


def test_ai_refutation_shows_one_matching_card() -> None:
    player = new_game(["A", "B", "C"], seed=5).players[0]
    knife = Card("weapon", "Knife")
    kitchen = Card("room", "Kitchen")
    player.hand = [knife, kitchen, Card("suspect", "Professor Plum")]

    shown = choose_refutation_card(
        player,
        suspect="Miss Scarlet",
        weapon="Knife",
        room="Kitchen",
        rng=random.Random(1),
    )

    assert shown in [knife, kitchen]


def test_ai_refutation_does_not_show_non_matching_cards() -> None:
    player = new_game(["A", "B", "C"], seed=6).players[0]
    player.hand = [Card("weapon", "Rope")]

    shown = choose_refutation_card(
        player,
        suspect="Miss Scarlet",
        weapon="Knife",
        room="Kitchen",
        rng=random.Random(1),
    )

    assert shown is None


def test_private_shown_card_updates_only_suggesting_ai_notes() -> None:
    state = new_game(
        ["AI 1", "AI 2", "Human"],
        seed=7,
        player_types=[AI_PLAYER, AI_PLAYER, HUMAN_PLAYER],
    )
    suggester = state.players[0]
    other_ai = state.players[1]
    shown = Card("weapon", "Knife")

    record_suggestion_result(
        suggester,
        {"suspect": "Miss Scarlet", "weapon": "Knife", "room": "Kitchen"},
        RefuteResult(refuted=True, refuting_player="Human", card_shown=shown),
    )

    assert ("weapon", "Knife") in suggester.ai_notes.seen_cards
    assert ("weapon", "Knife") not in other_ai.ai_notes.seen_cards


def test_ai_turn_does_not_read_solution_when_not_accusing() -> None:
    class ForbiddenSolution(dict):
        def __getitem__(self, key):
            raise AssertionError(f"AI should not read solution[{key!r}]")

        def values(self):
            raise AssertionError("AI should not inspect solution values")

    state = new_game(
        ["AI", "Bob", "Carol"],
        seed=8,
        player_types=[AI_PLAYER, HUMAN_PLAYER, HUMAN_PLAYER],
    )
    state.solution = ForbiddenSolution()

    result = take_ai_turn(state, RandomAIPlayerStrategy(random.Random(8)))

    assert result.accusation is None
    assert get_current_player(state).name == "Bob"


def test_ai_wrong_accusation_eliminates_and_still_can_refute() -> None:
    state = new_game(
        ["AI", "Bob", "Carol"],
        seed=9,
        player_types=[AI_PLAYER, HUMAN_PLAYER, HUMAN_PLAYER],
    )
    ai_player = state.players[0]
    solution = state.solution
    wrong_suspect = next(name for name in SUSPECTS if name != solution["suspect"].name)

    result = make_accusation(
        state,
        ai_player,
        suspect=wrong_suspect,
        weapon=solution["weapon"].name,
        room=solution["room"].name,
    )

    assert result.correct is False
    assert ai_player.is_eliminated is True
    assert get_current_player(state) is not ai_player

    ai_player.hand = [Card("weapon", "Knife")]
    assert choose_refutation_card(
        ai_player,
        suspect="Miss Scarlet",
        weapon="Knife",
        room="Kitchen",
    ).name == "Knife"


def test_ai_makes_accusation_when_notes_have_single_candidate() -> None:
    state = new_game(
        ["AI", "Bob", "Carol"],
        seed=12,
        player_types=[AI_PLAYER, HUMAN_PLAYER, HUMAN_PLAYER],
    )
    ai_player = state.players[0]
    solution = state.solution
    ai_player.ai_notes.possible_suspects = {solution["suspect"].name}
    ai_player.ai_notes.possible_weapons = {solution["weapon"].name}
    ai_player.ai_notes.possible_rooms = {solution["room"].name}

    result = take_ai_turn(state, RandomAIPlayerStrategy(random.Random(12)))

    assert result.accusation is not None
    assert result.accusation.correct is True
    assert state.game_over is True
    assert state.winner == "AI"


def test_all_ai_simulation_runs_for_reasonable_turns() -> None:
    state = new_game(
        ["AI Scarlet", "AI Mustard", "AI Plum"],
        seed=10,
        player_types=[AI_PLAYER, AI_PLAYER, AI_PLAYER],
    )

    results = run_ai_simulation(
        state,
        max_turns=20,
        strategy=RandomAIPlayerStrategy(random.Random(10)),
    )

    assert len(results) == 20 or state.game_over
    assert all(result.dice_roll is None or 1 <= result.dice_roll <= 6 for result in results)
    assert all(result.moved_to is None or result.moved_to in ROOMS for result in results)


def test_ai_strategy_suggestion_choices_are_canonical_cards() -> None:
    state = new_game(
        ["AI", "Bob", "Carol"],
        seed=11,
        player_types=[AI_PLAYER, HUMAN_PLAYER, HUMAN_PLAYER],
    )
    ai_player = state.players[0]

    suspect, weapon = RandomAIPlayerStrategy(random.Random(11)).choose_suggestion(ai_player)

    assert suspect in SUSPECTS
    assert weapon in WEAPONS
