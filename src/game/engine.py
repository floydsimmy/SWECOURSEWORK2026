"""Cluedo game engine.

All gameplay rules live here. Functions take a GameState plus arguments
and mutate the state in place. The engine knows nothing about Pygame
or any presentation concern; it is fully testable on its own.

Public API (consumed by tests and the UI):

    new_game, reset_game, get_current_player, get_game_status,
    get_turn_summary, roll_die, legal_moves_for_roll, move_by_dice,
    move_to_room, make_suggestion, make_accusation, next_turn,
    check_for_winner, validate_game_state
"""

from __future__ import annotations

import random
from typing import Callable

from .deck import (
    EXPECTED_DECK_SIZE,
    ROOMS,
    SUSPECTS,
    WEAPONS,
    create_deck,
    verify_deck,
)
from .models import (
    AI_PLAYER,
    AccusationResult,
    Card,
    DetectiveNotes,
    GameState,
    HUMAN_PLAYER,
    PLAYER_TYPES,
    Player,
    RefuteResult,
)

MIN_PLAYERS = 3
MAX_PLAYERS = 6
BOARD_GRID_SIZE = 24

ROOM_LAYOUT: dict[str, tuple[int, int, int, int]] = {
    "Kitchen": (0, 0, 6, 6),
    "Ballroom": (7, 0, 10, 7),
    "Conservatory": (18, 0, 6, 6),
    "Dining Room": (0, 8, 7, 8),
    "Billiard Room": (17, 7, 7, 5),
    "Library": (17, 13, 7, 4),
    "Lounge": (0, 18, 7, 6),
    "Hall": (9, 18, 7, 6),
    "Study": (18, 18, 6, 6),
}

CENTER_AREA = (8, 9, 8, 6)

ROOM_DOORS: dict[str, list[tuple[str, int]]] = {
    "Kitchen": [("bottom", 4)],
    "Ballroom": [("bottom", 2), ("bottom", 7), ("left", 5), ("right", 5)],
    "Conservatory": [("bottom", 1)],
    "Dining Room": [("right", 2), ("right", 6)],
    "Billiard Room": [("left", 1), ("bottom", 3)],
    "Library": [("left", 1), ("left", 3)],
    "Lounge": [("top", 5)],
    "Hall": [("top", 1), ("top", 5)],
    "Study": [("top", 1)],
}

CHARACTER_START_TILES: dict[str, tuple[int, int]] = {
    "Miss Scarlet": (7, 23),
    "Colonel Mustard": (7, 17),
    "Professor Plum": (23, 17),
    "Reverend Green": (17, 0),
    "Mrs. Peacock": (23, 6),
    "Mrs. White": (6, 0),
}


# ---------------------------------------------------------------------------
# Game setup
# ---------------------------------------------------------------------------


def new_game(
    player_names: list[str],
    seed: int | None = None,
    player_types: list[str] | None = None,
) -> GameState:
    """Create and start a fresh game for the given player names.

    Validates the player count (3–6), uniqueness, and that no name is
    blank. Builds the deck, draws the solution (one of each card type),
    deals the remaining 18 cards round-robin, and returns a started
    GameState.

    `seed` makes setup deterministic for reproducible tests; same seed
    => same solution, same deal, same turn order. None => non-deterministic.
    """
    _validate_player_names(player_names)
    normalised_player_types = _normalise_player_types(player_names, player_types)

    rng = random.Random(seed)
    players = [
        Player(
            name=name,
            player_type=normalised_player_types[index],
            character=SUSPECTS[index % len(SUSPECTS)],
            board_position=CHARACTER_START_TILES[SUSPECTS[index % len(SUSPECTS)]],
        )
        for index, name in enumerate(player_names)
    ]
    deck = create_deck()

    solution = _draw_solution(deck, rng)
    _deal_round_robin(deck, players, rng)

    # F12: every suspect and weapon token has a location field, initially
    # unplaced (None). A suggestion writes the suggester's room into the
    # named entries.
    suspect_locations: dict[str, str | None] = {name: None for name in SUSPECTS}
    weapon_locations: dict[str, str | None] = {name: None for name in WEAPONS}

    state = GameState(
        players=players,
        solution=solution,
        current_turn_index=0,
        started=True,
        suspect_locations=suspect_locations,
        weapon_locations=weapon_locations,
    )
    _initialise_ai_notes(state)
    return state


def reset_game(
    player_names: list[str],
    seed: int | None = None,
    player_types: list[str] | None = None,
) -> GameState:
    """Return a brand-new game for the same (or any) set of player names."""
    return new_game(player_names, seed=seed, player_types=player_types)


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


def _normalise_player_types(
    names: list[str],
    player_types: list[str] | None,
) -> list[str]:
    """Return one player type per name, defaulting to human players."""
    if player_types is None:
        return [HUMAN_PLAYER for _ in names]
    if len(player_types) != len(names):
        raise ValueError("player_types must match player_names length")

    normalised = [kind.lower() for kind in player_types]
    for kind in normalised:
        if kind not in PLAYER_TYPES:
            raise ValueError(f"unknown player type: {kind!r}")
    return normalised


def _initialise_ai_notes(state: GameState) -> None:
    """Create private notes for AI players from only their own hands."""
    for player in state.players:
        if player.player_type != AI_PLAYER:
            player.ai_notes = None
            continue

        notes = DetectiveNotes(
            possible_suspects=set(SUSPECTS),
            possible_weapons=set(WEAPONS),
            possible_rooms=set(ROOMS),
        )
        for card in player.hand:
            _record_known_card(notes, card, owned=True)
        player.ai_notes = notes


def _record_known_card(
    notes: DetectiveNotes,
    card: Card,
    *,
    owned: bool = False,
) -> None:
    key = (card.card_type, card.name)
    if owned:
        notes.owned_cards.add(key)
    notes.seen_cards.add(key)
    notes.known_not_in_envelope.add(key)

    if card.card_type == "suspect":
        notes.possible_suspects.discard(card.name)
    elif card.card_type == "weapon":
        notes.possible_weapons.discard(card.name)
    elif card.card_type == "room":
        notes.possible_rooms.discard(card.name)


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


def roll_die(rng: random.Random | None = None) -> int:
    """Roll one fair six-sided die."""
    roller = rng or random
    return roller.randint(1, 6)


def legal_moves_for_roll(
    state: GameState,
    player: Player,
    dice_roll: int,
) -> dict[str, list]:
    """Return hallway tiles and rooms the player may reach with this roll."""
    _check_game_in_progress(state)
    _check_is_current_player(state, player)
    _check_dice_roll(dice_roll)
    if player.is_eliminated:
        raise ValueError("eliminated players cannot move")

    occupied = _occupied_player_tiles(state, excluding=player)
    tile_distances = _reachable_corridor_tiles(player, dice_roll, occupied)

    hallway_tiles = sorted(
        tile
        for tile, distance in tile_distances.items()
        if distance == dice_roll
    )

    rooms = sorted(
        room
        for room, door_tiles in _room_door_tiles().items()
        if room != player.current_room
        and any(tile_distances.get(tile, dice_roll + 1) <= dice_roll for tile in door_tiles)
    )

    return {"tiles": hallway_tiles, "rooms": rooms}


def move_by_dice(
    state: GameState,
    player: Player,
    dice_roll: int,
    destination: str | tuple[int, int],
) -> None:
    """Move a player to a legal dice destination."""
    legal_moves = legal_moves_for_roll(state, player, dice_roll)

    if isinstance(destination, str):
        if destination not in legal_moves["rooms"]:
            raise ValueError(f"room is not reachable with this roll: {destination!r}")
        player.current_room = destination
        player.board_position = None
        state.turn_history.append(
            {
                "action": "move",
                "player": player.name,
                "dice": dice_roll,
                "room": destination,
            }
        )
        return

    if not _is_tile(destination):
        raise ValueError(f"invalid board position: {destination!r}")

    tile = (int(destination[0]), int(destination[1]))
    if tile not in legal_moves["tiles"]:
        raise ValueError(f"tile is not reachable with this roll: {tile!r}")

    player.current_room = None
    player.board_position = tile
    state.turn_history.append(
        {
            "action": "move",
            "player": player.name,
            "dice": dice_roll,
            "position": tile,
        }
    )


def move_to_room(state: GameState, player: Player, room: str) -> None:
    _check_game_in_progress(state)
    _check_is_current_player(state, player)
    if room not in ROOMS:
        raise ValueError(f"unknown room: {room!r}")

    player.current_room = room
    player.board_position = None
    state.turn_history.append(
        {"action": "move", "player": player.name, "room": room}
    )


def make_suggestion(
    state: GameState,
    player: Player,
    suspect: Card | str,
    weapon: Card | str,
    refute_card_chooser: Callable[[Player, list[Card]], Card] | None = None,
) -> RefuteResult:
    """Make a suggestion in the current player's room.

    F12 (domain): the named suspect and weapon tokens are moved into
    the suggester's current room and remain there after refutation
    completes — they are NOT returned to wherever they were. This is
    written to `state.suspect_locations` / `state.weapon_locations`
    BEFORE the refutation walk so positions persist regardless of
    refutation outcome.

    Refutation walks players in turn order starting immediately after
    the suggester. Eliminated players are still checked because wrong
    accusers stop taking normal turns but keep showing cards when they
    can refute. The first matching card is shown; the suggester's turn does NOT
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
        matching_cards = [
            card for card in other.hand
            if (card.card_type, card.name) in suggested
        ]
        if matching_cards:
            card_shown = (
                refute_card_chooser(other, matching_cards)
                if refute_card_chooser
                else matching_cards[0]
            )
            if card_shown not in matching_cards:
                raise ValueError("refute_card_chooser must return a matching card")
            return RefuteResult(
                refuted=True,
                refuting_player=other.name,
                card_shown=card_shown,
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
        if p.player_type not in PLAYER_TYPES:
            raise ValueError(f"unknown player type: {p.player_type!r}")
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
# Board movement helpers
# ---------------------------------------------------------------------------


def _check_dice_roll(dice_roll: int) -> None:
    if not isinstance(dice_roll, int) or not 1 <= dice_roll <= 6:
        raise ValueError(f"dice_roll must be between 1 and 6, got {dice_roll!r}")


def _reachable_corridor_tiles(
    player: Player,
    dice_roll: int,
    occupied: set[tuple[int, int]],
) -> dict[tuple[int, int], int]:
    distances: dict[tuple[int, int], int] = {}
    queue: list[tuple[tuple[int, int], int]] = []

    if player.current_room in ROOMS:
        for tile in _room_door_tiles()[player.current_room]:
            if tile not in occupied:
                distances[tile] = 1
                queue.append((tile, 1))
    else:
        start = _player_board_position(player)
        distances[start] = 0
        queue.append((start, 0))

    queue_index = 0
    while queue_index < len(queue):
        tile, distance = queue[queue_index]
        queue_index += 1

        if distance >= dice_roll:
            continue

        for next_tile in _adjacent_corridor_tiles(tile):
            if next_tile in occupied:
                continue
            next_distance = distance + 1
            if next_distance < distances.get(next_tile, dice_roll + 1):
                distances[next_tile] = next_distance
                queue.append((next_tile, next_distance))

    return distances


def _player_board_position(player: Player) -> tuple[int, int]:
    if _is_tile(player.board_position) and _is_walkable_tile(player.board_position):
        return (int(player.board_position[0]), int(player.board_position[1]))
    if player.character in CHARACTER_START_TILES:
        return CHARACTER_START_TILES[player.character]
    return CHARACTER_START_TILES["Miss Scarlet"]


def _adjacent_corridor_tiles(tile: tuple[int, int]) -> list[tuple[int, int]]:
    col, row = tile
    candidates = [
        (col + 1, row),
        (col - 1, row),
        (col, row + 1),
        (col, row - 1),
    ]
    return [candidate for candidate in candidates if _is_walkable_tile(candidate)]


def _room_door_tiles() -> dict[str, list[tuple[int, int]]]:
    return {
        room: [
            tile
            for tile in (
                _external_door_tile(room, side, offset)
                for side, offset in doors
            )
            if _is_walkable_tile(tile)
        ]
        for room, doors in ROOM_DOORS.items()
    }


def _external_door_tile(room: str, side: str, offset: int) -> tuple[int, int]:
    col, row, width, height = ROOM_LAYOUT[room]
    if side == "top":
        return (col + offset, row - 1)
    if side == "bottom":
        return (col + offset, row + height)
    if side == "left":
        return (col - 1, row + offset)
    return (col + width, row + offset)


def _occupied_player_tiles(
    state: GameState,
    *,
    excluding: Player,
) -> set[tuple[int, int]]:
    occupied: set[tuple[int, int]] = set()
    for other in state.players:
        if other is excluding or other.current_room is not None:
            continue
        tile = _player_board_position(other)
        if _is_walkable_tile(tile):
            occupied.add(tile)
    return occupied


def _is_walkable_tile(tile: tuple[int, int]) -> bool:
    return (
        _is_tile(tile)
        and 0 <= tile[0] < BOARD_GRID_SIZE
        and 0 <= tile[1] < BOARD_GRID_SIZE
        and tile not in _blocked_board_tiles()
    )


def _blocked_board_tiles() -> set[tuple[int, int]]:
    blocked: set[tuple[int, int]] = set()
    for layout in list(ROOM_LAYOUT.values()) + [CENTER_AREA]:
        col, row, width, height = layout
        for blocked_col in range(col, col + width):
            for blocked_row in range(row, row + height):
                blocked.add((blocked_col, blocked_row))
    return blocked


def _is_tile(value: object) -> bool:
    return (
        isinstance(value, tuple)
        and len(value) == 2
        and isinstance(value[0], int)
        and isinstance(value[1], int)
    )


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
