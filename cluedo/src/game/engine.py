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

from typing import Optional

from game.deck import ROOMS, SUSPECTS, WEAPONS, create_deck, deal_cards, select_solution
from game.models import AccusationResult, Card, GameState, Player, RefuteResult


def new_game(player_names: list[str]) -> GameState:
    """Initialise a new Cluedo game.

    Creates the deck, randomly selects the solution, deals the remaining
    cards to the players, and returns the initial GameState.

    Args:
        player_names: Display names for each player. Must contain between
                      3 and 6 unique, non-empty names (inclusive).

    Returns:
        A fully initialised :class:`GameState` with ``started=True``.

    Raises:
        ValueError: If fewer than 3 or more than 6 player names are supplied,
                    any name is empty, or names contain duplicates.
    """
    if len(player_names) < 3 or len(player_names) > 6:
        raise ValueError(
            f"Cluedo requires 3–6 players, but {len(player_names)} were given."
        )
    if any(not name.strip() for name in player_names):
        raise ValueError("Player names must not be empty.")
    if len(player_names) != len(set(player_names)):
        raise ValueError("Player names must be unique.")

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


def move_to_room(state: GameState, player: Player, room: str) -> None:
    """Move a player into the specified room.

    Args:
        state: The current game state.
        player: The player to move. Must be the current player.
        room: The destination room name. Must be one of the canonical :data:`ROOMS`.

    Raises:
        ValueError: If the game is over, it is not this player's turn, or
                    ``room`` is not a recognised room name.
    """
    if state.game_over:
        raise ValueError("Game is already over.")
    current = get_current_player(state)
    if current is not player:
        raise ValueError(f"It is {current.name}'s turn, not {player.name}'s.")
    if room not in ROOMS:
        raise ValueError(
            f"Invalid room '{room}'. Must be one of: {', '.join(ROOMS)}."
        )
    player.current_room = room
    state.turn_history.append({
        "action": "move",
        "player": player.name,
        "details": {"room": room},
        "result": {},
    })


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
    one such card. Eliminated players are skipped. The turn does NOT advance
    after a suggestion — the player may still wish to accuse.

    Args:
        state: The current game state.
        player: The player making the suggestion. Must be the current player
                and must currently be in a room.
        suspect: Name of the suspected character. Must be in :data:`SUSPECTS`.
        weapon: Name of the suspected weapon. Must be in :data:`WEAPONS`.

    Returns:
        A :class:`RefuteResult` indicating whether the suggestion was refuted
        and, if so, who refuted it and which card they showed.

    Raises:
        ValueError: If the game is over, it is not this player's turn,
                    the player is eliminated, the suspect or weapon is invalid,
                    or the player is not currently in any room.
    """
    if state.game_over:
        raise ValueError("Game is already over.")
    current = get_current_player(state)
    if current is not player:
        raise ValueError(f"It is {current.name}'s turn, not {player.name}'s.")
    if player.is_eliminated:
        raise ValueError(f"{player.name} is eliminated and cannot make a suggestion.")
    if suspect not in SUSPECTS:
        raise ValueError(
            f"Invalid suspect '{suspect}'. Must be one of: {', '.join(SUSPECTS)}."
        )
    if weapon not in WEAPONS:
        raise ValueError(
            f"Invalid weapon '{weapon}'. Must be one of: {', '.join(WEAPONS)}."
        )
    if player.current_room is None:
        raise ValueError("Player must be in a room to make a suggestion.")

    room = player.current_room
    current_index = state.players.index(player)
    num_players = len(state.players)

    result: RefuteResult = RefuteResult(refuted=False)
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
            result = RefuteResult(
                refuted=True,
                refuting_player=other.name,
                card_shown=matching[0],
            )
            break

    state.turn_history.append({
        "action": "suggestion",
        "player": player.name,
        "details": {"suspect": suspect, "weapon": weapon, "room": room},
        "result": {
            "refuted": result.refuted,
            "refuting_player": result.refuting_player,
        },
    })
    return result


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
    player is eliminated (``is_eliminated`` set to ``True``). The turn
    automatically advances to the next active player after any accusation.

    Args:
        state: The current game state containing the solution.
        player: The player making the accusation. Must be the current player.
        suspect: Name of the suspected character. Must be in :data:`SUSPECTS`.
        weapon: Name of the suspected weapon. Must be in :data:`WEAPONS`.
        room: Name of the suspected room. Must be in :data:`ROOMS`.

    Returns:
        An :class:`AccusationResult` with ``correct=True`` for a winning
        accusation, or ``correct=False`` (and the player eliminated) otherwise.

    Raises:
        ValueError: If the game is over, it is not this player's turn,
                    the player is already eliminated, or any of the three
                    accusation values are not valid.
    """
    if state.game_over:
        raise ValueError("Game is already over.")
    current = get_current_player(state)
    if current is not player:
        raise ValueError(f"It is {current.name}'s turn, not {player.name}'s.")
    if player.is_eliminated:
        raise ValueError(f"{player.name} is eliminated and cannot make an accusation.")
    if suspect not in SUSPECTS:
        raise ValueError(
            f"Invalid suspect '{suspect}'. Must be one of: {', '.join(SUSPECTS)}."
        )
    if weapon not in WEAPONS:
        raise ValueError(
            f"Invalid weapon '{weapon}'. Must be one of: {', '.join(WEAPONS)}."
        )
    if room not in ROOMS:
        raise ValueError(
            f"Invalid room '{room}'. Must be one of: {', '.join(ROOMS)}."
        )

    solution = state.solution
    correct: bool = (
        solution["suspect"].name == suspect
        and solution["weapon"].name == weapon
        and solution["room"].name == room
    )

    if correct:
        state.game_over = True
        state.winner = player.name
    else:
        player.is_eliminated = True
        active = [p for p in state.players if not p.is_eliminated]
        if len(active) == 0:
            state.game_over = True
            # winner stays None — draw, no one solved it

    result = AccusationResult(
        correct=correct,
        player_name=player.name,
        suspect=suspect,
        weapon=weapon,
        room=room,
    )

    state.turn_history.append({
        "action": "accusation",
        "player": player.name,
        "details": {"suspect": suspect, "weapon": weapon, "room": room},
        "result": {"correct": result.correct},
    })

    next_turn(state)
    return result


def check_for_winner(state: GameState) -> Optional[Player]:
    """Return the sole surviving player if all others are eliminated, else None.

    If exactly one non-eliminated player remains the game is set to over and
    that player is recorded as the winner on *state* before being returned.
    If zero active players remain the game is set to over with no winner (draw).

    Args:
        state: The current game state. May be mutated (``game_over`` /
               ``winner``) if a last-player-standing condition is detected.

    Returns:
        The winning :class:`Player`, or ``None`` if the game is already over
        through a correct accusation or if more than one player is still active.
    """
    if state.game_over:
        # Already won via a correct accusation — look up and return that player.
        for p in state.players:
            if p.name == state.winner:
                return p
        return None

    active = [p for p in state.players if not p.is_eliminated]
    if len(active) == 0:
        state.game_over = True
        # winner stays None — draw
        return None
    if len(active) == 1:
        state.game_over = True
        state.winner = active[0].name
        return active[0]

    return None


def get_game_status(state: GameState) -> dict:
    """Return a summary dictionary describing the current game state.

    Args:
        state: The current game state.

    Returns:
        A dict with the following keys:

        * ``"current_player"`` — display name of the player whose turn it is.
        * ``"players_remaining"`` — count of non-eliminated players.
        * ``"game_over"`` — ``True`` once the game has ended.
        * ``"winner"`` — display name of the winner, or ``None`` if the game
          is still in progress.
    """
    active = [p for p in state.players if not p.is_eliminated]
    return {
        "current_player": get_current_player(state).name,
        "players_remaining": len(active),
        "game_over": state.game_over,
        "winner": state.winner,
    }


def get_turn_summary(state: GameState) -> dict:
    """Return a dict describing the current player's position and available actions.

    Args:
        state: The current game state.

    Returns:
        A dict with the following keys:

        * ``"player_name"`` — display name of the current player.
        * ``"available_actions"`` — list of action strings the player can take.
          Always includes ``"move"`` and ``"accuse"``; includes ``"suggest"``
          only when the player is in a room.
        * ``"room"`` — the player's current room name, or ``None``.
        * ``"is_eliminated"`` — ``True`` if the player has been eliminated.
        * ``"cards_in_hand"`` — number of cards held (not the cards themselves).
    """
    player = get_current_player(state)
    actions: list[str] = ["move", "suggest", "accuse"] if player.current_room is not None else ["move", "accuse"]
    return {
        "player_name": player.name,
        "available_actions": actions,
        "room": player.current_room,
        "is_eliminated": player.is_eliminated,
        "cards_in_hand": len(player.hand),
    }


def reset_game(player_names: list[str]) -> GameState:
    """Start a fresh game with the same player names.

    Args:
        player_names: Display names for each player, subject to the same
                      constraints as :func:`new_game`.

    Returns:
        A brand-new :class:`GameState` as if :func:`new_game` had been called.
    """
    return new_game(player_names)


def validate_game_state(state: GameState) -> bool:
    """Assert that a GameState is internally consistent.

    Performs four checks:

    1. The solution contains exactly the keys ``"suspect"``, ``"weapon"``,
       and ``"room"``, each mapping to a card of the matching type.
    2. ``current_turn_index`` is within the bounds of ``state.players``.
    3. The combined card count (solution cards + all player hands) equals 21.
    4. No card (identified by ``card_type`` + ``name``) appears more than once
       across the solution and all player hands.

    Args:
        state: The :class:`GameState` to validate.

    Returns:
        ``True`` if every check passes.

    Raises:
        ValueError: With a descriptive message identifying the first failed
                    check.
    """
    expected_keys = {"suspect", "weapon", "room"}
    if set(state.solution.keys()) != expected_keys:
        raise ValueError(
            f"Solution must have exactly the keys {expected_keys}; "
            f"got: {set(state.solution.keys())}."
        )
    for key in ("suspect", "weapon", "room"):
        card = state.solution[key]
        if card.card_type != key:
            raise ValueError(
                f"Solution card for '{key}' has wrong card_type '{card.card_type}'."
            )

    num_players = len(state.players)
    if not (0 <= state.current_turn_index < num_players):
        raise ValueError(
            f"current_turn_index {state.current_turn_index} is out of bounds "
            f"for {num_players} player(s)."
        )

    solution_cards = list(state.solution.values())
    hand_cards = [card for player in state.players for card in player.hand]
    all_cards = solution_cards + hand_cards

    if len(all_cards) != 21:
        raise ValueError(
            f"Expected 21 total cards (solution + all hands), found {len(all_cards)}."
        )

    card_ids = [(c.card_type, c.name) for c in all_cards]
    if len(card_ids) != len(set(card_ids)):
        seen: set[tuple[str, str]] = set()
        duplicates: list[tuple[str, str]] = []
        for cid in card_ids:
            if cid in seen:
                duplicates.append(cid)
            seen.add(cid)
        raise ValueError(
            f"Duplicate cards found: {duplicates}."
        )

    return True
