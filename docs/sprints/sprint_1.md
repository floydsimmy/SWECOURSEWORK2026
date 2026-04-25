# Sprint 1 — Foundation & Engine Core

## 1) Summary data

| Field                | Value                          |
| -------------------- | ------------------------------ |
| Team number          | (assigned)                     |
| Sprint technical lead| Maysarah                       |
| Sprint start date    | 2026-02-02                     |
| Sprint end date      | 2026-02-15                     |

## 2) Individual key contributions

| Team member | Key contribution(s)                                                |
| ----------- | ------------------------------------------------------------------ |
| Floyd       | Repo scaffold, `pytest.ini`, package `__init__.py`s, Pygame skeleton (`main.py`, `ScreenManager`, MainMenuScreen). Engine API contract co-author. |
| Maysarah    | `models.py` (Card, Player, GameState, RefuteResult, AccusationResult), `deck.py` (constants, `create_deck`, `verify_deck`), `engine.new_game`, `next_turn`, `get_current_player`. Unit tests for F1-F3. |
| Member C    | User stories F1-F8 with acceptance criteria; backlog priority. |
| Member D    | System test plan v0.1 with requirement IDs F1-F8 and the test-case template. |
| Member E    | Kickoff meeting minutes; Sprint 1 start/end docs; Discord channels and decisions log. |

## 3) User stories / task cards (selected for this sprint)

> "As a player, I want the game to set up automatically with a hidden
> solution so I don't have to track which cards were removed." — F1

> "As a player, I want the remaining cards to be dealt fairly so the
> game is balanced." — F2

> "As a player, I want turns to cycle in order so we know who is up
> next." — F3

Task cards (priority H = high, M = medium):

| ID  | Card                                                      | Priority |
| --- | --------------------------------------------------------- | -------- |
| TC1 | `Card`, `Player`, `GameState` data classes                | H        |
| TC2 | `create_deck()` returns the 21 canonical cards            | H        |
| TC3 | `new_game(names)` validates 3-6 players + creates state   | H        |
| TC4 | `next_turn` advances and skips eliminated players         | H        |
| TC5 | Pygame window + ScreenManager + MainMenu                  | M        |

## 4) Requirements analysis

Functional (mandatory unless noted):
- F1 (shall): solution dict has exactly one suspect, one weapon, one room.
- F2 (shall): all 18 non-solution cards are dealt; no card is duplicated or lost.
- F3 (shall): `next_turn` advances by one active index, wraps, skips eliminated.
- F0a (shall): `new_game` rejects fewer than 3 or more than 6 players.

Non-functional:
- NF1 (shall): `pytest -q` runs in under 5 seconds.
- NF2 (shall): engine code has no Pygame imports (testable without a display).

Domain:
- Cluedo cards: 6 suspects, 6 weapons, 9 rooms (= 21 cards). Solution
  is one of each.

## 5) Design

See `docs/design/architecture.md` and `docs/design/class_diagram.md`.
Key decisions made in this sprint:

- Engine and GUI are separate packages (`game.*` vs `ui.*`). The engine
  has zero Pygame imports.
- Engine functions take a `GameState` and a `Player`; they mutate state
  in place and return either `None` or a result dataclass.
- `RefuteResult` and `AccusationResult` are dataclasses (not dicts).
- Deck constants live in `deck.py` only — single source of truth.

## 6) Test plan and evidence of testing

Unit tests added in Sprint 1 (`tests/test_models.py` + `tests/test_engine.py`):

| Test                                              | Maps to | Result |
| ------------------------------------------------- | ------- | ------ |
| `test_card_stores_type_and_name`                  | F1      | Pass   |
| `test_player_default_*` (4 tests)                 | F1      | Pass   |
| `test_solution_has_one_suspect/weapon/room`       | F1      | Pass   |
| `test_solution_has_exactly_three_keys`            | F1      | Pass   |
| `test_all_cards_dealt_no_loss`                    | F2      | Pass   |
| `test_no_duplicate_cards_in_hands`                | F2      | Pass   |
| `test_solution_cards_not_in_any_hand`             | F2      | Pass   |
| `test_next_turn_advances_index`                   | F3      | Pass   |
| `test_next_turn_wraps_around`                     | F3      | Pass   |
| `test_next_turn_skips_eliminated_player`          | F3      | Pass   |
| `test_next_turn_skips_multiple_eliminated_players`| F3      | Pass   |
| `test_deal_fairness_three_players`                | F2      | Pass   |
| `test_deal_fairness_six_players`                  | F2      | Pass   |
| `test_new_game_rejects_*` (4 tests)               | F0a     | Pass   |

Evidence: `pytest -q` reports `33 passed` at end of Sprint 1.

System test mapping is collected in `docs/testing/system_test_report.md`
(rows F1-F3).

## 7) Summary of sprint

**Did we achieve the objectives?** Yes. The engine core is in place,
all Sprint 1 tests pass, and a Pygame window opens with the title
screen.

**Working prototype?** Yes — `python src/main.py` opens a window with Start
/ Quit. The engine is fully usable from the REPL.

**What went well?** Locking the engine API up front meant Floyd could
build the GUI skeleton in parallel without conflicts. Naming the cards
in the American Cluedo style ("Miss Scarlet", "Knife", "Wrench") made
tests far more readable than the British names from the spec.

**What did not go well?** Initial deal logic dropped the solution
cards back into the deck, breaking the count test. Caught immediately
by the F2 test before any merge — the test suite paid for itself on
day one.

**Customer feedback?** Member C confirmed via Canvas that the Sprint 1
scope (engine core, no GUI gameplay yet) is acceptable.
