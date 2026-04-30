# Sprint 3 — Robustness, Validation & AI Stretch

## 1) Summary data

| Field                | Value                          |
| -------------------- | ------------------------------ |
| Team number          | 53                             |
| Sprint technical lead| Maysarah                       |
| Sprint start date    | 2026-03-30                     |
| Sprint end date      | 2026-04-12                     |

## 2) Individual key contributions

| Team member  | Key contribution(s)                                                                                                                                                                                                                                            |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Adam         | Sprint planning and acceptance criteria for F9–F16, NF2, and the AI requirements F20–F23; F12 token-position bug identified and added to Sprint 3 scope (PO sign-off); Sprint 3 midpoint minutes (2026-04-08), Sprint 3 review minutes (2026-04-13); group-report skeleton expanded; system test report review.                       |
| Floyd        | `EndScreen` polish (solution reveal, Play Again / Main Menu); button hover states across all screens; message-history panel on `GameScreen`; `MessageBox` component refinement; **off-by-one fix on `legal_moves_for_roll`** carried over from Sprint 2; Sprint 4 planning started in parallel (submission pack structure, video planning).                                       |
| Maysarah     | Validation suite — unknown suspect/weapon/room rejection, wrong-turn guards on every action, eliminated-cannot-act enforcement, action-after-game-over guards, draw / last-player-standing logic; **F12 fix** (suspect/weapon location tracking added to `GameState`, populated in `make_suggestion`); `get_turn_summary`, `turn_history`, `reset_game`, `validate_game_state`, `verify_deck`; **AI player module** (`src/game/ai.py`) — `RandomAIPlayerStrategy`, `take_ai_turn`, `run_ai_simulation`, `DetectiveNotes`, the privacy invariants, and the `tests/test_ai.py` file (13 tests). |
| Nasser       | Visual polish on `GameScreen` layout; hover states implementation across `Button` instances; minor cleanup of `MessageBox` rendering; AI vs Human visual differentiation in the player legend.                                                                                                                                                                                                                                                          |
| Abdurrahman  | 30+ new system test cases covering F9–F16, NF2, and the AI requirements F20–F23; full regression run; bug log audit (zero open critical bugs at sprint close); test-coverage report submitted via Discord ahead of the Sprint 3 review meeting.                                                                                                                                                                              |

## 3) User stories / task cards

> **F9–F12, NF1 — Defensive validation.** "As a player, I want clear errors when I do something illegal (out of turn, invalid room name, eliminated) so I learn the rules and the game does not crash."

> **F12 — Token movement.** "As a player making a suggestion, I expect the suspect and weapon I name to be moved into the room I am in, and to remain there afterwards."

> **F16 — State validation.** "As a developer or tester, I want to validate a `GameState` at any point so we can catch corruption before it hides a bug."

| ID    | Card                                                              | Priority |
| ----- | ----------------------------------------------------------------- | -------- |
| TC12  | All actions reject unknown suspect / weapon / room names          | H        |
| TC13  | Wrong-turn raises `ValueError`                                    | H        |
| TC14  | Eliminated cannot suggest / accuse                                 | H        |
| TC15  | Action-after-game-over raises `ValueError("already over")`         | H        |
| TC16  | Draw path: all players eliminated → game_over, winner = None       | H        |
| TC17  | Last-player-standing path via `check_for_winner`                   | H        |
| **TC18** | **F12 — suggestion moves suspect and weapon tokens into the room and they stay there** | **H** |
| TC19  | `get_turn_summary` and `turn_history`                               | M        |
| TC20  | `reset_game`, `validate_game_state`, `verify_deck`                  | M        |
| **TC21** | **AI player module — `RandomAIPlayerStrategy`, `take_ai_turn`, `run_ai_simulation`, `DetectiveNotes` invariants** | **H** (the Sprint 3 stretch goal per ADR-006) |
| TC22  | `tests/test_ai.py` covering 13 AI behaviour tests including privacy invariants | H |

## 4) Requirements analysis

**Functional (mandatory — "shall"):**

- F9 — unknown suspect/weapon/room names shall be rejected with an error message that names the offending field.
- F10 — only the current player shall be able to move, suggest, or accuse.
- F11 — eliminated players shall not be able to suggest or accuse.
- F12 — when a suggestion is made, the named suspect and weapon shall be moved into the suggester's current room, and they shall remain there after the refutation walk completes.
- F13 — no actions shall be permitted once `game_over` is True.
- F14 — if all players are eliminated, the game shall end as a draw.
- F15 — if only one player remains active, `check_for_winner` shall return them as the winner.
- F16 — `validate_game_state` shall detect missing/extra cards, duplicates, malformed solutions, and out-of-range turn indices.

**AI / autonomous-player requirements (per ADR-006):**

- F20 — each player slot shall be configurable as Human or AI on the Setup screen, with any mix accepted.
- F21 — an AI player shall take its full turn automatically: roll, move, suggest, optionally accuse.
- F22 — an AI player shall make decisions using only information it is allowed to know, never `state.solution` or another player's hand.
- F23 — an AI player shall accuse only when its private notes have narrowed each card type to a single remaining candidate.

**Non-functional (mandatory — "shall"):**

- NF2 — the game shall not crash for any valid sequence of user actions.

## 5) Design

No new architectural changes to the engine boundary. Several additions inside the engine and a new sibling module for the AI:

- `GameState.turn_history: list[dict]` (default empty) — records each move and suggestion as the game progresses.
- `GameState.suspect_locations: dict[str, str | None]` and `GameState.weapon_locations: dict[str, str | None]` — track where each suspect/weapon token currently sits. Populated in `new_game` (all values None initially) and updated in `make_suggestion`. This is the data structure that closes the F12 bug.
- `Player.player_type: str` (= `"human"` or `"ai"`) plus the `HUMAN_PLAYER` / `AI_PLAYER` constants in `models.py`.
- `Player.ai_notes: DetectiveNotes | None` — populated for AI slots inside `new_game._initialise_ai_notes`. Notes are seeded from the player's own hand and from the canonical card lists. The notes are private to that player.
- New module `src/game/ai.py` containing `RandomAIPlayerStrategy`, `take_ai_turn`, `run_ai_simulation`, and the helper functions for maintaining notes. The AI module is a third consumer of the engine API alongside `tests/` and `src/ui/`; it does not mutate the engine itself.

`validate_game_state` was given a strict order of checks so each test case can isolate one error at a time:

1. Solution has exactly the 3 keys (`suspect`, `weapon`, `room`).
2. Every `Player.player_type` is one of `{"human", "ai"}`.
3. Total card count is 21.
4. No duplicate `(card_type, name)` pairs.
5. `verify_deck` over the union catches any non-canonical cards.
6. `current_turn_index` is in `[0, len(players))`.

The AI's privacy invariants (F22) are checked by `tests/test_ai.py::test_ai_turn_does_not_read_solution_when_not_accusing` and `test_private_shown_card_updates_only_suggesting_ai_notes`. They are tested behaviourally rather than by patching `state.solution` so that any future strategy that quietly reads the solution would fail the same way.

The F12 fix integrates with the GUI in Sprint 4 — see `sprint_4.md`.

## 6) Test plan and evidence of testing

Unit tests added in Sprint 3: 50 (cumulative 113 across Sprints 1–3 — 33 + 30 + 50). The 50 break down roughly as: ~12 validation tests (F9–F11, F13–F16), 4 F12 token-position tests, 5 reproducibility / typed-signature tests, 16 edge-case and full-game regression tests across the engine, and 13 AI behaviour tests in `tests/test_ai.py`. All 113 passing.

System tests run this sprint (full table in `docs/testing/system_test_report.md`):

| Ref     | Req | Pass/Fail |
| ------- | --- | --------- |
| ST-04 (re-run) | F4 | Pass — fixes the BFS off-by-one carried over from Sprint 2 |
| ST-09   | F9  | Pass |
| ST-10   | F10 | Pass |
| ST-11   | F11 | Pass |
| ST-12d  | F12 (domain) | Pass — 4 unit tests + 1 system test row covering "tokens move into room" and "tokens stay after refutation" |
| ST-13   | F13 | Pass |
| ST-14   | F14 | Pass |
| ST-15   | F15 | Pass |
| ST-16   | F16 | Pass |
| ST-20   | F20 | Pass — Setup screen Human/AI toggle works, mixed games run |
| ST-21   | F21 | Pass — `take_ai_turn` drives a full turn for an AI slot |
| ST-22   | F22 | Pass — privacy invariants pinned by `tests/test_ai.py` |
| ST-23   | F23 | Pass — AI accuses only on single-candidate notes |
| ST-NF2  | NF2 | Pass |

**Bugs found and fixed in-sprint (1):** one regression — `next_turn` skipped one too many players after an eliminated-player edit. Caught on the next `pytest` run before merge, fixed within an hour.

## 7) Summary of sprint

**Did we achieve our objectives?** Yes. The engine is now substantially more robust. The GUI shows clear errors for every illegal action. The F12 token-position bug carried over from Sprint 2 is closed. The AI player module — the stretch deliverable committed in ADR-006 — landed with full test coverage.

**Is there a working prototype?** Yes — full playable build with mixed Human / AI games, EndScreen, and complete edge-case handling. **113 unit tests passing.**

**What went well?** The cumulative test suite carried into Sprint 3 gave confidence on every change. Adding `validate_game_state` led directly to discovering one stale assumption in our deal logic that hadn't been caught by the F2 tests — exactly what defensive validation is for. Identifying F12 cleanly at the midpoint meeting on 2026-04-08 (which had a slim attendance) and writing it up async on Discord let Maysarah pick it up immediately when she was back from illness. The AI module dropped in cleanly because the engine API was already frozen and exposed `roll_die` / `legal_moves_for_roll` / `move_by_dice` / `make_suggestion` with optional callbacks — the AI was a third consumer, not a special case.

**What did not go well?** The Sprint 3 midpoint meeting on 2026-04-08 had only Adam and Floyd attending in real-time — Maysarah was ill and the other two had clashing deadlines. The team relied heavily on async written updates via Discord that week. This worked but it's a fragile pattern; a longer absence by any single member would have caused real slippage. Some redundancy also crept into the codebase: both `validate_game_state` and `verify_deck` independently enumerate the canonical card set, and the AI's `record_known_card` near-duplicates the engine's `_record_known_card`. We chose to keep both for now (the AI helper is part of `ai.py`'s public surface; the engine helper is private), and documented the intentional duplication for any future refactor.

**Customer feedback?** None blocking. PO confirmed via Canvas that the AI behaviour as demonstrated (random over what the AI legally knows, accuse only on single-candidate notes) meets the specification.
