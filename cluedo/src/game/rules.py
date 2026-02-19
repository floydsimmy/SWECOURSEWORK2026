# src/game/rules.py
# ==================
# Enforces the rules of Cluedo.
# The engine calls functions here to check whether an action is legal
# before carrying it out.
#
# Planned rules to implement:
#   - Movement rules  — can a player move to a given square? (valid path, dice roll)
#   - Suggestion rules — can a player make a suggestion? (must be in a room)
#   - Accusation rules — is an accusation correct? (compare to the solution)
#   - Disproof rules   — which players can disprove a suggestion, and how
#
# Keeping rules here (separate from the engine) makes it easy to find,
# test, and change the game rules without touching other code.
