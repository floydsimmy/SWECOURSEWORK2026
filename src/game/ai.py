"""Autonomous player support for the Cluedo engine.

The first coursework AI is intentionally simple: it makes legal random
choices and keeps private notes from only the information it is allowed
to know. It does not inspect the hidden solution directly.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from .deck import ROOMS, SUSPECTS, WEAPONS
from .engine import (
    check_for_winner,
    get_current_player,
    make_accusation,
    make_suggestion,
    move_to_room,
    next_turn,
)
from .models import (
    AI_PLAYER,
    AccusationResult,
    Card,
    DetectiveNotes,
    GameState,
    Player,
    RefuteResult,
)


@dataclass
class AITurnResult:
    """Summary of one AI turn, useful for logs and tests."""

    player_name: str
    dice_roll: int | None = None
    moved_to: str | None = None
    suggestion: dict[str, str] | None = None
    refute_result: RefuteResult | None = None
    accusation: AccusationResult | None = None
    skipped: bool = False
    game_over: bool = False


class RandomAIPlayerStrategy:
    """Baseline random strategy that delegates all rule checks to engine APIs."""

    def __init__(self, rng: random.Random | None = None):
        self.rng = rng or random.Random()

    def roll_die(self) -> int:
        """Roll one fair six-sided die."""
        return self.rng.randint(1, 6)

    def choose_room(self, player: Player, dice_roll: int) -> str:
        """Choose a legal room accepted by the current simplified movement rule."""
        del player, dice_roll
        return self.rng.choice(ROOMS)

    def choose_suggestion(self, player: Player) -> tuple[str, str]:
        """Choose suspect and weapon for a suggestion in player's current room."""
        notes = ensure_ai_notes(player)
        suspects = sorted(notes.possible_suspects) or SUSPECTS
        weapons = sorted(notes.possible_weapons) or WEAPONS
        return self.rng.choice(suspects), self.rng.choice(weapons)

    def choose_refutation_card(
        self,
        player: Player,
        matching_cards: list[Card],
    ) -> Card:
        """Choose exactly one matching card to show."""
        del player
        return self.rng.choice(matching_cards)

    def choose_accusation(self, player: Player) -> tuple[str, str, str] | None:
        """Accuse only when private notes leave one possible card of each type."""
        notes = ensure_ai_notes(player)
        if (
            len(notes.possible_suspects) == 1
            and len(notes.possible_weapons) == 1
            and len(notes.possible_rooms) == 1
        ):
            return (
                next(iter(notes.possible_suspects)),
                next(iter(notes.possible_weapons)),
                next(iter(notes.possible_rooms)),
            )
        return None


def is_ai_player(player: Player) -> bool:
    """Return True if this player is computer-controlled."""
    return player.player_type == AI_PLAYER


def take_ai_turn(
    state: GameState,
    strategy: RandomAIPlayerStrategy | None = None,
) -> AITurnResult:
    """Execute one complete turn for the current AI player."""
    if state.game_over:
        return AITurnResult(player_name="", skipped=True, game_over=True)

    player = get_current_player(state)
    if not is_ai_player(player):
        raise ValueError(f"{player.name} is not an AI player")

    strategy = strategy or RandomAIPlayerStrategy()
    ensure_ai_notes(player)

    result = AITurnResult(player_name=player.name)
    if player.is_eliminated:
        result.skipped = True
        next_turn(state)
        return result

    dice_roll = strategy.roll_die()
    result.dice_roll = dice_roll
    state.turn_history.append(
        {"action": "roll", "player": player.name, "dice": dice_roll}
    )

    destination = strategy.choose_room(player, dice_roll)
    move_to_room(state, player, destination)
    result.moved_to = destination

    if player.current_room is not None:
        suspect, weapon = strategy.choose_suggestion(player)
        result.suggestion = {
            "suspect": suspect,
            "weapon": weapon,
            "room": player.current_room,
        }
        refute_result = make_suggestion(
            state,
            player,
            Card("suspect", suspect),
            Card("weapon", weapon),
            refute_card_chooser=strategy.choose_refutation_card,
        )
        result.refute_result = refute_result
        record_suggestion_result(player, result.suggestion, refute_result)

    accusation = strategy.choose_accusation(player)
    if accusation is not None and not state.game_over:
        suspect, weapon, room = accusation
        result.accusation = make_accusation(
            state,
            player,
            Card("suspect", suspect),
            Card("weapon", weapon),
            Card("room", room),
        )
    else:
        next_turn(state)

    check_for_winner(state)
    result.game_over = state.game_over
    return result


def run_ai_simulation(
    state: GameState,
    max_turns: int = 100,
    strategy: RandomAIPlayerStrategy | None = None,
) -> list[AITurnResult]:
    """Run AI turns until game over, a human turn, or max_turns is reached."""
    strategy = strategy or RandomAIPlayerStrategy()
    results: list[AITurnResult] = []
    for _ in range(max_turns):
        if state.game_over:
            break
        current_player = get_current_player(state)
        if not is_ai_player(current_player):
            break
        results.append(take_ai_turn(state, strategy))
    return results


def choose_refutation_card(
    player: Player,
    suspect: str,
    weapon: str,
    room: str,
    rng: random.Random | None = None,
) -> Card | None:
    """Choose one legal card to disprove a suggestion, or None if impossible."""
    suggested = {("suspect", suspect), ("weapon", weapon), ("room", room)}
    matches = [
        card for card in player.hand
        if (card.card_type, card.name) in suggested
    ]
    if not matches:
        return None
    return (rng or random.Random()).choice(matches)


def ensure_ai_notes(player: Player) -> DetectiveNotes:
    """Create notes for an AI player if a test or legacy state lacks them."""
    if player.ai_notes is None:
        player.ai_notes = DetectiveNotes(
            possible_suspects=set(SUSPECTS),
            possible_weapons=set(WEAPONS),
            possible_rooms=set(ROOMS),
        )
        for card in player.hand:
            record_known_card(player.ai_notes, card, owned=True)
    return player.ai_notes


def record_known_card(
    notes: DetectiveNotes,
    card: Card,
    *,
    owned: bool = False,
) -> None:
    """Mark a card as impossible to be in the envelope."""
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


def record_suggestion_result(
    player: Player,
    suggestion: dict[str, str],
    result: RefuteResult,
) -> None:
    """Update only the suggesting AI's private notes after a suggestion."""
    notes = ensure_ai_notes(player)
    history_entry = {
        **suggestion,
        "refuted": result.refuted,
        "refuting_player": result.refuting_player,
    }
    notes.suggestion_history.append(history_entry)

    if result.refuted and result.card_shown is not None:
        record_known_card(notes, result.card_shown)
    elif not result.refuted:
        notes.failed_disprovals.append(history_entry)
