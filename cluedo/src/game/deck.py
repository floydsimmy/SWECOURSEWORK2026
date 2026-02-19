# src/game/deck.py
# =================
# Handles everything to do with the card deck.
#
# In Cluedo, cards are split into three types:
#   - Suspect cards  (e.g. Miss Scarlett, Colonel Mustard)
#   - Weapon cards   (e.g. Candlestick, Revolver)
#   - Room cards     (e.g. Kitchen, Ballroom)
#
# One card of each type is secretly chosen as the "solution" (the murder answer).
# The rest are shuffled and dealt to the players.
#
# This file will contain:
#   - A list of all cards in the game
#   - Logic to pick the solution (one random card of each type)
#   - Logic to shuffle and deal the remaining cards to players
