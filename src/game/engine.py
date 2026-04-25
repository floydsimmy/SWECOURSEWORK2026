"""Cluedo game engine.

All gameplay rules live here. Functions take a GameState plus arguments
and mutate the state in place. The engine knows nothing about Pygame
or any presentation concern; it is fully testable on its own.

Public API (consumed by tests and the UI):

    new_game, reset_game, get_current_player, get_game_status,
    get_turn_summary, move_to_room, make_suggestion, make_accusation,
    next_turn, check_for_winner, validate_game_state
"""

from __future__ import annotations

import random

from .deck import (
    EXPECTED_DECK_SIZE,
    ROOMS,
    SUSPECTS,
    WEAPONS,
    create_deck,
    verify_deck,
)
from .models import (
    AccusationResult,
    Card,
    GameState,
    Player,
    RefuteResult,
)

MIN_PLAYERS = 3
MAX_PLAYERS = 6


# ---------------------------------------------------------------------------
# Game setup
# ---------------------------------------------------------------------------


def new_game(player_names: list[str], seed: int | None = None) -> GameState:
    """Create and start a fresh game for the given player names.

    Validates the player count (3–6), uniqueness, and that no name is
    blank. Builds the deck, draws the solution (one of each card type),
    deals the remaining 18 cards round-robin, and returns a started
    GameState.

    `seed` makes setup deterministic for reproducible tests; same seed
    => same solution, same deal, same turn order. None => non-deterministic.
    """
    _validate_player_names(player_names)

    rng = random.Random(seed)
    players = [Player(name=name) for name in player_names]
    deck = create_deck()

    solution = _draw_solution(deck, rng)
    _deal_round_robin(deck, players, rng)

    # F12: every suspect and weapon token has a location field, initially
    # unplaced (None). A suggestion writes the suggester's room into the
    # named entries.
    suspect_locations: dict[str, str | None] = {name: None for name in SUSPECTS}
    weapon_locations: dict[str, str | None] = {name: None for name in WEAPONS}

    return GameState(
        players=players,
        solution=solution,
        current_turn_index=0,
        started=True,
        suspect_locations=suspect_locations,
        weapon_locations=weapon_locations,
    )


def reset_game(player_names: list[str], seed: int | None = None) -> GameState:
    """Return a brand-new game for the same (or any) set of player names."""
    return new_game(player_names, seed=seed)


def _validate_player_names(names: list[str]) -> None:
    if not (MIN_PLAYERS <= len(names) <= MAX_PLAYERS):
        raise ValueError(
            f"player count must be between {MIN_PLAYERS} and {MAX_PLAYERS}, "
            f"got {len(names)}"
        )
    if any(not name for name in names):
        raise ValueError("player names must be non-empty")
    if len(set(names)) != len(names):
        raise ValueError("player names must be unique")


def _draw_solution(deck: list[Card], rng: random.Random) -> dict[str, Card]:
    """Pick one suspect, one weapon, one room from `deck` (mutates `deck`)."""
    solution: dict[str, Card] = {}
    for kind in ("suspect", "weapon", "room"):
        candidates = [c for c in deck if c.card_type == kind]
        chosen = rng.choice(candidates)
        deck.remove(chosen)
        solution[kind] = chosen
    return solution


def _deal_round_robin(
    deck: list[Card],
    players: list[Player],
    rng: random.Random,
) -> None:
    """Shuffle `deck` and deal it round-robin into each player's hand."""
    rng.shuffle(deck)
    for i, card in enumerate(deck):
        players[i % len(players)].hand.append(card)


# ---------------------------------------------------------------------------
# Player / turn queries
# ---------------------------------------------------------------------------


def get_current_player(state: GameState) -> Player:
    return state.players[state.current_turn_index]


def next_turn(state: GameState) -> None:
    """Advance the turn index, skipping eliminated players.

    If every player is eliminated this would loop forever — guard against
    that by stopping after one full pass and leaving the index unchanged.
    """
    n = len(state.players)
    for step in range(1, n + 1):
        candidate = (state.current_turn_index + step) % n
        if not state.players[candidate].is_eliminated:
            state.current_turn_index = candidate
            return
    # No active players left: leave index alone; game_over should be True.


def get_game_status(state: GameState) -> dict:
    return {
        "current_player": get_current_player(state).name,
        "players_remaining": sum(1 for p in state.players if not p.is_eliminated),
        "game_over": state.game_over,
        "winner": state.winner,
    }


def get_turn_summary(state: GameState) -> dict:
    """Return a concise snapshot of whose turn it is and what they may do."""
    player = get_current_player(state)
    actions = ["move", "accuse"]
    if player.current_room is not None:
        actions.insert(1, "suggest")
    return {
        "player_name": player.name,
        "available_actions": actions,
        "room": player.current_room,
        "is_eliminated": player.is_eliminated,
        "cards_in_hand": len(player.hand),
    }


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------


def move_to_room(state: GameState, player: Player, room: str) -> None:
    _check_game_in_progress(state)
    _check_is_current_player(state, player)
    if room not in ROOMS:
        raise ValueError(f"unknown room: {room!r}")

    player.current_room = room
    state.turn_history.append(
        {"action": "move", "player": player.name, "room": room}
    )


def make_suggestion(
    state: GameState,
    player: Player,
    suspect: Card | str,
    weapon: Card | str,
) -> RefuteResult:
    """Make a suggestion in the current player's room.

    F12 (domain): the named suspect and weapon tokens are moved into
    the suggester's current room and remain there after refutation
    completes — they are NOT returned to wherever they were. This is
    written to `state.suspect_locations` / `state.weapon_locations`
    BEFORE the refutation walk so positions persist regardless of
    refutation outcome.

    Refutation walks players in turn order starting immediately after
    the suggester, skipping eliminated ones. The first matching card
    held by an active player is shown; the suggester's turn does NOT
    advance — they may still choose to accuse.

    `suspect` and `weapon` accept either a `Card` (per the §5 contract)
    or a string (back-compat for existing callers); names are validated
    against the canonical SUSPECTS / WEAPONS lists either way.
    """
    _check_game_in_progress(state)
    _check_is_current_player(state, player)
    if player.is_eliminated:
        raise ValueError("eliminated players cannot make suggestions")
    if player.current_room is None:
        raise ValueError("player must be in a room to make a suggestion")

    suspect_name = _name_of(suspect, expected_type="suspect", field="suspect")
    weapon_name = _name_of(weapon, expected_type="weapon", field="weapon")
    if suspect_name not in SUSPECTS:
        raise ValueError(f"unknown suspect: {suspect_name!r}")
    if weapon_name not in WEAPONS:
        raise ValueError(f"unknown weapon: {weapon_name!r}")

    room = player.current_room

    # F12: move the suspect and weapon tokens into the suggester's room
    # BEFORE the refutation walk — they stay here whatever happens next.
    state.suspect_locations[suspect_name] = room
    state.weapon_locations[weapon_name] = room

    state.turn_history.append(
        {
            "action": "suggestion",
            "player": player.name,
            "suspect": suspect_name,
            "weapon": weapon_name,
            "room": room,
        }
    )

    suggested = {("suspect", suspect_name), ("weapon", weapon_name), ("room", room)}
    n = len(state.players)
    suggester_idx = state.players.index(player)

    for step in range(1, n):
        idx = (suggester_idx + step) % n
        other = state.players[idx]
        if other.is_eliminated:
            continue
        for card in other.hand:
            if (card.card_type, card.name) in suggested:
                return RefuteResult(
                    refuted=True,
                    refuting_player=other.name,
                    card_shown=card,
                )

    return RefuteResult(refuted=False)


def make_accusation(
    state: GameState,
    player: Player,
    suspect: Card | str,
    weapon: Card | str,
    room: Card | str,
) -> AccusationResult:
    """Make a final accusation. Always advances the turn afterwards.

    A correct accusation ends the game with `player` as the winner. A
    wrong accusation eliminates `player`; if that empties the active
    pool, the game ends with no winner (a draw).

    `suspect`, `weapon`, and `room` accept either a `Card` (per §5)
    or a string (back-compat); names are validated against the
    canonical lists either way.
    """
    _check_game_in_progress(state)
    _check_is_current_player(state, player)
    if player.is_eliminated:
        raise ValueError("eliminated players cannot make accusations")

    suspect_name = _name_of(suspect, expected_type="suspect", field="suspect")
    weapon_name = _name_of(weapon, expected_type="weapon", field="weapon")
    room_name = _name_of(room, expected_type="room", field="room")
    if suspect_name not in SUSPECTS:
        raise ValueError(f"unknown suspect: {suspect_name!r}")
    if weapon_name not in WEAPONS:
        raise ValueError(f"unknown weapon: {weapon_name!r}")
    if room_name not in ROOMS:
        raise ValueError(f"unknown room: {room_name!r}")

    sol = state.solution
    correct = (
        suspect_name == sol["suspect"].name
        and weapon_name == sol["weapon"].name
        and room_name == sol["room"].name
    )
    result = AccusationResult(
        correct=correct,
        player_name=player.name,
        suspect=suspect_name,
        weapon=weapon_name,
        room=room_name,
    )

    if correct:
        state.game_over = True
        state.winner = player.name
    else:
        player.is_eliminated = True
        active_count = sum(1 for p in state.players if not p.is_eliminated)
        if active_count == 0:
            state.game_over = True
            state.winner = None

    next_turn(state)
    return result


def check_for_winner(state: GameState) -> Player | None:
    """Detect end-of-game by elimination.

    If there is exactly one player still active and the game has not
    already been decided by a correct accusation, declare them the
    winner and end the game. Returns the winning Player, or None if
    play should continue.
    """
    if state.game_over:
        if state.winner is None:
            return None
        for p in state.players:
            if p.name == state.winner:
                return p
        return None

    active = [p for p in state.players if not p.is_eliminated]
    if len(active) == 1:
        winner = active[0]
        state.game_over = True
        state.winner = winner.name
        return winner
    return None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_game_state(state: GameState) -> bool:
    """Sanity-check a GameState. Returns True or raises ValueError."""
    if set(state.solution.keys()) != {"suspect", "weapon", "room"}:
        raise ValueError(
            "solution must have exactly the keys 'suspect', 'weapon', 'room'"
        )

    all_cards: list[Card] = []
    for p in state.players:
        all_cards.extend(p.hand)
    all_cards.extend(state.solution.values())

    if len(all_cards) != EXPECTED_DECK_SIZE:
        raise ValueError(
            f"total card count is {len(all_cards)}, expected {EXPECTED_DECK_SIZE} (21)"
        )

    seen: set[tuple[str, str]] = set()
    for card in all_cards:
        key = (card.card_type, card.name)
        if key in seen:
            raise ValueError(f"Duplicate card in game state: {card}")
        seen.add(key)

    verify_deck(all_cards)

    if not 0 <= state.current_turn_index < len(state.players):
        raise ValueError(
            f"current_turn_index {state.current_turn_index} is out of bounds"
        )
    return True


# ---------------------------------------------------------------------------
# Internal guards
# ---------------------------------------------------------------------------


def _check_game_in_progress(state: GameState) -> None:
    if state.game_over:
        raise ValueError("Game is already over")


def _check_is_current_player(state: GameState, player: Player) -> None:
    if state.players[state.current_turn_index] is not player:
        raise ValueError(
            f"it is not {player.name}'s turn "
            f"(current is {get_current_player(state).name})"
        )


def _name_of(card_or_str: Card | str, *, expected_type: str, field: str) -> str:
    """Coerce a `Card` or a bare name string to a name.

    Per §5 the contract is `Card`. Existing string call sites are
    accepted unchanged. If a `Card` is passed with the wrong
    `card_type`, raise — that is a programming error in the caller.
    """
    if isinstance(card_or_str, Card):
        if card_or_str.card_type != expected_type:
            raise ValueError(
                f"{field} expected a {expected_type} card, "
                f"got a {card_or_str.card_type} card ({card_or_str.name!r})"
            )
        return card_or_str.name
    if isinstance(card_or_str, str):
        return card_or_str
    raise TypeError(
        f"{field} must be a Card or str, got {type(card_or_str).__name__}"
    )
