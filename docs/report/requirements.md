# Requirements

Derived from the Watson Games user requirements document (Cluedo!) and
refined into testable functional, non-functional, and domain
requirements. Each ID appears verbatim in the unit and system tests.

## Functional (mandatory: "shall")

| ID  | Requirement                                                                                                  |
| --- | ------------------------------------------------------------------------------------------------------------ |
| F1  | The game shall set up with one suspect, one weapon, and one room as the hidden solution.                     |
| F2  | The game shall deal all 18 remaining cards to players such that no card is lost or duplicated.               |
| F3  | The game shall cycle turns in player order and skip eliminated players.                                       |
| F4  | The game shall allow a player to move into any of the 9 named rooms.                                          |
| F5  | The game shall use the suggesting player's current room as the room in their suggestion.                      |
| F6  | The game shall walk other players in turn order from the suggester's left, skipping eliminated, and reveal exactly one matching card to the suggester. |
| F7  | The game shall declare a player the winner when they make a correct accusation.                                |
| F8  | The game shall eliminate a player who makes a wrong accusation; their cards shall remain available to refute future suggestions. |
| F9  | The game shall reject suggestions and accusations referencing unknown suspects, weapons, or rooms.             |
| F10 | The game shall reject any action attempted by a player who is not the current player.                         |
| F11 | The game shall reject suggestions and accusations from eliminated players.                                     |
| F12 | The game shall reject any action once the game is over.                                                         |
| F13 | The game shall end as a draw if every player has been eliminated.                                              |
| F14 | The game shall declare the last remaining active player as the winner.                                         |
| F15 | The game shall record each move and each suggestion in `turn_history`.                                         |
| F16 | The game shall provide a `validate_game_state` function that detects card-count mismatches, duplicates, malformed solutions, and out-of-range turn indices. |

## Functional (desirable: "should")

| ID  | Requirement                                                                  |
| --- | ---------------------------------------------------------------------------- |
| F17 | The game should reveal the solution on the EndScreen.                        |
| F18 | The game should allow the player to start a new game from the EndScreen.    |

## Non-functional

| ID  | Requirement                                                                  |
| --- | ---------------------------------------------------------------------------- |
| NF1 | The GUI shall display clear prompts and surface engine errors to the player. |
| NF2 | The game shall not crash for any valid sequence of user actions.             |
| NF3 | `pytest -q` shall complete in under 5 seconds on a developer laptop.         |
| NF4 | The engine package shall not import Pygame.                                  |

## Domain (informational)

| ID  | Domain rule (Cluedo)                                                                                          |
| --- | ------------------------------------------------------------------------------------------------------------- |
| D1  | There are 6 suspects, 6 weapons, 9 rooms (= 21 cards).                                                         |
| D2  | The dealer (in our digital version, the engine) places one of each into the murder envelope.                   |
| D3  | A suggestion is made from a room and asks one suspect, one weapon, and the room.                               |
| D4  | A player may make at most one accusation; a wrong one removes them from active play.                           |
| D5  | An eliminated player still refutes suggestions with the cards in their hand.                                   |

## Out of scope (descoped from MVP)

- Grid-based board with adjacency rules (descoped Sprint 2).
- AI / autonomous player (descoped Sprint 2).
- Save / load games.
- Network multiplayer.
- Mobile build.

These items are documented in `docs/sprints/` decisions sections and
acknowledged in the Group Report.
