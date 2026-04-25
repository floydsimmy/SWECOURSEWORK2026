# Project Plan — Cluedo (G6046)

## 1. Overview

Watson Games asked for a digital version of their *Clue!* board game with
a Pygame GUI, 3-6 players, the full suggestion / refutation / accusation
loop, and an autonomous-player option as a stretch goal. We delivered the
human-player MVP across four two-week sprints.

## 2. Team & roles

| Member   | Role                                 | Primary responsibilities                              |
| -------- | ------------------------------------ | ----------------------------------------------------- |
| Floyd    | Technical Lead & Integrator (dev)    | Architecture, Pygame integration, repo, code review   |
| Maysarah | Game Logic Engineer (dev)            | Engine, models, deck, unit tests                      |
| Member C | Product Owner                        | User stories, requirements, acceptance criteria       |
| Member D | QA Lead                              | System test plan, regression, bug log                 |
| Member E | Scrum Master & Documentation Owner   | Meetings, sprint docs, group report, submission pack  |

## 3. Sprints (Gantt summary)

| Sprint | Window                  | Goal                                                  |
| ------ | ----------------------- | ----------------------------------------------------- |
| 1      | 2026-02-02 → 2026-02-15 | Foundation: models, deck, engine core, repo, CI rules |
| 2      | 2026-02-16 → 2026-03-01 | Core gameplay + Pygame screens wired to engine        |
| 3      | 2026-03-02 → 2026-03-15 | Robustness, validation, end-screen, edge cases        |
| 4      | 2026-03-16 → 2026-03-29 | Polish, full system test, video, group report         |

## 4. PERT-style task breakdown

Each task: `id  duration(days)  predecessors  owner`.

| ID  | Task                                | Dur | Pred       | Owner    |
| --- | ----------------------------------- | --- | ---------- | -------- |
| T1  | Define engine API contract          | 2   | -          | Floyd, M |
| T2  | Implement data models               | 2   | T1         | Maysarah |
| T3  | Implement deck (SUSPECTS/WEAPONS/ROOMS, create_deck, verify_deck) | 1 | T2 | Maysarah |
| T4  | Implement engine core (new_game, deal, next_turn) | 3 | T2, T3 | Maysarah |
| T5  | Pygame window skeleton + ScreenManager | 2 | T1      | Floyd    |
| T6  | Unit tests F1-F3                    | 2   | T4         | Maysarah, QA |
| T7  | Implement move / suggest / refute   | 3   | T4         | Maysarah |
| T8  | Implement accusation + win / lose   | 2   | T7         | Maysarah |
| T9  | MainMenu / Setup / Game / End screens | 4 | T5, T7   | Floyd    |
| T10 | Wire dropdowns + buttons to engine  | 2   | T9         | Floyd    |
| T11 | System tests F1-F8 (Sprint 2)       | 2   | T7, T8, T10 | QA      |
| T12 | Validation: invalid names, wrong turn, game-over guards | 2 | T8 | Maysarah |
| T13 | Last-player-standing + draw logic   | 1   | T12        | Maysarah |
| T14 | get_turn_summary, turn_history, reset_game | 1 | T12  | Maysarah |
| T15 | UI polish + MessageBox + colour scheme | 2 | T10      | Floyd    |
| T16 | validate_game_state + verify_deck integrity | 1 | T13 | Maysarah |
| T17 | Final regression + bug fix pass     | 2   | all        | QA, devs |
| T18 | Video demo recording                | 1   | T17        | Scrum    |
| T19 | Group report + peer review          | 2   | T17        | PO, Scrum|
| T20 | Submission pack assembly            | 1   | T18, T19   | Scrum    |

**Critical path:** T1 → T2 → T4 → T7 → T8 → T12 → T13 → T16 → T17 → T20
(estimated 19 days of effort, comfortably within the four-sprint window).

## 5. Risk register

| ID  | Risk                                          | Likelihood | Impact | Mitigation                                                          |
| --- | --------------------------------------------- | ---------- | ------ | ------------------------------------------------------------------- |
| R1  | Only two coders bottleneck delivery           | High       | High   | QA writes system tests, PO + Scrum own all docs; devs focus on code |
| R2  | Engine / GUI integration breaks late          | Medium     | High   | Define engine API in Sprint 1, integrate every sprint, smoke-test on each PR |
| R3  | Pygame quirks on Windows (font, SDL paths)    | Medium     | Medium | Use `pygame.font.Font(None, …)` (default font), test on Windows from Sprint 2 |
| R4  | Scope creep (board movement, AI, save games)  | High       | Medium | PO controls backlog; stretch goals are explicitly out of MVP        |
| R5  | Last-minute documentation gap                 | Medium     | High   | DoD includes doc update; Scrum checks every sprint                  |
| R6  | A team member becomes inactive                | Medium     | High   | Meeting notes track attendance; tasks are reassignable each sprint  |
| R7  | Tests rot as engine evolves                   | Low        | Medium | `pytest -x -q` is the gate before any merge to main                 |

## 6. Resources

- **Languages / runtime:** Python 3.11+ (CI used 3.13)
- **Libraries:** `pygame`, `pytest`
- **Tooling:** Git + GitHub, Discord for async standups, draw.io for diagrams
- **Hardware:** any laptop (Mac or Windows); the prototype was developed on Windows 11
- **Time budget:** ~120 person-hours total (8 weeks × 5 people × ~3 h/week)

## 7. Plan-vs-actual notes

The plan above was followed without major deviation. The two notable
adjustments:

1. **Board with grid coordinates was descoped** at the end of Sprint 2;
   "move to room" became a dropdown selection instead of a tile-based
   walk. The PO confirmed this was acceptable for the MVP and the
   marker-facing scope.
2. **AI player was descoped entirely** since the marking criteria states
   the AI carries a small weight and only matters at the very top of the
   code band. Effort was redirected into validation and the system test
   report.

Both decisions are logged in `docs/sprints/` summaries.
