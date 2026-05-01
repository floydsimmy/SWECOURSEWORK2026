# Project Plan — Cluedo (Team 53, G6046)

## 1. Overview

Watson Games asked for a digital version of their *Clue!* board game with a Pygame GUI, 3–6 players, the full suggestion / refutation / accusation loop, the standard tile-based grid + dice movement, and an autonomous-player option. We worked through four planned sprint cycles between February and April 2026 — see ADR-006 in `docs/decisions.md` for the Sprint 2 midpoint decision to keep grid + dice and AI in scope rather than descope them.

## 2. Team and roles

| Member       | Role                                              | Primary responsibilities                                      |
| ------------ | ------------------------------------------------- | ------------------------------------------------------------- |
| Floyd        | Technical Lead & Integrator                       | Architecture, Pygame integration, integration testing, code review |
| Maysarah     | Game Logic Engineer                               | Engine, models, deck, game rules                              |
| Adam         | Scrum Master, Documentation Lead & Product Owner   | Meetings, documentation, requirements, submission             |
| Nasser       | UI/GUI Engineer                                   | Pygame screens, components, visual layout                     |
| Abdurrahman  | QA Lead                                           | Unit test suite, regression, system test execution            |

## 3. Sprint schedule

| Sprint | Window                  | Length   | Goal                                                  |
| ------ | ----------------------- | -------- | ----------------------------------------------------- |
| 1      | 2026-02-23 → 2026-03-08 | 14 days  | Foundation: models, deck, engine core, repo, Pygame skeleton |
| 2      | 2026-03-09 → 2026-03-29 | 21 days  | Core gameplay + Pygame screens + grid/dice movement (extended one week at midpoint after the keep-in-scope decision on grid + dice / AI — ADR-006) |
| 3      | 2026-03-30 → 2026-04-12 | 14 days  | Robustness, validation, F12 token-position fix, AI player module |
| 4      | 2026-04-13 → 2026-04-29 | 17 days  | Polish, video, group report, submission               |

## 4. PERT-style task breakdown

Each task: `id  duration(days)  predecessors  owner`.

| ID  | Task                                                  | Dur | Pred       | Owner       |
| --- | ----------------------------------------------------- | --- | ---------- | ----------- |
| T1  | Define engine API contract                            | 2   | —          | Floyd, Maysarah |
| T2  | Implement data models                                 | 2   | T1         | Maysarah    |
| T3  | Implement deck constants and helpers                  | 1   | T2         | Maysarah    |
| T4  | Implement engine core (`new_game`, deal, `next_turn`) | 3   | T2, T3     | Maysarah    |
| T5  | Pygame skeleton + ScreenManager                       | 2   | T1         | Floyd       |
| T6  | Title-screen mockups + colour palette                  | 1   | T5         | Nasser      |
| T7  | Unit tests F1–F3                                      | 2   | T4         | Abdurrahman |
| T8  | Implement Move / Suggest / Refute                     | 3   | T4         | Maysarah    |
| T8b | Grid + dice movement (`roll_die`, `legal_moves_for_roll`, `move_by_dice`, board layout) | 3 | T4 | Floyd |
| T9  | Implement Accusation + win/lose                       | 2   | T8         | Maysarah    |
| T10 | Setup, Game, End screens (with Human/AI toggle)       | 4   | T5, T8, T8b | Floyd, Nasser |
| T11 | UI components (Button, PopupSelect, MessageBox) + Board renderer | 3 | T5 | Nasser |
| T12 | System tests F4–F8                                    | 2   | T9, T10    | Abdurrahman |
| T13 | Validation guards (wrong turn, eliminated, game-over) | 2   | T9         | Maysarah    |
| T14 | F12 token-position fix                                 | 1   | T13        | Maysarah    |
| T14b| AI player module (`ai.py`, `RandomAIPlayerStrategy`, `take_ai_turn`, `DetectiveNotes`) and `tests/test_ai.py` | 2 | T13, T14 | Maysarah |
| T15 | UI polish (hover, end-screen, message log)             | 2   | T10, T11   | Floyd, Nasser |
| T16 | `validate_game_state`, `verify_deck`                   | 1   | T14        | Maysarah    |
| T17 | System tests F9–F16, NF2, F20–F23                      | 2   | T13, T14, T14b, T16 | Abdurrahman |
| T18 | Final regression and code freeze                       | 1   | T15, T17   | Floyd, Abdurrahman |
| T19 | Demo video recording                                   | 1   | T18        | Adam        |
| T20 | Group report + peer review                             | 2   | T18        | Adam, all   |
| T21 | Screenshots for README and system test report          | 1   | T15        | Nasser      |
| T22 | Submission ZIP assembly and integrity check            | 1   | T19, T20, T21 | Adam, Floyd |

**Critical path:** T1 → T2 → T4 → T8 → T9 → T13 → T14 → T14b → T16 → T17 → T18 → T22. (T8b runs in parallel with T8 in Sprint 2; T14b runs in parallel with T16 in Sprint 3 because they touch different parts of the engine package.)

## 5. Resources

- **Languages and runtime:** Python 3.10+ (developed on 3.13).
- **Libraries:** `pygame==2.6.1`, `pytest==9.0.3` (pinned in `requirements.txt`).
- **Tooling:** Git + GitHub for version control, Discord for async coordination, Google Meet for scheduled meetings, draw.io for diagrams.
- **Hardware:** developer laptops (Windows 11 primary).
- **Time budget:** approximately 120 person-hours total across the team over 9 weeks.

## 6. Plan vs actual

The plan was followed without scope cuts. The notable adjustments were:

1. **Grid + dice movement and the AI player were both kept in scope** at the Sprint 2 midpoint meeting (2026-03-18) — the meeting that had been called as a candidate point to descope them. ADR-006 in `docs/decisions.md` records the rationale: marking-criteria leverage, identity of the Cluedo movement rule, and a judgement that the engineering risk was acceptable on the back of a frozen Sprint 1 engine API. Sprint 2 was extended by one week at the same meeting to absorb the integration work (planned 14 days, actual 21 days).
2. **The AI module was deferred from Sprint 2 to Sprint 3** to keep the Sprint 2 ambition focused on grid + dice and the human-player gameplay loop. The AI landed in Sprint 3 as a clean third consumer of the frozen engine API; the engine itself did not need to change to support it.
3. **F12 token-position bug was identified at the Sprint 3 midpoint** (2026-04-08) and added to Sprint 3 scope; closed within the sprint with new unit tests covering "tokens move into room" and "tokens stay after refutation".
4. **Sprint 4 was strict freeze** with one critical bugfix permitted (TC-25, the F12 visibility log line in the GUI's suggestion handler).

The shipped test count reflects the kept-in-scope decision: the final shipped count is 116, covering engine, AI, and models.
