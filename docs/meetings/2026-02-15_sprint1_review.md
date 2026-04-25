# Team Meeting — Sprint 1 Review

| Field                | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Members present      | Floyd, Maysarah, Member C, Member D, Member E          |
| Meeting format       | In person                                              |
| Date and time        | 2026-02-15, 14:00-14:50                                |
| Meeting co-ordinator | Floyd (technical lead this sprint)                     |

## 1) Matters to note from last meeting

- Engine API frozen and documented (Maysarah, completed).
- ValueError as the standard exception type (adopted across engine).

## 2) Issues discussed at this meeting

- Demo of `pytest -q` — F1, F2, F3 tests passing (33 tests so far).
- Demo of Pygame window opening with title screen + Start / Quit buttons.
- Identified a subtle bug: dealing was not skipping the solution cards
  initially, so totals didn't add up. Fixed by drawing the solution
  *before* `random.shuffle` of the remainder.
- Docs status: PO has user stories, QA has draft test cases, Scrum has
  Sprint 1 start/end docs.

## 3) Decisions agreed at this meeting

- Sprint 1 goal met. Move to Sprint 2.
- Sprint 2 goal: Suggestion + Refutation + Accusation rules, plus full
  Pygame screen flow wired to the engine.
- Floyd technical lead again for Sprint 2 (GUI-heavy work).
- QA to start a system test report linked to `docs/testing/`.

## 4) Date of next meeting

2026-02-22, mid-Sprint-2 sync.

END
