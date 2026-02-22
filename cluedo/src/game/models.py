# src/game/models.py
# ===================
# Defines the core data objects (models) used throughout the game.
# A model is just a Python class that represents a real-world "thing" in the game.
#
# Planned models:
#   - Player      — a player in the game (name, character, cards in hand, position)
#   - Character   — a Cluedo suspect (e.g. Miss Scarlett, Colonel Mustard)
#   - Room        — a room on the board (e.g. Kitchen, Library)
#   - Weapon      — a weapon card (e.g. Candlestick, Lead Pipe)
#   - Card        — a single card (could be a character, room, or weapon)
#
# These classes hold data only — no game logic goes here.
# Logic lives in engine.py and rules.py.
