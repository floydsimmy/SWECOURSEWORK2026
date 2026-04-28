# Risk Register — Team 53

Risks are scored on a 1–3 scale (1 = low, 3 = high). Score = Likelihood × Impact. Anything scoring ≥ 6 was actively monitored at sprint reviews.

| ID  | Risk                                                       | L | I | Score | Mitigation                                                                  | Status at submission |
| --- | ---------------------------------------------------------- | - | - | ----- | --------------------------------------------------------------------------- | -------------------- |
| R1  | Engine / GUI integration breaks late                       | 2 | 3 | 6     | Engine API frozen in Sprint 1; integration smoke-test on every PR           | Held; integration was clean from Sprint 2 |
| R2  | Pygame quirks on Windows                                   | 2 | 2 | 4     | Use Pygame default font; develop on Windows; SDL_VIDEODRIVER=dummy in tests | Held; no platform issues |
| R3  | Scope creep (board grid, AI, save/load)                    | 3 | 2 | 6     | PO owns backlog; stretch goals explicitly out of MVP                         | Held; descopes signed off Sprint 2 midpoint |
| R4  | Documentation gap at the end                                | 2 | 3 | 6     | DoD requires doc update each sprint; submission pack assembled progressively | Held; Sprint 4 had real polish budget |
| R5  | Team member inactive                                        | 2 | 3 | 6     | Meeting notes record attendance; tasks reassignable each sprint              | Mitigated; uneven attendance handled async via Discord |
| R6  | Tests rot as engine evolves                                 | 1 | 2 | 2     | `pytest -q` gates every merge to main                                        | Held; 100 tests green at submission |
| R7  | Marker cannot run the code                                   | 2 | 3 | 6     | One-line install (`pip install -r requirements.txt`); README spells it out  | Mitigated; instructions in `README.md` |
| R8  | Submission upload fails close to deadline                    | 2 | 3 | 6     | Adam to upload by 18:00 on 2026-04-28 — full 22-hour buffer before 4PM 30 April deadline | Mitigated; uploaded on time |
| R9  | Coursework clashes from other modules reduce attendance     | 3 | 2 | 6     | Async work via Discord; written updates accepted in lieu of meeting attendance | Held; 3 members had reduced attendance, all delivered assigned tasks |

## Risks that fired

- **R3 (scope creep)** fired mid-Sprint 2 when one team member started building grid-based movement. The PO closed it within a week and re-scoped to dropdown room selection. No code shipped. Roughly six person-hours of exploratory work did not merge.
- **R6 (tests rot)** fired once during Sprint 3 when a fix to `next_turn` broke the elimination test. Caught on the next `pytest` run before merge.
- **R9 (attendance)** fired across the project. Adam (9/9) and Floyd (9/9) attended every meeting; Maysarah (8/9), Nasser (5/9), and Abdurrahman (4/9) had clashes. Mitigation worked: every member delivered their assigned tasks despite uneven meeting attendance.

No other risk fired with material impact.
