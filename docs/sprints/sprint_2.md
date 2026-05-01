# Sprint 2 — Core Gameplay Mechanics

## 1) Summary data

| Field                | Value                          |
| -------------------- | ------------------------------ |
| Team number          | 53                             |
| Sprint technical lead| Floyd                          |
| Sprint start date    | 2026-03-09                     |
| Sprint end date      | 2026-03-29                     |

> **Note on sprint length.** Sprint 2 was extended by one week at the midpoint meeting on 2026-03-18, from a planned 14-day sprint to 21 days. The extension was needed to absorb the integration work for the keep-in-scope decision on grid + dice movement and the AI player (see §5 / §7 and ADR-006 in `docs/decisions.md`). The PO (Adam) signed off on the extension and updated the sprint planning documents accordingly.

## 2) Individual key contributions

| Team member  | Key contribution(s)                                                                                                                                                                                                                                       |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Adam         | Sprint planning and the keep-in-scope decision on grid + dice movement and the AI player (ADR-006 sign-off, recorded in `docs/decisions.md`); Sprint 2 midpoint minutes (2026-03-18), Team Progress Review form (2026-03-25), Sprint 2 review minutes (2026-03-30); group-report skeleton drafted; Canvas check-ins. |
| Floyd        | Owned `SetupScreen` with the per-slot Human/AI toggle; led the implementation of `GameScreen` integration with hand, room, and log panels and action buttons; led the design and implementation of the **grid pathfinder** in `engine.py` (`roll_die`, `legal_moves_for_roll` BFS over corridor tiles, `move_by_dice`) and the static `ROOM_LAYOUT`, `ROOM_DOORS`, `CHARACTER_START_TILES` tables; `ScreenManager` wiring; owned `EndScreen` v1; integration testing across the full Setup → Game → End flow.                                                                                                                                                          |
| Maysarah     | Led the design and implementation of `move_to_room`, `make_suggestion`, `make_accusation`; refutation walk in turn order including eliminated players; auto-advance on accusation (correct or wrong); `check_for_winner`; in-meeting bugfix for wrong-turn protection on `move_to_room` during the Sprint 2 review demo.                                                                                                                          |
| Nasser       | Owned the UI component library — `Button`, `TextInput`, `PopupSelect`, `MessageBox`; `GameScreen` layout (sidebar, log panel, action button cluster); owned the `Board` renderer in `src/ui/gui.py` (24 × 24 grid, room shapes, doors, player tokens, dice-move highlight overlay); colour-palette polish.                                                                                                                                                                                                                                  |
| Abdurrahman  | System tests for F4–F8 in `docs/testing/system_test_report.md`; GitHub Issues bug log set up; in-sprint regression runs.                                                                                                                                                                                                                                                                              |

## 3) User stories / task cards

> **F4 — Movement.** "As a player, I want to roll a die and move that many squares across the board, ending in either a corridor tile or a room reached through a door, so I can make a suggestion from a chosen room."

> **F5 / F6 — Suggestion + Refutation.** "As a player in a room, I want to make a suggestion that other players must refute, so I can narrow down the solution."

> **F7 / F8 — Accusation.** "As a player, I want to make an accusation that ends my participation if wrong, so the game has stakes."

| ID  | Card                                                                       | Priority |
| --- | -------------------------------------------------------------------------- | -------- |
| TC6 | `move_to_room` validates room and current player                           | H        |
| TC6b| Grid pathfinder: `roll_die`, `legal_moves_for_roll`, `move_by_dice`; static board layout | H |
| TC7 | `make_suggestion` checks room, names; refutation walks turn order          | H        |
| TC8 | `make_accusation` updates winner / eliminates and auto-advances            | H        |
| TC9 | `SetupScreen` accepts 3–6 names, rejects duplicates, per-slot Human/AI toggle | H     |
| TC10| `GameScreen` wires Roll Dice / Suggest / Accuse / EndTurn to engine        | H        |
| TC10b| `Board` renderer (24x24 grid, doors, tokens, dice-move highlight)         | H        |
| TC11| `EndScreen` reveals the solution                                            | M        |

## 4) Requirements analysis

**Functional (mandatory — "shall"):**

- F4 — a player shall be able to roll a six-sided die and move that many squares along the board, ending in either a corridor tile or a room reached via a door (per the user requirements). Pathfinding is BFS over the 24 × 24 grid, blocked by other players' tiles.
- F5 — a suggestion shall use the suggesting player's current room.
- F6 — refutation shall walk other players in turn order from the suggester's left, including eliminated players (D5), and reveal exactly one matching card to the suggester.
- F7 — a correct accusation shall end the game with that player as the winner.
- F8 — a wrong accusation shall eliminate the player; their cards shall remain available to refute future suggestions.

**Non-functional (mandatory — "shall"):**

- NF1 — the GUI shall be usable end-to-end without crashes for valid input.

## 5) Design

Design artefacts produced or updated this sprint (in `docs/design/`):

- Sequence diagram for the Suggestion / Refutation flow (`sequence_diagram.md`).
- Class diagram updated with the action-result dataclasses (`class_diagram.md`).

Key design decisions taken at the Sprint 2 midpoint meeting (2026-03-18):

- **Refutation order** is "from the suggester's left, including eliminated players" — modulo arithmetic on the player list. The first matching card stops the walk. Eliminated players are *included* in the walk because D5 says they still refute.
- **`make_accusation` always calls `next_turn`** before returning, even on a correct accusation. This makes the "Game is already over" guard fire deterministically when the next player tries to act.
- **`ScreenManager` holds `game_state` as a class attribute** so all screens share it. Pragmatic for a single-game prototype; flagged for future refactor if scaled.
- **Grid + dice movement KEPT in MVP scope.** Replaces the "dropdown only" simplification raised earlier in the sprint. Sprint 2 will deliver the full BFS pathfinder; Floyd owns it. Decision recorded in `docs/decisions.md` (ADR-006).
- **AI player KEPT in scope, deferred to Sprint 3.** Sprint 2 focuses on the human gameplay loop and grid + dice; the AI module lands in Sprint 3 once the engine has been hardened. Decision recorded in `docs/decisions.md` (ADR-006).

## 6) Test plan and evidence of testing

Unit tests added in Sprint 2 covered F4–F8. All passing. Note that the grid + dice pathfinder is exercised end-to-end via the AI's turn loop in Sprint 3 (`tests/test_ai.py::test_ai_uses_only_legal_room_moves`, `test_ai_dice_rolls_are_one_to_six`, etc.) and via the F4 system test rows; we did not write narrow unit tests on `legal_moves_for_roll` itself in this sprint, which is called out as a lesson in §7.

System tests run this sprint:

| Ref    | Req | Pass/Fail | Notes                                                       |
| ------ | --- | --------- | ----------------------------------------------------------- |
| ST-04  | F4  | Pass      | Roll dice, move into Kitchen succeeds                       |
| ST-05  | F5  | Pass      | Suggestion offered only from a room                         |
| ST-06  | F6  | Pass      | Refuter holding the suggested weapon shows it               |
| ST-06b | F6  | Pass      | Refutation walks include an eliminated player whose hand still matches |
| ST-07  | F7  | Pass      | Correct accusation triggers `EndScreen`                     |
| ST-08  | F8  | Pass      | Wrong accusation eliminates and auto-advances               |

**Bugs found and fixed in-sprint (3 total):**

1. Wrong-turn protection missing on `move_to_room` (caught at Sprint 2 review demo, fixed live by Maysarah).
2. Eliminated-suggest order — eliminated check ran after room check, so eliminated players got an unhelpful error message. Reordered.
3. `EndScreen` rendered "None" as winner when the game ended by all players being eliminated. Fixed by adding an explicit "draw" path.

## 7) Summary of sprint

**Did we achieve our objectives?** Yes, with a one-week extension. A complete game can be played end-to-end from setup through to the end screen. The engine implements the full F4–F8 ruleset including grid + dice movement; the AI is deferred to Sprint 3 per ADR-006.

**Is there a working prototype?** Yes — playable.

**What went well?** Engine API was already frozen from Sprint 1, so wiring the screens and the new grid pathfinder to the engine was a clean exercise — both consumed the same public interface. The `RefuteResult` and `AccusationResult` dataclasses made the GameScreen log easy to write. The keep-in-scope decisions on grid + dice and AI (ADR-006) were made cleanly mid-sprint with PO sign-off rather than being chased on intuition.

**What did not go well?** The grid pathfinder's first cut had a corner-case bug — the BFS counted the door tile twice when starting in a room, so a roll of `n` showed reachable rooms at distance `n+1`. The bug shipped at the end of Sprint 2 because the F4 system test row only checked "legal room reachable somewhere"; the off-by-one was caught by Abdurrahman's tighter system-test pass in Sprint 3 and Floyd fixed it there. Lesson: write a unit test on the BFS distance directly, not only via system tests through the GUI. Sprint 2 also had to be extended by a week (planned 14 days, actual 21 days) — an unavoidable cost of the keep-in-scope decision, but a slippage agile teams usually want to avoid.

**Customer feedback?** None blocking. PO confirmed via Canvas that the kept-in-scope grid + dice movement and the AI deferral into Sprint 3 are acceptable for the MVP plan.
