# Sprint 2 — Core Gameplay Mechanics

## 1) Summary data

| Field                | Value                          |
| -------------------- | ------------------------------ |
| Team number          | (assigned)                     |
| Sprint technical lead| Floyd                          |
| Sprint start date    | 2026-02-16                     |
| Sprint end date      | 2026-03-01                     |

## 2) Individual key contributions

| Team member | Key contribution(s)                                                |
| ----------- | ------------------------------------------------------------------ |
| Floyd       | SetupScreen (player-name entry with validation), GameScreen with hand/room/log panels and action buttons, ScreenManager wiring, EndScreen v1. |
| Maysarah    | `move_to_room`, `make_suggestion`, `make_accusation`, refutation order with elimination skip, auto-advance on accusation, `check_for_winner`. |
| Member C    | Acceptance criteria checklists for F4-F8 + NF1; Canvas check-ins. |
| Member D    | System tests F4-F8 written and executed; bug log on GitHub Issues. |
| Member E    | Sprint 2 start/end docs; Decision log entries (grid-movement and AI descope). |

## 3) User stories / task cards

> "As a player in a room, I want to make a suggestion that other players
> must refute, so I can narrow down the solution." — F5, F6

> "As a player, I want to make an accusation that ends my participation
> if wrong, so the game has stakes." — F7, F8

| ID  | Card                                                                       | Priority |
| --- | -------------------------------------------------------------------------- | -------- |
| TC6 | `move_to_room` validates room and current player                           | H        |
| TC7 | `make_suggestion` checks room, names; refutation walks turn order          | H        |
| TC8 | `make_accusation` updates winner / eliminates and auto-advances            | H        |
| TC9 | SetupScreen accepts 3-6 names, rejects duplicates                          | H        |
| TC10| GameScreen wires Move/Suggest/Accuse/EndTurn to engine                     | H        |
| TC11| EndScreen reveals the solution                                              | M        |

## 4) Requirements analysis

Functional:
- F4 (shall): a player can move to any room (simplified: any of the 9).
- F5 (shall): a suggestion uses the player's current room.
- F6 (shall): refutation walks active players in turn order, first match wins.
- F7 (shall): a correct accusation ends the game with that player as winner.
- F8 (shall): a wrong accusation eliminates the player; their cards stay in hand.

Non-functional:
- NF1 (shall): the GUI is usable end-to-end without crashes for valid input.

## 5) Design

Class diagram and sequence diagram for the suggestion / refutation
flow are in `docs/design/`. Key decisions:

- Refutation order is "from current player's left, skipping eliminated",
  i.e. modulo arithmetic in the player list. First matching card stops
  the walk.
- `make_accusation` always calls `next_turn` before returning, even on a
  correct accusation. This lets the next player's "Game is over" guard
  fire deterministically.
- ScreenManager holds `game_state` as a class attribute so all screens
  share it. Pragmatic for a prototype; flagged for refactor if we ever
  scale beyond one game at a time.

## 6) Test plan and evidence of testing

Unit tests added: 30 (cumulative ~63). All pass.

System tests run this sprint:

| Ref | Req | Pass/Fail | Notes |
| --- | --- | --------- | ----- |
| ST-04 | F4 | Pass | Drop-down move into Kitchen succeeds |
| ST-05 | F5 | Pass | Suggestion offered only from a room |
| ST-06 | F6 | Pass | Bob refutes when holding the suggested weapon |
| ST-06b | F6 | Pass | Eliminated player skipped during refutation |
| ST-07 | F7 | Pass | Correct accusation triggers EndScreen |
| ST-08 | F8 | Pass | Wrong accusation eliminates + auto-advances |

Bugs found and fixed in-sprint: 3 (wrong-turn protection on `move`,
eliminated-suggest order, EndScreen rendering for draw path).

## 7) Summary of sprint

**Objectives met?** Yes. A complete game can be played from setup to
end-screen.

**Prototype?** Yes — playable.

**What went well?** Engine API was already frozen, so wiring screens
to the engine was a pure plumbing exercise. The `RefuteResult` and
`AccusationResult` dataclasses made the GameScreen log easy to write.

**What did not go well?** We initially tried grid-based movement; it
was descoped mid-sprint after the PO ruled it out of MVP scope. Some
exploratory work was thrown away. Lesson: agree scope at the sprint
start and resist the temptation to "just try" out-of-scope features.

**Customer feedback?** None blocking. PO confirmed the descope was
acceptable.
