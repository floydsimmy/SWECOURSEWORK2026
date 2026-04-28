# Project Plan — Cluedo (Team 53, G6046)

## 1. Overview

Watson Games asked for a digital version of their *Clue!* board game with a Pygame GUI, 3–6 players, the full suggestion / refutation / accusation loop, and an autonomous-player option as a stretch goal. We delivered the human-player MVP across four sprints between 23 February and 29 April 2026.

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
| 2      | 2026-03-09 → 2026-03-29 | 21 days  | Core gameplay + Pygame screens wired to engine (extended one week at midpoint) |
| 3      | 2026-03-30 → 2026-04-12 | 14 days  | Robustness, validation, F12 token-position fix        |
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
| T9  | Implement Accusation + win/lose                       | 2   | T8         | Maysarah    |
| T10 | Setup, Game, End screens                              | 4   | T5, T8     | Floyd, Nasser |
| T11 | UI components (Button, Dropdown, MessageBox)          | 3   | T5         | Nasser      |
| T12 | System tests F4–F8                                    | 2   | T9, T10    | Abdurrahman |
| T13 | Validation guards (wrong turn, eliminated, game-over) | 2   | T9         | Maysarah    |
| T14 | F12 token-position fix                                 | 1   | T13        | Maysarah    |
| T15 | UI polish (hover, end-screen, message log)             | 2   | T10, T11   | Floyd, Nasser |
| T16 | `validate_game_state`, `verify_deck`                   | 1   | T14        | Maysarah    |
| T17 | System tests F9–F16, NF2                               | 2   | T13, T14, T16 | Abdurrahman |
| T18 | Final regression and code freeze                       | 1   | T15, T17   | Floyd, Abdurrahman |
| T19 | Demo video recording                                   | 1   | T18        | Adam        |
| T20 | Group report + peer review                             | 2   | T18        | Adam, all   |
| T21 | Screenshots for README and system test report          | 1   | T15        | Nasser      |
| T22 | Submission ZIP assembly and integrity check            | 1   | T19, T20, T21 | Adam, Floyd |

**Critical path:** T1 → T2 → T4 → T8 → T9 → T13 → T14 → T16 → T17 → T18 → T22.

## 5. Resources

- **Languages and runtime:** Python 3.10+ (developed on 3.13).
- **Libraries:** `pygame==2.6.1`, `pytest==9.0.3` (pinned in `requirements.txt`).
- **Tooling:** Git + GitHub for version control, Discord for async coordination, Google Meet for scheduled meetings, draw.io for diagrams.
- **Hardware:** developer laptops (Windows 11 primary).
- **Time budget:** approximately 120 person-hours total across the team over 9 weeks.

## 6. Plan vs actual

The plan was followed without major deviation. Two notable adjustments:

1. **Grid-based board movement was descoped at the Sprint 2 midpoint** (2026-03-18). "Move to room" became a dropdown selection rather than a tile-based walk. Recorded in `docs/decisions.md`.
2. **AI / autonomous player was descoped entirely** at the same meeting. The marking criteria places AI in the upper code band; effort was redirected into validation and the system test report.

Sprint 2 also ran one week long (planned 14 days, actual 21 days). The PO signed off on the extension at the midpoint meeting.
