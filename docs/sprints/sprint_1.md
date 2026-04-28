# Sprint 1 — Foundation & Engine Core

## 1) Summary data

| Field                | Value                          |
| -------------------- | ------------------------------ |
| Team number          | 53                             |
| Sprint technical lead| Maysarah                       |
| Sprint start date    | 2026-02-23                     |
| Sprint end date      | 2026-03-08                     |

## 2) Individual key contributions

| Team member  | Key contribution(s)                                                                                                                                            |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Adam         | Repository scaffold and folder structure; user stories F1–F8 with acceptance criteria; Discord server setup with channels (`#announcements`, `#standup`, `#dev`, `#qa-testing`, `#decisions`); kickoff meeting minutes (2026-02-25), Sprint 1 midpoint minutes (2026-03-04), and Sprint 1 review minutes (2026-03-09); decision log entries.                                                                                                                  |
| Floyd        | Pygame skeleton — `main.py`, `ScreenManager`, `MainMenuScreen`; engine API contract co-author with Maysarah; Python and Git setup support for team members who hit installation issues at the Sprint 1 midpoint.                                                                                                                                                                                                                                          |
| Maysarah     | `models.py` (`Card`, `Player`, `GameState`, `RefuteResult`, `AccusationResult` dataclasses); `deck.py` (canonical card constants, `create_deck`, `verify_deck`); `engine.new_game`, `next_turn`, `get_current_player`; deal-and-solution bugfix during the Sprint 1 review demo.                                                                                                                                                                                  |
| Nasser       | Initial title-screen mockups; colour palette exploration (flat dark-blue palette adopted by the team).                                                                                                                                                                                                                                                                                                                                                       |
| Abdurrahman  | First pass on the system test report template using requirement IDs F1–F8; unit tests for F1–F3.                                                                                                                                                                                                                                                                                                                                                            |

## 3) User stories / task cards

The following user stories were selected from the user requirements document for this sprint. They were prioritised at the kickoff meeting on 2026-02-25.

> **F1 — Solution selection.** "As a player, I want the game to set up automatically with a hidden solution so I do not have to track which cards were removed."

> **F2 — Fair deal.** "As a player, I want the remaining cards to be dealt fairly so the game is balanced."

> **F3 — Turn order.** "As a player, I want turns to cycle in order so we know who is up next."

Task cards (priority H = high, M = medium):

| ID  | Card                                                       | Priority |
| --- | ---------------------------------------------------------- | -------- |
| TC1 | `Card`, `Player`, `GameState` data classes                 | H        |
| TC2 | `create_deck()` returns the 21 canonical cards             | H        |
| TC3 | `new_game(names)` validates 3–6 players and creates state  | H        |
| TC4 | `next_turn` advances and skips eliminated players          | H        |
| TC5 | Pygame window + `ScreenManager` + `MainMenuScreen`         | M        |

## 4) Requirements analysis

**Functional (mandatory — "shall"):**

- F1 — the solution dictionary shall have exactly one suspect, one weapon, and one room.
- F2 — all 18 non-solution cards shall be dealt; no card shall be lost or duplicated.
- F3 — `next_turn` shall advance by one active index, wrap, and skip eliminated players.
- F0a — `new_game` shall reject fewer than 3 or more than 6 players.

**Non-functional (mandatory — "shall"):**

- NF1 — `pytest -q` shall complete in under 5 seconds.
- NF2 — engine code shall not import Pygame (the engine must be testable without a display).

**Domain:**

- D1 — Cluedo decks consist of 6 suspects, 6 weapons, and 9 rooms (= 21 cards).
- D2 — One of each card type forms the hidden solution; the rest is dealt to players.

## 5) Design

The design decisions for Sprint 1 were:

- Engine and GUI are separate packages (`game.*` and `ui.*`). The engine has zero Pygame imports.
- Engine functions take a `GameState` and a `Player`; they mutate the state in place and return either `None` or a result dataclass.
- `RefuteResult` and `AccusationResult` are dataclasses, not dicts (agreed at the Sprint 1 midpoint meeting on 2026-03-04 for type safety and IDE support).
- Deck card constants live only in `deck.py` — single source of truth for suspects, weapons, and rooms.
- All engine functions raise `ValueError` (not bare `Exception`) for illegal input, with descriptive messages (agreed 2026-03-04).

The full architecture diagram is in `docs/design/architecture.md`. The class diagram for the engine is in `docs/design/class_diagram.md`.

## 6) Test plan and evidence of testing

Unit tests added in Sprint 1, mapped to requirement IDs:

| Test                                                | Maps to | Result |
| --------------------------------------------------- | ------- | ------ |
| `test_card_stores_type_and_name`                    | F1      | Pass   |
| `test_player_default_*` (4 tests)                   | F1      | Pass   |
| `test_solution_has_one_suspect/weapon/room`         | F1      | Pass   |
| `test_solution_has_exactly_three_keys`              | F1      | Pass   |
| `test_all_cards_dealt_no_loss`                      | F2      | Pass   |
| `test_no_duplicate_cards_in_hands`                  | F2      | Pass   |
| `test_solution_cards_not_in_any_hand`               | F2      | Pass   |
| `test_next_turn_advances_index`                     | F3      | Pass   |
| `test_next_turn_wraps_around`                       | F3      | Pass   |
| `test_next_turn_skips_eliminated_player`            | F3      | Pass   |
| `test_next_turn_skips_multiple_eliminated_players`  | F3      | Pass   |
| `test_deal_fairness_three_players`                  | F2      | Pass   |
| `test_deal_fairness_six_players`                    | F2      | Pass   |
| `test_new_game_rejects_*` (4 tests)                 | F0a     | Pass   |

`pytest -q` reports 33 passed at the end of Sprint 1.

System test mapping rows for F1–F3 are in `docs/testing/system_test_report.md`.

**Boundary conditions tested:** exactly 3 players (minimum), exactly 6 players (maximum), 2 players (rejected), 7 players (rejected), empty player names (rejected), duplicate player names (rejected).

## 7) Summary of sprint

**Did we achieve our objectives?** Yes. The engine core is in place with all Sprint 1 tests passing, and a Pygame window opens on the title screen with Start and Quit buttons working.

**Is there a working prototype?** Yes — `python -m src.main` opens a window with Start and Quit. The engine is fully usable from a Python REPL.

**What went well?** Locking the engine API contract early in the sprint (agreed 2026-03-04) meant Floyd could build the GUI skeleton in parallel without conflicts. Naming the cards in the American Cluedo style ("Miss Scarlet", "Knife", "Wrench") made tests readable. Adam's repo scaffold and Discord channel structure made async coordination smooth from day one.

**What did not go well?** Two team members had Python and Git setup issues at the start of the sprint (Microsoft Store stub problem on Windows, Git branching unfamiliarity). This was resolved at the Sprint 1 midpoint meeting on 2026-03-04 with a setup checklist Floyd pinned in `#dev`. Initial deal logic also dropped solution cards back into the deal pool — caught by the F2 test before any merge to main, and fixed live during the Sprint 1 review demo. Lesson: write tests for invariants you care about *before* implementing.

**Customer feedback?** No formal customer feedback this sprint. Adam (PO) checked the Canvas discussion thread and confirmed Sprint 1 scope (engine core only, no GUI gameplay yet) is acceptable.
