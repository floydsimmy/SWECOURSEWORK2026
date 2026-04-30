# Peer Review — Team 53

Per the coursework specification, each five-member team has 20 points per member, totalling 100 across the team. Marks reflect each member's contribution to the project as a whole. Marks are non-negative integers and sum to exactly 100. A score of 0 means a member made no contribution at all (a "ghost") and triggers an overall coursework grade of 0 for that member; the team unanimously confirms this is **not** the case for any member here.

## Agreed marks

| Member       | Project role                                       | Peer mark |
| ------------ | -------------------------------------------------- | --------- |
| Floyd        | Technical Lead & Integrator                        | 20        |
| Maysarah     | Game Logic Engineer                                | 20        |
| Adam         | Scrum Master, Documentation Lead & Product Owner   | 20        |
| Nasser       | UI/GUI Engineer                                    | 20        |
| Abdurrahman  | QA Lead                                            | 20        |
| **Total**    |                                                    | **100**   |

The team agreed an equal split. Although attendance at scheduled meetings was uneven (Adam and Floyd attended every meeting; Maysarah missed one due to illness; Nasser and Abdurrahman missed several due to coursework clashes from other modules), every member delivered the work assigned to their role across the four sprints. The team's view is that contribution should be measured by output, not by meeting attendance, and on that basis the contributions are equivalent within the scope of each role.

## Justification — evidence per member

The marks above are supported by the per-sprint contribution tables in `docs/sprints/sprint_*.md` and by the meeting minutes in `docs/meetings/`. A summary follows.

### Floyd — Technical Lead & Integrator

- Pygame skeleton, `ScreenManager`, all four screens (`MainMenu`, `Setup`, `Game`, `End`); engine-API contract co-author with Maysarah (Sprint 1).
- `SetupScreen` (with the per-slot Human/AI toggle) and `GameScreen` integration; **grid pathfinder** in `engine.py` (`roll_die`, `legal_moves_for_roll` BFS, `move_by_dice`) and the static board-layout tables; `ScreenManager` wiring; `EndScreen` v1 (Sprint 2).
- `EndScreen` polish, hover states, `MessageBox`, message-history panel; off-by-one fix on the BFS distance check; Sprint 4 planning started in parallel (Sprint 3).
- TC-25 bugfix surfacing F12 token movement in the suggestion log; final UI polish; code-freeze enforcement; submission ZIP build (Sprint 4).
- Attended 9 of 9 scheduled meetings.

### Maysarah — Game Logic Engineer

- `models.py`, `deck.py`, and the foundation of `engine.py` — `new_game`, `next_turn`, `get_current_player` (Sprint 1).
- `move_to_room`, `make_suggestion`, `make_accusation`, refutation walk, auto-advance on accusation, `check_for_winner` (Sprint 2).
- Full validation suite, **F12 fix** (suspect/weapon location tracking), `validate_game_state`, `verify_deck`, `get_turn_summary`, `turn_history`, `reset_game`; **AI player module** (`src/game/ai.py`) — `RandomAIPlayerStrategy`, `take_ai_turn`, `run_ai_simulation`, `DetectiveNotes`, the private-notes invariants, `tests/test_ai.py` covering 13 AI behaviour tests (Sprint 3).
- Final test suite verification; `__str__` polish on `Card` and `Player`; final code-documentation sweep (Sprint 4).
- Attended 8 of 9 scheduled meetings (one absence: illness, written update via Discord).

### Adam — Scrum Master, Documentation Lead & Product Owner

- Repository scaffold, Discord server setup with channels, user stories F1–F8 (Sprint 1).
- Sprint planning, scope decisions including the keep-in-scope decision for grid + dice and the AI player (ADR-006 sign-off), `docs/decisions.md` entries, group-report skeleton; Sprint 2 extension sign-off (Sprint 2).
- Acceptance criteria for F9–F16, **F12 bug identified and added to Sprint 3 scope**, AI requirements F20–F23 written up after the AI module landed, group-report skeleton expansion, system test report review (Sprint 3).
- Final group report, `peer_review.md`, demo video script and recording, top-level `README.md` polish, submission ZIP assembly and Canvas upload (Sprint 4).
- Coordinated and minuted all 9 scheduled meetings.
- Attended 9 of 9 scheduled meetings.

### Nasser — UI/GUI Engineer

- Initial title-screen mockups; colour-palette exploration (Sprint 1).
- UI component library — `Button`, `TextInput`, `PopupSelect`, `MessageBox`; `GameScreen` layout (sidebar, log panel, action button cluster); `Board` renderer in `src/ui/gui.py` (24 × 24 grid, room shapes, doors, player tokens, dice-move highlight overlay) (Sprint 2).
- `GameScreen` visual polish; hover states across `Button` instances; `MessageBox` rendering cleanup; AI vs Human visual differentiation in the player legend (Sprint 3).
- Title-screen, gameplay, and end-screen screenshots for `README.md` and the system test report; ad-hoc UI polish from screenshot review (Sprint 4).
- Attended 5 of 9 scheduled meetings; contributed async via Discord on missed dates.

### Abdurrahman — QA Lead

- System test report template using F1–F8 IDs; unit tests for F1–F3 (Sprint 1).
- System tests F4–F8 in `docs/testing/system_test_report.md`; GitHub Issues bug log; in-sprint regression runs; first system-test pass on F4 grid + dice movement (which surfaced the BFS off-by-one corner case Floyd then fixed in Sprint 3) (Sprint 2).
- New system test cases for F9–F16, NF2, F20–F23; full regression run; bug log audit (zero open critical bugs at sprint close); test-coverage report submitted via Discord ahead of the Sprint 3 review (Sprint 3).
- Final regression run on 27 April (116 of 116); system test report finalised; bug log closed; final regression on the unpacked submission ZIP — also 116 of 116, confirming clean export (Sprint 4).
- Attended 4 of 9 scheduled meetings; contributed async via Discord on missed dates.

## Sign-off

This allocation was discussed and agreed at the final review meeting on 2026-04-28 (see `docs/meetings/2026-04-28_final_review.md`). All five members approved the equal split as a fair reflection of contribution within their roles. No dispute was raised; no escalation to the module convenor was required.
