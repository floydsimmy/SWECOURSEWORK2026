# Requirements — Cluedo (Team 53)

Derived from the Watson Games user requirements document (Cluedo!) and refined into testable functional, non-functional, and domain requirements. Each ID appears in the unit test suite (`tests/`) and in the system test report (`docs/testing/system_test_report.md`).

## Functional requirements (mandatory — "shall")

| ID  | Requirement                                                                                                                                    |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| F1  | The game shall set up with one suspect, one weapon, and one room as the hidden solution.                                                       |
| F2  | The game shall deal all 18 remaining cards to players such that no card is lost or duplicated.                                                  |
| F3  | The game shall cycle turns in player order and skip eliminated players.                                                                         |
| F4  | The game shall allow a player to roll a six-sided die and move that number of squares along the 24 × 24 board, ending in either a corridor tile or a room reached via a door. F4 includes the door-tile rule — players enter rooms only through their door tiles and cannot enter and exit the same room within a single dice move. |
| F5  | The game shall use the suggesting player's current room as the room in their suggestion.                                                        |
| F6  | The game shall walk other players in turn order from the suggester's left, including eliminated players, and reveal exactly one matching card to the suggester. |
| F7  | The game shall declare a player the winner when they make a correct accusation.                                                                 |
| F8  | The game shall eliminate a player who makes a wrong accusation; their cards shall remain available to refute future suggestions.                 |
| F9  | The game shall reject suggestions and accusations referencing unknown suspects, weapons, or rooms.                                              |
| F10 | The game shall reject any action attempted by a player who is not the current player.                                                            |
| F11 | The game shall reject suggestions and accusations from eliminated players.                                                                       |
| F12 | When a suggestion is made, the game shall move the named suspect and weapon tokens into the suggester's current room, and they shall remain there after the refutation walk completes. |
| F13 | The game shall reject any action once the game is over.                                                                                          |
| F14 | The game shall end as a draw if every player has been eliminated.                                                                                |
| F15 | The game shall declare the last remaining active player as the winner via `check_for_winner`.                                                   |
| F16 | The game shall provide a `validate_game_state` function that detects card-count mismatches, duplicates, malformed solutions, and out-of-range turn indices. |

### AI / autonomous-player requirements

| ID  | Requirement                                                                                                                                    |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| F20 | The game shall allow each player slot to be configured as Human or AI on the Setup screen, with any mix accepted (subject to the 3–6 player count rule). |
| F21 | An AI player shall take its full turn automatically: roll a die, move to a legal destination, optionally make a suggestion in its current room, and optionally make an accusation. |
| F22 | An AI player shall make decisions using only information it is allowed to know: its own hand, cards shown directly to it during refutation, and public suggestion outcomes. It shall not read the hidden solution. |
| F23 | An AI player shall accuse only when its private notes have narrowed each card type to a single remaining candidate.                              |

## Functional requirements (desirable — "should")

| ID  | Requirement                                                                  |
| --- | ---------------------------------------------------------------------------- |
| F17 | The game should reveal the solution on the EndScreen.                         |
| F18 | The game should allow the player to start a new game from the EndScreen.     |
| F19 | The game should record each move and each suggestion in `turn_history`.       |
| F24 | The in-game suggestion log should surface the F12 token movement so the side effect is visible to a player and a marker (TC-25 visibility line). |

## Non-functional requirements

| ID  | Requirement                                                                  |
| --- | ---------------------------------------------------------------------------- |
| NF1 | The GUI shall display clear prompts and surface engine errors to the player. |
| NF2 | The game shall not crash for any valid sequence of user actions.              |
| NF3 | `pytest -q` shall complete in under 5 seconds on a developer laptop.          |
| NF4 | The engine package (`src/game/`) shall not import Pygame.                    |

## Domain requirements (informational)

| ID  | Domain rule (Cluedo)                                                                                          |
| --- | ------------------------------------------------------------------------------------------------------------- |
| D1  | There are 6 suspects, 6 weapons, 9 rooms — 21 cards total.                                                     |
| D2  | The dealer (in our digital version, the engine) places one of each card type into the murder envelope.        |
| D3  | A suggestion is made from a room and asks one suspect, one weapon, and the room.                               |
| D4  | A player may make at most one accusation; a wrong one removes them from active play.                           |
| D5  | An eliminated player still refutes suggestions with the cards in their hand.                                   |

## Out of scope (explicitly not built)

The following items were considered and explicitly excluded from MVP. Decisions are recorded in `docs/decisions.md`.

- Save / load games.
- Networked multiplayer (the `ScreenManager.game_state` class attribute would need to become a per-session object).
- Animated tokens, sound effects, mobile or web build.
- Detective-notes sheet rendered for human players. (The AI keeps its own private notes — see F22 — but surfacing them would change the privacy rules in ADR-003.)
- Secret passages between corner rooms — the user requirements describe them; we omitted the `passage` relation from `ROOM_LAYOUT` and they are documented as future work in the group report.
- Per-character primacy of Miss Scarlet's first-turn rule. The engine treats free-text player names rather than binding players to suspect characters; documented as a known limitation.
- Initial data upload from external files for board/player/customisation (Section 5 spec item; deferred for future iteration).

## Mapping to test evidence

Every functional and non-functional requirement above is exercised by at least one automated unit test in `tests/test_engine.py`, `tests/test_models.py`, or `tests/test_ai.py`, and is documented as a system test row in `docs/testing/system_test_report.md`. Cross-references are visible in the system test report's "Unit refs" column. The total at submission is **116 unit tests** passing in well under one second.
