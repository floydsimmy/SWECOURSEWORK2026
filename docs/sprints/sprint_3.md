# Sprint 3 — Robustness & Validation

## 1) Summary data

| Field                | Value                          |
| -------------------- | ------------------------------ |
| Team number          | (assigned)                     |
| Sprint technical lead| Maysarah                       |
| Sprint start date    | 2026-03-02                     |
| Sprint end date      | 2026-03-15                     |

## 2) Individual key contributions

| Team member | Key contribution(s)                                                 |
| ----------- | ------------------------------------------------------------------- |
| Floyd       | EndScreen polish (solution reveal + Play Again / Main Menu), button hover states, message-history panel, MessageBox component. |
| Maysarah    | Validation: invalid suspect/weapon/room, wrong-turn guards, empty/duplicate names, action-after-game-over, draw / last-standing logic, `get_turn_summary`, `turn_history`, `reset_game`, `validate_game_state`, `verify_deck`. |
| Member C    | Acceptance criteria for F9-F16 and NF2; sign-off on edge cases. |
| Member D    | 35+ new system test cases; full regression run; bug log audit. |
| Member E    | Sprint 3 start/end docs; group-report skeleton drafted. |

## 3) User stories / task cards

> "As a player, I want clear errors when I do something illegal (out
> of turn, invalid room name, eliminated) so I learn the rules and the
> game doesn't crash." — F9-F12, NF1

> "As a developer / tester, I want to validate a GameState at any point
> so we can catch corruption before it hides a bug." — F16

| ID   | Card                                                          | Priority |
| ---- | ------------------------------------------------------------- | -------- |
| TC12 | All actions reject unknown suspect / weapon / room names      | H        |
| TC13 | Wrong-turn raises ValueError                                  | H        |
| TC14 | Eliminated-cannot-suggest / accuse                            | H        |
| TC15 | Action-after-game-over raises ValueError("already over")      | H        |
| TC16 | Draw path: all players eliminated -> game_over, winner=None   | H        |
| TC17 | Last-player-standing path via `check_for_winner`              | H        |
| TC18 | `get_turn_summary` + `turn_history`                            | M        |
| TC19 | `reset_game`, `validate_game_state`, `verify_deck`             | M        |

## 4) Requirements analysis

Functional:
- F9 (shall): unknown suspect/weapon/room names are rejected with a
  matching word in the error.
- F10 (shall): only the current player can move/suggest/accuse.
- F11 (shall): eliminated players cannot suggest or accuse.
- F12 (shall): no actions are permitted once `game_over` is True.
- F13 (shall): if all players are eliminated, the game ends as a draw.
- F14 (shall): if only one player remains active, `check_for_winner`
  returns them as the winner.
- F15 (shall): `turn_history` records each move and suggestion.
- F16 (shall): `validate_game_state` detects: missing/extra cards,
  duplicates, malformed solution, out-of-bounds turn index.

Non-functional:
- NF2 (shall): the game runs without crashing for any sequence of valid
  user actions.

## 5) Design

No new architecture. Two small additions:
- `turn_history: list[dict]` on `GameState` (default empty).
- `get_turn_summary(state) -> dict` for the UI log panel.

`validate_game_state` was given a strict order of checks so each test
case can hit one error at a time:

1. Solution shape (3 keys exactly).
2. Total card count = 21.
3. No duplicate (card_type, name) pairs.
4. `verify_deck` over the union (catches any non-canonical cards).
5. `current_turn_index` is in bounds.

## 6) Test plan and evidence of testing

Unit tests added: 28 (cumulative ~91). All pass.

System tests run this sprint (representative subset; full table in
`docs/testing/system_test_report.md`):

| Ref   | Req | Pass/Fail |
| ----- | --- | --------- |
| ST-09 | F9  | Pass |
| ST-10 | F10 | Pass |
| ST-11 | F11 | Pass |
| ST-12 | F12 | Pass |
| ST-13 | F13 | Pass |
| ST-14 | F14 | Pass |
| ST-15 | F15 | Pass |
| ST-16 | F16 | Pass |
| ST-NF2 | NF2 | Pass |

Bug log: 1 regression caught (next_turn skipped one too many; fixed
within an hour of detection).

## 7) Summary of sprint

**Objectives met?** Yes. The engine is now substantially more robust;
the GUI shows clear errors for every illegal action.

**Prototype?** Yes — full playable build with end-screen and edge cases.

**What went well?** The 91-test suite gives confidence on every change.
Adding `validate_game_state` led directly to discovering one stale
assumption in our deal logic that wasn't caught by the F2 tests.

**What did not go well?** Some redundancy crept in: both `validate_game_state`
and `verify_deck` independently enumerate the canonical card set. We
chose to keep both for now (different abstraction layers), and
documented the intentional duplication.

**Customer feedback?** None.
