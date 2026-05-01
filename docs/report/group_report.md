# Group Report — Cluedo (Software Engineering G6046, Team 53)

## 1. Project overview

**What was built.** A Python + Pygame implementation of Watson Games' *Clue!* for 3–6 hot-seat players, mixed Human and AI. The build supports a title screen, a setup screen with per-slot Human/AI toggles and player-name validation, a game screen with the full board (24 × 24 grid with corridors, rooms, doors), private hand display, and the full turn-based action loop (Roll Dice → click destination, Suggest, Accuse, End Turn), and an end screen that reveals the hidden solution. The engine implements requirements F1–F16 plus the AI requirements F20–F23 and the desirable F17–F19, F24 from the requirements document, against NF1–NF4.

**The two ambitious deliverables.** The user requirements describe the classic tile-based board with grid coordinates, doors, and dice-distance pathing, and they describe an autonomous-player option. Both were on the table for descope at the Sprint 2 midpoint meeting on 2026-03-18 — they were explicitly the two largest pieces of "above-the-line" work. The team chose to keep both in scope and absorb the cost (recorded in ADR-006 in `docs/decisions.md`), with the Sprint 2 window extended by one week to allow the integration. The judgement was that a dropdown room selector instead of grid + dice would have walked away from the part of Cluedo that gives the game its identity, and that adding a basic AI — random selection over un-eliminated cards plus a simple notes-tracking accusation gate — would, alongside the full board, sit comfortably in the 31–40 code band of the marking criteria. The cost was real but the team was confident — particularly on the back of the Sprint 1 engine API freeze, which made the AI a clean third consumer alongside the GUI and the tests.

**Out of scope for the MVP** (see `docs/report/requirements.md` and `docs/decisions.md`): save / load games, networked multiplayer, animations / sound effects, mobile or web build, detective-notes sheet rendered for human players, secret passages between corner rooms.

**Run the build.**

```
pip install -r requirements.txt
python -m src.main
```

**Final state at submission.**

- 116 of 116 unit tests passing (`python -m pytest -q`, well under one second).
- Engine and AI packages have zero Pygame imports — both are fully testable headless.
- All requirements F1–F16, F20–F23 and NF1–NF4 covered in `docs/testing/system_test_report.md` with linked unit-test evidence.

## 2. Team organisation

| Person       | Project role                                       |
| ------------ | -------------------------------------------------- |
| Floyd        | Technical Lead & Integrator                        |
| Maysarah     | Game Logic Engineer                                |
| Adam         | Scrum Master, Documentation Lead & Product Owner   |
| Nasser       | UI/GUI Engineer                                    |
| Abdurrahman  | QA Lead                                            |

**How we worked.** Two-week sprints (Sprint 2 extended to three weeks at its midpoint) totalling four sprints across the period 23 February to 29 April 2026. Scheduled meetings on Google Meet, plus a final hybrid review with Adam and Floyd in person at Floyd's house and the rest of the team on Google Meet. Async coordination through a Discord server with channels for announcements, dev work, QA, decisions, and standups. Adam coordinated meetings and documentation; Floyd led integration and the grid-pathing work; Maysarah owned the engine, rules, and the AI module; Nasser owned the GUI screens, components, and the board renderer; Abdurrahman owned the unit and system test suites.

**Attendance at scheduled meetings (across 9 scheduled meetings).**

| Person       | Attended | Notes                                                                  |
| ------------ | -------- | ---------------------------------------------------------------------- |
| Adam         | 9 of 9   | Coordinated every meeting.                                              |
| Floyd        | 9 of 9   | Technical lead reference for every sprint review.                       |
| Maysarah     | 8 of 9   | Missed one due to illness; sent a written update via Discord.           |
| Nasser       | 5 of 9   | Coursework clashes from other modules; contributed primarily async.     |
| Abdurrahman  | 4 of 9   | Coursework clashes from other modules; contributed primarily async.     |

The team relied on Discord for async updates from absent members. This was workable but not ideal — see §5.

## 3. Sprint-by-sprint progress

### Sprint 1 — Foundation (23 Feb – 8 Mar 2026)

Engine core (`models.py`, `deck.py`, the start of `engine.py`), Pygame window skeleton with title screen, repository scaffold, Discord set up. Engine API frozen on 2026-03-04 so screens could be built against a stable contract. Reference: `docs/sprints/sprint_1.md`.

### Sprint 2 — Core gameplay (9 Mar – 29 Mar 2026, extended)

The big sprint. Three streams running in parallel:

- **Engine — rules and movement.** Maysarah implemented `move_to_room`, `make_suggestion` (refutation walk in turn order), `make_accusation` with auto-advance, `check_for_winner`. Floyd added the grid-pathing functions (`roll_die`, `legal_moves_for_roll` with BFS over corridor tiles, `move_by_dice`) and the static board layout tables (`ROOM_LAYOUT`, `ROOM_DOORS`, `CHARACTER_START_TILES`).
- **GUI — screens and board renderer.** Floyd built `SetupScreen`, `GameScreen`, and the `ScreenManager` wiring; Nasser built the component library (`Button`, `TextInput`, `PopupSelect`, `MessageBox`) and the `Board` renderer in `src/ui/gui.py` that draws the 24 × 24 grid, room shapes, doors, and player tokens.
- **Scope decision at the midpoint.** The 2026-03-18 midpoint meeting debated dropping grid + dice and dropping AI. After the PO re-read the marking criteria the team committed to keep both in scope; ADR-006 was logged the same day. Sprint 2 extended by one week (planned 14 days, actual 21 days) to absorb the integration work.

Sprint 2 closed with the full human gameplay loop running end-to-end through the GUI. Reference: `docs/sprints/sprint_2.md`.

### Sprint 3 — Robustness & AI stretch (30 Mar – 12 Apr 2026)

Hardening sprint plus the AI deliverable:

- **Validation everywhere.** Input validation across every action, wrong-turn guards, eliminated-cannot-act enforcement, action-after-game-over guards, draw and last-player-standing logic, `validate_game_state`, `verify_deck`, `turn_history`, `reset_game`.
- **F12 token-position bug** (the suspect and weapon should move into the suggester's room and stay there) was identified by Adam at the midpoint meeting and closed within the sprint, with new unit tests covering "tokens move" and "tokens stay after refutation".
- **AI player stretch goal landed.** The team had the bandwidth to bring back the autonomous-player work that ADR-006 had committed to. Maysarah built `src/game/ai.py` — `RandomAIPlayerStrategy`, `take_ai_turn`, `run_ai_simulation`, `DetectiveNotes`, the private-notes invariants — and the new `tests/test_ai.py` file. The AI is a third consumer of the engine API; the engine itself did not need to change to support it.

The final shipped count is 116 unit tests, covering engine, AI, and models. Reference: `docs/sprints/sprint_3.md`.

### Sprint 4 — Polish, demo, and submission (13 Apr – 29 Apr 2026)

Code-freeze sprint with one critical bugfix permitted: a 3-line change in `src/ui/screens.py` (TC-25) to surface the F12 token movement in the in-game suggestion log so the fix is visible to a player and a marker. Otherwise: top-level `README.md` polish, system test report final fill-in, group report draft, demo video recording, peer review agreement, submission ZIP assembly. Two engine-side additions also landed during submission prep — a dice-fairness distribution test (covering the fair-dice rule from the brief) and an engine-level guard preventing a player from rolling twice in a single turn. Final regression run: 116 of 116. Reference: `docs/sprints/sprint_4.md`.

## 4. What went well

- **Engine, GUI, and AI separation held cleanly across all four sprints.** The engine has zero Pygame imports. The 116-test suite runs in well under a second because no test touches the display layer. The AI module is engine-only too — same testability win. Late changes in Sprint 3 — validation, F12, the AI stretch — shipped with confidence because every change was gated by `pytest -q` before merge.
- **Engine API frozen early; AI and GUI both consumed it.** The Sprint 1 decision to freeze the engine API meant Sprint 2 could run three streams in parallel (rules, screens, board renderer) and Sprint 3 could add the AI as a third consumer without touching the engine itself. This is the single thing the team got most right architecturally.
- **The big scope decision was resolved cleanly.** The Sprint 2 midpoint debate over grid + dice and AI was a real fork in the project. ADR-006 records the rationale (marking criteria, identity of Cluedo, time risk acceptable). The team held the line in Sprint 3 and delivered the AI rather than letting it slip into "future work".
- **Documentation kept pace with the code.** Sprint docs were filed at the end of each sprint, not retrofitted at submission time. ADRs were written when decisions were taken. The submission pack assembled progressively rather than in a panic during the final week.
- **Async-friendly process worked even with uneven attendance.** Discord channels for `#standup`, `#dev`, `#qa-testing`, and `#decisions` meant absent members could catch up and contribute without blocking the team. The Sprint 3 midpoint (Adam and Floyd attending in real-time, the other three async) is an example of the pattern functioning under pressure.

## 5. What did not go well

- **Sprint 2 ran a week long.** The team caught the slip at the midpoint and the PO signed off on the extension, but a tighter scope or earlier integration could have avoided it. Two streams of engine work plus a board renderer was ambitious for 14 days; in retrospect the extension was foreseeable a week earlier than we acted on it.
- **The grid-pathing first cut had a corner-case bug.** `legal_moves_for_roll` initially counted the door tile twice when the player started in a room, so a roll of `n` showed reachable rooms at distance `n+1`. Caught by Abdurrahman's first system test pass on F4 in Sprint 3 and fixed there; would have been better to have a unit test on the BFS itself in Sprint 2.
- **Attendance was uneven.** Three members attended fewer than two-thirds of scheduled meetings due to coursework clashes from other modules. The team mitigated with Discord updates, but several meetings (notably Sprint 3 midpoint and Sprint 4 midpoint) had only two or three real-time attendees. Decisions were still made and documented, but the pattern is fragile — a longer absence by any single member would have caused real slippage.
- **No automated GUI tests.** Every automated test covers the engine or the AI. The GUI is only validated by manual play and the demo video. A small Pygame-based smoke test would have caught the Sprint 2 EndScreen draw-path bug at least a week earlier than manual testing did.
- **Demo video took two attempts.** A system notification interrupted the first take. Trivial to avoid (Do Not Disturb mode); we just didn't think of it ahead of time.

## 6. What we would do differently

- **Smaller PRs split by layer.** Some Sprint 2 PRs bundled an engine change with the screen change that consumed it. Reviewable, but harder than they needed to be. Next time: one PR per layer.
- **Pin Python and dependency versions from Sprint 1.** `requirements.txt` was added in Sprint 3. The Python 3.10 vs 3.13 spread across team laptops caused the setup friction that ate the Sprint 1 midpoint meeting. A `requirements.txt` plus a `pyproject.toml` with `requires-python` from day one would have prevented it.
- **Schedule meetings around the rest of the cohort's coursework load, not just our team's.** Three of the missed meetings were predictable from a quick look at other modules' deadlines. A shared calendar across all five members' coursework loads would have flagged conflicts a week ahead.
- **Add at least one Pygame-based GUI smoke test.** Even one headless test that opens the title screen and pages through the screens would have caught the EndScreen rendering bug earlier.
- **Unit-test the BFS pathfinder directly.** We tested grid + dice movement only via the AI's full-turn loop and via system tests. Direct unit tests on `legal_moves_for_roll` would have caught the off-by-one corner case in Sprint 2 instead of Sprint 3.

## 7. Outstanding issues at submission

| Item                                                                 | Status / what we would do next                                                                                                                                                                                                                                               |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Secret passages between corner rooms                                 | Documented in the user requirements; not implemented. The `ROOM_LAYOUT` and `ROOM_DOORS` tables would need a `passage` relation; `legal_moves_for_roll` would treat passages as zero-cost moves between linked rooms. Estimate: half a day plus tests.                       |
| F3 Miss Scarlet primacy rule                                          | The engine cycles turn order clockwise correctly (verified by ST-03a–c), but does not seat Miss Scarlet first when present. The implementation accepts free-text player names rather than binding players to suspect characters. Future work would add a character-pick step on the Setup screen and a primacy check in `new_game`. Documented as a known limitation. |
| Smarter AI strategy                                                   | The shipped strategy is intentionally simple: random over what the AI knows is possible, and accuse only when notes narrow each card type to one. Future work could add probabilistic narrowing from refutation outcomes, or a "block" heuristic that suggests cards the AI knows are not in the envelope to learn what an opponent holds. |
| Save/load games, networked multiplayer, animations, sound effects     | All deliberately out of scope per the team's decision log.                                                                                                                                                                                                                  |
| No automated GUI tests                                                 | Engine and AI fully tested; GUI is validated manually and by the demo video. Future work would add a small `pygame`-based smoke test that exercises each screen transition.                                                                                                  |

None of these items block a customer pilot of the prototype. The build is stable, the rules are correct, and the engine API is clean enough that any of the deferred work would be additive rather than a rewrite.

## 8. Closing

This was a working agile delivery with four sprint cycles, a working prototype at the end of every sprint, and a final build that holds 116 unit tests green across engine, AI, and models. Scope was protected by the Product Owner — and on the two big "above-the-line" deliverables we decided to keep both in scope and to put in the time it would take. Requirements became unit and system tests; tests caught regressions; and the submission pack documents the journey from kickoff to handover.

The team is comfortable with the equal 20/20/20/20/20 peer review split — within their roles, every member delivered what was asked of them. Attendance was uneven but contribution was not: Discord-based async work covered the gap. The marker is invited to inspect the meeting minutes (`docs/meetings/`) and the per-sprint contribution tables (`docs/sprints/sprint_*.md`) for evidence behind the peer review.

Submitted by Adam (Scrum Master, Documentation Lead & Product Owner) on behalf of Team 53.
