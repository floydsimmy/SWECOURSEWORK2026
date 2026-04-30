"""The 21 Cluedo cards and helpers to build / check the deck."""

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
    """Return True if the deck is the full 21-card set, otherwise raise ValueError."""
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

    expected: set[tuple[str, str]] = set()
    for n in SUSPECTS:
        expected.add(("suspect", n))
    for n in WEAPONS:
        expected.add(("weapon", n))
    for n in ROOMS:
        expected.add(("room", n))
    if seen != expected:
        raise ValueError("deck does not match the canonical 21-card set")
    return True
