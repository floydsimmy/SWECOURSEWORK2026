# src/game/engine.py
# ===================
# The game engine — the brain of the game.
# It controls the flow of a match from start to finish:
#   - Setting up the game (players, cards, starting positions)
#   - Managing whose turn it is
#   - Processing player actions (moving, making suggestions, making accusations)
#   - Checking win/loss conditions
#
# The engine uses the models from models.py to represent game state,
# and checks rules.py to decide what is and isn't allowed.
