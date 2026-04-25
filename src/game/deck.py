"""Card deck definitions and helpers.

Defines the canonical Cluedo card sets and the deck-construction +
verification helpers. `create_deck()` is the single source of truth
used by the engine for setup; `verify_deck()` is the integrity check
exposed to tests and `validate_game_state`.
"""

from __future__ import annotations

from .models import Card

SUSPECTS: list[str] = [
    "Miss Scarlet",
    "Colonel Mustard",
    "Professor Plum",
    "Reverend Green",
    "Mrs. Peacock",
    "Mrs. White",
]

WEAPONS: list[str] = [
    "Knife",
    "Candlestick",
    "Revolver",
    "Rope",
    "Lead Pipe",
    "Wrench",
]

ROOMS: list[str] = [
    "Kitchen",
    "Ballroom",
    "Conservatory",
    "Dining Room",
    "Billiard Room",
    "Library",
    "Lounge",
    "Hall",
    "Study",
]

# 6 suspects + 6 weapons + 9 rooms = 21
EXPECTED_DECK_SIZE = len(SUSPECTS) + len(WEAPONS) + len(ROOMS)


def create_deck() -> list[Card]:
    """Build the full 21-card deck in canonical order."""
    deck: list[Card] = []
    deck.extend(Card(card_type="suspect", name=name) for name in SUSPECTS)
    deck.extend(Card(card_type="weapon", name=name) for name in WEAPONS)
    deck.extend(Card(card_type="room", name=name) for name in ROOMS)
    return deck


def verify_deck(deck: list[Card]) -> bool:
    """Return True iff `deck` contains exactly the 21 canonical cards.

    Raises ValueError on any deviation: wrong count, unknown card name,
    duplicate card, or wrong card_type for a known name.
    """
    if len(deck) != EXPECTED_DECK_SIZE:
        raise ValueError(
            f"deck has {len(deck)} cards, expected {EXPECTED_DECK_SIZE}"
        )

    seen: set[tuple[str, str]] = set()
    for card in deck:
        key = (card.card_type, card.name)
        if key in seen:
            raise ValueError(f"duplicate card in deck: {card}")
        seen.add(key)

    expected = (
        {("suspect", n) for n in SUSPECTS}
        | {("weapon", n) for n in WEAPONS}
        | {("room", n) for n in ROOMS}
    )
    if seen != expected:
        missing = expected - seen
        extra = seen - expected
        raise ValueError(
            f"deck does not match canonical set; missing={missing}, extra={extra}"
        )
    return True
