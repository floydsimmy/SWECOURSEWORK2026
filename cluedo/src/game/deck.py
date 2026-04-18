# src/game/deck.py
# =================
# Handles everything to do with the card deck:
#   - Canonical lists of suspects, weapons, and rooms.
#   - Creating the full 21-card deck.
#   - Randomly selecting the secret solution (one card of each type).
#   - Dealing the remaining cards as evenly as possible to players.

from __future__ import annotations

import random

from game.models import Card

# ---------------------------------------------------------------------------
# Canonical card lists
# ---------------------------------------------------------------------------

SUSPECTS: list[str] = [
    "Miss Scarlet",
    "Colonel Mustard",
    "Mrs White",
    "Reverend Green",
    "Mrs Peacock",
    "Professor Plum",
]

WEAPONS: list[str] = [
    "Candlestick",
    "Knife",
    "Lead Pipe",
    "Revolver",
    "Rope",
    "Wrench",
]

ROOMS: list[str] = [
    "Kitchen",
    "Ballroom",
    "Conservatory",
    "Billiard Room",
    "Library",
    "Study",
    "Hall",
    "Lounge",
    "Dining Room",
]


# ---------------------------------------------------------------------------
# Deck functions
# ---------------------------------------------------------------------------


def create_deck() -> list[Card]:
    """Create and return the full 21-card Cluedo deck (unsorted, not shuffled).

    Returns:
        A list containing one Card for each suspect, weapon, and room.
    """
    deck: list[Card] = []
    for name in SUSPECTS:
        deck.append(Card(card_type="suspect", name=name))
    for name in WEAPONS:
        deck.append(Card(card_type="weapon", name=name))
    for name in ROOMS:
        deck.append(Card(card_type="room", name=name))
    return deck


def select_solution(deck: list[Card]) -> tuple[dict[str, Card], list[Card]]:
    """Randomly pick one suspect, one weapon, and one room card as the solution.

    Args:
        deck: The full list of cards returned by :func:`create_deck`.

    Returns:
        A 2-tuple of:
          - solution dict with keys ``"suspect"``, ``"weapon"``, ``"room"``
            each mapping to the chosen Card.
          - remaining cards (all deck cards *not* in the solution).
    """
    suspects = [c for c in deck if c.card_type == "suspect"]
    weapons = [c for c in deck if c.card_type == "weapon"]
    rooms = [c for c in deck if c.card_type == "room"]

    chosen_suspect = random.choice(suspects)
    chosen_weapon = random.choice(weapons)
    chosen_room = random.choice(rooms)

    solution: dict[str, Card] = {
        "suspect": chosen_suspect,
        "weapon": chosen_weapon,
        "room": chosen_room,
    }

    remaining = [
        c for c in deck
        if c is not chosen_suspect
        and c is not chosen_weapon
        and c is not chosen_room
    ]

    return solution, remaining


def verify_deck(deck: list[Card]) -> bool:
    """Verify that a deck has the correct Cluedo composition.

    A valid Cluedo deck contains exactly 6 suspects, 6 weapons, and 9 rooms
    (21 cards total).

    Args:
        deck: The list of :class:`~game.models.Card` objects to verify.

    Returns:
        True if the deck is valid.

    Raises:
        ValueError: With a descriptive message if the deck has the wrong
                    number of suspects, weapons, or rooms.
    """
    suspects = [c for c in deck if c.card_type == "suspect"]
    weapons = [c for c in deck if c.card_type == "weapon"]
    rooms = [c for c in deck if c.card_type == "room"]

    errors: list[str] = []
    if len(suspects) != 6:
        errors.append(f"expected 6 suspects, found {len(suspects)}")
    if len(weapons) != 6:
        errors.append(f"expected 6 weapons, found {len(weapons)}")
    if len(rooms) != 9:
        errors.append(f"expected 9 rooms, found {len(rooms)}")

    if errors:
        raise ValueError(f"Deck verification failed: {'; '.join(errors)}.")

    return True


def deal_cards(cards: list[Card], num_players: int) -> list[list[Card]]:
    """Shuffle and deal cards as evenly as possible across all players.

    Cards are distributed in round-robin order so that hand sizes differ by
    at most one card.

    Args:
        cards: The remaining cards after the solution has been removed.
        num_players: The number of players to deal to.

    Returns:
        A list of ``num_players`` hands, where each hand is a list of Cards.
    """
    shuffled = list(cards)
    random.shuffle(shuffled)

    hands: list[list[Card]] = [[] for _ in range(num_players)]
    for i, card in enumerate(shuffled):
        hands[i % num_players].append(card)

    return hands
