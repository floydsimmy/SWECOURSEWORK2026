# Group Report — Cluedo (Software Engineering G6046, Team 53)

## 1. Project overview

**What was built.** A Python + Pygame implementation of Watson Games' *Clue!* for 3–6 hot-seat human players. The build supports a title screen, a setup screen with player-name entry and validation, a game screen with a private hand display and the full turn-based action loop (move, suggest, accuse, end turn), and an end screen that reveals the hidden solution. The engine implements requirements F1–F16 and NF1–NF2 from the user requirements document.

**What was not built (and why).** The original user requirements describe a tile-based Cluedo board with grid coordinates, doors, secret passages, and dice-distance pathing. They also describe an AI / autonomous-player option. The team made deliberate scope decisions in Sprint 2 (recorded in `docs/decisions.md`) to:

- Replace tile-based movement with dropdown room selection (F4 in our refined requirements set);
- Drop the AI player entirely.

These choices were made by the Product Owner (Adam) after re-reading the marking criteria — both items were assessed as low-leverage relative to the time available, with the marking criteria placing AI in the upper 41–50 code band only. Effort was instead redirected into validation (Sprint 3) and submission quality (Sprint 4). No save/load, networked multiplayer, animations, or sound — all out of scope per the team's decision log.

**Run the build.**
pip install -r requirements.txt
python -m src.main

**Final state at submission.**

- 100 of 100 unit tests passing (`python -m pytest -q`, 0.06s).
- Engine has zero Pygame imports — fully testable without a display.
- All requirements F1–F8 and NF1–NF2 covered in `docs/testing/system_test_report.md` with linked unit-test evidence.

## 2. Team organisation

| Person       | Project role                                       |
| ------------ | -------------------------------------------------- |
| Floyd        | Technical Lead & Integrator                        |
| Maysarah     | Game Logic Engineer                                |
| Adam         | Scrum Master, Documentation Lead & Product Owner   |
| Nasser       | UI/GUI Engineer                                    |
| Abdurrahman  | QA Lead                                            |

**How we worked.** Two-week sprints (Sprint 2 extended to three weeks at its midpoint) totalling four sprints across the period 23 February to 29 April 2026. Scheduled meetings on Google Meet, plus a final hybrid review with Adam and Floyd in person at Floyd's house and the rest of the team on Google Meet. Async coordination through a Discord server with channels for announcements, dev work, QA, decisions, and standups. Adam coordinated meetings and documentation; Floyd led integration; Maysarah owned the engine and rules; Nasser owned the GUI screens and components; Abdurrahman owned the unit and system test suites.

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

Engine core (`models.py`, `deck.py`, the start of `engine.py`), Pygame window skeleton with title screen, repository scaffold, Discord set up. Sprint 1 closed with 33 unit tests passing. Reference: `docs/sprints/sprint_1.md`.

### Sprint 2 — Core gameplay (9 Mar – 29 Mar 2026, extended)

Full gameplay loop: Move, Suggest, Refute, Accuse implemented in the engine and wired through Setup, Game, and End screens. Two scope decisions taken at the midpoint meeting on 18 March: grid-based movement descoped to dropdown room selection, and the AI player descoped entirely. Sprint extended by one week (planned 14 days, actual 21 days) to absorb integration work. Sprint 2 closed with ~63 unit tests passing. Reference: `docs/sprints/sprint_2.md`.

### Sprint 3 — Robustness & validation (30 Mar – 12 Apr 2026)

Hardening sprint: input validation across every action, wrong-turn guards, eliminated-cannot-act enforcement, action-after-game-over guards, draw and last-player-standing logic, `validate_game_state`, `verify_deck`, `turn_history`, `reset_game`. **F12 token-position bug** (the suspect and weapon should move into the suggester's room and stay there) was identified at the midpoint meeting and closed within the sprint, with new unit tests covering "tokens move" and "tokens stay after refutation". Sprint 3 closed with 100 unit tests passing. Reference: `docs/sprints/sprint_3.md`.

### Sprint 4 — Polish, demo, and submission (13 Apr – 29 Apr 2026)

Code-freeze sprint with one critical bugfix permitted: a 3-line change in `src/ui/screens.py` to surface the F12 token movement in the in-game suggestion log so the fix is visible to a player and a marker. Otherwise: top-level `README.md` polish, system test report final fill-in, group report draft, demo video recording, peer review agreement, submission ZIP assembly. Final regression run on 27 April: 100 of 100. Reference: `docs/sprints/sprint_4.md`.

## 4. What went well

- **Engine and GUI separation held cleanly across all four sprints.** The engine has zero Pygame imports. The 100-test suite runs in 0.06 seconds because no test touches the display layer. Late changes in Sprint 3 — validation, F12 — shipped with confidence because every change was gated by `pytest -q` before merge. This is the single thing the team got most right architecturally.
- **Scope decisions were taken early and stuck.** The Sprint 2 midpoint descopes (grid movement, AI) were made cleanly, signed off by the PO with reference to the marking criteria, and recorded in `docs/decisions.md`. The team did not re-litigate them. This kept Sprint 4 a real polish sprint rather than a feature-completion scramble.
- **Documentation kept pace with the code.** Sprint docs were filed at the end of each sprint, not retrofitted at submission time. ADRs were written when decisions were taken, not afterwards. The submission pack assembled progressively rather than in a panic during the final week.
- **Async-friendly process worked even with uneven attendance.** Discord channels for `#standup`, `#dev`, `#qa-testing`, and `#decisions` meant absent members could catch up and contribute without blocking the team. The Sprint 3 midpoint meeting (Adam and Floyd attending in real-time, the other three async) is an example of the pattern functioning under pressure.

## 5. What did not go well

- **One scope mistake mid-Sprint-2.** Tile-based movement was briefly attempted before being descoped at the midpoint meeting. Around six person-hours of exploratory work did not ship. Lesson: agree the sprint goal at the start of the sprint, resist the temptation to expand mid-sprint even if the work looks tractable.
- **Sprint 2 ran a week long.** The team caught the slip at the midpoint and the PO signed off on the extension, but a tighter scope or earlier integration could have avoided it. This is a real Sprint 2 anti-pattern across most agile teams; we hit it on cue.
- **Attendance was uneven.** Three members attended fewer than two-thirds of scheduled meetings due to coursework clashes from other modules. The team mitigated with Discord updates, but several meetings (notably Sprint 3 midpoint and Sprint 4 midpoint) had only two or three real-time attendees. Decisions were still made and documented, but the pattern is fragile — a longer absence by any single member would have caused real slippage.
- **No automated GUI tests.** Every automated test covers the engine. The GUI is only validated by manual play and the demo video. A small Pygame-based smoke test would have caught the Sprint 2 EndScreen draw-path bug at least a week earlier than manual testing did.
- **Demo video took two attempts.** A system notification interrupted the first take. Trivial to avoid (Do Not Disturb mode); we just didn't think of it ahead of time.

## 6. What we would do differently

- **Smaller PRs split by layer.** Some Sprint 2 PRs bundled an engine change with the screen change that consumed it. Reviewable, but harder than they needed to be. Next time: one PR per layer.
- **Pin Python and dependency versions from Sprint 1.** `requirements.txt` was added in Sprint 3. The Python 3.10 vs 3.13 spread across team laptops caused the setup friction that ate the Sprint 1 midpoint meeting. A `requirements.txt` plus a `pyproject.toml` with `requires-python` from day one would have prevented it.
- **Schedule meetings around the rest of the cohort's coursework load, not just our team's.** Three of the missed meetings were predictable from a quick look at other modules' deadlines. A shared calendar across all five members' coursework loads would have flagged conflicts a week ahead.
- **Add at least one Pygame-based GUI smoke test.** Even one headless test that opens the title screen and pages through the screens would have caught the EndScreen rendering bug earlier.
- **Document the engine API as it stabilises, not at the end.** Most public functions have docstrings now (added in Sprint 4), but doing the doc-string sweep continuously across Sprint 2 and Sprint 3 would have been cheaper than the end-of-project pass.

## 7. Outstanding issues at submission

| Item                                                                 | Status / what we would do next                                                                                                                                                                                                                                               |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tile-based board movement (with grid, doors, secret passages, dice)  | Deliberate scope choice — descoped at the Sprint 2 midpoint with PO sign-off. Future work would add a `board.py` module, adjacency rules, and a dice-distance pathing component. Estimated ~600+ lines of new code plus ~150 tests, which is roughly a Sprint 2-sized piece of work. |
| AI / autonomous player                                                | Deliberate scope choice — descoped at the Sprint 2 midpoint. The marking criteria places AI in the 41–50 code band only; the team prioritised validation depth instead.                                                                                                       |
| F3 Miss Scarlett primacy rule                                         | The engine cycles turn order clockwise correctly (verified by ST-03a–c), but does not seat Miss Scarlett first when present. The implementation accepts free-text player names rather than binding players to suspect characters. Future work would add a character-pick step on the Setup screen and a primacy check in `new_game`. Documented as a known limitation. |
| Save/load games, networked multiplayer, animations, sound effects     | All deliberately out of scope per the team's decision log.                                                                                                                                                                                                                  |
| No automated GUI tests                                                 | Engine is fully tested; GUI is validated manually and by the demo video. Future work would add a small `pygame`-based smoke test that exercises each screen transition.                                                                                                       |

None of these items block a customer pilot of the prototype. The build is stable, the rules are correct, and the engine API is clean enough that any of the deferred work would be additive rather than a rewrite.

## 8. Closing

This was a working agile delivery with four sprint cycles, a working prototype at the end of every sprint, and a final build that holds 100 unit tests green. Scope was protected by the Product Owner; requirements became unit and system tests; tests caught regressions; and the submission pack documents the journey from kickoff to handover.

The team is comfortable with the equal 20/20/20/20/20 peer review split — within their roles, every member delivered what was asked of them. Attendance was uneven but contribution was not: Discord-based async work covered the gap. The marker is invited to inspect the meeting minutes (`docs/meetings/`) and the per-sprint contribution tables (`docs/sprints/sprint_*.md`) for evidence behind the peer review.

Submitted by Adam (Scrum Master, Documentation Lead & Product Owner) on behalf of Team 53.
