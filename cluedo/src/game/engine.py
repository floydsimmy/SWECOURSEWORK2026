# src/game/engine.py
# ===================
# The game engine — controls the flow of a Cluedo match:
#   - Setting up the game (players, deck, solution, dealt hands).
#   - Managing whose turn it is.
#   - Processing player actions (move, suggest, accuse).
#
# The engine uses models from models.py to represent game state.
# Room validation relies on the canonical ROOMS list from deck.py.

from __future__ import annotations

from game.deck import ROOMS, create_deck, deal_cards, select_solution
from game.models import AccusationResult, Card, GameState, Player, RefuteResult


def new_game(player_names: list[str]) -> GameState:
    """Initialise a new Cluedo game.

    Creates the deck, randomly selects the solution, deals the remaining
    cards to the players, and returns the initial GameState.

    Args:
        player_names: Display names for each player. Must contain between
                      3 and 6 names (inclusive).

    Returns:
        A fully initialised :class:`GameState` with ``started=True``.

    Raises:
        ValueError: If fewer than 3 or more than 6 player names are supplied.
    """
    if len(player_names) < 3 or len(player_names) > 6:
        raise ValueError(
            f"Cluedo requires 3–6 players, but {len(player_names)} were given."
        )

    deck = create_deck()
    solution, remaining = select_solution(deck)
    hands = deal_cards(remaining, len(player_names))

    players = [
        Player(name=name, hand=hands[i])
        for i, name in enumerate(player_names)
    ]

    return GameState(
        players=players,
        solution=solution,
        current_turn_index=0,
        started=True,
    )


def get_current_player(state: GameState) -> Player:
    """Return the player whose turn it currently is.

    Args:
        state: The current game state.

    Returns:
        The :class:`Player` at ``state.current_turn_index``.
    """
    return state.players[state.current_turn_index]


def next_turn(state: GameState) -> None:
    """Advance the turn to the next non-eliminated player.

    Wraps around to index 0 when the end of the player list is reached.
    If every other player is eliminated, the index stays on the current
    player (edge case — the caller should handle end-of-game detection).

    Args:
        state: The current game state. Modified in place.
    """
    num_players = len(state.players)
    for _ in range(num_players):
        state.current_turn_index = (state.current_turn_index + 1) % num_players
        if not state.players[state.current_turn_index].is_eliminated:
            return


def move_to_room(state: GameState, player: Player, room: str) -> None:  # noqa: ARG001
    """Move a player into the specified room.

    Args:
        state: The current game state (unused directly, kept for API consistency).
        player: The player to move.
        room: The destination room name. Must be one of the canonical :data:`ROOMS`.

    Raises:
        ValueError: If ``room`` is not a recognised room name.
    """
    if room not in ROOMS:
        raise ValueError(
            f"'{room}' is not a valid room. Valid rooms are: {ROOMS}"
        )
    player.current_room = room


def make_suggestion(
    state: GameState,
    player: Player,
    suspect: str,
    weapon: str,
) -> RefuteResult:
    """Make a suggestion about who committed the murder.

    The room used in the suggestion is the player's current room. Other
    players are checked in clockwise (turn-order) sequence; the first
    player who holds a matching card (suspect, weapon, or the room) reveals
    one such card. Eliminated players are skipped.

    Args:
        state: The current game state.
        player: The player making the suggestion. Must currently be in a room.
        suspect: Name of the suspected character.
        weapon: Name of the suspected weapon.

    Returns:
        A :class:`RefuteResult` indicating whether the suggestion was refuted
        and, if so, who refuted it and which card they showed.

    Raises:
        ValueError: If ``player`` is not currently in any room.
    """
    if player.current_room is None:
        raise ValueError("Player must be in a room to make a suggestion.")

    room = player.current_room
    current_index = state.players.index(player)
    num_players = len(state.players)

    for offset in range(1, num_players):
        check_index = (current_index + offset) % num_players
        other = state.players[check_index]

        if other.is_eliminated:
            continue

        matching: list[Card] = [
            c for c in other.hand
            if (c.card_type == "suspect" and c.name == suspect)
            or (c.card_type == "weapon" and c.name == weapon)
            or (c.card_type == "room" and c.name == room)
        ]

        if matching:
            return RefuteResult(
                refuted=True,
                refuting_player=other.name,
                card_shown=matching[0],
            )

    return RefuteResult(refuted=False)


def make_accusation(
    state: GameState,
    player: Player,
    suspect: str,
    weapon: str,
    room: str,
) -> AccusationResult:
    """Make a formal accusation against the solution.

    If all three parts of the accusation match the solution exactly the
    accusation is correct and the player wins. If any part is wrong the
    player is eliminated (``is_eliminated`` set to ``True``).

    Args:
        state: The current game state containing the solution.
        player: The player making the accusation.
        suspect: Name of the suspected character.
        weapon: Name of the suspected weapon.
        room: Name of the suspected room.

    Returns:
        An :class:`AccusationResult` with ``correct=True`` for a winning
        accusation, or ``correct=False`` (and the player eliminated) otherwise.
    """
    solution = state.solution
    correct: bool = (
        solution["suspect"].name == suspect
        and solution["weapon"].name == weapon
        and solution["room"].name == room
    )

    if not correct:
        player.is_eliminated = True

    return AccusationResult(
        correct=correct,
        player_name=player.name,
        suspect=suspect,
        weapon=weapon,
        room=room,
    )
