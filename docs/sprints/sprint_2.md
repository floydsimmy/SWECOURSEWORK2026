# Sprint 2 — Core Gameplay Mechanics

## 1) Summary data

| Field                | Value                          |
| -------------------- | ------------------------------ |
| Team number          | 53                             |
| Sprint technical lead| Floyd                          |
| Sprint start date    | 2026-03-09                     |
| Sprint end date      | 2026-03-29                     |

> **Note on sprint length.** Sprint 2 was extended by one week at the midpoint meeting on 2026-03-18, from a planned 14-day sprint to 21 days. The extension was needed to absorb integration work that ran longer than estimated and to handle the descope of grid-based movement (see §7). The PO (Adam) signed off on the extension and updated the sprint planning documents accordingly.

## 2) Individual key contributions

| Team member  | Key contribution(s)                                                                                                                                                                                                                                       |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Adam         | Sprint planning and scope decisions — grid-movement descope sign-off and AI descope sign-off (recorded in `docs/decisions.md`); Sprint 2 midpoint minutes (2026-03-18), Team Progress Review form (2026-03-25), Sprint 2 review minutes (2026-03-30); group-report skeleton drafted; Canvas check-ins. |
| Floyd        | `SetupScreen` (player-name entry with validation); `GameScreen` integration with hand, room, and log panels and action buttons; `ScreenManager` wiring across all screens; `EndScreen` v1; integration testing across the full Setup → Game → End flow.                                                                                                                                                          |
| Maysarah     | `move_to_room`, `make_suggestion`, `make_accusation`; refutation walk in turn order with elimination-skip; auto-advance on accusation (correct or wrong); `check_for_winner`; in-meeting bugfix for wrong-turn protection on `move_to_room` during the Sprint 2 review demo.                                                                                                                          |
| Nasser       | UI component library — `Button`, `TextInput`, `DropdownMenu`, `MessageBox`; `GameScreen` layout (sidebar, log panel, action button cluster); colour-palette polish.                                                                                                                                                                                                                                  |
| Abdurrahman  | System tests for F4–F8 in `docs/testing/system_test_report.md`; GitHub Issues bug log set up; in-sprint regression runs.                                                                                                                                                                                                                                                                              |

## 3) User stories / task cards

> **F4 — Movement.** "As a player, I want to move to a room so I can make a suggestion from there."

> **F5 / F6 — Suggestion + Refutation.** "As a player in a room, I want to make a suggestion that other players must refute, so I can narrow down the solution."

> **F7 / F8 — Accusation.** "As a player, I want to make an accusation that ends my participation if wrong, so the game has stakes."

| ID  | Card                                                                       | Priority |
| --- | -------------------------------------------------------------------------- | -------- |
| TC6 | `move_to_room` validates room and current player                           | H        |
| TC7 | `make_suggestion` checks room, names; refutation walks turn order          | H        |
| TC8 | `make_accusation` updates winner / eliminates and auto-advances            | H        |
| TC9 | `SetupScreen` accepts 3–6 names, rejects duplicates                        | H        |
| TC10| `GameScreen` wires Move / Suggest / Accuse / EndTurn to engine             | H        |
| TC11| `EndScreen` reveals the solution                                            | M        |

## 4) Requirements analysis

**Functional (mandatory — "shall"):**

- F4 — a player shall be able to move to any of the 9 named rooms (simplified from the user requirements: dropdown room selection, no grid pathing — see §7 and `docs/decisions.md` ADR for the descope rationale).
- F5 — a suggestion shall use the suggesting player's current room.
- F6 — refutation shall walk active players in turn order from the suggester's left, skipping eliminated players, and reveal exactly one matching card to the suggester.
- F7 — a correct accusation shall end the game with that player as the winner.
- F8 — a wrong accusation shall eliminate the player; their cards shall remain available to refute future suggestions.

**Non-functional (mandatory — "shall"):**

- NF1 — the GUI shall be usable end-to-end without crashes for valid input.

## 5) Design

Design artefacts produced or updated this sprint (in `docs/design/`):

- Sequence diagram for the Suggestion / Refutation flow (`sequence_diagram.md`).
- Class diagram updated with the action-result dataclasses (`class_diagram.md`).

Key design decisions taken at the Sprint 2 midpoint meeting (2026-03-18):

- **Refutation order** is "from the suggester's left, skipping eliminated players" — modulo arithmetic on the player list. The first matching card stops the walk.
- **`make_accusation` always calls `next_turn`** before returning, even on a correct accusation. This makes the "Game is already over" guard fire deterministically when the next player tries to act.
- **`ScreenManager` holds `game_state` as a class attribute** so all screens share it. Pragmatic for a single-game prototype; flagged for future refactor if scaled.
- **Grid-based movement DROPPED from MVP scope.** Replaced with dropdown room selection. Decision recorded in `docs/decisions.md`.
- **AI player DROPPED from scope.** Decision recorded in `docs/decisions.md`.

## 6) Test plan and evidence of testing

Unit tests added in Sprint 2: 30 (cumulative ~63 across Sprints 1 and 2). All passing.

System tests run this sprint:

| Ref    | Req | Pass/Fail | Notes                                                       |
| ------ | --- | --------- | ----------------------------------------------------------- |
| ST-04  | F4  | Pass      | Drop-down move into Kitchen succeeds                        |
| ST-05  | F5  | Pass      | Suggestion offered only from a room                         |
| ST-06  | F6  | Pass      | Refuter holding the suggested weapon shows it               |
| ST-06b | F6  | Pass      | Eliminated player skipped during refutation                 |
| ST-07  | F7  | Pass      | Correct accusation triggers `EndScreen`                     |
| ST-08  | F8  | Pass      | Wrong accusation eliminates and auto-advances               |

**Bugs found and fixed in-sprint (3 total):**

1. Wrong-turn protection missing on `move_to_room` (caught at Sprint 2 review demo, fixed live by Maysarah).
2. Eliminated-suggest order — eliminated check ran after room check, so eliminated players got an unhelpful error message. Reordered.
3. `EndScreen` rendered "None" as winner when the game ended by all players being eliminated. Fixed by adding an explicit "draw" path.

## 7) Summary of sprint

**Did we achieve our objectives?** Yes, with a one-week extension. A complete game can be played end-to-end from setup through to the end screen. The engine implements the full F4–F8 ruleset.

**Is there a working prototype?** Yes — playable.

**What went well?** Engine API was already frozen from Sprint 1, so wiring screens to the engine was a pure plumbing exercise. The `RefuteResult` and `AccusationResult` dataclasses made the GameScreen log easy to write. The descope decisions on grid movement and AI were made cleanly mid-sprint with PO sign-off, rather than getting deferred into Sprint 3.

**What did not go well?** Floyd initially started a tile-based movement prototype during the week before the midpoint meeting; this ran into time risk quickly and was descoped at the 2026-03-18 midpoint after Adam re-read the user requirements. Roughly six person-hours of exploratory work did not ship. Lesson: agree the sprint goal at the start, resist the temptation to expand scope mid-sprint. Sprint 2 also had to be extended by a week (planned 14 days, actual 21 days) which is the kind of slippage agile teams usually want to avoid.

**Customer feedback?** None blocking. PO confirmed via Canvas that the descope of grid movement (to dropdown room selection) is acceptable for the MVP.
