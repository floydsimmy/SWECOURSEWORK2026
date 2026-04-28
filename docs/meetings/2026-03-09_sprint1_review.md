# Team Meeting — Sprint 1 Review

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Team number          | 53                                                     |
| Members present      | Adam, Floyd, Maysarah, Nasser                          |
| Members absent       | Abdurrahman (had a clashing deadline; sent regrets via Discord) |
| Meeting format       | Google Meet                                            |
| Date and time        | 2026-03-09, 18:00–19:00                                |
| Meeting co-ordinator | Floyd (Technical Lead this sprint)                     |

## 1) Matters to note from last meeting

- Engine API frozen and pushed to main.
- `ValueError` standard adopted across the engine.

## 2) Issues discussed at this meeting

- Demo of `pytest -q` showing the Sprint 1 unit tests passing (engine setup, deal, turn cycling).
- Demo of the Pygame window opening with the title screen, Start and Quit buttons working.
- Bug surfaced during the demo: initial deal did not skip the solution cards, so totals didn't add up. Maysarah identified the cause (drawing the solution after shuffling instead of before) and fixed it on the call.
- Sprint 2 scope. Agreed: full gameplay loop — Move, Suggest, Refute, Accuse, plus the screens to drive them.
- Adam flagged that Abdurrahman would need to expand the unit-test coverage in Sprint 2 to keep up with the new gameplay code.

## 3) Decisions agreed at this meeting

- Sprint 1 goal met. Move to Sprint 2.
- Sprint 2 technical lead: Floyd (the work is GUI-heavy, integration-focused).
- Sprint 2 priority backlog: Move/Suggest/Accuse rules and the Setup, Game, and End screens. (Action: Floyd, Nasser, Maysarah.)
- Abdurrahman to start the system test report skeleton and add unit tests for F4–F8 as code lands. (Action: Abdurrahman, async via Discord.)

## 4) Date of next meeting

2026-03-18, Sprint 2 midpoint, Google Meet.

END
