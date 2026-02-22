# tests/test_engine.py
# =====================
# Automated tests for the game engine (src/game/engine.py).
#
# Each test function checks that a specific part of the engine behaves correctly.
# Run all tests from the project root with:
#   pytest
#
# Tests to write (once engine.py is implemented):
#   - test that a new game starts with the correct number of players
#   - test that turns advance correctly after each player action
#   - test that a correct accusation ends the game with the right winner
#   - test that a wrong accusation eliminates the player
